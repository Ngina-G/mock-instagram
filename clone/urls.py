from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path 
from . import views

urlpatterns=[
    re_path('^$', views.home, name='home'),
    re_path('^post_form/', views.user_image_request, name='pofile_edit'),
    re_path('^profile/<user_name>/', views.profile, name='profile'),
    re_path('^user_profile/<username>/', views.user_profile, name='user_profile'),
    re_path('^post/<id>', views.post_comment, name='comment'),
    re_path('^like/<int:pk>', views.LikeView, name='like_image'),
    re_path('^search/', views.search_profile, name='search'),
    re_path('^signup/', views.signup, name ='signup'),
    re_path('logout/',views.logout_user, name='logout'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)