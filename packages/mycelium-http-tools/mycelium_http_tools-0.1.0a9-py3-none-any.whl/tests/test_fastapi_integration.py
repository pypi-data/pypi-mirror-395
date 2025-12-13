"""
Integration tests for FastAPI middleware and dependencies.

These tests only run if FastAPI is available and test the actual integration
with FastAPI dependency injection and middleware.
"""

from pathlib import Path
from uuid import UUID

import pytest

from myc_http_tools.functions import decode_and_decompress_profile_from_base64
from myc_http_tools.models.profile import Profile

# Try to import FastAPI dependencies
try:
    from fastapi import FastAPI, Depends, Request
    from fastapi.testclient import TestClient
    from starlette.middleware.base import BaseHTTPMiddleware
    from myc_http_tools.fastapi.middleware import (
        get_profile_from_header,
        get_profile_from_header_required,
        profile_middleware,
    )

    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    # Define placeholders to avoid import errors
    FastAPI = None  # type: ignore[assignment, misc]
    Depends = None  # type: ignore[assignment, misc]
    BaseHTTPMiddleware = None  # type: ignore[assignment, misc]
    TestClient = None  # type: ignore[assignment, misc]
    get_profile_from_header = None  # type: ignore[assignment, misc]
    get_profile_from_header_required = None  # type: ignore[assignment, misc]
    profile_middleware = None  # type: ignore[assignment, misc]


def _load_large_profile_encoded() -> str:
    """Load large profile from encoded file."""
    mock_path = Path(__file__).parent / "mock" / "large-profile-encoded.txt"
    with open(mock_path, "r", encoding="utf-8") as f:
        return f.read().strip()


@pytest.mark.skipif(not FASTAPI_AVAILABLE, reason="FastAPI is not available")
class TestFastAPIIntegration:
    """Integration tests for FastAPI middleware and dependencies"""

    def test_get_profile_from_header_optional_with_encoded_profile(self):
        """Test get_profile_from_header dependency with encoded profile"""
        app = FastAPI()
        encoded_profile = _load_large_profile_encoded()

        @app.get("/test")
        async def test_route(
            profile: Profile | None = Depends(get_profile_from_header),
        ):
            if profile is None:
                return {"error": "Profile is None"}
            return {
                "has_licensed_resources": profile.licensed_resources
                is not None,
                "licensed_resources_count": (
                    len(profile.licensed_resources.records)
                    if profile.licensed_resources
                    and profile.licensed_resources.records
                    else 0
                ),
            }

        client = TestClient(app)
        response = client.get(
            "/test", headers={"x-mycelium-profile": encoded_profile}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["has_licensed_resources"] is True
        assert data["licensed_resources_count"] > 0

    def test_get_profile_from_header_required_with_encoded_profile(self):
        """Test get_profile_from_header_required dependency with encoded profile"""
        app = FastAPI()
        encoded_profile = _load_large_profile_encoded()

        @app.get("/test")
        async def test_route(
            profile: Profile = Depends(get_profile_from_header_required),
        ):
            return {
                "has_licensed_resources": profile.licensed_resources
                is not None,
                "licensed_resources_count": (
                    len(profile.licensed_resources.records)
                    if profile.licensed_resources
                    and profile.licensed_resources.records
                    else 0
                ),
            }

        client = TestClient(app)
        response = client.get(
            "/test", headers={"x-mycelium-profile": encoded_profile}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["has_licensed_resources"] is True
        assert data["licensed_resources_count"] > 0

    def test_profile_middleware_with_encoded_profile(self):
        """Test profile_middleware with encoded profile"""
        app = FastAPI()
        encoded_profile = _load_large_profile_encoded()

        app.add_middleware(BaseHTTPMiddleware, dispatch=profile_middleware)

        @app.get("/test")
        async def test_route(request: Request):
            profile = request.state.profile
            if profile is None:
                return {"error": "Profile is None"}
            return {
                "has_licensed_resources": profile.licensed_resources
                is not None,
                "licensed_resources_count": (
                    len(profile.licensed_resources.records)
                    if profile.licensed_resources
                    and profile.licensed_resources.records
                    else 0
                ),
            }

        client = TestClient(app)
        response = client.get(
            "/test", headers={"x-mycelium-profile": encoded_profile}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["has_licensed_resources"] is True
        assert data["licensed_resources_count"] > 0

    def test_profile_licensed_resources_preserved_after_chained_filtering_in_fastapi(
        self,
    ):
        """Test that licensed_resources is preserved after chained filtering in FastAPI context.

        This test simulates the exact scenario: FastAPI dependency injection followed by
        chained filtering, then passing to another method.
        """
        app = FastAPI()
        encoded_profile = _load_large_profile_encoded()

        # Decode profile to get customer_id and tenant_id
        profile = decode_and_decompress_profile_from_base64(encoded_profile)
        profile.is_staff = False
        profile.is_manager = False

        # Select the first record with role "customer"
        if (
            profile.licensed_resources is None
            or profile.licensed_resources.records is None
        ):
            raise ValueError("licensed_resources or records is None")
        customer_record = next(
            record
            for record in profile.licensed_resources.records
            if record.role == "customer"
        )
        customer_id = customer_record.acc_id
        tenant_id = customer_record.tenant_id
        global_roles = ["admin", "user", "customer"]

        # Simulate passing to another method/class
        class MockService:
            def process_profile(self, profile: Profile) -> Profile:
                if profile.licensed_resources is None:
                    raise ValueError("licensed_resources is None!")
                return profile

        @app.get("/test")
        async def test_route(
            profile: Profile = Depends(get_profile_from_header_required),
        ):
            # Apply chained filtering (like in test_chained_methods_with_encoded_profile)
            filtered_profile = (
                profile.on_account(customer_id)
                .on_tenant(tenant_id)
                .with_read_access()
                .with_roles(global_roles)
            )

            # Verify filtered profile has licensed_resources
            if filtered_profile.licensed_resources is None:
                return {
                    "error": "licensed_resources is None after chained filtering",
                    "has_licensed_resources": False,
                }

            service = MockService()
            processed_profile = service.process_profile(filtered_profile)

            return {
                "has_licensed_resources": processed_profile.licensed_resources
                is not None,
                "licensed_resources_count": (
                    len(processed_profile.licensed_resources.records)
                    if processed_profile.licensed_resources
                    and processed_profile.licensed_resources.records
                    else 0
                ),
                "filtering_state": processed_profile.filtering_state,
            }

        client = TestClient(app)
        response = client.get(
            "/test", headers={"x-mycelium-profile": encoded_profile}
        )

        assert response.status_code == 200
        data = response.json()
        assert "error" not in data, f"Error in response: {data.get('error')}"
        assert (
            data["has_licensed_resources"] is True
        ), "licensed_resources should not be None after chained filtering in FastAPI"
        assert (
            data["licensed_resources_count"] > 0
        ), "licensed_resources.records should have records after chained filtering in FastAPI"
        assert data["filtering_state"] is not None

    def test_profile_licensed_resources_preserved_after_model_copy_deep_and_validation(
        self,
    ):
        """Test that licensed_resources is preserved after model_copy(deep=True) and validate_read_access.

        This test reproduces the exact scenario from metadata.py where:
        1. Profile comes from FastAPI dependency injection
        2. profile.model_copy(deep=True) is called
        3. The copy is passed to validate_read_access which calls on_account, on_tenant, etc.
        4. licensed_resources should remain populated throughout
        """
        app = FastAPI()
        encoded_profile = _load_large_profile_encoded()

        # Decode profile to get customer_id and tenant_id
        profile = decode_and_decompress_profile_from_base64(encoded_profile)
        profile.is_staff = False
        profile.is_manager = False

        # Select the first record with role "customer"
        if (
            profile.licensed_resources is None
            or profile.licensed_resources.records is None
        ):
            raise ValueError("licensed_resources or records is None")
        customer_record = next(
            record
            for record in profile.licensed_resources.records
            if record.role == "customer"
        )
        customer_id = customer_record.acc_id
        tenant_id = customer_record.tenant_id

        @app.get("/test")
        async def test_route(
            profile: Profile = Depends(get_profile_from_header_required),
        ):
            # Simulate the exact scenario from metadata.py
            # Step 1: Verify profile has licensed_resources
            if profile.licensed_resources is None:
                return {
                    "error": "licensed_resources is None before model_copy",
                    "has_licensed_resources": False,
                }

            # Step 2: Make a deep copy (as in metadata.py line 85)
            profile_copy = profile.model_copy(deep=True)

            # Step 3: Verify copy has licensed_resources
            if profile_copy.licensed_resources is None:
                return {
                    "error": "licensed_resources is None after model_copy(deep=True)",
                    "has_licensed_resources": False,
                }

            # Debug: Verify to_licenses_vector works after deep copy
            all_resources = profile_copy.licensed_resources.to_licenses_vector()
            if not all_resources:
                return {
                    "error": "to_licenses_vector returned empty list after model_copy(deep=True)",
                    "has_licensed_resources": False,
                    "records_count": (
                        len(profile_copy.licensed_resources.records)
                        if profile_copy.licensed_resources.records
                        else 0
                    ),
                }

            # Step 4: Simulate validate_read_access (convert string to UUID as in metadata.py)
            customer_id_uuid = UUID(str(customer_id))
            tenant_id_uuid = UUID(str(tenant_id)) if tenant_id else None

            # Debug: Check if account_id exists in resources before filtering
            matching_resources = [
                resource
                for resource in all_resources
                if resource.acc_id == customer_id_uuid
            ]
            if not matching_resources:
                return {
                    "error": f"No resources found matching account_id {customer_id_uuid}",
                    "has_licensed_resources": False,
                    "available_account_ids": [
                        str(r.acc_id) for r in all_resources[:5]
                    ],  # First 5 for debugging
                }

            # Apply the same filtering chain as validate_read_access
            base_profile = profile_copy.on_account(customer_id_uuid)

            # Debug: Check if licensed_resources is None after on_account
            if base_profile.licensed_resources is None:
                return {
                    "error": "licensed_resources is None after on_account",
                    "has_licensed_resources": False,
                    "matching_resources_count": len(matching_resources),
                }

            filtered_profile = (
                (
                    base_profile.on_tenant(tenant_id_uuid)
                    if tenant_id_uuid is not None
                    else base_profile
                )
                .with_read_access()
                .with_roles(["customer", "results-expert"])
            )

            # Step 5: Verify filtered profile still has licensed_resources
            if filtered_profile.licensed_resources is None:
                return {
                    "error": "licensed_resources is None after filtering chain",
                    "has_licensed_resources": False,
                }

            return {
                "has_licensed_resources": filtered_profile.licensed_resources
                is not None,
                "licensed_resources_count": (
                    len(filtered_profile.licensed_resources.records)
                    if filtered_profile.licensed_resources
                    and filtered_profile.licensed_resources.records
                    else 0
                ),
                "filtering_state": filtered_profile.filtering_state,
            }

        client = TestClient(app)
        response = client.get(
            "/test", headers={"x-mycelium-profile": encoded_profile}
        )

        assert response.status_code == 200
        data = response.json()
        assert "error" not in data, f"Error in response: {data.get('error')}"
        assert (
            data["has_licensed_resources"] is True
        ), "licensed_resources should not be None after model_copy(deep=True) and filtering"
        assert (
            data["licensed_resources_count"] > 0
        ), "licensed_resources.records should have records after model_copy(deep=True) and filtering"
        assert data["filtering_state"] is not None

    def test_profile_licensed_resources_preserved_through_multiple_dependencies(
        self,
    ):
        """Test that licensed_resources is preserved when Profile passes through multiple dependencies"""
        app = FastAPI()
        encoded_profile = _load_large_profile_encoded()

        def get_customer_id(
            profile: Profile = Depends(get_profile_from_header_required),
        ) -> UUID:
            """Dependency that extracts customer_id from profile"""
            if (
                profile.licensed_resources is None
                or profile.licensed_resources.records is None
            ):
                raise ValueError(
                    "licensed_resources is None in get_customer_id"
                )
            # Select the first record with role "customer"
            customer_record = next(
                record
                for record in profile.licensed_resources.records
                if record.role == "customer"
            )
            return customer_record.acc_id

        def get_tenant_id(
            profile: Profile = Depends(get_profile_from_header_required),
        ) -> UUID:
            """Dependency that extracts tenant_id from profile"""
            if (
                profile.licensed_resources is None
                or profile.licensed_resources.records is None
            ):
                raise ValueError("licensed_resources is None in get_tenant_id")
            # Select the first record with role "customer"
            customer_record = next(
                record
                for record in profile.licensed_resources.records
                if record.role == "customer"
            )
            return customer_record.tenant_id

        @app.get("/test")
        async def test_route(
            profile: Profile = Depends(get_profile_from_header_required),
            customer_id: UUID = Depends(get_customer_id),
            tenant_id: UUID = Depends(get_tenant_id),
        ):
            # Verify profile still has licensed_resources after multiple dependencies
            if profile.licensed_resources is None:
                return {
                    "error": "licensed_resources is None after multiple dependencies",
                    "has_licensed_resources": False,
                }

            # Apply chained filtering
            global_roles = ["admin", "user", "customer"]
            filtered_profile = (
                profile.on_account(customer_id)
                .on_tenant(tenant_id)
                .with_read_access()
                .with_roles(global_roles)
            )

            return {
                "has_licensed_resources": filtered_profile.licensed_resources
                is not None,
                "licensed_resources_count": (
                    len(filtered_profile.licensed_resources.records)
                    if filtered_profile.licensed_resources
                    and filtered_profile.licensed_resources.records
                    else 0
                ),
            }

        client = TestClient(app)
        response = client.get(
            "/test", headers={"x-mycelium-profile": encoded_profile}
        )

        assert response.status_code == 200
        data = response.json()
        assert "error" not in data, f"Error in response: {data.get('error')}"
        assert (
            data["has_licensed_resources"] is True
        ), "licensed_resources should not be None after multiple dependencies"
        assert (
            data["licensed_resources_count"] > 0
        ), "licensed_resources.records should have records after multiple dependencies"

    def test_profile_licensed_resources_preserved_with_middleware_and_dependency(
        self,
    ):
        """Test that licensed_resources is preserved when using both middleware and dependency"""
        app = FastAPI()
        encoded_profile = _load_large_profile_encoded()

        app.add_middleware(BaseHTTPMiddleware, dispatch=profile_middleware)

        @app.get("/test")
        async def test_route(
            request: Request,
            profile_from_dep: Profile = Depends(
                get_profile_from_header_required
            ),
        ):
            # Get profile from middleware
            profile_from_middleware = request.state.profile

            # Verify both profiles have licensed_resources
            if profile_from_middleware is None:
                return {"error": "Profile from middleware is None"}

            if profile_from_dep.licensed_resources is None:
                return {
                    "error": "licensed_resources is None in dependency profile"
                }

            if profile_from_middleware.licensed_resources is None:
                return {
                    "error": "licensed_resources is None in middleware profile"
                }

            return {
                "middleware_has_licensed_resources": (
                    profile_from_middleware.licensed_resources is not None
                ),
                "dependency_has_licensed_resources": (
                    profile_from_dep.licensed_resources is not None
                ),
                "middleware_licensed_resources_count": (
                    len(profile_from_middleware.licensed_resources.records)
                    if profile_from_middleware.licensed_resources
                    and profile_from_middleware.licensed_resources.records
                    else 0
                ),
                "dependency_licensed_resources_count": (
                    len(profile_from_dep.licensed_resources.records)
                    if profile_from_dep.licensed_resources
                    and profile_from_dep.licensed_resources.records
                    else 0
                ),
            }

        client = TestClient(app)
        response = client.get(
            "/test", headers={"x-mycelium-profile": encoded_profile}
        )

        assert response.status_code == 200
        data = response.json()
        assert "error" not in data, f"Error in response: {data.get('error')}"
        assert (
            data["middleware_has_licensed_resources"] is True
        ), "licensed_resources should not be None in middleware profile"
        assert (
            data["dependency_has_licensed_resources"] is True
        ), "licensed_resources should not be None in dependency profile"
        assert (
            data["middleware_licensed_resources_count"] > 0
        ), "middleware profile should have licensed_resources records"
        assert (
            data["dependency_licensed_resources_count"] > 0
        ), "dependency profile should have licensed_resources records"
