"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from home.views import *
from student.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("about", about, name="about"),
    path("contact", contact, name="contact"),
    path("success_page", success_page, name="success_page"),
    path("student_page", student_page, name="student_page"),
    path("delete-student<id>", delete_student, name="delete_student"),
    path("update-student<id>", update_student, name="update_student"),
    path("register", register_page, name="register_page"),
    path("login", login_page, name="login_page"),
    path("logout", logout_page, name="logout_page"),
    path("student", get_students, name="get_students"),
    path("marks<student_id>", see_marks, name="see_marks"),
    path("mail", send_email, name="send_email"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
