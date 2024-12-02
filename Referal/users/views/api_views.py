# users/views/api_views.py
from users.models import PhoneNumberVerification
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated
from users.serializers import PhoneNumberVerificationSerializer, UserSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class UserDetailAPIView(generics.RetrieveAPIView):
    # permission classes swiched to AllowAny for testing
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserDetailByIdAPIView(generics.RetrieveAPIView):
    # permission classes swiched to AllowAny for testing
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhoneNumberVerificationSerializer
    serializer_class = UserSerializer
    lookup_field = "id"

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        user_id = self.kwargs.get("id")
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound(detail="User not found.")


class ProfileReferralsAPIView(generics.GenericAPIView):
    # permission classes swiched to AllowAny for testing
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhoneNumberVerificationSerializer

    def get(self, request, *args, **kwargs):
        if getattr(self, "swagger_fake_view", False):
            return Response()  # needed for correct generation of the scheme

        user_id = kwargs.get("id")
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise NotFound(detail="User not found.")
        else:
            user = request.user
            if not user.is_authenticated:
                return Response({"detail": "You must use the endpoint with user ID: /api/profile-referals/<int:id>/"}, status=status.HTTP_403_FORBIDDEN)

        phone_verification = PhoneNumberVerification.objects.get(user=user)

        # We get a list of users who used the invite code of the specified user
        invited_users = PhoneNumberVerification.objects.filter(activated_referal_number=phone_verification.referal_number)
        serializer = PhoneNumberVerificationSerializer(invited_users, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user_id = self.kwargs.get("id")
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise NotFound(detail="User not found.")
        else:
            user = self.request.user
            if not user.is_authenticated:
                raise NotAuthenticated(detail="Authentication credentials were not provided.")

        phone_verification = PhoneNumberVerification.objects.get(user=user)
        return PhoneNumberVerification.objects.filter(activated_referal_number=phone_verification.referal_number)


class PhoneNumberVerificationCreateAPIView(generics.CreateAPIView):
    # permission classes swiched to AllowAny for testing
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhoneNumberVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PhoneNumberVerificationUpdateAPIView(generics.UpdateAPIView):
    # permission classes swiched to AllowAny for testing
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhoneNumberVerificationSerializer
    lookup_field = "phone_number"

    def get_queryset(self):
        return PhoneNumberVerification.objects.all()
