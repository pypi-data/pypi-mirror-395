
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from hwmux_client.api.token_auth_api import TokenAuthApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from hwmux_client.api.token_auth_api import TokenAuthApi
from hwmux_client.api.callback_api import CallbackApi
from hwmux_client.api.devices_api import DevicesApi
from hwmux_client.api.django_login_api import DjangoLoginApi
from hwmux_client.api.external_signin_api import ExternalSigninApi
from hwmux_client.api.groups_api import GroupsApi
from hwmux_client.api.labels_api import LabelsApi
from hwmux_client.api.logs_api import LogsApi
from hwmux_client.api.outbox_api import OutboxApi
from hwmux_client.api.part_families_api import PartFamiliesApi
from hwmux_client.api.parts_api import PartsApi
from hwmux_client.api.permissions_api import PermissionsApi
from hwmux_client.api.reservations_api import ReservationsApi
from hwmux_client.api.rooms_api import RoomsApi
from hwmux_client.api.schema_api import SchemaApi
from hwmux_client.api.signin_api import SigninApi
from hwmux_client.api.signout_api import SignoutApi
from hwmux_client.api.sites_api import SitesApi
from hwmux_client.api.user_api import UserApi
