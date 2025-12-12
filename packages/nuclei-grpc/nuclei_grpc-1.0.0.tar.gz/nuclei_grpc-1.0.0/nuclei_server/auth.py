# -*- coding: utf-8 -*-
import os
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional

class TokenInfo:
    def __init__(self, username: str):
        self.username = username
        self.expires_at = datetime.now() + timedelta(hours=24)

class AuthManager:
    def __init__(self):
        self.users: Dict[str, str] = {}
        self.tokens: Dict[str, TokenInfo] = {}
    
    def add_user(self, username: str, password: str):
        """Add a user with hashed password"""
        self.users[username] = self._hash_password(password)
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return token"""
        if username not in self.users:
            return None
        
        if self.users[username] != self._hash_password(password):
            return None
        
        # Generate token
        token = secrets.token_hex(32)
        self.tokens[token] = TokenInfo(username)
        
        return token
    
    def validate_token(self, token: str) -> Optional[str]:
        """Validate token and return username"""
        if token not in self.tokens:
            return None
        
        token_info = self.tokens[token]
        if datetime.now() > token_info.expires_at:
            del self.tokens[token]
            return None
        
        return token_info.username
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
