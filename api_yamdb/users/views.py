from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from api.services import get_all_objects
from api.serializers import UserSerializer
from users.serializers import AuthSerializer, SignUpSerializer
from users.services import get_tokens_for_user
from .services import generate_verification_code, send_verification_email

User = get_user_model()


class Auth(GenericAPIView):
    # Этот класс пока очень сырой, я буду его дорабатывать,
    # но он начал работать!
    serializer_class = AuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = get_object_or_404(
            User,
            username=data.get('username'),
            confirmation_code=data.get('confirmation_code'),
        )
        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)


class Signup(mixins.CreateModelMixin,
             viewsets.GenericViewSet):
    queryset = get_all_objects(User)
    serializer_class = SignUpSerializer

    def perform_create(self, serializer, user=User):
        verification_code = generate_verification_code()
        user.profile.verification_code = verification_code
        user.profile.save()

        send_verification_email(user.email, verification_code)
        return Response({'message': 'Регистрация прошла успешно. Проверьте вашу почту для активации аккаунта.'},
                        status=status.HTTP_201_CREATED)
