# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from web.businesses.api.views import *
from web.businesses.api.viewsets import GrownStrainViewSet

router = DefaultRouter()
router.register(r'grown-strain', GrownStrainViewSet, base_name='grown_strain')

urlpatterns = [
    url(
        regex=r'^(?P<business_id>[0-9]+)/image',
        view=BusinessImageView.as_view(),
        name='upload_business_image'
    ),
    url(
        regex=r'^location/lookup/$',
        view=LocationLookupView.as_view(),
        name='location_lookup'
    ),
    url(
        regex=r'^(?P<business_id>[0-9]+)/locations/(?P<business_location_id>[0-9]+)/menu$',
        view=BusinessLocationMenuView.as_view(),
        name='business_location_menu'
    ),
    url(
        regex=r'^(?P<business_id>[0-9]+)/locations/(?P<business_location_id>[0-9]+)/',
        view=include(router.urls, namespace='business_location')
    ),
    url(
        regex=r'^(?P<business_id>[0-9]+)/locations/(?P<business_location_id>[0-9]+)/image$',
        view=BusinessLocationImageView.as_view(),
        name='business_location_image'
    ),
    url(
        regex=r'^(?P<business_id>[0-9]+)/locations/(?P<business_location_id>[0-9]+)/reviews$',
        view=BusinessLocationReviewView.as_view(),
        name='business_location_reviews'
    ),
    url(
        regex=r'^(?P<business_id>[0-9]+)/locations/(?P<business_location_id>[0-9]+)/favorite$',
        view=BusinessLocationFavoriteView.as_view(),
        name='business_location_favorite'
    ),
    url(
        regex=r'^(?P<business_id>[0-9]+)/locations/(?P<business_location_id>[0-9]+)/partnerships/(?P<partnership_id>[0-9]+)$',
        view=GrowerDispensaryPartnershipDetailView.as_view(),
        name='grower_dispensary_partnerships_detail'
    ),
    url(
        regex=r'^(?P<business_id>[0-9]+)/locations/(?P<business_location_id>[0-9]+)/partnerships$',
        view=GrowerDispensaryPartnershipListView.as_view(),
        name='grower_dispensary_partnerships_list'
    ),
    url(
        regex=r'^(?P<business_id>[0-9]+)/locations/(?P<business_location_id>[0-9]+)/menu-update-requests$',
        view=BusinessLocationMenuUpdateRequestDetailView.as_view(),
        name='business_location_menu_update_detail'
    ),
    url(
        regex=r'^(?P<business_id>[0-9]+)/menu_item/(?P<menu_item_id>[0-9]+)/report-out-of-stock$',
        view=BusinessLocationReportOutOfStockView.as_view(),
        name='business_location_report_out_of_stock'
    ),
    url(
        regex=r'^(?P<business_id>[0-9]+)/locations/(?P<business_location_id>[0-9]+)$',
        view=BusinessLocationView.as_view(),
        name='business_location'
    ),
    url(
        regex=r'^locations/featured/$',
        view=FeaturedBusinessLocationsView.as_view(),
        name='business_locations_featured'
    ),
    url(
        regex=r'^(?P<state_abbreviation>.+)/(?P<city_slug>.+)/$',
        view=BusinessLocationsPerCityView.as_view(),
        name='business_locations_per_city'
    ),
    url(
        regex=r'^signup',
        view=BusinessSignUpWizardView.as_view(),
        name='signup'
    ),
    url(
        regex=r'^resend-email-confirmation',
        view=ResendConfirmationEmailView.as_view(),
        name='resend_email_confirmation'
    ),
]
