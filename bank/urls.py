from django.urls import path

from bank.views import update_bank_account, start_audit, upload_declaration

urlpatterns = [
    path('ajax-top-up-account/', update_bank_account, name='update_bank_account'),
    path('ajax-start-audit/', start_audit, name='start_audit'),
    path('ajax-upload-declaration/', upload_declaration, name='upload_declaration')
]