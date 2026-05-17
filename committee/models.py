from django.db import models
from django.conf import settings


# =========================================================
# Base Model
# =========================================================

class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاريخ التعديل"
    )

    class Meta:
        abstract = True


# =========================================================
# Patient Model
# =========================================================

class Patient(BaseModel):

    class Gender(models.TextChoices):
        MALE = "male", "ذكر"
        FEMALE = "female", "أنثى"

    national_id = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="الرقم القومي"
    )

    full_name = models.CharField(
        max_length=255,
        verbose_name="اسم المريض"
    )

    birth_date = models.DateField(
        verbose_name="تاريخ الميلاد"
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        verbose_name="النوع"
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="رقم الهاتف"
    )

    governorate = models.CharField(
        max_length=100,
        verbose_name="محافظة السكن"
    )

    affiliated_branch = models.CharField(
        max_length=255,
        verbose_name="الفرع التابع له"
    )

    diagnosis = models.TextField(
        verbose_name="التشخيص"
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "مريض"
        verbose_name_plural = "المرضى"
        ordering = ["full_name"]
        
        
class Doctor(BaseModel):

    full_name = models.CharField(
        max_length=255,
        verbose_name="اسم الطبيب"
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "طبيب"
        verbose_name_plural = "الأطباء"


# =========================================================
# Patient Documents
# =========================================================

class PatientDocument(BaseModel):

    class DocumentType(models.TextChoices):
        NATIONAL_ID = "national_id", "البطاقة الشخصية"
        BIRTH_CERTIFICATE = "birth_certificate", "شهادة الميلاد"
        INSURANCE_CARD = "insurance_card", "البطاقة الصحية / الكارنيه"
        OTHER = "other", "أخرى"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="المريض"
    )

    document_type = models.CharField(
        max_length=50,
        choices=DocumentType.choices,
        verbose_name="نوع المستند"
    )

    file = models.FileField(
        upload_to="patient_documents/",
        verbose_name="الملف"
    )

    def __str__(self):
        return f"{self.patient.full_name} - {self.get_document_type_display()}"

    class Meta:
        verbose_name = "مستند مريض"
        verbose_name_plural = "مستندات المرضى"


# =========================================================
# Committee Case
# =========================================================

class CommitteeSession(BaseModel):

    class Status(models.TextChoices):

        OPEN = "open", "مفتوحة"
        CLOSED = "closed", "مغلقة"

    session_date = models.DateField(
        verbose_name="تاريخ الجلسة"
    )

    doctors = models.ManyToManyField(
        Doctor,
        related_name="committee_sessions",
        verbose_name="الأطباء"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name="حالة الجلسة"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    def __str__(self):
        return f"لجنة {self.session_date}"

    class Meta:
        verbose_name = "جلسة لجنة"
        verbose_name_plural = "جلسات اللجنة"
        ordering = ["-session_date"]
        

class CommitteeCase(BaseModel):

    class Status(models.TextChoices):

        PENDING = "pending", "في انتظار العرض"
        REVIEWED = "reviewed", "تم العرض"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="committee_cases",
        verbose_name="المريض"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="الحالة"
    )

    committee_date = models.DateField(
        verbose_name="تاريخ اللجنة"
    )
    
    committee_session = models.ForeignKey(
    CommitteeSession,
    on_delete=models.CASCADE,
    related_name="cases"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.patient.full_name} - {self.get_status_display()}"

    class Meta:
        verbose_name = "عرض لجنة"
        verbose_name_plural = "عروض اللجنة"
        ordering = ["-created_at"]


# =========================================================
# Procedures
# =========================================================

class Procedure(BaseModel):

    class Category(models.TextChoices):
        THERAPEUTIC = "therapeutic", "إجراء علاجي"
        RADIOLOGY = "radiology", "فحوصات أشعة"
        LABORATORY = "laboratory", "تحاليل طبية"

    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        verbose_name="التصنيف"
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="اسم الإجراء"
    )
    
    requires_referral = models.BooleanField(
        default=False,
        verbose_name="يتطلب تحويل؟"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "إجراء"
        verbose_name_plural = "الإجراءات"
        ordering = ["category", "name"]


# =========================================================
# Committee Recommendations
# =========================================================

class CommitteeRecommendation(BaseModel):

    committee_case = models.OneToOneField(
        CommitteeCase,
        on_delete=models.CASCADE,
        related_name="recommendation"
    )

    procedure = models.ForeignKey(
        Procedure,
        on_delete=models.CASCADE
    )

    recommendation_text = models.TextField(
        verbose_name="قرار اللجنة",
  
    )

    notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.committee_case.patient.full_name


# =========================================================
# Referrals
# =========================================================

class ReferralCenter(models.Model):

    name = models.CharField(max_length=255, verbose_name="اسم الجهة")
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Referral(BaseModel):

    class Status(models.TextChoices):
        ACTIVE = "active", "نشط"
        CANCELLED = "cancelled", "ملغي"

    recommendation = models.ForeignKey(
        CommitteeRecommendation,
        on_delete=models.PROTECT,
        related_name="referrals",
        verbose_name="التوصية"
    )

    referral_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="رقم التحويل"
    )

    organization = models.ForeignKey(
    ReferralCenter,
    on_delete=models.PROTECT,
    verbose_name="الجهة المحول إليها"
)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="الحالة"
    )

    cancellation_reason = models.TextField(
        blank=True,
        verbose_name="سبب الإلغاء"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    def __str__(self):
        return self.referral_number

    class Meta:
        verbose_name = "تحويل"
        verbose_name_plural = "التحويلات"
        ordering = ["-created_at"]
        


