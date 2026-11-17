from django.urls import path
from core import views as v
urlpatterns=[
 path('',v.dashboard),path('health/',v.health,name='health'),path('login/',v.login_view,name='login'),path('logout/',v.logout_view,name='logout'),
 path('dashboard/',v.dashboard,name='dashboard'),path('schedule/',v.schedule,name='schedule'),
 path('records/<slug:key>/',v.record_list,name='record_list'),path('records/<slug:key>/new/',v.record_edit,name='record_create'),
 path('records/<slug:key>/<int:pk>/',v.record_detail,name='record_detail'),path('records/<slug:key>/<int:pk>/edit/',v.record_edit,name='record_edit'),path('records/<slug:key>/<int:pk>/action/',v.record_action,name='record_action'),
 path('patients/<int:pk>/',v.patient_chart,name='patient'),path('appointments/<int:pk>/check-in/',v.checkin,name='checkin'),
 path('encounters/<int:pk>/',v.encounter_view,name='encounter'),path('encounters/<int:pk>/intake/',v.intake,name='intake'),path('encounters/<int:pk>/bill/',v.bill_encounter,name='bill_encounter'),
 path('claims/<int:pk>/payment/',v.payment_view,name='payment'),path('payments/<int:pk>/receipt/',v.receipt,name='receipt'),
 path('portal/',v.portal,name='portal'),path('requests/<int:pk>/book/',v.request_booking,name='request_booking'),path('ai/',v.ai_page,name='ai'),path('reports/',v.reports,name='reports'),
 path('administration/',v.administration,name='administration'),path('administration/staff/new/',v.staff_edit,name='staff_create'),path('administration/staff/<int:pk>/',v.staff_edit,name='staff_edit'),path('administration/reset/',v.reset_demo,name='reset'),path('help/',v.help_view,name='help'),path('fhir/<str:resource>/<int:pk>/',v.fhir,name='fhir'),
]
