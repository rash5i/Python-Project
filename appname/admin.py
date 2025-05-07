from django.contrib import admin
from .models import Courses, Registration, Opted_course, Temp_otp

# Register your models here.
admin.site.register(Courses)
admin.site.register(Registration)
admin.site.register(Opted_course)
admin.site.register(Temp_otp)


