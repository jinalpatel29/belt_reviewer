# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, Book, Author, Review
from django.contrib import messages
# Create your views here.
def index(req):
    if 'id' not in req.session:
        req.session['id'] = 0
    if 'name' not in req.session:
        req.session['name'] = ""
    return render(req, 'belt_rev/index.html')

def login(req):
    results = User.objects.validate_login(req.POST)
    if results[0]:
        req.session['id'] = results[1][0].id
        req.session['name'] = results[1][0].alias       
        messages.success(req, "Successfully logged in)!")
        return redirect('/books')
    else:
        for result in results[1]:
            messages.error(req, results[result])
        return redirect('/')

def register(req):
    if req.method == "POST":
        results = User.objects.validate_register(req.POST)       
        if results[0]:
            req.session['name'] = results[1].alias
            req.session['id'] = results[1].id
            messages.success(req, "Successfully registered!")
            return redirect('/books')
        else:
            errors = results[1]
            for result in errors:
                messages.error(req, errors[result])
            return redirect('/')
    return redirect('/')        

def books(req):
    if req.session['id'] == 0:
        messages.error(req, "You are not logged in !")
        return redirect('/')  
    else:
        recent_reviews = Review.objects.all().order_by('-created_at')[:3]
        reviews = Review.objects.all()
        context = {
        'recent_reviews' : recent_reviews,
        'reviews' : reviews
        }
        return render(req, 'belt_rev/books.html', context)  

def add(req):
    if req.session['id'] == 0:
        messages.error(req, "You are not logged in !")
        return redirect('/')
    else:  
        authors = Author.objects.all()
        context = {
            'authors' : authors
        }
        return render(req, 'belt_rev/add.html', context) 

def addBook(req):
    if req.session['id'] == 0:
        messages.error(req, "You are not logged in !")
        return redirect('/')
    else:  
        if req.method == "POST":       
            results = Book.objects.validate_book(req.POST, req.session['id'])
            if results[0]:             
                bid = results[1].id 
                messages.success(req, "Successfully added Book!")
                return redirect('/books/'+str(bid)) 
            else:
                errors = results[1]
                for result in errors:
                    messages.error(req, errors[result])
                return redirect('/books/add')
        else:
            return redirect('/books/add')

def review(req, id):
    if req.session['id'] == 0:
        messages.error(req, "You are not logged in !")
        return redirect('/')
    else:
        results = Book.objects.validate_book_id(id)
        if results[0]:
            context = {
                'book' :results[1],
                'author': results[1].author.name,
                'reviews': results[2]
            }
            return render(req, 'belt_rev/review.html', context )
        else:
            errors = results[1]
            for result in errors:
                messages.error(req, errors[result])
            req.session.clear()
            return render(req, 'belt_rev/index.html')
      

def addReview(req, id):
    if req.session['id'] == 0:
        messages.error(req, "You are not logged in !")
        return redirect('/')
    else:
        if req.method == "POST":
            results = Review.objects.validate_review(req.POST, id, req.session['id'])

            if results[0]:
                messages.success(req, "Successfully added review!")
                return redirect('/books/'+str(id))
            else:
                errors = results[1]
                for result in errors:
                    messages.error(req, errors[result])
                return redirect('/books/'+str(id))
        else:
            return redirect('/books/'+str(id))
   
def profile(req, id):
    results = User.objects.validate_user(id)
    if results[0]:
        total = len(results[2])
        context = {
            'user' : results[1],
            'total' : total,
            'reviews' : results[2]
        }
        return render(req, 'belt_rev/user.html', context)
    else:        
        errors = results[1]
        for result in errors:
            messages.error(req, errors[result])
        return render(req,'belt_rev/index.html' )

def logout(req):
    req.session.clear()
    return redirect('/')