from django.urls import path
from . import views

urlpatterns = [
    path('device/<int:device_id>/grid/', views.InterfaceGridView.as_view(), name='interface_grid'),
    path('rack/<int:rack_id>/grid/', views.RackInterfaceGridView.as_view(), name='rack_interface_grid'),
]
