from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from account.models import USER


class USERAdmin(UserAdmin):
    fieldsets = (
        ("اطلاعات کاربری", {'fields': ('username', 'password', 'pass_per_save')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'gender', 'avatar', 'familier', 'email')}),
        (('اطلاعات کاربردی'), {'fields': ('phone_number', 'custom_user_id', 'code_send', 'email_sended')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ("pass_per_save",)
    add_fieldsets = (
        ("اطلاعات کاربری", {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'phone_number', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser',)
    list_display_links = ('username', 'phone_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'gender')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            self.readonly_fields = ("pass_per_save",)
            self.fieldsets = (
                ("اطلاعات کاربری", {'fields': ('username', 'password', 'pass_per_save')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'gender', 'avatar', 'familier', 'email')}),
                (('اطلاعات کاربردی'), {'fields': ('phone_number', 'custom_user_id', 'code_send', 'email_sended')}),
                (_('Permissions'), {
                    'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                }),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
            )
        return request.user.is_superuser or (obj and obj.id == request.user.id)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser:
            return qs
        else:
            self.fieldsets = (
                ("اطلاعات کاربری", {'fields': ('username', 'pass_per_save')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'gender', 'avatar', 'familier', 'email')}),
                (('اطلاعات کاربردی'), {'fields': ('phone_number',)}),
            )
            self.readonly_fields = (
                "username", "pass_per_save", "familier", "custom_user_id",
                "code_send", "email_sended", "is_active",
                "is_staff", "is_superuser", "groups", "user_permissions",
                "last_login", "date_joined",
            )
            return qs.filter(id=user.id)


admin.site.register(USER, USERAdmin)


def make_True_Status(modeladmin, request, queryset):
    queryset.update(status=True)


make_True_Status.short_description = 'نمایش همه انتخاب شده ها به کاربر'


def make_False_Status(modeladmin, request, queryset):
    queryset.update(status=False)


make_False_Status.short_description = 'عدم نمایش انتخاب شده ها به کاربر'
