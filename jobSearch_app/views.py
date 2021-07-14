from django.contrib.messages.api import info
from jobSearch_app.decorators import validate_request
from django.contrib import messages
from jobSearch_app.models import *
from django.shortcuts import render, redirect
import datetime as dt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import json

@validate_request
def home(request, logged_user):

    context = {
        "user_info": logged_user,
    }
    return render(request, "home.html", context)