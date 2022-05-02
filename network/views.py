import http
import json
from urllib.request import Request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import NewPostForm
from .models import User, Post, Likes, Follows
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.db.models import Count
from itertools import chain
from django.core.paginator import Paginator

def other_profile(request, user_id):
    if int(user_id) == request.user.id:
        return redirect(profile)
    posts =  Post.objects.filter(user = user_id).order_by("-date")
    user=posts[0].user
    paginated = paginate(request, posts, 10)
    return render(request, "network/otherprofile.html", {
    "posts":paginated, "user":user})

def index(request):
    posts = Post.objects.all().order_by("-date")
    paginated = paginate(request, posts, 10)
    newpost=NewPostForm(request.POST or None)
    if request.method == "POST":
        if newpost.is_valid():
            savepost = newpost.save(commit=False)
            savepost.user=request.user
            savepost.date = datetime.today()
            savepost.save()
            newlikes = Likes.objects.create(post=savepost)
            newlikes.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/index.html", {"newpost":newpost,
    "posts":paginated})

@login_required(login_url='http://127.0.0.1:8000/login')
def edit(request, post_id):
    data = json.loads(request.body)
    content = data.get("post", "")
    post=Post.objects.get(id=post_id)
    page = data.get("page", "")
    request.session['page'] = page
    if request.method == "POST":
        if post.user == request.user:
            post.post=content
            post.save()    
            return HttpResponse(page)

@login_required(login_url='http://127.0.0.1:8000/login')
def profile(request):
    mypostlist = Post.objects.filter(user = request.user).order_by("-date")
    paginated = paginate(request, mypostlist, 10)
    newpost=NewPostForm(request.POST or None)
    if request.method == "POST":
        if newpost.is_valid():
            savepost = newpost.save(commit=False)
            savepost.user=request.user
            savepost.date = datetime.today()
            savepost.save()
            newlikes = Likes.objects.create(post=savepost)
            newlikes.save()
        return HttpResponseRedirect(reverse("profile"))
    return render(request, "network/profile.html", {"newpost":newpost,
    "posts":paginated})

@login_required(login_url='http://127.0.0.1:8000/login')
def following(request):
    followquery = Follows.objects.filter(following__in=[request.user])
    followposts = []
    for i in followquery:
        post=Post.objects.filter(user=i.user_id)
        followposts.append(post)
    sorted=list(chain.from_iterable(followposts))
    sortids = [i.id for i in sorted]
    posts=Post.objects.filter(id__in=sortids).order_by("-date")
    paginated = paginate(request, posts, 10)
    return render(request, "network/following.html", {
 "posts":paginated})

def paginate(request, posts, num):
    paginator = Paginator(posts,num)
    if request.session.has_key('page'):
        page_number = request.session['page']
        del request.session['page']
    else:
        page_number = request.GET.get('page')
    paginated = paginator.get_page(page_number)
    return paginated

def follows(request, user_id):
    getfollow=Follows.objects.get(user__id=user_id)
    if request.user.is_authenticated:
        follows=Follows.objects.filter(user__id=user_id).filter(following__in=[request.user])
        if not follows:
            if request.method=="POST":
                getfollow.following.add(request.user)
                status="following"
            else:
                status="nofollow"
        else:
            if request.method=="POST":
                getfollow.following.remove(request.user)
                status="nofollow"
            else:
                status="following"
    else:
        status="nofollow"
    follownum=getfollow.following.count()
    followingnum=User.objects.get(id=user_id).followed.all().count()
    response=[status, str(follownum), str(followingnum)]
    return JsonResponse(response, safe=False)

def likes(request, post_id):
    getlike=Likes.objects.get(post__id=post_id)
    if request.user.is_authenticated:
        liked=Likes.objects.filter(post__id=post_id).filter(like__in=[request.user])
        if not liked:
            if request.method=="POST":
                getlike.like.add(request.user)
                status="like"
            else:
                status="nolike"
        else:
            if request.method=="POST":
                getlike.like.remove(request.user)
                status="nolike"
            else:
                status="like"
    else:
        status="nolike"
    likenum=getlike.like.count()
    response=[status, str(likenum)]
    return JsonResponse(response, safe=False)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        newfollows = Follows.objects.create(user=User.objects.get(id=request.user.id))
        newfollows.save()
        newfollows.following.add(request.user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
