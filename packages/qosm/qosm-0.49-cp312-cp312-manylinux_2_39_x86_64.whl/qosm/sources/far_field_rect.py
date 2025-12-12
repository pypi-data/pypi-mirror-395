import matplotlib.pyplot as plt
import numpy as np
from numpy import array, sqrt, pi, linspace, zeros_like
from scipy.special import fresnel
import math


def fresnelC(x):
    S, C = fresnel(x)
    return C


def fresnelS(x):
    S, C = fresnel(x)
    return S


def F(x):
    return fresnelC(x) - 1j * fresnelS(x)


def F0(v, s):
    vs = v / s
    return (1 / s) * np.exp(1j * 0.5 * np.pi * (vs) ** 2) * (F(vs + s) - F(vs - s))


def F1(v, s):
    return 0.5 * (F0(v + 0.5, s) + F0(v - 0.5, s))


def c(th):
    return (1 + np.cos(th)) / 2


def get_horn_transmission_coefficients(horn_data):
    """
    Extract transmission coefficients from horn mode data
    Returns dictionaries of TE and TM mode coefficients
    """
    te_modes = {}  # Dictionary to store TE mode coefficients {(m,n): coefficient}
    tm_modes = {}  # Dictionary to store TM mode coefficients {(m,n): coefficient}

    # Default reflection coefficients (can be modified based on your model)
    te_reflection = {}
    tm_reflection = {}

    for mode in horn_data['modes']:
        m, n = mode['indices']
        coefficient = mode['coefficient']

        if mode['type'] == 'TE':
            te_modes[(m, n)] = coefficient
            te_reflection[(m, n)] = 0j  # Default reflection coefficient
        elif mode['type'] == 'TM':
            tm_modes[(m, n)] = coefficient
            tm_reflection[(m, n)] = 0j  # Default reflection coefficient

    return {'te_transmission': te_modes, 'tm_transmission': tm_modes,
            'te_reflection': te_reflection, 'tm_reflection': tm_reflection}


def get_horn_dimensions(horn_data):
    """
    Extract physical dimensions from horn data
    Returns Lx, Ly (aperture dimensions) and sx, sy (normalized aperture parameters)
    """
    # Use the aperture dimensions (a, b) as the effective radiating aperture
    Lx = horn_data['a']  # Width
    Ly = horn_data['b']  # Height

    # Normalized aperture parameters (these may need adjustment based on your horn model)
    # For a rectangular horn, these are typically related to the taper
    sx = 1.0  # Default normalized parameter
    sy = 1.0  # Default normalized parameter

    return Lx, Ly, sx, sy


def calculate_mode_field_components(m, n, mode_type, vx, vy, sx, sy, phi):
    """
    Calculate field components for a specific TE or TM mode

    Parameters:
    m, n: mode indices
    mode_type: 'TE' or 'TM'
    vx, vy: normalized aperture coordinates
    sx, sy: aperture parameters
    phi: azimuth angle

    Returns:
    fx, fy: field components for this mode
    """
    if mode_type == 'TE':
        if m == 0 and n == 1:
            # TE01 mode
            fx = F1(vy, sy) * F0(vx, sx)
            fy = 0j * np.ones_like(fx)
        elif m == 1 and n == 0:
            # TE10 mode
            fx = 0j * np.ones_like(vx)
            fy = F1(vx, sx) * F0(vy, sy)
        else:
            # Higher order TE modes - generalized calculation
            # This is a simplified approach; more sophisticated mode calculations
            # may be needed for specific applications
            if n == 0:
                # TEmn0 modes (similar to TE10)
                fx = 0j * np.ones_like(vx)
                fy = F1(vx, sx) * F0(vy, sy) * np.cos(m * np.pi * vx / (2 * sx))
            elif m == 0:
                # TE0mn modes (similar to TE01)
                fx = F1(vy, sy) * F0(vx, sx) * np.cos(n * np.pi * vy / (2 * sy))
                fy = 0j * np.ones_like(fx)
            else:
                # TEmn modes with both m,n > 0
                fx = F1(vy, sy) * F0(vx, sx) * np.cos(m * np.pi * vx / (2 * sx)) * np.cos(n * np.pi * vy / (2 * sy))
                fy = F1(vx, sx) * F0(vy, sy) * np.cos(m * np.pi * vx / (2 * sx)) * np.cos(n * np.pi * vy / (2 * sy))

    elif mode_type == 'TM':
        # TM modes - these have both Ex and Ey components
        if m >= 1 and n >= 1:
            # TMmn modes
            fx = F1(vy, sy) * F0(vx, sx) * np.sin(m * np.pi * vx / (2 * sx)) * np.sin(n * np.pi * vy / (2 * sy))
            fy = F1(vx, sx) * F0(vy, sy) * np.sin(m * np.pi * vx / (2 * sx)) * np.sin(n * np.pi * vy / (2 * sy))
        else:
            # TM modes with m=0 or n=0 don't exist in rectangular waveguides
            fx = 0j * np.ones_like(vx)
            fy = 0j * np.ones_like(vx)
    else:
        fx = 0j * np.ones_like(vx)
        fy = 0j * np.ones_like(vx)

    return fx, fy


def far_field_from_request(ff_request, horn_data, normalise=True):
    """
    Calculate far field pattern from far field request and horn data
    Now supports all TE and TM modes

    Parameters:
    ff_request: dict with 'horn', 'phi', 'theta_range' keys
    horn_data: dict with horn parameters
    normalise: bool, whether to normalize the pattern

    Returns:
    UdB: Far field pattern in dB
    GdB: Gain in dB
    theta_deg: Theta angles in degrees
    phi_deg: Phi angle in degrees (single value)
    """
    # Extract parameters from far field request
    rot_z_deg = horn_data['rot_z_deg']
    phi_deg = ff_request['phi'] - rot_z_deg  # Cut-plane angle in degrees
    theta_start, theta_stop, theta_step = ff_request['theta_range']  # Theta range in degrees

    # Convert to radians
    phi_rad = math.radians(phi_deg)
    theta_start_rad = math.radians(theta_start)
    theta_stop_rad = math.radians(theta_stop)
    theta_step_rad = math.radians(theta_step)

    # Create theta array
    theta_rad = np.arange(theta_start_rad, theta_stop_rad + theta_step_rad, theta_step_rad)
    theta_deg_array = np.degrees(theta_rad)

    # Get horn parameters
    freq = horn_data['frequency_GHz'] * 1e9  # Convert GHz to Hz
    Lx, Ly, sx, sy = get_horn_dimensions(horn_data)
    mode_coeffs = get_horn_transmission_coefficients(horn_data)

    # Calculate far field pattern
    c0 = 299792458  # speed of light in m/s
    lmbda = c0 / freq

    # Single phi cut (the requested cut-plane)
    phi = phi_rad

    vx = (Lx / lmbda) * np.sin(theta_rad) * np.cos(phi)
    vy = (Ly / lmbda) * np.sin(theta_rad) * np.sin(phi)

    # Initialize total field components
    fx_total = np.zeros_like(vx, dtype=complex)
    fy_total = np.zeros_like(vx, dtype=complex)

    # Sum contributions from all TE modes
    te_modes = mode_coeffs['te_transmission']
    for (m, n), coefficient in te_modes.items():
        fx_mode, fy_mode = calculate_mode_field_components(m, n, 'TE', vx, vy, sx, sy, phi)
        fx_total += coefficient * fx_mode
        fy_total += coefficient * fy_mode

    # Sum contributions from all TM modes
    tm_modes = mode_coeffs['tm_transmission']
    for (m, n), coefficient in tm_modes.items():
        fx_mode, fy_mode = calculate_mode_field_components(m, n, 'TM', vx, vy, sx, sy, phi)
        fx_total += coefficient * fx_mode
        fy_total += coefficient * fy_mode

    # Calculate field components at boresight (theta=0) for normalization
    vx0 = 0
    vy0 = 0
    fx0_total = 0j
    fy0_total = 0j

    # Sum contributions from all TE modes at boresight
    for (m, n), coefficient in te_modes.items():
        fx0_mode, fy0_mode = calculate_mode_field_components(m, n, 'TE', np.array([vx0]), np.array([vy0]), sx, sy, phi)
        fx0_total += coefficient * fx0_mode[0]
        fy0_total += coefficient * fy0_mode[0]

    # Sum contributions from all TM modes at boresight
    for (m, n), coefficient in tm_modes.items():
        fx0_mode, fy0_mode = calculate_mode_field_components(m, n, 'TM', np.array([vx0]), np.array([vy0]), sx, sy, phi)
        fx0_total += coefficient * fx0_mode[0]
        fy0_total += coefficient * fy0_mode[0]

    # Calculate total electric field components
    E_theta = c(theta_rad) * (fx_total * np.cos(phi) + fy_total * np.sin(phi))
    E_phi = c(theta_rad) * (fy_total * np.cos(phi) - fx_total * np.sin(phi))

    E_theta0 = fx0_total * np.cos(phi) + fy0_total * np.sin(phi)
    E_phi0 = fy0_total * np.cos(phi) - fx0_total * np.sin(phi)

    # Calculate radiation pattern
    numerator = np.abs(E_theta) ** 2 + np.abs(E_phi) ** 2
    denominator = np.abs(E_theta0) ** 2 + np.abs(E_phi0) ** 2

    # Avoid division by zero
    if np.abs(denominator) < 1e-12:
        U = np.zeros_like(numerator)
    else:
        U = numerator / denominator

    # Calculate total mode power for aperture efficiency
    total_mode_power = 0
    for coefficient in te_modes.values():
        total_mode_power += np.abs(coefficient) ** 2
    for coefficient in tm_modes.values():
        total_mode_power += np.abs(coefficient) ** 2

    # Aperture efficiency
    if total_mode_power > 0:
        e = 0.125 * (np.abs(E_theta0) ** 2 + np.abs(E_phi0) ** 2) / total_mode_power
    else:
        e = 0

    # Gain
    G0 = 4 * np.pi * (Lx * Ly) / (lmbda ** 2)
    G = e * G0
    GdB = 10 * np.log10(G) if G > 0 else -np.inf

    # Convert to dB, handling zeros
    UdB = np.where(U > 0, 10 * np.log10(U), -np.inf)

    if not normalise:
        UdB = np.where(np.isfinite(UdB), UdB + GdB, -np.inf)

    return UdB, GdB, theta_deg_array, phi_deg


def plot_far_field_pattern(ff_request, horn_data, normalise=True, title=None):
    """
    Plot the far field pattern for a given request and horn

    Parameters:
    ff_request: dict with far field request parameters
    horn_data: dict with horn parameters
    normalise: bool, whether to normalize the pattern
    title: str, optional plot title
    """
    UdB, GdB, theta_deg, phi_deg = far_field_from_request(ff_request, horn_data, normalise)

    plt.figure(figsize=(10, 6))
    plt.plot(theta_deg, UdB, 'b-', linewidth=2)
    plt.xlabel('Theta (degrees)')
    plt.ylabel('Pattern (dB)')
    plt.grid(True, alpha=0.3)

    if title is None:
        title = f"Far Field Pattern - φ={phi_deg}°, Horn: {horn_data.get('source_name', 'Unknown')}"
    plt.title(title)

    # Add gain information
    info_text = f"Gain: {GdB:.1f} dB\nFreq: {horn_data['frequency_GHz']} GHz"
    plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    return plt.gcf()


def validate_horn_for_far_field(horn_data):
    """
    Validate that horn data has required parameters for far field calculation

    Returns:
    bool: True if valid, False otherwise
    list: List of missing/invalid parameters
    """
    required_keys = ['frequency_GHz', 'a', 'b', 'modes']
    missing = []

    for key in required_keys:
        if key not in horn_data:
            missing.append(key)

    # Check if we have valid modes with transmission coefficients
    if 'modes' in horn_data:
        has_valid_modes = any(mode['type'] in ['TE', 'TM'] for mode in horn_data['modes'])
        if not has_valid_modes:
            missing.append('Valid TE or TM modes')

    return len(missing) == 0, missing


# Example usage function
if __name__ == "__main__":
    """Example of how to use the adapted functions"""

    # Example horn data with multiple modes
    horn_data = {
        'source_name': 'TestHorn',
        'frequency_GHz': 275,
        'shape': 'rect',
        'a': 0.0056,  # 15mm
        'b': 0.0056,  # 12mm
        'rot_z_deg': 45.,
        'enable_mode_matching': True,
        'length': 0.056,  # 80mm
        'num_discontinuities': 155,
        'waveguide_type': 'WR3.4',
        'modes': [
            {'type': 'TE', 'indices': (1, 0), 'coefficient': 0.707 + 0j},
            {'type': 'TE', 'indices': (0, 1), 'coefficient': 0.707 + 0j},
        ]
    }

    # Example far field request
    ff_request = {
        'horn': 'horn_uuid_123',  # Reference to horn
        'phi': 0,  # Cut-plane at 0 degrees
        'theta_range': (-90, 90, 1)  # -90 to 90 degrees, 1 degree step
    }

    # Validate horn data
    is_valid, missing = validate_horn_for_far_field(horn_data)
    if not is_valid:
        print(f"Horn data validation failed. Missing: {missing}")
        exit(1)

    # Calculate and plot far field
    UdB, GdB, theta_deg, phi_deg = far_field_from_request(ff_request, horn_data)
    print(f"Calculated pattern for φ={phi_deg}° with {len(theta_deg)} points")
    print(f"Horn gain: {GdB:.2f} dB")

    # Create plot
    fig = plot_far_field_pattern(ff_request, horn_data)
    plt.show()
