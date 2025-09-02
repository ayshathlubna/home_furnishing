from django.db import models

# Create your models here.
class Category(models.Model):
    category_id = models.CharField(primary_key=True, max_length=20)
    category_name = models.CharField(max_length=20)
    category_image = models.ImageField(upload_to='category_image/',null=True)

    def __str__(self):
        return self.category_name