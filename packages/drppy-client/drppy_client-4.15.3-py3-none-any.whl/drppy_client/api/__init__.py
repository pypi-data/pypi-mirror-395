from __future__ import absolute_import

# flake8: noqa

# import apis into api package
from drppy_client.api.activities_api import ActivitiesApi
from drppy_client.api.alerts_api import AlertsApi
from drppy_client.api.batches_api import BatchesApi
from drppy_client.api.blueprints_api import BlueprintsApi
from drppy_client.api.boot_envs_api import BootEnvsApi
from drppy_client.api.catalog_items_api import CatalogItemsApi
from drppy_client.api.clusters_api import ClustersApi
from drppy_client.api.connections_api import ConnectionsApi
from drppy_client.api.contents_api import ContentsApi
from drppy_client.api.contexts_api import ContextsApi
from drppy_client.api.endpoints_api import EndpointsApi
from drppy_client.api.events_api import EventsApi
from drppy_client.api.files_api import FilesApi
from drppy_client.api.filters_api import FiltersApi
from drppy_client.api.identity_providers_api import IdentityProvidersApi
from drppy_client.api.indexes_api import IndexesApi
from drppy_client.api.info_api import InfoApi
from drppy_client.api.interfaces_api import InterfacesApi
from drppy_client.api.isos_api import IsosApi
from drppy_client.api.jobs_api import JobsApi
from drppy_client.api.leases_api import LeasesApi
from drppy_client.api.logs_api import LogsApi
from drppy_client.api.machines_api import MachinesApi
from drppy_client.api.meta_api import MetaApi
from drppy_client.api.objects_api import ObjectsApi
from drppy_client.api.params_api import ParamsApi
from drppy_client.api.plugin_providers_api import PluginProvidersApi
from drppy_client.api.plugins_api import PluginsApi
from drppy_client.api.pools_api import PoolsApi
from drppy_client.api.prefs_api import PrefsApi
from drppy_client.api.profiles_api import ProfilesApi
from drppy_client.api.reservations_api import ReservationsApi
from drppy_client.api.resource_brokers_api import ResourceBrokersApi
from drppy_client.api.roles_api import RolesApi
from drppy_client.api.stages_api import StagesApi
from drppy_client.api.store_objects_api import StoreObjectsApi
from drppy_client.api.subnets_api import SubnetsApi
from drppy_client.api.system_api import SystemApi
from drppy_client.api.tasks_api import TasksApi
from drppy_client.api.templates_api import TemplatesApi
from drppy_client.api.tenants_api import TenantsApi
from drppy_client.api.trigger_providers_api import TriggerProvidersApi
from drppy_client.api.triggers_api import TriggersApi
from drppy_client.api.users_api import UsersApi
from drppy_client.api.ux_options_api import UxOptionsApi
from drppy_client.api.ux_settings_api import UxSettingsApi
from drppy_client.api.ux_views_api import UxViewsApi
from drppy_client.api.version_sets_api import VersionSetsApi
from drppy_client.api.whoami_api import WhoamiApi
from drppy_client.api.work_orders_api import WorkOrdersApi
from drppy_client.api.workflows_api import WorkflowsApi
from drppy_client.api.zones_api import ZonesApi

# import code needed for monkey patch code
# edit the mustache file to add additional imports
from .custom_overrides import custom_post_machine_param

MachinesApi.post_machine_param = classmethod(custom_post_machine_param)
