from django.conf.urls.defaults import *
from django.views.generic import list_detail 
from inmobil.views import index
from inmobil.balance import views
from inmobil.balance.models import Consorcio



consorcio_info  = {
    "queryset" : Consorcio.objects.all(),
    "template_object_name" : "consorcio",    
}

urlpatterns = patterns('',
    
    (r'index/$', index), 
    #(r'^consorcios/$', 'inmobil.views.listarConsorcios'), 
    #lo hago mediante una generic view. ver http://djangobook.com/en/1.0/chapter09/
    (r'^consorcios/',   list_detail.object_list, consorcio_info),
    

    

 	(r'^static/(.*)$','django.views.static.serve',{'document_root': 'static/', 'show_indexes': True}),
 	(r'^media/(.*)$','django.views.static.serve',{'document_root': 'upload/', 'show_indexes': True}),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
)
