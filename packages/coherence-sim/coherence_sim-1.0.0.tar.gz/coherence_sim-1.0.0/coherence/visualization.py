"""
Визуализация моделей когерентности.

Этот модуль содержит функции для построения графиков
и визуализации результатов анализа.
"""

from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

from .analysis import UnifiedAnalysis, UniverseSimulator
from .constants import UNIVERSE_STAGES_SHORT, UniverseConstants
from .models import CoherenceModel, SymmetryBreaking

# Цветовая палитра
COLORS = {
    "primary": "#E63946",
    "secondary": "#457B9D",
    "accent": "#2A9D8F",
    "highlight": "#E9C46A",
    "background": "#F1FAEE",
    "dark": "#1D3557",
}


def plot_coherence_evolution(
    simulation_results: Dict,
    stages: List[str] = None,
    figsize: Tuple[int, int] = (14, 5),
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Построение графика эволюции когерентности.

    Parameters:
    -----------
    simulation_results : Dict
        Результаты из UnifiedAnalysis.run_simulation()
    stages : List[str], optional
        Названия этапов
    figsize : Tuple[int, int]
        Размер фигуры
    save_path : str, optional
        Путь для сохранения

    Returns:
    --------
    plt.Figure
        Фигура matplotlib
    """
    stages = stages or UNIVERSE_STAGES_SHORT

    fig, axes = plt.subplots(1, 2, figsize=figsize)
    x = np.arange(len(stages))

    colors = [COLORS["primary"], COLORS["secondary"], COLORS["accent"], COLORS["highlight"]]

    # График 1: Потенциальная когерентность
    ax = axes[0]
    for i, (key, data) in enumerate(simulation_results.items()):
        ax.plot(x, data["K"], "o-", color=colors[i], linewidth=2, markersize=5, label=data["label"])

    ax.set_xticks(x)
    ax.set_xticklabels(stages, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Потенциальная когерентность K(n)")
    ax.set_title("Эволюция когерентности")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # График 2: Накопленная когерентность
    ax = axes[1]
    for i, (key, data) in enumerate(simulation_results.items()):
        ax.fill_between(x, 0, data["Total"], alpha=0.2, color=colors[i])
        ax.plot(x, data["Total"], "-", color=colors[i], linewidth=2, label=data["label"])

    ax.set_xticks(x)
    ax.set_xticklabels(stages, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Накопленная когерентность")
    ax.set_title("Накопление сложности во Вселенной")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")

    return fig


def plot_universe_distribution(
    universes: List[Dict],
    constants: UniverseConstants = None,
    figsize: Tuple[int, int] = (15, 5),
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Построение распределений параметров случайных вселенных.

    Parameters:
    -----------
    universes : List[Dict]
        Список вселенных из UniverseSimulator.generate()
    constants : UniverseConstants, optional
        Константы нашей Вселенной для отметки
    figsize : Tuple[int, int]
        Размер фигуры
    save_path : str, optional
        Путь для сохранения

    Returns:
    --------
    plt.Figure
        Фигура matplotlib
    """
    constants = constants or UniverseConstants()

    fig, axes = plt.subplots(1, 3, figsize=figsize)

    # График 1: Распределение k
    ax = axes[0]
    k_values = [u["k"] for u in universes]
    ax.hist(k_values, bins=30, alpha=0.7, color=COLORS["secondary"], edgecolor="white")
    ax.axvline(
        constants.k_observed,
        color=COLORS["primary"],
        linestyle="--",
        linewidth=2,
        label=f"Наша Вселенная: k={constants.k_observed:.4f}",
    )
    ax.set_xlabel("Голографический параметр k")
    ax.set_ylabel("Количество вселенных")
    ax.set_title("Распределение k")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # График 2: Распределение α_eff
    ax = axes[1]
    alpha_values = [u["alpha_eff"] for u in universes]
    ax.hist(alpha_values, bins=30, alpha=0.7, color=COLORS["accent"], edgecolor="white")
    ax.axvline(
        constants.effective_alpha(),
        color=COLORS["primary"],
        linestyle="--",
        linewidth=2,
        label=f"Наша Вселенная: α={constants.effective_alpha():.3f}",
    )
    ax.set_xlabel("Эффективный параметр α")
    ax.set_ylabel("Количество вселенных")
    ax.set_title("Распределение α_eff")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # График 3: Распределение финальной когерентности
    ax = axes[2]
    if "final_coherence" in universes[0]:
        coh_values = [u["final_coherence"] for u in universes]
        ax.hist(coh_values, bins=30, alpha=0.7, color=COLORS["highlight"], edgecolor="white")

        # Когерентность нашей Вселенной
        model = CoherenceModel(constants)
        K, _, _ = model.evolve(12, 1.0, constants.effective_alpha(), 0.2)
        ax.axvline(
            K[-1],
            color=COLORS["primary"],
            linestyle="--",
            linewidth=2,
            label=f"Наша Вселенная: K={K[-1]:.2f}",
        )
        ax.set_xlabel("Финальная когерентность K(N)")
        ax.set_ylabel("Количество вселенных")
        ax.set_title("Распределение когерентности")
        ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")

    return fig


def plot_phase_diagram(
    alpha_range: Tuple[float, float] = (0.1, 0.9),
    n_points: int = 50,
    our_alpha: Optional[float] = None,
    figsize: Tuple[int, int] = (8, 6),
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Построение фазовой диаграммы α vs рост когерентности.

    Parameters:
    -----------
    alpha_range : Tuple[float, float]
        Диапазон α
    n_points : int
        Количество точек
    our_alpha : float, optional
        Значение α для нашей Вселенной
    figsize : Tuple[int, int]
        Размер фигуры
    save_path : str, optional
        Путь для сохранения

    Returns:
    --------
    plt.Figure
        Фигура matplotlib
    """
    model = CoherenceModel()
    alphas = np.linspace(alpha_range[0], alpha_range[1], n_points)
    growth_factors = [model.growth_factor(a, 12) for a in alphas]

    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(alphas, growth_factors, color=COLORS["secondary"], linewidth=2)
    ax.fill_between(alphas, 1, growth_factors, alpha=0.2, color=COLORS["secondary"])

    if our_alpha is None:
        our_alpha = UniverseConstants().effective_alpha()

    our_growth = model.growth_factor(our_alpha, 12)
    ax.axvline(
        our_alpha,
        color=COLORS["primary"],
        linestyle="--",
        linewidth=2,
        label=f"Наша Вселенная: α={our_alpha:.3f}",
    )
    ax.axhline(our_growth, color=COLORS["primary"], linestyle=":", alpha=0.5)
    ax.scatter([our_alpha], [our_growth], color=COLORS["primary"], s=100, zorder=5)

    ax.set_xlabel("Эффективный параметр α")
    ax.set_ylabel("Фактор роста когерентности K(N)/K(0)")
    ax.set_title("Фазовая диаграмма: α vs рост")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")

    return fig


def plot_symmetry_breaking(
    figsize: Tuple[int, int] = (8, 6), save_path: Optional[str] = None
) -> plt.Figure:
    """
    Построение графика спонтанного нарушения симметрии.

    Returns:
    --------
    plt.Figure
        Фигура matplotlib
    """
    phi, V_sym, V_broken = SymmetryBreaking.phase_transition()

    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(phi, V_sym, color=COLORS["primary"], linewidth=2, label="Высокая T: Симметрия")
    ax.plot(
        phi, V_broken, color=COLORS["secondary"], linewidth=2, label="Низкая T: Нарушение симметрии"
    )

    ax.set_xlabel("Поле φ")
    ax.set_ylabel("Потенциал V(φ)")
    ax.set_title("Спонтанное нарушение симметрии")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")

    return fig


def create_full_visualization(
    save_path: str = "coherence_analysis.png", n_universes: int = 500
) -> Tuple[plt.Figure, Dict]:
    """
    Создание полной визуализации (9 графиков).

    Parameters:
    -----------
    save_path : str
        Путь для сохранения
    n_universes : int
        Количество случайных вселенных

    Returns:
    --------
    fig : plt.Figure
        Фигура matplotlib
    results : Dict
        Результаты анализа
    """
    analysis = UnifiedAnalysis()
    simulator = UniverseSimulator()

    # Получаем данные
    correspondence = analysis.analyze_correspondence()
    simulation = analysis.run_simulation()
    universes = simulator.generate(n_universes, with_coherence=True)

    # Создаём фигуру
    fig = plt.figure(figsize=(18, 14))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)

    stages = UNIVERSE_STAGES_SHORT
    x = np.arange(len(stages))
    colors = [COLORS["primary"], COLORS["secondary"], COLORS["accent"], COLORS["highlight"]]

    # =========== ГРАФИК 1: Эволюция когерентности ===========
    ax1 = fig.add_subplot(gs[0, 0])
    for i, (key, data) in enumerate(simulation.items()):
        ax1.plot(
            x, data["K"], "o-", color=colors[i], linewidth=2, markersize=4, label=data["label"]
        )
    ax1.set_xticks(x)
    ax1.set_xticklabels(stages, rotation=45, ha="right", fontsize=7)
    ax1.set_ylabel("K(n)")
    ax1.set_title("Эволюция когерентности")
    ax1.legend(fontsize=7)
    ax1.grid(True, alpha=0.3)

    # =========== ГРАФИК 2: Накопленная когерентность ===========
    ax2 = fig.add_subplot(gs[0, 1])
    for i, (key, data) in enumerate(simulation.items()):
        ax2.fill_between(x, 0, data["Total"], alpha=0.2, color=colors[i])
        ax2.plot(x, data["Total"], "-", color=colors[i], linewidth=2)
    ax2.set_xticks(x)
    ax2.set_xticklabels(stages, rotation=45, ha="right", fontsize=7)
    ax2.set_ylabel("Накопленная когерентность")
    ax2.set_title("Накопление сложности")
    ax2.grid(True, alpha=0.3)

    # =========== ГРАФИК 3: Информация о константах ===========
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.axis("off")
    text = f"""
СВЯЗЬ КОНСТАНТ

α = {correspondence['alpha_fine_structure']:.10f}
1/α ≈ {correspondence['inverse_alpha']:.2f}

k_наблюд = {correspondence['k_observed']:.6f}
k_теорет = {correspondence['k_theoretical']:.6f}
Ошибка: {correspondence['k_error_percent']:.2f}%

k/α ≈ {correspondence['k_over_alpha']:.2f}

Формула:
k = π × α × ln(1/A_s) / n_s

α_eff ≈ {correspondence['alpha_effective']:.4f}
"""
    ax3.text(
        0.05,
        0.95,
        text,
        transform=ax3.transAxes,
        fontsize=9,
        verticalalignment="top",
        fontfamily="monospace",
        bbox=dict(boxstyle="round", facecolor=COLORS["background"], alpha=0.9),
    )

    # =========== ГРАФИК 4: Распределение k ===========
    ax4 = fig.add_subplot(gs[1, 0])
    k_values = [u["k"] for u in universes]
    ax4.hist(k_values, bins=30, alpha=0.7, color=COLORS["secondary"], edgecolor="white")
    ax4.axvline(
        analysis.constants.k_observed,
        color=COLORS["primary"],
        linestyle="--",
        linewidth=2,
        label="Наша Вселенная",
    )
    ax4.set_xlabel("k")
    ax4.set_ylabel("Количество")
    ax4.set_title("Распределение k")
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # =========== ГРАФИК 5: k vs α_eff ===========
    ax5 = fig.add_subplot(gs[1, 1])
    k_vals = [u["k"] for u in universes]
    alpha_vals = [u["alpha_eff"] for u in universes]
    growth_vals = [u["growth_factor"] for u in universes]
    scatter = ax5.scatter(k_vals, alpha_vals, c=growth_vals, cmap="viridis", alpha=0.6, s=15)
    ax5.axvline(analysis.constants.k_observed, color=COLORS["primary"], linestyle="--", alpha=0.7)
    ax5.set_xlabel("k")
    ax5.set_ylabel("α_eff")
    ax5.set_title("Связь k и α_eff")
    plt.colorbar(scatter, ax=ax5, label="Рост")
    ax5.grid(True, alpha=0.3)

    # =========== ГРАФИК 6: Распределение когерентности ===========
    ax6 = fig.add_subplot(gs[1, 2])
    coh_vals = [u["final_coherence"] for u in universes]
    ax6.hist(coh_vals, bins=30, alpha=0.7, color=COLORS["accent"], edgecolor="white")
    model = CoherenceModel()
    K_our, _, _ = model.evolve(12, 1.0, analysis.constants.effective_alpha(), 0.2)
    ax6.axvline(K_our[-1], color=COLORS["primary"], linestyle="--", linewidth=2)
    ax6.set_xlabel("K(N)")
    ax6.set_ylabel("Количество")
    ax6.set_title("Распределение когерентности")
    ax6.grid(True, alpha=0.3)

    # =========== ГРАФИК 7: Формулы ===========
    ax7 = fig.add_subplot(gs[2, 0])
    ax7.axis("off")
    formula = r"""
$\mathbf{Модель:}$

$K(n) = K_0 + \alpha \cdot \sum_{k=0}^{n-1} \frac{K(k)}{N - k}$

$\mathbf{Связь:}$

$\alpha_{eff} = \frac{k}{100 \cdot \alpha_{fs}}$

$\mathbf{Для\ нашей\ Вселенной:}$

$\alpha_{eff} \approx 0.66 \approx \frac{2}{3}$
"""
    ax7.text(
        0.5,
        0.5,
        formula,
        transform=ax7.transAxes,
        fontsize=12,
        verticalalignment="center",
        horizontalalignment="center",
        bbox=dict(boxstyle="round", facecolor="#FFF3B0", alpha=0.9),
    )

    # =========== ГРАФИК 8: Фазовая диаграмма ===========
    ax8 = fig.add_subplot(gs[2, 1])
    alphas = np.linspace(0.1, 0.9, 50)
    growth_factors = [model.growth_factor(a, 12) for a in alphas]
    ax8.plot(alphas, growth_factors, color=COLORS["secondary"], linewidth=2)
    ax8.fill_between(alphas, 1, growth_factors, alpha=0.2, color=COLORS["secondary"])
    our_alpha = analysis.constants.effective_alpha()
    ax8.axvline(our_alpha, color=COLORS["primary"], linestyle="--", linewidth=2)
    ax8.set_xlabel("α")
    ax8.set_ylabel("Рост K(N)/K(0)")
    ax8.set_title("Фазовая диаграмма")
    ax8.grid(True, alpha=0.3)

    # =========== ГРАФИК 9: Сравнение формул k ===========
    ax9 = fig.add_subplot(gs[2, 2])
    constants = UniverseConstants()
    formulas = {
        "Наблюд.": constants.k_observed,
        "π×α×...": constants.k_formula_new(),
        "(49/8)×α×Δm": constants.k_formula_old(),
    }
    bars = ax9.bar(
        formulas.keys(),
        formulas.values(),
        color=[COLORS["primary"], COLORS["secondary"], COLORS["accent"]],
        edgecolor="white",
        linewidth=2,
    )
    for bar, val in zip(bars, formulas.values()):
        ax9.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            f"{val:.4f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax9.set_ylabel("k")
    ax9.set_title("Сравнение формул")
    ax9.grid(True, alpha=0.3, axis="y")

    # Общий заголовок
    fig.suptitle(
        "Когерентность Вселенной: Объединённый анализ", fontsize=14, fontweight="bold", y=0.98
    )

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")

    return fig, {"correspondence": correspondence, "simulation": simulation, "universes": universes}
