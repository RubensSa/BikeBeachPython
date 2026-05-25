from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('', include(('rentals.urls', 'rentals'), namespace='rentals')),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
]
