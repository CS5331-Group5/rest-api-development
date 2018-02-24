from rest_framework import permissions, viewsets

from .models import Diary
from .serializers import DiarySerializer

class DairyViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
