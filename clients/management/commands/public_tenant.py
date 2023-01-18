
from django.core.management.base import BaseCommand
from tenant_users.tenants.models import ExistsError
from tenant_users.tenants.utils import create_public_tenant

from users.models import TenantUser


class Command(BaseCommand):
    help = "Setup Public Tenant"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):

        domain = "test.com"

        try:
            create_public_tenant(domain, "admin@" + domain)
            TenantUser.objects.create_superuser(
                email="superuser@" + domain, password="admin", is_active=True
            )
            print("Public tenant created.")
        except ExistsError:
            print("Public tenant already exists.")
        except Exception as error:
            print(error)
