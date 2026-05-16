from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("patients/create/", views.create_patient, name="create_patient"),
    path("patients/", views.patients_list, name="patients_list"),
    path("patients/<int:pk>/", views.patient_profile, name="patient_profile"),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)