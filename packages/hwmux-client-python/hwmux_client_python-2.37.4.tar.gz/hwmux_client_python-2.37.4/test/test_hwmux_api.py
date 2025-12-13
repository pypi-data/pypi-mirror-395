import asyncio
import time
from hwmux_client.hwmux_api import (
    HwMuxApi,
    HwMuxApiAsync,
    ReservationRequest,
    ReservationNotSatisfiedException,
)
import pytest
from urllib3.util.retry import Retry


@pytest.fixture()
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def hwmux_api(hwmux_token):
    retries = Retry(
        connect=5, status=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504]
    )
    yield HwMuxApi(hwmux_token, retries=retries)


@pytest.fixture()
async def hwmux_api_async(hwmux_token):
    retries = Retry(
        connect=5, status=5, backoff_factor=2, status_forcelist=[500, 502, 503, 504]
    )
    yield HwMuxApiAsync(hwmux_token, retries=retries)


def test_hwmux_api_groups(hwmux_api):
    groups = hwmux_api.groups_api.groups_list()
    assert groups


def test_hwmux_create_reservation(hwmux_api: HwMuxApi):
    label = "iotvalsw-rf-software-regression"
    labels_list = hwmux_api.labels_api.labels_list(name=label)
    assert len(labels_list.results) == 1
    label_to_reserve = labels_list.results[0]
    reservation_request = ReservationRequest(
        r_device_group_labels=[label_to_reserve.id],
        use_watchdog=True,
        metadata={"foo": "bar"},
        details="HWMux example with watchdog",
    )
    reservation_watchdog = hwmux_api.create_reservation(
        reservation_request, raise_error_if_not_satisfied=True
    )
    resey = reservation_watchdog.reservation
    reserved_group = reservation_watchdog.reservation.a_device_groups[0]
    try:
        resource_data = reservation_watchdog.get_resource_data()
        time.sleep(1)
    finally:
        reservation_watchdog.release()


def test_hwmux_create_reservation_without_watchdog(hwmux_api: HwMuxApi):
    label = "iotvalsw-rf-software-regression"
    labels_list = hwmux_api.labels_api.labels_list(name=label)
    assert len(labels_list.results) == 1
    label_to_reserve = labels_list.results[0]
    reservation_request = ReservationRequest(
        r_device_group_labels=[label_to_reserve.id],
        use_watchdog=False,
        metadata={"foo": "bar"},
        details="HWMux example without watchdog",
    )
    reservation_watchdog = hwmux_api.create_reservation_without_watchdog(
        reservation_request, raise_error_if_not_satisfied=True
    )
    try:
        resource_data = reservation_watchdog.get_resource_data()
        time.sleep(1)
    finally:
        reservation_watchdog.release()


def test_hwmux_create_reservation_exceptions(hwmux_api: HwMuxApi):
    label = "iotvalsw-rf-software-regression"
    labels_list = hwmux_api.labels_api.labels_list(name=label)
    assert len(labels_list.results) == 1
    label_to_reserve = labels_list.results[0]
    reservation_request = ReservationRequest(
        r_device_group_labels=[label_to_reserve.id],
        use_watchdog=True,
        metadata={"foo": "bar"},
        details="HWMux example",
    )
    reservation_watchdog = hwmux_api.create_reservation(
        reservation_request, raise_error_if_not_satisfied=True
    )
    try:
        reserved_group_id = reservation_watchdog.reservation.a_device_groups[0]
        reservation_request = ReservationRequest(
            r_device_groups=[reserved_group_id],
            use_watchdog=True,
            metadata={"foo": "bar"},
            details="HWMux example 2",
        )
        with pytest.raises(ReservationNotSatisfiedException):
            hwmux_api.create_reservation(
                reservation_request,
                raise_error_if_not_satisfied=True,
                max_wait_time_sec_if_raise_error_if_not_satisfied=5,
            )
    finally:
        reservation_watchdog.release()


@pytest.mark.anyio
async def test_hwmux_create_reservation_async(hwmux_api_async: HwMuxApiAsync):
    label = "iotvalsw-rf-software-regression"
    labels_list = await hwmux_api_async.labels_api.labels_list(name=label)
    assert len(labels_list.results) == 1
    label_to_reserve = labels_list.results[0]
    reservation_request = ReservationRequest(
        r_device_group_labels=[label_to_reserve.id],
        use_watchdog=True,
        metadata={"foo": "bar"},
        details="HWMux example with watchdog async",
    )
    reservation_watchdog = await hwmux_api_async.create_reservation(
        reservation_request, raise_error_if_not_satisfied=True
    )
    await asyncio.sleep(1)
    await reservation_watchdog.release()


@pytest.mark.anyio
async def test_hwmux_create_reservation_async_exceptions(
    hwmux_api_async: HwMuxApiAsync,
):
    label = "iotvalsw-rf-software-regression"
    labels_list = await hwmux_api_async.labels_api.labels_list(name=label)
    assert len(labels_list.results) == 1
    label_to_reserve = labels_list.results[0]
    reservation_request = ReservationRequest(
        r_device_group_labels=[label_to_reserve.id],
        use_watchdog=True,
        metadata={"foo": "bar"},
        details="HWMux example",
    )
    reservation_watchdog = await hwmux_api_async.create_reservation(
        reservation_request, raise_error_if_not_satisfied=True
    )
    try:
        reserved_group_id = reservation_watchdog.reservation.a_device_groups[0]
        reservation_request = ReservationRequest(
            r_device_groups=[reserved_group_id],
            use_watchdog=True,
            metadata={"foo": "bar"},
            details="HWMux example 2",
        )
        with pytest.raises(ReservationNotSatisfiedException):
            await hwmux_api_async.create_reservation(
                reservation_request,
                raise_error_if_not_satisfied=True,
                max_wait_time_sec_if_raise_error_if_not_satisfied=5,
            )
    finally:
        await reservation_watchdog.release()
