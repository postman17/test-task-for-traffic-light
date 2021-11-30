from rest_framework import mixins, viewsets

from accounts.models import Client, Department

from accounts.serializers import ClientSerializer, DepartmentSerializer


class ClientListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class DepartmentListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self, queryset=None):
        queryset = Department.objects.filter(parent=None)
        return queryset.get_cached_trees()
