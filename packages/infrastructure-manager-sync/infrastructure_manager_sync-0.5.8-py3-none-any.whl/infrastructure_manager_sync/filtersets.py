import django_filters
from netbox.filtersets import NetBoxModelFilterSet
from .models import (
    InfrastructureManagerSync,
    InfrastructureManagerSyncVMInfo,
    InfrastructureManagerSyncHostInfo,
)
from tenancy.models import Tenant
from virtualization.models import Cluster
from django.db.models import Q


class InfrastructureManagerSyncFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = InfrastructureManagerSync
        fields = (
            "name",
            "fqdn",
            "username",
            "primary_site_id",
            "enabled",
            "update_prio",
            "cluster_tenant_id",
        )

    assign_by_default_to_cluster_tenant = django_filters.BooleanFilter(
        label="Assigned tenant by default",
    )

    enabled = django_filters.BooleanFilter(
        label="Enabled",
    )

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(fqdn__icontains=value)
        return queryset.filter(qs_filter)


class InfrastructureManagerSyncVMInfoFilterSet(NetBoxModelFilterSet):

    tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name="vm__tenant",
        queryset=Tenant.objects.all(),
        label="Tenant (ID)",
    )

    cluster_id = django_filters.ModelMultipleChoiceFilter(
        field_name="vm__cluster",
        queryset=Cluster.objects.all(),
        label="Cluster (ID)",
    )

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(vm__name__icontains=value)
        return queryset.filter(qs_filter)

    class Meta:
        model = InfrastructureManagerSyncVMInfo
        fields = (
            "environment",
            "criticality",
            "financial_info",
            "licensing",
            "backup_status",
            "backup_plan",
            "backup_type",
            "deployed_by",
            "billing_reference",
            "ims",
            "vmware_tools_version",
            "vm_hardware_compatibility",
            "requested_by",
            "managed_by",
            "financial_type",
            "cost_center",
        )


class InfrastructureManagerSyncHostInfoFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = InfrastructureManagerSyncHostInfo
        fields = (
            "memory",
            "build_number",
            "ims",
        )

    tenant_id = django_filters.ModelMultipleChoiceFilter(
        field_name="host__tenant",
        queryset=Tenant.objects.all(),
        label="Tenant (ID)",
    )

    cluster_id = django_filters.ModelMultipleChoiceFilter(
        field_name="host__cluster",
        queryset=Cluster.objects.all(),
        label="Cluster (ID)",
    )

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(host__name__icontains=value)
        return queryset.filter(qs_filter)
