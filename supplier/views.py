from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import SupplierSerializer
from django.db import IntegrityError
from .models import Supplier
from .permissions import IsActiveEmployee

class SupplierView(GenericAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsActiveEmployee]
    def get(self, request):
        try:
            business = request.user.employee_records.get(is_active=True).business
        except Exception:
            return Response(
                {
                    "success" : False,
                    "message" : "unauthorized",
                    "errors" : "you are unauthorized to perform this action"
                },
                status=401
            )
        try:
            query = Supplier.objects.filter(business=business).order_by("created_at")
            page = self.paginate_queryset(query)

            serializer = self.serializer_class(page, many=True)

            return self.get_paginated_response(serializer.data)
        except Exception as e:
            print(str(e))
            return Response(
                {
                    "success" : False,
                    "message" : "internal server error",
                    "errors" : str(e)
                }
            )

    def post(self, request):
        business = request.user.employee_records.filter(is_active=True).first()

        if not business:
            return Response(
                {
                    "success" : True,
                    "message" : "unauthorized",
                    "errors" : "user is unauthorized to perform this action"
                },
                status=401
            )

        serializer = self.serializer_class(data=request.data, context={"business" : business.business})

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

class SingleSupplierView(GenericAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsActiveEmployee]

    def get(self, request, supplier_id):

        employee = request.user.employee_records.filter(is_active=True)
        try:
            supplier = Supplier.objects.get(id=supplier_id, business=employee.business)
            return Response(
                {
                    "success" : True,
                    "message" : "supplier's detail fetched successfully",
                    "data" : self.serializer_class(supplier).data
                },
                status=200
            )
        except Supplier.DoesNotExist:
            return Response(
                {
                    "success" : False,
                    "message" : "supplier not found",
                    "errors" : "there's no found supplier"
                },
                status=404
            )
        except Exception as e:
            print(str(e))
            return Response(
                {
                    "success" : False,
                    "message" : "internal server error",
                    "errors" : "server failed to fetch user data"
                },
                status=500
            )
        

    def patch(self, request, supplier_id):
        employee = request.user.employee_records.filter(is_active=True)

        try:
            supplier = Supplier.objects.filter(id=supplier_id, business=employee.business)

            seriaizer = self.serializer_class(supplier, partial=True, data=request.data)

            supplier_data = seriaizer.save()

            return Response(
                {
                    "success" : True,
                    "message" : "supplier's data updated successfully",
                    "data" : self.serializer_class(supplier_data).data
                },
                status=200
            )
        except Supplier.DoesNotExist:
            return Response(
                {
                    "success" : False,
                    "message" : "supplier not found",
                    "errors" : "supplier was not found"
                },
                status=404
            )
        except Exception as e:
            print(str(e))
            return Response(
                {
                    "success" : False,
                    "message" : "internal server error",
                    "errors" : "server failed to update supplier's data"
                }
            )
