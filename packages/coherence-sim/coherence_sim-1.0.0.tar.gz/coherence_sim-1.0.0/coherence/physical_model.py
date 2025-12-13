"""
Физическая трёхкомпонентная модель когерентности.

Этот модуль реализует модель с тремя физическими компонентами:
1. Гравитационная когерентность — рост структуры
2. Информационная когерентность — звездообразование, металличность
3. Сложностная когерентность — самоорганизация, иерархия
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy.optimize import curve_fit

# ============================================================================
# НАБЛЮДАТЕЛЬНЫЕ ДАННЫЕ
# ============================================================================

COSMOLOGICAL_OBSERVATIONS = {
    "redshift": [float("inf"), 1e28, 1e12, 1e9, 1100, 30, 20, 3, 2, 0.5, 0.1, 0, 0],
    "mass_in_halos": [0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.05, 0.2, 0.3, 0.4, 0.45, 0.5, 0.5],
    "star_formation_rate": [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.5, 2.0, 3.0, 1.5, 1.0, 1.0, 1.0],
    "metallicity": [0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.05, 0.3, 0.5, 0.8, 0.9, 1.0, 1.0],
    "black_hole_mass": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.001,
        0.005,
        0.01,
        0.008,
        0.006,
        0.005,
        0.005,
    ],
}

PHYSICAL_PROCESSES = {
    "gravity": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 0.9, 0.7, 0.6, 0.5, 0.4],
    "information": [0.0, 0.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 0.9, 1.0, 1.1, 1.2],
    "complexity": [0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 1.0, 1.0],
    "feedback": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
}

EXTENDED_STAGES = [
    "Планковская эпоха (z=∞)",
    "Инфляция (z=10²⁸)",
    "Кварк-глюонная плазма (z=10¹²)",
    "Нуклеосинтез (z=10⁹)",
    "Рекомбинация (z=1100)",
    "Тёмные века (z=30)",
    "Первые звёзды (z=20)",
    "Образование галактик (z=3)",
    "Пик звездообразования (z=2)",
    "Солнечная система (z=0.5)",
    "Жизнь на Земле (z=0.1)",
    "Разум (z=0)",
    "Современная эпоха (z=0)",
]


# ============================================================================
# DATACLASSES
# ============================================================================


@dataclass
class PhysicalParameters:
    """Параметры физической модели."""

    gravity_weight: float = 0.4
    info_weight: float = 0.4
    complexity_weight: float = 0.2
    feedback_factor: float = 0.3
    merger_factor: float = 0.2

    def normalize(self):
        """Нормализация весов."""
        total = self.gravity_weight + self.info_weight + self.complexity_weight
        if total > 0:
            self.gravity_weight /= total
            self.info_weight /= total
            self.complexity_weight /= total


@dataclass
class CosmologicalParams:
    """Космологические параметры."""

    H0: float = 67.36  # км/с/Мпк
    Omega_m: float = 0.315
    Omega_lambda: float = 0.685
    sigma_8: float = 0.811
    z_reion: float = 7.7
    t0: float = 13.8e9  # лет


@dataclass
class ValidationResult:
    """Результат валидации модели."""

    chi2: float
    chi2_per_dof: float
    r_squared: float
    mean_deviation: float
    residuals: np.ndarray
    model_normalized: np.ndarray
    obs_normalized: np.ndarray

    @property
    def quality(self) -> str:
        if self.chi2_per_dof < 1:
            return "отличное"
        elif self.chi2_per_dof < 2:
            return "хорошее"
        elif self.chi2_per_dof < 3:
            return "удовлетворительное"
        else:
            return "плохое"


# ============================================================================
# ТРЁХКОМПОНЕНТНАЯ МОДЕЛЬ
# ============================================================================


class ThreeComponentModel:
    """
    Физическая модель когерентности с тремя компонентами.

    Компоненты:
    -----------
    1. Гравитационная когерентность — рост структуры, тёмная материя
    2. Информационная когерентность — звездообразование, металличность, ЧД
    3. Сложностная когерентность — иерархия, самоорганизация, обратная связь

    Примеры:
    --------
    >>> from coherence.physical_model import ThreeComponentModel
    >>> model = ThreeComponentModel()
    >>> K = model.total_coherence(z=0)  # Когерентность сейчас
    """

    def __init__(self, cosmo_params: Optional[CosmologicalParams] = None):
        self.params = cosmo_params or CosmologicalParams()
        self.stages = EXTENDED_STAGES

    def gravitational_coherence(self, z: float) -> float:
        """
        Гравитационная компонента когерентности.

        Зависит от роста структуры и тёмной материи.
        Использует линейную теорию роста для Lambda-CDM.
        """
        if z <= 0:
            z = 1e-10

        Omega_m = self.params.Omega_m
        Omega_lambda = self.params.Omega_lambda

        # Масштабный фактор
        a = 1 / (1 + z)

        # Упрощённая функция роста
        try:
            D_z = (5 * Omega_m / 2) * a / (Omega_m * (1 + z) ** 3 + Omega_lambda) ** 0.5
            D0 = (5 * Omega_m / 2) / (Omega_m + Omega_lambda) ** 0.5
            growth = D_z / D0 if D0 > 0 else 1.0
        except:
            growth = 1.0

        # Нелинейная поправка
        nonlinear_factor = 1 + 0.5 * np.exp(-z / 2)

        return max(0, growth * nonlinear_factor)

    def information_coherence(self, z: float) -> float:
        """
        Информационная компонента когерентности.

        Зависит от сложности структуры и накопления информации:
        - Звездообразование (SFR)
        - Металличность
        - Доля массы в чёрных дырах
        """
        SFR = self._star_formation_rate(z)
        metals = self._metal_abundance(z)
        BHF = self._black_hole_fraction(z)

        # Комбинированная информация
        info = SFR**0.5 * metals**0.3 * (1 + BHF) ** 0.2

        return max(0, info)

    def complexity_coherence(self, z: float) -> float:
        """
        Сложностная компонента когерентности.

        Зависит от иерархической структуры и самоорганизации.
        """
        # Иерархический рост
        hierarchy = np.exp(-z / 3)

        # Самоорганизация (обратная связь)
        feedback = 1 + 0.5 * np.exp(-z / 5)

        # Крупномасштабная структура
        large_scale = 1 / (1 + np.exp(-(2 - z)))

        return max(0, hierarchy * feedback * large_scale)

    def total_coherence(self, z: float, weights: Optional[List[float]] = None) -> float:
        """
        Общая когерентность как взвешенная сумма компонент.

        Parameters:
        -----------
        z : float
            Красное смещение
        weights : list, optional
            Веса [гравитация, информация, сложность]
        """
        if weights is None:
            weights = [0.4, 0.4, 0.2]

        G = self.gravitational_coherence(z)
        I = self.information_coherence(z)
        C = self.complexity_coherence(z)

        return weights[0] * G + weights[1] * I + weights[2] * C

    def coherence_array(
        self, z_array: np.ndarray, weights: Optional[List[float]] = None
    ) -> np.ndarray:
        """Когерентность для массива красных смещений."""
        return np.array([self.total_coherence(z, weights) for z in z_array])

    def _star_formation_rate(self, z: float) -> float:
        """Модель скорости звездообразования (Madau & Dickinson 2014)."""
        if z < 0:
            z = 0
        return (1 + z) ** 2.7 / (1 + ((1 + z) / 2.9) ** 5.6)

    def _metal_abundance(self, z: float) -> float:
        """Металличность как функция z."""
        return np.exp(-z / 3)

    def _black_hole_fraction(self, z: float) -> float:
        """Доля массы в чёрных дырах."""
        return 0.001 * np.exp(-z / 2)

    def components_at_z(self, z: float) -> Dict[str, float]:
        """Все компоненты когерентности при данном z."""
        return {
            "gravitational": self.gravitational_coherence(z),
            "informational": self.information_coherence(z),
            "complexity": self.complexity_coherence(z),
            "total": self.total_coherence(z),
        }


# ============================================================================
# ФИЗИЧЕСКАЯ РЕКУРРЕНТНАЯ МОДЕЛЬ
# ============================================================================


class PhysicalRecurrenceModel:
    """
    Рекуррентная модель с физическими компонентами.

    Улучшенная модель с:
    - Взвешенными вкладами компонент
    - Экспоненциальным затуханием
    - Нелинейной обратной связью
    """

    def __init__(self, params: Optional[PhysicalParameters] = None):
        self.params = params or PhysicalParameters()
        self.stages = EXTENDED_STAGES
        self.processes = {k: np.array(v) for k, v in PHYSICAL_PROCESSES.items()}

    def evolve(
        self, N: int = 13, k: float = 0.6721, K0: float = 1.0
    ) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
        """
        Эволюция когерентности с физическими компонентами.

        Parameters:
        -----------
        N : int
            Количество этапов (по умолчанию 13)
        k : float
            Параметр роста
        K0 : float
            Начальная когерентность

        Returns:
        --------
        tuple
            (массив когерентности, словарь процессов)
        """
        K = np.zeros(N)
        K[0] = K0

        # Обрезаем или расширяем процессы до N
        processes = {}
        for name, arr in self.processes.items():
            if len(arr) >= N:
                processes[name] = arr[:N]
            else:
                # Экстраполяция
                extended = np.zeros(N)
                extended[: len(arr)] = arr
                extended[len(arr) :] = arr[-1]
                processes[name] = extended

        for n in range(1, N):
            sum_gravity = 0
            sum_info = 0
            sum_complexity = 0

            for i in range(n):
                decay = np.exp(-0.5 * (n - i))
                weight = 1 / (N - i) if N > i else 1

                sum_gravity += K[i] * processes["gravity"][i] * decay * weight
                sum_info += K[i] * processes["information"][i] * decay * weight
                sum_complexity += K[i] * processes["complexity"][i] * decay * weight

            # Обратная связь
            feedback = 1 + self.params.feedback_factor * processes["feedback"][n]

            # Основная формула
            K[n] = (
                K0
                + k
                * (
                    self.params.gravity_weight * sum_gravity
                    + self.params.info_weight * sum_info
                    + self.params.complexity_weight * sum_complexity
                )
            ) * feedback

            # Ограничение роста
            K[n] = min(K[n], 10 * K0)

        return K, processes

    def validate_with_observations(self, K: np.ndarray) -> ValidationResult:
        """
        Валидация модели с наблюдательными данными.

        Parameters:
        -----------
        K : np.ndarray
            Массив когерентности

        Returns:
        --------
        ValidationResult
            Результат валидации
        """
        obs = COSMOLOGICAL_OBSERVATIONS
        N = len(K)

        # Проверка размерности
        if N > len(obs["mass_in_halos"]):
            N = len(obs["mass_in_halos"])
            K = K[:N]

        # Комбинированная наблюдаемая когерентность
        weights = [0.3, 0.3, 0.2, 0.2]
        obs_coherence = (
            weights[0] * np.array(obs["mass_in_halos"][:N])
            + weights[1] * np.array(obs["star_formation_rate"][:N]) / 3.0
            + weights[2] * np.array(obs["metallicity"][:N])
            + weights[3] * np.array(obs["black_hole_mass"][:N]) * 100
        )

        # Нормализация
        model_norm = K / np.max(K) if np.max(K) > 0 else K
        obs_norm = (
            obs_coherence / np.max(obs_coherence) if np.max(obs_coherence) > 0 else obs_coherence
        )

        # Статистика
        residuals = model_norm - obs_norm
        chi2 = np.sum(residuals**2 / 0.1**2)
        chi2_per_dof = chi2 / max(1, N - 1)

        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((obs_norm - np.mean(obs_norm)) ** 2)
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        return ValidationResult(
            chi2=chi2,
            chi2_per_dof=chi2_per_dof,
            r_squared=r_squared,
            mean_deviation=np.mean(np.abs(residuals)),
            residuals=residuals,
            model_normalized=model_norm,
            obs_normalized=obs_norm,
        )

    def optimize_k(
        self, k_range: Tuple[float, float] = (0.3, 0.9), n_points: int = 20
    ) -> Tuple[float, float]:
        """
        Поиск оптимального k.

        Returns:
        --------
        tuple
            (оптимальное k, минимальное χ²)
        """
        k_values = np.linspace(k_range[0], k_range[1], n_points)
        best_k = k_values[0]
        best_chi2 = float("inf")

        for k in k_values:
            K, _ = self.evolve(k=k)
            result = self.validate_with_observations(K)
            if result.chi2_per_dof < best_chi2:
                best_chi2 = result.chi2_per_dof
                best_k = k

        return best_k, best_chi2


# ============================================================================
# ФУНКЦИИ БЫСТРОГО ДОСТУПА
# ============================================================================


def physical_coherence(N: int = 13, k: float = 0.6721) -> Tuple[np.ndarray, Dict]:
    """
    Быстрый расчёт физической когерентности.

    Parameters:
    -----------
    N : int
        Количество этапов
    k : float
        Параметр роста

    Returns:
    --------
    tuple
        (массив когерентности, процессы)
    """
    model = PhysicalRecurrenceModel()
    return model.evolve(N, k)


def validate_model(K: np.ndarray) -> ValidationResult:
    """
    Валидация модели с наблюдениями.

    Parameters:
    -----------
    K : np.ndarray
        Массив когерентности

    Returns:
    --------
    ValidationResult
        Результат валидации
    """
    model = PhysicalRecurrenceModel()
    return model.validate_with_observations(K)


def find_optimal_k() -> Tuple[float, float]:
    """
    Поиск оптимального параметра k.

    Returns:
    --------
    tuple
        (оптимальное k, минимальное χ²)
    """
    model = PhysicalRecurrenceModel()
    return model.optimize_k()


def get_extended_stages() -> List[str]:
    """Получить расширенный список этапов (13 этапов)."""
    return EXTENDED_STAGES.copy()


def get_physical_processes() -> Dict[str, List[float]]:
    """Получить физические процессы по этапам."""
    return {k: list(v) for k, v in PHYSICAL_PROCESSES.items()}


def get_cosmological_observations() -> Dict[str, List[float]]:
    """Получить наблюдательные данные."""
    return {k: list(v) for k, v in COSMOLOGICAL_OBSERVATIONS.items()}
