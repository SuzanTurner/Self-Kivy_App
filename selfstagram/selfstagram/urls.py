from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # This will require login due to @login_required
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('like/<int:image_id>/', views.toggle_like, name='toggle_like'),
    path('comment/<int:image_id>/', views.add_comment, name='add_comment'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('search/', views.search_users, name='search_users'),
    path('delete/image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('delete/comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/feed/", views.FeedAPIView.as_view(), name="api_feed"),
    path("api/users/me/",views.MyProfileAPIView.as_view(),name="api_my_profile"),
    path("api/users/<str:username>/",views.UserProfileAPIView.as_view(),name="api_user_profile"),
    path("api/users/<int:user_id>/follow/",views.FollowAPIView.as_view(),name="api_follow"),
    path("api/users/<int:user_id>/unfollow/",views.UnfollowAPIView.as_view(),name="api_unfollow"),
    path("api/posts/",views.CreatePostAPIView.as_view(),name="api_create_post"),
    path("api/search/", views.SearchUsersAPIView.as_view(), name="api_search_users"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
