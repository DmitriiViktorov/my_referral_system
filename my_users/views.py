from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import MyUser
from .serializers import MyUserSerializer
from .utils import set_code_to_cache, get_code_from_cache, verify_phone_number
import random
import time


class AuthView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Phone number of the user, starts from 7 or 8, contains 11 digits'
                ),
            },
            required=['phone_number'],
        ),
        responses={200: 'Code sent successfully', 400: 'Bad request'}
    )

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not verify_phone_number(phone_number):
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

        user_exists = MyUser.objects.filter(phone_number=phone_number).exists()
        if user_exists:
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        code = ''.join(random.choices('0123456789', k=4))
        set_code_to_cache(code, phone_number)

        time.sleep(random.uniform(1, 3))
        return Response({'code': code}, status=status.HTTP_200_OK)

class VerifyCodeView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Phone number of the user, starts from 7 or 8, contains 11 digits'
                ),
                'code': openapi.Schema(type=openapi.TYPE_STRING, description='Verification code')
            },
            required=['phone_number', 'code']
        ),
        responses={200: 'User authenticated', 400: 'Bad request'}
    )
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        if not phone_number or not code:
            return Response({'error': 'phone_number and code are required'}, status=status.HTTP_400_BAD_REQUEST)

        if not verify_phone_number(phone_number):
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)

        verify_code = get_code_from_cache(code, phone_number)
        if not verify_code:
            return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = MyUser.objects.get_or_create(phone_number=phone_number)

        if created:
            user.save()

        return Response({'message': 'User authenticated', "user_id": user.id}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: 'User profile retrieved', 404: 'User not found'}
    )
    def get(self, request, user_id):
        try:
            user = MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MyUserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'invite_code': openapi.Schema(type=openapi.TYPE_STRING, description='Invite code')
            },
            required=['invite_code']
        ),
        responses={200: 'Invite code applied', 400: 'Bad request', 404: 'User not found'}
    )
    def post(self, request, user_id):

        try:
            user = MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        invite_code = request.data.get('invite_code')
        if not invite_code:
            return Response({"error": "Invite code is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            referred_by = MyUser.objects.get(invite_code=invite_code)
        except MyUser.DoesNotExist:
            return Response({"error": "Invalid invite code"}, status=status.HTTP_400_BAD_REQUEST)

        if user.referred_by:
            return Response({"error": "Invite code already used"}, status=status.HTTP_400_BAD_REQUEST)

        user.referred_by = referred_by
        user.save()
        return Response({"message": "Invite code applied"})

