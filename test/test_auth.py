from fastapi import Request
from starlette.responses import Response
from unittest.mock import AsyncMock, MagicMock
import unittest
from src.geo_api.auth import AuthMiddleware


class TestAuthMiddleware(unittest.TestCase):
    async def test_jump_paths_processed_without_authentication(self):
        middleware = AuthMiddleware(None)
        request = MagicMock(spec=Request)
        request.url.path = '/docs'
        call_next = AsyncMock(return_value=Response())

        response = await middleware.dispatch(request, call_next)

        call_next.assert_called_once_with(request)
        self.assertEqual(response.status_code, 200)
