from .views_handler import super_user_views, logged_user_views, logged_out_views, event_views
from .api_views_handler import logged_views, loggedout_views
from .api_views_handler import superuser_view
from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'cart', logged_views.CartViewSet, basename='cart')
router.register(r'product-types', logged_views.ProductTypeViewSet, basename='producttype')
router.register(r'products', logged_views.ProductViewSet, basename='product')
router.register(r'manage-products', logged_views.ProductManipulationSet, basename='product-manipulation')
router.register(r'comissionupdate', superuser_view.ComissionViewSet, basename='comissionupdate')



urlpatterns = [
    path('', logged_user_views.Index.as_view(), name="index"),
    path('login', logged_out_views.login_page, name='login'),
    path('signup', logged_out_views.signup_page, name='signup'),
    path('product_user', logged_user_views.add_product, name='product_user'),
    path('product_view/<int:product_id>', logged_user_views.view_product, name="product_view"),
    path('product_edit/<int:product_id>', logged_user_views.edit_product, name="edit_product"),
    path('faturamento', super_user_views.faturamento, name="faturamento"),
    path('profile/<int:user_id>', logged_user_views.Profile.as_view(), name="profile"),
    path('auto_complete', event_views.auto_complete, name='auto_complete'),
    path('create_staff_account', super_user_views.create_staff_account, name="staff_account"),
    path('cart', logged_user_views.ViewCart.as_view(), name='cart'),
    path('dashboard', logged_user_views.SellerDashboard.as_view(), name='seller_dashboard'),
    path('comission', super_user_views.comission_update, name='comission_update'),
    path('buy/<int:product_id>/<int:quantity>', logged_user_views.buy_item, name="buy_item"),
    path('add_cart/<int:product_id>/<int:quantity>', logged_user_views.add_to_cart, name="add_to_cart"),
    path('deletefromcart/<int:product_id>', logged_user_views.remove_from_cart, name="removefromcart"),
    path('logout', logged_user_views.handle_logout, name="logout"),
    path('api/', include(router.urls)),
    path('api/faturamento', superuser_view.faturamento, name='faturamento'),
    path('api/buyitem', logged_views.BuyItem.as_view(), name="buyitem"),
    path('api/cartbuy', logged_views.BuyAllFromCart.as_view(), name="cartbuy"),
    path('api/addtocart', logged_views.AddToCart.as_view(), name="addtocart"),
    path('api/removefromcart', logged_views.RemoveCartItem.as_view(), name="removecartitem"),
    path('api/signup', loggedout_views.signup_user, name="signup")
]
