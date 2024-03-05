from rest_framework import generics
from .models import Form1, Director
from .serializers import Form1Serializer, DirectorSerializer
from rest_framework.response import Response

class Form1ListCreateView(generics.ListCreateAPIView):
    queryset = Form1.objects.all()
    serializer_class = Form1Serializer

    def perform_create(self, serializer):
        directors_data = self.request.data.pop('directors', None)
        form1_instance = serializer.save()

        if directors_data:
            director_serializer = DirectorSerializer(data=directors_data, many=True)
            director_serializer.is_valid(raise_exception=True)
            directors = director_serializer.save()
            form1_instance.directors.set(directors)
            return Response("Success")
        
