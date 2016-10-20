from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.core.mail import send_mail


def staff_check(user):
    return user.is_staff

@login_required(login_url='forms:login')
def home(request):
    return redirect('/forms/display')


@login_required(login_url='forms:login')
@user_passes_test(staff_check)
def approve(request):
    maintenance = Maintenance.objects.get(id=request.POST.get('maintenance_id'))
    maintenance.status = 2
    maintenance.save()
    messages.success(request, 'Maintenance Application was Approved')
    recipient_mail = maintenance.user.email
    send_mail(
        'Approval',
        'Hi, we glad to tell you that your maintenance form with ID = '+str(maintenance.id)+ ' has been approved',
        'mailbotfadli@gmail.com',
        [recipient_mail],
        fail_silently=False,
    )
    return redirect('/forms/display')

@login_required(login_url='forms:login')
@user_passes_test(staff_check)
def reject(request):
    maintenance = Maintenance.objects.get(id=request.POST.get('maintenance_id'))
    maintenance.status = 3
    maintenance.save()
    messages.error(request, 'Maintenance Application was Rejected')
    recipient_mail = maintenance.user.email
    send_mail(
        'Rejection',
        'Hi, we regret to tell you that your maintenance form with ID = '+str(maintenance.id)+ ' has been rejected. Please create your new form.',
        'mailbotfadli@gmail.com',
        [recipient_mail],
        fail_silently=False,
    )
    return redirect('/forms/display')

@login_required(login_url='forms:login')
def detail(request):
    maintenance = Maintenance.objects.get(id=request.POST.get('maintenance_id'))
    schedule_and_pic = ScheduleAndPIC.objects.get(maintenance_id=maintenance.id)
    location_and_device = LocationAndDevice.objects.get(maintenance_id=maintenance.id)
    activity = Activity.objects.get(maintenance_id=maintenance.id)
    customer_impact = CustomerImpact.objects.get(maintenance_id=maintenance.id)
    device_replacement = DeviceReplacement.objects.get(maintenance_id=maintenance.id)
    return render(request, 'forms/detail.html', {'maintenance' : maintenance, 'schedule_and_pic' : schedule_and_pic, 'location_and_device' : location_and_device, 'activity' : activity, 'customer_impact' : customer_impact, 'device_replacement' : device_replacement})

@login_required(login_url='forms:login')
def display(request):
    if request.user.is_staff:
        schedule_and_pic_set = ScheduleAndPIC.objects.all().order_by('maintenance__status','-start_date')
    else:
        schedule_and_pic_set = ScheduleAndPIC.objects.filter(maintenance__user_id=request.user.id).order_by('maintenance__status','-start_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(schedule_and_pic_set, 10)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)    
    return render(request, 'forms/display.html', {'schedule_and_pic_set' : result})    
    #return render(request, 'forms/display.html', {'schedule_and_pic_set' : schedule_and_pic_set})

@login_required(login_url='forms:login')	
def create_form(request):  
    if request.method == "POST":
        schedule_and_pic_form = ScheduleAndPICForm(request.POST)
        location_and_device_form = LocationAndDeviceForm(request.POST)
        activity_form = ActivityForm(request.POST, request.FILES)
        customer_impact_form = CustomerImpactForm(request.POST)
        device_replacement_form = DeviceReplacementForm(request.POST)
        is_valid = schedule_and_pic_form.is_valid() and location_and_device_form.is_valid() and activity_form.is_valid() and customer_impact_form.is_valid() and device_replacement_form.is_valid()
        if is_valid is True:
            maintenance_obj = Maintenance(user=request.user, status=1)
            maintenance_obj.save()
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
            messages.success(request, 'Maintenance Application was Submitted')
            return redirect('/forms/display')
    else:
        schedule_and_pic_form = ScheduleAndPICForm()
        location_and_device_form = LocationAndDeviceForm()
        activity_form = ActivityForm()
        customer_impact_form = CustomerImpactForm()
        device_replacement_form = DeviceReplacementForm()
    return render(request, 'forms/form.html', {'schedule_and_pic_form' : schedule_and_pic_form, 'location_and_device_form' : location_and_device_form, 'activity_form' : activity_form, 'customer_impact_form' : customer_impact_form, 'device_replacement_form' : device_replacement_form})
