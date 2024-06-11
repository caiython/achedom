from django.db import models
from django.core.validators import RegexValidator


class ServiceOrder(models.Model):
    id = models.AutoField(primary_key=True)

    operator = models.CharField(max_length=255)

    service_order_code = models.CharField(
        max_length=11,
        validators=[RegexValidator(
            regex=r'^\w{4}-\w{6}$',
            message='O código do pedido de serviço deve estar no formato XXXX-XXXXXX',
            code='invalid_service_order_code'
        )]
    )
    creation_datetime = models.DateTimeField()
    user = models.CharField(max_length=255)
    customer = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    whatsapp_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.service_order_code} - {self.subject}"

    def to_dict(self):
        return {field.name: (getattr(self, field.name).isoformat() if isinstance(getattr(self, field.name), models.DateTimeField) else getattr(self, field.name)) for field in self._meta.fields}
