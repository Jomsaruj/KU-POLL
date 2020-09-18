from django.contrib import admin

from .models import Question, Choice

__author__ = "Saruj Sattayanurak"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['pub_date']
    search_fields = ['question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),

    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'end_date', 'was_published_recently',)


admin.site.register(Question, QuestionAdmin)
