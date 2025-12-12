"""
Utility functions for Notify Africa SDK
"""

import re
from typing import List, Union, Dict
import pandas as pd
from datetime import datetime


def normalize_phone_number(phone: str) -> str:
    """
    Normalize phone number to Tanzanian format (255XXXXXXXXX)
    Based on PhoneNumberHelper from the codebase
    """
    # Remove all non-numeric characters
    cleaned = re.sub(r'[^\d]', '', str(phone))
    
    if len(cleaned) == 10 and cleaned.startswith('0'):
        # Format: 07XXXXXXXX or 06XXXXXXXX -> Replace leading 0 with country code
        second_digit = cleaned[1]
        if second_digit in ['6', '7']:
            return '255' + cleaned[1:]
    elif len(cleaned) == 12 and cleaned.startswith('255'):
        # Format: 255XXXXXXXXX -> Verify it's a valid Tanzanian prefix
        prefix_digit = cleaned[3]
        if prefix_digit in ['6', '7']:
            return cleaned
    elif len(cleaned) == 13 and cleaned.startswith('+255'):
        # Format: +255XXXXXXXXX -> Remove + and verify
        without_plus = cleaned[1:]
        prefix_digit = without_plus[3]
        if prefix_digit in ['6', '7']:
            return without_plus
    
    # If none of the formats match, raise an error
    raise ValueError(f"Invalid phone number format: {phone}")


def validate_phone_numbers(phone_numbers: Union[str, List[str]]) -> List[str]:
    """Validate and normalize a list of phone numbers"""
    if isinstance(phone_numbers, str):
        phone_numbers = [phone_numbers]
    
    validated_numbers = []
    for phone in phone_numbers:
        try:
            normalized = normalize_phone_number(phone)
            validated_numbers.append(normalized)
        except ValueError as e:
            raise ValueError(f"Invalid phone number {phone}: {e}")
    
    return validated_numbers


def calculate_sms_credits(message: str) -> int:
    """Calculate SMS credits needed based on message length"""
    # SMS length is 160 characters per credit
    return max(1, len(message) // 160 + (1 if len(message) % 160 > 0 else 0))


def parse_excel_contacts(file_path: str, phone_column: str = "phone", 
                        message_column: str = "message", 
                        names_column: str = "names") -> List[Dict[str, str]]:
    """Parse contacts from Excel file"""
    try:
        df = pd.read_excel(file_path)
        
        # Check if required columns exist
        if phone_column not in df.columns:
            raise ValueError(f"Column '{phone_column}' not found in Excel file")
        
        contacts = []
        for _, row in df.iterrows():
            contact = {
                'phone': str(row[phone_column]).strip(),
            }
            
            # Add message if column exists
            if message_column in df.columns and pd.notna(row[message_column]):
                contact['message'] = str(row[message_column]).strip()
            
            # Add names if column exists
            if names_column in df.columns and pd.notna(row[names_column]):
                contact['names'] = str(row[names_column]).strip()
            
            # Skip empty phone numbers
            if contact['phone'] and contact['phone'] != 'nan':
                contacts.append(contact)
        
        return contacts
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")


def format_datetime_for_api(dt: datetime) -> str:
    """Format datetime for API requests"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")



