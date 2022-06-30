from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .forms import *
from .serializers import *


def index(request):
    user_id = request.user.id

    user_images = Image.objects.filter(user__id=user_id)
    serializer = ImageSerializer(user_images, many=True)

    context = {}
    context.update({"images": serializer.data})

    return render(request, 'base.html', context)


@staff_member_required
@api_view(["POST"])
def delete_all_images(request):
    Image.objects.all().delete()

    return Response(status=status.HTTP_200_OK, data="Deleted all images")


class ImageView(APIView):
    def post(self, request, _id):
        user_id_from_request = request.user.id

        try:
            user = User.objects.get(id=_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data="User not found")

        if user.id != user_id_from_request:
            return Response(status=status.HTTP_403_FORBIDDEN, data="Forbidden")

        file = request.FILES['image']

        image = Image(image=file, user=user)
        image.save()

        return redirect("home")

    def get(self, request, _id):
        user_images = Image.objects.filter(user__id=_id)
        serializer = ImageSerializer(user_images, many=True)

        return Response(serializer.data)

    @method_decorator(login_required, name='dispatch')
    def delete(self, request, _id):
        user_id_from_request = request.user.id

        try:
            image = Image.objects.get(id=_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data="Image not found")

        if image.user.id == user_id_from_request:
            image.delete()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data="You can not delete another user`s image")

        return Response(status=status.HTTP_200_OK, data="Deleted")


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserView(APIView):
    def get(self, request):
        user_id = request.user.id

        try:
            user = User.objects.get(id=user_id)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data="User not found")

        serializer = UserSerializer(user)

        return Response(status=status.HTTP_200_OK, data=serializer.data)






