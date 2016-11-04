from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import F
from itertools import chain

def staff_check(user):
    return user.is_staff


@login_required(login_url='forms:login')
def home(request):
    return redirect('/forms/display')


@login_required(login_url='forms:login')
@user_passes_test(staff_check)
def approve(request):
    maintenance = Maintenance.objects.get(id=request.POST.get('maintenance_id'))
    username = request.user.username
    maintenance_code = str(maintenance.code)
    if request.POST.get('approve'):
        maintenance.status = 2
        maintenance.save()
        messages.success(request, 'Maintenance Application was Approved')
        recipient_mail = maintenance.user.email
        send_mail(
            'Approval',
            'Hi, we glad to tell you that your maintenance form with the code = '+maintenance_code+ ' has been approved by '+username+ '.',
            'mailbotfadli@gmail.com',
            [recipient_mail],
            fail_silently=False,
        )
    else:
        maintenance.status = 3
        maintenance.save()
        messages.error(request, 'Maintenance Application was Rejected')
        recipient_mail = maintenance.user.email
        send_mail(
            'Rejection',
            'Hi, we regret to tell you that your maintenance form with the code = '+maintenance_code+ ' has been rejected by '+ username+ '. Please create your new form.',
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


def checking(var):
    return ((var is not None) and (var != ''))


@login_required(login_url='forms:login')
def display(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    status = request.POST.get('status')
    start_date_checking = checking(start_date)
    end_date_checking = checking(end_date)
    status_checking = checking(status)
    if request.user.is_staff:
        if start_date_checking and end_date_checking and status_checking: 
            if status == '0':
                schedule_and_pic_set = ScheduleAndPIC.objects.filter(start_date__gte=start_date, end_date__lte=end_date).order_by('maintenance__status','start_date').annotate(code=F('maintenance__code'),site=F('maintenance__locationanddevice__site'),device_id=F('maintenance__locationanddevice__device_id'))
            else:
                schedule_and_pic_set = ScheduleAndPIC.objects.filter(start_date__gte=start_date, end_date__lte=end_date, maintenance__status=status).order_by('maintenance__status','start_date').annotate(code=F('maintenance__code'),site=F('maintenance__locationanddevice__site'),device_id=F('maintenance__locationanddevice__device_id'))
        elif status_checking and (status != '0'):
            result_1 = ScheduleAndPIC.objects.filter(maintenance__status=status,start_date__gte=datetime.date.today()).order_by('maintenance__status','start_date').annotate(code=F('maintenance__code'),site=F('maintenance__locationanddevice__site'),device_id=F('maintenance__locationanddevice__device_id'))
            result_2 = ScheduleAndPIC.objects.filter(maintenance__status=status,start_date__lt=datetime.date.today()).order_by('maintenance__status','-start_date').annotate(code=F('maintenance__code'),site=F('maintenance__locationanddevice__site'),device_id=F('maintenance__locationanddevice__device_id'))
            schedule_and_pic_set = list(chain(result_1, result_2))
        else:   
            result_1 = ScheduleAndPIC.objects.filter(start_date__gte=datetime.date.today()).order_by('maintenance__status','start_date').annotate(code=F('maintenance__code'),site=F('maintenance__locationanddevice__site'),device_id=F('maintenance__locationanddevice__device_id'))
            result_2 = ScheduleAndPIC.objects.filter(start_date__lt=datetime.date.today()).order_by('maintenance__status','-start_date').annotate(code=F('maintenance__code'),site=F('maintenance__locationanddevice__site'),device_id=F('maintenance__locationanddevice__device_id'))
            schedule_and_pic_set = list(chain(result_1, result_2))
    else:
        if start_date_checking and end_date_checking and status_checking:
            if status == '0':
                schedule_and_pic_set = ScheduleAndPIC.objects.filter(maintenance__user_id=request.user.id,start_date__gte=start_date, end_date__lte=end_date).order_by('maintenance__status','start_date').annotate(code=F('maintenance__code'),site=F('maintenance__locationanddevice__site'),device_id=F('maintenance__locationanddevice__device_id'))
            else:
                schedule_and_pic_set = ScheduleAndPIC.objects.filter(maintenance__user_id=request.user.id, start_date__gte=start_date, end_date__lte=end_date, maintenance__status=status).order_by('maintenance__status','start_date').annotate(code=F('maintenance__code'),site=F('maintenance__locationanddevice__site'),device_id=F('maintenance__locationanddevice__device_id'))
        elif status_checking and (status != '0'):
            result_1 = ScheduleAndPIC.objects.filter(maintenance__user_id=request.user.id, maintenance__status=status, start_date__gte=datetime.date.today()).order_by('maintenance__status','start_date').annotate(code=F('maintenance__code'),site=F('maintenance__locationanddevice__site'),device_id=F('maintenance__locationanddevice__device_id'))
            result_2 = ScheduleAndPIC.objects.filter(maintenance__user_id=request.user.id, maintenance__status=status, start_date__lt=datetime.date.today()).order_by('maintenance__status','-start_date').annotate(code=F('maintenance__code'),site=F('maintenance__locationanddevice__site'),device_id=F('maintenance__locationanddevice__device_id'))
            schedule_and_pic_set = list(chain(result_1, result_2))
        else:   
            result_1 = ScheduleAndPIC.objects.filter(maintenance__user_id=request.user.id,start_date__gte=datetime.date.today()).order_by('maintenance__status','start_date').annotate(code=F('maintenance__code'),site=F('maintenance__locationanddevice__site'),device_id=F('maintenance__locationanddevice__device_id'))
            result_2 = ScheduleAndPIC.objects.filter(maintenance__user_id=request.user.id,start_date__lt=datetime.date.today()).order_by('maintenance__status','-start_date').annotate(code=F('maintenance__code'),site=F('maintenance__locationanddevice__site'),device_id=F('maintenance__locationanddevice__device_id'))
            schedule_and_pic_set = list(chain(result_1, result_2))
    page = request.GET.get('page', 1)
    paginator = Paginator(schedule_and_pic_set, 10)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)    
    return render(request, 'forms/display.html', {'schedule_and_pic_set' : result})


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
            maintenance_obj.code = str(datetime.date.today().strftime('%y%m%d'))+str(maintenance_obj.id+1000)
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


@login_required(login_url='forms:login')    
def reschedule(request):  
    if request.method == "POST" and request.POST.get('save'):
        maintenance_id = request.POST.get('maintenance_id')
        maintenance = Maintenance.objects.get(id=maintenance_id)
        schedule_and_pic_obj = ScheduleAndPIC.objects.get(maintenance_id=maintenance_id)
        schedule_and_pic_form = ScheduleAndPICForm(request.POST, instance=schedule_and_pic_obj)
        is_valid = schedule_and_pic_form.is_valid()
        username = request.user.username
        maintenance_code = str(maintenance.code)
        if is_valid is True:
            schedule_and_pic_form.save()
            new_schedule = str(schedule_and_pic_obj.start_date)+' '+str(schedule_and_pic_obj.start_time)+' till '+str(schedule_and_pic_obj.end_date)+' '+str(schedule_and_pic_obj.end_time)+'.'
            messages.success(request, 'Maintenance Application was Rescheduled')
            recipient_mail = maintenance.user.email
            send_mail(
                'Reschedule',
                'Hi, your maintenance form with the code = '+maintenance_code+ ' has been rescheduled by '+username+ '. The maintenance will be held on '+new_schedule+ ' Please check your form for the detail.',
                'mailbotfadli@gmail.com',
                [recipient_mail],
                fail_silently=False,
            )
            return redirect('/forms/display')
        return render(request, 'forms/form.html', {'schedule_and_pic_form' : schedule_and_pic_form, 'reschedule' : True, 'maintenance_id' : maintenance_id})  
    else:
        maintenance_id = request.POST.get('maintenance_id')
        schedule_and_pic_obj = ScheduleAndPIC.objects.get(maintenance_id=maintenance_id)
        schedule_and_pic_form = ScheduleAndPICForm(instance=schedule_and_pic_obj)      
        return render(request, 'forms/form.html', {'schedule_and_pic_form' : schedule_and_pic_form, 'reschedule' : True, 'maintenance_id' : maintenance_id})   


@login_required(login_url='forms:login')    
def profile(request):       
    if request.method == "POST" and request.POST.get('save'):
        user_form = UserForm(request.POST, instance=request.user)
        is_valid = user_form.is_valid() and check_password(request)
        if is_valid is True:
            user_obj = user_form.save(commit=False)
            if bool(user_form.data.get('new_password')):
                user_obj.set_password(user_form.data.get('new_password'))
            else:
                user_obj.set_password(user_form.data.get('password'))    
            user_obj.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Your Profile has been Successfully Updated')
            return redirect('/forms/display')
        return render(request, 'forms/form.html', {'user_form' : user_form})  
    else:
        user_form = UserForm(instance=request.user)      
        return render(request, 'forms/form.html', {'user_form' : user_form})   

def check_password(request):
    new_password = request.POST.get('new_password')
    re_new_password = request.POST.get('re_new_password')
    return new_password == re_new_password
