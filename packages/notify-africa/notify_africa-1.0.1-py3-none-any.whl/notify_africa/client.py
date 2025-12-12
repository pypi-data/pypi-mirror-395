"""
Main client for Notify Africa SMS SDK
"""

import requests
from typing import List, Dict, Any
import json

from .exceptions import (
    NotifyAfricaException,
    NetworkError
)
from .models import (
    SendSingleResponse,
    SendBatchResponse,
    MessageStatusResponse
)


class NotifyAfrica:
    """
    Notify Africa SMS Client
    
    A Python client for interacting with Notify Africa SMS API.
    Matches the Node.js SDK structure.
    """
    
    def __init__(self, apiToken: str, baseUrl: str = "https://api.notify.africa"):
        """
        Initialize the Notify Africa client
        
        Args:
            apiToken (str): Your Notify Africa API token
            baseUrl (str, optional): Base URL for the API (defaults to https://api.notify.africa)
        """
        self.apiToken = apiToken
        # Remove trailing slash if present
        self.baseUrl = baseUrl.rstrip('/')
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.apiToken}"
        })
    
    def send_single_message(
        self,
        phoneNumber: str,
        message: str,
        senderId: str
    ) -> SendSingleResponse:
        """
        Sends a single SMS message.
        
        Args:
            phoneNumber: The recipient's phone number (e.g., "2556XXXXX459").
            message: The message content.
            senderId: The sender ID (e.g., "137").
            
        Returns:
            SendSingleResponse: The response data with messageId and status.
        """
        url = f"{self.baseUrl}/api/v1/api/messages/send"
        body: Dict[str, Any] = {
            "phone_number": phoneNumber,
            "message": message,
            "sender_id": senderId,
        }
        
        headers = {
            "Authorization": f"Bearer {self.apiToken}",
            "Content-Type": "application/json",
        }
        
        try:
            response = self.session.post(url, headers=headers, json=body)
            
            if not response.ok:
                try:
                    error_data = response.json()
                    raise NotifyAfricaException(
                        error_data.get('message', f'HTTP error! Status: {response.status_code}'),
                        response.status_code,
                        error_data
                    )
                except json.JSONDecodeError:
                    raise NotifyAfricaException(
                        f'HTTP error! Status: {response.status_code}',
                        response.status_code
                    )
            
            data = response.json()
            if data.get('status') != 200:
                raise NotifyAfricaException(
                    data.get('message', 'Failed to send message'),
                    response.status_code,
                    data
                )
            
            response_data = data.get('data', {})
            return SendSingleResponse(
                messageId=response_data.get('messageId', ''),
                status=response_data.get('status', '')
            )
            
        except requests.RequestException as e:
            raise NetworkError(f"Error sending single message: {str(e)}")
        except NotifyAfricaException:
            raise
        except Exception as e:
            raise NotifyAfricaException(f"Error sending single message: {str(e)}")
    
    def send_batch_messages(
        self,
        phoneNumbers: List[str],
        message: str,
        senderId: str
    ) -> SendBatchResponse:
        """
        Sends a batch of SMS messages to multiple recipients.
        
        Args:
            phoneNumbers: Array of recipient phone numbers (e.g., ["2556XXXXX459", "2556XXXXX459"]).
            message: The message content.
            senderId: The sender ID (e.g., "137").
            
        Returns:
            SendBatchResponse: The response data with messageCount, creditsDeducted, and remainingBalance.
        """
        url = f"{self.baseUrl}/api/v1/api/messages/batch"
        body: Dict[str, Any] = {
            "phone_numbers": phoneNumbers,
            "message": message,
            "sender_id": senderId,
        }
        
        headers = {
            "Authorization": f"Bearer {self.apiToken}",
            "Content-Type": "application/json",
        }
        
        try:
            response = self.session.post(url, headers=headers, json=body)
            
            if not response.ok:
                try:
                    error_data = response.json()
                    raise NotifyAfricaException(
                        error_data.get('message', f'HTTP error! Status: {response.status_code}'),
                        response.status_code,
                        error_data
                    )
                except json.JSONDecodeError:
                    raise NotifyAfricaException(
                        f'HTTP error! Status: {response.status_code}',
                        response.status_code
                    )
            
            data = response.json()
            if data.get('status') != 200:
                raise NotifyAfricaException(
                    data.get('message', 'Failed to send batch messages'),
                    response.status_code,
                    data
                )
            
            response_data = data.get('data', {})
            return SendBatchResponse(
                messageCount=response_data.get('messageCount', 0),
                creditsDeducted=response_data.get('creditsDeducted', 0),
                remainingBalance=response_data.get('remainingBalance', 0)
            )
            
        except requests.RequestException as e:
            raise NetworkError(f"Error sending batch messages: {str(e)}")
        except NotifyAfricaException:
            raise
        except Exception as e:
            raise NotifyAfricaException(f"Error sending batch messages: {str(e)}")
    
    def check_message_status(self, messageId: str) -> MessageStatusResponse:
        """
        Checks the status of a sent message.
        
        Args:
            messageId: The ID of the message to check (e.g., "156022").
            
        Returns:
            MessageStatusResponse: The response data with messageId, status, sentAt, and deliveredAt.
        """
        url = f"{self.baseUrl}/api/v1/api/messages/status/{messageId}"
        headers = {
            "Authorization": f"Bearer {self.apiToken}",
        }
        
        try:
            response = self.session.get(url, headers=headers)
            
            if not response.ok:
                try:
                    error_data = response.json()
                    raise NotifyAfricaException(
                        error_data.get('message', f'HTTP error! Status: {response.status_code}'),
                        response.status_code,
                        error_data
                    )
                except json.JSONDecodeError:
                    raise NotifyAfricaException(
                        f'HTTP error! Status: {response.status_code}',
                        response.status_code
                    )
            
            data = response.json()
            if data.get('status') != 200:
                raise NotifyAfricaException(
                    data.get('message', 'Failed to retrieve message status'),
                    response.status_code,
                    data
                )
            
            response_data = data.get('data', {})
            return MessageStatusResponse(
                messageId=response_data.get('messageId', ''),
                status=response_data.get('status', ''),
                sentAt=response_data.get('sentAt'),
                deliveredAt=response_data.get('deliveredAt')
            )
            
        except requests.RequestException as e:
            raise NetworkError(f"Error checking message status: {str(e)}")
        except NotifyAfricaException:
            raise
        except Exception as e:
            raise NotifyAfricaException(f"Error checking message status: {str(e)}")