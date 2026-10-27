from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chickens/', include('chickens.urls')),
    path('', RedirectView.as_view(
        pattern_name='batch_list',
        permanent=False
    )),
]
