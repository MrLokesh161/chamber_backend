from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Form1, Director, Form2


class Form1Admin(admin.ModelAdmin):
    list_display = (
        'Nameofapplicant',
        'constitution',
        'individual_name',
        'is_individual',
        'Businessactivity',
        'regoffadd',
        'acoffice',
        'acwork',
        'cdlan',
        'cdphone',
        'cdemail',
        'cdweb',
        'aadhar',
        'pancardno',
        'GSTNo',
        'CompanyFirmRegNo',
        'SocietyAssociationRegNo',
        'paname',
        'papan',
        'paphone',
        'padesignation',
        'paaadhaar',
        'pamail_id',
        'indmain_category',
        'indsub_category',
        'cmdomestic',
        'cmboth',
        'cmpercentage_of_imports',
        'cmglobal_market',
        'cmpercentage_of_exports',
        'country_name_foreign_collaboration',
        'collaborator_name_foreign_collaboration',
        'annual_turnover_year1',
        'annual_turnover_year2',
        'annual_turnover_year3',
        'classindustry',
        'direct_office_employees',
        'indirect_contractual_employees',
        'works_employees',
        'outsourced_employees',
        'esic',
        'epf',
        'branches_outside_india',
        'is_member_of_association',
        'association_name',
        'is_office_bearer',
        'association_position',
        'reason_for_joining_chamber',
        'e_sign',
        'seal_image',
    )


class Form2Admin(admin.ModelAdmin):
    list_display = ['__str__', 'iande', 'incometaxtpan', 'FactoryRegistrationCertificate', 'MemorandumArticleofAssociation', 'GSTINRegistrationCopy', 'IECodeCertificate', 'ProfessionalCertificate', 'CopyofLandDocument', 'LandHolding', 'passportsizephoto', 'DirectorsPartners']


admin.site.register(Form2, Form2Admin)
admin.site.register(Form1, Form1Admin)
admin.site.register(Director)

