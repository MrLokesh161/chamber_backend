from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .models import Form1, Director
from .serializers import Form1Serializer, DirectorSerializer

@api_view(['POST'])
def create_form1(request):
    if request.method == 'POST':
        serializer = Form1Serializer(data=request.data)
        print(request.data)

        if serializer.is_valid():
            directors_data = request.data.pop('directors', None)
            form1_instance = serializer.save()

            if directors_data:
                director_serializer = DirectorSerializer(data=directors_data, many=True)
                director_serializer.is_valid(raise_exception=True)
                directors = director_serializer.save()

                form1_instance.directors.set(directors)

            return Response({"detail": "Success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
