"""NAFLDdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views, search, details, structure, screen, reposition, annotation
from django.conf.urls import url


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^search/$', search.search),
    url(r'^strategies/$', views.strategies),
    url(r'^strategy_details/$', details.strategy_details),
    url(r'^targets/$', views.targets),
    url(r'^target_details/$', details.target_details),
    url(r'^drugs/$', views.drugs),
    url(r'^drug_details/$', details.drug_details),
    url(r'^trials/$', views.trials),
    url(r'^trial_details/$', details.trial_details),
    url(r'^diseases/$', views.diseases),
    url(r'^disease_details/$', details.disease_details),
    url(r'^candidates/$', views.candidates),
    url(r'^candidate_details/$', details.candidate_details),
    url(r'^compounds/$', views.compounds),
    url(r'^compound_details/$', details.compound_details),
    url(r'^articles/$', views.articles),
    url(r'^article_details/$', details.article_details),
    url(r'^structure/$', views.structure),
    url(r'^structure/structure_search/$', structure.search),
    url(r'^screening/$', views.screening),
    url(r'^screening/screening_screen/$', screen.screen),
    url(r'^reposition/$', views.reposition),
    url(r'^reposition/reposition_node/$', reposition.getnodename),
    url(r'^reposition/reposition/$', reposition.reposition),
    url(r'^cmap/$', views.cmap),
    url(r'^cmap_details/$', details.cmap_details),
    url(r'^products/$', views.products),
    url(r'^product_details/$', details.product_details),
    url(r'^casestudy/$', views.casestudy),
    url(r'^downloads/$', views.downloads),
    url(r'^about/$', views.about),
    url(r'^download/$', views.download),
    url(r'^tutorial/$', views.tutorial),
    url(r'^annotation/$', views.annotation),
    url(r'^annotation/annotation_search/$', annotation.annotation_search),
    url(r'^models/$', views.models),
    url(r'^pathogenesis/$', views.pathogenesis),
]
