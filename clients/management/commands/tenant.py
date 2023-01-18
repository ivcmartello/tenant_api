
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django_tenants.utils import get_public_schema_name, schema_context
from tenant_users.tenants.models import ExistsError
from tenant_users.tenants.tasks import provision_tenant

from users.models import TenantUser


class Command(BaseCommand):
    help = "Setup Tenant"

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('pass', type=str)


    def handle(self, *args, **options):
        tenant_name = options["name"]
        user_email = options["email"]
        user_pass = options["pass"]

        with schema_context(get_public_schema_name()):
            user = (
                get_user_model()
                .objects.filter(email__exact=user_email)
                .first()
            )
            if not user:
                TenantUser.objects.create_user(is_active=True, email=user_email, password=user_pass)

        try:
            provision_tenant(tenant_name, tenant_name, user_email, is_staff=True)
            print("Tenant created.")
        except ExistsError:
            print("Tenant already exists.")
        except Exception as error:
            print(error)
