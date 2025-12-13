from . import Configuration, ApiClient, ApiClientAsync
from .apis import (
    GroupsApi,
    DevicesApi,
    SitesApi,
    RoomsApi,
    PartsApi,
    PartFamiliesApi,
    LabelsApi,
    LogsApi,
    SchemaApi,
    ReservationsApi,
)
from .models import ReservationRequest, ReservationSessionSerializerReadOnly
from urllib3.util.retry import Retry
from typing import Optional
from threading import Thread
from time import sleep
from datetime import datetime, timezone, timedelta
import logging
import asyncio

__all__ = [
    "HwMuxApi",
    "ReservationNotSatisfiedException",
    "SatisfiedReservationWatchdog",
    "HwMuxApiAsync",
]


class ReservationNotSatisfiedException(Exception):
    """
    Raised from HwMuxApicreate_reservation() when a reservation is not
    satisfied and raise_error_if_not_satisfied=True
    """


class FailedToFetchResourceDataException(Exception):
    """
    Raised when failed to fetch resource data for a reservation.
    """


def ApiDecorator(apiClass):
    class NewApiClass(apiClass):
        @classmethod
        def list_all(cls, method, *args, **kwargs):
            return HwMuxApi.list_all(method, *args, **kwargs)

    return NewApiClass


class HwMuxApi:
    """
    HwMuxApi is a wrapper around the hwmux_client library that provides access to all public APIs.
    """

    def __init__(
        self,
        user_token: Optional[str] = None,
        server_url: Optional[str] = None,
        retries: Optional[Retry] = None,
        config: Optional[Configuration] = None,
    ):
        if config is None:
            config = Configuration(host=server_url)
            if user_token is not None:
                config = Configuration(
                    host=server_url,
                    api_key={"tokenAuth": user_token},
                    api_key_prefix={"tokenAuth": "Token"},
                    discard_unknown_keys=True,
                )
            config.retries = retries
        else:
            if any(t is not None for t in [user_token, server_url, retries]):
                raise ValueError(
                    "If config is provided, user_token, server_url, and retries must be None"
                )
        self.client = ApiClient(config)
        self._create_apis(self.client)
        self.logger = logging.getLogger(__name__)

    def _create_apis(self, client):
        self.apis = {}
        for api in [
            GroupsApi,
            DevicesApi,
            SitesApi,
            RoomsApi,
            PartsApi,
            PartFamiliesApi,
            LabelsApi,
            LogsApi,
            SchemaApi,
            ReservationsApi,
        ]:
            self.apis[api.__name__] = ApiDecorator(api)(client)

    @classmethod
    def list_all(cls, method, *args, **kwargs):
        all_items = []
        page = 0
        while True:
            page += 1
            kwargs["page"] = page
            items = method(*args, **kwargs)
            all_items.extend(items.results)
            if items.next is None:
                break
        return all_items

    def get_location_url(self, site, room, location_id):
        url = f"{self.client.configuration.host}/api/sites/{site}/rooms/{room}/locations/{location_id}/".replace(
            "https", "http"
        )
        return url

    @property
    def groups_api(self) -> GroupsApi:
        return self.apis["GroupsApi"]

    @property
    def devices_api(self) -> DevicesApi:
        return self.apis["DevicesApi"]

    @property
    def sites_api(self) -> SitesApi:
        return self.apis["SitesApi"]

    @property
    def rooms_api(self) -> RoomsApi:
        return self.apis["RoomsApi"]

    @property
    def parts_api(self) -> PartsApi:
        return self.apis["PartsApi"]

    @property
    def part_families_api(self) -> PartFamiliesApi:
        return self.apis["PartFamiliesApi"]

    @property
    def labels_api(self) -> LabelsApi:
        return self.apis["LabelsApi"]

    @property
    def logs_api(self) -> LogsApi:
        return self.apis["LogsApi"]

    @property
    def schema_api(self) -> SchemaApi:
        return self.apis["SchemaApi"]

    @property
    def reservations_api(self) -> ReservationsApi:
        return self.apis["ReservationsApi"]

    def _create_and_wait_until_satisfied(
        self,
        request: ReservationRequest,
        raise_error_if_not_satisfied: bool,
        max_time_delta: timedelta,
    ) -> ReservationSessionSerializerReadOnly:
        """Create a reservation and wait until it is satisfied."""
        reservation: ReservationSessionSerializerReadOnly = (
            self.reservations_api.reservations_create(reservation_request=request)
        )
        if not reservation.is_satisfied:
            reservation = self.reservations_api.reservations_update(reservation.id)
        start_time = datetime.now()
        while not reservation.is_satisfied:
            if (
                raise_error_if_not_satisfied
                and datetime.now() - start_time > max_time_delta
            ):
                self.reservations_api.reservations_cancel_update(reservation.id)
                raise ReservationNotSatisfiedException("Reservation not satisfied")
            interval = (
                5
                if raise_error_if_not_satisfied
                else min(
                    30,
                    int(seconds_until_lease_expires(reservation) / 2),
                )
            )
            self.logger.info(
                f"Reservation not satisfied, waiting {interval} seconds..."
            )
            sleep(interval)
            reservation = self.reservations_api.reservations_update(reservation.id)
        return reservation

    def create_reservation_without_watchdog(
        self,
        request: ReservationRequest,
        raise_error_if_not_satisfied=False,
        max_wait_time_sec_if_raise_error_if_not_satisfied=30,
    ):
        """
        Create a reservation and wait until it is satisfied.
        Args:
            request: reservation request
            raise_error_if_not_satisfied: if True, raise ReservationNotSatisfiedException if reservation
                  is not satisfied within max_wait_time_sec_if_raise_error_if_not_satisfied seconds
            max_wait_time_sec_if_raise_error_if_not_satisfied: maximum time to wait for reservation to be satisfied before
                  raising ReservationNotSatisfiedException if raise_error_if_not_satisfied is True

        Returns:
            SatisfiedReservationWithoutWatchdog object that can be used to release the reservation.

        """
        max_time_delta = timedelta(
            seconds=max_wait_time_sec_if_raise_error_if_not_satisfied
        )

        if request.use_watchdog:
            self.logger.warning(
                "use_watchdog is set to True. This is not supported when using create_reservation_without_watchdog()"
                "and will be ignored. Please use create_reservation() instead."
            )
            request.use_watchdog = False  # disable the watchdog

        reservation = self._create_and_wait_until_satisfied(
            request, raise_error_if_not_satisfied, max_time_delta
        )
        return SatisfiedReservationWithoutWatchdog(self, reservation)

    def create_reservation(
        self,
        request: ReservationRequest,
        raise_error_if_not_satisfied=False,
        max_wait_time_sec_if_raise_error_if_not_satisfied=30,
    ):
        """
        Create a reservation with the watchdong enabled and wait until it is satisfied.
        Args:
            request: reservation request
            raise_error_if_not_satisfied: if True, raise ReservationNotSatisfiedException if reservation
                  is not satisfied within max_wait_time_sec_if_raise_error_if_not_satisfied seconds
            max_wait_time_sec_if_raise_error_if_not_satisfied: maximum time to wait for reservation to be satisfied before
                  raising ReservationNotSatisfiedException if raise_error_if_not_satisfied is True

        Returns:
            SatisfiedReservationWatchdog object that periodically renews the
            reservation lease in a background thread and can be used to release the reservation.

        """
        max_time_delta = timedelta(
            seconds=max_wait_time_sec_if_raise_error_if_not_satisfied
        )

        if not request.use_watchdog:
            self.logger.warning(
                "use_watchdog is set to False. This is not supported when using create_reservation()"
                "and will be ignored. Please use create_reservation_without_watchdog() instead."
            )
            request.use_watchdog = True  # enable the watchdog

        reservation = self._create_and_wait_until_satisfied(
            request, raise_error_if_not_satisfied, max_time_delta
        )
        return SatisfiedReservationWatchdog(self, reservation)


class SatisfiedReservationWithoutWatchdog:
    """
    A SatisfiedReservationWithoutWatchdog object is returned from HwMuxApi.create_reservation_without_watchdog()
    It can be used to release the reservation.
    """

    def __init__(
        self,
        hwmux: HwMuxApi,
        reservation: ReservationSessionSerializerReadOnly,
    ):
        self.reservation = reservation
        self.reservations_api: ReservationsApi = hwmux.reservations_api
        self.devices_api: DevicesApi = hwmux.devices_api
        self.groups_api: GroupsApi = hwmux.groups_api

    @property
    def reservation_id(self):
        return self.reservation.id

    def release(self):
        """
        Releases the reservation.
        """
        return self.reservations_api.reservations_release_update(self.reservation_id)

    def get_resource_data(self) -> dict:
        """
        Returns the resource data for the reservation.
        """
        devices = {}
        # save device data from r_devices into a dict
        r_devices: list[int] = self.reservation.r_devices
        if r_devices:
            devices_resp = self.devices_api.devices_list(id__in=r_devices)
            if devices_resp is None:
                raise FailedToFetchResourceDataException(
                    "Failed to get devices. API Response is None."
                )
            actual_ids_set = {device.id for device in devices_resp.results}
            expected_ids_set = set(r_devices)
            if actual_ids_set != expected_ids_set:
                raise FailedToFetchResourceDataException(
                    f"Failed to get all devices. Expected: {expected_ids_set}, Actual: {actual_ids_set}"
                )

            for device in devices_resp.results:
                devices[device.id] = device

        groups = {}

        # save group data from a_device_groups into a dict
        a_device_groups: list[int] = self.reservation.a_device_groups
        if a_device_groups:
            groups_resp = self.groups_api.groups_list(id__in=a_device_groups)
            if groups_resp is None:
                raise FailedToFetchResourceDataException(
                    "Failed to get groups. API Response is None."
                )
            actual_ids_set = {group.id for group in groups_resp.results}
            expected_ids_set = set(a_device_groups)
            if actual_ids_set != expected_ids_set:
                raise FailedToFetchResourceDataException(
                    f"Failed to get all groups. Expected: {expected_ids_set}, Actual: {actual_ids_set}"
                )

            for group in groups_resp.results:
                groups[group.id] = group

        resource_data = {"devices": devices, "device_groups": groups}
        return resource_data


class SatisfiedReservationWatchdog(SatisfiedReservationWithoutWatchdog):
    """
    A SatisfiedReservationWatchdog object is returned from HwMuxApi.create_reservation()
    It contains a background thread that periodically renews the reservation lease and a
    release() method that cancels the background thread and releases the reservation.
    """

    default_watchdog_max_interval = 30

    def __init__(
        self,
        hwmux: HwMuxApi,
        reservation: ReservationSessionSerializerReadOnly,
    ):
        """
        Creates a new SatisfiedReservationWatchdog object and starts the background thread.
        Args:
            hwmux_api: instance of HwMuxApi
            reservation_id: reservation id
        """
        super().__init__(hwmux, reservation)
        self.stop_watchdog = False
        self.reservation = reservation
        self.watchdog_thread = Thread(target=self.watchdog_thread)
        self.watchdog_thread.daemon = True
        self.watchdog_thread.start()

    def _release(self, reservations_api):
        self.stop_watchdog = True
        self.watchdog_thread.join()
        return reservations_api.reservations_release_update(self.reservation_id)

    def release(self):
        """
        Releases the reservation and stops the background thread.
        """
        self._release(self.reservations_api)

    def wait_for_watchdog_interval(self, interval: int):
        """
        Waits for the watchdog interval to expire or until stop_watchdog is set to True.
        """
        start = datetime.now()
        while (
            datetime.now() - start
        ).total_seconds() < interval and not self.stop_watchdog:
            sleep(0.1)

    def watchdog_thread(self):
        """
        Background thread that periodically renews the reservation lease.
        """
        logger = logging.getLogger(__name__)
        while not self.stop_watchdog:
            interval = min(
                self.default_watchdog_max_interval,
                int(seconds_until_lease_expires(self.reservation) / 2),
            )
            self.wait_for_watchdog_interval(interval)
            if not self.stop_watchdog:
                logger.debug("Renewing reservation lease")
                self.reservation = self.reservations_api.reservations_update(
                    self.reservation_id
                )


class HwMuxApiAsync(HwMuxApi):
    def __init__(
        self,
        user_token: Optional[str] = None,
        server_url: Optional[str] = None,
        retries: Optional[Retry] = None,
        config: Optional[Configuration] = None,
    ):
        super().__init__(user_token, server_url, retries, config)
        # store params so we can create a sync client later if needed
        self.user_token = user_token
        self.server_url = server_url
        self.retries = retries
        self.config = config

        self.client = ApiClientAsync(self.client.configuration)
        self._create_apis(self.client)

    def get_sync_client(self) -> HwMuxApi:
        return HwMuxApi(self.user_token, self.server_url, self.retries, self.config)

    @classmethod
    async def list_all(cls, method, *args, **kwargs):
        all_items = []
        page = 0
        while True:
            page += 1
            kwargs["page"] = page
            items = await method(*args, **kwargs)
            all_items.extend(items.results)
            if items.next is None:
                break
        return all_items

    async def create_reservation(
        self,
        request: ReservationRequest,
        raise_error_if_not_satisfied=False,
        max_wait_time_sec_if_raise_error_if_not_satisfied=30,
    ):
        """
        Create a reservation and wait until it is satisfied.
        Args:
            request: reservation request
            raise_error_if_not_satisfied: if True, raise ReservationNotSatisfiedException if reservation
                  is not satisfied within max_wait_time_sec_if_raise_error_if_not_satisfied seconds
            max_wait_time_sec_if_raise_error_if_not_satisfied: maximum time to wait for reservation to be satisfied before
                  raising ReservationNotSatisfiedException if raise_error_if_not_satisfied is True

        Returns:
            SatisfiedReservationWatchdog object that periodically renews the
            reservation lease in a background thread and can be used to release the reservation.

        """
        logger = logging.getLogger(__name__)
        max_time_delta = timedelta(
            seconds=max_wait_time_sec_if_raise_error_if_not_satisfied
        )
        reservation: ReservationSessionSerializerReadOnly = (
            await self.reservations_api.reservations_create(reservation_request=request)
        )
        if not reservation.is_satisfied:
            reservation = await self.reservations_api.reservations_update(
                reservation.id
            )
        start_time = datetime.now()
        while not reservation.is_satisfied:
            if (
                raise_error_if_not_satisfied
                and datetime.now() - start_time > max_time_delta
            ):
                await self.reservations_api.reservations_cancel_update(reservation.id)
                raise ReservationNotSatisfiedException("Reservation not satisfied")
            interval = (
                5
                if raise_error_if_not_satisfied
                else min(
                    30,
                    int(seconds_until_lease_expires(reservation) / 2),
                )
            )
            logger.info(f"Reservation not satisfied, waiting {interval} seconds...")
            await asyncio.sleep(interval)
            reservation = await self.reservations_api.reservations_update(
                reservation.id
            )
        return SatisfiedReservationWatchdogAsync(self, reservation)


def seconds_until_lease_expires(reservation: ReservationSessionSerializerReadOnly):
    if reservation.t_lease_expires is None:
        return 60  # default to 60 seconds if lease expiration time is not set
    return (reservation.t_lease_expires - datetime.now(timezone.utc)).total_seconds()


class SatisfiedReservationWatchdogAsync(SatisfiedReservationWatchdog):
    def __init__(self, async_hwmux: HwMuxApiAsync, reservation):
        super().__init__(async_hwmux.get_sync_client(), reservation)
        self.async_reservations_api = async_hwmux.reservations_api

    async def release(self):
        """
        Releases the reservation and stops the background thread.
        """
        await self._release(self.async_reservations_api)
