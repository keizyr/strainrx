import json

from web.es_service import BaseElasticService
from web.search import es_mappings
from web.search.serializers import StrainESSerializer


class StrainESService(BaseElasticService):
    def get_strain_by_db_id(self, db_strain_id):
        url = '{base}{index}/{type}/_search'.format(base=self.BASE_ELASTIC_URL,
                                                    index=self.URLS.get('STRAIN'),
                                                    type=es_mappings.TYPES.get('strain'))
        query = {
            "query": {
                "match": {
                    "id": db_strain_id
                }
            }
        }

        es_response = self._request(self.METHODS.get('POST'), url, data=json.dumps(query))
        return es_response

    def get_strain_review_by_db_id(self, db_strain_review_id):
        url = '{base}{index}/{type}/_search'.format(base=self.BASE_ELASTIC_URL,
                                                    index=self.URLS.get('STRAIN'),
                                                    type=es_mappings.TYPES.get('strain_review'))
        query = {
            "query": {
                "match": {
                    "id": db_strain_review_id
                }
            }
        }

        es_response = self._request(self.METHODS.get('POST'), url, data=json.dumps(query))
        return es_response

    def save_strain_review(self, data, review_db_id, parent_strain_db_id):
        es_response = self.get_strain_review_by_db_id(review_db_id)
        es_review = es_response.get('hits', {}).get('hits', [])
        es_response = self.get_strain_by_db_id(parent_strain_db_id)
        es_strain = es_response.get('hits', {}).get('hits', [])

        if len(es_review) > 0:
            url = '{base}{index}/{type}/{es_id}?parent={parent}'.format(base=self.BASE_ELASTIC_URL,
                                                                        index=self.URLS.get('STRAIN'),
                                                                        type=es_mappings.TYPES.get('strain_review'),
                                                                        es_id=es_review[0].get('_id'),
                                                                        parent=es_strain[0].get('_id'))
            es_response = self._request(self.METHODS.get('PUT'), url, data=json.dumps(data))
        else:
            url = '{base}{index}/{type}?parent={parent}'.format(base=self.BASE_ELASTIC_URL,
                                                                index=self.URLS.get('STRAIN'),
                                                                type=es_mappings.TYPES.get('strain_review'),
                                                                parent=es_strain[0].get('_id'))
            es_response = self._request(self.METHODS.get('POST'), url, data=json.dumps(data))

        return es_response

    def save_strain(self, strain):
        es_response = self.get_strain_by_db_id(strain.id)
        es_strains = es_response.get('hits', {}).get('hits', [])
        es_serializer = StrainESSerializer(instance=strain)
        data = es_serializer.data

        if len(es_strains) > 0:
            es_strain = es_strains[0]
            es_strain_source = es_strain.get('_source')
            es_strain_source.update(data)

            url = '{base}{index}/{type}/{es_id}'.format(base=self.BASE_ELASTIC_URL, index=self.URLS.get('STRAIN'),
                                                        type=es_mappings.TYPES.get('strain'),
                                                        es_id=es_strain.get('_id'))
            print('--- updating')
            print(es_strain_source['removed_date'], strain.name)
            es_response = self._request(self.METHODS.get('PUT'), url, data=json.dumps(es_strain_source))
        else:
            data['removed_by_id'] = data.get('removed_by')
            data.pop('removed_by', None)

            url = '{base}{index}/{type}'.format(base=self.BASE_ELASTIC_URL, index=self.URLS.get('STRAIN'),
                                                type=es_mappings.TYPES.get('strain'))
            es_response = self._request(self.METHODS.get('POST'), url, data=json.dumps(data))

        return es_response

    def delete_strain(self, strain_id):
        es_response = self.get_strain_by_db_id(strain_id)
        es_strains = es_response.get('hits', {}).get('hits', [])

        if len(es_strains) > 0:
            es_strain = es_strains[0]
            url = '{base}{index}/{type}/{es_id}'.format(base=self.BASE_ELASTIC_URL, index=self.URLS.get('STRAIN'),
                                                        type=es_mappings.TYPES.get('strain'),
                                                        es_id=es_strain.get('_id'))
            es_response = self._request(self.METHODS.get('DELETE'), url)
            return es_response
