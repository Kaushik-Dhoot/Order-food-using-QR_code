from django.contrib import admin
from django.urls import path, include
from cafe import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.menu, name='menu'),
    path('delete_dish/<int:item_id>/', views.delete_dish, name='delete_dish'),
    path('offers', views.offers, name='offers'),
    path('reviews', views.reviews, name='reviews'),
    path('profile', views.profile, name='profile'),
    path('all_orders', views.all_orders, name='all_orders'),
    path('manage_menu', views.manage_menu, name='manage_menu'),
    path('cart', views.cart, name='cart'),
    # path('checkout', views.checkout, name='checkout'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('login', views.Login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.Logout, name='logout'),
    path('generate_bill', views.generate_bill, name='generate_bill'),
    path('view_bills', views.view_bills, name='view_bills'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
