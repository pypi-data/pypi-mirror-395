import unittest
from unittest.mock import Mock, patch
import json

from notify_africa import NotifyAfrica
from notify_africa.exceptions import NotifyAfricaException, NetworkError
from notify_africa.models import SendSingleResponse, SendBatchResponse, MessageStatusResponse


class TestNotifyAfrica(unittest.TestCase):
    
    def setUp(self):
        self.client = NotifyAfrica(
            apiToken="test_api_token",
            baseUrl="https://test-api.notify.africa"
        )
    
    @patch('requests.Session.post')
    def test_send_single_message_success(self, mock_post):
        """Test successful single message send"""
        # Mock successful response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "message": "Message sent successfully",
            "data": {
                "messageId": "165102",
                "status": "PROCESSING"
            }
        }
        mock_post.return_value = mock_response
        
        response = self.client.send_single_message(
            phoneNumber="255694192317",
            message="Test message",
            senderId="164"
        )
        
        self.assertIsInstance(response, SendSingleResponse)
        self.assertEqual(response.messageId, "165102")
        self.assertEqual(response.status, "PROCESSING")
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertIn("/api/v1/api/messages/send", call_args[0][0])
        self.assertEqual(call_args[1]["json"]["phone_number"], "255694192317")
        self.assertEqual(call_args[1]["json"]["message"], "Test message")
        self.assertEqual(call_args[1]["json"]["sender_id"], "164")
    
    @patch('requests.Session.post')
    def test_send_single_message_api_error(self, mock_post):
        """Test single message send with API error"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 400,
            "message": "Invalid phone number"
        }
        mock_post.return_value = mock_response
        
        with self.assertRaises(NotifyAfricaException) as context:
            self.client.send_single_message(
                phoneNumber="invalid",
                message="Test",
                senderId="164"
            )
        
        self.assertIn("Invalid phone number", str(context.exception))
    
    @patch('requests.Session.post')
    def test_send_single_message_http_error(self, mock_post):
        """Test single message send with HTTP error"""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "message": "Unauthorized"
        }
        mock_post.return_value = mock_response
        
        with self.assertRaises(NotifyAfricaException) as context:
            self.client.send_single_message(
                phoneNumber="255694192317",
                message="Test",
                senderId="164"
            )
        
        self.assertEqual(context.exception.status_code, 401)
    
    @patch('requests.Session.post')
    def test_send_single_message_network_error(self, mock_post):
        """Test single message send with network error"""
        import requests
        mock_post.side_effect = requests.RequestException("Network error")
        
        with self.assertRaises(NetworkError):
            self.client.send_single_message(
                phoneNumber="255694192317",
                message="Test",
                senderId="164"
            )
    
    @patch('requests.Session.post')
    def test_send_batch_messages_success(self, mock_post):
        """Test successful batch message send"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "message": "Batch messages sent successfully",
            "data": {
                "messageCount": 2,
                "creditsDeducted": 2,
                "remainingBalance": 84
            }
        }
        mock_post.return_value = mock_response
        
        response = self.client.send_batch_messages(
            phoneNumbers=["255694192317", "255743517612"],
            message="Batch test message",
            senderId="164"
        )
        
        self.assertIsInstance(response, SendBatchResponse)
        self.assertEqual(response.messageCount, 2)
        self.assertEqual(response.creditsDeducted, 2)
        self.assertEqual(response.remainingBalance, 84)
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertIn("/api/v1/api/messages/batch", call_args[0][0])
        self.assertEqual(call_args[1]["json"]["phone_numbers"], ["255694192317", "255743517612"])
        self.assertEqual(call_args[1]["json"]["message"], "Batch test message")
        self.assertEqual(call_args[1]["json"]["sender_id"], "164")
    
    @patch('requests.Session.post')
    def test_send_batch_messages_api_error(self, mock_post):
        """Test batch message send with API error"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 400,
            "message": "Invalid sender ID"
        }
        mock_post.return_value = mock_response
        
        with self.assertRaises(NotifyAfricaException) as context:
            self.client.send_batch_messages(
                phoneNumbers=["255694192317"],
                message="Test",
                senderId="invalid"
            )
        
        self.assertIn("Invalid sender ID", str(context.exception))
    
    @patch('requests.Session.post')
    def test_send_batch_messages_http_error(self, mock_post):
        """Test batch message send with HTTP error"""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 402
        mock_response.json.return_value = {
            "message": "Insufficient credits"
        }
        mock_post.return_value = mock_response
        
        with self.assertRaises(NotifyAfricaException) as context:
            self.client.send_batch_messages(
                phoneNumbers=["255694192317"],
                message="Test",
                senderId="164"
            )
        
        self.assertEqual(context.exception.status_code, 402)
    
    @patch('requests.Session.get')
    def test_check_message_status_success(self, mock_get):
        """Test successful message status check"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "message": "Status retrieved successfully",
            "data": {
                "messageId": "165102",
                "status": "DELIVERED",
                "sentAt": "2024-01-15T10:30:00Z",
                "deliveredAt": "2024-01-15T10:30:15Z"
            }
        }
        mock_get.return_value = mock_response
        
        response = self.client.check_message_status(messageId="165102")
        
        self.assertIsInstance(response, MessageStatusResponse)
        self.assertEqual(response.messageId, "165102")
        self.assertEqual(response.status, "DELIVERED")
        self.assertEqual(response.sentAt, "2024-01-15T10:30:00Z")
        self.assertEqual(response.deliveredAt, "2024-01-15T10:30:15Z")
        
        # Verify the request was made correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertIn("/api/v1/api/messages/status/165102", call_args[0][0])
    
    @patch('requests.Session.get')
    def test_check_message_status_not_found(self, mock_get):
        """Test message status check when message not found"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 404,
            "message": "Message not found"
        }
        mock_get.return_value = mock_response
        
        with self.assertRaises(NotifyAfricaException) as context:
            self.client.check_message_status(messageId="999999")
        
        self.assertIn("Message not found", str(context.exception))
    
    @patch('requests.Session.get')
    def test_check_message_status_http_error(self, mock_get):
        """Test message status check with HTTP error"""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "message": "Internal server error"
        }
        mock_get.return_value = mock_response
        
        with self.assertRaises(NotifyAfricaException) as context:
            self.client.check_message_status(messageId="165102")
        
        self.assertEqual(context.exception.status_code, 500)
    
    @patch('requests.Session.get')
    def test_check_message_status_network_error(self, mock_get):
        """Test message status check with network error"""
        import requests
        mock_get.side_effect = requests.RequestException("Network error")
        
        with self.assertRaises(NetworkError):
            self.client.check_message_status(messageId="165102")
    
    @patch('requests.Session.get')
    def test_check_message_status_null_timestamps(self, mock_get):
        """Test message status with null timestamps"""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": 200,
            "message": "Status retrieved",
            "data": {
                "messageId": "165102",
                "status": "PROCESSING",
                "sentAt": None,
                "deliveredAt": None
            }
        }
        mock_get.return_value = mock_response
        
        response = self.client.check_message_status(messageId="165102")
        
        self.assertEqual(response.messageId, "165102")
        self.assertEqual(response.status, "PROCESSING")
        self.assertIsNone(response.sentAt)
        self.assertIsNone(response.deliveredAt)
    
    def test_constructor_with_default_base_url(self):
        """Test constructor with default base URL"""
        client = NotifyAfrica(apiToken="test_token")
        self.assertEqual(client.baseUrl, "https://api.notify.africa")
        self.assertEqual(client.apiToken, "test_token")
    
    def test_constructor_with_custom_base_url(self):
        """Test constructor with custom base URL"""
        client = NotifyAfrica(
            apiToken="test_token",
            baseUrl="https://custom-api.notify.africa"
        )
        self.assertEqual(client.baseUrl, "https://custom-api.notify.africa")
    
    def test_constructor_removes_trailing_slash(self):
        """Test constructor removes trailing slash from base URL"""
        client = NotifyAfrica(
            apiToken="test_token",
            baseUrl="https://api.notify.africa/"
        )
        self.assertEqual(client.baseUrl, "https://api.notify.africa")
    
    @patch('requests.Session.post')
    def test_send_single_message_json_decode_error(self, mock_post):
        """Test single message send with invalid JSON response"""
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_post.return_value = mock_response
        
        with self.assertRaises(NotifyAfricaException) as context:
            self.client.send_single_message(
                phoneNumber="255694192317",
                message="Test",
                senderId="164"
            )
        
        self.assertEqual(context.exception.status_code, 500)


if __name__ == '__main__':
    unittest.main()
