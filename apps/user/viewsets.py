"""User views."""
# Rest Framework
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action

# permision
from rest_framework.permissions import (IsAuthenticated, AllowAny)
# from apps.serializers.profiles import ProfileModelSerializer
# from ..permisisions import IsAccountOwner

# Serializers
from apps.user.serializers import UserModelSerializer, UserLoginSerializer

# from apps.user.serializers import (UserLoginSerializer,
#                                  UserModelSerializer,
#                                  UserCreateSerializer,
#                                  UserVerifySerializer,
#                                  UserExistAccountSerializer,
#                                  UserResetPasswordSerializer)

# models
from apps.user.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    #login
    
class UserLoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserLoginSerializer
    lookup_field = 'username'

    #login

    def create(self, request, *args, **kwargs):
        """Create user."""
        
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data_user = UserModelSerializer(user).data
        data_user.pop('password')
        data = {
            'user': data_user,
            'acces_token': token
        }
        #return Response(data, status=status.HTTP_200_OK)


        # serializer = UserModelSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.save()
        # data = self.get_serializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


    # def get_permissions(self):
    #     """Assign permissions based on action."""
    #     if self.action in ['create_user', 'login', 'reset_password', 'exist_account', 'verify_and_reset_password', 'list_users', 'destroy', 'update']:
    #         permission_classes = [AllowAny]
    #     elif self.action in ['retrieve', 'update', 'partial_update', 'profile']:
    #         # permission_classes = [IsAuthenticated,IsAccountOwner]
    #         permission_classes = [AllowAny]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]

    # @action(detail=False, methods=['post'])
    # def create_user(self, request):
    #     """Sign up user."""
    #     serializer = UserCreateSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     data = self.get_serializer(user).data
    #     return Response(data, status=status.HTTP_201_CREATED)

    # def exist_account(self, email):
    #     """Verify exist account."""
    #     user = User.objects.filter(email=email)
    #     if user.exists():
    #         user = user.first()
    #         data = UserExistAccountSerializer(user).data
    #         return data
    #     else:
    #         return False

    # @action(detail=False, methods=['post'])
    # def login(self, request):
    #     """Login user."""
    #     passwd = request.data.get('password')
    #     if not passwd:
    #         result = self.exist_account(request.data.get('email'))
    #         if result:
    #             return Response(result, status=status.HTTP_200_OK)
    #         else:
    #             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = UserLoginSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user, token = serializer.save()
    #     data = {
    #         'user': UserModelSerializer(user).data,
    #         'acces_token': token
    #     }
    #     return Response(data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'])
    # def verify



# class UserViewSet(mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin,
#                   viewsets.GenericViewSet):
#     """
#         User view set
#         Handle sign up, login and verification user
#     """
#     queryset = User.objects.filter(is_active=True)
#     serializer_class = UserModelSerializer
    #lookup_field = 'username'

    # def get_permissions(self):
    #     """Assign permissions based on action."""
    #     if self.action in ['create_user', 'login', 'reset_password', 'exist_account', 'verify_and_reset_password', 'list_users', 'destroy', 'update']:
    #         permission_classes = [AllowAny]
    #     elif self.action in ['retrieve', 'update', 'partial_update', 'profile']:
    #         # permission_classes = [IsAuthenticated,IsAccountOwner]
    #         permission_classes = [AllowAny]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]

    # @action(detail=False, methods=['post'])
    # def create_user(self, request):
    #     """Sign up user."""
    #     serializer = UserCreateSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     data = self.get_serializer(user).data
    #     return Response(data, status=status.HTTP_201_CREATED)

    # def exist_account(self, email):
    #     """Verify exist account."""
    #     user = User.objects.filter(email=email)
    #     if user.exists():
    #         user = user.first()
    #         data = UserExistAccountSerializer(user).data
    #         return data
    #     else:
    #         return False

    # @action(detail=False, methods=['post'])
    # def login(self, request):
    #     """Login user."""
    #     passwd = request.data.get('password')
    #     if not passwd:
    #         result = self.exist_account(request.data.get('email'))
    #         if result:
    #             return Response(result, status=status.HTTP_200_OK)
    #         else:
    #             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = UserLoginSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user, token = serializer.save()
    #     data = {
    #         'user': UserModelSerializer(user).data,
    #         'acces_token': token
    #     }
    #     return Response(data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'])
    # def verify_and_reset_password(self, request):
    #     """verify_and_reset_password user."""
    #     serializer = UserVerifySerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     data = {
    #         'message': 'Bienvenido. Su contraseña ha sido cambiada'
    #     }
    #     return Response(data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['post'])
    # def reset_password(self, request):
    #     """Set password user."""
    #     account = self.exist_account(request.data.get('email'))
    #     if not account:
    #         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    #     if account['is_verified']:
    #         serializer = UserResetPasswordSerializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save(data=request.data)
    #         data = {
    #             'message': 'Password reset successfully.'
    #         }
    #         return Response(data, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'error': 'User not verified'}, status=status.HTTP_404_NOT_FOUND)

    # @action(detail=True, methods=['put', 'patch'])
    # def profile(self, request, *args, **kwargs):
    #     """Update profile user."""
    #     user = self.get_object()
    #     profile = user.profile
    #     partial = request.method == 'PATCH'
    #     serializer = ProfileModelSerializer(
    #         profile, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     data = UserModelSerializer(user).data
    #     return Response(data, status=status.HTTP_200_OK)

    # def retrieve(self, request, *args, **kwargs):
    #     """Retrieve user profile."""
    #     response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
    #     response.data['profile'] = ProfileModelSerializer(
    #         self.get_object().profile).data
    #     return response

    # @action(detail=False, methods=['get'])
    # def list_users(self, request):
    #     """List users."""
    #     users = User.objects.filter(is_active=True)
    #     data = UserModelSerializer(users, many=True).data
    #     return Response(data, status=status.HTTP_200_OK)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.is_active = False
    #     self.perform_destroy(instance)
    #     return Response({'detail': 'eliminado'}, status=status.HTTP_200_OK)

    # def update(self, request, *args, **kwargs):
    #     """ Update user """
    #     #partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(
    #         instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)
