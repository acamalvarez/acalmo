from django.contrib import admin

from .models.contact_models import Contact
from .models.project_models import Project
from .models.publication_models import Publication
from .models.qualification_models import Qualification
from .models.skill_models import Skill, SubSkill

admin.site.register(Contact)
admin.site.register(Project)
admin.site.register(Publication)
admin.site.register(Qualification)
admin.site.register(Skill)
admin.site.register(SubSkill)
