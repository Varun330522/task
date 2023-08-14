from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserDetails(AbstractUser):

    username = models.CharField(max_length=150, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    token = models.JSONField(null=True, blank=True)
    is_staff = None
    is_active = None
    date_joined = None
    groups = None
    user_permissions = None
    last_login = None
    is_superuser = None
    first_name = None
    last_name = None

    def __str__(self):
        return self.username


class Loan(models.Model):
    loan_id = models.CharField(primary_key=True)
    user_id = models.ForeignKey(UserDetails, on_delete=models.DO_NOTHING)
    amount = models.SmallIntegerField()
    tenure_month = models.SmallIntegerField()
    status = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_loanId():
        last_loan = Loan.objects.filter().last()
        if last_loan:
            last_id = int(last_loan.loan_id.split('_')[1]) + 1
        else:
            last_id = 1
        return f"loan_{last_id}"
