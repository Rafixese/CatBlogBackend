from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from rest_framework import status
from django.http import JsonResponse
from .serializers import LoginSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    request=LoginSerializer,  # Document request body structure
    responses={200: None},    # Define response codes (optional)
)
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("User authenticated:", user)  # Debugging line
            login(request, user)
            return JsonResponse({"message": "Login successful", "sessionid": request.session.session_key})
        else:
            print("Authentication failed")  # Debugging line
            return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
