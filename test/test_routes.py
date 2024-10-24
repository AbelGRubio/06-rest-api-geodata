import unittest
from unittest.mock import patch, Mock, MagicMock

from fastapi.testclient import TestClient

from src.app.configuration import DATABASE, LOGGER
from src.app.models import ApiUser
from src.app.routes.api_routes import api_router, close_db
from src.app.routes.v1_routes import (v1_router, adding_user, user_listing,
                                      updating_user, delete_user)
from app.models.schemas import ShowUserSchema, UserSchema


class TestRoutes(unittest.TestCase):
    def test_health_status_code(self):
        client = TestClient(api_router)
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)

    def test_close_database(self):
        with patch.object(DATABASE, 'is_closed',
                          return_value=False) as mock_is_closed, \
                patch.object(DATABASE, 'close') as mock_close:
            close_db()
            mock_is_closed.assert_called_once()
            mock_close.assert_called_once()

    def test_add_user(self):
        client = TestClient(v1_router)

        user_data = {
            "name": "John Doe",
            "postal_code": "12345",
            "city": "Sample City"
        }

        with patch('src.app.routes.v1_routes.add_user',
                   return_value="Added user 1:John Doe to database."):
            response = client.post('/user', json=user_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {"msg": "Added user 1:John Doe to database."})

    def test_retrieve_users_successfully(self):
        mocker = Mock()
        mock_users = [
            ApiUser(id=1, name="John Doe", city='12345', postal_code="12345"),
            ApiUser(id=2, name="Jane Doe", city='67890', postal_code="67890")
        ]

        with patch('src.app.routes.v1_routes.ApiUser.select',
                   return_value=mock_users):
            response = user_listing()
            expected_response = [ShowUserSchema.model_validate(user)
                                 for user in mock_users]

            self.assertEqual(response, expected_response)
    def test_log_error_message_on_exception(self):
        user_parameter = UserSchema(name="test_user", email="test@example.com")

        with patch('src.app.routes.v1_routes.add_user',
                   side_effect=Exception("Test Exception")):
            with patch.object(LOGGER, 'error') as mock_logger_error:
                response = adding_user(user_parameter)
                mock_logger_error.assert_called_once_with(
                    "There was a problem. msg Test Exception")
                self.assertEqual(response.status_code, 404)

    def test_listing_users(self):
        mock_users = [
            ApiUser(id=1, name="John Doe", city='12345', postal_code="12345"),
            ApiUser(id=2, name="Jane Doe", city='67890', postal_code="67890")
        ]

        with patch('src.app.routes.v1_routes.ApiUser.select',
                   return_value=mock_users):
            users_ = ApiUser.select()
            result = [ShowUserSchema.from_orm(usr_) for usr_ in users_]
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0].name, "John Doe")
            self.assertEqual(result[1].name, "Jane Doe")

    def test_successfully_updates_user_with_valid_data(self):
        user_id = "123"
        user_update = UserSchema(name="New Name", city="New City", postal_code="12345")

        mock_user = ApiUser(id=user_id, name="John Doe", city='12345', postal_code="12345")

        with patch('src.app.routes.v1_routes.ApiUser.get_or_none', return_value=mock_user):
            with patch('src.app.routes.v1_routes.update_user', return_value=mock_user):
                response = updating_user(user_id, user_update)
                self.assertEqual(response.name, "John Doe")
                self.assertEqual(response.city, "12345")
                self.assertEqual(response.postal_code, "12345")

    def test_user_deleted_successfully(self):

        user_id = 1

        with patch('src.app.routes.v1_routes.ApiUser.get_or_none') as mock_get_or_none:
            mock_user = MagicMock()
            mock_get_or_none.return_value = mock_user

            response = delete_user(user_id)

            mock_user.delete_instance.assert_called_once()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.body, b'"User deleted"')