"""
Security utilities for Evolvishub Outlook Ingestor.

This module provides secure credential management, encryption utilities,
and security validation functions to protect sensitive data throughout
the application lifecycle.

Features:
- Encrypted credential storage using Fernet symmetric encryption
- Environment variable-based credential management
- Credential masking for logs and error messages
- Secure configuration validation
- Input sanitization utilities
"""

import base64
import os
import re
from typing import Any, Dict, Optional, Union
from urllib.parse import quote_plus

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecureCredentialManager:
    """Manages secure storage and retrieval of credentials."""
    
    def __init__(self, master_key: Optional[str] = None):
        """
        Initialize credential manager.
        
        Args:
            master_key: Master encryption key. If None, uses environment variable
                       OUTLOOK_INGESTOR_MASTER_KEY or generates a new one.
        """
        self._master_key = master_key or os.environ.get("OUTLOOK_INGESTOR_MASTER_KEY")
        
        if not self._master_key:
            # Generate a new master key for development
            self._master_key = base64.urlsafe_b64encode(os.urandom(32)).decode()
            
        self._fernet = self._create_fernet_cipher(self._master_key)
    
    def _create_fernet_cipher(self, master_key: str) -> Fernet:
        """Create Fernet cipher from master key."""
        # Use PBKDF2 to derive a proper key from the master key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'outlook_ingestor_salt',  # In production, use random salt
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        return Fernet(key)
    
    def encrypt_credential(self, credential: str) -> str:
        """
        Encrypt a credential.
        
        Args:
            credential: Plain text credential to encrypt
            
        Returns:
            Base64-encoded encrypted credential
        """
        if not credential:
            return ""
        
        encrypted = self._fernet.encrypt(credential.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_credential(self, encrypted_credential: str) -> str:
        """
        Decrypt a credential.
        
        Args:
            encrypted_credential: Base64-encoded encrypted credential
            
        Returns:
            Plain text credential
        """
        if not encrypted_credential:
            return ""
        
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_credential.encode())
            decrypted = self._fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception:
            # If decryption fails, assume it's already plain text (for backward compatibility)
            return encrypted_credential
    
    def get_credential_from_env(self, env_var: str, default: str = "") -> str:
        """
        Get credential from environment variable.
        
        Args:
            env_var: Environment variable name
            default: Default value if environment variable is not set
            
        Returns:
            Credential value
        """
        return os.environ.get(env_var, default)


class CredentialMasker:
    """Utility class for masking sensitive information in logs and outputs."""
    
    # Patterns for detecting sensitive information
    SENSITIVE_PATTERNS = {
        'password': re.compile(r'(password["\']?\s*[:=]\s*["\']?)([^"\'\s]+)', re.IGNORECASE),
        'secret': re.compile(r'(secret["\']?\s*[:=]\s*["\']?)([^"\'\s]+)', re.IGNORECASE),
        'token': re.compile(r'(token["\']?\s*[:=]\s*["\']?)([^"\'\s]+)', re.IGNORECASE),
        'key': re.compile(r'(["\']?(?:api_?)?key["\']?\s*[:=]\s*["\']?)([^"\'\s]+)', re.IGNORECASE),
        'dsn': re.compile(r'(://[^:]+:)([^@]+)(@)', re.IGNORECASE),
        'email': re.compile(r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', re.IGNORECASE),
    }
    
    @classmethod
    def mask_sensitive_data(cls, text: str, mask_char: str = "*") -> str:
        """
        Mask sensitive information in text.
        
        Args:
            text: Text to mask
            mask_char: Character to use for masking
            
        Returns:
            Text with sensitive information masked
        """
        if not text:
            return text
        
        masked_text = text
        
        for pattern_name, pattern in cls.SENSITIVE_PATTERNS.items():
            if pattern_name == 'dsn':
                # Special handling for database DSN
                masked_text = pattern.sub(r'\1' + mask_char * 8 + r'\3', masked_text)
            elif pattern_name == 'email':
                # Mask email addresses partially
                masked_text = pattern.sub(r'\1***@\2', masked_text)
            else:
                # Mask the sensitive value part
                masked_text = pattern.sub(r'\1' + mask_char * 8, masked_text)
        
        return masked_text
    
    @classmethod
    def mask_dict(cls, data: Dict[str, Any], mask_char: str = "*") -> Dict[str, Any]:
        """
        Mask sensitive information in dictionary.
        
        Args:
            data: Dictionary to mask
            mask_char: Character to use for masking
            
        Returns:
            Dictionary with sensitive values masked
        """
        if not isinstance(data, dict):
            return data
        
        masked_data = {}
        sensitive_keys = {
            'password', 'secret', 'token', 'key', 'api_key', 'client_secret',
            'access_token', 'refresh_token', 'private_key', 'cert', 'credential'
        }
        
        for key, value in data.items():
            if isinstance(value, dict):
                masked_data[key] = cls.mask_dict(value, mask_char)
            elif isinstance(value, str) and key.lower() in sensitive_keys:
                masked_data[key] = mask_char * min(8, len(value)) if value else value
            elif isinstance(value, str):
                masked_data[key] = cls.mask_sensitive_data(value, mask_char)
            else:
                masked_data[key] = value
        
        return masked_data


class InputSanitizer:
    """Utility class for sanitizing and validating input data."""
    
    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        re.compile(r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)", re.IGNORECASE),
        re.compile(r"(--|#|/\*|\*/)", re.IGNORECASE),
        re.compile(r"(\b(OR|AND)\s+\d+\s*=\s*\d+)", re.IGNORECASE),
        re.compile(r"(\bUNION\s+SELECT)", re.IGNORECASE),
    ]
    
    # XSS patterns
    XSS_PATTERNS = [
        re.compile(r"<script[^>]*>.*?</script>", re.IGNORECASE | re.DOTALL),
        re.compile(r"javascript:", re.IGNORECASE),
        re.compile(r"on\w+\s*=", re.IGNORECASE),
        re.compile(r"<iframe[^>]*>.*?</iframe>", re.IGNORECASE | re.DOTALL),
    ]
    
    @classmethod
    def sanitize_sql_input(cls, value: str) -> str:
        """
        Sanitize input to prevent SQL injection.
        
        Args:
            value: Input value to sanitize
            
        Returns:
            Sanitized value
        """
        if not isinstance(value, str):
            return value
        
        # Remove potentially dangerous SQL patterns
        sanitized = value
        for pattern in cls.SQL_INJECTION_PATTERNS:
            sanitized = pattern.sub("", sanitized)
        
        return sanitized.strip()
    
    @classmethod
    def sanitize_html_input(cls, value: str) -> str:
        """
        Sanitize input to prevent XSS attacks.
        
        Args:
            value: Input value to sanitize
            
        Returns:
            Sanitized value
        """
        if not isinstance(value, str):
            return value
        
        # Remove potentially dangerous HTML/JS patterns
        sanitized = value
        for pattern in cls.XSS_PATTERNS:
            sanitized = pattern.sub("", sanitized)
        
        # Escape remaining HTML entities
        sanitized = (sanitized
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace('"', "&quot;")
                    .replace("'", "&#x27;"))
        
        return sanitized
    
    @classmethod
    def validate_email_address(cls, email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(email, str):
            return False
        
        # Basic email validation pattern
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(pattern.match(email))
    
    @classmethod
    def validate_file_extension(cls, filename: str, allowed_extensions: set) -> bool:
        """
        Validate file extension against allowed list.
        
        Args:
            filename: Filename to validate
            allowed_extensions: Set of allowed extensions (e.g., {'.txt', '.pdf'})
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(filename, str):
            return False
        
        _, ext = os.path.splitext(filename.lower())
        return ext in allowed_extensions


def create_secure_dsn(
    host: str,
    port: int,
    database: str,
    username: str,
    password: str,
    driver: str = "postgresql"
) -> str:
    """
    Create a secure database DSN with properly encoded credentials.
    
    Args:
        host: Database host
        port: Database port
        database: Database name
        username: Database username
        password: Database password
        driver: Database driver name
        
    Returns:
        Secure DSN string with encoded credentials
    """
    # URL-encode the password to handle special characters
    encoded_password = quote_plus(password) if password else ""
    encoded_username = quote_plus(username) if username else ""
    
    if encoded_password:
        return f"{driver}://{encoded_username}:{encoded_password}@{host}:{port}/{database}"
    else:
        return f"{driver}://{encoded_username}@{host}:{port}/{database}"


# Global instances for easy access
_credential_manager = None
_credential_masker = CredentialMasker()
_input_sanitizer = InputSanitizer()


def get_credential_manager() -> SecureCredentialManager:
    """Get global credential manager instance."""
    global _credential_manager
    if _credential_manager is None:
        _credential_manager = SecureCredentialManager()
    return _credential_manager


def mask_sensitive_data(text: str) -> str:
    """Convenience function to mask sensitive data."""
    return _credential_masker.mask_sensitive_data(text)


def mask_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to mask sensitive data in dictionary."""
    return _credential_masker.mask_dict(data)


def sanitize_input(value: str, input_type: str = "general") -> str:
    """
    Convenience function to sanitize input.
    
    Args:
        value: Value to sanitize
        input_type: Type of input ('sql', 'html', 'general')
        
    Returns:
        Sanitized value
    """
    if input_type == "sql":
        return _input_sanitizer.sanitize_sql_input(value)
    elif input_type == "html":
        return _input_sanitizer.sanitize_html_input(value)
    else:
        # General sanitization
        return _input_sanitizer.sanitize_html_input(
            _input_sanitizer.sanitize_sql_input(value)
        )
