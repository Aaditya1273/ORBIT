"""
Simple Email Test
Quick test of SMTP configuration
"""

import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment
load_dotenv('.env.local')

print("=" * 70)
print("📧 SIMPLE EMAIL TEST")
print("=" * 70)

# Get configuration
smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
smtp_port = int(os.getenv('SMTP_PORT', '587'))
smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')
from_email = os.getenv('FROM_EMAIL', smtp_user)

print(f"\nConfiguration:")
print(f"  Host: {smtp_host}")
print(f"  Port: {smtp_port}")
print(f"  User: {smtp_user}")
print(f"  Password: {'*' * len(smtp_password) if smtp_password else 'Not set'}")
print(f"  From: {from_email}")

if not all([smtp_user, smtp_password]):
    print("\n❌ Missing SMTP credentials!")
    exit(1)

print("\n" + "-" * 70)
print("Testing SMTP connection...")
print("-" * 70)

try:
    # Create connection
    print(f"\n1. Connecting to {smtp_host}:{smtp_port}...")
    server = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
    print("   ✅ Connected")
    
    # Start TLS
    print("\n2. Starting TLS encryption...")
    server.starttls()
    print("   ✅ TLS enabled")
    
    # Login
    print("\n3. Authenticating...")
    server.login(smtp_user, smtp_password)
    print("   ✅ Authentication successful!")
    
    # Send test email
    print("\n4. Sending test email...")
    msg = MIMEText("This is a test email from ORBIT AI Platform.\n\nIf you receive this, your email configuration is working!")
    msg['Subject'] = '🎉 ORBIT Email Test - Success!'
    msg['From'] = from_email
    msg['To'] = smtp_user
    
    server.sendmail(from_email, [smtp_user], msg.as_string())
    print("   ✅ Email sent!")
    
    # Close connection
    server.quit()
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! Email configuration is working!")
    print("=" * 70)
    print(f"\n📬 Check your inbox at {smtp_user}")
    print("\n")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"\n❌ Authentication failed!")
    print(f"   Error: {str(e)}")
    print("\n💡 Troubleshooting:")
    print("   For Gmail (@gmail.com or institutional Gmail):")
    print("   1. Enable 2-Step Verification in Google Account")
    print("   2. Generate an App Password:")
    print("      • Go to: https://myaccount.google.com/apppasswords")
    print("      • Select 'Mail' and your device")
    print("      • Copy the 16-character password")
    print("      • Use that password in SMTP_PASSWORD")
    print("\n   For institutional email (@nith.ac.in):")
    print("   • Check if your institution uses Gmail")
    print("   • You may need to enable 'Less secure app access'")
    print("   • Or use an App Password (recommended)")
    
except smtplib.SMTPException as e:
    print(f"\n❌ SMTP Error: {str(e)}")
    
except TimeoutError:
    print(f"\n❌ Connection timed out!")
    print("\n💡 Possible causes:")
    print("   • Firewall blocking port 587")
    print("   • Network restrictions")
    print("   • VPN interference")
    print("   • Try port 465 with SSL instead")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print(f"   Type: {type(e).__name__}")

print("\n")
