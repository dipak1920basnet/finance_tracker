import urllib.parse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User, Category, Transaction, Budget
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages

# required import to display chart in html and python alone.
import matplotlib.pyplot as plt
import uuid
import time
import io
import urllib.parse
import base64
import graphviz  # For flow chart
import os  # Delete the image once session is over

# required import for errors:
import traceback
import logging
from django.core.exceptions import ObjectDoesNotExist

logging.basicConfig(
    level=logging.INFO,
    filename="finance.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.debug("debug")
logging.info("info")
logging.warning("warning")
logging.error("error")
logging.critical("criticals")

# Create your views here.


def pie_chart(data, labels):
    if len(data) != len(labels):
        raise Exception("labels and data length mismatched")
    else:
        fig, ax = plt.subplots()
        ax.pie(data, labels=labels, autopct="%1.1f%%")
        ax.axis("equal")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        string = base64.b64encode(buf.read()).decode()
        uri = urllib.parse.quote(string)

        return uri


def home(request, name):
    if not request.user.is_authenticated:
        return redirect("finance:login_view")
    # The home page should display the name of logged in user.
    #
    name = request.user.username
    income = 10  # Get the total income of the user
    expense = 5  # Get the total expense of the user
    balance = income - expense

    data = [income, expense, balance]
    label = ["income", "expense", "balance"]

    try:
        user_name = User.objects.get(username=name)
    except User.DoesNotExist:
        error_message = traceback.format_exc()
        logging.error(error_message)

    try:
        get_budget_category = Category.objects.filter(user=user_name)
    except UnboundLocalError:
        error_message = traceback.format_exc()
        logging.error(error_message)

    # print(get_budget_category)
    Budget_category_list = []
    for i in get_budget_category:
        if not str(i) == "<Category: Salary>":
            Budget_category_list.append(i)

    # Try getting the data for budget management

    return render(
        request,
        "finance/home.html",
        {
            "name": (name.lower()).capitalize(),
            "income": income,
            "expense": expense,
            "balance": balance,
            "budget_category_list": Budget_category_list,
            "budget_month": [i for i in range(1, 13)],
            "data": pie_chart(data, label)
            # "budget_category_list":get_budget_category,
        },
    )


def register_view(request, message=None):
    if message != None:
        return render(request, "finance/register.html", {"message": message})
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
    logging.info("logged out successfully")
    return redirect("finance:login_view")
    # else:
    #     message = {
    #         # log out error message:
    #         "error_message" : "please log in to log out",
    #     }


def Login(request):
    if request.method != "POST":
        # display a error method then return it
        return render(
            request,
            "finance/signin.html",
            {"message": "The error occured in submitting the form application."},
        )
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
        logging.info("logged in successfully")
        request.session["username"] = for_login.username
        return redirect("finance:home", name=for_login.username)


def register(request):
    def display_error_message(name):
        message = f"{name} has failed please try again"
        return message

    if request.method != "POST":
        # display a error method then return it
        return render(
            request,
            "finance/register.html",
            {"message": "The error occured in submitting the form application."},
        )
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
        return render(
            request,
            "finance/register.html",
            {"message": "The user name is already taken"},
        )

    for_login = authenticate(request, username=name, password=password)

    if for_login:
        login(request, for_login)
        return redirect("finance:home",name=request.user.username)


# Receive data for manage Transactions and create, update data
# @login_required
def manage_transaction(request):
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        category = request.POST.get("category")
        date = request.POST.get("date")
        description = request.POST.get("description")
        income_expense = request.POST.get("income_expense")

        try:
            user_name = User.objects.get(username=request.user.username)
        except ObjectDoesNotExist:
            logging.error(f"User {request.user.username} does not exist")
            message = "user does not exist"
            messages.info(request, message)
            # display message in home page
            return redirect("finance:home",name=request.user.username)

        try:
            current_amount = Transaction.objects.filter(user=user_name).values_list(
                "amount", flat=True
            )
            if current_amount:
                current_amount = sum(current_amount)
            else:
                current_amount = 0
        except Exception as e:
            logging.error(f"Error fetching current amount {traceback.format_exc()}")
            message = "There was an error fetching your balance."
            messages.info(request, message)
            return redirect("finance:home",name=request.user.username)

        # Model creation feature is yet to be implemented
        if income_expense == "expense":
            # get the amount from the data

            if current_amount < amount:
                message = "The amount is not sufficient"
            else:
                current_amount -= amount
                message = f"Your amount is {current_amount}"
        else:
            current_amount += amount
            message = f"Your amount is {current_amount}"

        try:
            category_name = request.POST.get("category")
        except Category.DoesNotExist:
            logging.error(f"Category {category_name} does not exist")
            messages.info(request, "Selected category does not exist.")
            return redirect("finance:home", name=request.user.username)
        try:
            # Check if a transaction already exists with the same user, category, and date
            existing_transaction = Transaction.objects.filter(
                user=user_name, category=category_name, date=date
            ).exists()
            if existing_transaction:
                message = "Transaction already exists for the given category and date."
                return redirect("finance:home",name=request.user.username)
        except Exception as e:
            logging.error(f"Error checking if transaction exists: {traceback.format_exc()}")
            message = "There was an error checking the transaction."

        try:
            Transaction.objects.create(
                user=user_name,
                category=category,
                amount=amount,
                date=date,
                description=description,
                type=income_expense,
            )
            message = "Transaction successfully created."
            logging.info(f"{message}")

        except Exception as e:
            logging.error(f"Error creating transaction: {traceback.format_exc()}")
            message = "There was an error creating your transaction."
    
    messages.info(request, message)
    return redirect("finance:home",name=request.user.username)


@login_required
def manage_budget(request):
    user_name = request.user

    if request.method == "POST":
        expense = request.POST.get("expense_in")
        month = request.POST.get("month")
        amount = request.POST.get("amount")

    # Check if the data exists in Budgets
    # if data exists then update data
    try:
        # retrive data
        category = Category.objects.get(name=expense)
    except Category.DoesNotExist:
        # if the data does not exist then create it
        messages.error(request, "Selected category does not exist.")
        return redirect("finance:home", name=user_name)
    try:
        budget = Budget.objects.get(user=user_name, category=category, month=month)
        # If budget exists, update it
        budget.amount = amount
        budget.save()
        messages.success(request, "Budget updated successfully.")
    except Budget.DoesNotExist:
        # If it does not exist, create a new budget entry
        Budget.objects.create(user=user_name, category=category, month=month, amount=amount)
        messages.success(request, "Budget created successfully.")
    except Exception as e:
        logging.error(f"Error managing budget: {traceback.format_exc()}")
        messages.error(request, "There was an error processing the budget.")
    
    return redirect("finance:home", name=user_name.username)
