import datetime
import unittest
from unittest import mock
from unittest.mock import patch

import requests

from src.geo_api.configuration import API_GEO_URL
from src.geo_api.functions import add_user, ApiUser, UserSchema, \
    check_response_geojson
from src.geo_api.functions import get_direction_from_response, update_user


class TestFunctions(unittest.TestCase):
    def test_returns_place_name_when_full_dir_is_false(self):
        response_mock = mock.Mock()
        response_mock.json.return_value = {
            'postalCodes': [
                {'placeName': 'TestCity', 'adminName1': 'TestAdmin',
                 'countryCode': 'TC'}]
        }
        result = get_direction_from_response(response=response_mock,
                                             full_dir=False)
        self.assertEqual(result, 'TestCity')

    def test_add_user_with_known_city(self):

        user = UserSchema(name='John Doe', city='New York', postal_code='10001')
        result = add_user(user)

        res_ = result == 'The user already exists!' or 'Added user ' in result

        self.assertTrue(res_)

        exist_user = ApiUser.get_or_none(**user.model_dump())
        
        name_ = str(datetime.datetime.now())
        
        user_update = UserSchema(name=name_, city='45ee6',
                                 postal_code="ABC")

        # Call the function to update the user
        updated_user = update_user(exist_user, user_update)
        self.assertEqual(updated_user.name, name_)
        self.assertEqual(updated_user.postal_code, "ABC")

    @patch('requests.get')
    def test_update_city_with_valid_response(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = {'postalCodes': [
            {'placeName': 'TestCity', 'adminName1':
                'TestAdmin', 'countryCode': 'TC'}]}
        mock_get.return_value = mock_response

        user = UserSchema(name='TestUser', postal_code='12345', city='-')
        response = requests.get(API_GEO_URL.format(user.postal_code))

        if check_response_geojson(response):
            user.city = get_direction_from_response(response=response)

        assert user.city == 'TestCity'

    def test_get_direction_from_response(self):
        res = get_direction_from_response(None)
        self.assertEqual(res,' ')
