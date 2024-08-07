#!/usr/bin/env python3
"""Auth.py"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    takes in a password string arguments
    and returns bytes
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def _generate_uuid() -> str:
    """Generate a new UUID."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
         take mandatory email and password string arguments
         and return a User object.
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            user = db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        expect email and password required arguments and return a boolean
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
            return bcrypt.checkpw(
                                  password.encode('utf-8'),
                                  user.hashed_password
                                  )
        except NoResultFound:
            return False
        except Exception as e:
            return False

    def create_session(self, email: str) -> str:
        """create session and return id"""
        db = self._db
        try:
            user = db.find_user_by(email=email)
            session_id = _generate_uuid()
            db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        akes a single session_id string argument and returns
        the corresponding User or None
        """
        if session_id is None:
            return None
        db = self._db
        try:
            user = db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """destroy user session"""
        db = self._db
        if user_id is None:
            return None
        # set session_id for user to None
        db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        take an email string argument and returns a string.
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
            reset_token = _generate_uuid()
            db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError(f"User {email} does not exist")

    def update_password(self, reset_token: str, password: str) -> None:
        """reset token to find user and change password"""
        db = self._db
        try:
            user = db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError(f"User with {reset_token} doesnt exit")
        hashed_password = _hash_password(password)
        db.update_user(user.id,
                       hashed_password=hashed_password,
                       reset_token=None
                       )
