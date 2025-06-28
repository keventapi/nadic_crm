from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_page, name='login'),
    path('signup', views.signup_page, name='signup'),
    path('product_user', views.add_product, name='product_user'),
    path('product_view/<int:product_id>', views.view_product, name="product_view"),
    path('product_edit/<int:product_id>', views.edit_product, name="edit_product"),
    path('faturamento', views.faturamento, name="faturamento"),
    path('profile/<int:user_id>', views.profile, name="profile"),
    path('auto_complete', views.auto_complete, name='auto_complete'),
]
