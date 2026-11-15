from rest_framework import generics
from rest_framework.response import Response
from .serializers import SignUpSerializer
from django.db import IntegrityError

class HomeView(generics.GenericAPIView):
    def get(self, request):
        return Response({"message": "Welcome to the Home Page!"})
    
class UserSignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "bad request",
                    "errors": serializer.errors,
                },
                status=400
            )

        try:
            user = serializer.save()

            return Response(
                {
                    "success" : True,
                    "message" : "account created successfully",
                    "data" : self.serializer_class(user)
                },
                status=201
            )
        except IntegrityError:
            return Response(
                {
                    "success": False,
                    "message": "bad request",
                    "errors": "user already exist"
                },
                status=400
            )
        except Exception:
            return Response(
                {
                    "success": False,
                    "message": "internal server error"
                },
                status=500                
            )
