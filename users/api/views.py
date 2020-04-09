from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer, ProfileSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from users.models import Profile
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes


@api_view(['POST'])
def register(request):
    acc_serializer = AccountSerializer(data=request.data)
    data = {}
    if acc_serializer.is_valid():
        user = acc_serializer.save()
        data["token"] = Token.objects.get(user=user).key
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(acc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile_update(request):
    pserializer = ProfileSerializer(Profile.objects.get(user=request.user), data=request.data)
    userializer = UserSerializer(request.user, data=request.data)
    if pserializer.is_valid() and userializer.is_valid():
        pserializer.save()
        userializer.save()
        return Response({'success': 'Your profile has been successfully updated.'}, status=status.HTTP_200_OK)
    return Response({'failed': 'failed to update profile.'}, status=status.HTTP_400_BAD_REQUEST)
