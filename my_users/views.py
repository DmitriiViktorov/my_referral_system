from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MyUser
from .serializers import MyUserSerializer

import random
import time


class AuthView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        #TODO:
        #система временного хранения кода. Встроенный кеш, редис или в БД?
        code = ''.join(random.choices('0123456789', k=4))
        time.sleep(random.uniform(1, 3))
        return Response({'code': code}, status=status.HTTP_200_OK)

class VerifyCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        if not phone_number or not code:
            return Response({'error': 'phone_number and code are required'}, status=status.HTTP_400_BAD_REQUEST)

        #TODO:
        #Проверка кода, сравнение с данными из хранилища
        user, created = MyUser.objects.get_or_create(phone_number=phone_number)
        if created:
            user.save()

        return Response({'message': 'User authenticated', "user_id": user.id}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    def get(self, request, user_id):
        try:
            user = MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MyUserSerializer(user)
        return Response(serializer.data)


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

