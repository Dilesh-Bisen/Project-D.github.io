from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Student
from django.db.models import Q, Sum
from .seed import generate_reportcard
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


@login_required(login_url="/login")
def student_page(request):
    if request.method == "POST":
        data = request.POST

        stu_name = data.get("stu_name")
        stu_description = data.get("stu_description")
        stu_image = request.FILES.get("stu_image")

        print(stu_name)
        print(stu_description)
        print(stu_image)

        College_Student.objects.create(
            stu_name=stu_name,
            stu_description=stu_description,
            stu_image=stu_image,
        )

        return redirect("/student_page")

    queryset = College_Student.objects.all()

    if request.GET.get("search_student"):
        queryset = queryset.filter(stu_name__icontains=request.GET.get("search_student"))

    context = {"student_page": queryset, "heading": "Students Data"}

    return render(request, "student_page.html", context)


@login_required(login_url="/login")
def delete_student(request, id):
    queryset = College_Student.objects.get(id=id)
    queryset.delete()
    return redirect("/student_page")


@login_required(login_url="/login")
def update_student(request, id):
    queryset = College_Student.objects.get(id=id)

    if request.method == "POST":
        data = request.POST

        stu_name = data.get("stu_name")
        stu_description = data.get("stu_description")
        stu_image = request.FILES.get("stu_image")

        print(stu_name)
        print(stu_description)
        print(stu_image)

        queryset.stu_name = stu_name
        queryset.stu_description = stu_description
        queryset.stu_image = stu_image

        queryset.save()

        return redirect("/student_page")

    context = {"student_page": queryset, "heading": "Update Student Data"}
    return render(request, "update_student.html", context)


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already exists.")
            return redirect("/register")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)

        user.save()
        messages.info(request, "Account created successfully. Pls log in.")

        return redirect("/login")

    context = {"heading": "Register Page"}
    return render(request, "register.html", context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)
        if not user.exists():
            messages.info(request, "Invalid Username.")
            return redirect("/login")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Invalid Password.")
            return redirect("/login")
        else:
            login(request, user)
            return redirect("/student_page")

    context = {"heading": "Login Page"}
    return render(request, "login.html", context)


def logout_page(request):
    logout(request)
    return redirect("/login")


def get_students(request):
    queryset = Student.objects.annotate(
        total_marks=Sum("studentmarks__marks")
    ).order_by("-total_marks")

    if request.GET.get("search"):
        queryset = queryset.filter(
            Q(student_id__student_id__icontains=request.GET.get("search"))
            | Q(department__department__icontains=request.GET.get("search"))
            | Q(student_name__icontains=request.GET.get("search"))
            | Q(student_email__icontains=request.GET.get("search"))
            | Q(student_age__icontains=request.GET.get("search"))
        )

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request, "report/student.html", {"page_obj": page_obj, "heading": "Student"}
    )


def see_marks(request, student_id):
    # generate_reportcard()
    queryset = SubjectMarks.objects.filter(student__student_id__student_id=student_id)

    current_rank = -1
    ranks = Student.objects.annotate(marks=Sum("studentmarks__marks")).order_by(
        "-marks", "-student_age"
    )
    i = 1
    for rank in ranks:
        if student_id == rank.student_id.student_id:
            current_rank = i
            break
        i += 1

    total_marks = queryset.aggregate(total_marks=Sum("marks"))

    context = {
        "queryset": queryset,
        "current_rank": current_rank,
        "total_marks": total_marks,
        "heading": "Report-Card",
    }
    return render(request, "report/see_marks.html", context)
