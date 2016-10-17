from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
# this login required decorator is to not allow to any  
# view without authenticating
@login_required(login_url='login/')
def home(request):
    return redirect('/forms/display')

@login_required(login_url='login/')	
def index(request):
    return HttpResponse("Hello, world. You're at the form index.")

@login_required(login_url='login/')
def approve(request):
    maintenance = Maintenance.objects.get(id=request.POST.get('maintenance_id'))
    maintenance.status = 1
    maintenance.save()
    messages.success(request, 'Maintenance Application was Approved')
    return redirect('/forms/display', message = 'maintenance application was approved')

@login_required(login_url='login/')
def reject(request):
    maintenance = Maintenance.objects.get(id=request.POST.get('maintenance_id'))
    maintenance.status = 2
    maintenance.save()
    messages.error(request, 'Maintenance Application was Rejected')
    return redirect('/forms/display')

@login_required(login_url='login/')
def detail(request):
    maintenance = Maintenance.objects.get(id=request.POST.get('maintenance_id'))
    schedule_and_pic = ScheduleAndPIC.objects.get(maintenance_id=maintenance.id)
    location_and_device = LocationAndDevice.objects.get(maintenance_id=maintenance.id)
    activity = Activity.objects.get(maintenance_id=maintenance.id)
    customer_impact = CustomerImpact.objects.get(maintenance_id=maintenance.id)
    device_replacement = DeviceReplacement.objects.get(maintenance_id=maintenance.id)
    return render(request, 'forms/detail.html', {'maintenance' : maintenance, 'schedule_and_pic' : schedule_and_pic, 'location_and_device' : location_and_device, 'activity' : activity, 'customer_impact' : customer_impact, 'device_replacement' : device_replacement})

@login_required(login_url='login/')
def display(request):
    maintenance_set = Maintenance.objects.all()
    schedule_and_pic_set = ScheduleAndPIC.objects.all()
    location_and_device_set = LocationAndDevice.objects.all()
    activity_set = Activity.objects.all()
    customer_impact_set = CustomerImpact.objects.all()
    device_replacement_set = DeviceReplacement.objects.all()
    return render(request, 'forms/display.html', {'maintenance_set' : maintenance_set, 'schedule_and_pic_set' : schedule_and_pic_set, 'location_and_device_set' : location_and_device_set, 'activity_set' : activity_set, 'customer_impact_set' : customer_impact_set, 'device_replacement_set' : device_replacement_set})

@login_required(login_url='login/')	
def create_form(request):  
    if request.method == "POST":
        schedule_and_pic_form = ScheduleAndPICForm(request.POST)
        location_and_device_form = LocationAndDeviceForm(request.POST)
        activity_form = ActivityForm(request.POST)
        customer_impact_form = CustomerImpactForm(request.POST)
        device_replacement_form = DeviceReplacementForm(request.POST)
        is_valid = schedule_and_pic_form.is_valid() and location_and_device_form.is_valid() and activity_form.is_valid() and customer_impact_form.is_valid() and device_replacement_form.is_valid()
        if is_valid is True:
            maintenance_obj = Maintenance.objects.get(user=(User.objects.get(id=1))) 
            schedule_and_pic_obj = schedule_and_pic_form.save(commit=False)
            schedule_and_pic_obj.maintenance = maintenance_obj
            schedule_and_pic_obj.save()
            location_and_device_obj = location_and_device_form.save(commit=False)
            location_and_device_obj.maintenance = maintenance_obj
            location_and_device_obj.save() 
            activity_obj = activity_form.save(commit=False)
            activity_obj.maintenance = maintenance_obj
            activity_obj.save()
            customer_impact_obj = customer_impact_form.save(commit=False)
            customer_impact_obj.maintenance = maintenance_obj
            customer_impact_obj.save()
            device_replacement_obj = device_replacement_form.save(commit=False)
            device_replacement_obj.maintenance = maintenance_obj
            device_replacement_obj.save()
            return HttpResponse("Hello, success")
    else:
        schedule_and_pic_form = ScheduleAndPICForm()
        location_and_device_form = LocationAndDeviceForm()
        activity_form = ActivityForm()
        customer_impact_form = CustomerImpactForm()
        device_replacement_form = DeviceReplacementForm()
    return render(request, 'forms/form.html', {'schedule_and_pic_form' : schedule_and_pic_form, 'location_and_device_form' : location_and_device_form, 'activity_form' : activity_form, 'customer_impact_form' : customer_impact_form, 'device_replacement_form' : device_replacement_form})
