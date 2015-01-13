from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ztreeproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^get_tree_data','ztree.views.JSONGetView',name='get_tree_data'),
    url(r'^set_tree','ztree.views.JSONSetView',name='set_tree'),
)
