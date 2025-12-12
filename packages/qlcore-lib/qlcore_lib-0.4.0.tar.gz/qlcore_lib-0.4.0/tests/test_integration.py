import tempfile
import os
from decimal import Decimal

from qlcore.portfolio import Portfolio
from qlcore.events.fill import Fill
from qlcore.core.enums import OrderSide
from qlcore.serialization.json_codec import save_to_file, load_from_file
from qlcore.security.audit import AuditTrail
from qlcore.monitoring.metrics import timed_operation, get_metrics


def test_full_workflow_with_phase2():
    """Test complete workflow with Phase 2 features."""
    # Setup
    portfolio = Portfolio()
    audit = AuditTrail()

    # Execute trades with timing
    with timed_operation("apply_fill"):
        fill = Fill(
            "o1",
            "BTC-USD",
            OrderSide.BUY,
            Decimal("1"),
            Decimal("10000"),
            Decimal("10"),
            0,
        )
        portfolio.apply_fill(fill, user_id="trader1")
        audit.record_fill(
            user_id="trader1",
            order_id="o1",
            instrument_id="BTC-USD",
            side="BUY",
            quantity=Decimal("1"),
            price=Decimal("10000"),
            fee=Decimal("10"),
        )

    # Serialize
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "portfolio.json")
        save_to_file(portfolio, filepath)

        # Load
        restored = load_from_file(filepath, Portfolio)
        assert len(restored.positions) == 1

    # Check metrics
    stats = get_metrics().get_stats()
    assert "apply_fill" in stats["timings"]

    # Check audit trail
    user_events = audit.get_events_by_user("trader1")
    assert len(user_events) == 1


def test_error_recovery_with_audit():
    """Test error handling with audit trail."""
    from qlcore.core.exceptions import ValidationError
    import pytest

    audit = AuditTrail()

    # Try invalid fill
    with pytest.raises(ValidationError):
        Fill(
            "",
            "BTC-USD",
            OrderSide.BUY,  # Empty order_id
            Decimal("1"),
            Decimal("10000"),
            Decimal("10"),
            0,
        )

    # Audit trail should be empty (no record of failed operation)
    assert len(audit.events) == 0
