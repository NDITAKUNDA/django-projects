# views.py in the `api` app
from rest_framework import viewsets
from .models import Company, Department, Employee, Role
from .serializers import CompanySerializer, DepartmentSerializer, RoleSerializer, EmployeeSerializer

# views.py in the `api` app
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        employees_data = request.data.get('employees', [])
        for employee_data in employees_data:
            serializer = self.get_serializer(data=employee_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "bulk upload successful"}, status=status.HTTP_201_CREATED)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

# views.py in the `api` app
from rest_framework.permissions import IsAuthenticated
from .permisions import IsAdminUser, IsCompanyUser

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     permission_classes = [IsAuthenticated, IsCompanyUser]

