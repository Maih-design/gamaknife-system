from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientForm, PatientUpdateForm, PatientDocumentForm, CommitteeSessionForm
from .models import Patient, CommitteeCase, CommitteeSession
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from django.shortcuts import render


def home(request):
    return render(request, "home.html")


#@login_required
def dashboard(request):
    return render(request, "dashboard.html")

#@login_required
def create_patient(request):

    if request.method == "POST":

        form = PatientForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "تم إضافة المريض بنجاح"
            )

            return redirect("patients_list")

        else:
            print(form.errors)

    else:
        form = PatientForm()

    return render(request,
                  "patients/create_patient.html",
                  {"form": form})
    
def patients_list(request):

    patients = Patient.objects.all().order_by('-id')

    search_query = request.GET.get("search", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    # 🔎 Search by name or national ID
    if search_query:
        patients = patients.filter(
            Q(full_name__icontains=search_query) |
            Q(national_id__icontains=search_query)
        )

    # 📅 Filter by date range (assuming created_at exists)
    if start_date and end_date:
        patients = patients.filter(created_at__range=[start_date, end_date])

    return render(request, "patients/patients_list.html", {
        "patients": patients,
        "search_query": search_query,
        "start_date": start_date,
        "end_date": end_date,
    })


def patient_profile(request, pk):

    patient = get_object_or_404(Patient, pk=pk)

    # 🟢 ALWAYS bound form هنا
    patient_form = PatientUpdateForm(instance=patient)
    document_form = PatientDocumentForm()

    if request.method == "POST":

        if "update_patient" in request.POST:

            form = PatientUpdateForm(
                request.POST,
                instance=patient
            )

            if form.is_valid():
                form.save()
                return redirect("patient_profile", pk=pk)

        elif "upload_document" in request.POST:

            doc_form = PatientDocumentForm(
                request.POST,
                request.FILES
            )

            if doc_form.is_valid():
                doc = doc_form.save(commit=False)
                doc.patient = patient
                doc.save()
                return redirect("patient_profile", pk=pk)

    return render(request, "patients/patient_profile.html", {
        "patient": patient,
        "patient_form": patient_form,
        "document_form": document_form,
    })
    

def create_committee_session(request):

    if request.method == "POST":

        form = CommitteeSessionForm(request.POST)

        if form.is_valid():

            session = form.save()

            return redirect(
                "add_case_to_session",
                session_id=session.id
            )

    else:

        form = CommitteeSessionForm()

    return render(
        request,
        "sessions/create_session.html",
        {
            "form": form
        }
    )
    


def add_case_to_session(request, session_id):

    session = get_object_or_404(
        CommitteeSession,
        id=session_id
    )

    patient = None

    query = request.GET.get("q")

    if query:

        patient = Patient.objects.filter(
            national_id=query
        ).first()

    if request.method == "POST":

        patient_id = request.POST.get("patient_id")

        patient = get_object_or_404(
            Patient,
            id=patient_id
        )

        CommitteeCase.objects.create(
            patient=patient,
            committee_session=session
        )

        return redirect(
            "add_case_to_session",
            session_id=session.id
        )

    return render(
        request,
        "sessions/add_case.html",
        {
            "session": session,
            "patient": patient,
        }
    )
    


def pending_cases(request):

    cases = CommitteeCase.objects.filter(
        status="pending"
    ).select_related(
        "patient",
        "committee_session"
    )

    return render(
        request,
        "cases/pending_cases.html",
        {
            "cases": cases
        }
    )