from django.urls import path

from accounts.views import ClientListViewSet, DepartmentListViewSet

urlpatterns = [
    path('clients/', ClientListViewSet.as_view({'get': 'list'}), name='clients-list'),
    path('departments/', DepartmentListViewSet.as_view({'get': 'list'}), name='departments-list'),
]
