"""Tests for pricing models and calculate_cost methods."""

from decimal import Decimal

import pytest

from unitysvc_services.models.base import (
    UsageData,
    validate_pricing,
    TokenPriceData,
    TimePriceData,
    ImagePriceData,
    StepPriceData,
    RevenueSharePriceData,
    ConstantPriceData,
    AddPriceData,
    MultiplyPriceData,
    TieredPriceData,
    GraduatedPriceData,
)


class TestTokenPriceData:
    """Tests for token-based pricing."""

    def test_unified_pricing(self) -> None:
        """Test unified token pricing (same price for input/output)."""
        pricing = validate_pricing({"type": "one_million_tokens", "price": "2.50"})
        usage = UsageData(input_tokens=1_000_000, output_tokens=500_000)

        cost = pricing.calculate_cost(usage)

        # 1.5M tokens * $2.50/M = $3.75
        assert cost == Decimal("3.75")

    def test_separate_input_output_pricing(self) -> None:
        """Test separate input/output token pricing."""
        pricing = validate_pricing({
            "type": "one_million_tokens",
            "input": "1.00",
            "output": "3.00",
        })
        usage = UsageData(input_tokens=1_000_000, output_tokens=500_000)

        cost = pricing.calculate_cost(usage)

        # 1M input * $1.00 + 0.5M output * $3.00 = $1.00 + $1.50 = $2.50
        assert cost == Decimal("2.50")

    def test_zero_tokens(self) -> None:
        """Test with zero tokens."""
        pricing = validate_pricing({"type": "one_million_tokens", "price": "5.00"})
        usage = UsageData(input_tokens=0, output_tokens=0)

        cost = pricing.calculate_cost(usage)

        assert cost == Decimal("0")


class TestTimePriceData:
    """Tests for time-based pricing."""

    def test_basic_time_pricing(self) -> None:
        """Test basic time-based pricing."""
        pricing = validate_pricing({"type": "one_second", "price": "0.006"})
        usage = UsageData(seconds=100.0)

        cost = pricing.calculate_cost(usage)

        # 100 seconds * $0.006 = $0.60
        assert cost == Decimal("0.6")

    def test_missing_seconds_raises_error(self) -> None:
        """Test that missing seconds raises ValueError."""
        pricing = validate_pricing({"type": "one_second", "price": "0.006"})
        usage = UsageData()

        with pytest.raises(ValueError, match="seconds"):
            pricing.calculate_cost(usage)


class TestImagePriceData:
    """Tests for image-based pricing."""

    def test_basic_image_pricing(self) -> None:
        """Test basic image pricing."""
        pricing = validate_pricing({"type": "image", "price": "0.04"})
        usage = UsageData(count=10)

        cost = pricing.calculate_cost(usage)

        # 10 images * $0.04 = $0.40
        assert cost == Decimal("0.40")

    def test_missing_count_raises_error(self) -> None:
        """Test that missing count raises ValueError."""
        pricing = validate_pricing({"type": "image", "price": "0.04"})
        usage = UsageData()

        with pytest.raises(ValueError, match="count"):
            pricing.calculate_cost(usage)


class TestStepPriceData:
    """Tests for step-based pricing."""

    def test_basic_step_pricing(self) -> None:
        """Test basic step pricing."""
        pricing = validate_pricing({"type": "step", "price": "0.001"})
        usage = UsageData(count=50)

        cost = pricing.calculate_cost(usage)

        # 50 steps * $0.001 = $0.05
        assert cost == Decimal("0.050")


class TestRevenueSharePriceData:
    """Tests for revenue share pricing."""

    def test_basic_revenue_share(self) -> None:
        """Test basic revenue share calculation."""
        pricing = validate_pricing({"type": "revenue_share", "percentage": "70.00"})
        usage = UsageData()

        cost = pricing.calculate_cost(usage, customer_charge=Decimal("100.00"))

        # 70% of $100 = $70
        assert cost == Decimal("70.00")

    def test_fractional_percentage(self) -> None:
        """Test revenue share with fractional percentage."""
        pricing = validate_pricing({"type": "revenue_share", "percentage": "85.5"})
        usage = UsageData()

        cost = pricing.calculate_cost(usage, customer_charge=Decimal("200.00"))

        # 85.5% of $200 = $171
        assert cost == Decimal("171.0")

    def test_missing_customer_charge_raises_error(self) -> None:
        """Test that missing customer_charge raises ValueError."""
        pricing = validate_pricing({"type": "revenue_share", "percentage": "70.00"})
        usage = UsageData()

        with pytest.raises(ValueError, match="customer_charge"):
            pricing.calculate_cost(usage)


class TestConstantPriceData:
    """Tests for constant pricing."""

    def test_positive_amount(self) -> None:
        """Test constant pricing with positive amount (fee)."""
        pricing = validate_pricing({"type": "constant", "amount": "5.00"})
        usage = UsageData()

        cost = pricing.calculate_cost(usage)

        assert cost == Decimal("5.00")

    def test_negative_amount(self) -> None:
        """Test constant pricing with negative amount (discount)."""
        pricing = validate_pricing({"type": "constant", "amount": "-10.00"})
        usage = UsageData()

        cost = pricing.calculate_cost(usage)

        assert cost == Decimal("-10.00")

    def test_ignores_usage(self) -> None:
        """Test that constant pricing ignores usage data."""
        pricing = validate_pricing({"type": "constant", "amount": "25.00"})
        usage = UsageData(input_tokens=1_000_000, seconds=100.0, count=50)

        cost = pricing.calculate_cost(usage)

        assert cost == Decimal("25.00")


class TestAddPriceData:
    """Tests for add (sum) pricing."""

    def test_sum_two_prices(self) -> None:
        """Test summing two pricing components."""
        pricing = validate_pricing({
            "type": "add",
            "prices": [
                {"type": "one_million_tokens", "price": "2.00"},
                {"type": "constant", "amount": "5.00"},
            ],
        })
        usage = UsageData(input_tokens=1_000_000)

        cost = pricing.calculate_cost(usage)

        # 1M tokens * $2.00 + $5.00 = $2.00 + $5.00 = $7.00
        assert cost == Decimal("7.00")

    def test_sum_with_discount(self) -> None:
        """Test summing with a negative constant (discount)."""
        pricing = validate_pricing({
            "type": "add",
            "prices": [
                {"type": "one_million_tokens", "input": "1.00", "output": "2.00"},
                {"type": "constant", "amount": "-3.00"},
            ],
        })
        usage = UsageData(input_tokens=2_000_000, output_tokens=1_000_000)

        cost = pricing.calculate_cost(usage)

        # 2M input * $1.00 + 1M output * $2.00 - $3.00 = $2.00 + $2.00 - $3.00 = $1.00
        assert cost == Decimal("1.00")

    def test_sum_multiple_components(self) -> None:
        """Test summing multiple pricing components."""
        pricing = validate_pricing({
            "type": "add",
            "prices": [
                {"type": "constant", "amount": "10.00"},
                {"type": "constant", "amount": "5.00"},
                {"type": "constant", "amount": "-2.50"},
            ],
        })
        usage = UsageData()

        cost = pricing.calculate_cost(usage)

        assert cost == Decimal("12.50")


class TestMultiplyPriceData:
    """Tests for multiply pricing."""

    def test_basic_multiply(self) -> None:
        """Test basic multiplication (70% discount factor)."""
        pricing = validate_pricing({
            "type": "multiply",
            "factor": "0.70",
            "base": {"type": "one_million_tokens", "price": "10.00"},
        })
        usage = UsageData(input_tokens=1_000_000)

        cost = pricing.calculate_cost(usage)

        # 1M tokens * $10.00 * 0.70 = $7.00
        assert cost == Decimal("7.00")

    def test_multiply_with_markup(self) -> None:
        """Test multiplication with markup (factor > 1)."""
        pricing = validate_pricing({
            "type": "multiply",
            "factor": "1.25",
            "base": {"type": "constant", "amount": "100.00"},
        })
        usage = UsageData()

        cost = pricing.calculate_cost(usage)

        # $100.00 * 1.25 = $125.00
        assert cost == Decimal("125.00")

    def test_nested_multiply(self) -> None:
        """Test nested multiply pricing."""
        pricing = validate_pricing({
            "type": "multiply",
            "factor": "0.80",
            "base": {
                "type": "multiply",
                "factor": "0.90",
                "base": {"type": "constant", "amount": "100.00"},
            },
        })
        usage = UsageData()

        cost = pricing.calculate_cost(usage)

        # $100.00 * 0.90 * 0.80 = $72.00
        assert cost == Decimal("72.00")


class TestTieredPriceData:
    """Tests for tiered (volume-based) pricing."""

    def test_first_tier(self) -> None:
        """Test pricing falls into first tier."""
        pricing = validate_pricing({
            "type": "tiered",
            "based_on": "request_count",
            "tiers": [
                {"up_to": 1000, "price": {"type": "constant", "amount": "10.00"}},
                {"up_to": 10000, "price": {"type": "constant", "amount": "80.00"}},
                {"up_to": None, "price": {"type": "constant", "amount": "500.00"}},
            ],
        })
        usage = UsageData()

        cost = pricing.calculate_cost(usage, request_count=500)

        assert cost == Decimal("10.00")

    def test_second_tier(self) -> None:
        """Test pricing falls into second tier."""
        pricing = validate_pricing({
            "type": "tiered",
            "based_on": "request_count",
            "tiers": [
                {"up_to": 1000, "price": {"type": "constant", "amount": "10.00"}},
                {"up_to": 10000, "price": {"type": "constant", "amount": "80.00"}},
                {"up_to": None, "price": {"type": "constant", "amount": "500.00"}},
            ],
        })
        usage = UsageData()

        cost = pricing.calculate_cost(usage, request_count=5000)

        assert cost == Decimal("80.00")

    def test_unlimited_tier(self) -> None:
        """Test pricing falls into unlimited tier."""
        pricing = validate_pricing({
            "type": "tiered",
            "based_on": "request_count",
            "tiers": [
                {"up_to": 1000, "price": {"type": "constant", "amount": "10.00"}},
                {"up_to": None, "price": {"type": "constant", "amount": "50.00"}},
            ],
        })
        usage = UsageData()

        cost = pricing.calculate_cost(usage, request_count=50000)

        assert cost == Decimal("50.00")

    def test_tier_boundary(self) -> None:
        """Test pricing at tier boundary (exactly 1000)."""
        pricing = validate_pricing({
            "type": "tiered",
            "based_on": "request_count",
            "tiers": [
                {"up_to": 1000, "price": {"type": "constant", "amount": "10.00"}},
                {"up_to": None, "price": {"type": "constant", "amount": "50.00"}},
            ],
        })
        usage = UsageData()

        cost = pricing.calculate_cost(usage, request_count=1000)

        # At boundary, should be tier 1
        assert cost == Decimal("10.00")

    def test_tiered_by_input_tokens(self) -> None:
        """Test tiered pricing based on input_tokens from UsageData."""
        pricing = validate_pricing({
            "type": "tiered",
            "based_on": "input_tokens",
            "tiers": [
                {"up_to": 1000000, "price": {"type": "one_million_tokens", "price": "5.00"}},
                {"up_to": None, "price": {"type": "one_million_tokens", "price": "2.50"}},
            ],
        })

        # Small usage - tier 1
        usage_small = UsageData(input_tokens=500_000, output_tokens=100_000)
        cost_small = pricing.calculate_cost(usage_small)
        # 0.6M tokens * $5.00 = $3.00
        assert cost_small == Decimal("3.00")

        # Large usage - tier 2
        usage_large = UsageData(input_tokens=5_000_000, output_tokens=100_000)
        cost_large = pricing.calculate_cost(usage_large)
        # 5.1M tokens * $2.50 = $12.75
        assert cost_large == Decimal("12.75")

    def test_tiered_with_usage_based_price(self) -> None:
        """Test tiered pricing where tier prices are usage-based."""
        pricing = validate_pricing({
            "type": "tiered",
            "based_on": "request_count",
            "tiers": [
                {"up_to": 1000, "price": {"type": "one_million_tokens", "input": "3.00", "output": "15.00"}},
                {"up_to": None, "price": {"type": "one_million_tokens", "input": "1.50", "output": "7.50"}},
            ],
        })
        usage = UsageData(input_tokens=100_000, output_tokens=50_000)

        # Small tier (high rate)
        cost_small = pricing.calculate_cost(usage, request_count=500)
        # 0.1M * $3.00 + 0.05M * $15.00 = $0.30 + $0.75 = $1.05
        assert cost_small == Decimal("1.05")

        # Large tier (low rate)
        cost_large = pricing.calculate_cost(usage, request_count=5000)
        # 0.1M * $1.50 + 0.05M * $7.50 = $0.15 + $0.375 = $0.525
        assert cost_large == Decimal("0.525")


class TestGraduatedPriceData:
    """Tests for graduated (AWS-style) pricing."""

    def test_first_tier_only(self) -> None:
        """Test graduated pricing within first tier."""
        pricing = validate_pricing({
            "type": "graduated",
            "based_on": "request_count",
            "tiers": [
                {"up_to": 1000, "unit_price": "0.01"},
                {"up_to": 10000, "unit_price": "0.008"},
                {"up_to": None, "unit_price": "0.005"},
            ],
        })
        usage = UsageData()

        cost = pricing.calculate_cost(usage, request_count=500)

        # 500 * $0.01 = $5.00
        assert cost == Decimal("5.00")

    def test_spans_two_tiers(self) -> None:
        """Test graduated pricing spanning two tiers."""
        pricing = validate_pricing({
            "type": "graduated",
            "based_on": "request_count",
            "tiers": [
                {"up_to": 1000, "unit_price": "0.01"},
                {"up_to": 10000, "unit_price": "0.008"},
                {"up_to": None, "unit_price": "0.005"},
            ],
        })
        usage = UsageData()

        cost = pricing.calculate_cost(usage, request_count=5000)

        # First 1000 * $0.01 + next 4000 * $0.008 = $10.00 + $32.00 = $42.00
        assert cost == Decimal("42.000")

    def test_spans_all_tiers(self) -> None:
        """Test graduated pricing spanning all tiers."""
        pricing = validate_pricing({
            "type": "graduated",
            "based_on": "request_count",
            "tiers": [
                {"up_to": 1000, "unit_price": "0.01"},
                {"up_to": 10000, "unit_price": "0.008"},
                {"up_to": None, "unit_price": "0.005"},
            ],
        })
        usage = UsageData()

        cost = pricing.calculate_cost(usage, request_count=15000)

        # First 1000 * $0.01 + next 9000 * $0.008 + next 5000 * $0.005
        # = $10.00 + $72.00 + $25.00 = $107.00
        assert cost == Decimal("107.000")

    def test_graduated_by_tokens(self) -> None:
        """Test graduated pricing based on tokens."""
        pricing = validate_pricing({
            "type": "graduated",
            "based_on": "input_tokens",
            "tiers": [
                {"up_to": 1000000, "unit_price": "0.000005"},  # $5 per 1M
                {"up_to": None, "unit_price": "0.0000025"},    # $2.50 per 1M
            ],
        })
        usage = UsageData(input_tokens=3_000_000)

        cost = pricing.calculate_cost(usage)

        # First 1M * $0.000005 + next 2M * $0.0000025
        # = $5.00 + $5.00 = $10.00
        assert cost == Decimal("10.0000000")

    def test_zero_usage(self) -> None:
        """Test graduated pricing with zero usage."""
        pricing = validate_pricing({
            "type": "graduated",
            "based_on": "request_count",
            "tiers": [
                {"up_to": 1000, "unit_price": "0.01"},
                {"up_to": None, "unit_price": "0.005"},
            ],
        })
        usage = UsageData()

        cost = pricing.calculate_cost(usage, request_count=0)

        assert cost == Decimal("0")


class TestTieredVsGraduated:
    """Tests comparing tiered vs graduated pricing behavior."""

    def test_different_results_for_same_volume(self) -> None:
        """Verify tiered and graduated give different results for same volume."""
        tiered = validate_pricing({
            "type": "tiered",
            "based_on": "request_count",
            "tiers": [
                {"up_to": 1000, "price": {"type": "constant", "amount": "10.00"}},
                {"up_to": None, "price": {"type": "constant", "amount": "40.00"}},
            ],
        })

        graduated = validate_pricing({
            "type": "graduated",
            "based_on": "request_count",
            "tiers": [
                {"up_to": 1000, "unit_price": "0.01"},
                {"up_to": None, "unit_price": "0.008"},
            ],
        })

        usage = UsageData()

        # For 5000 requests:
        # Tiered: Falls into tier 2 → $40.00 flat
        tiered_cost = tiered.calculate_cost(usage, request_count=5000)
        assert tiered_cost == Decimal("40.00")

        # Graduated: 1000 * $0.01 + 4000 * $0.008 = $10 + $32 = $42
        graduated_cost = graduated.calculate_cost(usage, request_count=5000)
        assert graduated_cost == Decimal("42.000")

        # They should be different
        assert tiered_cost != graduated_cost


class TestNestedCompositePricing:
    """Tests for nested composite pricing structures."""

    def test_add_with_tiered(self) -> None:
        """Test add pricing containing tiered pricing."""
        pricing = validate_pricing({
            "type": "add",
            "prices": [
                {
                    "type": "tiered",
                    "based_on": "request_count",
                    "tiers": [
                        {"up_to": 1000, "price": {"type": "constant", "amount": "10.00"}},
                        {"up_to": None, "price": {"type": "constant", "amount": "50.00"}},
                    ],
                },
                {"type": "constant", "amount": "5.00"},  # Platform fee
            ],
        })
        usage = UsageData()

        # Small volume: $10.00 + $5.00 = $15.00
        cost_small = pricing.calculate_cost(usage, request_count=500)
        assert cost_small == Decimal("15.00")

        # Large volume: $50.00 + $5.00 = $55.00
        cost_large = pricing.calculate_cost(usage, request_count=5000)
        assert cost_large == Decimal("55.00")

    def test_multiply_with_tiered(self) -> None:
        """Test multiply pricing with tiered base."""
        pricing = validate_pricing({
            "type": "multiply",
            "factor": "0.80",  # 20% discount
            "base": {
                "type": "tiered",
                "based_on": "request_count",
                "tiers": [
                    {"up_to": 1000, "price": {"type": "constant", "amount": "100.00"}},
                    {"up_to": None, "price": {"type": "constant", "amount": "500.00"}},
                ],
            },
        })
        usage = UsageData()

        # Small volume: $100.00 * 0.80 = $80.00
        cost_small = pricing.calculate_cost(usage, request_count=500)
        assert cost_small == Decimal("80.00")

        # Large volume: $500.00 * 0.80 = $400.00
        cost_large = pricing.calculate_cost(usage, request_count=5000)
        assert cost_large == Decimal("400.00")

    def test_deeply_nested_pricing(self) -> None:
        """Test deeply nested pricing structure."""
        pricing = validate_pricing({
            "type": "add",
            "prices": [
                {
                    "type": "multiply",
                    "factor": "0.90",
                    "base": {
                        "type": "tiered",
                        "based_on": "request_count",
                        "tiers": [
                            {"up_to": 1000, "price": {"type": "one_million_tokens", "price": "10.00"}},
                            {"up_to": None, "price": {"type": "one_million_tokens", "price": "5.00"}},
                        ],
                    },
                },
                {"type": "constant", "amount": "2.00"},  # Fixed fee
            ],
        })
        usage = UsageData(input_tokens=1_000_000)

        # Small volume: (1M * $10.00) * 0.90 + $2.00 = $9.00 + $2.00 = $11.00
        cost_small = pricing.calculate_cost(usage, request_count=500)
        assert cost_small == Decimal("11.00")

        # Large volume: (1M * $5.00) * 0.90 + $2.00 = $4.50 + $2.00 = $6.50
        cost_large = pricing.calculate_cost(usage, request_count=5000)
        assert cost_large == Decimal("6.50")
