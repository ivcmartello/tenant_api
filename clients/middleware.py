import logging
from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django_tenants.middleware import TenantMainMiddleware
from django_tenants.utils import get_public_schema_name, get_tenant_model

logger = logging.getLogger(__name__)


class RequestIDTenantMiddleware(TenantMainMiddleware):
    def get_tenant_by_schema(self, tenant_model, hostname, request):
        public_schema_name = get_public_schema_name()
        logger.info(f"Public schema name: {public_schema_name}")
        try:
            public_tenant = tenant_model.objects.get(schema_name=public_schema_name)
        except ObjectDoesNotExist:
            public_tenant = tenant_model.objects.create(
                domain_url=hostname,
                schema_name=public_schema_name,
                name=public_schema_name.capitalize(),
                paid_until=date.today() + relativedelta(months=+1),
                on_trial=False,
            )
        public_tenant.save()
        logger.info(f"Public Tenant: {public_tenant}")

        x_request_id = request.META.get("HTTP_X_REQUEST_ID", public_tenant.uuid)
        logger.info(f"X-Request ID: {x_request_id}")

        tenant = tenant_model.objects.filter(uuid=x_request_id).first()
        logger.info(f"Tenant: {tenant}")

        if tenant == None:
            return public_tenant
        return tenant

    def process_request(self, request):
        # Connection needs first to be at the public schema, as this is where
        # the tenant metadata is stored.

        connection.set_schema_to_public()
        hostname = self.hostname_from_request(request)

        tenant_model = get_tenant_model()
        tenant = self.get_tenant_by_schema(tenant_model, hostname, request)

        tenant.domain_url = hostname
        request.tenant = tenant
        connection.set_tenant(request.tenant)
        self.setup_url_routing(request)
