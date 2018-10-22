from django.db import models
from django.core.validators import validate_email, MaxValueValidator, MinValueValidator
import bcrypt

class UserManager(models.Manager):
    def validation(self, postdata):
        errors = {}
        if len(postdata['first_name']) < 2:
            errors['first_name'] = 'First name needs to be at least 2 characters.'
        if len(postdata['last_name']) < 2:
            errors['last_name'] = 'Last name needs to be at least 2 characters.'
        if len(postdata['password']) < 8:
            errors['password'] = 'password needs to be at least 8 characters.'
        try:
            validate_email(postdata['email'])
        except:
            errors['email'] = 'invalid email format.'
        if postdata['password'] != postdata['passconfirm']:
            errors['password_confirm'] = 'passwords must match.'
        try:
            User.objects.get(email = postdata['email'])
            errors['email_taken'] = 'email has already been registered'
        except:
            print('success')
        return errors
    def login_validation(self,postdata):
        errors={}
        try:
            user = User.objects.get(email = postdata['username'])
            print('email')
        except Exception as e:
            errors['login'] = 'invalid login'
            print(e)
        if bcrypt.checkpw(postdata['pw'].encode(), user.password.encode()) == False:
            errors['login'] = 'invalid login'

        return errors


class JobManager(models.Manager):
    def job_validation(self,postdata):
        errors = {}
        if len(postdata['title']) < 3:
            errors['title'] = 'Job Title needs to be at least 3 characters.'
        if len(postdata['desc']) < 3:
            errors['desc'] = 'Job Description needs to be at least 3 characters.'
        if len(postdata['new_location']) < 3:
            errors['new_location'] = 'The Job Location needs to be at least 3 characters.'
        try:
            Location.objects.get(location = postdata['new_location'])
            errors['location_taken'] = 'This location already exists please select from the list above'
        except:
            print('success')

        return errors
    def edit_validation(self, postdata):
        errors = {}
        if len(postdata['title']) < 3:
            errors['title'] = 'Job Title needs to be at least 3 characters.'
        if len(postdata['desc']) < 3:
            errors['desc'] = 'Job Description needs to be at least 3 characters.'
        if len(postdata['location']) < 3:
            errors['location'] = 'Job Location needs to be at least 3 characters.'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Location(models.Model):
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Job(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(Location, related_name='jobs')
    user = models.ForeignKey(User, related_name='jobs')
    objects = JobManager()

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    jobs = models.ManyToManyField(Job, related_name='job_categories')
