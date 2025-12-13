from django.contrib import admin
from .models import (Question, Country, Player, Team, PlayerChoice, TeamChoice, TeamType, QuestionType, Coach, CoachChoice)

class PlayerChoiceInline(admin.TabularInline):
    model = PlayerChoice
    extra = 3

class TeamChoiceInline(admin.TabularInline):
    model = TeamChoice
    extra = 3

class CoachChoiceInline(admin.TabularInline):
    model = CoachChoice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["text", "type"]}),
        ("Creation Date", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [PlayerChoiceInline, TeamChoiceInline, CoachChoiceInline]
    list_display = ["text", "type", "pub_date", "was_published_recently"]
    list_filter = ["type", "pub_date"]
    search_fields = ["text", "pub_date"]
    list_per_page = 7
    date_hierarchy = "pub_date"

admin.site.register(QuestionType)
admin.site.register(TeamType)
admin.site.register(Country)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Coach)
admin.site.register(Question, QuestionAdmin)
admin.site.register(PlayerChoice)
admin.site.register(TeamChoice)
admin.site.register(CoachChoice)