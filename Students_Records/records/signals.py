from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import Records
from django.contrib.auth.models import User
from django.core.mail import  send_mail

#triggered before saving a records.
@receiver(pre_save, sender=Records) 
def before_record_save(sender, instance, **kwargs):
    print(f" About to save Records[pre-save]:{instance.name}")

#Triggered after saving a records.
@receiver(post_save, sender=Records)
def after_record_save(sender, instance, created, ** kwargs):
    if created:
        print(f"New Records created[post-save]: {instance.name}")
    else:
        print(f"Records Updated[Post-Save]: {instance.name}")


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.username}")

        subject = "Welcome to Django Tutorial"
        message = f"Hi, {instance.username}, Thank you for enrolling in Django Course."
        from_email = 'lamabiraj482@gmail.com'
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print("Welcome email sent successfully.")
