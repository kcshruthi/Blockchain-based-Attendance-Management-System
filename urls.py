from django.urls import path, include
from . import views

# urlpatterns is the list of url paths that connect the web application.
urlpatterns = [
    # These are the user authentication urls. Each is linked to a function
    # in views.py.
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('logout/', views.logoutuser, name="logoutuser"),

    # These are the urls corresponding to the blockchain implementation
    # part of the website.
    path('dashboard/', views.dashboard, name="dashboard"),
    path('create_course/', views.create_course, name="create_course"),
    path('success/', views.success, name="success"),
    path('course_view/<int:chain_id>/', views.course_view, name="course_view"),
    path('mark_attendance/<int:chain_id>/', views.mark_attendance, name="mark_attendance"),
    path('attendance_view/<int:chain_id>/<int:block_id>/', views.attendance_view, name="attendance_view"),
    path('attendance_view/<int:chain_id>/', views.integrity, name="integrity"),
]