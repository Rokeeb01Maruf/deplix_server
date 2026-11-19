from rest_framework import generics
from rest_framework.response import Response
from .serializers import SignUpSerializer, EmailVerificationSerializer, SigninSerializer, PasswordRequestSerializer, PasswordResetSerializer, ResetVerifySerializer, PasswordChangeSerializer, LogoutSerializer
from django.db import IntegrityError
from utils.otp import hash_otp, store_otp, retrieve_otp, verify_otp, store_reset_token, retrieve_reset_token
from utils.email import send_email_verification_otp, send_password_reset_otp
import secrets
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework.permissions import IsAuthenticated


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

class PasswordResetView(generics.GenericAPIView):

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PasswordRequestSerializer
        return PasswordResetSerializer

    def post(self, request):
        serializer_class = PasswordRequestSerializer
        serializers = serializer_class(data=request.data)

        if not serializers.is_valid():
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "error" : serializers.errors
                },
                status=400
            )

        try:
            user = serializers.save()

            otp = f"{secrets.randbelow(1_000_000):06d}"
            store = store_otp(user_id=user.id, purpose="password", hash=hash_otp(otp=otp))
            send_password_reset_otp(user.email, otp, user.first_name)

            return Response(
                {
                    "success" : True,
                    "message" : "if an account with this email exists, a password reset otp has been sent to your mail",
                    "data" : {}
                },
                status=200
            )
        except User.DoesNotExist:
            Response(
                {
                    "success" : True,
                    "message" : "if an account with this email exists, a password reset otp has been sent to your mail",
                    "data" : {}
                },
                status=200
            )

    def patch(self, request):
        serializer_class = PasswordResetSerializer
        serializers = serializer_class(data=request.data)

        if not serializers.is_valid():
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : serializers.errors
                }
            )

        try:
            user = User.objects.get(email = serializers.validated_data.get("email"))

            token = retrieve_reset_token(userid=user.id, purpose="password")

            if not token:
                raise ValueError("invalid or expired token")
            
            verify = verify_otp(digested=token, digest=hash_otp(otp=serializers.validated_data.get("token")))

            if not verify:
                raise ValueError("invalid or expired token")

            try:
                user = serializers.save()
                return Response(
                    {
                        "success" : True,
                        "message" : "password reset successfully",
                        "data" : {}
                    },
                    status=200
                )
            
            except Exception as e:
                print(str(e))
                return Response(
                    {
                        "success" : False,
                        "message" : "internal server error",
                        "errors" : "server failed to reset password"
                    },
                    status=500
                )

        except Exception:
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : "invalid or expired token"
                },
                status=400
            )


class ResetVerifyView(generics.GenericAPIView):
    serializer_class = ResetVerifySerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)

        if not serializers.is_valid():
            return Response(
                {
                    "succcess" : False,
                    "message" : "bad request",
                    "errors" : serializers.errors
                },
                status=400
            )

        try:
            user = serializers.save()

            otp = serializers.validated_data.get("otp")
            user_id = user.id
            
            try:
                digested = retrieve_otp(user_id=user_id, purpose="password")
                if digested == None: raise ValueError("invalid")
                verify = verify_otp(digested=digested, digest=hash_otp(otp))
                if not verify: raise ValueError("invalid")
            except Exception as e:
                print(str(e))
                return Response({
                    "success" : False,
                    "message" : "bad request",
                    "error" : "invalid or expired otp"
                },
                status=400)
        except User.DoesNotExist:
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : "no otp records for this user"
                },
                status=400
            )

        try:
            token = secrets.token_urlsafe(32)

            store = store_reset_token(userid=user.id, purpose="password", token=hash_otp(otp=token))

            return Response(
                {
                    "success" : True,
                    "message" : "otp successfully verified",
                    "data" : {
                        "token" : token
                    }
                }
            )
        except Exception:
            return Response(
                {
                    "success" : False,
                    "message" : "internal server error",
                    "errors" : "server failed to verify otp"
                },
                status=500
            )

class PasswordChangeView(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data, context={"user" : request.user})

        if not serializer.is_valid():
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "error" : serializer.errors
                },
                status=400
            )

        try:
            user = serializer.save()
            return Response(
                {
                    "success" : True,
                    "message" : "password reset successfully",
                    "data" : {}
                }
            )
        except ValueError as e:
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : str(e)
                },
                status=400
            )
        except Exception as e:
            print(str(e))
            return Response(
                {
                    "success" : False,
                    "message" : "internal server error",
                    "errors" : "server failed to change password"
                },
                status=500
            )


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer
    def post(self, request):
        user = request.user

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : serializer.errors
                },
                status=400
            )

        token = RefreshToken(serializer.validated_data.get("refresh"))
        token.blacklist()

        return Response(
            {
                "success" : True,
                "message" : "user successfully logout",
                "data" : {}
            },
            status=200
        )