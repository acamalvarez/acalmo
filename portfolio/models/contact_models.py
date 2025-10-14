from django.db import models


class Contact(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=63)
    email = models.EmailField()
    subject = models.CharField(max_length=127)
    message = models.TextField()

    def __str__(self) -> str:
        return self.name
