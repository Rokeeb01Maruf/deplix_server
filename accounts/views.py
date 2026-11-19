from rest_framework import generics
from rest_framework.response import Response
from .serializers import SignUpSerializer, EmailVerificationSerializer, SigninSerializer
from django.db import IntegrityError
from utils.otp import hash_otp, store_otp, retrieve_otp, verify_otp
from utils.email import send_email_verification_otp
import secrets
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


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

            otp = f"{secrets.randbelow(1_000_000):06d}"
            store = store_otp(user_id=user.id, purpose="email", hash=hash_otp(otp=otp))
            send_email_verification_otp(user.email, otp, user.first_name)

            return Response(
                {
                    "success" : True,
                    "message" : "account created successfully",
                    "data" : self.serializer_class(user).data
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
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "internal server error",
                    "error" : str(e)
                },
                status=500                
            )
        

class EmailVerifyView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : serializer.errors,
                },
                status=400
            )

        otp = serializer.validated_data.get("otp")
        user_id = serializer.validated_data.get("id")

        try:
            digested = retrieve_otp(user_id=user_id, purpose="email")
            if digested == None: raise ValueError("invalid")
            verify = verify_otp(digested=digested, digest=hash_otp(otp))
            if not verify: raise ValueError("invalid")
        except ValueError:
            return Response({
                "success" : False,
                "message" : "bad request",
                "error" : "invalid or expired otp"
            },
            status=400)

        try:
            user = serializer.save()
        except ValueError:
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : "email already verified"
                },
                status=400
            )
        except Exception:
            return Response(
                {
                    "success" : False,
                    "message" : "internal server error",
                    "error" : "server failed to verify user"
                },
                status=500
            )

        tokens = RefreshToken.for_user(user)

        return Response(
            {
                "success" : True,
                "message" : "email verified successfully",
                "data" : {
                    "id": user.id
                },
                "tokens" : {
                    "access" : str(tokens.access_token),
                    "refresh" : str(tokens)
                }
            },
            status=200
        )

class SigninView(generics.GenericAPIView):
    serializer_class = SigninSerializer
    def post(self, request):
        serializers = self.serializer_class(data=request.data)

        if not serializers.is_valid():
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : serializers.errors
                },
                status=400
            )

        try:
            user = serializers.save()

            if not user.is_email_verified:
                return Response(
                    {
                        "success" : False,
                        "message" : "bad request",
                        "errors" : "email is unverified"
                    },
                    status=400
                )

            if not user.is_active:
                return Response(
                    {
                        "success" : False,
                        "message" : "unauthorized",
                        "error" : "You are not permitted to perform this action"
                    },
                    status=401
                )

            if not user.check_password(serializers.validated_data.get("password")):
                raise User.DoesNotExist("invalid")

        except User.DoesNotExist:
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : "invalid email or password"
                },
                status=400
            )

        tokens = RefreshToken.for_user(user=user)

        return Response(
            {
                "success" : True,
                "message" : "signin successful",
                "data" : {
                    "id" : user.id
                },
                "tokens" : {
                    "access" : str(tokens.access_token),
                    "refresh" : str(tokens)
                }
            },
            status=200
        )