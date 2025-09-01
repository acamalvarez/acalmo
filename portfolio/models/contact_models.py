from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=63)
    email = models.EmailField()
    subject = models.CharField(max_length=127)
    message = models.TextField()

    def __str__(self) -> str:
        return self.name
