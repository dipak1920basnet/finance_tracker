import urllib.parse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User, Category, Transaction, Budget
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# required import to display chart in html and python alone.  
import matplotlib.pyplot as plt
import uuid
import time 
import io
import urllib
import base64
import graphviz # For flow chart 
import os # Delete the image once session is over 

# Create your views here.

def pie_chart(data, labels):
    if len(data) != len(labels):
        raise Exception("labels and data length mismatched")
    else:
        fig, ax = plt.subplots()
        ax.pie(data, labels=labels,  autopct='%1.1f%')
        ax.axis('equal')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        string = base64.b64eencode(buf.read())
        uri = urllib.parse.quote(string)

        return uri



def home(request, name):
    # The home page should display the name of logged in user. 
    # 
    name = request.user.username
    income = 0 #Get the total income of the user
    expense = 0 #Get the total expense of the user
    balance = income-expense
    
    data = [income,expense,balance]
    label = ["income","expense","balance"]

    user_name = User.objects.get(username=name)
    get_budget_category = Category.objects.filter(user=user_name)
    print(get_budget_category)
    Budget_category_list = []
    for i in get_budget_category:
        if not str(i) == "<Category: Salary>":
            Budget_category_list.append(i)

    if request.user.is_authenticated:
        return render(request,"finance/home.html",
                    {
                        "name":(name.lower()).capitalize(),
                        "income":income,
                        "expense":expense,
                        "balance":balance,
                        "budget_category_list": Budget_category_list,
                        "budget_month":[i for i in range(1,13)],
                        'data': pie_chart(data, label)
                        # "budget_category_list":get_budget_category,
                    })
    else:
        return redirect('finance:login_view')

def register_view(request, message=None):
    if message != None:
        return render(request, "finance/register.html",
                    {
                        "message":message
                    })
    else:
        return render(request, "finance/register.html")

def login_view(request):
    return render(request, "finance/signin.html")

def reset_password_view(request):
    return render(request, "finance/forget_password.html")

def reset_password(request):
    ...

# @login_required
def Logout(request):
    # if authenticate(request):
    logout(request)
    return redirect('finance:login_view')
    # else:
    #     message = {
    #         # log out error message:
    #         "error_message" : "please log in to log out",
    #     }

def Login(request):
    if request.method != "POST":
        # display a error method then return it 
        return render(request, "finance/signin.html",
                      {
                          "message":"The error occured in submitting the form application."
                      })
    username = request.POST.get("Username").lower()
    password = request.POST.get("Password")
    print(username)
    print(password)
    # Check for password confirmation. 
    # for wrong password display error.
    # for correct password login to user.
    for_login = authenticate(request, username=username, password=password)

    if for_login:
        login(request, for_login)
        return redirect("finance:home", username)

def register(request):
    def display_error_message(name):
        message = f"{name} has failed please try again"
        return message
    
    if request.method != "post":
        # display a error method then return it 
        return render(request, "finance/register.html",
                      {
                          "message":"The error occured in submitting the form application."
                      })
    name = request.POST.get("username")
    print(name)
    email = request.POST.get("email")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")
    if password != confirm_password:
        error_message = display_error_message("password confirmation")
        return redirect("finance:register_view")

    # Check if email is valid
    try:
        validate_email(email)
    except ValidationError:
        error_message = display_error_message("Email validation")
        return redirect("finance:register_view")
    
    # Feature to implement in future is:
    # Error message should be displayed
    # Make sure that if once the error occures the information typed in form is not lost 
    # User should be able to edit it out.

    # Register a data. 
    try:
        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()

    except IntegrityError:
        return render(request, "finance/register.html",{
            "message":"The user name is already taken"
        })
    
    for_login = authenticate(request, username=name, password=password)

    if for_login:
        login(request, for_login)
        return redirect("finance:home")

    