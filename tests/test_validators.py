"""
Unit tests for validation utilities
"""
import unittest
from utils.validators import (
    validate_email, validate_password, validate_price,
    validate_date, validate_phone, validate_name,
    validate_quantity
)

class TestValidators(unittest.TestCase):
    
    def test_validate_email(self):
        """Test email validation"""
        # Valid emails
        self.assertTrue(validate_email("test@example.com")[0])
        self.assertTrue(validate_email("user.name@domain.co.uk")[0])
        
        # Invalid emails
        self.assertFalse(validate_email("invalid")[0])
        self.assertFalse(validate_email("invalid@")[0])
        self.assertFalse(validate_email("@domain.com")[0])
        self.assertFalse(validate_email("")[0])
    
    def test_validate_password(self):
        """Test password validation"""
        # Valid passwords
        self.assertTrue(validate_password("password123")[0])
        self.assertTrue(validate_password("a" * 6)[0])
        
        # Invalid passwords
        self.assertFalse(validate_password("short")[0])
        self.assertFalse(validate_password("")[0])
    
    def test_validate_price(self):
        """Test price validation"""
        # Valid prices
        valid, price, _ = validate_price("10.99")
        self.assertTrue(valid)
        self.assertEqual(price, 10.99)
        
        valid, price, _ = validate_price("0.01")
        self.assertTrue(valid)
        
        # Invalid prices
        self.assertFalse(validate_price("-5")[0])
        self.assertFalse(validate_price("invalid")[0])
        self.assertFalse(validate_price("")[0])
    
    def test_validate_date(self):
        """Test date validation"""
        # Valid dates
        self.assertTrue(validate_date("2025-12-30")[0])
        
        # Invalid dates
        self.assertFalse(validate_date("invalid")[0])
        self.assertFalse(validate_date("12/30/2025")[0])
        self.assertFalse(validate_date("")[0])
    
    def test_validate_phone(self):
        """Test phone validation"""
        # Valid phones
        self.assertTrue(validate_phone("1234567890")[0])
        self.assertTrue(validate_phone("(123) 456-7890")[0])
        self.assertTrue(validate_phone("")[0])  # Optional
        
        # Invalid phones
        self.assertFalse(validate_phone("123")[0])  # Too short
        self.assertFalse(validate_phone("abc123")[0])  # Contains letters
    
    def test_validate_name(self):
        """Test name validation"""
        # Valid names
        self.assertTrue(validate_name("John", "First name")[0])
        self.assertTrue(validate_name("O'Brien", "Last name")[0])
        
        # Invalid names
        self.assertFalse(validate_name("", "Name")[0])
        self.assertFalse(validate_name("A" * 101, "Name")[0])  # Too long
        self.assertFalse(validate_name("John<script>", "Name")[0])  # Invalid chars
    
    def test_validate_quantity(self):
        """Test quantity validation"""
        # Valid quantities
        valid, qty, _ = validate_quantity("5")
        self.assertTrue(valid)
        self.assertEqual(qty, 5)
        
        # Invalid quantities
        self.assertFalse(validate_quantity("0")[0])
        self.assertFalse(validate_quantity("100")[0])  # Over max
        self.assertFalse(validate_quantity("invalid")[0])

if __name__ == "__main__":
    unittest.main()

