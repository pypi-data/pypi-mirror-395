from django import forms

from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import (
    CommentField,
    TagFilterField,
    DynamicModelMultipleChoiceField,
)
from .models import (
    CriticalityChoise,
    EnvironmentChoise,
    InfrastructureManagerSync,
    InfrastructureManagerSyncVMInfo,
    SyncType,
    InfrastructureManagerSyncHostInfo,
)
from utilities.forms.widgets import DatePicker, DateTimePicker
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, add_blank_choice
from django.utils.translation import gettext as _
from tenancy.models import Tenant
from virtualization.models import Cluster
from utilities.forms.rendering import FieldSet


class InfrastructureManagerSyncForm(NetBoxModelForm):
    comments = CommentField()

    assign_by_default_to_cluster_tenant = forms.BooleanField(
        label=("Assign untagged vms to cluster tenant"),
        required=False,
        initial=False,
        help_text=_(
            "Assign VMs without tenant tag automatically to the Cluster tenant"
        ),
    )

    class Meta:
        model = InfrastructureManagerSync
        fields = (
            "name",
            "fqdn",
            "username",
            "password",
            "cluster_tenant",
            "entry_type",
            "primary_site",
            "enabled",
            "update_prio",
            "assign_by_default_to_cluster_tenant",
            "comments",
            "tags",
        )


class InfrastructureManagerSyncFilterForm(NetBoxModelFilterSetForm):
    model = InfrastructureManagerSync

    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet(
            "entry_type",
            "update_prio",
            "assign_by_default_to_cluster_tenant",
            "enabled",
            name=_("IMS"),
        ),
        FieldSet(
            "cluster_tenant_id",
            name=_("Tenancy"),
        ),
    )

    entry_type = forms.MultipleChoiceField(choices=SyncType, required=False)

    assign_by_default_to_cluster_tenant = forms.NullBooleanField(
        required=False,
        label=_("Assign default tenant"),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    enabled = forms.NullBooleanField(
        required=False,
        label=_("Enabled"),
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    cluster_tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        null_option="None",
        label=_("Cluster Tenant"),
    )

    tag = TagFilterField(model)


class InfrastructureManagerSyncVMInfoSyncForm(NetBoxModelForm):
    class Meta:
        model = InfrastructureManagerSyncVMInfo
        fields = (
            "vm",
            "backup_plan",
            "backup_type",
            "criticality",
            "environment",
            "financial_info",
            "licensing",
            "service_info",
            "backup_status",
            "last_backup",
            "deployed_on",
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
        widgets = {
            "deployed_on": DatePicker(),
            "last_backup": DateTimePicker(),
        }


class InfrastructureManagerSyncVMInfoFilterForm(NetBoxModelFilterSetForm):
    model = InfrastructureManagerSyncVMInfo

    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet(
            "environment",
            "criticality",
            "financial_info",
            "licensing",
            "ims",
            "backup_plan",
            "backup_type",
            "requested_by",
            "managed_by",
            "financial_type",
            "cost_center",
            name=_("Attributes"),
        ),
        FieldSet("tenant_id", name=_("Tenant")),
        FieldSet("cluster_id", name=_("Cluster")),
    )

    environment = forms.MultipleChoiceField(choices=EnvironmentChoise, required=False)
    criticality = forms.MultipleChoiceField(choices=CriticalityChoise, required=False)

    ims = forms.ModelChoiceField(
        queryset=InfrastructureManagerSync.objects.all(),
        required=False,
        label=_("ims"),
    )


    backup_plan = forms.CharField(max_length=100, required=False)

    backup_type = forms.CharField(max_length=100, required=False)

    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(), required=False, label=_("Tenants")
    )
    cluster_id = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(), required=False, label=_("Clusters")
    )


class InfrastructureManagerSyncHostInfoSyncForm(NetBoxModelForm):
    class Meta:
        model = InfrastructureManagerSyncHostInfo
        fields = ("host", "build_number")


class InfrastructureManagerSyncHostInfoFilterForm(NetBoxModelFilterSetForm):
    model = InfrastructureManagerSyncHostInfo

    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("ims", name=_("Attributes")),
        FieldSet("tenant_id", name=_("Tenant")),
        FieldSet("cluster_id", name=_("Cluster")),
    )

    ims = forms.ModelChoiceField(
        queryset=InfrastructureManagerSync.objects.all(),
        required=False,
        label=_("ims"),
    )

    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(), required=False, label=_("Tenants")
    )

    cluster_id = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(), required=False, label=_("Clusters")
    )
