from django.urls import path

from . import views

urlpatterns=[
    path("",views.index,name="index_page"),
    path("login",views.login , name="login_page"),
    path("register",views.register , name="register_page"),
    path("authors",views.authors,name='authors'),
    path("add-blog",views.addBlog,name="add-blog"),
    path("all-blogs",views.allBlogs,name="all-blogs"),
    path("logout",views.logout,name="logout"),
    path("all-blogs/<int:blogId>",views.blog,name="single-blog"),
    path("like-blog/<int:blogId>",views.likeBlog,name="like-blog")
]