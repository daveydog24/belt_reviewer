from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import bcrypt

class UserManager(models.Manager):
    def validate_user(self, postData):
        errors = {} 

        if len(postData['name']) < 2:
            errors['first_name'] = "First name can not be less than 2 characters."

        if len(postData['alias']) < 2:
            errors['last_name'] = "Last name can not be less than 2 characters."

        if len(postData['email']) < 1:
            errors['email'] = "Email cant be less than 1 character."

        if len(postData['registration_password']) < 8:
            errors['password'] = "password cant be less than 8 characters."

        if postData['registration_password'] != postData['confirm_password']:
            errors['confirm_password'] = "passwords do not match please reconfirm."
            
        try:
            validate_email(postData['email'])
        except ValidationError:
            errors['email'] = "This is not a valid email."
        else:
            if User.objects.filter(email=postData['email']):
                errors['email'] = "This user already exists."
        return errors

class BookManager(models.Model):
    def dashboardQuery(self):
        latest_three = Reviews.objects.all().order_by['created_at'][0:3]
        ids = []
        for review in latest_three:
            ids.append(review.book.id)
        other_books = self.exclude(id__in=ids)

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    book = models.ForeignKey(Book, related_name="reviews")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)