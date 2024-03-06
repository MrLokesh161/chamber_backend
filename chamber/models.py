from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Director(models.Model):
    name = models.CharField(max_length=255,null=True)
    designation = models.CharField(max_length=255,null=True)
    pan = models.CharField(max_length=10,null=True)

    def __str__(self):
        return f" {self.name} - {self.designation}"

class Form1(models.Model):
    Nameofapplicant = models.CharField(max_length=255)
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
        max_length=30,  # Increase max_length to accommodate the longest choice
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
    Businessactivity = models.CharField(max_length=500)
    regoffadd = models.CharField(max_length=500)
    acoffice = models.CharField(max_length=500)
    acwork = models.CharField(max_length=500)
    cdlan = models.IntegerField() 
    cdphone = models.IntegerField()
    cdemail = models.EmailField(max_length=254,blank=True) 
    cdweb = models.URLField(max_length=200, blank=True, null=True,)
    aadhar = models.IntegerField()
    pancardno = models.IntegerField()
    GSTNo = models.IntegerField()
    CompanyFirmRegNo = models.IntegerField()
    SocietyAssociationRegNo = models.IntegerField()


    paname = models.CharField(max_length=255)
    papan = models.CharField(max_length=10)
    paphone = models.CharField(max_length=15)
    padesignation = models.CharField(max_length=255)
    paaadhaar = models.CharField(max_length=12)
    pamail_id = models.EmailField()
    indmain_category = models.CharField(max_length=255)
    indsub_category = models.CharField(max_length=255)
    cmdomestic = models.CharField(max_length=255)
    cmboth = models.CharField(max_length=255)
    cmpercentage_of_imports = models.CharField(max_length=10)
    cmglobal_market = models.CharField(max_length=255)
    cmpercentage_of_exports = models.CharField(max_length=10)
    country_name_foreign_collaboration = models.CharField(max_length=255)
    collaborator_name_foreign_collaboration = models.CharField(max_length=255)
    annual_turnover_year1 = models.DecimalField(max_digits=15, decimal_places=2)
    annual_turnover_year2 = models.DecimalField(max_digits=15, decimal_places=2)
    annual_turnover_year3 = models.DecimalField(max_digits=15, decimal_places=2)
    classindustry = models.CharField(max_length=255, choices=[
        ('Large', 'Large'),
        ('Medium', 'Medium'),
        ('Small', 'Small'),
        ('Micro', 'Micro'),
    ])
    direct_office_employees = models.IntegerField()
    indirect_contractual_employees = models.IntegerField()
    works_employees = models.IntegerField()
    outsourced_employees = models.IntegerField()
    esic = models.CharField(max_length=255)
    epf = models.CharField(max_length=255)
    branches_outside_india = models.CharField(max_length=500)
    is_member_of_association = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")], default="No", verbose_name="Are you a member of any other Association")
    association_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Association Name")
    is_office_bearer = models.CharField(max_length=3, choices=[("Yes", "Yes"), ("No", "No")], default="No", verbose_name="Do you hold any Office Bearers position in any Association")
    association_position = models.CharField(max_length=255, blank=True, null=True, verbose_name="Association Position")
    directors = models.ManyToManyField(Director, related_name='form1s', blank=True,)
    reason_for_joining_chamber = models.TextField()
    
    e_sign = models.ImageField(upload_to='e_signs/', null=True, blank=True)
    seal_image = models.ImageField(upload_to='seals/', null=True, blank=True)


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


