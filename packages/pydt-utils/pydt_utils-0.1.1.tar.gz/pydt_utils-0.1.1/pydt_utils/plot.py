"""
Plotting Utilities Module

This module provides visualization functions for thermal cycle analysis:
- Thermal cycle plotting
- Brazing stage visualization
- Anomaly highlighting
- Temperature distribution plots
- Cycle comparison
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Optional, Union, Tuple
from matplotlib.figure import Figure
from matplotlib.axes import Axes


def plot_thermal_cycle(
    time: np.ndarray,
    temperature: np.ndarray,
    stages: Optional[List[Dict]] = None,
    title: str = "Thermal Cycle",
    xlabel: str = "Time (min)",
    ylabel: str = "Temperature (°C)",
    figsize: Tuple[int, int] = (12, 6),
    save_path: Optional[str] = None,
    show: bool = True
) -> Figure:
    """
    Plot a complete thermal cycle with optional stage annotations.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values
        stages: Optional list of stage dictionaries from segment_thermal_cycle()
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        figsize: Figure size (width, height)
        save_path: Optional path to save figure
        show: Whether to display the plot
    
    Returns:
        Matplotlib Figure object
    
    Example:
        >>> fig = plot_thermal_cycle(time, temp, stages=stages, save_path='cycle.png')
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot main temperature curve
    ax.plot(time, temperature, 'b-', linewidth=2, label='Temperature')
    
    # Add stage annotations if provided
    if stages is not None:
        colors = {
            'ramp_up': 'orange',
            'soak': 'green',
            'ramp_down': 'purple',
            'cool': 'cyan'
        }
        
        for stage in stages:
            start_idx = stage['start_idx']
            end_idx = stage['end_idx']
            stage_type = stage['stage_type']
            
            # Highlight stage region
            ax.axvspan(
                time[start_idx],
                time[end_idx],
                alpha=0.2,
                color=colors.get(stage_type, 'gray'),
                label=stage_type.replace('_', ' ').title()
            )
    
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Remove duplicate labels in legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='best')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def plot_brazing_stages(
    time: np.ndarray,
    temperature: np.ndarray,
    liquidus_temp: float,
    stages: Optional[List[Dict]] = None,
    target_temp: Optional[float] = None,
    figsize: Tuple[int, int] = (12, 6),
    save_path: Optional[str] = None,
    show: bool = True
) -> Figure:
    """
    Plot thermal cycle with brazing-specific annotations.
    
    Highlights liquidus temperature crossing and brazing zones.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values
        liquidus_temp: Liquidus temperature of material (°C)
        stages: Optional list of brazing stages
        target_temp: Optional target brazing temperature
        figsize: Figure size (width, height)
        save_path: Optional path to save figure
        show: Whether to display the plot
    
    Returns:
        Matplotlib Figure object
    
    Example:
        >>> fig = plot_brazing_stages(time, temp, liquidus_temp=450, target_temp=600)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot temperature curve
    ax.plot(time, temperature, 'b-', linewidth=2, label='Temperature')
    
    # Add liquidus temperature line
    ax.axhline(
        liquidus_temp,
        color='red',
        linestyle='--',
        linewidth=2,
        label=f'Liquidus Temp ({liquidus_temp}°C)'
    )
    
    # Add target temperature line if provided
    if target_temp is not None:
        ax.axhline(
            target_temp,
            color='green',
            linestyle='--',
            linewidth=2,
            label=f'Target Temp ({target_temp}°C)'
        )
    
    # Highlight region above liquidus (brazing zone)
    above_liquidus = temperature > liquidus_temp
    if np.any(above_liquidus):
        # Find continuous regions above liquidus
        in_zone = False
        zone_start = 0
        
        for i in range(len(temperature)):
            if above_liquidus[i] and not in_zone:
                zone_start = i
                in_zone = True
            elif (not above_liquidus[i] or i == len(temperature) - 1) and in_zone:
                zone_end = i - 1 if not above_liquidus[i] else i
                ax.axvspan(
                    time[zone_start],
                    time[zone_end],
                    alpha=0.3,
                    color='yellow',
                    label='Brazing Zone' if zone_start == np.where(above_liquidus)[0][0] else ''
                )
                in_zone = False
    
    ax.set_xlabel('Time (min)', fontsize=12)
    ax.set_ylabel('Temperature (°C)', fontsize=12)
    ax.set_title('Brazing Cycle Analysis', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Remove duplicate labels
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='best')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def plot_with_anomalies(
    time: np.ndarray,
    temperature: np.ndarray,
    anomaly_indices: Union[List[int], np.ndarray],
    anomaly_type: str = "Anomaly",
    figsize: Tuple[int, int] = (12, 6),
    save_path: Optional[str] = None,
    show: bool = True
) -> Figure:
    """
    Plot temperature data with anomalies highlighted.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values
        anomaly_indices: Indices of detected anomalies
        anomaly_type: Type of anomaly for legend (e.g., "Spike", "Overshoot")
        figsize: Figure size (width, height)
        save_path: Optional path to save figure
        show: Whether to display the plot
    
    Returns:
        Matplotlib Figure object
    
    Example:
        >>> spikes = [100, 250, 500]
        >>> fig = plot_with_anomalies(time, temp, spikes, anomaly_type="Temperature Spike")
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot temperature curve
    ax.plot(time, temperature, 'b-', linewidth=2, label='Temperature', alpha=0.7)
    
    # Highlight anomalies
    if len(anomaly_indices) > 0:
        anomaly_times = time[anomaly_indices]
        anomaly_temps = temperature[anomaly_indices]
        
        ax.scatter(
            anomaly_times,
            anomaly_temps,
            color='red',
            s=100,
            marker='o',
            edgecolors='darkred',
            linewidths=2,
            label=anomaly_type,
            zorder=5
        )
    
    ax.set_xlabel('Time (min)', fontsize=12)
    ax.set_ylabel('Temperature (°C)', fontsize=12)
    ax.set_title(f'Thermal Cycle with {anomaly_type} Detection', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def plot_temperature_distribution(
    x: np.ndarray,
    temperature: Union[np.ndarray, List[np.ndarray]],
    time_labels: Optional[Union[str, List[str]]] = None,
    xlabel: str = "Position (m)",
    ylabel: str = "Temperature (°C)",
    title: str = "Temperature Distribution",
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None,
    show: bool = True
) -> Figure:
    """
    Plot spatial temperature distribution at one or more time points.
    
    Args:
        x: Array of spatial positions
        temperature: Temperature array or list of arrays for multiple time points
        time_labels: Label(s) for time point(s)
        xlabel: X-axis label
        ylabel: Y-axis label
        title: Plot title
        figsize: Figure size (width, height)
        save_path: Optional path to save figure
        show: Whether to display the plot
    
    Returns:
        Matplotlib Figure object
    
    Example:
        >>> x = np.linspace(0, 0.1, 50)
        >>> T1 = 600 * np.exp(-x/0.02)
        >>> T2 = 400 * np.exp(-x/0.02)
        >>> fig = plot_temperature_distribution(x, [T1, T2], time_labels=['t=0', 't=100'])
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Handle single or multiple temperature arrays
    if isinstance(temperature, np.ndarray) and temperature.ndim == 1:
        temperature = [temperature]
        time_labels = [time_labels] if time_labels else ['Temperature']
    elif time_labels is None:
        time_labels = [f'Time {i}' for i in range(len(temperature))]
    
    # Plot each temperature distribution
    colors = plt.cm.viridis(np.linspace(0, 1, len(temperature)))
    
    for i, (temp, label) in enumerate(zip(temperature, time_labels)):
        ax.plot(x, temp, linewidth=2, label=label, color=colors[i])
    
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def create_cycle_comparison(
    cycles_dict: Dict[str, Tuple[np.ndarray, np.ndarray]],
    title: str = "Thermal Cycle Comparison",
    figsize: Tuple[int, int] = (12, 6),
    save_path: Optional[str] = None,
    show: bool = True
) -> Figure:
    """
    Compare multiple thermal cycles on the same plot.
    
    Args:
        cycles_dict: Dictionary mapping cycle names to (time, temperature) tuples
        title: Plot title
        figsize: Figure size (width, height)
        save_path: Optional path to save figure
        show: Whether to display the plot
    
    Returns:
        Matplotlib Figure object
    
    Example:
        >>> cycles = {
        ...     'Cycle 1': (time1, temp1),
        ...     'Cycle 2': (time2, temp2),
        ...     'Cycle 3': (time3, temp3)
        ... }
        >>> fig = create_cycle_comparison(cycles)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Generate distinct colors
    colors = plt.cm.tab10(np.linspace(0, 1, len(cycles_dict)))
    
    for i, (name, (time, temp)) in enumerate(cycles_dict.items()):
        ax.plot(time, temp, linewidth=2, label=name, color=colors[i])
    
    ax.set_xlabel('Time (min)', fontsize=12)
    ax.set_ylabel('Temperature (°C)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def plot_ramp_rate_analysis(
    time: np.ndarray,
    temperature: np.ndarray,
    ramp_rates: np.ndarray,
    expected_rate: Optional[float] = None,
    figsize: Tuple[int, int] = (12, 8),
    save_path: Optional[str] = None,
    show: bool = True
) -> Figure:
    """
    Create a dual-axis plot showing temperature and ramp rate.
    
    Args:
        time: Array of time values
        temperature: Array of temperature values
        ramp_rates: Array of calculated ramp rates
        expected_rate: Optional expected ramp rate for comparison
        figsize: Figure size (width, height)
        save_path: Optional path to save figure
        show: Whether to display the plot
    
    Returns:
        Matplotlib Figure object
    
    Example:
        >>> from pydt_utils.cycle import calculate_ramp_rate
        >>> rates = calculate_ramp_rate(time, temp)
        >>> fig = plot_ramp_rate_analysis(time, temp, rates, expected_rate=5.0)
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
    
    # Plot temperature
    ax1.plot(time, temperature, 'b-', linewidth=2)
    ax1.set_ylabel('Temperature (°C)', fontsize=12)
    ax1.set_title('Temperature and Ramp Rate Analysis', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Plot ramp rate
    ax2.plot(time, ramp_rates, 'r-', linewidth=2, label='Actual Rate')
    
    if expected_rate is not None:
        ax2.axhline(
            expected_rate,
            color='green',
            linestyle='--',
            linewidth=2,
            label=f'Expected Rate ({expected_rate}°C/min)'
        )
    
    ax2.axhline(0, color='black', linestyle='-', linewidth=0.5)
    ax2.set_xlabel('Time (min)', fontsize=12)
    ax2.set_ylabel('Ramp Rate (°C/min)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='best')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig
