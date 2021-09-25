from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .permissions import IsAdminUser
from .serializers import ActivationSerializer, UserSerializer
from .tokens import account_activation_token
from .utils import get_tokens_for_user


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     permission_classes = [IsAuthenticated, IsAdminUser, ]

#     pagination_class = PageNumberPagination
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['username', ]
#     lookup_field = 'username'
#     lookup_value_regex = '[^/]+'

#     @action(
#         detail=False,
#         methods=['get', 'patch'],
#         permission_classes=[IsAuthenticated])
#     def me(self, request, pk=None):
#         user = request.user
#         if request.method == 'GET':
#             serializer = self.get_serializer(user)
#             return Response(serializer.data)
#         serializer = self.get_serializer(user,
#                                          data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(role=user.role, partial=True)
#         return Response(serializer.data)


# @api_view(['POST'])
# def signup(request):
#     serializer = UserSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.save(is_active=False)

#     current_site = get_current_site(request)
#     subject = 'Activate Your YaMDb Account'
#     message = render_to_string('emails/account_activation_email.html', {
#         'username': user.username,
#         'domain': current_site.domain,
#         'confirmation_code': account_activation_token.make_token(user)
#     })
#     user.email_user(subject, message)

#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# def activate(request):
#     activation = ActivationSerializer(data=request.data)
#     activation.is_valid(raise_exception=True)
#     user = get_object_or_404(User, email=activation.validated_data['email'])

#     if (activation.validated_data['confirmation_code']
#             == request.data['confirmation_code']):
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(
#             is_active=True,
#             email_confirmed=True,
#         )
#         tokens = get_tokens_for_user(user)
#         return Response({'token': tokens['access']})

#     return Response(status=status.HTTP_403_FORBIDDEN)
