from django.contrib import admin

from .models import Project, Publication, Qualification, Skill, SubSkill

admin.site.register(Project)
admin.site.register(Publication)
admin.site.register(Qualification)
admin.site.register(Skill)
admin.site.register(SubSkill)
