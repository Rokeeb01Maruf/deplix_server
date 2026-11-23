from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CreateBusinessSerializer
from rest_framework.generics import GenericAPIView
from .models import Business

class BusinessView(GenericAPIView):
    serializer_class = CreateBusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Business.objects.prefetch_related("branch").all()

    def get(self, request):
        business_data = self.get_queryset()

        serializer = self.get_serializer(business_data, many=True)

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
        except InterruptedError:
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : "user can only manage one business on deplix"
                },
                status=400
            )
        except Exception as e:
            print(str(e))
            return Response(
                {
                    "success" : False,
                    "message" : "internal server error",
                    "errors" : "server failed to create business"
                },
                status=500
            )