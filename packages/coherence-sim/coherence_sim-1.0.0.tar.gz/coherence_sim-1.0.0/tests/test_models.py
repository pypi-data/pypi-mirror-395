"""Tests for coherence.models module."""

import pytest
import numpy as np
from coherence.models import CoherenceModel, DepositionModel, SymmetryBreaking
from coherence.constants import UniverseConstants


class TestCoherenceModel:
    """Tests for CoherenceModel class."""

    def test_initialization(self):
        """Test model initialization."""
        model = CoherenceModel()
        assert model.constants is not None
        assert isinstance(model.constants, UniverseConstants)

    def test_evolve_basic(self):
        """Test basic evolution."""
        model = CoherenceModel()
        K, C, Total = model.evolve(N=12, K0=1.0, alpha=0.66, gamma=0.2)

        assert len(K) == 12
        assert len(C) == 12
        assert len(Total) == 12

    def test_evolve_initial_conditions(self):
        """Test that initial conditions are respected."""
        model = CoherenceModel()
        K, C, Total = model.evolve(N=10, K0=2.0, alpha=0.5, gamma=0.3)

        assert K[0] == 2.0
        assert C[0] == pytest.approx(0.6)  # gamma * K0

    def test_evolve_monotonic_growth(self):
        """Test that coherence grows monotonically."""
        model = CoherenceModel()
        K, C, Total = model.evolve(N=12, alpha=0.66)

        for i in range(1, len(K)):
            assert K[i] >= K[i - 1], f"K decreased at step {i}"

    def test_evolve_total_accumulation(self):
        """Test that total is accumulated correctly."""
        model = CoherenceModel()
        K, C, Total = model.evolve(N=12, gamma=0.2)

        assert Total[-1] == pytest.approx(np.sum(C), rel=1e-10)

    def test_evolve_alpha_effect(self):
        """Test that higher alpha gives higher growth."""
        model = CoherenceModel()

        K_low, _, _ = model.evolve(N=12, alpha=0.3)
        K_high, _, _ = model.evolve(N=12, alpha=0.8)

        assert K_high[-1] > K_low[-1]

    def test_evolve_default_alpha(self):
        """Test evolution with default alpha from constants."""
        model = CoherenceModel()
        K, C, Total = model.evolve(N=12)

        # Should use effective_alpha from constants
        assert K[-1] > K[0]

    def test_growth_factor(self):
        """Test growth factor calculation."""
        model = CoherenceModel()

        growth = model.growth_factor(alpha=0.66, N=12)

        # Should be around 3.6
        assert growth == pytest.approx(3.6, rel=0.05)

    def test_find_optimal_alpha(self):
        """Test optimal alpha finding."""
        model = CoherenceModel()

        alpha_opt = model.find_optimal_alpha(target_growth=2.0, N=12)

        # Check that it achieves target
        K, _, _ = model.evolve(N=12, alpha=alpha_opt)
        actual_growth = K[-1] / K[0]

        assert actual_growth == pytest.approx(2.0, rel=0.01)


class TestDepositionModel:
    """Tests for DepositionModel class."""

    def test_initialization(self):
        """Test model initialization."""
        model = DepositionModel(M0=1.0, N=10, alpha=0.5, gamma=0.3)

        assert model.M0 == 1.0
        assert model.N == 10
        assert model.alpha == 0.5
        assert model.gamma == 0.3
        assert model.beta == pytest.approx(0.2)

    def test_parameter_normalization(self):
        """Test that parameters are normalized if sum != 1."""
        model = DepositionModel(M0=1.0, N=10, alpha=0.6, gamma=0.6, beta=0.6)

        # Sum should be 1
        assert model.alpha + model.beta + model.gamma == pytest.approx(1.0)

    def test_calculate_basic(self):
        """Test basic calculation."""
        model = DepositionModel(M0=1.0, N=10, alpha=0.5, gamma=0.3)
        C, P, m = model.calculate()

        assert len(C) == 10
        assert len(P) == 10
        assert len(m) == 10

    def test_efficiency(self):
        """Test efficiency calculation."""
        model = DepositionModel(M0=1.0, N=10, alpha=0.5, gamma=0.3)
        eff = model.efficiency()

        assert 0 < eff < 1

    def test_amplification(self):
        """Test amplification calculation."""
        model = DepositionModel(M0=1.0, N=10, alpha=0.5, gamma=0.3)
        amp = model.amplification()

        # Should be greater than 1 with positive alpha
        assert amp > 1


class TestSymmetryBreaking:
    """Tests for SymmetryBreaking class."""

    def test_potential_symmetric(self):
        """Test symmetric potential (mu2 > 0)."""
        phi = np.linspace(-2, 2, 100)
        V = SymmetryBreaking.potential(phi, mu2=1.0, lam=0.25)

        # Minimum should be at phi = 0
        min_idx = np.argmin(V)
        assert phi[min_idx] == pytest.approx(0, abs=0.1)

    def test_potential_broken(self):
        """Test broken symmetry potential (mu2 < 0)."""
        phi = np.linspace(-2, 2, 100)
        V = SymmetryBreaking.potential(phi, mu2=-1.0, lam=0.25)

        # Should have two minima (not at phi = 0)
        # The value at phi = 0 should be a local maximum
        mid_idx = len(phi) // 2
        assert V[mid_idx] > V[mid_idx - 20]
        assert V[mid_idx] > V[mid_idx + 20]

    def test_phase_transition(self):
        """Test phase transition function."""
        phi, V_sym, V_broken = SymmetryBreaking.phase_transition()

        assert len(phi) == 1000
        assert len(V_sym) == 1000
        assert len(V_broken) == 1000

        # V_sym should have minimum at 0
        # V_broken should have minimum away from 0
        assert V_sym[len(phi) // 2] < V_sym[0]
        assert V_broken[len(phi) // 2] > V_broken[len(phi) // 4]
