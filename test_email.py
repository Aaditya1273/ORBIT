"""
Test ORBIT Email Configuration
Verifies SMTP settings and sends a test email
"""

import asyncio
from dotenv import load_dotenv
import os

# Load environment
load_dotenv('.env.local')

def test_email_config():
    """Test email configuration"""
    print("=" * 70)
    print("📧 ORBIT EMAIL CONFIGURATION TEST")
    print("=" * 70)
    
    # Check environment variables
    print("\n1️⃣  Checking Email Configuration...")
    print("-" * 70)
    
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = os.getenv('SMTP_PORT')
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')
    from_name = os.getenv('FROM_NAME', 'ORBIT AI Platform')
    
    if smtp_host:
        print(f"✅ SMTP Host: {smtp_host}")
    else:
        print(f"❌ SMTP Host: Not configured")
    
    if smtp_port:
        print(f"✅ SMTP Port: {smtp_port}")
    else:
        print(f"❌ SMTP Port: Not configured")
    
    if smtp_user:
        print(f"✅ SMTP User: {smtp_user}")
    else:
        print(f"❌ SMTP User: Not configured")
    
    if smtp_password:
        print(f"✅ SMTP Password: {'*' * len(smtp_password)} (configured)")
    else:
        print(f"❌ SMTP Password: Not configured")
    
    if from_email:
        print(f"✅ From Email: {from_email}")
    else:
        print(f"❌ From Email: Not configured")
    
    print(f"✅ From Name: {from_name}")
    
    # Test SMTP connection
    print("\n2️⃣  Testing SMTP Connection...")
    print("-" * 70)
    
    if not all([smtp_host, smtp_port, smtp_user, smtp_password]):
        print("❌ Cannot test connection - missing configuration")
        return False
    
    try:
        import smtplib
        
        print(f"Connecting to {smtp_host}:{smtp_port}...")
        
        # Create SMTP connection
        server = smtplib.SMTP(smtp_host, int(smtp_port), timeout=10)
        server.starttls()
        
        print("✅ TLS connection established")
        
        # Login
        server.login(smtp_user, smtp_password)
        print("✅ Authentication successful")
        
        server.quit()
        print("✅ SMTP connection test passed!")
        
        connection_success = True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {str(e)}")
        print("\n💡 Troubleshooting:")
        print("   • Check if your email password is correct")
        print("   • For Gmail, you may need an 'App Password':")
        print("     1. Go to Google Account settings")
        print("     2. Security > 2-Step Verification")
        print("     3. App passwords > Generate new password")
        print("     4. Use that password instead of your regular password")
        connection_success = False
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        connection_success = False
    
    # Test sending email (optional)
    print("\n3️⃣  Send Test Email?")
    print("-" * 70)
    
    if connection_success:
        send_test = input("Send a test email to yourself? (y/n): ").lower().strip()
        
        if send_test == 'y':
            try:
                from src.core.email import email_service
                
                print(f"\nSending test email to {smtp_user}...")
                
                success = email_service.send_email(
                    to_email=smtp_user,
                    subject="🎉 ORBIT Email Test - Success!",
                    body_text=f"""
Hi there!

This is a test email from your ORBIT AI Platform.

If you're reading this, your email configuration is working perfectly! ✅

Configuration Details:
- SMTP Host: {smtp_host}
- SMTP Port: {smtp_port}
- From Email: {from_email}
- From Name: {from_name}

You're all set to receive:
• Welcome emails
• Email verification
• Password reset links
• Intervention notifications
• Goal milestone alerts

Best regards,
The ORBIT Team
""",
                    body_html=f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 10px; margin-top: 20px; }}
        .success {{ background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .config {{ background: white; padding: 15px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Email Test Successful!</h1>
            <p>Your ORBIT email configuration is working perfectly</p>
        </div>
        <div class="content">
            <div class="success">
                <strong>✅ Success!</strong><br>
                If you're reading this, your email configuration is working perfectly!
            </div>
            
            <h3>Configuration Details:</h3>
            <div class="config">
                <p><strong>SMTP Host:</strong> {smtp_host}</p>
                <p><strong>SMTP Port:</strong> {smtp_port}</p>
                <p><strong>From Email:</strong> {from_email}</p>
                <p><strong>From Name:</strong> {from_name}</p>
            </div>
            
            <h3>You're all set to receive:</h3>
            <ul>
                <li>✉️ Welcome emails</li>
                <li>🔐 Email verification</li>
                <li>🔑 Password reset links</li>
                <li>🎯 Intervention notifications</li>
                <li>🏆 Goal milestone alerts</li>
            </ul>
            
            <p>Best regards,<br>The ORBIT Team</p>
        </div>
    </div>
</body>
</html>
"""
                )
                
                if success:
                    print("✅ Test email sent successfully!")
                    print(f"📬 Check your inbox at {smtp_user}")
                else:
                    print("❌ Failed to send test email")
                    
            except Exception as e:
                print(f"❌ Error sending test email: {str(e)}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    if connection_success:
        print("\n✅ Email Configuration: WORKING")
        print("\n🎉 Your ORBIT platform can now send emails!")
        print("\nEmail Features Available:")
        print("  • Welcome emails for new users")
        print("  • Email verification")
        print("  • Password reset")
        print("  • Intervention notifications")
        print("  • Goal milestone alerts")
    else:
        print("\n⚠️  Email Configuration: NEEDS ATTENTION")
        print("\nPlease fix the configuration issues above.")
    
    print("\n" + "=" * 70)
    
    return connection_success


if __name__ == "__main__":
    test_email_config()
