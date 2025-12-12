import numpy as np


class TRLCalibration:
    """
    TRL (Thru-Reflect-Line) calibration with 12-term error correction
    for 2-port S-parameter measurements

    TRL Calibration
    --------------------------------
    Assume:
    --------------------------------
      - S11 THRU = 0
      - S21 REFLECT = 0
      - S11 LINE = 0
      - S12 = S21 for all standards
      - S11 = S22 for all standards
    --------------------------------
    """

    def __init__(self, config):
        """
        Initialize TRL calibration with configuration

        Args:
            config: Dict with TRL configuration:
                    {'line_offset': value_in_meters, 'type_reflector': 'co' or 'cc'}
        """
        # Validate configuration
        if not isinstance(config, dict):
            raise ValueError("config must be a dictionary")

        required_keys = ['line_offset', 'type_reflector']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"trl_config must contain '{key}' key")

        self.line_offset = config['line_offset']
        self.type_reflector = config['type_reflector'].lower()

        if self.type_reflector not in ['cc', 'co']:
            raise ValueError("type_reflector must be 'cc' or 'co'")

        # Store configuration
        self.trl_config = config

        # 12-term error model parameters (single values)
        self.error_terms = {}
        self.calibrated = False

    def get_reflect_coefficient(self):
        """
        Get ideal reflection coefficient based on reflector type

        Returns:
            Complex reflection coefficient
        """
        if self.type_reflector == "cc":  # Short circuit
            return -1.0 + 0j
        elif self.type_reflector == "co":  # Open circuit
            return 1.0 + 0j
        return None

    def get_line_phase(self, frequency):
        """
        Calculate line phase based on frequency and line offset

        Args:
            frequency: Frequency in Hz (float)

        Returns:
            Phase in radians (float)
        """
        # Speed of light
        c = 299792458

        # Calculate wavelength
        wavelength = c / frequency

        # Phase = 2π × length / wavelength
        phase = 2 * np.pi * self.line_offset / wavelength

        return phase

    @staticmethod
    def s_to_t(S):
        """
        Converts an S-matrix to a T-matrix.

        Args:
            S (np.ndarray): A 2x2 S-matrix (scattering parameters).

        Returns:
            np.ndarray: A 2x2 T-matrix (transmission parameters).
        """
        T = np.zeros(S.shape, dtype=complex)

        T[0, 0] = 1. / S[1, 0]
        T[1, 0] = S[0, 0] / S[1, 0]
        T[0, 1] = -S[1, 1] / S[1, 0]
        T[1, 1] = -(S[1, 1] * S[0, 0] - S[0, 1] * S[1, 0]) / S[1, 0]

        return T

    @staticmethod
    def compute_rss(params, G1, G2, v1, v2):
        """
        Computes the RSS (Root Sum Square) value based on input parameters.
        """
        sign = 1
        r1 = sign * np.sqrt(G1 * v1 / G2 / v2)
        gamma = G2 * r1
        phi = 0

        gcal1 = gamma * np.exp(1j * phi)
        gcal2 = -gcal1

        reflect = 1 if params['type_reflector'].lower() == 'co' else -1

        dist1 = abs(reflect - gcal1)
        dist2 = abs(reflect - gcal2)

        if dist1 < dist2:
            sign = 1  # Sign imposed by: gcal1 = r1
        else:
            sign = -1  # Sign imposed by: gcal2 = -r1

        r1 = sign * r1

        return r1

    @staticmethod
    def compute_ps_kr(matT, vect1, vect2, vect3, vect4):
        """
        Computes the values v1 and v2 based on input matrices and vectors.
        """
        t11 = matT[0, 0]
        t12 = matT[0, 1]
        t21 = matT[1, 0]
        t22 = matT[1, 1]

        ac1 = vect1[0] * vect3[0]
        ac2 = vect1[1] * vect4[0]

        bd1 = vect2[0] * vect3[1]
        bd2 = vect2[1] * vect4[1]

        ac3 = vect1[0] * vect4[0]
        ac4 = vect1[1] * vect3[0]

        bd3 = vect2[0] * vect4[1]
        bd4 = vect2[1] * vect3[1]

        # Compute sums
        A = ac1 ** 2 + ac2 ** 2 + ac3 ** 2 + ac4 ** 2
        D = bd1 ** 2 + bd2 ** 2 + bd3 ** 2 + bd4 ** 2
        B = ac1 * bd1 + ac2 * bd2 + ac3 * bd3 + ac4 * bd4
        C = B
        E = t11 * ac1 + t12 * ac3 + t21 * ac4 + t22 * ac2
        F = t11 * bd1 + t12 * bd3 + t21 * bd4 + t22 * bd2

        det = A * D - B * C
        if abs(det) > 1e-306:
            v2 = (A * F - C * E) / det  # = ps
            v1 = (E * D - F * B) / det  # = kr
            return v1, v2
        else:
            raise ValueError("Determinant is too close to zero, calculation cannot proceed.")

    @staticmethod
    def calc_g1(gamma, vect1, vect2):
        """
        Computes the value G1 based on input parameters.
        """
        return (gamma - vect1[1] / vect1[0]) / (vect2[1] / vect1[0] - gamma * vect2[0] / vect1[0])

    @staticmethod
    def calc_g2(gamma, vect1, vect2):
        """
        Computes the value G2 based on input parameters.
        """
        return (gamma + vect2[0] / vect1[0]) / (vect2[1] / vect1[0] + gamma * vect1[1] / vect1[0])

    def extract_error_terms(self, s21_thru, s11_reflect, s21_line):
        """
        Extract 12-term error model parameters from TRL measurements

        Using TRL assumptions:
        - S11 THRU = 0
        - S21 REFLECT = 0
        - S11 LINE = 0
        - S12 = S21 for all standards
        - S11 = S22 for all standards

        Args:
            s21_thru: Measured S21 for thru standard (complex)
            s11_reflect: Measured S11 for reflect standard (complex)
            s21_line: Measured S21 for line standard (complex)
            frequency: Frequency in Hz (float)
        """

        # Define S-matrices for Thru, Reflect, and Line standards
        matSThru = np.array([[0, s21_thru], [s21_thru, 0]], dtype=complex)
        matSReflect = np.array([[s11_reflect, 0], [0, s11_reflect]], dtype=complex)
        matSLine = np.array([[0, s21_line], [s21_line, 0]], dtype=complex)

        gamma1 = matSReflect[0, 0]
        gamma2 = matSReflect[1, 1]

        # Convert S-matrices to T-matrices
        Tthru = self.s_to_t(matSThru)
        TLine = self.s_to_t(matSLine)

        # Compute the inverse of the Thru T-matrix
        TthruInv = np.zeros(Tthru.shape, dtype=complex)
        detTthru = Tthru[0, 0] * Tthru[1, 1] - Tthru[1, 0] * Tthru[0, 1]
        TthruInv[0, 0] = Tthru[1, 1]
        TthruInv[0, 1] = -Tthru[0, 1]
        TthruInv[1, 0] = -Tthru[1, 0]
        TthruInv[1, 1] = Tthru[0, 0]
        TthruInv /= detTthru

        # Compute Tme and Tms matrices
        Tme = TLine @ TthruInv
        Tms = TthruInv @ TLine

        # Compute eigenvectors and eigenvalues
        vpe, vecte = np.linalg.eig(Tme)
        vps, vects = np.linalg.eig(Tms)

        # Extract eigenvectors
        vect1e = vecte[:, 0]  # a1 a2
        vect2e = vecte[:, 1]  # b1 b2
        vect1s = vects[:, 0]  # A1 A2
        vect2s = vects[:, 1]  # B1 B2

        # Permute eigenvectors
        d2 = vect1s[0]  # d2 = A1
        d1 = -vect1s[1]  # d1 = -A2
        c2 = -vect2s[0]  # c2 = -B1
        c1 = vect2s[1]  # c1 = B2

        vect1s[0] = c1  # Matrix Ts
        vect1s[1] = d1
        vect2s[0] = c2
        vect2s[1] = d2

        # Compute kr and ps
        kr, ps = self.compute_ps_kr(Tthru, vect1e, vect2e, vect1s, vect2s)  # v2 = ps and v1 = kr

        # Compute G1 and G2
        G1 = self.calc_g1(gamma1, vect1e, vect2e)
        G2 = self.calc_g2(gamma2, vect1s, vect2s)

        # Compute r1 and r2
        r1 = self.compute_rss(self.trl_config, G1, G2, kr, ps)  # = r / s
        r2 = (kr / ps) / r1  # = k / p

        # Determine error terms: direction E -> S
        edf = vect1e[1] / vect1e[0]  # edf = a2 / a1
        etf = 1 / (vect1e[0] * vect1s[0] * kr)  # etf = 1 / (kr * a1 * c1)
        elf = vect1s[1] / vect1s[0] / r1  # elf = (d1 / c1) / (r / s)
        esf = -vect2e[0] / vect1e[0] / r2  # esf = -(b1 / a1) / (k / p)
        c4 = vect2e[1] - vect2e[0] * vect1e[1] / vect1e[0]  # c4 = b2 - (b1 * a2 / a1)
        erf = c4 / (vect1e[0] * r2)  # erf = (1 / (k / p * a1)) * (b2 - b1 * a2 / a1)

        # Determine error terms: direction S -> E
        edr = -vect2s[0] / vect1s[0]  # edr = -c2 / c1
        c3 = vect2s[1] - vect1s[1] * vect2s[0] / vect1s[0]  # c3 = d2 - (d1 * c2 / c1)
        err = c3 / (vect1s[0] * r1)  # err = (d2 - (d1 * c2 / c1)) / ((r / s) * c1)
        etr = c3 * c4 * ps  # etr = ps * (d2 - d1 * c2 / c1) * (b2 - b1 * a2 / a1)
        esr = elf
        elr = esf

        exf = 0
        exr = 0

        # Store error terms for apply_correction
        self.error_terms = {
            'edf': edf,
            'edr': edr,
            'erf': erf,
            'err': err,
            'etf': etf,
            'etr': etr,
            'esf': esf,
            'esr': esr,
            'elf': elf,
            'elr': elr,
            'exf': exf,
            'exr': exr,
        }

    def apply_correction(self, s11, s12, s21, s22):
        """
        Apply correction to S-parameters

        Args:
            s11, s12, s21, s22: S-parameters (complex values)

        Returns:
            Tuple of corrected S-parameters (s11_c, s12_c, s21_c, s22_c)
        """
        # Get error terms
        edf = self.error_terms['edf']
        edr = self.error_terms['edr']
        erf = self.error_terms['erf']
        err = self.error_terms['err']
        etf = self.error_terms['etf']
        etr = self.error_terms['etr']
        esf = self.error_terms['esf']
        esr = self.error_terms['esr']
        elf = self.error_terms['elf']
        elr = self.error_terms['elr']
        exf = self.error_terms['exf']
        exr = self.error_terms['exr']

        # Apply calibration using the working algorithm
        A = (s11 - edf) / erf
        B = (s22 - edr) / err
        C = (s21 - exf) / etf
        D = (s12 - exr) / etr

        F = (1 + A * esf) * (1 + B * esr) - C * D * elf * elr
        s11_cal = (A * (1 + B * esr) - C * D * elf) / F
        s12_cal = D * (1 + A * (esf - elr)) / F
        s21_cal = C * (1 + B * (esr - elf)) / F
        s22_cal = (B * (1 + A * esf) - C * D * elr) / F

        return s11_cal, s12_cal, s21_cal, s22_cal


# Example usage
if __name__ == "__main__":
    # Define TRL configuration
    trl_config = {
        'line_offset': 0.010,  # 10mm line offset
        'type_reflector': 'cc'  # Short circuit reflector
    }

    # Create calibration object with configuration
    trl_cal = TRLCalibration(trl_config)

    # Single frequency point
    frequency = 5e9  # 5 GHz

    # Simulate measured calibration standards (single complex values)
    np.random.seed(42)  # For reproducible results
    noise_level = 0.005  # Reduced noise for stability

    # Create realistic measurements based on TRL assumptions
    # THRU: S11=0, S21=measured (close to 1 with some loss)
    s21_thru = 0.98 * np.exp(-1j * 0.05) + noise_level * (np.random.randn() + 1j * np.random.randn())

    # REFLECT: S11=measured (close to -1 for short circuit)
    s11_reflect = -0.95 * np.exp(1j * 0.1) + noise_level * (np.random.randn() + 1j * np.random.randn())

    # LINE: S11=0, S21=measured (with phase shift due to line length)
    line_phase = trl_cal.get_line_phase(frequency)
    s21_line = 0.97 * np.exp(-1j * line_phase) + noise_level * (np.random.randn() + 1j * np.random.randn())

    # Perform TRL calibration
    print("Performing TRL calibration...")
    trl_cal.extract_error_terms(s21_thru, s11_reflect, s21_line)

    # Simulate a DUT measurement (single S-parameters)
    s11_dut = 0.1 + 0.05j + noise_level * (np.random.randn() + 1j * np.random.randn())
    s12_dut = 0.9 * np.exp(-1j * 2 * np.pi * frequency / 3e8 * 0.005) + noise_level * (
                np.random.randn() + 1j * np.random.randn())
    s21_dut = 0.9 * np.exp(-1j * 2 * np.pi * frequency / 3e8 * 0.005) + noise_level * (
                np.random.randn() + 1j * np.random.randn())
    s22_dut = 0.2 + 0.1j + noise_level * (np.random.randn() + 1j * np.random.randn())

    # Apply TRL correction
    print("Applying TRL correction to DUT...")
    s11_corrected, s12_corrected, s21_corrected, s22_corrected = trl_cal.apply_correction(s11_dut, s12_dut, s21_dut,
                                                                                          s22_dut)

    print("\nDUT Results:")
    print(f"Original S11: {s11_dut:.6f}")
    print(f"Corrected S11: {s11_corrected:.6f}")
    print(f"Original S21: {s21_dut:.6f}")
    print(f"Corrected S21: {s21_corrected:.6f}")

    print("\nTRL calibration example completed!")

"""
Usage Example:

# Define TRL configuration
trl_config = {
    'line_offset': 0.010,    # Line offset in meters (10mm)
    'type_reflector': 'cc'   # 'cc' for short circuit, 'co' for open circuit
}

# Create calibration with config in constructor
trl_cal = TRLCalibration(trl_config)

# Input your measured values (single complex values)
s21_thru = 0.95 + 0.02j      # Complex value
s11_reflect = -0.9 + 0.01j   # Complex value
s21_line = 0.98 * exp(-1j * phase)  # Complex value
frequency = 5e9              # Float in Hz

# Extract error terms
trl_cal.extract_error_terms(s21_thru, s11_reflect, s21_line, frequency)

# Apply correction to DUT (single S-parameters)
s11_c, s12_c, s21_c, s22_c = trl_cal.apply_correction(s11_dut, s12_dut, s21_dut, s22_dut)

# View results
print(trl_cal.get_summary())
"""