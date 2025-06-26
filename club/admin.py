from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import MembershipApplication, Profile, Post, Comment

class MembershipApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'classroom', 'application_date', 'approved')
    list_filter = ('approved', 'school')
    search_fields = ('name', 'school')
    readonly_fields = ('application_date',)
    actions = ['approve_applications']

    def approve_applications(self, request, queryset):
        for application in queryset:
            if not application.approved:
                application.approved = True
                application.approved_by = request.user
                application.save()
    approve_applications.short_description = "Approve selected applications"

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'classroom')
    search_fields = ('user__username', 'school')

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_preview', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'user__username')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content_preview', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'user__username')
    
    def content_preview(self, obj):
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
    content_preview.short_description = 'Content'

admin.site.register(MembershipApplication, MembershipApplicationAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)