from web.search.api.serializers import StrainDetailSerializer, StrainRatingSerializer
from web.search.es_service import SearchElasticService
from web.search.models import UserSearch, Strain, StrainImage, StrainReview, StrainRating, UserFavoriteStrain
from web.search.services import build_strain_rating


class StrainDetailsService:
    def build_strain_details(self, strain_id, current_user):
        strain = Strain.objects.get(pk=strain_id)
        image = StrainImage.objects.filter(strain=strain)[:1]
        strain_origins = self.get_strain_origins(strain)
        rating = build_strain_rating(strain)
        strain_srx_score = self.calculate_srx_score(strain, current_user)
        reviews = self.get_strain_reviews(strain)
        strain_review = StrainRating.objects.filter(strain=strain, created_by=current_user, removed_date=None)
        favorite = UserFavoriteStrain.objects.filter(strain=strain, created_by=current_user).exists()
        is_rated = StrainReview.objects.filter(strain=strain, created_by=current_user).exists()

        return {
            'strain': StrainDetailSerializer(strain).data,
            'strain_image': image[0].image.url if image else None,
            'strain_origins': strain_origins,
            'strain_rating': rating,
            'user_strain_review': StrainRatingSerializer(strain_review[0]).data if len(strain_review) > 0 else None,
            'strain_reviews': reviews,
            'strain_srx_score': strain_srx_score,
            'favorite': favorite,
            'is_rated': is_rated
        }

    @staticmethod
    def get_strain_origins(current_strain):
        strain_origins = []
        for o in current_strain.origins.all()[:5]:
            strain_origins.append(StrainDetailSerializer(o).data)
        return strain_origins

    @staticmethod
    def get_also_like_strains(current_strain, current_user):
        latest_user_search = UserSearch.objects.filter(user=current_user).order_by('-last_modified_date')[:1]
        also_like_strains = []

        if latest_user_search and len(latest_user_search) > 0:
            data = SearchElasticService().query_strain_srx_score(latest_user_search[0].to_search_criteria(), 2000, 0,
                                                                 include_locations=False, is_similar=True,
                                                                 similar_strain_id=current_strain.id)

            start_index = 0
            initial = 0
            for index, s in enumerate(data.get('list')):
                if s.get('id') == current_strain.id:
                    start_index = index + 1
                    initial = index + 1

                if index + 1 != start_index and 0 < start_index < initial + 5:
                    also_like_strains.append(s)
                    start_index += 1

                if start_index == initial + 5:
                    break

        if len(also_like_strains) == 0:
            search_criteria = current_strain.to_search_criteria()
            search_criteria['strain_types'] = 'skipped'
            data = SearchElasticService().query_strain_srx_score(search_criteria, 6, 0, include_locations=False)
            for s in data.get('list')[1:]:
                also_like_strains.append(s)

        return also_like_strains

    @staticmethod
    def calculate_srx_score(current_strain, current_user):
        latest_user_search = UserSearch.objects.filter(user=current_user).order_by('-last_modified_date')[:1]

        if latest_user_search and len(latest_user_search) > 0:
            if StrainRating.objects.filter(strain=current_strain, created_by=current_user,
                                           removed_date=None).exists():
                score = SearchElasticService().query_user_review_srx_score(latest_user_search[0].to_search_criteria(),
                                                                           strain_id=current_strain.id,
                                                                           user_id=current_user.id)
                return score
            else:
                data = SearchElasticService().query_strain_srx_score(latest_user_search[0].to_search_criteria(),
                                                                     strain_id=current_strain.id)
                strain = data.get('list')[0]
                return strain.get('match_percentage')

        return 0

    def get_strain_reviews(self, current_strain):
        reviews_raw = StrainReview.objects.filter(strain=current_strain,
                                                  review_approved=True).order_by('-created_date')[:3]
        reviews = []
        for r in reviews_raw:
            reviews.append(self.build_review(r))
        return reviews

    def get_all_approved_strain_reviews(self, strain_id):
        reviews_raw = StrainReview.objects.filter(strain__id=strain_id,
                                                  review_approved=True).order_by('-created_date')
        reviews = []
        for r in reviews_raw:
            reviews.append(self.build_review(r))
        return reviews

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

    @staticmethod
    def build_strain_locations(strain_id, current_user, result_filter=None, order_field=None, order_dir=None):
        service = SearchElasticService()
        es_response = service.get_locations(strain_id=strain_id, current_user=current_user, result_filter=result_filter,
                                            order_field=order_field, order_dir=order_dir)
        locations = service.transform_location_results(es_response, strain_id=strain_id, result_filter=result_filter)
        return {'locations': locations}
