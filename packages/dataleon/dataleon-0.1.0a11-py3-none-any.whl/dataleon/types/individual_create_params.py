# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

__all__ = ["IndividualCreateParams", "Person", "TechnicalData"]


class IndividualCreateParams(TypedDict, total=False):
    workspace_id: Required[str]
    """Unique identifier of the workspace where the individual is being registered."""

    person: Person
    """Personal information about the individual."""

    source_id: str
    """
    Optional identifier for tracking the source system or integration from your
    system.
    """

    technical_data: TechnicalData
    """Technical metadata related to the request or processing."""


class Person(TypedDict, total=False):
    birthday: str
    """Date of birth in DD/MM/YYYY format."""

    email: str
    """Email address of the individual."""

    first_name: str
    """First name of the individual."""

    gender: Literal["M", "F"]
    """Gender of the individual (M for male, F for female)."""

    last_name: str
    """Last name (family name) of the individual."""

    maiden_name: str
    """Maiden name, if applicable."""

    nationality: str
    """Nationality of the individual (ISO 3166-1 alpha-3 country code)."""

    phone_number: str
    """Phone number of the individual."""


class TechnicalData(TypedDict, total=False):
    active_aml_suspicions: bool
    """
    Flag indicating whether there are active research AML (Anti-Money Laundering)
    suspicions for the individual when you apply for a new entry or get an existing
    one.
    """

    callback_url: str
    """URL to call back upon completion of processing."""

    callback_url_notification: str
    """URL for receive notifications about the processing state or status."""

    filtering_score_aml_suspicions: float
    """Minimum filtering score (between 0 and 1) for AML suspicions to be considered."""

    language: str
    """Preferred language for communication (e.g., "eng", "fra")."""

    portal_steps: List[Literal["identity_verification", "document_signing", "proof_of_address", "selfie", "face_match"]]
    """List of steps to include in the portal workflow."""

    raw_data: bool
    """Flag indicating whether to include raw data in the response."""
