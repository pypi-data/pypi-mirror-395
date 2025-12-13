"""Tests for coherence.constants module."""

import pytest
import numpy as np
from coherence.constants import UniverseConstants, UNIVERSE_STAGES, M_REF_GEV


class TestUniverseConstants:
    """Tests for UniverseConstants class."""

    def test_default_values(self):
        """Test that default constants are set correctly."""
        c = UniverseConstants()

        assert c.alpha == pytest.approx(0.0072973525693, rel=1e-10)
        assert c.A_s == pytest.approx(2.100e-9, rel=1e-3)
        assert c.n_s == pytest.approx(0.9649, rel=1e-4)
        assert c.m_z == pytest.approx(91.1876, rel=1e-4)
        assert c.m_w == pytest.approx(80.3790, rel=1e-4)
        assert c.k_observed == pytest.approx(0.483678, rel=1e-4)

    def test_inverse_alpha(self):
        """Test inverse fine structure constant."""
        c = UniverseConstants()
        assert c.inverse_alpha == pytest.approx(137.036, rel=1e-3)

    def test_delta_m(self):
        """Test mass difference calculation."""
        c = UniverseConstants()
        assert c.delta_m == pytest.approx(10.8086, rel=1e-3)

    def test_k_over_alpha(self):
        """Test k/α ratio."""
        c = UniverseConstants()
        assert c.k_over_alpha == pytest.approx(66.28, rel=1e-2)

    def test_k_formula_new(self):
        """Test holographic formula for k."""
        c = UniverseConstants()
        k_calc = c.k_formula_new()

        # Should be close to observed k (within 2%)
        assert k_calc == pytest.approx(c.k_observed, rel=0.02)

        # Check the formula explicitly
        expected = np.pi * c.alpha * np.log(1 / c.A_s) / c.n_s
        assert k_calc == pytest.approx(expected, rel=1e-10)

    def test_k_formula_old(self):
        """Test boson mass formula for k."""
        c = UniverseConstants()
        k_calc = c.k_formula_old(m_ref=1.0)

        # Should be very close to observed k (within 0.2%)
        assert k_calc == pytest.approx(c.k_observed, rel=0.002)

    def test_k_formula_old_with_different_m_ref(self):
        """Test that m_ref affects the result."""
        c = UniverseConstants()

        k1 = c.k_formula_old(m_ref=1.0)
        k2 = c.k_formula_old(m_ref=2.0)

        assert k1 == pytest.approx(2 * k2, rel=1e-10)

    def test_k_error_percent(self):
        """Test error calculation."""
        c = UniverseConstants()

        error_new = c.k_error_percent("new")
        error_old = c.k_error_percent("old")

        # New formula has larger error
        assert error_new > error_old
        assert error_new < 2.0  # Less than 2%
        assert error_old < 0.2  # Less than 0.2%

    def test_effective_alpha(self):
        """Test effective alpha calculation."""
        c = UniverseConstants()
        alpha_eff = c.effective_alpha()

        # Should be around 0.66
        assert alpha_eff == pytest.approx(0.66, rel=0.02)

    def test_summary(self):
        """Test that summary returns a string."""
        c = UniverseConstants()
        summary = c.summary()

        assert isinstance(summary, str)
        assert "α" in summary or "alpha" in summary.lower()


class TestUniverseStages:
    """Tests for universe stages constants."""

    def test_stages_count(self):
        """Test that there are 12 stages."""
        assert len(UNIVERSE_STAGES) == 12

    def test_stages_order(self):
        """Test stages start and end correctly."""
        assert "Планковская" in UNIVERSE_STAGES[0]
        assert "Сейчас" in UNIVERSE_STAGES[-1]


class TestMRefConstant:
    """Tests for M_REF_GEV constant."""

    def test_m_ref_value(self):
        """Test M_REF_GEV is 1 GeV."""
        assert M_REF_GEV == 1.0
