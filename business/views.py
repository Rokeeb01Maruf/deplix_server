from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import BusinessSerializer
from rest_framework.generics import GenericAPIView
from .models import Business
from django.db import IntegrityError

class BusinessView(GenericAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_business(self, user):
        return Business.objects.get(owner=user)

    def get(self, request):
        try:
            business_data = self.get_business(request.user)

        except Business.DoesNotExist:
            return Response(
                {
                    "success" : True,
                    "message" : "business data not found",
                    "data" : {}
                },
                status=404
            )

        serializer = self.serializer_class(business_data)

        return Response(
            {
                "success" : True,
                "message" : "business data retrieved successfully",
                "data" : serializer.data
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"user" : request.user})

        if not serializer.is_valid():
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : serializer.errors
                },
                status=400
            )

        try:
            business = serializer.save()

            return Response(
                {
                    "success" : False,
                    "message" : "business created successfully",
                    "data" : {}
                },
                status=201
            )
        except IntegrityError:
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : "user can only manage one business on deplix"
                },
                status=400
            )
        except Exception as e:
            print(type(e).__name__)
            return Response(
                {
                    "success" : False,
                    "message" : "internal server error",
                    "errors" : "server failed to create business"
                },
                status=500
            )

    def patch(self, request):
        business_data = self.get_business(request.user)
        serializer = self.serializer_class(business_data ,data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : serializer.errors
                },
                status=400
            )

        try:
            business = serializer.save()

            return Response(
                {
                    "success" : True,
                    "message" : "business data updated successfully",
                    "data" : self.serializer_class(business).data
                }
            )
        except Exception as e:
            print(str(e))
            return Response(
                {
                    "success" : False,
                    "message" : "internal server error",
                    "errors" : "server failed to update business data"
                },
                status=500
            )

