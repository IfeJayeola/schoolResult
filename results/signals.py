from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Assessment, TermReport, AcademicSession
from django.utils import timezone


@receiver(post_save, sender = Assessment)
def update_term_report_after_assessment_save(sender, instance, created, **kwargs):
    print('jjtj')
    try:
        report, report_created = TermReport.objects.get_or_create(
            student = instance.student,
            term = instance.term,
            session = instance.session,
            defaults={
                'classroom': instance.student.current_class
            }
        )

        report.calculate_summary()
        report.calculate_position()
    except Exception as e:
        print(f"Error updatin report due to {e}")        

