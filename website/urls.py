from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/', 'website.views.login_view'),
    url(r'^auth/', 'website.views.auth_and_login'),
    url(r'^signup/', 'website.views.sign_up_in'),
    url(r'^$', 'website.views.secured'),
    url(r'^logout/', 'website.views.logout_view'),
    url(r'^get_data/', 'website.views.get_data'),
    url(r'^get_new_upload_code/', 'website.views.get_new_upload_code'),
    url(r'^upload/', 'website.views.upload'),
    url(r'^get_upload_data/', 'website.views.get_upload_data'),
    url(r'^del_upload_data/', 'website.views.del_upload_data'),
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^website/', include('website.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)