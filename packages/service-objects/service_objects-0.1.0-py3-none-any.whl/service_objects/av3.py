"""
Service Objects, Inc.

AV3 client for validating and standardizing US addresses
using Service Objects AV3 API. Handles production/trial/backup
endpoints, fallback logic, and JSON parsing.
"""

from __future__ import annotations
from typing import Any
from .base import BaseClient
import requests

class AV3(BaseClient):
    _ENDPOINTS = {
        "production": "https://sws.serviceobjects.com/AV3/api.svc",
        "backup":     "https://swsbackup.serviceobjects.com/AV3/api.svc",
        "trial":      "https://trial.serviceobjects.com/AV3/api.svc",
    }

    def __init__(self, *, license_key: str, environment: str = "production", **kwargs):
        if environment not in self._ENDPOINTS:
            raise ValueError(f"Unknown environment: {environment}")

        self.environment = environment
        self.primary_url = self._ENDPOINTS[environment]
        self.backup_url = (
            self._ENDPOINTS["backup"]
            if environment == "production"
            else None
        )

        super().__init__(
            base_url=self.primary_url,
            license_key=license_key,
            **kwargs
        )

    def _request_with_fallback(
        self,
        *,
        path: str,
        params: dict[str, Any],
    ) -> dict:
        try:
            data = self._request(path=path, params=params)

            if self.environment == "production" and data.get("Error"):
                type_code = (data["Error"] or {}).get("TypeCode")
                if type_code == "3" and self.backup_url:
                    data = self._request_direct(self.backup_url, path, params)

            return data

        except requests.RequestException as e:
            if self.environment == "production" and self.backup_url:
                data = self._request_direct(self.backup_url, path, params)
                if data.get("Error"):
                    raise RuntimeError(f"AV3 backup error: {data['Error']}") from e
                return data

            raise RuntimeError(f"AV3 {self.environment} error: {str(e)}") from e

    def _request_direct(self, base_url: str, path: str, params: dict[str, Any]) -> dict:
        p = dict(params)
        p["LicenseKey"] = self.license_key
        url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
        resp = self.session.get(url, params=p, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def GetBestMatches(
        self,
        *,
        business_name: str = "",
        address: str,
        address_2: str = "",
        city: str = "",
        state: str = "",
        postal_code: str = "",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """
        Validate and standardize a US address using AV3.

        Args:
            business_name: Company name to assist suite parsing.
            address: Primary street address (e.g., "123 Main St"). Required.
            address_2: Secondary address information (e.g., "Apt 4B", "C/O John Smith").
            city: City name. Required if postal_code is not provided.
            state: State code or full name. Required if postal_code is not provided.
            postal_code: 5- or 9-digit ZIP. Required if city/state are not provided.
            **extra_params: Additional AV3 query parameters.

        Returns:
            Parsed JSON response containing address candidates, corrections, or an error payload.

        Raises:
            RuntimeError: If the service returns an error payload or all endpoints are unreachable.
        """
        params = {
            "BusinessName": business_name,
            "Address": address,
            "Address2": address_2,
            "City": city,
            "State": state,
            "PostalCode": postal_code,
            **extra_params,
        }

        return self._request_with_fallback(
            path="GetBestMatchesJson",
            params=params,
        )

    def GetBestMatchesSingleLine(
        self,
        *,
        business_name: str = "",
        address: str,
        **extra_params: Any,
    ) -> dict[str, Any]:
        """
        Validate and standardize a single-line US address using AV3.

        Args:
            business_name: Company name to assist suite parsing.
            address: Full address in one line (e.g., "123 Main St, Anytown CA 99999").
            **extra_params: Additional AV3 query parameters.

        Returns:
            Parsed JSON response containing the best match candidate or an error payload.

        Raises:
            RuntimeError: If the service returns an error payload or all endpoints are unreachable.
        """

        params = {
            "BusinessName": business_name,
            "Address": address,
            **extra_params,
        }

        return self._request_with_fallback(
            path="GetBestMatchesSingleLineJson",
            params=params,
        )
    
    def ValidateCityStateZip(
        self,
        *,
        city: str = "",
        state: str = "",
        zip: str = "",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """
        Validate a City/State/ZIP combination using AV3.

        Args:
            city: City name. Required if postal_code is not provided.
            state: State code or full name. Required if postal_code is not provided.
            zip: 5- or 9-digit ZIP. Required if city/state are not provided.
            **extra_params: Additional AV3 query parameters.

        Returns:
            Parsed JSON response containing location validation results or an error payload.

        Raises:
            RuntimeError: If the service returns an error payload or all endpoints are unreachable.
        """
        params = {
            "City": city,
            "State": state,
            "ZIP": zip,
            **extra_params,
        }

        return self._request_with_fallback(
            path="ValidateCityStateZipJson",
            params=params,
        )
    
    def GetSecondaryNumbers(
        self,
        *,
        address: str,
        city: str = "",
        state: str = "",
        postal_code: str = "",
        **extra_params: Any,
    ) -> dict[str, Any]:
        """
        Retrieve potential secondary numbers (unit/suite) for a U.S. address using AV3.

        This operation complements GetBestMatches by returning plausible secondary numbers
        when the input address is missing or has incorrect unit information.

        Args:
            address: Primary street address (e.g., "123 Main St"). Required.
            city: City name. Required if postal_code is not provided.
            state: State code or full name. Required if postal_code is not provided.
            postal_code: 5- or 9-digit ZIP. Required if city/state are not provided.
            **extra_params: Additional AV3 query parameters.

        Returns:
            Parsed JSON response containing validated address elements and a list of
            possible secondary numbers, or an error payload.

        Raises:
            RuntimeError: If the service returns an error payload or all endpoints are unreachable.
        """
        params = {
            "Address": address,
            "City": city,
            "State": state,
            "PostalCode": postal_code,
            **extra_params,
        }

        return self._request_with_fallback(
            path="GetSecondaryNumbersJson",
            params=params,
        )