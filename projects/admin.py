from django.contrib import admin
from .models import Project, Branch, SubBranch, ReleasedHistory


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'amount', 'start_date', 'total_released')
    list_filter = ('created_at', 'start_date')
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'total_spent')
    list_filter = ('created_at',)
    search_fields = ('name', 'project__name')
    readonly_fields = ('created_at',)


@admin.register(SubBranch)
class SubBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'amount', 'date')
    list_filter = ('date', 'created_at')
    search_fields = ('name', 'branch__name')
    readonly_fields = ('created_at',)


@admin.register(ReleasedHistory)
class ReleasedHistoryAdmin(admin.ModelAdmin):
    list_display = ('project', 'amount', 'date')
    list_filter = ('date', 'created_at')
    search_fields = ('project__name',)
    readonly_fields = ('created_at',)
