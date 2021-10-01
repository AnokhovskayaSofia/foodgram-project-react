from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SubscribedUser, User
from .serializers import SubscribeSerializer, UserSerializer


class UserViewSet(UserViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    queryset = User.objects.all()

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        subscribes = User.objects.filter(user_subscribed_to__user=request.user)
        queryset = SubscribedUser.objects.filter(user=self.request.user)
        page = self.paginate_queryset(subscribes)
        if page is not None:
            serializer = SubscribeSerializer(page, many=True,
                                             context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True,
                                         context={'request': request})
        return Response(serializer.data)

    @action(detail=True,
            methods=['GET', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        if request.method == 'GET':
            user_subscribed_to = get_object_or_404(User, pk=id)
            serializer = SubscribeSerializer(user_subscribed_to)

            if SubscribedUser.objects.filter(user=self.request.user,
                                             user_subscribed_to=user_subscribed_to).exists():
                return Response({'errors': 'Вы уже подписаны на пользователя'})
            else:
                SubscribedUser.objects.create(user=self.request.user,
                                              user_subscribed_to=user_subscribed_to)
            return Response(serializer.data)
        if request.method == 'DELETE':
            user_subscribed_to = get_object_or_404(User, pk=id)
            if SubscribedUser.objects.filter(user=self.request.user,
                                             user_subscribed_to=user_subscribed_to).exists():
                instance = SubscribedUser.objects.filter(user=self.request.user,
                                                         user_subscribed_to=user_subscribed_to)
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'errors': 'Вы не подписаны на пользователя'},
                                status=status.HTTP_400_BAD_REQUEST)
