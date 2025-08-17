from django.contrib import admin
from .models import UserProfile, Match, TicketCategory, Ticket, News, Report


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'date_of_birth']
    search_fields = ['user__username', 'user__email', 'phone']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['home_team', 'away_team', 'date_time', 'venue', 'status']
    list_filter = ['status', 'date_time']
    search_fields = ['home_team', 'away_team', 'venue']
    ordering = ['-date_time']


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description']
    ordering = ['price']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'match', 'category', 'quantity', 'total_amount', 'booking_date', 'is_paid']
    list_filter = ['category', 'is_paid', 'booking_date']
    search_fields = ['user__username', 'match__home_team', 'match__away_team']
    ordering = ['-booking_date']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'publish_date', 'is_featured']
    list_filter = ['category', 'publish_date', 'is_featured']
    search_fields = ['title', 'content']
    ordering = ['-publish_date']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['report_type', 'match', 'generated_date', 'generated_by']
    list_filter = ['report_type', 'generated_date']
    ordering = ['-generated_date']
