#!/usr/bin/env python3
"""Auth Class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentification"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentification"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif excluded_path.endswith('/') and path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """authorisation header"""
        if request is None:
            return None
        auth_header = request.headers.get('Authorization', None)
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None

        SESSION_NAME = getenv("SESSION_NAME")

        if SESSION_NAME is None:
            return None

        session_id = request.cookies.get(SESSION_NAME)

        return session_id
