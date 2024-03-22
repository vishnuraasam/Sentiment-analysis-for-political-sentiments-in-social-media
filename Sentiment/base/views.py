from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
import io
import urllib, base64

from django.shortcuts import render
import pickle
import numpy as np
import pandas as pd
import pickle
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
global scaler
import folium







def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')
@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

    



def getPredictions(inp):
    model = pickle.load(open('RF.pkl', 'rb'))
    transformed_text = pd.DataFrame([inp], columns=['text'])
    prediction = model.predict(transformed_text)
    return prediction[0]



def result(request):
    inp = str(request.GET['text'])
    result= getPredictions(inp)
    return render(request, 'result.html', {'result': result})