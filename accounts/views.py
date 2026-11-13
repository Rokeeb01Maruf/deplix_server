from rest_framework import generics
from rest_framework.response import Response


class HomeView(generics.GenericAPIView):
    def get(self, request):
        return Response({"message": "Welcome to the Home Page!"})
