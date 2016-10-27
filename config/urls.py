# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
                  url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
                  url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
                  url(r'^privacy/$', TemplateView.as_view(template_name='pages/privacy.html'), name='privacy'),
                  url(r'^terms/$', TemplateView.as_view(template_name='pages/terms.html'), name='terms'),
                  url(r'^contact/$', TemplateView.as_view(template_name='pages/contact.html'), name='contact'),
                  url(r'^details/$', TemplateView.as_view(template_name='pages/dispensary/details.html'), name='details'),



                  # Django Admin, use {% url 'admin:index' %}
                  url(settings.ADMIN_URL, include(admin.site.urls)),

                  # User management
                  url(r'^users/', include('web.users.urls', namespace='users')),
                  url(r'^search/', include('web.search.urls', namespace='search')),
                  url(r'^businesses/', include('web.businesses.urls', namespace='businesses')),
                  url(r'^accounts/', include('allauth.urls')),

                  # Your stuff: custom urls includes go here
                  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

                  # API
                  url(r'^api/v1/users/',
                      include('web.users.api.urls', namespace='users_api', app_name='users_api')),
                  url(r'^api/v1/search/',
                      include('web.search.api.urls', namespace='search_api', app_name='search_api')),
                  url(r'^api/v1/businesses/',
                      include('web.businesses.api.urls', namespace='businesses_api', app_name='businesses_api')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
