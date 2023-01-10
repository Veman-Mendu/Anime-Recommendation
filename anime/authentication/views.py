from turtle import title
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

from .models import *

# Create your views here.
def home(request):
    return render(request, 'authentication/index.html')

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pword']
        cpassword = request.POST['cpword']
        if User.objects.filter(username=username):
            messages.error(request, "Username already exits")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "email already exists")
            return redirect('home')

        if password != cpassword:
            messages.error(request, "passowrds didn't match")

        if not username.isalnum():
            messages.error(request, "Username must be alpha numeric")
            return redirect('home')

        myUser = User.objects.create_user(username, email, password)
        myUser.save()

        messages.success(request, "You are signedup")
        return redirect('signin')

    return render(request, 'authentication/signup.html')

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        passowrd = request.POST['pword']

        user = authenticate(username=username, password = passowrd)

        if user is not None:
            login(request, user)
            anime_list = anime.objects.all()
            return render(request, "authentication/main.html", {'uname':username, 'anime_list' : anime_list})

        else:
            messages.error(request, "Bad credentials")
            return redirect('home')

    return render(request, 'authentication/signin.html')

def main(request):
    anime_list = anime.objects.all()
    return render(request, 'authentication/main.html', {'anime_list' : anime_list})

def signout(request):
    logout(request)
    messages.success(request, "logged out successfully. Hope you enjoyed it")
    return redirect('home')

def random(request):
    import pandas as pd
    import random

    data = pd.read_csv('S:\Projects/anime\genrelistdata.csv')
    titles = data['titles']
    rand_title = random.choice(titles)
    rand_title = rand_title.lower()
    rand_title = rand_title.replace(' ','-')
    return render(request, 'authentication/random.html', {'rand_title' : rand_title})

def recommendation(request):
    import pandas as pd

    data = pd.read_csv('S:\Projects/anime\genrelistdata.csv')
    
    def create_soup(x):
        x['Genre'] = x['Genre'].replace('[','')
        x['Genre'] = x['Genre'].replace("'",'')
        x['Genre'] = x['Genre'].replace(',','')
        x['Genre'] = x['Genre'].replace(']','')
    
        x['Studio'] = x['Studio'].replace('[','')
        x['Studio'] = x['Studio'].replace("'",'')
        x['Studio'] = x['Studio'].replace(',','')
        x['Studio'] = x['Studio'].replace(']','')

        x['SP'] = str(x['SP'])
        x['SP'] = x['SP'].replace('[','')
        x['SP'] = x['SP'].replace("'",'')
        x['SP'] = x['SP'].replace(',','')
        x['SP'] = x['SP'].replace(']','')

        x['titles'] = x['titles'].replace(' ','')
        x['titles'] = x['titles'].lower()

        return ''.join(x['Genre'])+' '+''.join(x['Studio'])+' '+''.join(x['SP'])+' '+''.join(x['titles'])
    
    data['Soup'] = data.apply(create_soup, axis=1)
    data.iloc[0]['Soup']
    
    data['titles'] = data['titles'].str.lower()
    indices = pd.Series(data.index, index = data['titles']).drop_duplicates()

    from sklearn.feature_extraction.text import CountVectorizer

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(data['Soup'])

    from sklearn.metrics.pairwise import cosine_similarity

    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    if request.method == "POST":

        title = request.POST['reqdata']
        print(title)
    
    def content_recommender(title, cosine_sim=cosine_sim, data = data, indices = indices):
        idx = indices[title]
        sim_score = list(enumerate(cosine_sim[idx]))
        sim_score = sorted(sim_score,key = lambda x:x[1], reverse=True)
        sim_score = sim_score[1:11]

        anime_indices = [i[0] for i in sim_score]

        title_array = data['titles'].iloc[anime_indices]

        return title_array

    recommendations = content_recommender(title)

    rec_array = []
    for recommendation in recommendations:
        recommendation = recommendation.lower()
        recommendation = recommendation.replace(' ','-')
        rec_array.append(recommendation)
    return render(request, 'authentication/recommendation.html', {'recommendations' : rec_array})
