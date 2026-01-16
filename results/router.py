from rest_framework.routers import DefaultRouter  # type: ignore
from .views import StudentViewSet, UserViewSet, AssessmentViewSet, SubjectViewSet, AcademicSessionViewSet, ClassRoomViewSet, TermReportViewSet

router = DefaultRouter()

router.register(r'student', StudentViewSet)
router.register(r'users', UserViewSet)
router.register(r'classroom', ClassRoomViewSet)
router.register(r'subject', SubjectViewSet)
router.register(r'session', AcademicSessionViewSet)
router.register(r'assessment', AssessmentViewSet)
router.register(r'report', TermReportViewSet)

