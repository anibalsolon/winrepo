
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template import loader

import winrepo.settings as settings


def build_email(subject_template_name, email_template_name, html_email_template_name, context=None):

    subject = loader.render_to_string(subject_template_name, context)
    subject = settings.EMAIL_SUBJECT_PREFIX + ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, settings.EMAIL_FROM, None)
    html_email = loader.render_to_string(html_email_template_name, context)
    email_message.attach_alternative(html_email, 'text/html')

    return email_message


def user_create_confirm_email(
    user, token_generator=default_token_generator,
    subject_template_name='registration/signup_confirm_email_subject.txt',
    email_template_name='registration/signup_confirm_email_body.txt',
    html_email_template_name='registration/signup_confirm_email_body.html'
):
    context = {
        "user": user,
        "uid": urlsafe_base64_encode(force_bytes(user.email)),
        "token": token_generator.make_token(user)
    }

    message = build_email(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context
    )
    message.to = [user.email]
    return message

