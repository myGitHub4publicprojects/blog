from django.contrib import admin
from .models import Category, Post

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "timestamp", "updated"]
    list_display_links = ["title"]
    list_filter = ["timestamp", "updated"]
    search_fields = ["title", "content"]
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
admin.site.register(Category)



# class SignUpAdmin(admin.ModelAdmin):
# 	list_display = ["__unicode__", "timestamp", "updated"]
# 	form = SignUpForm
# 	# class Meta:
# 	# 	model = SignUp



# admin.site.register(SignUp, SignUpAdmin)