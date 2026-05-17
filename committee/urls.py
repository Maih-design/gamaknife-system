from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path("patients/create/", views.create_patient, name="create_patient"),
    path("patients/", views.patients_list, name="patients_list"),
    path("patients/<int:pk>/", views.patient_profile, name="patient_profile"),
    path("sessions/session/create/", views.create_committee_session, name="create_committee_session"),
    path("sessions/session/<int:session_id>/add-case/", views.add_case_to_session, name="add_case_to_session"),
    path("cases/pending/", views.pending_cases, name="pending_cases"),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)