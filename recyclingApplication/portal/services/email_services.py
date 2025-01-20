import sendgrid
import os
from sendgrid.helpers.mail import Mail, To, Personalization, Email
from django.conf import settings

class EmailService:
  def __init__(self):
    self.sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        
  def send_welcome_email(self, instance):
        self.sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        print(instance.status)
        
        email = Mail(
            from_email=settings.SENDGRID_EMAIL_FROM,
            to_emails=To(instance.email)
        )

        template_id = settings.SENDGRID_REQUEST_SUBMIT_EMAIL
        email.template_id = template_id

        personalization = Personalization()
        personalization.add_to(Email(instance.email))
        personalization.dynamic_template_data = {
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "status": instance.status,
            "token": instance.token,
            "address": (f"{instance.address} {instance.city} {instance.state}"),
            "subject": "Thank you for your pickup request!"
        }

        email.add_personalization(personalization)

        try:
            response = self.sg.send(email)
            print(f"Email sent to {instance.email} with status code {response.status_code}")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")