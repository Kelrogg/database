from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import *

# from django.contrib import admin

# from .models import *


# class TreatmentInline(admin.TabularInline):
#     model = Treatment
#     extra = 0


# @admin.register(Diagnosis)
# class DiagnosesAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Patient)
# class PatientAdmin(admin.ModelAdmin):
#     inlines = [TreatmentInline]


# @admin.register(Treatment)
# class Treatment(admin.ModelAdmin):
#     list_display = ["get_snapshot_for_admin", "patient"]


# @admin.register(TemporaryContraindications)
# class TemporaryContraindications(admin.ModelAdmin):
#     pass


# @admin.register(Doctor)
# class Doctor(admin.ModelAdmin):
#     pass


# @admin.register(RecommendText)
# class RecommendText(admin.ModelAdmin):
#     pass


# @admin.register(NeuronetPrediction)
# class NeuronetPrediction(admin.ModelAdmin):
#     inlines = [TreatmentInline]


# class FAQItemInline(admin.TabularInline):
#     model = FAQItem
#     extra = 1


# @admin.register(FAQ)
# class FAQ(admin.ModelAdmin):
#     inlines = [FAQItemInline]


# admin.site.site_header = 'Admin-panel'
# admin.site.index_title = 'Databases'

@admin.register(Admin)
class Admin(admin.ModelAdmin):
    pass

@admin.register(Prisoner)
class Prisoner(admin.ModelAdmin):
    pass

class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)