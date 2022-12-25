from django.urls import path
from . import views
urlpatterns = [
    path("login/",views.loginPage,name="login"),
    path("register/", views.registerPage, name="register"),
    path('user/',views.userPage,name='user-page'),
    path("logout/", views.logoutUser, name="logout"),
    path("",views.home,name="home"),
    path("customers/<int:pk>",views.customers,name="customers"),
    path("products/",views.products,name="products"),
    path("create_order/",views.createOrder,name="create-order"),
    path("update_order/<int:pk>", views.updateOrder, name="update-order"),
    path("delete_order/<int:pk>", views.deleteOrder, name="delete-order"),
    path('account/',views.account_settings,name='account')
]
