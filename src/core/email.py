"""
ORBIT Email Service
Handles email sending for notifications, verification, and alerts
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import structlog
from datetime import datetime

from .config import settings

logger = structlog.get_logger(__name__)


class EmailService:
    """
    Email service for sending notifications and alerts
    """
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL
        self.from_name = settings.FROM_NAME
        
        logger.info(
            "Email service initialized",
            smtp_host=self.smtp_host,
            smtp_port=self.smtp_port,
            from_email=self.from_email
        )
    
    def _create_smtp_connection(self):
        """Create SMTP connection"""
        try:
            # Create SMTP connection
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()  # Enable TLS encryption
            
            # Login if credentials provided
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
            
            return server
            
        except Exception as e:
            logger.error(f"Failed to create SMTP connection: {str(e)}")
            raise
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        Send an email
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body_text: Plain text body
            body_html: HTML body (optional)
            cc: CC recipients (optional)
            bcc: BCC recipients (optional)
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            
            # Add plain text part
            text_part = MIMEText(body_text, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if body_html:
                html_part = MIMEText(body_html, 'html')
                msg.attach(html_part)
            
            # Send email
            with self._create_smtp_connection() as server:
                recipients = [to_email]
                if cc:
                    recipients.extend(cc)
                if bcc:
                    recipients.extend(bcc)
                
                server.sendmail(self.from_email, recipients, msg.as_string())
            
            logger.info(
                "Email sent successfully",
                to_email=to_email,
                subject=subject
            )
            
            return True
            
        except Exception as e:
            logger.error(
                "Failed to send email",
                to_email=to_email,
                subject=subject,
                error=str(e),
                exc_info=True
            )
            return False
    
    def send_welcome_email(self, user_email: str, user_name: str) -> bool:
        """Send welcome email to new user"""
        subject = f"Welcome to ORBIT, {user_name}! 🎉"
        
        body_text = f"""
Hi {user_name},

Welcome to ORBIT - Your AI-Powered Life Optimization Platform!

We're excited to have you on board. ORBIT uses advanced AI to help you achieve your goals through:

• Personalized interventions based on behavioral science
• Real-time monitoring and adaptive support
• Cross-domain goal optimization
• Transparent AI with reliability tracking

Get started by:
1. Setting up your first goal
2. Connecting your calendar and apps
3. Letting our AI learn your patterns

If you have any questions, just reply to this email.

Best regards,
The ORBIT Team

---
ORBIT AI Platform
{settings.FRONTEND_URL}
"""
        
        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .features {{ background: white; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .feature {{ margin: 15px 0; padding-left: 30px; position: relative; }}
        .feature:before {{ content: "✓"; position: absolute; left: 0; color: #667eea; font-weight: bold; font-size: 20px; }}
        .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Welcome to ORBIT!</h1>
            <p>Your AI-Powered Life Optimization Platform</p>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            
            <p>We're thrilled to have you join ORBIT! Get ready to achieve your goals with the power of AI and behavioral science.</p>
            
            <div class="features">
                <h3>What You Get:</h3>
                <div class="feature">Personalized AI interventions based on proven behavioral science</div>
                <div class="feature">Real-time monitoring and adaptive support</div>
                <div class="feature">Cross-domain goal optimization</div>
                <div class="feature">Transparent AI with reliability tracking</div>
            </div>
            
            <p><strong>Get Started:</strong></p>
            <ol>
                <li>Set up your first goal</li>
                <li>Connect your calendar and apps</li>
                <li>Let our AI learn your patterns</li>
            </ol>
            
            <center>
                <a href="{settings.FRONTEND_URL}/onboarding" class="button">Complete Setup →</a>
            </center>
            
            <p>If you have any questions, just reply to this email. We're here to help!</p>
            
            <p>Best regards,<br>The ORBIT Team</p>
        </div>
        <div class="footer">
            <p>ORBIT AI Platform | {settings.FRONTEND_URL}</p>
            <p>You're receiving this because you signed up for ORBIT.</p>
        </div>
    </div>
</body>
</html>
"""
        
        return self.send_email(user_email, subject, body_text, body_html)
    
    def send_verification_email(self, user_email: str, user_name: str, verification_token: str) -> bool:
        """Send email verification link"""
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
        
        subject = "Verify Your ORBIT Email Address"
        
        body_text = f"""
Hi {user_name},

Please verify your email address by clicking the link below:

{verification_url}

This link will expire in 24 hours.

If you didn't create an ORBIT account, please ignore this email.

Best regards,
The ORBIT Team
"""
        
        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Verify Your Email Address</h2>
        <p>Hi {user_name},</p>
        <p>Please verify your email address by clicking the button below:</p>
        <center>
            <a href="{verification_url}" class="button">Verify Email Address</a>
        </center>
        <p>Or copy and paste this link into your browser:</p>
        <p style="word-break: break-all; color: #666;">{verification_url}</p>
        <p><small>This link will expire in 24 hours.</small></p>
        <p>If you didn't create an ORBIT account, please ignore this email.</p>
    </div>
</body>
</html>
"""
        
        return self.send_email(user_email, subject, body_text, body_html)
    
    def send_password_reset_email(self, user_email: str, user_name: str, reset_token: str) -> bool:
        """Send password reset link"""
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        subject = "Reset Your ORBIT Password"
        
        body_text = f"""
Hi {user_name},

We received a request to reset your ORBIT password.

Click the link below to reset your password:

{reset_url}

This link will expire in 1 hour.

If you didn't request a password reset, please ignore this email and your password will remain unchanged.

Best regards,
The ORBIT Team
"""
        
        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Reset Your Password</h2>
        <p>Hi {user_name},</p>
        <p>We received a request to reset your ORBIT password.</p>
        <center>
            <a href="{reset_url}" class="button">Reset Password</a>
        </center>
        <p>Or copy and paste this link into your browser:</p>
        <p style="word-break: break-all; color: #666;">{reset_url}</p>
        <p><small>This link will expire in 1 hour.</small></p>
        <div class="warning">
            <strong>⚠️ Security Notice:</strong><br>
            If you didn't request a password reset, please ignore this email and your password will remain unchanged.
        </div>
    </div>
</body>
</html>
"""
        
        return self.send_email(user_email, subject, body_text, body_html)
    
    def send_intervention_notification(
        self,
        user_email: str,
        user_name: str,
        intervention_content: str,
        goal_title: str
    ) -> bool:
        """Send intervention notification"""
        subject = f"🎯 New Intervention for: {goal_title}"
        
        body_text = f"""
Hi {user_name},

Your AI assistant has a new intervention for your goal: {goal_title}

{intervention_content}

Log in to ORBIT to view details and take action:
{settings.FRONTEND_URL}/dashboard

Best regards,
Your ORBIT AI Assistant
"""
        
        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .intervention {{ background: #f0f7ff; border-left: 4px solid #667eea; padding: 20px; margin: 20px 0; border-radius: 5px; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>🎯 New Intervention</h2>
        <p>Hi {user_name},</p>
        <p>Your AI assistant has a new intervention for your goal: <strong>{goal_title}</strong></p>
        <div class="intervention">
            <p>{intervention_content}</p>
        </div>
        <center>
            <a href="{settings.FRONTEND_URL}/dashboard" class="button">View in ORBIT →</a>
        </center>
        <p><small>This intervention was generated by your AI assistant based on your goals and behavioral patterns.</small></p>
    </div>
</body>
</html>
"""
        
        return self.send_email(user_email, subject, body_text, body_html)
    
    def send_goal_milestone_email(
        self,
        user_email: str,
        user_name: str,
        goal_title: str,
        milestone: str,
        progress: float
    ) -> bool:
        """Send goal milestone achievement notification"""
        subject = f"🎉 Milestone Achieved: {goal_title}"
        
        body_text = f"""
Hi {user_name},

Congratulations! You've reached a milestone on your goal: {goal_title}

Milestone: {milestone}
Progress: {progress}%

Keep up the great work! Your consistency is paying off.

View your progress:
{settings.FRONTEND_URL}/goals

Best regards,
The ORBIT Team
"""
        
        body_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .celebration {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; margin: 20px 0; }}
        .progress {{ background: #f9f9f9; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="celebration">
            <h1>🎉 Milestone Achieved!</h1>
            <h2>{goal_title}</h2>
        </div>
        <p>Hi {user_name},</p>
        <p>Congratulations! You've reached an important milestone:</p>
        <div class="progress">
            <h3>{milestone}</h3>
            <p><strong>Progress: {progress}%</strong></p>
        </div>
        <p>Keep up the great work! Your consistency is paying off.</p>
        <center>
            <a href="{settings.FRONTEND_URL}/goals" class="button">View Your Progress →</a>
        </center>
    </div>
</body>
</html>
"""
        
        return self.send_email(user_email, subject, body_text, body_html)
    
    async def test_connection(self) -> dict:
        """Test SMTP connection"""
        try:
            with self._create_smtp_connection() as server:
                logger.info("SMTP connection test successful")
                return {
                    "status": "success",
                    "message": "SMTP connection successful",
                    "smtp_host": self.smtp_host,
                    "smtp_port": self.smtp_port
                }
        except Exception as e:
            logger.error(f"SMTP connection test failed: {str(e)}")
            return {
                "status": "error",
                "message": f"SMTP connection failed: {str(e)}",
                "smtp_host": self.smtp_host,
                "smtp_port": self.smtp_port
            }


# Global email service instance
email_service = EmailService()
