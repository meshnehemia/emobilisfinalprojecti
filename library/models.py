from django.db import models

from socialmedia.models import User


# Create your models here.
class Framework(models.Model):
    framework_name = models.CharField(max_length=20)
    framework_description = models.TextField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    frameworks_image = models.ImageField(null=False, upload_to='framework/')

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.framework_name


class Category(models.Model):
    category_name = models.CharField(max_length=20)
    category_image = models.ImageField(null=True, upload_to='languages/', default="book_cover/bg2.png")
    category_description = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.category_name


class MainBooks(models.Model):
    option = (('sale', 'sale'), ('free', 'free'))
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    topic = models.CharField(max_length=250)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=False, upload_to='book_cover/')
    book = models.FileField(null=False, upload_to='books/')
    type = models.CharField(max_length=10, choices=option, default='free')
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class BookBought(models.Model):
    book = models.ForeignKey(MainBooks, null=False, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.book.title
