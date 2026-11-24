from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import BranchSerializer
from .permissions import IsOwner
from .models import Branch
from django.db import IntegrityError


class BranchView(GenericAPIView):
    permission_classes = [IsOwner]
    serializer_class = BranchSerializer
    def get(self, request):
        branch  = Branch.objects.filter(business=request.user.business)

        return Response(
            {
                "success" : True,
                "message" : "branches retrieved successfully",
                "data" : self.serializer_class(branch, many=True).data
            },
            status=200
        )

    def post(self, request):
        business = request.user.employee_records.filter(is_active=True).first().business

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
            branch = serializer.save()

            return Response(
                {
                    "success" : True,
                    "message" : "branch was created successfully",
                    "data" : self.serializer_class(branch).data
                },
                status=200
            )

        except IntegrityError:
            return Response(
                {
                    "success" : False,
                    "message" : "bad request",
                    "errors" : "a branch with this name already exists"
                },
                status=400
            )
        except Exception as e:
            print(str(e))
            return Response(
                {
                    "success" : False,
                    "message" : "internal server error",
                    "errors" : "server failed to create branch"
                },
                status=500
            )


class SingleBranchSerializer(GenericAPIView):
    serializer_class = BranchSerializer

    def get(self, request):
        try:
            branches = request.user.employee_records.filter(is_active=True)

            if len(branches) < 0:
                raise ValueError("user has no active employee record")
            
            branch_id = branches[0].id
            branch = Branch.objects.get(id=branch_id)

            return Response(
                {
                    "success" : True,
                    "message" : "branch data fetched successfully",
                    "data" : self.serializer_class(branch).data
                },
                status=200
            )
        except (Branch.DoesNotExist, ValueError):
            return Response(
                {
                    "success" : True,
                    "message" : "branch data fetched successfully",
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
                    "errors" : "server failed to fetch branches"
                }
            )


    def post(self, request):
        pass

    def patch(self, request):
        pass