from django.urls import path
from .views import *
from dashboard.category import views as ctg_views
from dashboard.product import views as pro_views
from dashboard.brands import views as brd_views

urlpatterns = [
    path('category/', ctg_views.ctg_list_detail, name="dashboard_ctg_list"),
    path('category/<int:pk>/', ctg_views.ctg_list_detail, name="dash_ctg_detail"),
    path('ctg/del/<int:dlt>/', ctg_views.del_conf_delete, name="dash_ctg_delete"),
    path('ctg/conf/<int:pk>/', ctg_views.del_conf_delete, name="dash_ctg_conf"),
    path('ctg/add/', ctg_views.edit_add, name="dash_ctg_add"),
    path('ctg/edit/<int:pk>/', ctg_views.edit_add, name="dash_ctg_edit"),



    path('product/', pro_views.ctg_list_detail, name="dashboard_pro_list"),
    path('product/<int:pk>', pro_views.ctg_list_detail, name="dash_pro_detail"),
    path('product/conf/<int:pk>/', pro_views.del_conf_delete, name="dash_pro_conf"),
    path('product/del/<int:dlt>/', pro_views.del_conf_delete, name="dash_pro_delete"),
    path('product/add/', pro_views.edit_add, name="dash_pro_add"),
    path('product/edit/<int:pk>/', pro_views.edit_add, name="dash_pro_edit"),


    path('brands/', brd_views.ctg_list_detail, name="dashboard_brd_list"),
    path('brands/<int:pk>', brd_views.ctg_list_detail, name="dash_brd_detail"),
    path('brands/conf/<int:pk>/', brd_views.del_conf_delete, name="dash_brd_conf"),
    path('brands/del/<int:dlt>/', brd_views.del_conf_delete, name="dash_brd_delete"),
    path('brands/add/', brd_views.edit_add, name="dash_brd_add"),
    path('brands/edit/<int:pk>/', brd_views.edit_add, name="dash_brd_edit"),


    path("", index, name="dashboard_home"),
    path("register/", register, name="dashboard_register"),
    path("login/", dashboard_login, name="dashboard_login"),
    path("logout/", dashboard_logout, name="dashboard_logout"),

]