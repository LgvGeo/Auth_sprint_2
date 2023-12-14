from rest_framework import routers

from api import views

router = routers.SimpleRouter()
router.register('movies', views.MovieReadOnlyModelViewSet)
urlpatterns = router.urls
