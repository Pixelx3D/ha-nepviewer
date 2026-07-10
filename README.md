# NEP Viewer

A Home Assistant custom integration for NEP Viewer photovoltaic systems.

## Features

- Cloud login via NEP Viewer account
- Configuration Flow
- Serial Number (SN) configuration
- Automatic token handling
- DataUpdateCoordinator support
- Device support in Home Assistant
- Cloud polling every 60 seconds

## Available Sensors

### Power

- Current Power
- Max Power
- PV Power
- Home Power
- Grid Power

### Energy

- Today
- Yesterday
- Month
- Year
- Total

### Status

- Status
- Last Update
- Alert Code
- Alert Title
- Alert Description

### Environmental

- CO₂ Saved
- Trees
- Car Distance
- Oil Saved

A total of **19 sensors** are currently available.

## Installation

1. Copy the `custom_components/nepviewer` folder to your Home Assistant installation.
2. Restart Home Assistant.
3. Go to **Settings → Devices & Services**.
4. Click **Add Integration**.
5. Search for **NEP Viewer**.

## Configuration

The integration requires:

- Email
- Password
- Serial Number (SN)

## Requirements

- Home Assistant
- NEP Viewer account
- Internet connection

## Current Status

**Version 0.2.0**

Implemented:

- Configuration Flow
- Cloud authentication
- Token handling
- Coordinator
- Device information
- 19 sensors
- English and German translations

## Roadmap

### Version 0.3.0

- Additional inverter information
- Diagnostics
- Options Flow
- Automatic Serial Number detection
- Additional device sensors

## License

MIT License