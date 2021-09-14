from django.db import models
from django.contrib.auth.models import AbstractUser
import json

from module import admin_config


class TBLUser(AbstractUser):
    reset_link = models.CharField(max_length=255, default='')
    permission = models.TextField(default=json.dumps({
        'max_active_bridges': admin_config.DEFAULT_MAX_ACTIVE_BRIDGES,
        'rate_limit_per_url': admin_config.DEFAULT_RATE_LIMIT_PER_URL,
        'allowed_frequency': admin_config.DEFAULT_ALLOWED_FREQUENCY,
        'available_bridges': admin_config.DEFAULT_AVAILABLE_BRIDGE
    }))

    class Meta:
        managed = False
        db_table = 'TBLUSER'


BRIDGE_TYPE = [
    (1, 'ws2wh'),
    (2, 'wh2ws'),
    (3, 'ws2api'),
    (4, 'api2ws'),
]


class TBLBridge(models.Model):
    user = models.ForeignKey(TBLUser, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, default='')
    type = models.IntegerField(choices=BRIDGE_TYPE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    api_calls = models.IntegerField(default=0)
    src_address = models.CharField(max_length=255, default='')
    dst_address = models.CharField(max_length=255, default='')
    format = models.TextField(blank=True, null=True)
    frequency = models.IntegerField(default=0)
    flush = models.IntegerField(default=0)
    file_format = models.CharField(max_length=255, default='')
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'TBLBRIDGE'


class TBLLog(models.Model):
    bridge = models.ForeignKey(TBLBridge, on_delete=models.CASCADE, blank=True, null=True)
    filename = models.CharField(max_length=255, default='')
    size = models.IntegerField(default=0)
    date_from = models.DateTimeField(auto_now_add=True)
    date_to = models.DateTimeField(auto_now_add=True)
    is_full = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'TBLLOG'


class TBLSetting(models.Model):
    server_setting = models.TextField(blank=True, null=True)
    max_active_bridges = models.IntegerField(default=0)
    rate_limit_per_url = models.IntegerField(default=0)
    allowed_frequency = models.TextField(blank=True, null=True)
    available_bridges = models.TextField(blank=True, null=True)
    smtp_setting = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TBLSETTING'