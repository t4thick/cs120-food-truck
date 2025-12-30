"""
Email service for sending verification codes and notifications.
Supports SMTP configuration via environment variables.
"""
import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class EmailService:
    """Email service for sending verification codes"""
    
    def __init__(self):
        self.smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        self.smtp_username = os.environ.get("SMTP_USERNAME", "")
        self.smtp_password = os.environ.get("SMTP_PASSWORD", "")
        self.from_email = os.environ.get("FROM_EMAIL", self.smtp_username)
        self.enabled = bool(self.smtp_username and self.smtp_password)
        
        if not self.enabled:
            logger.warning("Email service not configured. Set SMTP_USERNAME and SMTP_PASSWORD to enable.")
    
    def send_verification_code(self, to_email: str, code: str) -> Tuple[bool, Optional[str]]:
        """
        Send a 4-digit verification code to the user's email.
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        if not self.enabled:
            return False, "Email service is not configured"
        
        try:
            subject = "Item7 Food Truck - Email Verification Code"
            body = f"""
Hello,

Your verification code for Item7 Food Truck is:

    {code}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Thank you,
Item7 Food Truck Team
"""
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Verification code sent to {to_email}")
            return True, None
            
        except smtplib.SMTPAuthenticationError as e:
            error_msg = "SMTP authentication failed. Please check your email credentials."
            logger.error(f"SMTP auth error: {e}")
            return False, error_msg
        except smtplib.SMTPException as e:
            error_msg = f"Failed to send email: {str(e)}"
            logger.error(f"SMTP error: {e}")
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error sending email: {str(e)}"
            logger.error(f"Email send error: {e}", exc_info=True)
            return False, error_msg
    
    def send_order_confirmation(self, to_email: str, order_id: str, order_details: dict) -> Tuple[bool, Optional[str]]:
        """
        Send order confirmation email.
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        if not self.enabled:
            return False, "Email service is not configured"
        
        try:
            subject = f"Order Confirmation - {order_id}"
            body = f"""
Hello,

Thank you for your order with Item7 Food Truck!

Order ID: {order_id}
Total: ${order_details.get('total', 0):.2f}
Status: {order_details.get('status', 'Pending')}

Items: {order_details.get('items', 'N/A')}

You can track your order at: {order_details.get('tracking_url', 'N/A')}

Thank you for choosing Item7 Food Truck!

Best regards,
Item7 Food Truck Team
"""
            
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Order confirmation sent to {to_email} for order {order_id}")
            return True, None
            
        except Exception as e:
            logger.error(f"Error sending order confirmation: {e}", exc_info=True)
            return False, str(e)

# Global email service instance
email_service = EmailService()

