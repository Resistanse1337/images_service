from django.urls import path

from .views import *


urlpatterns = [
    path("", index, name="home"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path("user/", UserView.as_view(), name='get_user'),
    path("image/", ImageView.as_view(), name="image"),
    path("image/<int:_id>", ImageView.as_view(), name="image_with_user_id"),
    path("image/delete_all", delete_all_images, name="delete_all")
]
