from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from .sitemaps import (HomeSitemap,
                       FaqSitemap,
                       AboutSitemap,
                       ListSitemap,
                       ProfilesSitemap)

from . import views


SITEMAPS = {
    'home': HomeSitemap,
    'list': ListSitemap,
    'faq': FaqSitemap,
    'about': AboutSitemap,
    'profiles': ProfilesSitemap,
}

app_name = 'profiles'

urlpatterns = [
    path('', views.Home.as_view(),
         name='home'),
    path('list/', views.ListProfiles.as_view(),
         name='index'),
    path('list/<int:pk>/', views.ProfileDetail.as_view(),
         name='detail'),
    path('list/<int:pk>/edit', views.UpdateProfile.as_view(),
         name='edit'),
    path('list/create', views.CreateProfile.as_view(),
         name='create'),
    path('list/<int:pk>/recommend', views.CreateRecommendation.as_view(),
         name='recommend_profile'),
    path('list/recommend', views.CreateRecommendation.as_view(),
         name='recommend'),
    path('faq/', TemplateView.as_view(template_name='profiles/FAQs.html'),
         name='faq'),
    path('about/', TemplateView.as_view(template_name='profiles/about.html'),
         name='about'),
    path('profiles-autocomplete', views.ProfilesAutocomplete.as_view(),
         name='profiles_autocomplete'),
    path('countries-autocomplete', views.CountriesAutocomplete.as_view(),
         name='countries_autocomplete'),
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS},
         name='django.contrib.sitemaps.views.sitemap'),
    path('api/', include('profiles.api.urls')),
]
