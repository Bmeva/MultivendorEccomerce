from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings



from django.utils.http import urlsafe_base64_decode
from accounts.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def detectuser(user):
    if user.role ==1:
        redirecturl = 'vendordashboard'
        return redirecturl
    elif user.role == 2:
        redirecturl = 'customerdashboard'
        return redirecturl
    elif user.role == None and user.is_superadmin:
        redirecturl ='/admin'
        return redirecturl

def send_verification_email(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL 
    current_site = get_current_site(request)
    mail_subject = "Please activate your account"
    message = render_to_string('accounts/emails/account_verification_email.html', {

        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),

    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()


def activate(request, uidb64, token):
    #activating the user by setting the is_active status to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations your account has been activated")
        return redirect('myaccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myaccount')
    

def send_password_reset_email(request, user):
    
    from_email = settings.DEFAULT_FROM_EMAIL 
    current_site = get_current_site(request)
    mail_subject = "reset your password"
    message = render_to_string('accounts/emails/reset_password_email.html', {

        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),

    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()



def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    if(isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.content_subtype = "html"
    mail.send()

    return

