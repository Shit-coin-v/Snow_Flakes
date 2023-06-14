from rest_framework.routers import DefaultRouter as DR
from mainapp.views import ProjectView, ApplicationtView


router = DR()

router.register('project', ProjectView)
router.register('applicationt', ApplicationtView)

urlpatterns = []

urlpatterns += router.urls