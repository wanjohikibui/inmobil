from django.conf.urls.defaults import *
from inmobil.views import index
from inmobil.balance import views
urlpatterns = patterns('',
    
    (r'index/$', index), 
    (r'^consorcios/$', 'inmobil.views.listarConsorcios'),

 	(r'^static/(.*)$','django.views.static.serve',{'document_root': 'static/', 'show_indexes': True}),
 	(r'^media/(.*)$','django.views.static.serve',{'document_root': 'upload/', 'show_indexes': True}),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
)