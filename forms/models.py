from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import RegexValidator

# Create your models here.
@python_2_unicode_compatible	
class Maintenance(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.IntegerField(default=1)
    code = models.CharField(max_length=10,validators=[RegexValidator(regex='^.{10}$', message='Length has to be 4', code='nomatch')])
    def __str__(self):
		return "[user : "+unicode(self.user)+", status: "+unicode(self.status)+"]"

#@python_2_unicode_compatible	
class ScheduleAndPIC(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    pic = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
	
#@python_2_unicode_compatible	
class LocationAndDevice(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    fiberhood = models.CharField(max_length=30, blank=True)
    site = models.CharField(max_length=30)
    cluster = models.CharField(max_length=30, blank=True)
    floor_slash_block = models.CharField(max_length=30, blank=True)
    device_id = models.CharField(max_length=30)
    device_port = models.TextField(max_length=30)

#@python_2_unicode_compatible	
class Activity(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    symptom_of_problem = models.TextField()
    action_plan = models.TextField()
    estimation_duration = models.CharField(max_length=30)
    document = models.FileField()

#@python_2_unicode_compatible	
class CustomerImpact(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    count_of_customer_impact = models.CharField(max_length=30)
    network_interrupt = models.TextField()
    service_interrupt = models.TextField()

#@python_2_unicode_compatible	
class DeviceReplacement(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    old_device_id = models.CharField(max_length=30, blank=True) 
    old_device_type = models.CharField(max_length=30, blank=True)
    old_serial_number = models.CharField(max_length=30, blank=True)
    old_barcode = models.CharField(max_length=30, blank=True)
    new_device_id = models.CharField(max_length=30, blank=True)
    new_device_type = models.CharField(max_length=30, blank=True)
    new_serial_number = models.CharField(max_length=30, blank=True)
    new_barcode = models.CharField(max_length=30, blank=True)