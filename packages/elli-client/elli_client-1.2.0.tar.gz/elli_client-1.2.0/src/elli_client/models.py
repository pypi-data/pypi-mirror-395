"""Data models for Elli API"""

from typing import Optional

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """OAuth2 token response from Elli API."""

    access_token: str  # JWT access token for API authentication
    refresh_token: str  # Refresh token for obtaining new access tokens
    id_token: str  # OpenID Connect ID token
    token_type: str  # Token type (usually "Bearer")
    expires_in: int  # Token expiration time in seconds
    scope: str  # Granted OAuth2 scopes


class ChargingSession(BaseModel):
    """Charging session data from Elli API."""

    id: str
    station_id: str
    start_date_time: str

    # Energy and power data
    energy_consumption_wh: Optional[int] = None
    momentary_charging_speed_watts: Optional[int] = None

    # Session state
    lifecycle_state: Optional[str] = None
    charging_state: Optional[str] = None

    # Authentication and authorization
    connector_id: Optional[int] = None
    authentication_method: Optional[str] = None
    authorization_mode: Optional[str] = None
    rfid_card_id: Optional[str] = None
    rfid_card_serial_number: Optional[str] = None

    # Timestamps
    end_date_time: Optional[str] = None
    last_updated: Optional[str] = None


class FirmwareInfo(BaseModel):
    """Firmware information for a station."""

    id: str
    version: str
    release_notes_link: Optional[str] = None


class Station(BaseModel):
    """Charging station information."""

    id: str  # Unique station identifier
    name: str  # Station name
    serial_number: Optional[str] = None  # Hardware serial number
    model: Optional[str] = None  # Station model (e.g., "Elli Wallbox Pro")
    firmware_version: Optional[str] = None  # Current firmware version
    installed_firmware: Optional[FirmwareInfo] = None  # Detailed firmware info


class RFIDCard(BaseModel):
    """RFID card information."""

    id: str  # Unique card identifier
    number: str  # Card number (e.g., "ELLI-XXXXXXXX-XXXX-X")
    brand_id: Optional[int] = None  # Brand identifier
    created_at: Optional[str] = None  # Creation timestamp
    design_template: Optional[int] = None  # Design template ID
    public_charging: Optional[bool] = None  # Public charging enabled flag
    status: Optional[str] = None  # Card status (e.g., "active")
    subscriber_id: Optional[str] = None  # Subscriber identifier
    tenant_id: Optional[str] = None  # Tenant identifier
    tenant_name: Optional[str] = None  # Tenant name (e.g., "Elli")
    updated_at: Optional[str] = None  # Last update timestamp
