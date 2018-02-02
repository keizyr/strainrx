import calendar
import time

import sendgrid
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from sendgrid.helpers.mail import *

from web.common import html


class EmailService:
    host = settings.HOST

    basic_email_subject = 'StrainRx: {0}'
    basic_email_with_link_pattern = '<html><body><div style="font-size: 18px">{text} ' \
                                    '<a href="{link_url}">link</a>.</div></body></html>'

    header_logo_url = staticfiles_storage.url('images/logo_hr.png')
    envelope_image_url = staticfiles_storage.url('images/email-envelope.png')
    leaf_image_url = staticfiles_storage.url('images/favicon.png')

    @staticmethod
    def get_client():
        return sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

    def send_confirmation_email(self, user):
        sg = self.get_client()

        confirmation_url = '{host}{url}'.format(host=settings.HOST,
                                                url=reverse('businesses:confirm_email', kwargs={'uid': user.id}))

        from_email = Email(settings.DEFAULT_FROM_EMAIL)
        to_email = Email(user.email)
        subject = self.basic_email_subject.format('Verify Your Email')

        html_template = render_to_string('emails/user_consumer_confirmation_email.html', {
            'confirmation_url': confirmation_url,
            'sent_to': user.email,
            'header_logo_url': self.header_logo_url,
            'envelope_image_url': self.envelope_image_url,
            'leaf_image_url': self.leaf_image_url
        })

        html_content = Content('text/html', html_template)

        m = Mail(from_email, subject, to_email, html_content)
        return sg.client.mail.send.post(request_body=m.get())

    def send_menu_update_request_email(self, update_request):
        sg = self.get_client()

        location = update_request.business_location
        user = update_request.user
        message = update_request.message

        from_email = Email(settings.DEFAULT_FROM_EMAIL)
        to_email = Email(location.location_email)

        subject = 'Menu Update Request'

        html_template = render_to_string('emails/business_menu_update_request.html', {
            'business_location': location,
            'user': user,
            'header_logo_url': staticfiles_storage.url('images/logo_hr.png'),
            'envelope_image_url': staticfiles_storage.url('images/email-envelope.png'),
            'message': html.sanitize(message.replace('\n', '<br>')),
            'location_url': settings.HOST + location.urls.get('dispensary'),
            'login_url': settings.HOST + reverse('account_login'),
            'claim_url': settings.HOST + '/claim/',
            'update_date_url': settings.HOST + reverse('businesses:confirm_menu',
                                                       kwargs={'secret_key': update_request.secret_key}),
        })
        html_content = Content('text/html', html_template)

        # This should probably be a bcc, but sendgrid has some weird problems
        # with that.
        if not settings.DEBUG:
            m = Mail(from_email, subject, from_email, html_content)
            sg.client.mail.send.post(request_body=m.get())

        m = Mail(from_email, subject, to_email, html_content)
        return sg.client.mail.send.post(request_body=m.get())

    def send_menu_update_request_served_email(self, update_request):
        sg = self.get_client()

        location = update_request.business_location
        user = update_request.user

        from_email = Email(settings.DEFAULT_FROM_EMAIL)
        to_email = Email(user.email)

        subject = 'Menu Update Request'

        html_template = render_to_string('emails/business_menu_update_request_served.html', {
            'business_location': location,
            'user': user,
            'header_logo_url': staticfiles_storage.url('images/logo_hr.png'),
            'envelope_image_url': staticfiles_storage.url('images/email-envelope.png'),
            'location_url': settings.HOST + location.urls.get('dispensary'),
        })
        html_content = Content('text/html', html_template)

        m = Mail(from_email, subject, to_email, html_content)

        # 10 min from now
        m.send_at = int(calendar.timegm(time.gmtime())) + 600

        return sg.client.mail.send.post(request_body=m.get())

    def send_business_claim_request_served_email(self, context):
        sg = self.get_client()

        from_email = Email(settings.DEFAULT_FROM_EMAIL)
        to_email = Email('alec@strainrx.co')

        subject = 'Business Claim Request'

        html_template = render_to_string('emails/business_claim_request.html', context)
        html_content = Content('text/html', html_template)

        m = Mail(from_email, subject, to_email, html_content)
        return sg.client.mail.send.post(request_body=m.get())
