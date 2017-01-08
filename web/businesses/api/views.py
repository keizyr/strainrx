# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from boto.s3.connection import S3Connection, Bucket, Key
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from web.businesses.api.permissions import BusinessAccountOwner
from web.businesses.api.serializers import *
from web.businesses.api.services import BusinessSignUpService, BusinessLocationService, get_open_closed, \
    get_location_rating
from web.businesses.emails import EmailService
from web.businesses.models import Business, BusinessLocation, BusinessLocationMenuItem, LocationReview, \
    UserFavoriteLocation
from web.businesses.serializers import BusinessSerializer, BusinessLocationSerializer
from web.search.api.services import StrainDetailsService
from web.search.models import Strain

logger = logging.getLogger(__name__)


def bad_request(error_message):
    return Response({
        'error': error_message
    }, status=status.HTTP_400_BAD_REQUEST)


class BusinessSignUpWizardView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = BusinessSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            business = BusinessSignUpService().enroll_new_business(data=serializer.validated_data)
        except ValidationError as e:
            return bad_request(e.message)

        try:
            EmailService().send_confirmation_email(business.created_by)
        except Exception:
            logger.exception('Cannot send an email to {0}'.format(business.created_by.email))

        authenticated = authenticate(username=business.created_by.email, password=serializer.validated_data.get('pwd'))
        if authenticated is None:
            return bad_request('Cannot authenticate user')

        login(request, authenticated)

        serializer = BusinessSerializer(business)
        request.session['business'] = serializer.data

        return Response({
            'business_id': business.pk
        }, status=status.HTTP_200_OK)


class BusinessImageView(LoginRequiredMixin, APIView):
    permission_classes = (BusinessAccountOwner,)

    def post(self, request, business_id):
        business = Business.objects.get(pk=business_id)

        if business.image and business.image.url:
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            bucket = Bucket(conn, settings.AWS_STORAGE_BUCKET_NAME)
            k = Key(bucket=bucket, name=business.image.url.split(bucket.name)[1])
            k.delete()

        file = request.FILES.get('file')
        business.image = file
        business.save()

        request.session['business_image'] = business.image.url if business.image and business.image.url else None

        return Response({}, status=status.HTTP_200_OK)


class BusinessLocationImageView(LoginRequiredMixin, APIView):
    permission_classes = (BusinessAccountOwner,)

    def post(self, request, business_id, business_location_id):
        location = BusinessLocation.objects.get(pk=business_location_id)

        if location.image and location.image.url:
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            bucket = Bucket(conn, settings.AWS_STORAGE_BUCKET_NAME)
            k = Key(bucket=bucket, name=location.image.url.split(bucket.name)[1])
            k.delete()

        file = request.FILES.get('file')
        location.image = file
        location.save()

        if location.primary:
            request.session['business_image'] = location.image.url

        return Response({}, status=status.HTTP_200_OK)


class BusinessLocationReviewView(LoginRequiredMixin, APIView):
    def get(self, request, business_id, business_location_id):
        reviews_raw = LocationReview.objects.filter(location__id=business_location_id,
                                                    review_approved=True).order_by('-created_date')
        reviews = []
        for r in reviews_raw:
            reviews.append(self.build_review(r))
        return Response({'reviews': reviews}, status=status.HTTP_200_OK)

    @staticmethod
    def build_review(review):
        display_user_name = '{0} {1}'.format(review.created_by.first_name, review.created_by.last_name) \
            if review.created_by.first_name and review.created_by.last_name \
            else review.created_by.email.split('@')[0]

        return {
            'id': review.id,
            'rating': review.rating,
            'review': review.review,
            'created_date': review.created_date,
            'created_by_name': display_user_name,
            'created_by_image': None  # TODO implement UserImage
        }

    def post(self, request, business_id, business_location_id):
        location = BusinessLocation.objects.get(pk=business_location_id)
        serializer = LocationReviewFormSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review_text = serializer.validated_data.get('review')
        is_approved = False if review_text and len(review_text) > 0 else True
        review = LocationReview(location=location, created_by=request.user,
                                rating=serializer.validated_data.get('rating'),
                                review=review_text, review_approved=is_approved)
        review.save()
        return Response({}, status=status.HTTP_200_OK)


class BusinessLocationFavoriteView(LoginRequiredMixin, APIView):
    def post(self, request, business_id, business_location_id):
        add_to_favorites = request.data.get('like')
        favorite_location = UserFavoriteLocation.objects.filter(location__id=business_location_id,
                                                                created_by=request.user)

        if add_to_favorites and len(favorite_location) == 0:
            favorite_location = UserFavoriteLocation(
                location=BusinessLocation.objects.get(id=business_location_id),
                created_by=request.user
            )
            favorite_location.save()
        elif len(favorite_location) > 0:
            favorite_location[0].delete()

        return Response({}, status=status.HTTP_200_OK)


class ResendConfirmationEmailView(LoginRequiredMixin, APIView):
    def get(self, request):
        authenticated_user = request.user
        EmailService().send_confirmation_email(authenticated_user)
        return Response({}, status=status.HTTP_200_OK)


class BusinessLocationView(LoginRequiredMixin, APIView):
    permission_classes = (BusinessAccountOwner,)

    def get(self, request, business_id, business_location_id):
        if business_location_id == '0':
            locations_raw = BusinessLocation.objects.filter(business__id=business_id, removed_date=None).order_by('id')
            locations = []

            for l in locations_raw:
                serializer = BusinessLocationSerializer(l)
                locations.append(serializer.data)

            return Response({'locations': locations}, status=status.HTTP_200_OK)

        location = BusinessLocation.objects.get(pk=business_location_id)
        serializer = BusinessLocationSerializer(location)
        d = {'location': serializer.data}

        if request.GET.get('ddp'):
            current_user = request.user
            open_closed = get_open_closed(serializer.data, '%I:%M %p')
            d['location']['is_favorite'] = UserFavoriteLocation.objects.filter(created_by=current_user).exists()
            d['location']['is_rated'] = LocationReview.objects.filter(created_by=current_user).exists()
            d['location']['rating'] = get_location_rating(business_location_id)
            d['location']['is_open'] = open_closed == 'Opened'
            d['location']['open_closed'] = open_closed

        return Response(d, status=status.HTTP_200_OK)

    def post(self, request, business_id, business_location_id):
        existing_location = BusinessLocation.objects.get(pk=business_location_id)
        serializer = BusinessLocationDetailSerializer(existing_location, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(existing_location, serializer.validated_data)
        return Response({}, status=status.HTTP_200_OK)

    def put(self, request, business_id, business_location_id):
        serializer = BusinessLocationSerializer(data=request.data.get('location'))
        serializer.is_valid(raise_exception=True)

        if int(business_location_id) > 0:
            location = BusinessLocationService().update_location(business_location_id, serializer.validated_data)
        else:
            location = BusinessLocationService().create_location(business_id, serializer.validated_data)

        return Response({
            'location': BusinessLocationSerializer(location).data,
            'image_key': request.data.get('image_key')
        }, status=status.HTTP_200_OK)

    def delete(self, request, business_id, business_location_id):
        BusinessLocationService().remove_location(business_location_id, request.user.id)
        return Response({}, status=status.HTTP_200_OK)


class BusinessLocationMenuView(LoginRequiredMixin, APIView):
    permission_classes = (BusinessAccountOwner,)

    def get(self, request, business_id, business_location_id):
        menu_items_raw = BusinessLocationMenuItem.objects \
            .filter(business_location__id=business_location_id, removed_date=None) \
            .order_by('strain__name')

        menu_items = []
        for mi in menu_items_raw:
            menu_items.append(self.build_menu_item(mi))

        if request.GET.get('ddp'):
            strain_ids = []
            for mi in menu_items:
                strain_ids.append(mi.get('strain_id'))

            scores = StrainDetailsService().calculate_srx_scores(strain_ids, request.user)
            if len(scores) > 0:
                for mi in menu_items:
                    mi['match_score'] = scores.get(mi.get('strain_id'))

        return Response({'menu': menu_items}, status=status.HTTP_200_OK)

    def post(self, request, business_id, business_location_id):
        serializer = BusinessLocationMenuItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        strain = Strain.objects.get(pk=data.get('strain_id'))
        location = BusinessLocation.objects.get(pk=business_location_id)

        try:
            menu_item = BusinessLocationMenuItem.objects.get(business_location=location, strain=strain)
            menu_item.in_stock = data.get('in_stock')
            menu_item.price_gram = data.get('price_gram')
            menu_item.price_eighth = data.get('price_eighth')
            menu_item.price_quarter = data.get('price_quarter')
            menu_item.price_half = data.get('price_half')
            menu_item.removed_date = None
        except BusinessLocationMenuItem.DoesNotExist:
            menu_item = BusinessLocationMenuItem(business_location=location, strain=strain,
                                                 price_gram=data.get('price_gram'),
                                                 price_eighth=data.get('price_eighth'),
                                                 price_quarter=data.get('price_quarter'),
                                                 price_half=data.get('price_half'))

        menu_item.save()

        return Response(self.build_menu_item(menu_item), status=status.HTTP_200_OK)

    def put(self, request, business_id, business_location_id):
        menu_item = request.data.get('menu_item')
        item = BusinessLocationMenuItem.objects.get(pk=menu_item.get('id'))
        item.in_stock = menu_item.get('in_stock')
        item.save()
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, business_id, business_location_id):
        menu_item_id = request.data.get('menu_item_id')
        item = BusinessLocationMenuItem.objects.get(pk=menu_item_id)
        item.removed_date = datetime.now()
        item.save()
        return Response({}, status=status.HTTP_200_OK)

    def build_menu_item(self, menu_item):
        return {
            'id': menu_item.id,
            'strain_id': menu_item.strain.id,
            'strain_name': menu_item.strain.name,
            'strain_variety': menu_item.strain.variety,
            'price_gram': menu_item.price_gram,
            'price_eighth': menu_item.price_eighth,
            'price_quarter': menu_item.price_quarter,
            'price_half': menu_item.price_half,
            'in_stock': menu_item.in_stock
        }
