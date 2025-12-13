"""
Модели когерентности Вселенной.

Этот модуль содержит математические модели для расчёта
эволюции когерентности (сложности) во Вселенной.
"""

from typing import Optional, Tuple

import numpy as np
from scipy.optimize import brentq

from .constants import UniverseConstants


class CoherenceModel:
    """
    Рекуррентная модель роста когерентности.

    Центральная идея: когерентность на каждом этапе зависит от
    накопленного "осаждённого" потенциала всех предыдущих этапов.

    Формула:
        K(n) = K₀ + α_eff × Σ K(k)/(N-k)

    где α_eff может быть связан с фундаментальными константами.

    Параметры:
    ----------
    constants : UniverseConstants, optional
        Фундаментальные константы. Если None, используются стандартные.

    Примеры:
    --------
    >>> from coherence.models import CoherenceModel
    >>> model = CoherenceModel()
    >>> K, C, Total = model.evolve(N=12, alpha=0.66)
    >>> print(f"Рост когерентности: {K[-1]/K[0]:.2f}x")
    """

    def __init__(self, constants: Optional[UniverseConstants] = None):
        self.constants = constants or UniverseConstants()

    def evolve(
        self, N: int = 12, K0: float = 1.0, alpha: Optional[float] = None, gamma: float = 0.2
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Эволюция когерентности Вселенной.

        Parameters:
        -----------
        N : int
            Количество этапов эволюции
        K0 : float
            Начальная когерентность
        alpha : float, optional
            Параметр осаждения. Если None, вычисляется из констант.
        gamma : float
            Доля реализованной когерентности (0 < γ < 1)

        Returns:
        --------
        K : np.ndarray
            Потенциальная когерентность на каждом этапе
        C : np.ndarray
            Реализованная когерентность (C = γ × K)
        Total : np.ndarray
            Накопленная когерентность
        """
        if alpha is None:
            alpha = self.constants.effective_alpha()

        # Ограничиваем alpha разумным диапазоном
        alpha = np.clip(alpha, 0.01, 0.99)

        K = np.zeros(N)
        C = np.zeros(N)
        Total = np.zeros(N)

        K[0] = K0

        # Рекуррентное соотношение
        for n in range(1, N):
            deposited_sum = sum(K[k] / (N - k) for k in range(n))
            K[n] = K0 + alpha * deposited_sum

        # Реализованная когерентность
        for n in range(N):
            C[n] = gamma * K[n]
            Total[n] = np.sum(C[: n + 1])

        return K, C, Total

    def find_optimal_alpha(self, target_growth: float, N: int = 12, K0: float = 1.0) -> float:
        """
        Поиск α для достижения заданного роста когерентности.

        Parameters:
        -----------
        target_growth : float
            Желаемое отношение K(N)/K(0)
        N : int
            Количество этапов
        K0 : float
            Начальная когерентность

        Returns:
        --------
        float
            Оптимальное значение α
        """

        def objective(a):
            K, _, _ = self.evolve(N, K0, a)
            return K[-1] / K[0] - target_growth

        try:
            return brentq(objective, 0.01, 0.99)
        except ValueError:
            return 0.5

    def growth_factor(self, alpha: float, N: int = 12) -> float:
        """
        Вычисление фактора роста K(N)/K(0).

        Parameters:
        -----------
        alpha : float
            Параметр осаждения
        N : int
            Количество этапов

        Returns:
        --------
        float
            Фактор роста
        """
        K, _, _ = self.evolve(N, 1.0, alpha)
        return K[-1] / K[0]

    def evolve_corrected(
        self, N: int = 12, K0: float = 1.0, alpha: Optional[float] = None, gamma: float = 0.2
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Исправленная модель с нормировкой на номер этапа.

        Формула: K(n) = K₀ × (1 + α × Σ K(k)/max(1, N-k-1) / n)
        """
        if alpha is None:
            alpha = self.constants.effective_alpha()

        alpha = np.clip(alpha, 0.01, 0.99)

        K = np.zeros(N)
        C = np.zeros(N)
        Total = np.zeros(N)

        K[0] = K0

        for n in range(1, N):
            sum_term = 0
            for i in range(n):
                denominator = max(1, N - i - 1)
                sum_term += K[i] / denominator
            K[n] = K0 * (1 + alpha * sum_term / n)

        for n in range(N):
            C[n] = gamma * K[n]
            Total[n] = np.sum(C[: n + 1])

        return K, C, Total

    def evolve_with_dark_energy(
        self, N: int = 12, K0: float = 1.0, alpha: Optional[float] = None, gamma: float = 0.2
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Модель с учётом подавления тёмной энергией.

        Тёмная энергия подавляет рост когерентности на поздних этапах.
        """
        if alpha is None:
            alpha = self.constants.effective_alpha()

        alpha = np.clip(alpha, 0.01, 0.99)
        lambda_de = self.constants.Omega_lambda

        K = np.zeros(N)
        C = np.zeros(N)
        Total = np.zeros(N)

        K[0] = K0

        for n in range(1, N):
            sum_term = 0
            t_n = n / N

            for i in range(n):
                t_i = i / N
                dt = t_n - t_i
                if dt > 0:
                    # Подавление роста тёмной энергией
                    de_factor = 1 - lambda_de * (t_i**3)
                    sum_term += K[i] * de_factor / dt

            K[n] = K0 + alpha * sum_term / n

        for n in range(N):
            C[n] = gamma * K[n]
            Total[n] = np.sum(C[: n + 1])

        return K, C, Total

    def evolve_quantum(
        self, N: int = 12, K0: float = 1.0, alpha: Optional[float] = None, gamma: float = 0.2
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Квантовая модель с интерференцией амплитуд.

        Когерентность растёт через интерференцию квантовых амплитуд.
        """
        if alpha is None:
            alpha = self.constants.effective_alpha()

        alpha = np.clip(alpha, 0.01, 0.99)

        K = np.zeros(N)
        C = np.zeros(N)
        Total = np.zeros(N)

        K[0] = K0

        for n in range(1, N):
            # Квантовая суперпозиция вкладов
            amplitudes = []
            for i in range(n):
                # Амплитуда вероятности перехода
                amp = np.sqrt(K[i]) * np.exp(-((n - i) ** 2) / (2 * alpha**2))
                amplitudes.append(amp)

            # Интерференция амплитуд
            total_amp = np.sum(np.array(amplitudes))
            K[n] = K0 + alpha * np.abs(total_amp) ** 2

        for n in range(N):
            C[n] = gamma * K[n]
            Total[n] = np.sum(C[: n + 1])

        return K, C, Total

    def information_content(self, K: np.ndarray) -> dict:
        """
        Вычисление информационных характеристик когерентности.

        Parameters:
        -----------
        K : np.ndarray
            Массив значений когерентности

        Returns:
        --------
        dict
            Словарь с информационными метриками:
            - entropy: энтропия Шеннона
            - max_entropy: максимальная энтропия
            - efficiency: эффективность (entropy/max_entropy)
            - info_hartley: информация Хартли (биты)
            - info_rate: темп накопления информации
        """
        # Нормированное распределение (с регуляризацией)
        p = (K + 1e-10) / np.sum(K + 1e-10)

        # Энтропия Шеннона
        entropy = -np.sum(p * np.log2(p))

        # Максимальная энтропия
        max_entropy = np.log2(len(K))

        # Информация Хартли
        info_hartley = np.log2(K + 1)

        # Темп накопления информации
        info_rate = np.gradient(info_hartley)

        # Эффективность использования информации
        efficiency = entropy / max_entropy

        return {
            "entropy": entropy,
            "max_entropy": max_entropy,
            "efficiency": efficiency,
            "info_hartley": info_hartley,
            "info_rate": info_rate,
            "p": p,
        }

    def phase_transition_analysis(self, K: np.ndarray) -> dict:
        """
        Анализ фазовых переходов в эволюции когерентности.

        Parameters:
        -----------
        K : np.ndarray
            Массив значений когерентности

        Returns:
        --------
        dict
            Словарь с информацией о фазовых переходах:
            - inflection_points: точки перегиба
            - dlogK: первая производная log(K)
            - d2logK: вторая производная log(K)
        """
        log_K = np.log(K + 1e-10)

        # Первая и вторая производные
        dlogK = np.gradient(log_K)
        d2logK = np.gradient(dlogK)

        # Точки перегиба (смена знака второй производной)
        inflection_points = np.where(np.diff(np.sign(d2logK)))[0]

        return {"inflection_points": inflection_points, "dlogK": dlogK, "d2logK": d2logK}

    def predict_future(
        self, current_stage: int = 12, total_stages: int = 24, alpha: Optional[float] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Прогнозирование будущей эволюции когерентности.

        Parameters:
        -----------
        current_stage : int
            Текущий этап (по умолчанию 12)
        total_stages : int
            Общее количество этапов для прогноза
        alpha : float, optional
            Параметр осаждения

        Returns:
        --------
        K_future : np.ndarray
            Прогнозируемые значения когерентности
        stages : np.ndarray
            Номера будущих этапов
        """
        if alpha is None:
            alpha = self.constants.effective_alpha()

        # Текущее значение когерентности
        K_current, _, _ = self.evolve(current_stage + 1, alpha=alpha)
        K_now = K_current[-1]

        # Экстраполяция на будущие этапы
        future_stages = total_stages - current_stage
        K_future = np.zeros(future_stages)
        stages = np.arange(current_stage + 1, total_stages + 1)

        for i in range(future_stages):
            t_ratio = (current_stage + i) / total_stages
            # Формула экстраполяции: K ∝ (1 - t/T)^{-α}
            K_future[i] = (
                K_now * ((1 - current_stage / total_stages) / max(0.01, 1 - t_ratio)) ** alpha
            )

        return K_future, stages


class DepositionModel:
    """
    Модель осаждения с накоплением.

    Демонстрирует механизм накопления потенциала через осаждение.
    Аналогия с космологической моделью когерентности.

    Параметры:
    ----------
    M0 : float
        Начальное количество ресурса
    N : int
        Количество этапов
    alpha : float
        Доля осаждения (скрытый потенциал)
    gamma : float
        Доля реализации (использованный ресурс)
    beta : float, optional
        Потери. Если None, вычисляется как 1 - α - γ

    Примеры:
    --------
    >>> from coherence.models import DepositionModel
    >>> model = DepositionModel(M0=1.0, N=10, alpha=0.5, gamma=0.3)
    >>> C, P, m = model.calculate()
    >>> print(f"Использовано: {m[-1]:.2%}")
    """

    def __init__(
        self,
        M0: float = 1.0,
        N: int = 10,
        alpha: float = 0.5,
        gamma: float = 0.3,
        beta: Optional[float] = None,
    ):
        self.M0 = M0
        self.N = N
        self.alpha = alpha
        self.gamma = gamma

        if beta is None:
            self.beta = 1 - alpha - gamma
        else:
            self.beta = beta
            # Нормализуем, если сумма != 1
            total = alpha + beta + gamma
            if abs(total - 1) > 1e-10:
                self.alpha /= total
                self.beta /= total
                self.gamma /= total

    def calculate(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Расчёт процесса осаждения.

        Returns:
        --------
        C : np.ndarray
            Концентрация на каждом этапе
        P : np.ndarray
            Реализованный ресурс на каждом этапе
        m : np.ndarray
            Суммарная реализация после n этапов
        """
        C = np.zeros(self.N)
        P = np.zeros(self.N)
        m = np.zeros(self.N)

        C0 = self.M0 / self.N
        C[0] = C0

        # Рекуррентное накопление
        for n in range(1, self.N):
            deposited_sum = sum(C[k] / (self.N - k) for k in range(n))
            C[n] = C0 + self.alpha * deposited_sum

        # Потребление
        for n in range(self.N):
            P[n] = self.gamma * C[n]
            m[n] = np.sum(P[: n + 1])

        return C, P, m

    def efficiency(self) -> float:
        """
        Эффективность потребления (%).

        Returns:
        --------
        float
            Доля потреблённого вещества от начального
        """
        _, _, m = self.calculate()
        return m[-1] / self.M0

    def amplification(self) -> float:
        """
        Коэффициент усиления последнего этапа.

        Returns:
        --------
        float
            C(N) / C(0)
        """
        C, _, _ = self.calculate()
        return C[-1] / C[0]


class SymmetryBreaking:
    """
    Модель спонтанного нарушения симметрии.

    Потенциал Хиггса: V(φ) = μ² × φ² + λ × φ⁴

    При μ² > 0: симметричная фаза (один минимум)
    При μ² < 0: нарушение симметрии (два минимума)
    """

    @staticmethod
    def potential(phi: np.ndarray, mu2: float, lam: float = 0.25) -> np.ndarray:
        """
        Вычисление потенциала V(φ).

        Parameters:
        -----------
        phi : np.ndarray
            Значения поля
        mu2 : float
            Параметр μ² (положительный = симметрия, отрицательный = нарушение)
        lam : float
            Параметр λ (самодействие)

        Returns:
        --------
        np.ndarray
            Значения потенциала
        """
        return mu2 * phi**2 + lam * phi**4

    @staticmethod
    def phase_transition(
        phi_range: Tuple[float, float] = (-2, 2), n_points: int = 1000
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Генерация потенциалов для двух фаз.

        Returns:
        --------
        phi : np.ndarray
            Значения поля
        V_symmetric : np.ndarray
            Потенциал в симметричной фазе
        V_broken : np.ndarray
            Потенциал с нарушенной симметрией
        """
        phi = np.linspace(phi_range[0], phi_range[1], n_points)
        V_symmetric = SymmetryBreaking.potential(phi, mu2=1.0)
        V_broken = SymmetryBreaking.potential(phi, mu2=-1.0)
        return phi, V_symmetric, V_broken
