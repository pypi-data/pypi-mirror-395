"""Matplotlib plotting with iTerm2 inline image support.

Renders high-quality plots directly in iTerm2 terminal using the
inline image protocol (ESC ] 1337).

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import base64
import io
import os
import sys
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from aws_bedrock_cost_tool.core.models import CostData

# Professional color palette
COLORS = {
    "primary": "#2563eb",  # Blue
    "secondary": "#7c3aed",  # Purple
    "accent": "#059669",  # Green
    "warning": "#d97706",  # Amber
    "danger": "#dc2626",  # Red
    "neutral": "#6b7280",  # Gray
    "background": "#1f2937",  # Dark gray
    "text": "#f9fafb",  # Light gray
    "grid": "#374151",  # Medium gray
}

# Model colors for consistency
MODEL_COLORS = [
    "#3b82f6",  # Blue
    "#8b5cf6",  # Purple
    "#10b981",  # Emerald
    "#f59e0b",  # Amber
    "#ef4444",  # Red
    "#06b6d4",  # Cyan
    "#ec4899",  # Pink
    "#84cc16",  # Lime
    "#f97316",  # Orange
    "#6366f1",  # Indigo
]


def is_iterm2() -> bool:
    """Check if running in iTerm2."""
    term_program = os.environ.get("TERM_PROGRAM", "")
    return term_program == "iTerm.app"


def _send_image_to_iterm2(fig: Figure, name: str = "plot.png") -> None:
    """Send matplotlib figure to iTerm2 as inline image.

    Args:
        fig: Matplotlib figure to display
        name: Filename for the image
    """
    # Render to PNG in memory
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=COLORS["background"])
    buf.seek(0)

    # Base64 encode
    data = base64.b64encode(buf.read()).decode("ascii")
    buf.close()

    # iTerm2 inline image protocol
    # ESC ] 1337 ; File = [args] : base64 BEL
    escape_seq = f"\033]1337;File=inline=1;preserveAspectRatio=1;name={name}:{data}\a"
    sys.stdout.write(escape_seq)
    sys.stdout.write("\n")
    sys.stdout.flush()


def _setup_dark_style() -> None:
    """Configure matplotlib for dark terminal theme."""
    plt.style.use("dark_background")
    plt.rcParams.update(
        {
            "figure.facecolor": COLORS["background"],
            "axes.facecolor": COLORS["background"],
            "axes.edgecolor": COLORS["grid"],
            "axes.labelcolor": COLORS["text"],
            "text.color": COLORS["text"],
            "xtick.color": COLORS["text"],
            "ytick.color": COLORS["text"],
            "grid.color": COLORS["grid"],
            "grid.alpha": 0.3,
            "axes.grid": True,
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
        }
    )


def plot_time_series_iterm2(cost_data: CostData) -> None:
    """Plot time series of daily costs as iTerm2 inline image.

    Args:
        cost_data: Analyzed cost data
    """
    if not is_iterm2():
        print("Warning: Not running in iTerm2, image may not display.", file=sys.stderr)

    if not cost_data["daily_costs"]:
        print("No daily cost data available for plotting.", file=sys.stderr)
        return

    _setup_dark_style()

    # Extract data
    dates = [datetime.strptime(day["date"], "%Y-%m-%d") for day in cost_data["daily_costs"]]
    costs = [day["total_cost"] for day in cost_data["daily_costs"]]

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 5))

    # Plot area chart with gradient effect
    ax.fill_between(dates, costs, alpha=0.3, color=COLORS["primary"])  # type: ignore[arg-type]
    ax.plot(dates, costs, color=COLORS["primary"], linewidth=2, marker="o", markersize=4)  # type: ignore[arg-type]

    # Styling
    ax.set_title("AWS Bedrock Daily Costs", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Cost ($)", fontsize=11)

    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))  # type: ignore[no-untyped-call]
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # type: ignore[no-untyped-call]
    plt.xticks(rotation=45, ha="right")

    # Add cost annotations for peaks
    max_cost = max(costs)
    max_idx = costs.index(max_cost)
    ax.annotate(
        f"${max_cost:.2f}",
        xy=(dates[max_idx], max_cost),  # type: ignore[arg-type]
        xytext=(10, 10),
        textcoords="offset points",
        fontsize=9,
        color=COLORS["warning"],
        fontweight="bold",
    )

    # Add total in corner
    total = sum(costs)
    estimated = cost_data["has_estimated"]
    total_str = f"~${total:.2f}" if estimated else f"${total:.2f}"
    ax.text(
        0.98,
        0.98,
        f"Total: {total_str}",
        transform=ax.transAxes,
        fontsize=11,
        fontweight="bold",
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=COLORS["primary"], alpha=0.8),
    )

    plt.tight_layout()

    # Send to iTerm2
    _send_image_to_iterm2(fig, "daily_costs.png")
    plt.close(fig)


def plot_model_costs_iterm2(cost_data: CostData, top_n: int = 10) -> None:
    """Plot horizontal bar chart of model costs as iTerm2 inline image.

    Args:
        cost_data: Analyzed cost data
        top_n: Number of top models to display
    """
    if not is_iterm2():
        print("Warning: Not running in iTerm2, image may not display.", file=sys.stderr)

    if not cost_data["models"]:
        print("No model cost data available for plotting.", file=sys.stderr)
        return

    _setup_dark_style()

    # Get top models (reversed for horizontal bar chart)
    top_models = cost_data["models"][:top_n]
    top_models = list(reversed(top_models))

    names = [_shorten_model_name(m["model_name"]) for m in top_models]
    costs = [m["total_cost"] for m in top_models]
    colors = [MODEL_COLORS[i % len(MODEL_COLORS)] for i in range(len(top_models))]
    colors = list(reversed(colors))

    # Create figure
    fig, ax = plt.subplots(figsize=(10, max(4, len(top_models) * 0.6)))

    # Plot horizontal bars
    bars = ax.barh(names, costs, color=colors, height=0.7, edgecolor="none")

    # Add value labels
    for bar, cost in zip(bars, costs):
        width = bar.get_width()
        label = f"${cost:.2f}"
        ax.text(
            width + max(costs) * 0.02,
            bar.get_y() + bar.get_height() / 2,
            label,
            va="center",
            fontsize=9,
            color=COLORS["text"],
            fontweight="bold",
        )

    # Styling
    ax.set_title("AWS Bedrock Cost by Model", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Cost ($)", fontsize=11)
    ax.set_xlim(0, max(costs) * 1.2)

    # Remove y-axis spine
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    # Send to iTerm2
    _send_image_to_iterm2(fig, "model_costs.png")
    plt.close(fig)


def plot_cost_breakdown_iterm2(cost_data: CostData) -> None:
    """Plot pie chart of cost breakdown as iTerm2 inline image.

    Args:
        cost_data: Analyzed cost data
    """
    if not is_iterm2():
        print("Warning: Not running in iTerm2, image may not display.", file=sys.stderr)

    if not cost_data["models"]:
        print("No model cost data available for plotting.", file=sys.stderr)
        return

    _setup_dark_style()

    # Get models and group small ones
    models = cost_data["models"]
    total = sum(m["total_cost"] for m in models)

    # Group models < 5% as "Other"
    threshold = total * 0.05
    main_models = [m for m in models if m["total_cost"] >= threshold]
    other_cost = sum(m["total_cost"] for m in models if m["total_cost"] < threshold)

    labels = [_shorten_model_name(m["model_name"]) for m in main_models]
    sizes = [m["total_cost"] for m in main_models]
    colors = MODEL_COLORS[: len(main_models)]

    if other_cost > 0:
        labels.append("Other")
        sizes.append(other_cost)
        colors.append(COLORS["neutral"])

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot donut chart
    wedges, texts, autotexts = ax.pie(  # type: ignore[misc]
        sizes,
        labels=labels,
        colors=colors,
        autopct=lambda pct: f"${pct * total / 100:.2f}\n({pct:.1f}%)" if pct > 5 else "",
        startangle=90,
        pctdistance=0.75,
        wedgeprops=dict(width=0.5, edgecolor=COLORS["background"]),
    )

    # Style the labels
    for text in texts:
        text.set_color(COLORS["text"])
        text.set_fontsize(9)

    for autotext in autotexts:
        autotext.set_color(COLORS["text"])
        autotext.set_fontsize(8)
        autotext.set_fontweight("bold")

    # Add center text
    estimated = cost_data["has_estimated"]
    total_str = f"~${total:.2f}" if estimated else f"${total:.2f}"
    ax.text(
        0,
        0,
        f"Total\n{total_str}",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color=COLORS["text"],
    )

    ax.set_title("AWS Bedrock Cost Distribution", fontsize=14, fontweight="bold", pad=15)

    plt.tight_layout()

    # Send to iTerm2
    _send_image_to_iterm2(fig, "cost_breakdown.png")
    plt.close(fig)


def plot_token_usage_iterm2(cost_data: CostData, top_n: int = 5) -> None:
    """Plot stacked bar chart of token usage by model as iTerm2 inline image.

    Args:
        cost_data: Analyzed cost data
        top_n: Number of top models to display
    """
    if not is_iterm2():
        print("Warning: Not running in iTerm2, image may not display.", file=sys.stderr)

    if not cost_data["models"]:
        print("No model cost data available for plotting.", file=sys.stderr)
        return

    _setup_dark_style()

    # Get top models
    top_models = cost_data["models"][:top_n]

    # Extract token data
    names = []
    io_tokens = []
    cache_read = []
    cache_write = []

    for model in top_models:
        names.append(_shorten_model_name(model["model_name"]))

        io = 0.0
        cr = 0.0
        cw = 0.0

        for usage in model.get("usage_breakdown", []):
            usage_type = usage["usage_type"]
            qty = usage["quantity"]

            if "CacheRead" in usage_type:
                cr += qty
            elif "CacheWrite" in usage_type:
                cw += qty
            elif "TokenCount" in usage_type:
                io += qty

        io_tokens.append(io)
        cache_read.append(cr)
        cache_write.append(cw)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))

    x = range(len(names))
    width = 0.6

    # Stacked bars
    ax.bar(x, io_tokens, width, label="Input/Output", color=COLORS["primary"])
    ax.bar(x, cache_read, width, bottom=io_tokens, label="Cache Read", color=COLORS["accent"])
    ax.bar(
        x,
        cache_write,
        width,
        bottom=[i + c for i, c in zip(io_tokens, cache_read)],
        label="Cache Write",
        color=COLORS["warning"],
    )

    # Styling
    ax.set_title("Token Usage by Model (Millions)", fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel("Tokens (Millions)", fontsize=11)
    ax.set_xticks(list(x))
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.legend(loc="upper right", framealpha=0.9)

    # Add total labels on top
    for i, (io, cr, cw) in enumerate(zip(io_tokens, cache_read, cache_write)):
        total = io + cr + cw
        if total > 0:
            ax.text(
                i,
                total + max(io_tokens) * 0.02,
                f"{total:.1f}M",
                ha="center",
                va="bottom",
                fontsize=8,
                fontweight="bold",
                color=COLORS["text"],
            )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    # Send to iTerm2
    _send_image_to_iterm2(fig, "token_usage.png")
    plt.close(fig)


def plot_all_iterm2(cost_data: CostData) -> None:
    """Generate all iTerm2 plots.

    Args:
        cost_data: Analyzed cost data
    """
    print("\n📊 Generating visualizations...\n", file=sys.stderr)

    plot_time_series_iterm2(cost_data)
    print("", file=sys.stderr)  # Spacing

    plot_model_costs_iterm2(cost_data)
    print("", file=sys.stderr)

    plot_cost_breakdown_iterm2(cost_data)
    print("", file=sys.stderr)

    plot_token_usage_iterm2(cost_data)


def _shorten_model_name(model_name: str) -> str:
    """Shorten model name for display.

    Args:
        model_name: Full model name

    Returns:
        Shortened model name
    """
    short = model_name.replace(" (Amazon Bedrock Edition)", "")

    if len(short) > 25:
        short = short[:22] + "..."

    return short
