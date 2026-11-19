from django.core.mail import send_mail

def send_email_verification_otp(recipient, otp, first_name):
    return send_mail(
        subject="Verify your email",
        message=f"""
Dear { first_name },

Thank you for registering with Deplix.

To complete your registration and verify your email address, please use the One-Time Password (OTP) provided below:

        **{ otp }**

This OTP is valid for 5 minutes and can only be used once. For security purposes, please do not share this code with anyone.

If you did not initiate this registration, please disregard this email.

Kind regards,
Deplix Support Team
""",
        from_email=None,
        recipient_list=[recipient],
        fail_silently=False
    )

def send_password_reset_otp(recipient, otp, first_name):
    return send_mail(
        subject="Password Reset Otp",
        message=f"""
Dear { first_name },

To complete your password reset , please use the One-Time Password (OTP) provided below:

        **{ otp }**

This OTP is valid for 5 minutes and can only be used once. For security purposes, please do not share this code with anyone.

If you did not initiate this registration, please disregard this email.

Kind regards,
Deplix Support Team
""",
        from_email=None,
        recipient_list=[recipient],
        fail_silently=False
    )