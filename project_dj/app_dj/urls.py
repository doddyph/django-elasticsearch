from django.conf.urls import url, include
from django.views.generic import TemplateView
import views

urlpatterns = [
    url(r'^build-an-index/$', views.api_elastic_sample_build_an_index, name='api-elastic-sample-build-an-index'),
    url(r'^mapping/$', views.api_elastic_mapping, name='api-elastic-mapping'),
    url(r'^search/$', TemplateView.as_view(template_name='app_dj/search.html'), name='api-elastic-search'),
    url(r'^query/$', views.api_elastic_query, name='api-elastic-query'),
]