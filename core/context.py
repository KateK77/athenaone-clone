from core.access import role,patients_for
from django.db.models import Q
from core.models import Department,Practice
from engagement.models import Task
from engagement.messaging import unread_messages, MESSAGE_ROLES

NAV=[('dashboard','Overview','◫',None),('schedule','Schedule','▦',{'admin','manager','frontdesk','physician','nurse','assistant'}),('patients','Patients','♙',None),('encounters','Encounters','▤',{'admin','physician','nurse','assistant','billing','coder','manager'}),('tasks','Clinical inbox','▣',None),('orders','Orders','⊕',{'admin','physician','nurse','assistant'}),('results','Results','⌁',{'admin','physician','nurse','assistant'}),('medications','Medications','◈',{'admin','physician','nurse','assistant'}),('insurance','Insurance','▧',{'admin','manager','frontdesk','billing'}),('charges','Billing','＄',{'admin','manager','billing','coder'}),('claims','Claims','▱',{'admin','manager','billing','coder'}),('denials','Denials','⚑',{'admin','manager','billing','coder'}),('authorizations','Authorizations','◇',{'admin','physician','nurse','assistant','billing','coder','manager'}),('messages','Messages','▢',{'admin','manager','frontdesk','physician','nurse','assistant'}),('reports','Reports','▥',{'admin','manager','billing','coder'}),('ai','AI assistant','✧',{'admin','physician'}),('administration','Administration','⚙',{'admin'}),('audit','Audit logs','≡',{'admin'})]
def navigation(request):
    r=role(request.user)
    if not r: return {}
    nav=[]
    if r=='patient':
        nav=[{'key':'portal','label':'My health','icon':'◫','url':'/portal/'},{'key':'messages','label':'Messages','icon':'▢','url':'/records/messages/'}]
    else:
        for key,label,icon,roles in NAV:
            if roles is None or r in roles:
                url='/'+key+'/' if key in ['dashboard','reports','ai','administration','schedule'] else f'/records/{key}/'
                nav.append({'key':key,'label':label,'icon':icon,'url':url})
    tasks=Task.objects.filter(status='Open',patient__in=patients_for(request.user))
    if r!='admin': tasks=tasks.filter(Q(role=r)|Q(assigned=request.user))
    return {'message_access':r in MESSAGE_ROLES,'unread_message_count':unread_messages(request.user).count(),'nav':nav,'user_role':r,'role_label':request.user.profile.get_role_display(),'practice':Practice.objects.first(),'departments':Department.objects.all(),'task_count':tasks.count(),'today':__import__('django').utils.timezone.localdate()}
