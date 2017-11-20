# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from datetime import datetime, timedelta

NAME_REGEX = re.compile(r'^([^0-9]*)$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PWD_REGEX = re.compile(r'^(?=.*?[A-Z]).*\d')
# Create your models here.
class UserManager(models.Manager):
    def validate_register(self, postdata):
        errors = {}
        email = postdata['email']       
        user = User.objects.filter(email_id=email)
        if len(user) > 0:
            errors['email'] =  "Please try another email id"
        else:    
            if postdata['name'] == "" :
                errors['name'] = "Please enter Firstname"
            else:            
                if len(postdata['name']) < 2:
                    errors["name"] = "Name should not be fewer than 2 characters"
                if not NAME_REGEX.match(postdata['name']):
                    errors['name'] = "Numeric characters are not allowed in Firstname"
            
            if postdata['alias'] == "":
                errors['alias'] = "Please enter Alias"
            else:
                if len(postdata['alias']) < 2:
                    errors["alias"] = "alias Name should not be fewer than 2 characters"
                if not NAME_REGEX.match(postdata['alias']):
                    errors['alias'] = "Numeric characters are not allowed in Lastname"

            if postdata['email'] == "":
                errors['email'] = "Please enter Email Id"
            else:
                if not EMAIL_REGEX.match(postdata['email']):
                    errors["email"] = "Invalid Email Address! please follow abc@xyz.com"

            if postdata['pwd'] == "":
                errors['pwd'] = "Please enter passwod"
            else:
                if len(postdata['pwd']) < 8:
                    errors['pwd'] = " Password must be 8 characters long"
                if not PWD_REGEX.match(postdata['pwd']):
                    errors['pwd'] = "Invalid password! Password must contain atleast 1 Uppercase and 1 numeric value "
                
            if postdata['cpwd'] == "":
                errors['cpwd'] = "Please enter confirm passwod"
            else:
                if postdata['pwd'] != postdata['cpwd']:
                    errors['pwd'] = "Confirm Password does not match with Password "

        if len(errors) != 0:
            return (False, errors)
        else:                  
            unhash = postdata['pwd']
            pwd = bcrypt.hashpw(unhash.encode(), bcrypt.gensalt())
            user = User.objects.create(name=postdata['name'], alias= postdata['alias'],email_id = postdata['email'], password = pwd)
            return (True, user)

    def validate_login(self, postdata):
        errors = {}
        if postdata['username'] == "" and postdata['pwd'] == "":
            errors['username'] = "Please enter email and password"        
        else:
            user = User.objects.filter(email_id=postdata['username'])
            if len(user) > 0:
                hash1 = user[0].password
                if bcrypt.checkpw(postdata['pwd'].encode(), hash1.encode()):
                    return (True, user)
            else:
                errors['username'] = "Please verify username or password"
                return (False, errors)
        return (False, errors)

    
    def validate_book(self, postdata, id):
        errors = {}
        if postdata['title'] == "":
            errors['title'] = "Please enter Book title"
        if postdata['review'] == "":
            errors['review'] = "Please enter review for this book"
        print "author"
        print postdata['author']
        if postdata['author'] == "" and postdata['new_author'] == "":
            errors['author'] = "Please choose or enter author"
        
        if len(errors) == 0:
            if postdata['author'] != "":
                author_name = postdata['author']
                print author_name
            else:
                author_name = postdata['new_author']
                print author_name
            author = Author.objects.filter(name = author)            
            user = User.objects.get(id= id)           
            if len(author) == 0:
                author = Author.objects.create(name=author_name)
                book = Book.objects.create(title=postdata['title'], author_id= author.id)        
                review = Review.objects.create(review = postdata['review'], stars = postdata['stars'], rater = user, reviewed_book = book)
            else:
                book = Book.objects.create(title=postdata['title'], author=author[0])        
                review = Review.objects.create(review = postdata['review'], stars = postdata['stars'], rater = user, reviewed_book = book)
            return (True, book)        
        else:
            return (False, errors)

    def validate_review(self, postdata, bookid, userid):
        errors = {}
        if postdata['review'] == "":
            errors['review'] = "You havn't enter review for this book"
        if postdata['stars'] == "":
            errors['stars'] = "You havn't enter any stars for this book"
        
        if len(errors) == 0:
            review = Review.objects.create(review = postdata['review'], stars = postdata['stars'], rater_id = userid, reviewed_book_id = bookid)
            return (True, review)
        else:
            return (False, errors)
    
    def validate_user(self, userid):
        errors = {}
        user = User.objects.filter(id = userid)
        if len(user) == 0:
            errors['user'] = "This route Not allowed"
            return (False, errors)
        else:
            user = User.objects.get(id=userid)
            reviews = Review.objects.filter(rater_id = userid)
            return (True, user, reviews)

    def validate_book_id(self, id):
        errors = {}
        book = Book.objects.filter(id = id)
        if len(book) == 0:
            errors['user'] = "This route Not allowed"
            return (False, errors)
        else:
            book = Book.objects.get(id = id) 
            reviews = Review.objects.filter(reviewed_book=book)             
            return (True, book, reviews)

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email_id = models.CharField(max_length=255)   
    password = models.CharField(default="", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="written_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Review(models.Model):
    review = models.CharField(max_length=500)
    stars = models.SmallIntegerField()
    rater = models.ForeignKey(User, related_name="reviews")
    reviewed_book = models.ForeignKey(Book, related_name="book_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()