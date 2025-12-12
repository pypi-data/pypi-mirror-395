"""
Tests for RateLimitManager class.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from src.github_ioc_scanner.rate_limit_manager import RateLimitManager


class TestRateLimitManager:
    """Test cases for RateLimitManager."""
    
    def test_init(self):
        """Test RateLimitManager initialization."""
        manager = RateLimitManager()
        assert manager.primary_limit_reset is None
        assert manager.secondary_limit_reset is None
        assert manager.last_rate_limit_message is None
        assert manager.message_cooldown == 60
        
        # Test custom cooldown
        manager = RateLimitManager(message_cooldown=120)
        assert manager.message_cooldown == 120
        
    def test_handle_rate_limit_primary(self):
        """Test handling primary rate limit."""
        manager = RateLimitManager()
        reset_time = datetime.now() + timedelta(minutes=5)
        
        manager.handle_rate_limit(reset_time, is_secondary=False)
        
        assert manager.primary_limit_reset == reset_time
        assert manager.secondary_limit_reset is None
        
    def test_handle_rate_limit_secondary(self):
        """Test handling secondary rate limit."""
        manager = RateLimitManager()
        reset_time = datetime.now() + timedelta(minutes=2)
        
        manager.handle_rate_limit(reset_time, is_secondary=True)
        
        assert manager.secondary_limit_reset == reset_time
        assert manager.primary_limit_reset is None
        
    def test_should_show_message_first_time(self):
        """Test that first message should be shown."""
        manager = RateLimitManager()
        
        assert manager.should_show_message() is True
        assert manager.last_rate_limit_message is not None
        
    def test_should_show_message_cooldown(self):
        """Test message cooldown logic."""
        manager = RateLimitManager(message_cooldown=60)
        
        # First message should be shown
        assert manager.should_show_message() is True
        
        # Second message immediately should not be shown
        assert manager.should_show_message() is False
        
        # Mock time to be after cooldown
        future_time = datetime.now() + timedelta(seconds=61)
        with patch('src.github_ioc_scanner.rate_limit_manager.datetime') as mock_datetime:
            mock_datetime.now.return_value = future_time
            assert manager.should_show_message() is True
            
    def test_get_wait_time_no_limits(self):
        """Test wait time when no limits are active."""
        manager = RateLimitManager()
        assert manager.get_wait_time() == 0
        
    def test_get_wait_time_primary_limit(self):
        """Test wait time with primary limit."""
        manager = RateLimitManager()
        reset_time = datetime.now() + timedelta(minutes=5)
        
        manager.handle_rate_limit(reset_time, is_secondary=False)
        
        wait_time = manager.get_wait_time()
        assert 290 <= wait_time <= 300  # Should be around 5 minutes
        
    def test_get_wait_time_secondary_limit(self):
        """Test wait time with secondary limit."""
        manager = RateLimitManager()
        reset_time = datetime.now() + timedelta(minutes=2)
        
        manager.handle_rate_limit(reset_time, is_secondary=True)
        
        wait_time = manager.get_wait_time()
        assert 110 <= wait_time <= 120  # Should be around 2 minutes
        
    def test_get_wait_time_both_limits(self):
        """Test wait time with both limits active."""
        manager = RateLimitManager()
        primary_reset = datetime.now() + timedelta(minutes=5)
        secondary_reset = datetime.now() + timedelta(minutes=2)
        
        manager.handle_rate_limit(primary_reset, is_secondary=False)
        manager.handle_rate_limit(secondary_reset, is_secondary=True)
        
        wait_time = manager.get_wait_time()
        assert 290 <= wait_time <= 300  # Should use the longer wait time
        
    def test_is_rate_limited_no_limits(self):
        """Test rate limit status when no limits are active."""
        manager = RateLimitManager()
        assert manager.is_rate_limited() is False
        
    def test_is_rate_limited_with_limits(self):
        """Test rate limit status with active limits."""
        manager = RateLimitManager()
        reset_time = datetime.now() + timedelta(minutes=5)
        
        manager.handle_rate_limit(reset_time, is_secondary=False)
        assert manager.is_rate_limited() is True
        
    def test_is_rate_limited_expired_limits(self):
        """Test rate limit status with expired limits."""
        manager = RateLimitManager()
        reset_time = datetime.now() - timedelta(minutes=1)  # Past time
        
        manager.handle_rate_limit(reset_time, is_secondary=False)
        assert manager.is_rate_limited() is False
        
    def test_clear_expired_limits(self):
        """Test clearing expired rate limits."""
        manager = RateLimitManager()
        past_time = datetime.now() - timedelta(minutes=1)
        future_time = datetime.now() + timedelta(minutes=1)
        
        manager.handle_rate_limit(past_time, is_secondary=False)
        manager.handle_rate_limit(future_time, is_secondary=True)
        
        manager.clear_expired_limits()
        
        assert manager.primary_limit_reset is None  # Should be cleared
        assert manager.secondary_limit_reset == future_time  # Should remain
        
    def test_get_status_summary(self):
        """Test status summary generation."""
        manager = RateLimitManager()
        
        # No limits
        status = manager.get_status_summary()
        assert status['is_rate_limited'] is False
        assert status['wait_time_seconds'] == 0
        assert status['primary_limit_active'] is False
        assert status['secondary_limit_active'] is False
        
        # With limits
        reset_time = datetime.now() + timedelta(minutes=5)
        manager.handle_rate_limit(reset_time, is_secondary=False)
        
        status = manager.get_status_summary()
        assert status['is_rate_limited'] is True
        assert status['wait_time_seconds'] > 0
        assert status['primary_limit_active'] is True
        assert status['secondary_limit_active'] is False
        assert status['primary_reset_time'] == reset_time