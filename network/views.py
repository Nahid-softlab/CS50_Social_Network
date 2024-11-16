from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json 

from .models import User, Post, Follow, Like


def index(request):
    allposts = Post.objects.all().order_by("id").reverse()

    #like hadler
    like = 1
    all_likes= Like.objects.all()
    youliked = []

    for like in all_likes:
        if like.mainuser_like.id == request.user.id:
            youliked.append(like.liked_post.id)
    

    #paginator
    p = Paginator(allposts,10)
    page_number = request.GET.get('page')
    post_of_the_page= p.get_page(page_number)

    return render(request, "network/index.html", {
        "allpost" : allposts,
        "post_of_the_page": post_of_the_page,
        "youliked": youliked,
        "all_likes":all_likes,
        "like":like,
    })

def unlike(request, post_id):
    post = Post.objects.get(pk=post_id)
    userlike= User.objects.get(pk= request.user.id)
    deletlike= Like.objects.filter(mainuser_like= userlike, liked_post=post)
    if deletlike:
        deletlike.delete()
        post.number_of_likes -= 1
        post.save()
    return JsonResponse({
            "message": "unlike  successful",
            "number_of_likes": post.number_of_likes,
        })

def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    userlike= User.objects.get(pk= request.user.id)
    newlike, created= Like.objects.get_or_create(mainuser_like= userlike,liked_post=post)
    if created:
        post.number_of_likes +=1
        post.save()
    
    return JsonResponse({
            "message": "liked post successful",
            "number_of_likes": post.number_of_likes,
        })


def new_post(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk= request.user.id)
        newpost= Post(
            content= content,
            user= user
        )
        newpost.save()
        return HttpResponseRedirect(reverse(index))
    
def edit(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        edit_post= Post.objects.get(pk=id)
        edit_post.content= data["content"]
        edit_post.save()
        return JsonResponse({
            "message": "change successful",
            "data" : data["content"]
        })




def profile(request, id):
    user_profile= User.objects.get(pk=id)
    allposts_of_user = Post.objects.filter(user=user_profile).order_by("id").reverse()

    #follo class
    following= Follow.objects.filter(mainuser_follow=user_profile).count()
    followers = Follow.objects.filter(followingUsers= user_profile).count()

    #is following?
    followers_for_logic = Follow.objects.filter(followingUsers= user_profile)
    is_following_user = followers_for_logic.filter(mainuser_follow=User.objects.get(pk=request.user.id))#this user is current user
    if len(is_following_user) != 0:
        is_following=True
    else:
        is_following=False
    


    #paginator
    p = Paginator(allposts_of_user, 1)
    page_number = request.GET.get('page')
    post_of_the_page= p.get_page(page_number)

    return render(request, "network/profile.html", {
        "allpost" : allposts_of_user,
        "post_of_the_page": post_of_the_page,
        "following":following,
        "folloers": followers,
        "is_following": is_following,
        "profile_owner" : user_profile,
    })

def follow(request, ):
    profile_owner_username= request.POST['follow']
    profile_owner = User.objects.get(username = profile_owner_username)
    currentuser= User.objects.get(pk = request.user.id)
    user_to_follow= profile_owner
    f= Follow(mainuser_follow= currentuser, followingUsers=profile_owner)
    f.save()
    user_to_followid= user_to_follow.id
    return HttpResponseRedirect(reverse(profile, kwargs={'id': user_to_followid}))

def unfollow(request, ):
    profile_owner_username= request.POST['unfollow']
    profile_owner = User.objects.get(username = profile_owner_username)
    currentuser= User.objects.get(pk = request.user.id)
    user_to_follow= profile_owner
    f= Follow.objects.get(mainuser_follow= currentuser, followingUsers=profile_owner)
    f.delete()
    user_to_followid= user_to_follow.id
    return HttpResponseRedirect(reverse(profile, kwargs={'id': user_to_followid}))

#following page view
def following_page(request):
    currentuser = User.objects.get(pk=request.user.id)
    following_user_list= Follow.objects.filter(mainuser_follow = currentuser)

    allposts = Post.objects.all().order_by("id").reverse()
    following_user_post= []

    for post in allposts:
        for person in following_user_list:
            if person.followingUsers == post.user:
                following_user_post.append(post)

    #paginator
    p = Paginator(following_user_post,10)
    page_number = request.GET.get('page')
    post_of_the_page= p.get_page(page_number)

    return render(request, "network/following.html", {
        "allpost" : allposts, 
        "post_of_the_page": post_of_the_page,
    })


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
