#!/usr/bin/env python3
"""BasicAuth Class"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """Basic Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """
        returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        encoded = authorization_header.split(' ', 1)[1]
        return encoded

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, ValueError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        returns the user email and password from the
        Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email_pwd = decoded_base64_authorization_header.split(':')
        email = email_pwd[0]
        pwd = email_pwd[1]
        return (email, pwd)

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
        returns the User instance based on his
        email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        encoded = self.extract_base64_authorization_header(auth_header)
        if not encoded:
            return None
        decoded = self.decode_base64_authorization_header(encoded)
        if not decoded:
            return None
        email, pwd = self.extract_user_credentials(decoded)
        if not email or not pwd:
            return None
        user = self.user_object_from_credentials(email, pwd)
        return user
