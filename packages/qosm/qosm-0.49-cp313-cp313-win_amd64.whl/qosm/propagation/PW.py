from numpy import sqrt, exp, pi, sin, cos, array
from qosm import Vec3
from scipy.constants import c


def StoT(S11, S21, S12, S22):
    """
    Convert S-parameters to T-parameters (transfer matrix).

    Transforms scattering parameters to transfer matrix parameters using
    the standard conversion formulas. The transfer matrix relates input
    and output waves at the two ports of a two-port network.

    Parameters
    ----------
    S11 : complex
        Input reflection coefficient.
    S21 : complex
        Forward transmission coefficient.
    S12 : complex
        Reverse transmission coefficient.
    S22 : complex
        Output reflection coefficient.

    Returns
    -------
    tuple of complex
        Four-element tuple containing (T11, T21, T12, T22) transfer parameters.

    Notes
    -----
    Transfer matrix relates port variables as:
    [a1]   [T11 T12] [a2]
    [b1] = [T21 T22] [b2]

    Where a and b are normalized incident and reflected wave amplitudes.
    """
    # Convert S-parameters to T-parameters using standard formulas
    T11 = 1 / S21  # Forward voltage transfer ratio
    T22 = S12 - S11 * S22 / S21  # Reverse current transfer ratio
    T21 = S11 / S21  # Reverse voltage transfer ratio
    T12 = -T21  # Forward current transfer ratio (reciprocal network)
    return T11, T21, T12, T22


def TtoS(T):
    """
    Convert T-parameters (transfer matrix) to S-parameters.

    Transforms transfer matrix parameters back to scattering parameters
    for final S-parameter calculation and measurement comparison.

    Parameters
    ----------
    T : ndarray
        2x2 transfer matrix with elements [[T11, T12], [T21, T22]].

    Returns
    -------
    tuple of complex
        Four-element tuple containing (S11, S12, S21, S22) scattering parameters.

    Notes
    -----
    Inverse conversion from transfer matrix to S-parameters:
    S11 = T21/T11, S21 = 1/T11, S12 = (T22*T11 - T12*T21)/T11, S22 = -T12/T11
    """
    # Convert T-parameters back to S-parameters
    S11 = T[1, 0] / T[0, 0]  # Input reflection coefficient
    S21 = 1 / T[0, 0]  # Forward transmission coefficient
    S12 = T[1, 1] - T[0, 1] * T[1, 0] / T[0, 0]  # Reverse transmission coefficient
    S22 = -T[0, 1] / T[0, 0]  # Output reflection coefficient
    return S11, S12, S21, S22

def simulate(params: dict, frequency_GHz: float):
    """
    Simulate S-parameters using plane wave theory for multilayer structures.

    Calculates electromagnetic scattering parameters by modeling plane wave
    propagation through stratified media using Fresnel coefficients and
    transfer matrix method. Handles oblique incidence and multiple layers.

    Parameters
    ----------
    params : dict
        Dictionary containing all configuration options
    frequency_GHz : float
        Operating frequency in GHz for the simulation.

    Returns
    -------
    tuple of complex
        Four-element tuple containing (S11, S12, S21, S22) S-parameters
        calculated from plane wave theory.

    Notes
    -----
    The simulation process:
    1. Calculate wave parameters (wavelength, impedances, angles)
    2. For each layer: compute Fresnel coefficients and phase delays
    3. Build transfer matrix for each interface
    4. Cascade all transfer matrices
    5. Convert final T-matrix to S-parameters
    6. Apply phase corrections for reference plane positioning
    """

    # Extract simulation parameters from configuration
    slab_angle_deg = Vec3(params.get('sample_attitude_deg', (0, 0, 0))).norm()
    # slab_angle_deg = params.get('angle_deg', 0)  # Sample rotation angle in degrees
    slab_angle_rad = slab_angle_deg * pi / 180.  # Convert to radians for calculations
    freq_Hz = frequency_GHz * 1e9  # Convert frequency to Hz
    polar = 'tm'  # Polarization mode (TM = E-field parallel to incidence plane)
    k0 = 2 * pi * freq_Hz / c  # Free space wave number (rad/m)

    # Initialize medium properties for air (before first interface)
    n1 = eta1 = 1.  # Air: refractive index = 1, impedance = 1
    T11, T12, T21, T22 = StoT(0, 1, 1, 0)  # Initialize transfer matrix accumulator
    T = array([[T11, T12], [T21, T22]])

    # Calculate incident angle parameters
    cos_theta1 = cos(slab_angle_rad)  # Cosine of incident angle in air
    thickness_total = 0  # Accumulator for total structure thickness

    # Process each material layer in the multilayer structure
    for slab in params['mut']:
        # Update total thickness for phase reference calculations
        thickness_total += slab['thickness']
        slab_thickness = slab['thickness']  # Current layer thickness

        # Calculate material properties for current layer
        if hasattr(slab['epsilon_r'], '__call__'):
            n2 = sqrt(slab['epsilon_r'](frequency_GHz) + 0j)  # Complex refractive index: n = sqrt(εr)
        else:
            n2 = sqrt(slab['epsilon_r'] + 0j)  # Complex refractive index: n = sqrt(εr)
        eta2 = 1 / n2  # Wave impedance in medium: η = 1/n (normalized to free space)

        # Apply Snell's law to find transmission angle in current layer
        cos_theta2 = sqrt(1 - (n1 / n2) ** 2 * sin(slab_angle_rad) ** 2)

        # Calculate Fresnel reflection coefficient based on polarization
        if polar.lower() == 'te' or polar.lower() == 'h':
            # TE polarization (H-field parallel to interface, magnetic field transverse)
            den = eta2 * cos_theta1 + eta1 * cos_theta2  # Denominator for TE case
            rho = (eta2 * cos_theta1 - eta1 * cos_theta2) / den  # TE Fresnel coefficient
        elif polar.lower() == 'tm' or polar.lower() == 'e':
            # TM polarization (E-field parallel to incidence plane, electric field transverse)
            den = eta2 * cos_theta2 + eta1 * cos_theta1  # Denominator for TM case
            rho = (eta2 * cos_theta2 - eta1 * cos_theta1) / den  # TM Fresnel coefficient
        else:
            rho = 0  # Fallback (should not occur)

        # Calculate phase delay through current layer
        P = exp(-1j * k0 * n2 * slab_thickness * cos_theta2)  # Propagation phase factor

        # Calculate single-layer S-parameters using transmission line theory
        den = (1 - (P * rho) ** 2)  # Common denominator (1 - Γ²P²)
        S11 = ((1 - P ** 2) * rho) / den  # Layer reflection coefficient
        S21 = P * (1 - rho ** 2) / den  # Layer transmission coefficient

        # Convert layer S-parameters to T-parameters for cascading
        T11, T21, T12, T22 = StoT(S11, S21, S21, S11)

        # Cascade transfer matrices (matrix multiplication for series connection)
        T = T @ array([[T11, T12], [T21, T22]])

    # Convert final cascaded T-matrix back to S-parameters
    S11, S12, S21, S22 = TtoS(T)

    thru_line_by_reflection = params.get('thru_line_by_reflection', False)

    # Apply phase corrections for reference plane positioning
    if not thru_line_by_reflection:
        inv_S21_air = exp(1j * k0 * thickness_total * cos_theta1)  # Phase factor for total thickness
        S21 *= inv_S21_air  # Correct transmission phase
        S12 *= inv_S21_air  # Correct transmission phase
        S22 *= inv_S21_air ** 2  # Correct output reflection phase (double path)

    return S11, S12, S21, S22

# Example usage
if __name__ == "__main__":
    from numpy import log10, angle, full_like, linspace, nan

    import matplotlib
    matplotlib.use('Qt5Agg')
    from matplotlib import pyplot as plt

    # Example with two ports
    config_two_ports = {
        'sample_attitude_deg': (0.0, 0.0, 0.0),
        'mut': [
            {'epsilon_r': 2.53 - 0.005j, 'thickness': 0.012815}
        ],
    }

    frequencies_GHz = linspace(220., 330., 1001)

    # Test two ports
    s11 = full_like(frequencies_GHz, nan, dtype=complex)
    s12 = full_like(frequencies_GHz, nan, dtype=complex)
    s21 = full_like(frequencies_GHz, nan, dtype=complex)
    s22 = full_like(frequencies_GHz, nan, dtype=complex)
    for i, freq_GHz in enumerate(frequencies_GHz):
        s11[i], s12[i], s21[i], s22[i] = simulate(config_two_ports, freq_GHz)

    _, axes = plt.subplots(2, 2)
    axes[0, 0].plot(frequencies_GHz, 20 * log10(abs(s11)), label='S11')
    axes[0, 0].plot(frequencies_GHz, 20 * log10(abs(s22)), label='S22')
    axes[0, 1].plot(frequencies_GHz, 20 * log10(abs(s21)), label='S21')
    axes[0, 1].plot(frequencies_GHz, 20 * log10(abs(s12)), label='S12')

    axes[1, 0].plot(frequencies_GHz, angle(s11), label='S11')
    axes[1, 0].plot(frequencies_GHz, angle(s22), label='S22')
    axes[1, 1].plot(frequencies_GHz, angle(s21), label='S21')
    axes[1, 1].plot(frequencies_GHz, angle(s12), label='S12')

    plt.show()
