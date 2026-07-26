"""Constants for the NEP Viewer integration."""

from datetime import timedelta

DOMAIN = "nepviewer"

API_BASE = "https://api.nepviewer.net"

LOGIN_ENDPOINT = "/v1/sign-in"

REQUEST_TIMEOUT = 15

SCAN_INTERVAL = timedelta(seconds=60)

CONF_SN = "sn"