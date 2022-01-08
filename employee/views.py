from rest_framework import permissions
from rest_framework.response import Response

from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeModelViewSet(ReadOnlyModelViewSet):
    """
    Данные о сотрудниках.
    Их получают только авторизовавшиеся пользователи
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def employees_by_level(self, request, level=None):
        """Данные о сотрудниках одного уровня."""
        employees = self.queryset.filter(level=level)
        serializer = self.serializer_class(employees, many=True)
        return Response(serializer.data)
