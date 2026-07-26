"""Sensor platform for NEP Viewer."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NepViewerDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up NEP Viewer sensors."""

    coordinator: NepViewerDataUpdateCoordinator = hass.data[DOMAIN][
        entry.entry_id
    ]

    async_add_entities(
    [
        # Power
        NepViewerCurrentPowerSensor(coordinator),
        NepViewerMaxPowerSensor(coordinator),
        NepViewerPvPowerSensor(coordinator),
        NepViewerHomePowerSensor(coordinator),
        NepViewerGridPowerSensor(coordinator),

        # Energy
        NepViewerTodayEnergySensor(coordinator),
        NepViewerYesterdayEnergySensor(coordinator),
        NepViewerMonthEnergySensor(coordinator),
        NepViewerYearEnergySensor(coordinator),
        NepViewerTotalEnergySensor(coordinator),

        # Status
        NepViewerStatusSensor(coordinator),
        NepViewerLastUpdateSensor(coordinator),
        NepViewerAlertCodeSensor(coordinator),
        NepViewerAlertTitleSensor(coordinator),
        NepViewerAlertDescriptionSensor(coordinator),

        # Environmental
        NepViewerCo2Sensor(coordinator),
        NepViewerTreeSensor(coordinator),
        NepViewerCarSensor(coordinator),
        NepViewerOilSensor(coordinator),
    ]
)


class NepViewerBaseSensor(
    CoordinatorEntity[NepViewerDataUpdateCoordinator],
    SensorEntity,
):
    """Base class for NEP Viewer sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: NepViewerDataUpdateCoordinator,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, "33d1fb40")},
            manufacturer="Northern Electric Power",
            model="NEP Microinverter",
            name="NEP Viewer",
        )


class NepViewerCurrentPowerSensor(NepViewerBaseSensor):
    """Current power."""

    _attr_name = "Current Power"
    _attr_unique_id = "nepviewer_current_power"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:solar-power"

    @property
    def native_value(self):
        return self.coordinator.data["data"]["totalNow"]


class NepViewerMaxPowerSensor(NepViewerBaseSensor):
    """Maximum power."""

    _attr_name = "Max Power"
    _attr_unique_id = "nepviewer_max_power"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:solar-power"

    @property
    def native_value(self):
        return self.coordinator.data["data"]["maxNow"]


class NepViewerTodayEnergySensor(NepViewerBaseSensor):
    """Today's production."""

    _attr_name = "Today"
    _attr_unique_id = "nepviewer_today"
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_icon = "mdi:calendar-today"

    @property
    def native_value(self):
        return float(self.coordinator.data["data"]["production"]["today"])


class NepViewerYesterdayEnergySensor(NepViewerBaseSensor):
    """Yesterday's production."""

    _attr_name = "Yesterday"
    _attr_unique_id = "nepviewer_yesterday"
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_icon = "mdi:calendar"

    @property
    def native_value(self):
        return float(self.coordinator.data["data"]["production"]["yesterday"])


class NepViewerMonthEnergySensor(NepViewerBaseSensor):
    """Month production."""

    _attr_name = "Month"
    _attr_unique_id = "nepviewer_month"
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_icon = "mdi:calendar-month"

    @property
    def native_value(self):
        return float(self.coordinator.data["data"]["production"]["month"])


class NepViewerYearEnergySensor(NepViewerBaseSensor):
    """Year production."""

    _attr_name = "Year"
    _attr_unique_id = "nepviewer_year"
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_icon = "mdi:calendar-star"

    @property
    def native_value(self):
        return float(self.coordinator.data["data"]["production"]["year"])


class NepViewerTotalEnergySensor(NepViewerBaseSensor):
    """Lifetime production."""

    _attr_name = "Total"
    _attr_unique_id = "nepviewer_total"
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_icon = "mdi:solar-power-variant"

    @property
    def native_value(self):
        return float(self.coordinator.data["data"]["production"]["total"])


class NepViewerStatusSensor(NepViewerBaseSensor):
    """System status."""

    _attr_name = "Status"
    _attr_unique_id = "nepviewer_status"
    _attr_icon = "mdi:connection"

    @property
    def native_value(self):
        return self.coordinator.data["data"]["statusTitle"]


class NepViewerLastUpdateSensor(NepViewerBaseSensor):
    """Last update."""

    _attr_name = "Last Update"
    _attr_unique_id = "nepviewer_last_update"
    _attr_icon = "mdi:update"

    @property
    def native_value(self):
        return self.coordinator.data["data"]["lastUpdate"]
    
class NepViewerPvPowerSensor(NepViewerBaseSensor):
    """PV Power."""

    _attr_name = "PV Power"
    _attr_unique_id = "nepviewer_pv_power"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:solar-panel"

    @property
    def native_value(self):
        """Return PV power."""
        return self.coordinator.data["data"]["energy"]["PVPanel"]["power"]


class NepViewerHomePowerSensor(NepViewerBaseSensor):
    """Home Power."""

    _attr_name = "Home Power"
    _attr_unique_id = "nepviewer_home_power"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:home-lightning-bolt"

    @property
    def native_value(self):
        """Return home power."""
        return self.coordinator.data["data"]["energy"]["home"]["power"]


class NepViewerGridPowerSensor(NepViewerBaseSensor):
    """Grid Power."""

    _attr_name = "Grid Power"
    _attr_unique_id = "nepviewer_grid_power"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:transmission-tower"

    @property
    def native_value(self):
        """Return grid power."""
        return self.coordinator.data["data"]["energy"]["grid"]["power"]
    
class NepViewerCo2Sensor(NepViewerBaseSensor):
    """CO2 savings."""

    _attr_name = "CO2 Saved"
    _attr_unique_id = "nepviewer_co2"
    _attr_native_unit_of_measurement = "kg"
    _attr_icon = "mdi:molecule-co2"

    @property
    def native_value(self):
        """Return CO2 savings."""
        return float(
            self.coordinator.data["data"]["environmentalBenefit"]["co2"]
        )


class NepViewerTreeSensor(NepViewerBaseSensor):
    """Trees equivalent."""

    _attr_name = "Trees"
    _attr_unique_id = "nepviewer_trees"
    _attr_native_unit_of_measurement = "Trees"
    _attr_icon = "mdi:tree"

    @property
    def native_value(self):
        """Return tree equivalent."""
        return float(
            self.coordinator.data["data"]["environmentalBenefit"]["tree"]
        )


class NepViewerCarSensor(NepViewerBaseSensor):
    """Car distance equivalent."""

    _attr_name = "Car Distance"
    _attr_unique_id = "nepviewer_car"
    _attr_native_unit_of_measurement = "km"
    _attr_icon = "mdi:car"

    @property
    def native_value(self):
        """Return car distance equivalent."""
        return float(
            self.coordinator.data["data"]["environmentalBenefit"]["car"]
        )


class NepViewerOilSensor(NepViewerBaseSensor):
    """Oil saved."""

    _attr_name = "Oil Saved"
    _attr_unique_id = "nepviewer_oil"
    _attr_native_unit_of_measurement = "BBL"
    _attr_icon = "mdi:barrel"

    @property
    def native_value(self):
        """Return oil saved."""
        return float(
            self.coordinator.data["data"]["environmentalBenefit"]["oil"]
        )
class NepViewerAlertCodeSensor(NepViewerBaseSensor):
    """Alert code."""

    _attr_name = "Alert Code"
    _attr_unique_id = "nepviewer_alert_code"
    _attr_icon = "mdi:alert-circle-outline"

    @property
    def native_value(self):
        """Return alert code."""
        return self.coordinator.data["data"]["alertCode"]


class NepViewerAlertTitleSensor(NepViewerBaseSensor):
    """Alert title."""

    _attr_name = "Alert Title"
    _attr_unique_id = "nepviewer_alert_title"
    _attr_icon = "mdi:alert-circle"

    @property
    def native_value(self):
        """Return alert title."""
        return self.coordinator.data["data"]["alertTitle"]


class NepViewerAlertDescriptionSensor(NepViewerBaseSensor):
    """Alert description."""

    _attr_name = "Alert Description"
    _attr_unique_id = "nepviewer_alert_description"
    _attr_icon = "mdi:text-box-outline"

    @property
    def native_value(self):
        """Return alert description."""
        return self.coordinator.data["data"]["alertDescription"]