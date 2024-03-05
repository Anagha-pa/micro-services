from django.conf import settings
from django.core.mail import send_mail

def send_otp_via_email(email,otp):
    subject = 'Account Verification Email'
    message = f'Your OTP is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)