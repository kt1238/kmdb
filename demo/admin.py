from django.contrib import admin
from demo.models import Movie

# Creating modified admin class
class DemoAdmin(admin.ModelAdmin):
    search_fields = ['name']


# Register your models and new admin class here.
admin.site.register(Movie, DemoAdmin)