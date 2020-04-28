from django.conf.urls import  include, url
from forums import views
from migrate_spoken.views import chenage_drupal_userid_spoken
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'forums.views.home', name='home'),
    # url(r'^forums/', include('forums.foo.urls')),
    url(r'^', include('website.urls', namespace='website')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # User account urls
    url(r'^accounts/login/', views.user_login, name='user_login'),
    url(r'^accounts/logout/', views.user_logout, name='user_logout'),
    url(r'^migrate', chenage_drupal_userid_spoken, name='chenage_drupal_userid_spoken'),
    url(r'^accounts/update-password/$', views.updatepassword, name='updatepassword'),
]
