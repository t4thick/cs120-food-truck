# Email Verification Setup Guide

This guide explains how to set up email verification with 4-digit codes for your Item7 Food Truck application.

## Overview

When enabled, users will receive a 4-digit verification code via email after logging in. They must enter this code to complete the login process. This adds an extra layer of security to your application.

## Features

- ✅ 4-digit verification codes sent via email
- ✅ Codes expire after 10 minutes
- ✅ Maximum 5 verification attempts per code
- ✅ Resend code functionality
- ✅ Graceful degradation (if email fails, login still works)
- ✅ Optional feature (can be disabled)

## Setup Instructions

### Step 1: Configure Environment Variables

Add the following to your `.env` file:

```env
# Enable email verification (set to "true" to enable)
EMAIL_VERIFICATION_ENABLED=true

# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
```

### Step 2: Gmail Setup (Recommended)

If using Gmail, you need to:

1. **Enable 2-Step Verification** on your Google account
   - Go to: https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Generate an App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "Item7 Food Truck" as the name
   - Copy the 16-character password

3. **Use the App Password in `.env`**
   ```env
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # Use the 16-char app password (spaces optional)
   ```

### Step 3: Other Email Providers

#### Outlook/Hotmail
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
FROM_EMAIL=your-email@outlook.com
```

#### Yahoo Mail
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@yahoo.com
```

#### Custom SMTP
Use your email provider's SMTP settings. Common ports:
- **587** (TLS/STARTTLS) - Recommended
- **465** (SSL) - Alternative
- **25** (Unencrypted) - Not recommended for production

### Step 4: Test the Setup

1. Start your Flask application:
   ```bash
   python app.py
   ```

2. Try logging in with a test account
3. Check your email for the verification code
4. Enter the code on the verification page

## How It Works

1. **User logs in** with email and password
2. **System generates** a random 4-digit code
3. **Code is stored** in memory (expires in 10 minutes)
4. **Email is sent** with the code
5. **User enters code** on verification page
6. **System validates** the code
7. **Login completes** if code is correct

## Security Features

- **Code Expiration**: Codes expire after 10 minutes
- **Attempt Limiting**: Maximum 5 failed attempts per code
- **Rate Limiting**: Login attempts are rate-limited (existing feature)
- **CSRF Protection**: Verification forms are protected against CSRF attacks
- **Secure Storage**: Codes are stored in memory (not in database)

## Disabling Email Verification

To disable email verification, set:

```env
EMAIL_VERIFICATION_ENABLED=false
```

Or simply don't set the variable (defaults to disabled).

When disabled, users will log in normally without email verification.

## Troubleshooting

### "Email service is not configured"
- Make sure `SMTP_USERNAME` and `SMTP_PASSWORD` are set in your `.env` file
- Restart your Flask application after changing environment variables

### "SMTP authentication failed"
- For Gmail: Make sure you're using an App Password, not your regular password
- Check that 2-Step Verification is enabled
- Verify your SMTP credentials are correct

### "Failed to send email"
- Check your internet connection
- Verify SMTP host and port are correct
- Check firewall settings
- Some email providers block SMTP from certain IPs

### Code not received
- Check spam/junk folder
- Verify email address is correct
- Check SMTP logs in `ft_management.log`
- Try resending the code

### Codes expire too quickly
- Default expiration is 10 minutes
- You can modify `CODE_EXPIRY_MINUTES` in `utils/verification.py`

## Production Considerations

For production environments:

1. **Use a dedicated email service** (SendGrid, Mailgun, AWS SES)
2. **Store codes in Redis** instead of memory (for multi-server deployments)
3. **Monitor email delivery rates**
4. **Set up email templates** for better branding
5. **Add email queue** for high-volume applications

## Code Customization

### Change Code Expiration Time

Edit `utils/verification.py`:
```python
CODE_EXPIRY_MINUTES = 15  # Change from 10 to 15 minutes
```

### Change Maximum Attempts

Edit `utils/verification.py`:
```python
"max_attempts": 3  # Change from 5 to 3 attempts
```

### Customize Email Template

Edit `utils/email_service.py` in the `send_verification_code` method to customize the email body.

## Support

If you encounter issues:
1. Check the application logs: `ft_management.log`
2. Verify all environment variables are set correctly
3. Test SMTP connection manually using Python's `smtplib`
4. Review the error messages for specific guidance

