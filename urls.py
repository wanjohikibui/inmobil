from django.conf.urls.defaults import *
from inmobil.views import index
from inmobil.balance import views
urlpatterns = patterns('',
    (r'^list/$', 'inmobil.balance.views.listarConsorcios'),


    (r'index/$', index), 

 	(r'^static/(.*)$','django.views.static.serve',{'document_root': 'static/', 'show_indexes': True}),
 	(r'^media/(.*)$','django.views.static.serve',{'document_root': 'upload/', 'show_indexes': True}),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
)