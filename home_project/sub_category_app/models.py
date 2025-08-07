from django.db import models
from category_app.models import Category

# Create your models here.
class Sub_category(models.Model):
    sub_cat_id = models.CharField(primary_key=True,max_length=20)
    sub_cat_name = models.CharField(max_length = 20)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_cat_image = models.ImageField(upload_to='sub_cat_image/',null=True)


    def __str__(self):
        return self.sub_cat_name