from django.contrib import admin
from .models import (
	User, Reader, Editor, Journalist, ReaderProfile, EditorProfile,
	JournalistProfile, Article, Newsletter,
)

# Register your models here.

admin.site.register(User)
admin.site.register(Reader)
admin.site.register(Editor)
admin.site.register(Journalist)
admin.site.register(ReaderProfile)
admin.site.register(EditorProfile)
admin.site.register(JournalistProfile)
admin.site.register(Article)
admin.site.register(Newsletter)
