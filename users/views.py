from rest_framework import generics, permissions
from rest_framework.response import Response

class GetMeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user

        return Response(
            {
                "success" : True,
                "message" : "user data retrieved successsfully",
                "data" : {
                    "id" : user.id,
                    "first_name" : user.first_name,
                    "last_name" : user.last_name,
                    "email" : user.email,
                    "phone" : user.phone
                }
            },
            status=200
        )
