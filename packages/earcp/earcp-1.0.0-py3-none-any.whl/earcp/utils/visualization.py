"""
Visualization utilities for EARCP diagnostics.

Copyright (c) 2025 Mike Amega. All rights reserved.
"""

import numpy as np
from typing import Optional, Dict, Any
import matplotlib.pyplot as plt


def plot_weights(
    weights_history: np.ndarray,
    expert_names: Optional[list] = None,
    figsize: tuple = (12, 6),
    save_path: Optional[str] = None
):
    """
    Plot evolution of expert weights over time.

    Parameters
    ----------
    weights_history : np.ndarray
        Weight history (shape: T x n_experts).
    expert_names : list, optional
        Names for each expert.
    figsize : tuple
        Figure size.
    save_path : str, optional
        Path to save figure.
    """
    T, n_experts = weights_history.shape

    if expert_names is None:
        expert_names = [f'Expert {i+1}' for i in range(n_experts)]

    plt.figure(figsize=figsize)

    for i in range(n_experts):
        plt.plot(weights_history[:, i], label=expert_names[i], linewidth=2)

    plt.xlabel('Time Step', fontsize=12)
    plt.ylabel('Weight', fontsize=12)
    plt.title('Expert Weights Evolution', fontsize=14, fontweight='bold')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()


def plot_performance(
    performance_history: np.ndarray,
    coherence_history: np.ndarray,
    expert_names: Optional[list] = None,
    figsize: tuple = (14, 6),
    save_path: Optional[str] = None
):
    """
    Plot performance and coherence scores.

    Parameters
    ----------
    performance_history : np.ndarray
        Performance score history (shape: T x n_experts).
    coherence_history : np.ndarray
        Coherence score history (shape: T x n_experts).
    expert_names : list, optional
        Names for each expert.
    figsize : tuple
        Figure size.
    save_path : str, optional
        Path to save figure.
    """
    T, n_experts = performance_history.shape

    if expert_names is None:
        expert_names = [f'Expert {i+1}' for i in range(n_experts)]

    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # Performance plot
    for i in range(n_experts):
        axes[0].plot(
            performance_history[:, i],
            label=expert_names[i],
            linewidth=2
        )
    axes[0].set_xlabel('Time Step', fontsize=12)
    axes[0].set_ylabel('Performance Score', fontsize=12)
    axes[0].set_title('Performance Evolution', fontsize=14, fontweight='bold')
    axes[0].legend(loc='best')
    axes[0].grid(True, alpha=0.3)

    # Coherence plot
    for i in range(n_experts):
        axes[1].plot(
            coherence_history[:, i],
            label=expert_names[i],
            linewidth=2
        )
    axes[1].set_xlabel('Time Step', fontsize=12)
    axes[1].set_ylabel('Coherence Score', fontsize=12)
    axes[1].set_title('Coherence Evolution', fontsize=14, fontweight='bold')
    axes[1].legend(loc='best')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()


def plot_diagnostics(
    diagnostics: Dict[str, Any],
    expert_names: Optional[list] = None,
    figsize: tuple = (16, 10),
    save_path: Optional[str] = None
):
    """
    Plot comprehensive diagnostics.

    Parameters
    ----------
    diagnostics : dict
        Diagnostics dictionary from EARCP.get_diagnostics().
    expert_names : list, optional
        Names for each expert.
    figsize : tuple
        Figure size.
    save_path : str, optional
        Path to save figure.
    """
    weights_hist = diagnostics['weights_history']
    perf_hist = diagnostics['performance_history']
    coh_hist = diagnostics['coherence_history']
    cum_loss = diagnostics.get('cumulative_loss', None)

    T, n_experts = weights_hist.shape

    if expert_names is None:
        expert_names = [f'Expert {i+1}' for i in range(n_experts)]

    # Create subplots
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

    # 1. Weights evolution
    ax1 = fig.add_subplot(gs[0, :])
    for i in range(n_experts):
        ax1.plot(weights_hist[:, i], label=expert_names[i], linewidth=2)
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('Weight')
    ax1.set_title('Expert Weights Evolution', fontweight='bold')
    ax1.legend(loc='best', ncol=min(n_experts, 5))
    ax1.grid(True, alpha=0.3)

    # 2. Performance scores
    ax2 = fig.add_subplot(gs[1, 0])
    for i in range(n_experts):
        ax2.plot(perf_hist[:, i], label=expert_names[i], linewidth=2)
    ax2.set_xlabel('Time Step')
    ax2.set_ylabel('Performance Score')
    ax2.set_title('Performance Evolution', fontweight='bold')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)

    # 3. Coherence scores
    ax3 = fig.add_subplot(gs[1, 1])
    for i in range(n_experts):
        ax3.plot(coh_hist[:, i], label=expert_names[i], linewidth=2)
    ax3.set_xlabel('Time Step')
    ax3.set_ylabel('Coherence Score')
    ax3.set_title('Coherence Evolution', fontweight='bold')
    ax3.legend(loc='best')
    ax3.grid(True, alpha=0.3)

    # 4. Weight distribution (final)
    ax4 = fig.add_subplot(gs[2, 0])
    final_weights = weights_hist[-1, :]
    colors = plt.cm.viridis(np.linspace(0, 1, n_experts))
    bars = ax4.bar(range(n_experts), final_weights, color=colors)
    ax4.set_xlabel('Expert')
    ax4.set_ylabel('Final Weight')
    ax4.set_title('Final Weight Distribution', fontweight='bold')
    ax4.set_xticks(range(n_experts))
    ax4.set_xticklabels(expert_names, rotation=45, ha='right')
    ax4.grid(True, alpha=0.3, axis='y')

    # 5. Cumulative loss (if available)
    ax5 = fig.add_subplot(gs[2, 1])
    if cum_loss is not None:
        colors = plt.cm.viridis(np.linspace(0, 1, n_experts))
        bars = ax5.bar(range(n_experts), cum_loss, color=colors)
        ax5.set_xlabel('Expert')
        ax5.set_ylabel('Cumulative Loss')
        ax5.set_title('Cumulative Loss by Expert', fontweight='bold')
        ax5.set_xticks(range(n_experts))
        ax5.set_xticklabels(expert_names, rotation=45, ha='right')
        ax5.grid(True, alpha=0.3, axis='y')
    else:
        ax5.text(
            0.5, 0.5, 'Cumulative loss not available',
            ha='center', va='center', transform=ax5.transAxes
        )

    plt.suptitle('EARCP Diagnostics', fontsize=16, fontweight='bold', y=0.995)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()


def plot_regret(
    cumulative_losses: np.ndarray,
    ensemble_cumulative_loss: float,
    expert_names: Optional[list] = None,
    figsize: tuple = (10, 6),
    save_path: Optional[str] = None
):
    """
    Plot regret analysis.

    Parameters
    ----------
    cumulative_losses : np.ndarray
        Cumulative loss for each expert.
    ensemble_cumulative_loss : float
        Cumulative loss of the ensemble.
    expert_names : list, optional
        Names for each expert.
    figsize : tuple
        Figure size.
    save_path : str, optional
        Path to save figure.
    """
    n_experts = len(cumulative_losses)

    if expert_names is None:
        expert_names = [f'Expert {i+1}' for i in range(n_experts)]

    # Compute regret vs best single expert
    best_expert_loss = np.min(cumulative_losses)
    regret = ensemble_cumulative_loss - best_expert_loss

    plt.figure(figsize=figsize)

    # Plot expert losses
    colors = plt.cm.viridis(np.linspace(0, 1, n_experts))
    x = np.arange(n_experts)
    bars = plt.bar(x, cumulative_losses, color=colors, alpha=0.7, label='Experts')

    # Plot ensemble loss
    plt.axhline(
        y=ensemble_cumulative_loss,
        color='red',
        linestyle='--',
        linewidth=2,
        label=f'Ensemble (loss={ensemble_cumulative_loss:.4f})'
    )

    # Highlight best expert
    best_idx = np.argmin(cumulative_losses)
    bars[best_idx].set_edgecolor('green')
    bars[best_idx].set_linewidth(3)

    plt.xlabel('Expert', fontsize=12)
    plt.ylabel('Cumulative Loss', fontsize=12)
    plt.title(
        f'Regret Analysis (Regret = {regret:.4f})',
        fontsize=14,
        fontweight='bold'
    )
    plt.xticks(x, expert_names, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()
