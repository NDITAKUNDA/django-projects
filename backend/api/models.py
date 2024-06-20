# models.py in the `api` app
from django.db import models
from django.contrib.auth.models import User

# models.py in the `api` app
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_company_user = models.BooleanField(default=False)


class Company(models.Model):
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=255)
    date_of_registration = models.DateField()
    address = models.TextField()
    contact_person = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    role = models.CharField(max_length=255)
    date_started = models.DateField()
    date_left = models.DateField(null=True, blank=True)
    duties = models.TextField()

    def save(self, *args, **kwargs):
        if self.pk:
            # existing employee, update history
            previous = Employee.objects.get(pk=self.pk)
            EmployeeHistory.objects.create(
                employee=self,
                role=previous.role,
                department=previous.department.name if previous.department else None,
                date_started=previous.date_started,
                date_left=previous.date_left
            )
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# models.py in the `api` app
class EmployeeHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='history')
    role = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    date_started = models.DateField()
    date_left = models.DateField(null=True, blank=True)
