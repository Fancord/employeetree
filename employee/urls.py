from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'employees', views.EmployeeModelViewSet)




urlpatterns = [
    path('', include(router.urls)),
    path('employees/level/<int:level>/', views.EmployeeModelViewSet.as_view({'get': 'employees_by_level'})),
]
