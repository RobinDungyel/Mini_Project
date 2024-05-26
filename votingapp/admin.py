from django.contrib import admin
from .models import Candidate, Position, Time

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Add comma to make it a tuple
    search_fields = ('title',)  # Add comma to make it a tuple
    list_filter = ('title',)  # Add comma to make it a tuple

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'manifesto','total_vote')  # Add comma to make it a tuple
    list_filter = ('position',)  # Add comma to make it a tuple
    search_fields = ('name', 'position')  # Add comma to make it a tuple
    readonly_fields = ('total_vote',)

@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = ('voting_start', 'voting_end',)  # Add comma to make it a tuple
