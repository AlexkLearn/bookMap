from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.visitor_view, name="home"),
    path('login/', views.login_user, name="login"),
    path('register/', views.register, name="register"),
    path('add_book/', views.add_book, name='add_book'),
    path('edit/<int:pk>', views.edit_book, name="edit_book"),
    path('borrow/', views.borrow_book, name="borrow_book"),
    path('return/<int:pk>', views.return_book, name="return_book"),
    path('report-damage/', views.report_damage, name="report_damage"),
    path('logout/', views.logout_user, name="logout")
]