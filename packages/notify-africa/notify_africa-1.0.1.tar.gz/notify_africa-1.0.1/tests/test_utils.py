import unittest
from notify_africa.utils import normalize_phone_number, validate_phone_numbers, calculate_sms_credits


class TestUtils(unittest.TestCase):
    
    def test_normalize_phone_number(self):
        # Test various phone number formats
        test_cases = [
            ("0712345678", "255712345678"),
            ("255712345678", "255712345678"),
            ("+255712345678", "255712345678"),
            ("0687654321", "255687654321"),
        ]
        
        for input_phone, expected in test_cases:
            with self.subTest(input_phone=input_phone):
                result = normalize_phone_number(input_phone)
                self.assertEqual(result, expected)
    
    def test_invalid_phone_numbers(self):
        invalid_numbers = [
            "123456",  # Too short
            "255812345678",  # Invalid prefix (8)
            "254712345678",  # Wrong country code
        ]
        
        for invalid_number in invalid_numbers:
            with self.subTest(invalid_number=invalid_number):
                with self.assertRaises(ValueError):
                    normalize_phone_number(invalid_number)
    
    def test_validate_phone_numbers(self):
        # Test list of phone numbers
        numbers = ["0712345678", "255687654321"]
        result = validate_phone_numbers(numbers)
        expected = ["255712345678", "255687654321"]
        self.assertEqual(result, expected)
        
        # Test single phone number
        result = validate_phone_numbers("0712345678")
        expected = ["255712345678"]
        self.assertEqual(result, expected)
    
    def test_calculate_sms_credits(self):
        # Test message length calculations
        test_cases = [
            ("Hello", 1),  # Short message
            ("A" * 160, 1),  # Exactly 160 characters
            ("A" * 161, 2),  # Just over 160 characters
            ("A" * 320, 2),  # Exactly 320 characters
            ("A" * 321, 3),  # Just over 320 characters
        ]
        
        for message, expected_credits in test_cases:
            with self.subTest(message_length=len(message)):
                result = calculate_sms_credits(message)
                self.assertEqual(result, expected_credits)


if __name__ == '__main__':
    unittest.main()