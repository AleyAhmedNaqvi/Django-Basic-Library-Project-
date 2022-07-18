from argparse import _MutuallyExclusiveGroup
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
  name = models.CharField(max_length=100)
  
  def __str__(self):
    return self.name

class Language(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

class Book(models.Model):
  title = models.CharField(max_length=100)
  author = models.ForeignKey("Author",on_delete=models.SET_NULL,null=True)
  summary = models.TextField(max_length=1000)
  isbn = models.CharField("ISBN",max_length=13,unique=True)
  genre = models.ManyToManyField(Genre)
  language = models.ForeignKey("Language",on_delete=models.SET_NULL,null=True)

  def get_absolute_url(self):
    return reverse("book_detail",kwargs={"pk":self.pk})

  def __str__(self):
    return self.title

class Author(models.Model):
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  date_of_birth = models.DateField(null=True,blank=True)

  class Meta:
    ordering = ['last_name','first_name']

  def get_absolute_url(self):
    return reverse("author_detail",kwargs={"pk":self.pk})

  def __str__(self):
    return f"{self.last_name}, {self.first_name} born on {self.date_of_birth}"

import uuid

class BookInstance(models.Model):
  id = models.UUIDField(default = uuid.uuid4, primary_key=True)
  book = models.ForeignKey("Book",on_delete=models.RESTRICT,null=True,blank=True)
  imprint = models.CharField(max_length=100)
  due_date = models.DateField(null=True,blank=True)
  borrower = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

  LOAN_STATUS = (
    ('m','Maintainance'),
    ('o','On Loan'),
    ('r','Restricted'),
    ('a','Available')
  )

  status = models.CharField(choices=LOAN_STATUS,max_length=1,blank=True,default='a')

  class Meta:
    ordering = ['due_date']

  def __str__(self):
    return f'{self.id} ({self.book.title})'