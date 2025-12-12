"""
Thermal Simulation Module

This module provides functions for thermal physics calculations and simulations:
- Heat flux calculations (Fourier's law)
- 1D thermal diffusion solver
- Dimensionless numbers (Biot, Fourier)
- Cooling time estimation
"""

import numpy as np
from typing import Tuple, Optional, Callable, Union


def calculate_heat_flux(
    temperature_gradient: Union[float, np.ndarray],
    thermal_conductivity: float
) -> Union[float, np.ndarray]:
    """
    Calculate heat flux using Fourier's law of heat conduction.
    
    q = -k * dT/dx
    
    Args:
        temperature_gradient: Temperature gradient dT/dx (K/m or °C/m)
        thermal_conductivity: Thermal conductivity k (W/m·K)
    
    Returns:
        Heat flux q (W/m²)
    
    Example:
        >>> gradient = 100  # K/m
        >>> k = 15  # W/m·K (steel)
        >>> flux = calculate_heat_flux(gradient, k)
    """
    return -thermal_conductivity * temperature_gradient


def calculate_biot_number(
    h: float,
    L: float,
    k: float
) -> float:
    """
    Calculate the Biot number for heat transfer analysis.
    
    Bi = hL/k
    
    Bi << 1 (< 0.1): Lumped capacitance model valid (uniform internal temperature)
    Bi >> 1 (> 10): Large internal temperature gradients
    
    Args:
        h: Convective heat transfer coefficient (W/m²·K)
        L: Characteristic length (m) - typically volume/surface area
        k: Thermal conductivity of solid (W/m·K)
    
    Returns:
        Biot number (dimensionless)
    
    Example:
        >>> h = 10  # W/m²·K (natural convection)
        >>> L = 0.01  # m (1 cm characteristic length)
        >>> k = 15  # W/m·K (steel)
        >>> Bi = calculate_biot_number(h, L, k)
    """
    if k == 0:
        raise ValueError("Thermal conductivity cannot be zero")
    
    return (h * L) / k


def estimate_cooling_time(
    T_initial: float,
    T_final: float,
    T_ambient: float,
    characteristic_length: float,
    alpha: float,
    h: Optional[float] = None,
    k: Optional[float] = None
) -> float:
    """
    Estimate cooling time using lumped capacitance model.
    
    Valid when Biot number < 0.1 (uniform internal temperature assumption)
    
    T(t) = T_ambient + (T_initial - T_ambient) * exp(-t/τ)
    where τ = ρcV/(hA) = ρcL/h (for characteristic length L)
    
    Args:
        T_initial: Initial temperature (°C or K)
        T_final: Target final temperature (°C or K)
        T_ambient: Ambient temperature (°C or K)
        characteristic_length: Characteristic length L = V/A (m)
        alpha: Thermal diffusivity (m²/s)
        h: Convective heat transfer coefficient (W/m²·K, optional)
        k: Thermal conductivity (W/m·K, optional)
    
    Returns:
        Cooling time (seconds)
    
    Example:
        >>> t_cool = estimate_cooling_time(
        ...     T_initial=600, T_final=100, T_ambient=20,
        ...     characteristic_length=0.01, alpha=4e-6, h=10, k=15)
    """
    if T_initial <= T_ambient or T_final <= T_ambient:
        raise ValueError("Initial and final temperatures must be above ambient")
    
    if T_final >= T_initial:
        raise ValueError("Final temperature must be less than initial temperature")
    
    # Calculate time constant
    if h is not None and k is not None:
        # Check Biot number validity
        Bi = calculate_biot_number(h, characteristic_length, k)
        if Bi > 0.1:
            print(f"Warning: Biot number = {Bi:.3f} > 0.1. Lumped capacitance model may be inaccurate.")
        
        # τ = L/α * (k/hL) = k/(hα)
        tau = k / (h * alpha)
    else:
        # Simplified estimation: τ ≈ L²/α
        tau = characteristic_length**2 / alpha
    
    # Solve for time: (T_final - T_ambient) = (T_initial - T_ambient) * exp(-t/τ)
    ratio = (T_final - T_ambient) / (T_initial - T_ambient)
    
    if ratio <= 0:
        raise ValueError("Invalid temperature ratio")
    
    cooling_time = -tau * np.log(ratio)
    
    return cooling_time


def solve_1d_diffusion(
    initial_temp: np.ndarray,
    boundary_conditions: Tuple[Tuple[str, float], Tuple[str, float]],
    time_steps: int,
    dx: float,
    dt: float,
    alpha: float,
    source_term: Optional[Callable[[np.ndarray, float], np.ndarray]] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Solve 1D heat diffusion equation using explicit finite difference method.
    
    ∂T/∂t = α * ∂²T/∂x² + Q(x,t)
    
    Args:
        initial_temp: Initial temperature distribution (1D array)
        boundary_conditions: Tuple of ((type, value), (type, value)) for left and right boundaries
                           Types: 'dirichlet' (fixed temp), 'neumann' (fixed flux)
        time_steps: Number of time steps to simulate
        dx: Spatial step size (m)
        dt: Time step size (s)
        alpha: Thermal diffusivity (m²/s)
        source_term: Optional function Q(x, t) returning heat source array
    
    Returns:
        Tuple of (temperature_history, time_array)
        - temperature_history: 2D array (time_steps x spatial_points)
        - time_array: 1D array of time values
    
    Example:
        >>> x = np.linspace(0, 0.1, 50)
        >>> T0 = 20 + 580 * np.exp(-((x - 0.05)**2) / 0.001)
        >>> bc = (('dirichlet', 20), ('dirichlet', 20))
        >>> T_history, t = solve_1d_diffusion(T0, bc, 1000, 0.002, 0.01, 4e-6)
    """
    # Stability check (CFL condition)
    r = alpha * dt / (dx**2)
    if r > 0.5:
        raise ValueError(
            f"Stability condition violated: r = {r:.3f} > 0.5. "
            f"Reduce dt or increase dx. Suggested dt < {0.5 * dx**2 / alpha:.6f}"
        )
    
    # Initialize
    n_points = len(initial_temp)
    T = initial_temp.copy()
    T_history = np.zeros((time_steps, n_points))
    T_history[0, :] = T
    
    time_array = np.arange(time_steps) * dt
    x_array = np.arange(n_points) * dx
    
    # Parse boundary conditions
    bc_left_type, bc_left_value = boundary_conditions[0]
    bc_right_type, bc_right_value = boundary_conditions[1]
    
    # Time stepping
    for step in range(1, time_steps):
        T_new = T.copy()
        
        # Interior points (explicit FTCS scheme)
        for i in range(1, n_points - 1):
            laplacian = (T[i+1] - 2*T[i] + T[i-1]) / (dx**2)
            
            # Add source term if provided
            if source_term is not None:
                Q = source_term(x_array, time_array[step])
                T_new[i] = T[i] + dt * (alpha * laplacian + Q[i])
            else:
                T_new[i] = T[i] + dt * alpha * laplacian
        
        # Apply boundary conditions
        # Left boundary
        if bc_left_type == 'dirichlet':
            T_new[0] = bc_left_value
        elif bc_left_type == 'neumann':
            # dT/dx = bc_left_value at x=0
            # Use forward difference: T[1] = T[0] + dx * dT/dx
            T_new[0] = T_new[1] - dx * bc_left_value
        
        # Right boundary
        if bc_right_type == 'dirichlet':
            T_new[-1] = bc_right_value
        elif bc_right_type == 'neumann':
            # dT/dx = bc_right_value at x=L
            # Use backward difference: T[-2] = T[-1] - dx * dT/dx
            T_new[-1] = T_new[-2] + dx * bc_right_value
        
        T = T_new
        T_history[step, :] = T
    
    return T_history, time_array


def calculate_fourier_number(
    alpha: float,
    t: float,
    L: float
) -> float:
    """
    Calculate the Fourier number for transient heat conduction.
    
    Fo = αt/L²
    
    Dimensionless time parameter indicating the degree of heat penetration.
    Fo << 1: Early time, heat hasn't penetrated far
    Fo ~ 1: Intermediate time
    Fo >> 1: Steady state approached
    
    Args:
        alpha: Thermal diffusivity (m²/s)
        t: Time (s)
        L: Characteristic length (m)
    
    Returns:
        Fourier number (dimensionless)
    
    Example:
        >>> alpha = 4e-6  # m²/s (steel)
        >>> t = 100  # seconds
        >>> L = 0.01  # m
        >>> Fo = calculate_fourier_number(alpha, t, L)
    """
    if L == 0:
        raise ValueError("Characteristic length cannot be zero")
    
    return (alpha * t) / (L**2)


def calculate_thermal_diffusivity(
    k: float,
    rho: float,
    cp: float
) -> float:
    """
    Calculate thermal diffusivity from material properties.
    
    α = k / (ρ * cp)
    
    Args:
        k: Thermal conductivity (W/m·K)
        rho: Density (kg/m³)
        cp: Specific heat capacity (J/kg·K)
    
    Returns:
        Thermal diffusivity (m²/s)
    
    Example:
        >>> k = 15  # W/m·K (steel)
        >>> rho = 7850  # kg/m³
        >>> cp = 500  # J/kg·K
        >>> alpha = calculate_thermal_diffusivity(k, rho, cp)
    """
    if rho == 0 or cp == 0:
        raise ValueError("Density and specific heat must be non-zero")
    
    return k / (rho * cp)


def calculate_thermal_penetration_depth(
    alpha: float,
    t: float
) -> float:
    """
    Calculate thermal penetration depth for transient heat conduction.
    
    δ = √(αt)
    
    Approximate depth to which temperature disturbance has penetrated.
    
    Args:
        alpha: Thermal diffusivity (m²/s)
        t: Time (s)
    
    Returns:
        Penetration depth (m)
    
    Example:
        >>> alpha = 4e-6  # m²/s
        >>> t = 100  # s
        >>> depth = calculate_thermal_penetration_depth(alpha, t)
    """
    return np.sqrt(alpha * t)
