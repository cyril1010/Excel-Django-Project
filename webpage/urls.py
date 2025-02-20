from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.user_login_page, name='user_login_page'),
    path('userLogin/', views.userLogin, name='userLogin'),
    path('userLogout/', views.userLogout, name='userLogout'),

    path('userSignup/', views.userSignup, name='userSignup'),

    path('all_products/', views.all_products, name='all_products'),
    path('user-contact/', views.user_contact_page, name='user_contact_page'),
    path('contact_save/', views.contact_save, name='contact_save'),
    path('product_page/<prod_name>/', views.product_page, name="product_page"),
    path('filtered_page/<cat_name>/', views.filtered_page, name="filtered_page"),

    path('cart/', views.cart, name='cart'),
    path('save_cart/', views.save_cart, name='save_cart'),
    path('delete_cart_item/<cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),

    path('checkout/', views.checkout, name="checkout"),
    path('save_order/', views.save_order, name="save_order"),

    path('checkout/', views.checkout, name="checkout"),
    path('payment/', views.payment, name="payment"),

    path('save_newsletter/', views.save_newsletter, name="save_newsletter"),

    path('about/', views.about, name="about"),
    path('blog/', views.blog, name="blog"),

]