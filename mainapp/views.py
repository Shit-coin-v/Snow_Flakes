from rest_framework.viewsets import ModelViewSet
from mainapp.models import Project, Application
from mainapp.serializer import ProjectSerializer


class ProjectView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ApplicationtView(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ProjectSerializer