from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, UserViewSet

router = DefaultRouter()

router.register(r'student', StudentViewSet)
router.register(r'users', UserViewSet)
