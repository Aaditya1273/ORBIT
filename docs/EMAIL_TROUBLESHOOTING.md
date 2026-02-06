# 📧 Email Configuration Troubleshooting

## Current Issue: Connection Timeout

Both port 587 (TLS) and port 465 (SSL) are timing out when trying to connect to Gmail's SMTP server.

## Possible Causes

### 1. **Firewall/Antivirus Blocking**
Your Windows firewall or antivirus software may be blocking outbound SMTP connections.

**Solution:**
- Temporarily disable Windows Firewall to test
- Add Python to firewall exceptions
- Check antivirus SMTP/email protection settings

### 2. **Network Restrictions**
Your institution (NITH) or ISP may be blocking SMTP ports.

**Solution:**
- Try from a different network (mobile hotspot)
- Contact NITH IT department about SMTP access
- Use institution's SMTP server if available

### 3. **Gmail App Password Required**
If your @nith.ac.in email uses Google Workspace, you need an App Password.

**Solution:**
1. Go to: https://myaccount.google.com/apppasswords
2. Sign in with your NITH account
3. Select "Mail" and your device
4. Copy the 16-character password (no spaces)
5. Update `SMTP_PASSWORD` in `.env.local`

### 4. **Institution Email Server**
NITH may have its own email server that you should use instead of Gmail.

**Solution:**
Contact NITH IT department and ask for:
- SMTP server address
- SMTP port
- Authentication requirements

## Quick Tests

### Test 1: Check Port Connectivity
```bash
# Test if port 587 is reachable
telnet smtp.gmail.com 587

# Test if port 465 is reachable
telnet smtp.gmail.com 465
```

If telnet fails, the port is blocked.

### Test 2: Try Mobile Hotspot
1. Connect your laptop to mobile hotspot
2. Run: `python test_email_simple.py`
3. If it works, your network is blocking SMTP

### Test 3: Use Alternative SMTP
Try a different email service temporarily:

**Outlook/Hotmail:**
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-outlook-email@outlook.com
SMTP_PASSWORD=your-password
FROM_EMAIL=your-outlook-email@outlook.com
```

**SendGrid (Free tier - 100 emails/day):**
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
FROM_EMAIL=your-verified-sender@domain.com
```

## Recommended Solutions

### Option 1: Use SendGrid (Recommended for Development)
1. Sign up at: https://sendgrid.com/free/
2. Verify your sender email
3. Get API key
4. Update `.env.local`:
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
FROM_EMAIL=your-verified-email@domain.com
```

### Option 2: Use Mailtrap (Testing Only)
1. Sign up at: https://mailtrap.io/
2. Get SMTP credentials
3. Update `.env.local`:
```env
SMTP_HOST=smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USER=your-mailtrap-user
SMTP_PASSWORD=your-mailtrap-password
FROM_EMAIL=test@orbit.ai
```

### Option 3: Disable Email (Temporary)
For now, you can run ORBIT without email:
1. Email features will be skipped
2. Platform will still work
3. Fix email later when needed

## Testing Commands

```bash
# Test with TLS (port 587)
python test_email_simple.py

# Test with SSL (port 465)
python test_email_ssl.py

# Verify full setup
python verify_setup.py
```

## Next Steps

1. **Immediate**: Try mobile hotspot to confirm network issue
2. **Short-term**: Sign up for SendGrid free tier
3. **Long-term**: Contact NITH IT for proper SMTP access

## Platform Status

**Good News:** Email is NOT required for core functionality!

You can still:
- ✅ Register users
- ✅ Login/logout
- ✅ Create goals
- ✅ Get AI interventions
- ✅ View analytics

Email is only needed for:
- ⚠️ Welcome emails
- ⚠️ Password reset
- ⚠️ Email notifications

**You can launch without email and add it later!**
