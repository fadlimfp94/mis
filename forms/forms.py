from django.forms import *
from .models import * 
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User
import datetime

class ScheduleAndPICForm(ModelForm):
    class Meta:
        model = ScheduleAndPIC
        fields = ('start_date', 'end_date','start_time','end_time','pic','phone_number','department')
        widgets = {'start_date': DateInput(attrs={'type':'date','class' : 'form-control'}),'end_date': DateInput(attrs={'type':'date','class' : 'form-control'}),
	               'start_time': TimeInput(attrs={'type':'time','class' : 'form-control'}),'end_time': TimeInput(attrs={'type':'time','class' : 'form-control'}),
	               'phone_number' : TextInput(attrs={'pattern':'[0-9]+','class' : 'form-control'}), 'pic' : TextInput(attrs={'class' : 'form-control'}), 'department' : TextInput(attrs={'class' : 'form-control'})}
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
    def __init__(self, *args, **kwargs):
        super(ScheduleAndPICForm,self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['autofocus'] = 'on'
        self.fields['start_date'].label = "Start Date *"
        self.fields['end_date'].label = "End Date *"
        self.fields['start_time'].label = "Start Time *"
        self.fields['end_time'].label = "End Time *"
        self.fields['pic'].label = "PIC *"
        self.fields['phone_number'].label = "Phone Number *"
        self.fields['department'].label = "Department *"


            		
class LocationAndDeviceForm(ModelForm):
    class Meta:
        model = LocationAndDevice
        fields = ('fiberhood', 'site','cluster','floor_slash_block','device_id','device_port')
        widgets = {'fiberhood': TextInput(attrs={'class' : 'form-control'}),'site': TextInput(attrs={'class' : 'form-control'}),
                   'cluster': TextInput(attrs={'class' : 'form-control'}),'floor_slash_block': TextInput(attrs={'class' : 'form-control'}),
                   'device_id' : TextInput(attrs={'class' : 'form-control'}), 'device_port' : Textarea(attrs={'class' : 'form-control'})}
	labels = {'floor_slash_block': _('Floor / Block'),'site': _('Site *'), 'device_id': _('Device ID *'), 'device_port': _('Device Port *')}


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = ('symptom_of_problem','action_plan','estimation_duration','document')	
        widgets = {'symptom_of_problem' : Textarea(attrs={'class' : 'form-control'}), 'action_plan' : Textarea(attrs={'class' : 'form-control'}), 
                'estimation_duration' : TextInput(attrs={'class' : 'form-control'}), 'document' : FileInput(attrs={'class' : 'form-control'})        
        }	
	labels = {'document': _('MOP Document *'), 'symptom_of_problem': _('Symptom of Problem *'), 'action_plan': _('Action Plan *'),'estimation_duration': _('Estimation Duration *')}

class CustomerImpactForm(ModelForm):
    class Meta:
        model = CustomerImpact
        fields = ('count_of_customer_impact', 'network_interrupt','service_interrupt')
        widgets = {'count_of_customer_impact' : TextInput(attrs={'class' : 'form-control'}), 'network_interrupt' : Textarea(attrs={'class' : 'form-control'}),
                    'service_interrupt' : Textarea(attrs={'class' : 'form-control'})
        }    
    def __init__(self, *args, **kwargs):
        super(CustomerImpactForm,self).__init__(*args, **kwargs)
        self.fields['count_of_customer_impact'].label = "Count of Customer Impact *"
        self.fields['network_interrupt'].label = 'Network Interrupt *'
        self.fields['service_interrupt'].label = 'Service Interrupt *'

class DeviceReplacementForm(ModelForm):
    class Meta:
        model = DeviceReplacement
        fields = ('old_device_id', 'old_device_type','old_serial_number','old_barcode','new_device_id','new_device_type','new_serial_number','new_barcode')		
        widgets = {'old_device_id' : TextInput(attrs={'class' : 'form-control'}), 'old_device_type' : TextInput(attrs={'class' : 'form-control'}), 'old_serial_number' : TextInput(attrs={'class' : 'form-control'}), 'old_barcode' : TextInput(attrs={'class' : 'form-control'}),
                    'new_device_id' : TextInput(attrs={'class' : 'form-control'}), 'new_device_type' : TextInput(attrs={'class' : 'form-control'}), 'new_serial_number' : TextInput(attrs={'class' : 'form-control'}), 'new_barcode' : TextInput(attrs={'class' : 'form-control'})
        }
    labels = {'old_device_id': _('Old Device ID'), 'old_serial_number': _('Old Serial Number'), 'old_device_type': _('Old Device Type'), 'old_barcode': _('Old Barcode'),
            'new_device_type': _('New Device Type'), 'new_device_id': _('New Device ID'), 'new_serial_number': _('New Serial Number'), 'new_barcode': _('New Barcode')
    }    

class LoginForm(AuthenticationForm):
    username = CharField(label="Username", max_length=30, 
                               widget=TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder':'Username...'}))
    password = CharField(label="Password", max_length=30, 
                               widget=PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder':'Password...'}))
    def __init__(self, *args, **kwargs):
        super(LoginForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = 'on'
        self.error_messages['invalid_login'] = "Your username and password didn't match. Please try again."


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name', 'password')     
        widgets = {'username' : TextInput(attrs={'autofocus' : '','class' : 'form-control form-username', 'id' :'form-username', 'placeholder' : 'Username...'}), 'email' : EmailInput(attrs={'class' : 'form-control'}), 'first_name' : TextInput(attrs={'class' : 'form-control'}), 'last_name' : TextInput(attrs={'class' : 'form-control'}),
                     'password' : PasswordInput(attrs={'class' : 'form-control form-password', 'id' :'form-password', 'placeholder' : 'Password...'})}
        help_texts = {
            'username': None,
        }
    def clean(self):
        username = self.cleaned_data.get("username")
        user = User.objects.get(username=username)
        password =  self.cleaned_data.get("password")
        if not user.check_password(password):
            msg = "Current Password wrong"
            self._errors["password"] = self.error_class([msg])
    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True               