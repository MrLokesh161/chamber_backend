from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User 
from django.utils import timezone



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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Nameofapplicant = models.CharField(max_length=255, null=True, default=None)
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
    Businessactivity = models.CharField(max_length=500, null=True, default=None)
    regoffadd = models.CharField(max_length=500, null=True, default=None)
    acoffice = models.CharField(max_length=500, null=True, default=None)
    acwork = models.CharField(max_length=500, null=True, default=None)
    cdlan = models.CharField(max_length=20, null=True, default=None)
    cdphone = models.CharField(max_length=20, null=True, default=None)
    cdemail = models.EmailField(max_length=254, null=True, default=None)
    cdweb = models.URLField(max_length=200, blank=True, null=True, default=None)
    aadhar = models.CharField(max_length=12, null=True, default=None)
    pancardno = models.CharField(max_length=12, null=True)
    GSTNo = models.BigIntegerField(null=True, default=None)
    CompanyFirmRegNo = models.BigIntegerField(null=True, default=None)
    SocietyAssociationRegNo = models.BigIntegerField(null=True, default=None)

    paname = models.CharField(max_length=255, null=True, default=None)
    papan = models.CharField(max_length=10, null=True, default=None)
    paphone = models.CharField(max_length=15, null=True, default=None)
    padesignation = models.CharField(max_length=255, null=True, default=None)
    paaadhaar = models.CharField(max_length=12, null=True, default=None)
    pamail_id = models.EmailField(null=True, default=None)
    indmain_category = models.CharField(max_length=255, null=True, default=None)
    indsub_category = models.CharField(max_length=255, null=True, default=None)
    cmdomestic = models.CharField(max_length=255, null=True, default=None)
    cmboth = models.CharField(max_length=255, null=True, default=None)
    cmpercentage_of_imports = models.CharField(max_length=10, null=True, default=None)
    cmglobal_market = models.CharField(max_length=255, null=True, default=None)
    cmpercentage_of_exports = models.CharField(max_length=10, null=True, default=None)
    country_name_foreign_collaboration = models.CharField(max_length=255, null=True, default=None)
    collaborator_name_foreign_collaboration = models.CharField(max_length=255, null=True, default=None)
    annual_turnover_year1 = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=None)
    annual_turnover_year2 = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=None)
    annual_turnover_year3 = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=None)
    classindustry = models.CharField(max_length=255, choices=[
        ('Large', 'Large'),
        ('Medium', 'Medium'),
        ('Small', 'Small'),
        ('Micro', 'Micro'),
    ], null=True, default=None)
    direct_office_employees = models.BigIntegerField(null=True, default=None)
    indirect_contractual_employees = models.BigIntegerField(null=True, default=None)
    works_employees = models.BigIntegerField(null=True, default=None)
    outsourced_employees = models.BigIntegerField(null=True, default=None)
    esic = models.CharField(max_length=255, null=True, default=None)
    epf = models.CharField(max_length=255, null=True, default=None)
    branches_outside_india = models.CharField(max_length=500, null=True)
    is_member_of_association = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")], default="No",
                                                verbose_name="Are you a member of any other Association", null=True)
    association_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Association Name")
    is_office_bearer = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")], default="No",
                                        verbose_name="Do you hold any Office Bearers position in any Association", null=True)
    association_position = models.CharField(max_length=255, blank=True, null=True, verbose_name="Association Position", default=None)
    directors = models.ManyToManyField(Director, related_name='form1s', blank=True)
    reason_for_joining_chamber = models.TextField(null=True, default=None)

    e_sign = models.FileField(upload_to='e_sign/', null=True, verbose_name="")
    seal_image = models.FileField(upload_to='seal_image/', null=True, verbose_name="")
    form_status_options = (
        ("pending","pending"), 
        ("Approved by AO","Approved by AO"), 
        ("Approved by CEO","Approved by CEO"), 
        ("Approved by Membership Committee","Approved by Membership Committee"), 
        ("Approved by OB","Approved by OB"), 
        ("Approved as a Member","Approved as a Member"), 
        ("waiting for payment","waiting for payment"),
        ('payment done (approved as Member)','payment done (approved as Member)'), 
        ("rejected","rejected"),
    )
    ror = models.TextField(help_text="Reason of Rejection",null=True,blank=True, default=None)
    form_status = models.CharField( choices=form_status_options ,max_length=50, default="pending")
    Form2 = models.ManyToManyField(Form2, related_name='form2', blank=True)

    def __str__(self):
        return f"{self.Nameofapplicant}: {str(self.e_sign)}"

class PaymentTransaction(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership_type_choices = [
        ('general', 'General'),
        ('professional', 'Professional'),
        ('associations', 'Associations'),
        ('life', 'Life Membership'),
    ]

    sales_turnover_choices = [
        ('upTo5Crore', 'Up to Rs. 5 Crore'),
        ('above5CroreUpTo10Crore', 'Above Rs. 5 Crore up to Rs. 10 Crore'),
        ('above10CroreUpTo25Crore', 'Above Rs. 10 Crore up to Rs. 25 Crore'),
        ('above25Crore', 'Above Rs. 25 Crore'),
    ]

    membership_type = models.CharField(max_length=20, choices=membership_type_choices)
    sales_turnover = models.CharField(max_length=50, choices=sales_turnover_choices, blank=True, null=True)
    card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=100)
    cvv = models.CharField(max_length=40)
    cardholder_name = models.CharField(max_length=255)

    entrance_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selected_membership_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    registration_date = models.DateTimeField(default=timezone.now)
    membership_expiry_date = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.user.username

class MembershipPrices:
    upTo5Crore = 2950
    above5CroreUpTo10Crore = 4130
    above10CroreUpTo25Crore = 5000
    above25Crore = 8250

    professional = 2950
    associations = 2360
    lifeMembership = 88500
    admissionFee = 3540
    journalSubscription = 295
    chamberDayCelebrations = 1180

class Events(models.Model):
    Eventimage = models.FileField(upload_to='eventsimage/', null=True, verbose_name="")
    NameofEvent = models.CharField(max_length=255)
    Description = models.CharField(max_length=1000)
    DateofEvent = models.DateField(null=True)
    LinkforEvent = models.URLField(max_length=200, null=True)

class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    Email = models.EmailField()
    phonenumber = models.BigIntegerField()
    Description = models.CharField(max_length=1000)
    
class Certificate(models.Model):
    Name = models.CharField(max_length=255)
    issue_date = models.DateTimeField(default=timezone.now)


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
