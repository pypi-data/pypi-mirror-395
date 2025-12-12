from copy import deepcopy
from typing import Any

from numpy import (ndarray, array, linspace, linalg, zeros, zeros_like, nan, isnan, dtype, floating, complexfloating,
                   sqrt, mod, pi, any, tanh, abs, mean, unwrap, random, ones)
import skrf as rf
from scipy.interpolate import interp1d
from scipy.optimize import minimize
from scipy.stats import linregress
from tqdm import tqdm


class PermittivityEstimation:
    """
    Abstract base class for permittivity estimation models using S-parameters.

    This class provides the framework for estimating complex permittivity of materials
    under test (MUT) using electromagnetic simulation and inverse optimization techniques.

    Attributes
    ----------
    model_name : str
        Name identifier for the specific model implementation.
    params : dict
        Configuration parameters for the estimation model.
    s_idx : int
        Index of the sample layer to characterize in multi-layer configurations.
    """

    model_name: str = 'None'

    def __init__(self, model, params, unknown_sample_index=0):
        """
        Initialize the permittivity estimation model.

        Parameters
        ----------
        model : module
            Python module containing the 'simulate' function
        params : dict
            Dictionary containing all configuration options for frequency sweep and fitting.
        unknown_sample_index : int, optional
            Index of the sample to characterize in multi-layer slab configurations.
            Default is 0 (first layer).
        """
        self.model = model
        self.model_name = model.__name__.split('.')[-1]
        self.params = deepcopy(params)
        self.s_idx = unknown_sample_index

    def _cost_function(self, eps: tuple, frequency_GHz: float, s_to_fit: ndarray, params: dict,
                       phys_constraint: bool = False) -> float:
        """
        Compute the cost function for permittivity optimization.

        Calculates the error between simulated and measured S-parameters with
        physical constraints to ensure realistic permittivity values.

        Parameters
        ----------
        eps : tuple
            Two-element tuple containing (real_part, imaginary_part) of permittivity.
        frequency_GHz : float
            Operating frequency in GHz.
        s_to_fit : ndarray
            Reference S-parameter value (complex) for fitting. Can be a single value
            or array of values for multiple angles.
        params : dict
            Simulation parameters. May contain 'angles' key for multi-angle fitting.
        phys_constraint: bool, optional
            Constrains the imaginary part to be negative

        Returns
        -------
        float
            Calculated cost function value including physical penalties.

        Notes
        -----
        The cost function includes:
        - Bidirectional error calculation between simulated and measured values
        - Handle physical penalties for non-physical permittivity values (Im(ε) ≤ 0)
        - Hyperbolic tangent normalization using coefficient_3d parameter
        - Support for single value or multiple angles simulation
        """
        params['mut'][self.s_idx]['epsilon_r'] = eps[0] + 1j * eps[1]

        # Check if we have multiple angles (s_to_fit is an array)
        if hasattr(s_to_fit, '__len__') and 'angles' in params:
            # Multiple angles case
            angles = params['angles']

            if len(s_to_fit) != len(angles):
                raise ValueError("s_to_fit must have same length as angles array")

            total_error = 0
            coefficient_3d = params.get('coefficient_3d', 10)

            for i, (s_val, angle) in enumerate(zip(s_to_fit, angles)):
                # Create temporary params with current angle
                temp_params = params.copy()
                temp_params['angle'] = angle

                # Simulate for this angle
                S11calc, _, S21calc, _ = self.model.simulate(temp_params, frequency_GHz)

                # Error calculation for this angle
                err1 = 1 - s_val / S21calc
                err2 = 1 - S21calc / s_val

                total_error += abs(tanh((1 / coefficient_3d) * abs(err1 * err2)))

            # Average error across all angles
            error = total_error / len(angles)

        else:
            # Single value case (original behavior)
            S11calc, _, S21calc, _ = self.model.simulate(params, frequency_GHz)
            coefficient_3d = params.get('coefficient_3d', 10)

            # Error calculation
            err1 = 1 - s_to_fit / S21calc
            err2 = 1 - S21calc / s_to_fit

            error = abs(tanh((1 / coefficient_3d) * abs(err1 * err2)))

        # Physical constraint penalty
        penalty = (1e10 if eps[1] > 0 else 0) if phys_constraint else 0

        # Final Cost Function
        return error + penalty

    def fit(self, s_params_to_fit: rf.Network | str | list, initial_guess: complex, fit_options: dict | None = None,
            **kwargs) -> tuple[ndarray[Any, dtype[floating[Any]]], ndarray[Any, dtype[floating[Any]]] | None]:
        """
        Estimate complex permittivity by inverse optimization over frequency band.

        Performs frequency-by-frequency optimization to extract permittivity values
        by minimizing the difference between measured and simulated S-parameters.

        Parameters
        ----------
        s_params_to_fit : skrf.Network or str or list
            Measured S-parameters as Network object, filepath to S2P file, or list of pairs.
            For multi-angle fitting: list of tuples [(s2p1_angle1, s2p2_angle1), (s2p1_angle2, s2p2_angle2), ...]
            where each tuple contains 2 Networks or 2 filepaths for the same angle.
        initial_guess : complex
            Starting value for permittivity optimization (real + 1j*imag).
        fit_options : dict, optional
            Additional options passed to scipy.minimize optimizer.
        **kwargs : keyword arguments
            Additional fitting parameters:

            - half_win_size : int, optional
                Moving average window size for input data smoothing. Default is 0 (no smoothing).
            - use_parameter : str, optional
                S-parameter to fit against ('s11' or 's21'). Default is 's21'.
            - idx_input : tuple, optional
                S-parameter matrix indices (i,j) to extract from network. Default is (1,0) for S21.
            - lambda_reg : float, optional
                Spectral regularization weight for smoothness constraint. Default is 0.00.
            - use_bar : bool, optional
                Whether to show progress bar. Default is True.
            - angles : array_like, optional
                Array of angles for multi-angle fitting. Required when s_params_to_fit is a list
                of measurement pairs. Length must match the number of angle pairs.

        Returns
        -------
        ndarray
            Array of shape (N, 2) containing permittivity estimates where:
            - Column 0: Real part of relative permittivity
            - Column 1: Imaginary part of relative permittivity (positive for losses)

        Notes
        -----
        - Uses spectral regularization to promote smoothness across frequency
        - Handles NaN values gracefully in input data
        - Supports both file input and direct Network objects
        - Previous frequency point results are used to improve convergence
        - Multi-angle fitting: if 'angles' is provided in kwargs and s_params_to_fit
          is a list of measurement pairs, performs simultaneous fitting across all angles
          for each frequency point using s21 = 0.25 * (S21_1 + S12_1 + S21_2 + S12_2).
        """
        # Extract keyword arguments with defaults
        half_win_size = kwargs.get('half_win_size', 0)
        lambda_reg = kwargs.get('lambda_reg', 0.)
        use_bar = kwargs.get('use_bar', True)
        use_parameter = kwargs.get('use_parameter', 's21')
        input_parameter = kwargs.get('input_parameter', 's21').lower()
        interpolate_to = kwargs.get('interpolate_to', 0)
        angles = kwargs.get('angles', None)

        # Determine if we have multi-angle data (list of pairs)
        is_multi_angle = isinstance(s_params_to_fit, list) and angles is not None

        if is_multi_angle:
            # Multi-angle case: s_params_to_fit is a list of pairs
            if len(s_params_to_fit) != len(angles):
                raise ValueError("Number of measurement pairs must match number of angles")

            # Load and process each pair
            s_to_fit_all_angles = []
            frequencies_GHz = None

            for pair in s_params_to_fit:
                if len(pair) != 2:
                    raise ValueError("Each measurement pair must contain exactly 2 elements (s2p1, s2p2)")

                s2p1, s2p2 = pair

                # Load networks if they are strings
                if isinstance(s2p1, str):
                    s2p1 = filter_s2p(s2p1, half_window_size=0)
                if isinstance(s2p2, str):
                    s2p2 = filter_s2p(s2p2, half_window_size=0)

                # Set frequency grid from first pair
                if frequencies_GHz is None:
                    frequencies_GHz = s2p1.f * 1e-9

                # Extract transmission parameters: S21 and S12 from both networks
                s21_1 = s2p1.s[:, 1, 0]  # S21 from first network
                s12_1 = s2p1.s[:, 0, 1]  # S12 from first network
                s21_2 = s2p2.s[:, 1, 0]  # S21 from second network
                s12_2 = s2p2.s[:, 0, 1]  # S12 from second network

                # Calculate average: s21 = 0.25 * (S21_1 + S12_1 + S21_2 + S12_2)
                s21_avg = 0.25 * (s21_1 + s12_1 + s21_2 + s12_2)
                s_to_fit_all_angles.append(s21_avg)

            # Convert to array: shape (n_frequencies, n_angles)
            s_to_fit = array(s_to_fit_all_angles).T

        else:
            # Single measurement case (original behavior)
            # Load S-parameters if string filepath provided (without filtering)
            if isinstance(s_params_to_fit, str):
                s_params_to_fit = filter_s2p(s_params_to_fit, half_window_size=0)

            # Get the initial frequency array from the data to fit
            frequencies_GHz = s_params_to_fit.f * 1e-9

            if input_parameter in ('s21', 's12'):
                # transmission measurement mode
                s_to_fit1 = s_params_to_fit.s[:, 1, 0]
                s_to_fit2 = s_params_to_fit.s[:, 0, 1]
            elif input_parameter in ('s11', 's22'):
                # reflection measurement mode
                s_to_fit1 = s_params_to_fit.s[:, 0, 0]
                s_to_fit2 = s_params_to_fit.s[:, 1, 1]
            else:
                raise AttributeError(f'Invalid input parameter: {input_parameter}')

            # used data : mean between the two parameters (S21 & S12 or S11 & S22)
            s_to_fit = .5 * (s_to_fit1 + s_to_fit2)

        # backup original param dict
        _params = deepcopy(self.params)

        # Add angles to params if provided
        if is_multi_angle:
            _params['angles'] = angles

        # fitting options
        if fit_options is None:
            fit_options = {}
        eps_re_min = fit_options.get('eps_re_min', 1.)
        eps_re_max = fit_options.get('eps_re_max', 10.)
        num_points = fit_options.get('num_points', 201)
        _fit_options = {
            'maxiter': fit_options.get('max_iter', 10000),
            'fatol': fit_options.get('func_tol', 1e-15),
            'xatol': (eps_re_max - eps_re_min) / (num_points - 1),
            'maxfev': fit_options.get('max_fun_eval', 10000),
            'adaptive': fit_options.get('adaptive', False)
        }

        # Optional interpolation to different frequency grid
        if interpolate_to > 0:
            _frequencies_GHz = linspace(frequencies_GHz[0], frequencies_GHz[-1], interpolate_to, endpoint=True)

            if is_multi_angle:
                # Interpolate each angle separately
                s_to_fit_interp = []
                for angle_idx in range(s_to_fit.shape[1]):
                    fn = interp1d(frequencies_GHz, s_to_fit[:, angle_idx], kind='cubic', bounds_error=False,
                                  fill_value="extrapolate")
                    s_to_fit_interp.append(fn(_frequencies_GHz))
                s_to_fit = array(s_to_fit_interp).T
            else:
                fn1 = interp1d(frequencies_GHz, s_to_fit1, kind='cubic', bounds_error=False, fill_value="extrapolate")
                fn2 = interp1d(frequencies_GHz, s_to_fit2, kind='cubic', bounds_error=False, fill_value="extrapolate")
                s_to_fit1 = fn1(_frequencies_GHz)
                s_to_fit2 = fn2(_frequencies_GHz)
                s_to_fit = .5 * (s_to_fit1 + s_to_fit2)

            frequencies_GHz = _frequencies_GHz

        # Apply moving average smoothing if requested
        if half_win_size > 1:
            if is_multi_angle:
                # Apply smoothing to each angle separately
                s_to_fit_smooth = []
                for angle_idx in range(s_to_fit.shape[1]):
                    s_smooth = moving_average(s_to_fit[:, angle_idx], half_win_size)
                    s_to_fit_smooth.append(s_smooth)
                s_to_fit = array(s_to_fit_smooth).T
            else:
                s_to_fit1 = moving_average(s_to_fit1, half_win_size)
                s_to_fit2 = moving_average(s_to_fit2, half_win_size)
                s_to_fit = .5 * (s_to_fit1 + s_to_fit2)

            frequencies_GHz_used = frequencies_GHz[half_win_size:-half_win_size]
        else:
            frequencies_GHz_used = frequencies_GHz

        i_start = half_win_size
        bar = tqdm(total=len(frequencies_GHz_used), desc="%s model => Fit" % self.model_name) if use_bar else None

        # Frequency-by-frequency optimization
        epsilon_r = zeros((frequencies_GHz.shape[0], 2)) * nan

        # for the lower frequency, use initial guess given by the user
        eps_init = [initial_guess.real, initial_guess.imag]
        for i, freq_GHz in enumerate(frequencies_GHz_used):
            if use_bar:
                bar.update(1)

            i_full = i + i_start
            prev_eps = epsilon_r[i_full - 1] if i > 0 else None

            # Handle frequency-dependent permittivity in other layers
            if len(_params['mut']) > 1:
                for m, mut in enumerate(_params['mut']):
                    if 'epsilon_r' in mut and hasattr(mut['epsilon_r'], "__len__"):
                        _params['mut'][m]['epsilon_r'] = mut['epsilon_r'][i] + 0j

            def objective(eps):
                """Combined objective function with data fitting and regularization."""
                if is_multi_angle:
                    current_s_to_fit = s_to_fit[i, :]  # All angles for this frequency
                else:
                    current_s_to_fit = s_to_fit[i] if hasattr(s_to_fit, '__len__') else s_to_fit[i]

                loss = self._cost_function(
                    eps, frequency_GHz=freq_GHz, s_to_fit=current_s_to_fit, params=_params,
                    phys_constraint=kwargs.get('phys_constraint', False)
                )

                # Spectral regularization for smoothness
                reg = 0
                if prev_eps is not None and not any(isnan(prev_eps)):
                    reg = lambda_reg * float(linalg.norm(eps - prev_eps)) ** 2

                return loss + reg

            result = minimize(objective, eps_init, method='Nelder-Mead', options=_fit_options)

            if result.success:
                epsilon_r[i + i_start, :] = result.x
                eps_init = result.x

        return epsilon_r, frequencies_GHz

    def linear_regression(self, frequencies_GHz: ndarray, epsilon_r: ndarray) -> (ndarray, tuple, tuple, tuple):
        """
        Perform linear regression on complex permittivity vs frequency.

        Fits linear trends to both real and imaginary parts of permittivity
        as functions of frequency, useful for material characterization and
        extrapolation beyond measured frequency range.

        Parameters
        ----------
        frequencies_GHz : ndarray
            Array of shape (N, 1) of each frequency point
        epsilon_r : ndarray
            Array of shape (N, 2) where:
            - Column 0: Real part of relative permittivity
            - Column 1: Imaginary part of relative permittivity

        Returns
        -------
        regressed_values : ndarray
            Complex-valued array of regressed permittivity at all frequencies.
        re_params : tuple
            Linear fit parameters (slope, intercept) for real part.
        im_params : tuple
            Linear fit parameters (slope, intercept) for imaginary part.
        std_errs : tuple
            Standard errors (real_std_err, imag_std_err) of the regressions.

        Notes
        -----
        - Automatically handles NaN values by masking them out
        - Uses scipy.stats.linregress for robust linear fitting
        - Returns complex permittivity as: real_fit - 1j * imag_fit
        - Useful for identifying frequency-dependent material properties
        """
        # Remove NaN values for regression
        mask = ~isnan(epsilon_r[:, 0])

        # Linear regression on real part
        re_slope, re_intercept, _, _, re_std_err = linregress(frequencies_GHz[mask], epsilon_r[mask, 0])

        # Linear regression on imaginary part
        im_slope, im_intercept, _, _, im_std_err = linregress(frequencies_GHz[mask], epsilon_r[mask, 1])

        # Reconstruct complex permittivity from linear fits
        regressed_values = re_slope * frequencies_GHz + re_intercept + 1j * (
                im_slope * frequencies_GHz + im_intercept
        )

        fn = lambda frequencies_GHz: re_slope * frequencies_GHz + re_intercept + 1j * (
                    im_slope * frequencies_GHz + im_intercept)

        return regressed_values, fn, (re_std_err, im_std_err)


def moving_average(data, half_window_size, full_length: bool = False) -> ndarray[Any, dtype[complexfloating[Any, Any]]]:
    """Calculate moving average of a data series using convolution."""
    i_start = half_window_size
    i_end = len(data) - half_window_size

    moving_avg = zeros_like(data, dtype=complex) * (nan + 0j * nan)
    for i in range(i_start, i_end):
        moving_avg[i] = mean(data[i - half_window_size:i + half_window_size])

    if not full_length:
        moving_avg = moving_avg[i_start:i_end]
    return moving_avg


def filter_s2p(s2p: rf.Network | str, half_window_size, extrapolate=False) -> rf.Network:
    """Apply moving average filter to S-parameter data."""
    if isinstance(s2p, str):
        s_file = rf.Network(s2p)
        frequencies_GHz = s_file.f * 1e-9
    else:
        s_file = s2p
        frequencies_GHz = s_file.f * 1e-9

    if half_window_size < 1:
        return s_file

    # Initialize with NaN and fill filtered regions
    if not extrapolate:
        S = zeros((frequencies_GHz.shape[0], 2, 2), dtype=complex) * (nan + 0j * nan)
    else:
        S = ones((frequencies_GHz.shape[0], 2, 2), dtype=complex)
    S[:, 0, 0] = moving_average(s_file.s[:, 0, 0], half_window_size, full_length=True)
    S[:, 0, 1] = moving_average(s_file.s[:, 0, 1], half_window_size, full_length=True)
    S[:, 1, 0] = moving_average(s_file.s[:, 1, 0], half_window_size, full_length=True)
    S[:, 1, 1] = moving_average(s_file.s[:, 1, 1], half_window_size, full_length=True)
    if extrapolate:
        i_start = half_window_size
        i_end = len(S[:, 1, 1]) - half_window_size
        S[:, 0, 0] = interp1d(frequencies_GHz[i_start:i_end], S[i_start:i_end, 0, 0], kind='nearest-up',
                              fill_value='extrapolate')(frequencies_GHz)
        S[:, 0, 1] = interp1d(frequencies_GHz[i_start:i_end], S[i_start:i_end, 0, 1], kind='nearest-up',
                              fill_value='extrapolate')(frequencies_GHz)
        S[:, 1, 0] = interp1d(frequencies_GHz[i_start:i_end], S[i_start:i_end, 1, 0], kind='nearest-up',
                              fill_value='extrapolate')(frequencies_GHz)
        S[:, 1, 1] = interp1d(frequencies_GHz[i_start:i_end], S[i_start:i_end, 1, 1], kind='nearest-up',
                              fill_value='extrapolate')(frequencies_GHz)
    return rf.Network(s=S, f=frequencies_GHz, f_unit='GHz')


def rewrap_phase(phase, deg=False):
    """Rewrap phase data to remove discontinuities while preserving trends."""
    factor = pi / 180 if deg else 1
    p = unwrap((phase - phase[0]) * factor)
    p = mod(p * 180 / pi + 180, 360) - 180
    return p


def add_noise(network: rf.Network, snr_db=40):
    """Add complex Gaussian noise to S-parameter measurements."""
    noisy_network = network.copy()

    # Compute average signal power across all S-parameters
    signal_power = mean(abs(network.s) ** 2)

    # Convert SNR from dB to linear scale
    snr_linear = 10 ** (snr_db / 10)

    # Compute noise power per real/imaginary component
    noise_power = signal_power / snr_linear

    # Generate complex Gaussian noise
    noise_real = random.normal(scale=sqrt(noise_power / 2), size=network.s.shape)
    noise_imag = random.normal(scale=sqrt(noise_power / 2), size=network.s.shape)
    noise = noise_real + 1j * noise_imag

    # Add noise to the S-parameters
    noisy_network.s += noise

    return noisy_network, sqrt(noise_power / 2)