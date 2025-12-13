"""Plotting utilities for Veox."""

import logging
from typing import Dict, Any, List, Optional
import warnings

logger = logging.getLogger(__name__)

def plot_evolution(
    history_data: Dict[str, Any],
    title: str = "Evolution Progress",
    save_path: Optional[str] = None
) -> None:
    """
    Plot evolution history (fitness over generations).
    
    Args:
        history_data: Dictionary returned by /jobs/{job_id}/history endpoint.
                      Expected keys: 'generations', and optionally 'individuals'.
        title: Title of the plot.
        save_path: If provided, save stats plot to this file path.
    """
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
        import seaborn as sns
    except ImportError:
        logger.warning("Optional dependencies 'matplotlib' and 'seaborn' not found. Plotting skipped.")
        print("⚠️ Plotting skipped: matplotlib/seaborn not installed.")
        return

    generations = history_data.get("generations", [])
    if not generations:
        logger.warning("No generation data to plot.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(generations)
    # Ensure numeric types
    for col in ['gen', 'min_fitness', 'avg_fitness', 'max_fitness']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col])

    # Setup plot style
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot lines
    sns.lineplot(data=df, x="gen", y="max_fitness", label="Max Fitness", ax=ax, color="green", linewidth=2)
    sns.lineplot(data=df, x="gen", y="avg_fitness", label="Avg Fitness", ax=ax, color="blue", linestyle="--")
    
    # Fill between min and max
    ax.fill_between(df["gen"], df["min_fitness"], df["max_fitness"], alpha=0.15, color="green")

    # Plot individuals if available
    individuals = history_data.get("individuals", [])
    if individuals:
        ind_df = pd.DataFrame(individuals)
        if not ind_df.empty:
            sns.scatterplot(
                data=ind_df, 
                x="generation", 
                y="fitness", 
                alpha=0.3, 
                size=3, 
                color="gray", 
                ax=ax, 
                zorder=0,
                legend=False
            )

    ax.set_title(title)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"📊 Evolution plot saved to {save_path}")
    else:
        plt.show()
    
    # Clean up
    plt.close(fig)
