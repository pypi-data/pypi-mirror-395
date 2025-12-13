"""
Test target file for PIPRE transpiler
Contains destructive operations that collapse physical information
"""

import numpy as np


def calculate_graybody_temperature(energy_grid, kappa_values):
    """
    Calculate effective temperature from graybody radiation
    This function contains destructive operations that lose physical information
    """
    # Destructive operation: mean() collapses energy variation
    mean_energy = np.mean(energy_grid)

    # Destructive operation: sum() loses spatial variation
    total_kappa = np.sum(kappa_values, axis=0)

    # Premature discretization loses fine structure
    discrete_temp = int(mean_energy / total_kappa)

    # Another destructive mean operation
    avg_temperature = np.mean(discrete_temp)

    return avg_temperature


def process_hawking_radiation(field_data):
    """
    Process Hawking radiation field data
    Multiple destructive operations that lose physical information
    """
    # Line 147: This is the target line mentioned in the prompt
    mean_field = np.mean(field_data, axis=1)  # Collapses spatial dimensions

    # Sum over time dimension loses temporal variation
    total_radiation = np.sum(field_data, axis=0)

    # Find peak without preserving uncertainty
    peak_idx = np.argmax(mean_field)

    return peak_idx, total_radiation


def analyze_plasma_modes(plasma_data):
    """
    Analyze plasma modes with information loss
    """
    # Multiple destructive operations
    mode_amplitudes = np.mean(plasma_data, axis=2)
    total_energy = np.sum(plasma_data)

    # Premature discretization
    discrete_modes = int(np.mean(mode_amplitudes))

    return discrete_modes
