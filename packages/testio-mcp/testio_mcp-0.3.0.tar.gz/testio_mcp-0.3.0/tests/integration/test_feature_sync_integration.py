"""Integration tests for FeatureRepository with real TestIO API.

Tests validate section-aware sync with real products from TESTIO_PRODUCT_ID/TESTIO_PRODUCT_IDS.

IMPORTANT: Features are SHARED across sections within a product.
The repository deduplicates features when syncing section products.

NOTE: Section-specific tests are skipped as they require specific product configurations.
"""

import pytest
from sqlmodel import select

from testio_mcp.exceptions import TestIOAPIError
from testio_mcp.models.orm import Feature
from testio_mcp.repositories.feature_repository import FeatureRepository


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sync_features_basic(shared_cache, shared_client, test_product_id):
    """Integration test: Sync features for test product."""
    async with shared_cache.async_session_maker() as session:
        repo = FeatureRepository(
            session=session, client=shared_client, customer_id=shared_cache.customer_id
        )

        # Sync features
        try:
            stats = await repo.sync_features(product_id=test_product_id)
        except TestIOAPIError as e:
            if e.status_code in {404, 403}:
                pytest.skip(f"Product {test_product_id} not accessible (HTTP {e.status_code})")
            raise

        # Verify sync
        assert stats["total"] > 0, f"Product {test_product_id} should have at least one feature"
        assert stats["created"] > 0

        # Verify database
        result = await session.exec(select(Feature).where(Feature.product_id == test_product_id))
        features = result.all()
        assert len(features) > 0
        assert all(f.title for f in features)  # All have titles


@pytest.mark.integration
@pytest.mark.skip(reason="Requires section-specific product configuration (hardcoded CANVA)")
@pytest.mark.asyncio
async def test_sync_features_canva_section(shared_cache, shared_client):
    """Integration test: Sync features for section product.

    SKIPPED: This test requires specific section product IDs which are
    environment-specific. Needs refactoring to work with arbitrary test products.
    """
    pytest.skip("Requires section-specific product configuration")


@pytest.mark.integration
@pytest.mark.skip(reason="Requires section-specific product configuration (hardcoded REMOVEBG)")
@pytest.mark.asyncio
async def test_sync_features_removebg_single_section(shared_cache, shared_client):
    """Integration test: Sync features for single-section product.

    SKIPPED: This test requires specific section product IDs which are
    environment-specific. Needs refactoring to work with arbitrary test products.
    """
    pytest.skip("Requires section-specific product configuration")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_features_for_product_query(shared_cache, shared_client, test_product_id):
    """Integration test: Query features after sync."""
    async with shared_cache.async_session_maker() as session:
        repo = FeatureRepository(
            session=session, client=shared_client, customer_id=shared_cache.customer_id
        )

        # Sync features first
        try:
            await repo.sync_features(product_id=test_product_id)
        except TestIOAPIError as e:
            if e.status_code in {404, 403}:
                pytest.skip(f"Product {test_product_id} not accessible (HTTP {e.status_code})")
            raise

        # Query all features
        features = await repo.get_features_for_product(product_id=test_product_id)
        assert len(features) > 0, f"Product {test_product_id} should have features after sync"
        assert all(isinstance(f, Feature) for f in features)
        assert all(f.product_id == test_product_id for f in features)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_upsert_behavior_integration(shared_cache, shared_client, test_product_id):
    """Integration test: Verify upsert behavior (second sync updates, doesn't duplicate).

    The key assertion is that second sync shows 0 created (no duplicates).
    """
    async with shared_cache.async_session_maker() as session:
        repo = FeatureRepository(
            session=session, client=shared_client, customer_id=shared_cache.customer_id
        )

        # First sync (may create or update depending on test order)
        try:
            stats1 = await repo.sync_features(product_id=test_product_id)
        except TestIOAPIError as e:
            if e.status_code in {404, 403}:
                pytest.skip(f"Product {test_product_id} not accessible (HTTP {e.status_code})")
            raise

        total_features = stats1["total"]

        # Second sync - should update all, create none (tests no duplicates)
        stats2 = await repo.sync_features(product_id=test_product_id)
        assert stats2["created"] == 0  # No new features created
        assert stats2["updated"] == total_features  # All existing features updated
        assert stats2["total"] == total_features  # Same total count
