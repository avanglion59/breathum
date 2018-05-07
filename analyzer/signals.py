from django.db.models.signals import pre_save
from django.dispatch import receiver

from analyzer.models import DataItem


@receiver(pre_save, sender=DataItem)
def blockchain_hasher(sender, instance, *args, **kwargs):
    instance.previous_hash = sender.blockchain_hash(sender.objects.order_by('timestamp').last())
