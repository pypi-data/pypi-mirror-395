"""
Integration tests for kinglet.validation module

These tests involve complex validation logic and actual validation scenarios
that require real data validation rather than mocking.
"""

import pytest
from datetime import datetime

from kinglet.validation import (
    EmailValidator, LengthValidator, PasswordValidator, ChoicesValidator,
    ValidationSchema, ValidationRule, RequiredValidator,
    USER_REGISTRATION_SCHEMA, USER_LOGIN_SCHEMA, LISTING_CREATION_SCHEMA,
    validate_password
)


class TestValidationIntegration:
    """Integration tests for complex validation scenarios"""

    def test_email_validation_integration(self):
        """Test email validator with real scenarios"""
        validator = EmailValidator()
        
        # Valid emails should pass
        assert validator.validate("user@example.com") is True
        assert validator.validate("test.user+tag@domain.co.uk") is True
        
        # Empty string should fail (this was failing in unit tests)
        assert validator.validate("") is False
        assert validator.validate("not-an-email") is False

    def test_length_validation_integration(self):
        """Test length validator with real data"""
        validator = LengthValidator(min_length=3, max_length=10)
        
        # Valid lengths
        assert validator.validate("abc") is True
        assert validator.validate("abcdef") is True
        
        # Empty string with min_length should fail
        assert validator.validate("") is False
        assert validator.validate("ab") is False  # Too short
        assert validator.validate("abcdefghijk") is False  # Too long

    def test_password_validation_integration(self):
        """Test password validator with real password scenarios"""
        validator = PasswordValidator()
        
        # Valid passwords with uppercase, lowercase, digit, special char
        assert validator.validate("Password123!") is True
        assert validator.validate("MyStr0ng@Pass") is True
        
        # These should fail (were failing in unit tests)
        assert validator.validate("password123") is False  # No uppercase, no special
        assert validator.validate("PASSWORD123") is False  # No lowercase, no special
        assert validator.validate("Password") is False      # No digit, no special
        assert validator.validate("Pass1!") is False       # Too short

    def test_choices_validation_integration(self):
        """Test choices validator with real choice scenarios"""
        validator = ChoicesValidator(["red", "green", "blue"])
        
        # Valid choices
        assert validator.validate("red") is True
        assert validator.validate("green") is True
        
        # Invalid choices
        assert validator.validate("yellow") is False
        assert validator.validate("") is False

    def test_validation_schema_integration(self):
        """Test validation schema with real form data"""
        schema = ValidationSchema({
            "name": [RequiredValidator()],
            "email": [RequiredValidator(), EmailValidator()],
            "age": [RequiredValidator(), LengthValidator(min_length=1, max_length=3)],
        })
        
        # Valid data
        valid_data = {
            "name": "John Doe",
            "email": "john@example.com", 
            "age": "25"
        }
        result = schema.validate(valid_data)
        assert result.is_valid is True
        assert result.errors == {}
        
        # Invalid data
        invalid_data = {
            "name": "",  # Required but empty
            "email": "not-an-email",  # Invalid format
            "age": "1000"  # Too long
        }
        result = schema.validate(invalid_data)
        assert result.is_valid is False
        assert "name" in result.errors
        assert "email" in result.errors
        assert "age" in result.errors

    def test_user_registration_schema_integration(self):
        """Test predefined user registration schema with real data"""
        # Valid registration data
        valid_data = {
            "username": "johndoe",
            "email": "john@example.com",
            "password": "MyStr0ng@Pass",
            "name": "John Doe"
        }
        result = USER_REGISTRATION_SCHEMA.validate(valid_data)
        assert result.is_valid is True
        
        # Invalid registration data (missing required fields)
        invalid_data = {
            "username": "johndoe",
            "password": "weak"  # Doesn't meet password requirements
        }
        result = USER_REGISTRATION_SCHEMA.validate(invalid_data)
        assert result.is_valid is False
        assert "email" in result.errors  # Missing required field
        assert "name" in result.errors   # Missing required field
        assert "password" in result.errors  # Weak password

    def test_user_login_schema_integration(self):
        """Test predefined user login schema with real data"""
        # Valid login data
        valid_data = {
            "email": "user@example.com",
            "password": "anypassword"
        }
        result = USER_LOGIN_SCHEMA.validate(valid_data)
        assert result.is_valid is True
        
        # Invalid login data (missing email)
        invalid_data = {
            "password": "somepassword"
        }
        result = USER_LOGIN_SCHEMA.validate(invalid_data)
        assert result.is_valid is False
        assert "email" in result.errors

    def test_listing_creation_schema_integration(self):
        """Test predefined listing creation schema with real data"""
        # Valid listing data
        valid_data = {
            "title": "Beautiful Apartment",
            "description": "A lovely place to stay",
            "price_per_day": "100.00",
            "location": "New York, NY", 
            "type": "caravan"  # Must match the predefined choices
        }
        result = LISTING_CREATION_SCHEMA.validate(valid_data)
        assert result.is_valid is True
        
        # Invalid listing data (missing required fields)
        invalid_data = {
            "title": "Apartment",
            "description": "Nice place"
        }
        result = LISTING_CREATION_SCHEMA.validate(invalid_data)
        assert result.is_valid is False
        assert "price_per_day" in result.errors
        assert "location" in result.errors
        assert "type" in result.errors

    def test_password_utility_function_integration(self):
        """Test validate_password utility function with real passwords"""
        # Valid passwords - returns tuple (is_valid, message)
        is_valid, msg = validate_password("MyStr0ng@Pass")
        assert is_valid is True
        
        is_valid, msg = validate_password("Anoth3r!Good1")
        assert is_valid is True
        
        # Invalid passwords
        is_valid, msg = validate_password("password123")
        assert is_valid is False  # No uppercase, no special
        
        is_valid, msg = validate_password("short")
        assert is_valid is False  # Too short
        
        is_valid, msg = validate_password("")
        assert is_valid is False  # Empty