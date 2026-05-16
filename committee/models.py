from django.db import models


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

class CommitteeCase(BaseModel):

    class Status(models.TextChoices):
        PENDING = "pending", "قيد المراجعة"
        APPROVED = "approved", "مقبول"
        REJECTED = "rejected", "مرفوض"
        FOLLOW_UP = "follow_up", "متابعة"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="cases",
        verbose_name="المريض"
    )

    committee_date = models.DateField(
        verbose_name="تاريخ اللجنة"
    )

    diagnosis_details = models.TextField(
        verbose_name="تفاصيل التشخيص"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="الحالة"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    def __str__(self):
        return f"{self.patient.full_name} - {self.committee_date}"

    class Meta:
        verbose_name = "حالة لجنة"
        verbose_name_plural = "حالات اللجنة"
        ordering = ["-committee_date"]


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

    case = models.ForeignKey(
        CommitteeCase,
        on_delete=models.CASCADE,
        related_name="recommendations",
        verbose_name="الحالة"
    )

    procedure = models.ForeignKey(
        Procedure,
        on_delete=models.PROTECT,
        related_name="recommendations",
        verbose_name="الإجراء"
    )

    sessions_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="عدد الجلسات"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    def __str__(self):
        return f"{self.case.patient.full_name} - {self.procedure.name}"

    class Meta:
        verbose_name = "توصية لجنة"
        verbose_name_plural = "توصيات اللجنة"


# =========================================================
# Referrals
# =========================================================

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

    referred_to = models.CharField(
        max_length=255,
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