"""
Email Test with SSL (Port 465)
Alternative to TLS on port 587
"""

import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment
load_dotenv('.env.local')

print("=" * 70)
print("📧 EMAIL TEST - SSL (Port 465)")
print("=" * 70)

# Get configuration
smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
smtp_port = 465  # SSL port
smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')
from_email = os.getenv('FROM_EMAIL', smtp_user)

print(f"\nConfiguration:")
print(f"  Host: {smtp_host}")
print(f"  Port: {smtp_port} (SSL)")
print(f"  User: {smtp_user}")
print(f"  Password: {'*' * len(smtp_password) if smtp_password else 'Not set'}")
print(f"  From: {from_email}")

if not all([smtp_user, smtp_password]):
    print("\n❌ Missing SMTP credentials!")
    exit(1)

print("\n" + "-" * 70)
print("Testing SMTP connection with SSL...")
print("-" * 70)

try:
    # Create SSL connection
    print(f"\n1. Connecting to {smtp_host}:{smtp_port} with SSL...")
    server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30)
    print("   ✅ Connected with SSL")
    
    # Login
    print("\n2. Authenticating...")
    server.login(smtp_user, smtp_password)
    print("   ✅ Authentication successful!")
    
    # Send test email
    print("\n3. Sending test email...")
    msg = MIMEText("This is a test email from ORBIT AI Platform using SSL.\n\nIf you receive this, your email configuration is working!")
    msg['Subject'] = '🎉 ORBIT Email Test - SSL Success!'
    msg['From'] = from_email
    msg['To'] = smtp_user
    
    server.sendmail(from_email, [smtp_user], msg.as_string())
    print("   ✅ Email sent!")
    
    # Close connection
    server.quit()
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! Email configuration is working with SSL!")
    print("=" * 70)
    print(f"\n📬 Check your inbox at {smtp_user}")
    print("\n💡 Update .env.local to use port 465 for production")
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
    print("   • Firewall blocking port 465")
    print("   • Network restrictions")
    print("   • VPN interference")
    print("   • Institution blocking external SMTP")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print(f"   Type: {type(e).__name__}")

print("\n")
