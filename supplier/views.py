from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import SupplierSerializer
from django.db import IntegrityError

class SupplierView(GenericAPIView):
    serializer_class = SupplierSerializer

    def get(self, request):
        pass

    def post(self, request):
        business = request.user.employee_records.filter(is_active=True).first()

        if not business:
            return Response(
                {
                    "success" : True,
                    "message" : "unauthorized",
                    "errors" : "no current business to perform this action on"
                },
                status=401
            )

        serializer = self.serializer_class(data=request.data, context={"business" : business})

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
            supplier = serializer.save()

            return Response(
                {
                    "success" : True,
                    "message" : "supplier created successfully",
                    "data" : self.serializer_class(supplier).data
                },
                status=200
            )

        except IntegrityError:
            return Response(
                {
                    "success" : False,
                    "message" : "supplier already exist",
                    "errors" : serializer.errors
                },
                status=400
            )
        except Exception as e:
            print(str(e))
            return Response(
                {
                    "success" : False,
                    "message" : "internal server error",
                    "errors" : serializer.errors
                },
                status=500
            )


    def patch(self, request):
        pass
