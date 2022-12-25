from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timezone
import jwt
import os

from .forms import SignupForm, LoginForm

from .models import User

secret = os.environ['secret']


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            hashed_password = make_password(password)

            user = User(username=username, hashed_password=hashed_password, date_created=datetime.now(timezone.utc), ok_after=datetime.now(timezone.utc))
            user.save()
            
            token_payload = {
                'user_id': user.id,
                'time_created': datetime.now().timestamp
            }

            token = jwt.encode(token_payload, secret, algorithm='HS256')

            response = HttpResponseRedirect('/study')
            response.set_cookie('token', token, secure=True, httponly=True, samesite='Strict')

            return response

    elif request.method == 'GET':
        render(request, 'user/signup.html', {'form': SignupForm})