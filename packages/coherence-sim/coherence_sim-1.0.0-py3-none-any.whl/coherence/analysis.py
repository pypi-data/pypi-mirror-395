"""
Анализ и симуляции.

Этот модуль содержит инструменты для статистического анализа
и генерации случайных вселенных.
"""

from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy import stats

from .constants import UNIVERSE_STAGES, UniverseConstants
from .models import CoherenceModel


class UnifiedAnalysis:
    """
    Объединённый анализ когерентности и фундаментальных констант.

    Связывает рекуррентную модель роста когерентности
    с анализом фундаментальных физических констант.

    Примеры:
    --------
    >>> from coherence.analysis import UnifiedAnalysis
    >>> analysis = UnifiedAnalysis()
    >>> results = analysis.run_simulation()
    >>> print(f"Рост когерентности: {results['combined']['K'][-1]:.2f}")
    """

    def __init__(self, constants: Optional[UniverseConstants] = None):
        self.constants = constants or UniverseConstants()
        self.model = CoherenceModel(self.constants)
        self.stages = UNIVERSE_STAGES
        self.N = len(self.stages)

    def analyze_correspondence(self) -> Dict:
        """
        Анализ соответствия между α_fine_structure и α_coherence.

        Returns:
        --------
        Dict
            Словарь с результатами анализа
        """
        results = {
            "alpha_fine_structure": self.constants.alpha,
            "inverse_alpha": self.constants.inverse_alpha,
            "k_observed": self.constants.k_observed,
            "k_theoretical": self.constants.k_formula_new(),
            "k_error_percent": self.constants.k_error_percent("new"),
            "k_over_alpha": self.constants.k_over_alpha,
            "k_over_alpha_approx": round(self.constants.k_over_alpha),
            "alpha_effective": self.constants.effective_alpha(),
            "coherence_factor": np.pi * np.log(1 / self.constants.A_s) / self.constants.n_s,
        }
        return results

    def run_simulation(self, gamma: float = 0.2) -> Dict:
        """
        Запуск симуляции с разными значениями α.

        Parameters:
        -----------
        gamma : float
            Доля реализованной когерентности

        Returns:
        --------
        Dict
            Результаты для разных источников α
        """
        results = {}
        K0 = 1.0

        # 1. Модель с α из постоянной тонкой структуры (масштабированная)
        alpha_fs = self.constants.alpha * 100
        K1, C1, T1 = self.model.evolve(self.N, K0, alpha_fs, gamma)
        results["fine_structure"] = {
            "K": K1,
            "C": C1,
            "Total": T1,
            "alpha": alpha_fs,
            "label": f"α = 100×α_fs = {alpha_fs:.3f}",
        }

        # 2. Модель с α из голографического параметра
        alpha_k = self.constants.k_observed
        K2, C2, T2 = self.model.evolve(self.N, K0, alpha_k, gamma)
        results["holographic"] = {
            "K": K2,
            "C": C2,
            "Total": T2,
            "alpha": alpha_k,
            "label": f"α = k = {alpha_k:.3f}",
        }

        # 3. Модель с оптимальным α
        alpha_opt = 0.7
        K3, C3, T3 = self.model.evolve(self.N, K0, alpha_opt, gamma)
        results["optimal"] = {
            "K": K3,
            "C": C3,
            "Total": T3,
            "alpha": alpha_opt,
            "label": f"α = {alpha_opt:.3f} (оптим.)",
        }

        # 4. Модель с α = k/(α_fs × 100)
        alpha_comb = self.constants.effective_alpha()
        K4, C4, T4 = self.model.evolve(self.N, K0, alpha_comb, gamma)
        results["combined"] = {
            "K": K4,
            "C": C4,
            "Total": T4,
            "alpha": alpha_comb,
            "label": f"α = k/(100×α_fs) = {alpha_comb:.3f}",
        }

        return results

    def phase_diagram(
        self, alpha_range: Tuple[float, float] = (0.1, 0.9), n_points: int = 50
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Построение фазовой диаграммы α vs рост когерентности.

        Returns:
        --------
        alphas : np.ndarray
            Значения α
        growth_factors : np.ndarray
            Соответствующие факторы роста
        """
        alphas = np.linspace(alpha_range[0], alpha_range[1], n_points)
        growth_factors = np.array([self.model.growth_factor(a, self.N) for a in alphas])
        return alphas, growth_factors


class UniverseSimulator:
    """
    Генератор случайных вселенных для статистического анализа.

    Примеры:
    --------
    >>> from coherence.analysis import UniverseSimulator
    >>> sim = UniverseSimulator()
    >>> universes = sim.generate(n=1000)
    >>> print(f"Среднее k: {np.mean([u['k'] for u in universes]):.4f}")
    """

    def __init__(self, base_constants: Optional[UniverseConstants] = None):
        self.base = base_constants or UniverseConstants()

        # Диапазоны для генерации
        self.ranges = {
            "alpha": (0.00729, 0.00731),
            "A_s": (1.5e-9, 2.5e-9),
            "n_s": (0.94, 0.99),
            "m_z": (91.18, 91.20),
            "m_w": (80.37, 80.39),
        }

    def generate_one(self, method: str = "uniform") -> Dict:
        """
        Генерация одной случайной вселенной.

        Parameters:
        -----------
        method : str
            'uniform' — равномерное распределение
            'normal' — нормальное вокруг нашей Вселенной

        Returns:
        --------
        Dict
            Параметры вселенной
        """
        if method == "uniform":
            alpha = np.random.uniform(*self.ranges["alpha"])
            A_s = np.random.uniform(*self.ranges["A_s"])
            n_s = np.random.uniform(*self.ranges["n_s"])
            m_z = np.random.uniform(*self.ranges["m_z"])
            m_w = np.random.uniform(*self.ranges["m_w"])
        else:  # normal
            alpha = np.random.normal(self.base.alpha, self.base.uncertainties["alpha"])
            A_s = np.random.normal(self.base.A_s, self.base.uncertainties["A_s"])
            n_s = np.random.normal(self.base.n_s, self.base.uncertainties["n_s"])
            m_z = np.random.normal(self.base.m_z, self.base.uncertainties["m_z"])
            m_w = np.random.normal(self.base.m_w, self.base.uncertainties["m_w"])

        # Вычисляем k по формуле
        k = np.pi * alpha * np.log(1 / A_s) / n_s

        # Эффективный α
        alpha_eff = k / (alpha * 100)

        return {
            "alpha": alpha,
            "A_s": A_s,
            "n_s": n_s,
            "m_z": m_z,
            "m_w": m_w,
            "k": k,
            "alpha_eff": alpha_eff,
        }

    def generate(
        self, n: int = 1000, method: str = "uniform", with_coherence: bool = True
    ) -> List[Dict]:
        """
        Генерация набора случайных вселенных.

        Parameters:
        -----------
        n : int
            Количество вселенных
        method : str
            Метод генерации ('uniform' или 'normal')
        with_coherence : bool
            Вычислять ли когерентность для каждой вселенной

        Returns:
        --------
        List[Dict]
            Список параметров вселенных
        """
        universes = []
        model = CoherenceModel()
        N_stages = len(UNIVERSE_STAGES)

        for _ in range(n):
            universe = self.generate_one(method)

            if with_coherence:
                K, C, Total = model.evolve(N_stages, 1.0, universe["alpha_eff"], 0.2)
                universe["final_coherence"] = K[-1]
                universe["total_coherence"] = Total[-1]
                universe["growth_factor"] = K[-1] / K[0]

            universes.append(universe)

        return universes

    def statistical_analysis(self, universes: List[Dict]) -> Dict:
        """
        Статистический анализ набора вселенных.

        Parameters:
        -----------
        universes : List[Dict]
            Список вселенных

        Returns:
        --------
        Dict
            Статистика по параметрам
        """
        keys = ["k", "alpha_eff", "final_coherence", "growth_factor"]
        results = {}

        for key in keys:
            if key not in universes[0]:
                continue
            values = np.array([u[key] for u in universes])
            results[key] = {
                "mean": np.mean(values),
                "std": np.std(values),
                "median": np.median(values),
                "min": np.min(values),
                "max": np.max(values),
                "percentile_5": np.percentile(values, 5),
                "percentile_95": np.percentile(values, 95),
            }

        # Позиция нашей Вселенной
        k_values = np.array([u["k"] for u in universes])
        results["our_universe_percentile"] = stats.percentileofscore(k_values, self.base.k_observed)

        return results


class CoefficientAnalyzer:
    """
    Анализ "красивых" коэффициентов в формулах.

    Ищет совпадения с простыми числами, π, дробями и т.д.
    """

    # "Красивые" числа для поиска
    BEAUTIFUL_NUMBERS = [
        (1, "1"),
        (2, "2"),
        (np.pi, "π"),
        (np.pi / 2, "π/2"),
        (2 * np.pi, "2π"),
        (np.e, "e"),
        (3, "3"),
        (4, "4"),
        (6, "6"),
        (7, "7"),
        (8, "8"),
        (49 / 8, "49/8"),
        (66, "66"),
        (137, "137 (1/α)"),
    ]

    @staticmethod
    def find_nearest_beautiful(
        value: float, threshold: float = 0.05
    ) -> Optional[Tuple[float, str]]:
        """
        Найти ближайшее "красивое" число.

        Parameters:
        -----------
        value : float
            Искомое значение
        threshold : float
            Максимальное относительное отклонение

        Returns:
        --------
        Tuple[float, str] или None
            (число, название) или None если не найдено
        """
        best_match = None
        best_error = threshold

        for num, name in CoefficientAnalyzer.BEAUTIFUL_NUMBERS:
            error = abs(value - num) / num if num != 0 else float("inf")
            if error < best_error:
                best_error = error
                best_match = (num, name, error)

        return best_match

    @staticmethod
    def find_rational_approximation(
        value: float, max_denominator: int = 100
    ) -> Tuple[int, int, float]:
        """
        Найти рациональное приближение p/q.

        Returns:
        --------
        p : int
            Числитель
        q : int
            Знаменатель
        error : float
            Относительная ошибка
        """
        best_p, best_q = 1, 1
        best_error = float("inf")

        for q in range(1, max_denominator + 1):
            p = round(value * q)
            if p > 0:
                error = abs(p / q - value) / value
                if error < best_error:
                    best_error = error
                    best_p, best_q = p, q

        return best_p, best_q, best_error
