"""
Coherence — библиотека для моделирования когерентности Вселенной.

Эта библиотека реализует математическую модель роста когерентности
(сложности) во Вселенной, основанную на рекуррентном соотношении
и связи с фундаментальными физическими константами.

Основные модули:
----------------
- constants : Фундаментальные константы Вселенной
- models : Модели когерентности (CoherenceModel, DepositionModel)
- analysis : Анализ и симуляции
- visualization : Визуализация результатов

Быстрый старт:
--------------
>>> from coherence import CoherenceModel, UniverseConstants
>>>
>>> # Создание модели
>>> model = CoherenceModel()
>>>
>>> # Эволюция когерентности за 12 этапов
>>> K, C, Total = model.evolve(N=12, alpha=0.66)
>>>
>>> # Результат
>>> print(f"Рост когерентности: {K[-1]/K[0]:.2f}x")
Рост когерентности: 3.62x

Пример с анализом:
------------------
>>> from coherence import UnifiedAnalysis
>>>
>>> analysis = UnifiedAnalysis()
>>> results = analysis.analyze_correspondence()
>>> print(f"k/α ≈ {results['k_over_alpha']:.0f}")
k/α ≈ 66
"""

__version__ = "1.0.0"
__author__ = "Timur Isanov"

from .analysis import CoefficientAnalyzer, UnifiedAnalysis, UniverseSimulator

# Основные классы
from .constants import (
    FUTURE_STAGES,
    M_REF_GEV,
    UNIVERSE_STAGES,
    UNIVERSE_STAGES_SHORT,
    UniverseConstants,
)
from .models import CoherenceModel, DepositionModel, SymmetryBreaking

# Физическая трёхкомпонентная модель
from .physical_model import (
    COSMOLOGICAL_OBSERVATIONS,
    EXTENDED_STAGES,
    PHYSICAL_PROCESSES,
    CosmologicalParams,
    PhysicalParameters,
    PhysicalRecurrenceModel,
    ThreeComponentModel,
    ValidationResult,
    find_optimal_k,
    get_cosmological_observations,
    get_extended_stages,
    get_physical_processes,
    physical_coherence,
    validate_model,
)

# Предсказания и интерпретации
from .predictions import (
    OBSERVATIONAL_DATA,
    STAGE_DURATIONS,
    TESTABLE_PREDICTIONS,
    PhysicalInterpretation,
    compare_with_observations,
    corrected_growth_model,
    final_summary,
    find_beautiful_coincidences,
    get_stage_durations,
    get_testable_predictions,
    physical_interpretation,
    quantitative_predictions,
    sensitivity_to_k,
    universal_formula,
    universal_formula_array,
)

# Функции визуализации
from .visualization import (
    COLORS,
    create_full_visualization,
    plot_coherence_evolution,
    plot_phase_diagram,
    plot_symmetry_breaking,
    plot_universe_distribution,
)

__all__ = [
    # Константы
    "UniverseConstants",
    "UNIVERSE_STAGES",
    "UNIVERSE_STAGES_SHORT",
    "FUTURE_STAGES",
    "M_REF_GEV",
    # Модели
    "CoherenceModel",
    "DepositionModel",
    "SymmetryBreaking",
    # Анализ
    "UnifiedAnalysis",
    "UniverseSimulator",
    "CoefficientAnalyzer",
    # Предсказания и интерпретации
    "PhysicalInterpretation",
    "physical_interpretation",
    "compare_with_observations",
    "universal_formula",
    "universal_formula_array",
    "find_beautiful_coincidences",
    "quantitative_predictions",
    "sensitivity_to_k",
    "corrected_growth_model",
    "get_testable_predictions",
    "get_stage_durations",
    "final_summary",
    "OBSERVATIONAL_DATA",
    "TESTABLE_PREDICTIONS",
    "STAGE_DURATIONS",
    # Физическая трёхкомпонентная модель
    "ThreeComponentModel",
    "PhysicalRecurrenceModel",
    "PhysicalParameters",
    "CosmologicalParams",
    "ValidationResult",
    "physical_coherence",
    "validate_model",
    "find_optimal_k",
    "get_extended_stages",
    "get_physical_processes",
    "get_cosmological_observations",
    "EXTENDED_STAGES",
    "PHYSICAL_PROCESSES",
    "COSMOLOGICAL_OBSERVATIONS",
    # Визуализация
    "plot_coherence_evolution",
    "plot_universe_distribution",
    "plot_phase_diagram",
    "plot_symmetry_breaking",
    "create_full_visualization",
    "COLORS",
]
