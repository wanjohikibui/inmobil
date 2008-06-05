from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^inmobil/', include('inmobil.foo.urls')),

 	(r'^media/(.*)$','django.views.static.serve',{'document_root': 'upload/', 'show_indexes': True}),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
)
