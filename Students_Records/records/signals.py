from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import Records

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
