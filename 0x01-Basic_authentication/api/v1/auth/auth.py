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
        if excluded_paths is None len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """authorisation header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
