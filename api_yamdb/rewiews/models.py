from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category,on_delete = models.SET_NULL,
        related_name="titles", blank=True, null=True)
    genre = models.ForeignKey(
        Genre, on_delete = models.SET_NULL,
        related_name="titles", blank=True, null=True)
    
    def __str__(self):
        return self.name



