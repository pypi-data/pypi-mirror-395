"""
Integration tests for kinglet.pagination module

These tests involve complex async query building and real ORM interactions
that require actual query builder objects rather than mocking.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock

from kinglet.pagination import PaginationMixin, PaginatedResult, PaginationConfig, Paginator, paginate_queryset


class TestPaginationWithRealQueryBuilder:
    """Integration tests for pagination with actual query builder patterns"""

    @pytest.mark.asyncio
    async def test_pagination_mixin_real_workflow(self):
        """Test PaginationMixin with realistic query builder simulation"""
        
        class MockQueryBuilder(PaginationMixin):
            """Simulate a real ORM query builder"""
            
            def __init__(self, items=None):
                super().__init__()
                self.items = items or list(range(1, 101))  # 100 items
                self._limit_val = None
                self._offset_val = 0
                
            def _clone_for_count(self):
                # Return a clone for count queries
                clone = MockQueryBuilder(self.items)
                return clone
                
            def limit(self, limit_val):
                """Limit method that returns self for chaining"""
                self._limit_val = limit_val
                return self
                
            def offset(self, offset_val):
                """Offset method that returns self for chaining"""
                self._offset_val = offset_val
                return self
                
            async def all(self):
                """Get paginated results"""
                start = self._offset_val
                end = start + (self._limit_val or 20)
                return self.items[start:end]
                
            async def count(self):
                """Get total count"""
                return len(self.items)

        # Test pagination
        query_builder = MockQueryBuilder()
        result = await query_builder.paginate(page=2, per_page=10)

        assert isinstance(result, PaginatedResult)
        assert result.page == 2
        assert result.per_page == 10
        assert result.total_count == 100
        assert len(result.items) == 10
        # Should get items 11-20 (second page)
        assert result.items == list(range(11, 21))

    @pytest.mark.asyncio 
    async def test_pagination_mixin_with_custom_config(self):
        """Test PaginationMixin with custom pagination configuration"""
        
        class MockQueryBuilderWithConfig(PaginationMixin):
            def __init__(self):
                super().__init__()
                # Set custom pagination config
                custom_config = PaginationConfig(
                    default_per_page=5, 
                    max_per_page=15
                )
                self._paginator = Paginator(custom_config)
                self.items = list(range(1, 26))  # 25 items
                self._limit_val = None
                self._offset_val = 0
                
            def _clone_for_count(self):
                clone = MockQueryBuilderWithConfig()
                return clone
                
            def limit(self, limit_val):
                self._limit_val = limit_val
                return self
                
            def offset(self, offset_val):
                self._offset_val = offset_val
                return self
                
            async def all(self):
                start = self._offset_val
                end = start + (self._limit_val or 5)
                return self.items[start:end]
                
            async def count(self):
                return len(self.items)

        query_builder = MockQueryBuilderWithConfig()
        result = await query_builder.paginate()  # Use default config

        assert result.per_page == 5  # Custom default page size
        assert result.total_count == 25
        assert len(result.items) == 5
        assert result.items == [1, 2, 3, 4, 5]


class TestQuerysetPaginationIntegration:
    """Integration tests for queryset pagination utilities"""

    async def test_paginate_queryset_with_real_data(self):
        """Test paginate_queryset with realistic data structures"""
        
        # Simulate a large dataset
        all_items = [{"id": i, "name": f"Item {i}"} for i in range(1, 101)]
        
        def mock_queryset(items, limit=None, offset=0):
            """Mock queryset that simulates database slicing"""
            start = offset
            end = start + limit if limit else len(items)
            return items[start:end]
        
        # Mock query builder with realistic behavior
        query_builder = MagicMock()
        query_builder.limit = MagicMock(return_value=query_builder)
        query_builder.offset = MagicMock(return_value=query_builder)
        
        # Configure mock to return sliced data
        def configure_queryset_result(*args, **kwargs):
            # Extract pagination parameters from mock calls
            limit_calls = [call for call in query_builder.limit.call_args_list]
            offset_calls = [call for call in query_builder.offset.call_args_list]
            
            limit = limit_calls[-1][0][0] if limit_calls else 20
            offset = offset_calls[-1][0][0] if offset_calls else 0
            
            return mock_queryset(all_items, limit, offset)
        
        query_builder.side_effect = configure_queryset_result

        # Test pagination
        result = await paginate_queryset(all_items, page=3, per_page=10)
        
        assert isinstance(result, PaginatedResult)
        assert result.page == 3
        assert result.per_page == 10
        assert result.total_count == 100
        # Third page should have items 21-30
        assert len(result.items) == 10
        assert result.items[0]["id"] == 21
        assert result.items[-1]["id"] == 30

    async def test_paginate_queryset_edge_cases(self):
        """Test pagination edge cases with real data scenarios"""
        
        # Test with fewer items than page size
        small_dataset = [{"id": i} for i in range(1, 8)]  # 7 items
        
        result = await paginate_queryset(small_dataset, page=1, per_page=10)
        
        assert result.total_count == 7
        assert len(result.items) == 7
        assert result.page == 1
        assert result.per_page == 10
        
        # Test last page with partial results
        result_last_page = await paginate_queryset(small_dataset, page=1, per_page=5)
        assert len(result_last_page.items) == 5
        
        result_partial = await paginate_queryset(small_dataset, page=2, per_page=5) 
        assert len(result_partial.items) == 2  # Remaining 2 items


class TestPaginationConfigIntegration:
    """Integration tests for pagination configuration in real scenarios"""

    def test_pagination_config_validation_integration(self):
        """Test pagination config validation with real usage patterns"""
        
        # Test realistic config values
        config = PaginationConfig(
            default_per_page=20,
            max_per_page=100,
            per_page_param="limit",
            page_param="page"
        )
        
        # Test config is properly applied
        assert config.default_per_page == 20
        assert config.max_per_page == 100
        
        # Test with custom mixin using this config
        class ConfiguredMixin(PaginationMixin):
            def __init__(self):
                super().__init__()
                self._paginator = Paginator(config)
        
        mixin = ConfiguredMixin()
        assert mixin._paginator.config.default_per_page == 20
        assert mixin._paginator.config.max_per_page == 100