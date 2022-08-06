from importlib.resources import path
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
from django.db.models import F
from django.db.models import Count

from .models import User
from .models import Blog
from .models import Likes

# Create your views here.

def index(request):
    mostLiked=None
    topBlogs=[]
    try:
        mostLiked=Likes.objects.values("blog").annotate(Count("blog")).order_by("-blog__count")
    except:
        if("username" in request.session):
            return render(request,"blog/index.html",{
            "page":"index",
            "isLoggedIn": True,
            "username":request.session['username'],
            "fullname":request.session['fullName'],
            "topBlogs":[]
            })
        else:
             return render(request,"blog/index.html",{
            "page":"index",
            "topBlogs":[]
            })
    else:
        if(mostLiked.count()>=3):
            for i in mostLiked[:3]:
                topBlogs.append(Blog.objects.get(id=int(i["blog"])))
        else:
            for i in mostLiked[:]:
                topBlogs.append(Blog.objects.get(id=int(i["blog"])))
    if("username" in request.session):
        print(topBlogs)
        return render(request,"blog/index.html",{
        "page":"index",
        "isLoggedIn": request.session['isLoggedIn'],
        "username":request.session['username'],
        "fullname":request.session['fullName'],
        "topBlogs":topBlogs
    })
    else:
        return render(request,"blog/index.html",{
        "page":"index",
        "topBlogs":topBlogs
        })


def login(request):
    if(request.method=="POST"):
        user=None
        try:
            user=User.objects.get(username=request.POST['username'],password=request.POST['password'])
        except User.DoesNotExist:
            return render(request,"blog/login.html",{
                "error": True,
                "message": "Username or password is incorrect."
            })
        else:
            request.session['username']=user.username
            request.session['fullName']=user.fullName
            request.session['isLoggedIn']=True
            request.session['userId']=user.id
            return HttpResponseRedirect("/")
    else:     
        return render(request,"blog/login.html")


def register(request):
    if(request.method=="POST"):
        try:
            User.objects.get(username=request.POST['username'])
        except User.DoesNotExist:
            if(request.POST['username'].strip()=='' or request.POST['fullName'].strip()=='' or request.POST['password'].strip()=='' or request.POST['confirmPassword'].strip()==''):
                return render(request,"blog/register.html",{
                "error": True,
                "message": "Please fill the form correctly"
            })
            if(request.POST['password'].strip() != request.POST['confirmPassword'].strip()):
                return render(request,"blog/register.html",{
                "error": True,
                "message": "Password does not match with confirm password field."
            })
            newUser=User(username=request.POST['username'],fullName=request.POST['fullName'],password=request.POST['password'],confirmPassword=request.POST['confirmPassword'])
            newUser.save()
            return render(request,"blog/login.html")
        else:
            return render(request,"blog/register.html",{
                "error": True,
                "message": "Another user with this username already exists"
            })

    else:
        return render(request,"blog/register.html")
        

def authors(request):
    if("username" in request.session):
        return render(request,"blog/authors.html",{
            "page":"authors",
            "authors":User.objects.all(),
            "isLoggedIn": request.session['isLoggedIn'],
            "username":request.session['username'],
            "fullname":request.session['fullName']
        })
    else:
        return render(request,"blog/authors.html",{
            "page":"authors",
            "authors":User.objects.all(),
        })

def addBlog(request):
    if(request.method=="POST"):
        if(request.POST["title"].strip()=='' or request.POST["content"].strip()==''):
            return render(request,"blog/add-blog.html",{
                "page":"add-blog",
                "error": True,
                "message": "Please fill all the form fields.",
                "isLoggedIn": request.session['isLoggedIn'],
                "username":request.session['username'],
                "fullname":request.session['fullName'],
                "authorId":request.session['userId'],
            })
        else:
           blogAuthor= User.objects.get(id=int(request.POST["authorId"]))
           newBlog=Blog(title=request.POST["title"],content=request.POST["content"],author=blogAuthor)
           newBlog.save()
           return HttpResponseRedirect(f"/all-blogs")


    if("username" in request.session):
        return render(request,"blog/add-blog.html",{
            "page":"add-blog",
            "isLoggedIn": request.session['isLoggedIn'],
            "username":request.session['username'],
            "fullname":request.session['fullName'],
            "authorId":request.session['userId'],
        })
    else:
        return render(request,"blog/add-blog.html",{
            "page":"add-blog",
        })


def allBlogs(request):
    try:
        allBlogs=Blog.objects.all()
    except:
        return render(request,"blog/all-blogs.html",{
                "page":"all-blogs",
                "blogs":[],
                "isLoggedIn": request.session['isLoggedIn'],
                "username":request.session['username'],
                "fullname":request.session['fullName'],
                "authorId":request.session['userId'],
            })
    else:
        if("username" in request.session):
            return render(request,"blog/all-blogs.html",{
                "page":"all-blogs",
                "blogs":allBlogs,
                "isLoggedIn": request.session['isLoggedIn'],
                "username":request.session['username'],
                "fullname":request.session['fullName'],
                "authorId":request.session['userId'],
            })
        else:
            return render(request,"blog/all-blogs.html",{
                "page":"all-blogs",
                "blogs":allBlogs
            })

def blog(request,blogId):
    try:
        foundBlog=Blog.objects.get(id=blogId)
    except:
        return HttpResponseRedirect("/all-blogs")
    if "username" in request.session:
        # if "likedBlogs" in request.session:
        #     likedIds=request.session["likedBlogs"].split(',')
        #     try:
        #         findIndex=likedIds.index(f"{blogId}")
        #     except:
        #         return render(request,"blog/blog.html",{
        #             "page":"all-blogs",
        #             "blog":blog,
        #             "liked":False,
        #             "isLoggedIn":True,
        #             "username":request.session['username'],
        #             "fullname":request.session['fullName'],
        #             "authorId":request.session['userId'],
        #         })
        #     else:
        #         return render(request,"blog/blog.html",{
        #             "page":"all-blogs",
        #             "blog":blog,
        #             "liked":True,
        #             "isLoggedIn":True,
        #             "username":request.session['username'],
        #             "fullname":request.session['fullName'],
        #             "authorId":request.session['userId'],
        #         })
        # else:
        #     return render(request,"blog/blog.html",{
        #             "page":"all-blogs",
        #             "blog":blog,
        #             "liked":False,
        #             "isLoggedIn":True,
        #             "username":request.session['username'],
        #             "fullname":request.session['fullName'],
        #             "authorId":request.session['userId'],
        #         }) 
        foundUser=User.objects.get(id=int(request.session["userId"]))
        try:
            Likes.objects.get(blog=foundBlog,user=foundUser)
        except:
            return render(request,"blog/blog.html",{
                    "page":"all-blogs",
                    "blog":foundBlog,
                    "liked":False,
                    "isLoggedIn":True,
                    "username":request.session['username'],
                    "fullname":request.session['fullName'],
                    "authorId":request.session['userId'],
                })
        else:
           return render(request,"blog/blog.html",{
                    "page":"all-blogs",
                    "blog":foundBlog,
                    "liked":True,
                    "isLoggedIn":True,
                    "username":request.session['username'],
                    "fullname":request.session['fullName'],
                    "authorId":request.session['userId'],
                }) 
    else:
        return render(request,"blog/blog.html",{
                    "page":"all-blogs",
                    "blog":foundBlog,
                    "isLoggedIn":False,
                })


def logout(request):
    del request.session['username']
    del request.session['fullName']
    del request.session['isLoggedIn']
    del request.session['userId']
        
    return HttpResponseRedirect("/")
    


def likeBlog(request,blogId):
    user=User.objects.get(id=int(request.session["userId"]))
    blog=Blog.objects.get(id=int(blogId))
    like=Likes(user=user,blog=blog)
    like.save()

    return HttpResponseRedirect(f"/all-blogs/{blogId}")
    
