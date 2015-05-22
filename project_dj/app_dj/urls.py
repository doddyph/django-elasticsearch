from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^build-an-index/$', views.api_elastic_sample_build_an_index, name='api-elastic-sample-build-an-index'),
    url(r'^mapping/$', views.api_elastic_mapping, name='api-elastic-mapping'),
]