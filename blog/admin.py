from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'body', 'picture', 'published_on')
    prepopulated_fields = {"slug": ("title",)}

    def republish(self, request, queryset):
        queryset.update(published_on=True)
        self.message_user(request, "Выбранные записи были переизданы")

    republish.short_description = "Повторная публикация выбранных записей"
    actions = [republish]

