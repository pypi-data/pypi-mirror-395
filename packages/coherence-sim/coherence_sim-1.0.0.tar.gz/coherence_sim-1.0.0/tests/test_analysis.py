"""Tests for coherence.analysis module."""

import pytest
import numpy as np
from coherence.analysis import UnifiedAnalysis, UniverseSimulator, CoefficientAnalyzer


class TestUnifiedAnalysis:
    """Tests for UnifiedAnalysis class."""

    def test_initialization(self):
        """Test analysis initialization."""
        analysis = UnifiedAnalysis()

        assert analysis.constants is not None
        assert analysis.model is not None
        assert len(analysis.stages) == 12

    def test_analyze_correspondence(self):
        """Test correspondence analysis."""
        analysis = UnifiedAnalysis()
        results = analysis.analyze_correspondence()

        assert "alpha_fine_structure" in results
        assert "k_observed" in results
        assert "k_theoretical" in results
        assert "k_error_percent" in results
        assert "k_over_alpha" in results
        assert "alpha_effective" in results

    def test_run_simulation(self):
        """Test simulation run."""
        analysis = UnifiedAnalysis()
        results = analysis.run_simulation()

        assert "fine_structure" in results
        assert "holographic" in results
        assert "optimal" in results
        assert "combined" in results

        for key in results:
            assert "K" in results[key]
            assert "C" in results[key]
            assert "Total" in results[key]
            assert "alpha" in results[key]

    def test_phase_diagram(self):
        """Test phase diagram generation."""
        analysis = UnifiedAnalysis()
        alphas, growth_factors = analysis.phase_diagram(n_points=20)

        assert len(alphas) == 20
        assert len(growth_factors) == 20
        assert all(g >= 1 for g in growth_factors)


class TestUniverseSimulator:
    """Tests for UniverseSimulator class."""

    def test_initialization(self):
        """Test simulator initialization."""
        sim = UniverseSimulator()

        assert sim.base is not None
        assert "alpha" in sim.ranges
        assert "A_s" in sim.ranges

    def test_generate_one_uniform(self):
        """Test single universe generation (uniform)."""
        sim = UniverseSimulator()
        universe = sim.generate_one(method="uniform")

        assert "alpha" in universe
        assert "A_s" in universe
        assert "n_s" in universe
        assert "k" in universe
        assert "alpha_eff" in universe

    def test_generate_one_normal(self):
        """Test single universe generation (normal)."""
        sim = UniverseSimulator()
        universe = sim.generate_one(method="normal")

        assert "alpha" in universe
        assert "k" in universe

    def test_generate_multiple(self):
        """Test multiple universe generation."""
        sim = UniverseSimulator()
        universes = sim.generate(n=100, with_coherence=True)

        assert len(universes) == 100
        assert "final_coherence" in universes[0]
        assert "growth_factor" in universes[0]

    def test_generate_without_coherence(self):
        """Test generation without coherence calculation."""
        sim = UniverseSimulator()
        universes = sim.generate(n=50, with_coherence=False)

        assert len(universes) == 50
        assert "final_coherence" not in universes[0]

    def test_statistical_analysis(self):
        """Test statistical analysis."""
        sim = UniverseSimulator()
        universes = sim.generate(n=100, with_coherence=True)
        stats = sim.statistical_analysis(universes)

        assert "k" in stats
        assert "mean" in stats["k"]
        assert "std" in stats["k"]
        assert "our_universe_percentile" in stats


class TestCoefficientAnalyzer:
    """Tests for CoefficientAnalyzer class."""

    def test_find_nearest_beautiful_pi(self):
        """Test finding π as beautiful number."""
        result = CoefficientAnalyzer.find_nearest_beautiful(3.14, threshold=0.01)

        assert result is not None
        num, name, error = result
        assert name == "π"
        assert error < 0.01

    def test_find_nearest_beautiful_not_found(self):
        """Test when no beautiful number is close."""
        result = CoefficientAnalyzer.find_nearest_beautiful(42.5, threshold=0.01)

        assert result is None

    def test_find_rational_approximation(self):
        """Test rational approximation."""
        # Test with 2/3 ≈ 0.666...
        p, q, error = CoefficientAnalyzer.find_rational_approximation(0.666666, max_denominator=10)

        assert p == 2
        assert q == 3
        assert error < 0.001

    def test_find_rational_approximation_49_8(self):
        """Test finding 49/8."""
        value = 49 / 8  # 6.125
        p, q, error = CoefficientAnalyzer.find_rational_approximation(value, max_denominator=50)

        assert p == 49
        assert q == 8
        assert error < 1e-10
