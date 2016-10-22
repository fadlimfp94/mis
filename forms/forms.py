from django.forms import *
from .models import * 
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm 
import datetime

class ScheduleAndPICForm(ModelForm):
    class Meta:
        model = ScheduleAndPIC
        fields = ('start_date', 'end_date','start_time','end_time','pic','phone_number','department')
        widgets = {'start_date': DateInput(attrs={'type':'date'}),'end_date': DateInput(attrs={'type':'date'}),
	               'start_time': TimeInput(attrs={'type':'time'}),'end_time': TimeInput(attrs={'type':'time'}),
	               'phone_number' : TextInput(attrs={'pattern':'[0-9]+'})}
    def clean(self):
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        today_date = datetime.date.today()
        if start_date < today_date:
            msg = "Start date should be greater than today date"
            self._errors["end_date"] = self.error_class([msg])
        if end_date < start_date:
            msg = "End date should be greater than start date"
            self._errors["end_date"] = self.error_class([msg])
        if start_date == end_date:
            start_time = self.cleaned_data.get("start_time")
            end_time = self.cleaned_data.get("end_time")
            if end_time < start_time:
                msg = "End time should be greater than start time when those two within one day"
                self._errors["end_date"] = self.error_class([msg])
                
            		
class LocationAndDeviceForm(ModelForm):
    class Meta:
        model = LocationAndDevice
        fields = ('fiberhood', 'site','cluster','floor_slash_block','device_id','device_port')
	labels = {'floor_slash_block': _('Floor / block'),}

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ('symptom_of_problem','action_plan','estimation_duration','document')		
	
class CustomerImpactForm(ModelForm):
    class Meta:
        model = CustomerImpact
        fields = ('count_of_customer_impact', 'network_interrupt','service_interrupt')

class DeviceReplacementForm(ModelForm):
    class Meta:
        model = DeviceReplacement
        fields = ('old_device_id', 'old_device_type','old_serial_number','old_barcode','new_device_id','new_device_type','new_serial_number','new_barcode')		

class LoginForm(AuthenticationForm):
    username = CharField(label="Username", max_length=30, 
                               widget=TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = CharField(label="Password", max_length=30, 
                               widget=PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))	