from django.contrib import admin
from .models import Maintenance, ScheduleAndPIC, LocationAndDevice, Activity, CustomerImpact, DeviceReplacement
# Register your models here.


admin.site.register(Maintenance)
admin.site.register(ScheduleAndPIC)
admin.site.register(LocationAndDevice)
admin.site.register(Activity)
admin.site.register(CustomerImpact)
admin.site.register(DeviceReplacement)