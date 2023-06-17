from django.contrib import admin
from .models import User,UserProfile
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm

class UserAdminConfig(UserAdmin):
 #   add_form = CustomUserCreationForm
    model = User
    filter_horizontal = ()
    search_fields = ('email','username','first_name','last_name')
    list_filter = ()
    list_display = ('email','username','first_name','last_name','is_active','is_staff')
    ordering = ('-date_joined',)
    fieldsets = ()

    def add_view(self, request, form_url='', extra_context=None):
        self.form = self.add_form
        return super().add_view(request, form_url, extra_context)


# Register your models here.
admin.site.register(User,UserAdminConfig)
admin.site.register(UserProfile)