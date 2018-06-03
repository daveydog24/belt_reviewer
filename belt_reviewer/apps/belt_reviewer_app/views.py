from django.shortcuts import render, redirect
from django.contrib import messages
from models import User
import bcrypt

def index(request): # url route ('/')
    return render(request, 'belt_reviewer_templates/index.html')
    
def books_home(request): # url route ('/books')
    return render(request, 'belt_reviewer_templates/books_home.html')
    
def show_user(request): # url route ('users/(?P<id>\d+)')
    return render(request, 'belt_reviewer_templates/show_user.html')

def add_book(request):  # url route ('books/add')
    return render(request, 'belt_reviewer_templates/add_book.html')
    
def show_book(request): # url route ('books/(?P<id>\d+)')
    return render(request, 'belt_reviewer_templates/show_book.html')
    
def delete_book(request): # url route ('books/destroy/(?P<id>\d+)')
    return redirect(request, '/books')

def registration(request): # url route ('/registration')
    errors = User.objects.validate_user(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error)
            return redirect('/')

    messages.success(request, "you successfully registered!!!")
    name = request.POST['first_name']
    alias = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['registration_password']
    hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash_password)
    user.save()
    request.session['id'] = user.id
    
    return redirect('/books')

def login(request): # url route ('/login')
    email = request.POST['email']
    password = request.POST['password']
 
    get_user = User.objects.get(email=email)
    if (get_user):
        user_password = get_user.password
        check = bcrypt.checkpw(password.encode(), user_password.encode())
        if check == True:
            request.session['id'] = get_user.id
            messages.success(request, "you successfully logged in!!!")
            return redirect('/books')
        else:
            messages.error(request, "Email and password does not match our database.")
    return redirect('/')

def logout(request):# url route ('/logout')
    request.session.clear()
    return redirect('/')
