from unittest import mock

import pytest

from helios_websocket_api import Profile, Helios, HeliosInvalidInputException


@pytest.fixture
def helios():
    client = Helios("127.0.0.1")
    client.set_values = mock.AsyncMock()
    client.fetch_metrics = mock.AsyncMock()
    return client


async def test_set_fan_speed_home(helios: Helios):
    await helios.set_fan_speed(Profile.HOME, 19)

    helios.set_values.assert_called_once_with({"A_CYC_HOME_SPEED_SETTING": 19})


async def test_set_fan_speed_away(helios: Helios):
    await helios.set_fan_speed(Profile.AWAY, 0)

    helios.set_values.assert_called_once_with({"A_CYC_AWAY_SPEED_SETTING": 0})


async def test_set_fan_speed_boost(helios: Helios):
    await helios.set_fan_speed(Profile.BOOST, 100)

    helios.set_values.assert_called_once_with({"A_CYC_BOOST_SPEED_SETTING": 100})


async def test_set_fan_speed_wrong(helios: Helios):
    with pytest.raises(HeliosInvalidInputException):
        await helios.set_fan_speed(Profile.FIREPLACE, 19)


async def test_set_fan_speed_home_invalid_percentage(helios: Helios):
    with pytest.raises(HeliosInvalidInputException):
        await helios.set_fan_speed(Profile.HOME, -1)


async def test_set_fan_speed_home_invalid_percentage2(helios: Helios):
    with pytest.raises(HeliosInvalidInputException):
        await helios.set_fan_speed(Profile.HOME, 101)


async def test_get_fan_speed_for_profile_home(helios: Helios):
    helios.fetch_metrics.return_value = {"A_CYC_HOME_SPEED_SETTING": 19}

    data = await helios.fetch_metric_data()
    assert data.get_fan_speed(Profile.HOME) == 19
    helios.fetch_metrics.assert_called_once()
