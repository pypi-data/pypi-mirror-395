from typing import List
import strawberry
import strawberry_django

from . import models


@strawberry_django.type(
    models.InfrastructureManagerSync,
    fields=["name",
            "fqdn",
            "cluster_tenant",
            "entry_type",
            "primary_site",
            "enabled",
            "update_prio",
            "assign_by_default_to_cluster_tenant",
            "last_successful_sync",
            "build_number",
            "version",
            "id"
        ],
)
class InfrastructureManagerSyncType:
    pass


@strawberry.type(name="Query")
class DummyQuery:
    infrastructure_manager_sync: InfrastructureManagerSyncType = strawberry_django.field()
    infrastructure_manager_sync_list: List[InfrastructureManagerSyncType] = strawberry_django.field()


schema = [
    DummyQuery,
]