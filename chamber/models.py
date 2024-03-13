from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Director(models.Model):
    name = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=255, null=True)
    pan = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f" {self.name} - {self.designation}"


class Form2(models.Model):

    iande = models.FileField(upload_to='incomeandexpenditure/', null=True, verbose_name="")
    incometaxtpan = models.FileField(upload_to='incometaxtpan/', null=True, verbose_name="")
    FactoryRegistrationCertificate = models.FileField(upload_to='FactoryRegistrationCertificate/', null=True,
                                                      verbose_name="")
    MemorandumArticleofAssociation = models.FileField(upload_to='MemorandumArticleofAssociation/', null=True,
                                                      verbose_name="")
    GSTINRegistrationCopy = models.FileField(upload_to='GSTINRegistrationCopy/', null=True, verbose_name="")
    IECodeCertificate = models.FileField(upload_to='IECodeCertificate/', null=True, verbose_name="")
    ProfessionalCertificate = models.FileField(upload_to='ProfessionalCertificate/', null=True, verbose_name="")
    CopyofLandDocument = models.FileField(upload_to='CopyofLandDocument/', null=True, verbose_name="")
    LandHolding = models.FileField(upload_to='LandHolding/', null=True, verbose_name="")
    passportsizephoto = models.FileField(upload_to='passportsizephoto/', null=True, verbose_name="")
    DirectorsPartners = models.FileField(upload_to='DirectorsPartners/', null=True, verbose_name="")

    def __str__(self) -> str:
        return f"{str(self.incometaxtpan)}"


class Form1(models.Model):
    Nameofapplicant = models.CharField(max_length=255, null=True)
    constitution_options = [
        ('Individual', 'Individual'),
        ('Proprietory Firm', 'Proprietory Firm'),
        ('Partnership Firm', 'Partnership Firm'),
        ('LLP', 'LLP'),
        ('Private Limited', 'Private Limited'),
        ('Public Limited Unlisted', 'Public Limited Unlisted'),
        ('Public Limited Listed', 'Public Limited Listed'),
        ('Trust', 'Trust'),
        ('Society', 'Society'),
        ('Associations', 'Associations'),
    ]
    constitution = models.CharField(
        max_length=30, 
        choices=constitution_options,
        blank=True,
        null=True,
    )
    individual_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Enter the name of the Individual',
    )
    is_individual = models.BooleanField(
        default=False,
        help_text='Check if the constitution is Individual',
    )
    Businessactivity = models.CharField(max_length=500, null=True)
    regoffadd = models.CharField(max_length=500, null=True)
    acoffice = models.CharField(max_length=500, null=True)
    acwork = models.CharField(max_length=500, null=True)
    cdlan = models.BigIntegerField(null=True)
    cdphone = models.BigIntegerField(null=True)
    cdemail = models.EmailField(max_length=254,unique=True)
    cdweb = models.URLField(max_length=200, blank=True, null=True)
    aadhar = models.BigIntegerField(null=True)
    pancardno = models.BigIntegerField(null=True)
    GSTNo = models.BigIntegerField(null=True)
    CompanyFirmRegNo = models.BigIntegerField(null=True)
    SocietyAssociationRegNo = models.BigIntegerField(null=True)

    paname = models.CharField(max_length=255, null=True)
    papan = models.CharField(max_length=10, null=True)
    paphone = models.CharField(max_length=15, null=True)
    padesignation = models.CharField(max_length=255, null=True)
    paaadhaar = models.CharField(max_length=12, null=True)
    pamail_id = models.EmailField(null=True)
    indmain_category = models.CharField(max_length=255, null=True)
    indsub_category = models.CharField(max_length=255, null=True)
    cmdomestic = models.CharField(max_length=255, null=True)
    cmboth = models.CharField(max_length=255, null=True)
    cmpercentage_of_imports = models.CharField(max_length=10, null=True)
    cmglobal_market = models.CharField(max_length=255, null=True)
    cmpercentage_of_exports = models.CharField(max_length=10, null=True)
    country_name_foreign_collaboration = models.CharField(max_length=255, null=True)
    collaborator_name_foreign_collaboration = models.CharField(max_length=255, null=True)
    annual_turnover_year1 = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    annual_turnover_year2 = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    annual_turnover_year3 = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    classindustry = models.CharField(max_length=255, choices=[
        ('Large', 'Large'),
        ('Medium', 'Medium'),
        ('Small', 'Small'),
        ('Micro', 'Micro'),
    ], null=True)
    direct_office_employees = models.BigIntegerField(null=True)
    indirect_contractual_employees = models.BigIntegerField(null=True)
    works_employees = models.BigIntegerField(null=True)
    outsourced_employees = models.BigIntegerField(null=True)
    esic = models.CharField(max_length=255, null=True)
    epf = models.CharField(max_length=255, null=True)
    branches_outside_india = models.CharField(max_length=500, null=True)
    is_member_of_association = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")], default="No",
                                                verbose_name="Are you a member of any other Association", null=True)
    association_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Association Name")
    is_office_bearer = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")], default="No",
                                        verbose_name="Do you hold any Office Bearers position in any Association", null=True)
    association_position = models.CharField(max_length=255, blank=True, null=True, verbose_name="Association Position")
    directors = models.ManyToManyField(Director, related_name='form1s', blank=True)
    reason_for_joining_chamber = models.TextField(null=True)

    e_sign = models.FileField(upload_to='e_sign/', null=True, verbose_name="")
    seal_image = models.FileField(upload_to='seal_image/', null=True, verbose_name="")
    Form2 = models.ManyToManyField(Form2, related_name='form2', blank=True)

    def __str__(self):
        return f"{self.Nameofapplicant}: {str(self.e_sign)}"





'''
{
    "directors": [],
    "Nameofapplicant": "eeeeeeeeeeeeeeeeee",
    "constitution": null,
    "individual_name": "",
    "is_individual": false,
    "Businessactivity": "eeeeeeeeeeeeeeeeeeeee",
    "regoffadd": "eeeeeeeeeeeeeeeee",
    "acoffice": "eeeeeeeeeeee",
    "acwork": "eeeeeeeeeeeeeeeee",
    "cdlan": "1147483647",
    "cdphone": "1147483647",
    "cdemail": "lokesh07084@gmail.com",
    "cdweb": "https://lokeshdev.co/",
    "aadhar": "1147483647",
    "pancardno": "1147483647",
    "GSTNo": "1147483647",
    "CompanyFirmRegNo": "1147483647",
    "SocietyAssociationRegNo": "1147483647",
    "paname": "EEEEEEEEEEEEE",
    "papan": "114748364",
    "paphone": "114748364",
    "padesignation": "EEEEEEEEEEEE",
    "paaadhaar": "1147483647",
    "pamail_id": "lokesh07084@gmail.com",
    "indmain_category": "EEEEEEEEEE",
    "indsub_category": "EEEEEEEEEEEE",
    "cmdomestic": "EEEEEEEEEEEE",
    "cmboth": "EEEE",
    "cmpercentage_of_imports": "EEEEEE",
    "cmglobal_market": "EEEEE",
    "cmpercentage_of_exports": "EEEEEEEEE",
    "country_name_foreign_collaboration": "EEEEEEEE",
    "collaborator_name_foreign_collaboration": "EEEEEEEEEEEEEE",
    "annual_turnover_year1": "3",
    "annual_turnover_year2": "3",
    "annual_turnover_year3": "3",
    "classindustry": "Small",
    "direct_office_employees": "3",
    "indirect_contractual_employees": "3",
    "works_employees": "3",
    "outsourced_employees": "3",
    "esic": "EEEEE",
    "epf": "EEEEEEEE",
    "branches_outside_india": "EEEEEEE",
    "is_member_of_association": "Yes",
    "association_name": "eee",
    "is_office_bearer": "Yes",
    "association_position": "eee",
    "reason_for_joining_chamber": "EEE",
    "e_sign": null,
    "seal_image": null
}


'''


