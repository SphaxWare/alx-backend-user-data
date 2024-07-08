#!/usr/bin/env python3
"""Auth Class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentification"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentification"""
        return False

    def authorization_header(self, request=None) -> str:
        """authorisation header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
