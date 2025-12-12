import pickle
from copy import deepcopy
from pathlib import Path

from scipy.interpolate import interp1d

from qosm.propagation.GBTC import simulate
from qosm.propagation.PW import simulate as simulate_pw
from numpy import linspace, array, abs, genfromtxt, full, nan


class GBTCSimulationManager:
    def __init__(self, request_data, ports_data, sample_data, sweep_data=None, load_csv: bool = True, curr_file = None):
        """
        Generate GBTC configuration from ports, sample, request and sweep data.

        Args:
            request_data: Request dictionary with frequency sweep, calibration, etc.
            ports_data: List of port dictionaries with their parameters
            sample_data: Sample dictionary with MUT layers and other parameters
            sweep_data: Sweep dictionary

        Returns:
            Complete GBTC configuration dictionary
        """

        self.request_data = request_data['parameters']
        analysis_config = self.request_data.get('analysis_options', {})

        if sweep_data is None:
            sweep_target = ('None', None)
            sweep_attribute = None
        else:
            sweep_target = sweep_data.get('target', ('None', None))
            sweep_attribute = sweep_data.get('attribute', None)

        if sweep_target[0] != 'None':
            num_iterations = int(sweep_data['sweep'][2])
            start_val = float(sweep_data['sweep'][0])
            stop_val = float(sweep_data['sweep'][1])
            value_array = linspace(start_val, stop_val, num_iterations, endpoint=True)
        else:
            value_array = array([])
            num_iterations = 1
        frequency_list = linspace(float(self.request_data['frequency_sweep']['start']),
                                  float(self.request_data['frequency_sweep']['stop']),
                                  int(self.request_data['frequency_sweep']['num_points']),
                                  endpoint=True)

        # Create request
        self.requests = {
            'GBTCSim': {
                'name': 'GBTC Simulation',
                'type': 'GBTCSim',
                'sweep_target': sweep_target,
                'sweep_values': value_array,
                'sweep_attribute': sweep_attribute,
                'sweep_frequency_values': frequency_list,
                'compare_plane_wave': analysis_config.get('compare_plane_wave', False),
                'enabled': False
            }
        }

        # Create result structure
        self.results = {
            'GBTCSim': {
                'req_uuid': 'GBTCSim',
                'req_name': 'GBTC Simulation',
                'request_type': 'GBTCSim',
                'sweep_values': value_array,
                'sweep_attribute': sweep_attribute,
                'sweep_frequency_values': frequency_list,
                'compare_plane_wave': analysis_config.get('compare_plane_wave', False),
                'data': {
                    'gbtc': {
                        'S11': full((num_iterations, frequency_list.shape[0]), nan, dtype=complex),
                        'S12': full((num_iterations, frequency_list.shape[0]), nan, dtype=complex),
                        'S21': full((num_iterations, frequency_list.shape[0]), nan, dtype=complex),
                        'S22': full((num_iterations, frequency_list.shape[0]), nan, dtype=complex)
                    }
                }
            }
        }
        if analysis_config.get('compare_plane_wave', False):
            self.results['GBTCSim']['data']['pw'] = {
                'S11': full((num_iterations, frequency_list.shape[0]), nan, dtype=complex),
                'S12': full((num_iterations, frequency_list.shape[0]), nan, dtype=complex),
                'S21': full((num_iterations, frequency_list.shape[0]), nan, dtype=complex),
                'S22': full((num_iterations, frequency_list.shape[0]), nan, dtype=complex)
            }

        # Extract frequency sweep from request
        sweep_config = {
            'range': (self.request_data['frequency_sweep']['start'], self.request_data['frequency_sweep']['stop']),
            'num_points': int(self.request_data['frequency_sweep']['num_points'])
        }

        # Process ports
        ports_config = []
        for port_data in ports_data:
            port_params = port_data.get('parameters', {})

            # Extract beam parameters
            beam = port_params.get('beam', {})
            port_config = {
                'w0': beam['w0'],  # Default 10mm
                'z0': beam['z0'],
                'distance_lens_sample': port_params['distance_sample_output_lens'],
            }

            # Add distance if available
            follow_sample = port_params.get('follow_sample', False)
            if not follow_sample:
                port_config['attitude_deg'] = port_params.get('attitude')
            if 'offset' in port_params:
                port_config['offset'] = port_params['offset']

            # Process lenses
            port_config['lenses'] = port_params.get('lenses', [])

            ports_config.append(port_config)

        # Extract MUT layers from sample
        sample_params = sample_data.get('parameters', sample_data)
        mut_layers = deepcopy(sample_params.get('mut', []))

        # load csv if needed
        if load_csv:
            for i_mut, mut in enumerate(mut_layers):
                if isinstance(mut['epsilon_r'], str) and '.csv' in mut['epsilon_r']:
                    path = mut['epsilon_r']
                    if path.startswith('./') and curr_file is not None:
                        path = path.replace('./', str(Path(curr_file).parent) + '/')

                    skip_header = 1
                    # check if thickness is stored in the file
                    with open(path, 'r') as f:
                        f.readline()
                        second_line = f.readline().strip()
                        if second_line.startswith('#'):
                            skip_header = 2

                    data = genfromtxt(path, delimiter=',', skip_header=skip_header)
                    if data[0, 0] > 1e3:
                        # Hz -> GHz
                        data[:, 0] *= 1e-9
                    mut['epsilon_r'] = interp1d(data[:, 0], data[:, 1] + data[:, 2] * 1j, fill_value='extrapolate')

        # Get other sample parameters
        sample_offset = sample_params.get('offset', (0, 0, 0))
        sample_attitude = sample_params['rotation']
        num_reflections = sample_params['num_reflections']

        # Get calibration from request
        calibration = self.request_data['calibration']

        # Build complete configuration
        self.config = {
            'sweep': sweep_config,
            'ports': ports_config,
            'sample_attitude_deg': sample_attitude,
            'sample_offset': sample_offset,
            'mut': mut_layers,
            'calibration': calibration,
            'num_reflections': num_reflections,
            'thru_line_by_reflection': analysis_config.get('thru_line_by_reflection', False),
            'compare_plane_wave': analysis_config.get('compare_plane_wave', False)
        }

        if 'trl' in self.request_data:
            self.config['trl'] = self.request_data['trl']

    def run(self, progress_callback=None, warning_callback=None):
        if progress_callback:
            progress_callback(0)

        frequency_list = self.requests['GBTCSim']['sweep_frequency_values']
        value_array = self.requests['GBTCSim']['sweep_values']
        sweep_target = self.requests['GBTCSim']['sweep_target']
        sweep_attribute = self.requests['GBTCSim']['sweep_attribute']
        num_iterations = value_array.shape[0] if value_array.shape[0] > 0 else 1
        num_freq = frequency_list.shape[0]

        for iteration in range(num_iterations):

            if sweep_target[0] == 'gbtc_port':
                port_uuid = sweep_target[1]
                port_idx = -1

                if self.request_data['port1'] == port_uuid:
                    port_idx = 0
                elif self.request_data['port1'] == port_uuid:
                    port_idx = 1
                else:
                    pass

                indexes = {'delta.x': 0, 'delta.y': 1, 'delta.z': 2}
                # avoid 'tuple' object does not support item assignment
                values = [0, 0, 0]
                values[indexes[sweep_attribute]] = value_array[iteration] * 1e3
                self.config['ports'][port_idx]['offset'] = values

            if sweep_target[0] == 'gbtc_sample':
                indexes = {'pose.rx': 0, 'pose.ry': 1, 'pose.rz': 2}
                # avoid 'tuple' object does not support item assignment
                values = [el for el in self.config['sample_attitude_deg']]
                values[indexes[sweep_attribute]] = value_array[iteration]
                self.config['sample_attitude_deg'] = values


            for _i, frequency_GHz in enumerate(frequency_list):
                if progress_callback:
                    progress_percent = (iteration * num_freq + _i) * 100 // (num_iterations * num_freq)
                    progress_callback(progress_percent)

                s11, s12, s21, s22 = simulate(self.config, frequency_GHz)
                self.results['GBTCSim']['data']['gbtc']['S11'][iteration, _i] = s11
                self.results['GBTCSim']['data']['gbtc']['S12'][iteration, _i] = s12
                self.results['GBTCSim']['data']['gbtc']['S21'][iteration, _i] = s21
                self.results['GBTCSim']['data']['gbtc']['S22'][iteration, _i] = s22

                if self.config['compare_plane_wave']:
                    s11, s12, s21, s22 = simulate_pw(self.config, frequency_GHz)
                    if self.config['thru_line_by_reflection']:
                        self.results['GBTCSim']['data']['pw']['S12'][iteration, _i] = s11
                        self.results['GBTCSim']['data']['pw']['S21'][iteration, _i] = s22
                    else:
                        self.results['GBTCSim']['data']['pw']['S11'][iteration, _i] = s11
                        self.results['GBTCSim']['data']['pw']['S12'][iteration, _i] = s12
                        self.results['GBTCSim']['data']['pw']['S21'][iteration, _i] = s21
                        self.results['GBTCSim']['data']['pw']['S22'][iteration, _i] = s22

        if progress_callback:
            progress_callback(100)


def create_gbtc_from_qosm(file_path) -> GBTCSimulationManager:
    from qosm.gui.managers import ObjectManager, RequestManager, SimulationAborted

    # Load data from binary file
    with open(file_path, 'rb') as file:
        data = pickle.load(file)

    # Restore objects and sources
    object_manager = data.get('object_manager', ObjectManager())
    request_manager = data.get('request_manager', RequestManager())

    request_data = request_manager.requests
    object_data = object_manager.objects
    sweep_data = None

    ports_data = [obj for obj in object_data.values() if obj['type'] == 'GBTCPort']
    sample_data = [obj for obj in object_data.values() if obj['type'] == 'GBTCSample']
    request_data = [req for req in request_data.values() if req['type'] == 'GBTC']
    if len(sample_data) == 0:
        raise SimulationAborted('GBTC Sample is missing')
    if len(request_data) == 0:
        raise SimulationAborted('GBTC Request is missing')
    sim_manager = GBTCSimulationManager(request_data[0], ports_data, sample_data[0], sweep_data,
                                        curr_file=file_path)

    return sim_manager


if __name__ == "__main__":
    # Sample data for editing
    ports = {
        'kjbikjl': {
            'name': 'port1',
            'parameters': {
                'beam': {
                    'w0': 0.01,
                    'z0': 0.0
                },
                'distance_sample_output_lens': 0.2,
                'attitude': (0, 0.0, 0),
                'follow_sample': False,
                'lenses': [
                    {
                        'focal': 0.1,
                        'R1': 0.0,
                        'R2': -0.04,
                        'radius': 0.05,
                        'thickness': 0.0138,
                        'ior': 1.4,
                        'distance_from_previous': 0.095
                    },
                ]
            }
        },
        'dffezf': {
            'name': 'port2',
            'parameters': {
                'beam': {
                    'w0': 0.01,
                    'z0': 0.0
                },
                'distance_sample_output_lens': 0.2,
                'attitude': (0, 180.0, 0),
                'follow_sample': False,
                'lenses': [
                    {
                        'focal': 0.1,
                        'R1': 0.0,
                        'R2': -0.04,
                        'radius': 0.05,
                        'thickness': 0.0138,
                        'ior': 1.4,
                        'distance_from_previous': 0.095
                    },
                ]
            }
        }
    }

    request = {
        'port1': 'kjbikjl',
        'port2':'dffezf',
        'frequency_sweep': {
            'start': 220.,
            'stop': 330.,
            'num_points': 1001
        },
        'calibration': 'trl',
        'trl': {
            'type_reflector': 'cc',
            'line_offset': 0.00025
        }
    }

    sample = {
        'mut': [
            {
                'epsilon_r': 2.531,
                'thickness': 0.012815
            },
        ],
        'num_reflections': 4,
        'rotation': [.0, .0, .0]
    }

    ports_list = (ports[request['port1']], ports[request['port2']])

    manager = GBTCSimulationManager(request, ports_list, sample)

    from numpy import log10, angle

    import matplotlib

    matplotlib.use('Qt5Agg')
    from matplotlib import pyplot as plt

    manager.run()
    frequencies_GHz = manager.results['GBTCSim']['sweep_frequency_values']

    # Test two ports
    s11 = manager.results['GBTCSim']['data']['gbtc']['S11'][0, :]
    s12 = manager.results['GBTCSim']['data']['gbtc']['S12'][0, :]
    s21 = manager.results['GBTCSim']['data']['gbtc']['S21'][0, :]
    s22 = manager.results['GBTCSim']['data']['gbtc']['S22'][0, :]

    _, axes = plt.subplots(2, 2)
    axes[0, 0].plot(frequencies_GHz, 20 * log10(abs(s11)), label='S11')
    axes[0, 0].plot(frequencies_GHz, 20 * log10(abs(s22)), label='S22')
    axes[0, 1].plot(frequencies_GHz, 20 * log10(abs(s21)), label='S21')
    axes[0, 1].plot(frequencies_GHz, 20 * log10(abs(s12)), label='S12')

    axes[1, 0].plot(frequencies_GHz, angle(s11), label='S11')
    axes[1, 0].plot(frequencies_GHz, angle(s22), label='S22')
    axes[1, 1].plot(frequencies_GHz, angle(s21), label='S21')
    axes[1, 1].plot(frequencies_GHz, angle(s12), label='S12')

    for ax in axes.flat:
        ax.legend()

    plt.show()
