from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User, QuestionGroup, Question, Session
class UserAdmin(BaseUserAdmin):
  fieldsets = (
      (None, {'fields': ('email', 'password', )}),
      (_('Personal info'), {'fields': ('first_name', 'last_name')}),
      (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                     'groups', 'user_permissions')}),
      (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('user_info'), {'fields': ('username', 'token')}),
  )
  add_fieldsets = (
      (None, {
          'classes': ('wide', ),
          'fields': ('username', 'email', 'password1', 'password2'),
      }),
  )
  list_display = ['email', 'first_name', 'last_name', 'is_staff', "username", "token"]
  search_fields = ('email', 'first_name', 'last_name')
  ordering = ('email', )

class QuestionGroupAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('name', 'type', 'topic', 'description'),
        }),
    )
    list_display = ['name', 'type', 'topic', 'description']
    search_fields = ('name', 'type', 'topic')
    

class QuestionAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('questionGroup', 'partType', 'content'),
        }),
    )
    list_display = ['id', 'questionGroup', 'partType', 'content', 'createTime']
    search_fields = ('questionGroup', 'partType', 'content')
    
class SessionAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('user', 'openaiSessionId'),
        }),
    )
    list_display = ['id', 'user', 'openaiSessionId', 'createTime']
    search_fields = ('id', 'user', 'openaiSessionId')
    

admin.site.register(User, UserAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Session, SessionAdmin)