import inspect
from cmath import nan
import numpy as np
from numpy import linspace, full_like, log10, abs, nan, angle

from qosm import (Vec3, Quaternion, Surface, Item, GaussianBeam, gbtc_beam_tracing, gbtc_compute_coupling)
from qosm.propagation.TRL import TRLCalibration

def get_port_pointing_direction(port_data: dict, sample_attitude_deg: tuple) -> tuple:
    """Calculate port position and pointing direction"""
    attitude_deg = Vec3(port_data.get("attitude_deg", (sample_attitude_deg[0] * 2, sample_attitude_deg[1] * 2,
                                                       sample_attitude_deg[2] * 2)))

    # Get distance from port parameters
    distance_sample_lens = port_data['distance_lens_sample']

    # Calculate total distance including lens system
    total_distance = distance_sample_lens
    for lens in port_data['lenses']:
        total_distance += lens['distance_from_previous'] + lens['thickness']

    # Port position relative to sample (before rotation)
    pos_port = Vec3(0, 0, -total_distance)

    # Apply sample rotation
    angle = attitude_deg.norm()
    if angle > 0:
        axis = attitude_deg.normalised()
        q_rot = Quaternion(angle=angle, axis=axis, deg=True)
        pos_port = q_rot.rotate(pos_port)
        u_port = q_rot.rotate(Vec3(0, 0, 1))  # Pointing towards sample
        att_port = attitude_deg
    else:
        u_port = Vec3(0, 0, 1)
        att_port = Vec3(0, 0, 0)

    if 'offset' in port_data:
        pos_port += Vec3(port_data['offset'])

    return u_port, pos_port, att_port


def create_lens(lens, surface_id=0):

    surfaces = []
    current_z = 0

    for lens in lens:
        ior = lens['ior']
        f = lens['focal']
        R1 = lens['R1'] if lens['R1'] != 0 else nan
        R2 = lens['R2'] if lens['R2'] != 0 else nan
        radius = lens['radius']
        h = lens['thickness']
        current_z += lens['distance_from_previous']

        s1 = Surface(id=surface_id, centre=Vec3(0, 0, current_z), normal=Vec3(0, 0, -1),
                     ior1=1.0, ior2=ior, curvature=R1, max_radius=radius,
                     allow_reflection=False, allow_refraction=True)
        surfaces.append(s1)
        surface_id += 1

        n = ior.real
        # h2 = - f * (n - 1) * h / (n * R2)
        s2 = Surface(id=surface_id, centre=Vec3(0, 0, current_z + h), normal=Vec3(0, 0, 1),
                     ior1=1.0, ior2=ior, curvature=R2, max_radius=radius,
                     allow_reflection=False, allow_refraction=True)
        surfaces.append(s2)
        surface_id += 1

        current_z += h

    return surfaces, surface_id


def create_mut(config, frequency_GHz):
    sample_surfaces = []
    current_z_sample = 0
    surface_id_sample = 100
    sample_attitude_deg = Vec3(config.get('sample_attitude_deg', (0, 0, 0)))
    sample_offset = Vec3(config.get('sample_offset', (0, 0, 0)))

    ior_list = []
    for layer in config['mut']:
        eps = layer['epsilon_r']
        if hasattr(eps, '__call__'):
            # interpolation with frequency (generally from a CSV file)
            ior = np.sqrt(eps(frequency_GHz))
        else:
            ior = np.sqrt(eps)

        ior_list.append(ior)

    # First interface
    s_first = Surface(id=surface_id_sample, centre=Vec3(0, 0, current_z_sample) + sample_offset, normal=Vec3(0, 0, -1),
                      ior1=1.0, ior2=ior_list[0], curvature=nan, max_radius=1.0,
                      allow_reflection=True, allow_refraction=True)
    sample_surfaces.append(s_first)
    surface_id_sample += 1

    for i, layer in enumerate(config['mut']):
        current_z_sample += layer['thickness']
        next_ior = ior_list[i + 1] if i < len(ior_list) - 1 else 1.0
        z_normal = -1
        s = Surface(id=surface_id_sample, centre=Vec3(0, 0, current_z_sample) + sample_offset,
                    normal=Vec3(0, 0, z_normal), ior1=ior_list[i], ior2=next_ior, curvature=nan, max_radius=1.0,
                    allow_reflection=True, allow_refraction=True)
        sample_surfaces.append(s)
        surface_id_sample += 1

    sample_item = Item(pos=Vec3(), attitude_deg=sample_attitude_deg, surfaces=sample_surfaces)
    return sample_item


def simulate(config, frequency_GHz):
    """
    Simulate GBTC measurement.
    Returns: (S11, S12, S21, S22)
    """
    ports = config['ports']
    calibration = config['calibration']
    thru_line_by_reflection = config.get('thru_line_by_reflection', False)

    if len(ports) < 1:
        raise ValueError("Need at least 1 port for simulation")

    port1 = ports[0]
    port2 = ports[1]
    sensor_size = 0.01

    # Sample configuration
    sample_position = Vec3(0, 0, 0)
    sample_attitude_deg = Vec3(config.get('sample_attitude_deg', (0, 0, 0)))

    # Get port 1 position and direction
    u1, pos1, att1 = get_port_pointing_direction(port1, sample_attitude_deg)
    # Create lens group 1
    surfaces1, surface_id = create_lens(port1['lenses'])
    lens1 = Item(pos=pos1, attitude_deg=att1, surfaces=surfaces1)

    # Get port 2 position and direction
    u2, pos2, att2 = get_port_pointing_direction(port2, sample_attitude_deg)
    # Create lens group 2
    surfaces2, surface_id = create_lens(port2['lenses'], surface_id)
    lens2 = Item(pos=pos2, attitude_deg=att2, surfaces=surfaces2)

    # Create sample
    sample_item = create_mut(config, frequency_GHz)

    # Get TX beams
    beam_tx1 = GaussianBeam(frequency_GHz=frequency_GHz, w0=port1['w0'], z0=port1['z0'], ori=pos1, dir=u1)
    beam_tx2 = GaussianBeam(frequency_GHz=frequency_GHz, w0=port2['w0'], z0=port2['z0'], ori=pos2, dir=u2)

    # ===== CALIBRATION SIMULATIONS =====

    mirror1 = Item(pos=Vec3(0, 0, 0), attitude_deg=att1, surfaces=[
        Surface(id=1000, centre=Vec3(0, 0, 0), normal=Vec3(0, 0, -1), ior1=1.0, ior2=1e30,
                curvature=nan, max_radius=sensor_size, allow_reflection=True, allow_refraction=False)])
    mirror2 = Item(pos=Vec3(0, 0, 0), attitude_deg=att2, surfaces=[
        Surface(id=2000, centre=Vec3(0, 0, 0), normal=Vec3(0, 0, -1), ior1=1.0, ior2=1e30,
                curvature=nan, max_radius=sensor_size, allow_reflection=True, allow_refraction=False)])

    beams_s11_refl = gbtc_beam_tracing(beam=beam_tx1, items=[lens1, mirror1], num_reflections=1)
    beams_s21_thru = gbtc_beam_tracing(beam=beam_tx1, items=[lens1, lens2], num_reflections=0)

    if thru_line_by_reflection:
        # TX beams (for S21 and S12) need to reflect on mirror for calibration
        mirror = Item(pos=Vec3(0, 0, 0), attitude_deg=sample_attitude_deg, surfaces=[
            Surface(id=3000, centre=Vec3(0, 0, 0), normal=Vec3(0, 0, -1), ior1=1.0, ior2=1e30,
                    curvature=nan, max_radius=sensor_size, allow_reflection=True, allow_refraction=False)])
        beams_s21_thru = gbtc_beam_tracing(beam=beam_tx1, items=[lens1, mirror, lens2], num_reflections=1)
    else:
        mirror = None

    # Simulate s21_line with tx_beam1 (if TRL)
    beams_s21_line = []
    if calibration['method'] == 'trl':
        line_offset = calibration.get('trl', {}).get('line_offset', 0.00025)
        pos2_line = pos2 - u2 * line_offset
        lens2_line = Item(pos=pos2_line, attitude_deg=att2, surfaces=surfaces2)
        if thru_line_by_reflection:
            beams_s21_line = gbtc_beam_tracing(beam=beam_tx1, items=[lens1, mirror, lens2_line], num_reflections=1)
        else:
            beams_s21_line = gbtc_beam_tracing(beam=beam_tx1, items=[lens1, lens2_line], num_reflections=0)

    # Simulate s22_reflect with tx_beam2
    beams_s22_refl = gbtc_beam_tracing(beam=beam_tx2, items=[lens2, mirror2], num_reflections=1)

    # Simulate full system with beams=(tx_beam1, tx_beam2)
    beams_system = gbtc_beam_tracing(beams=(beam_tx1, beam_tx2), items=(lens1, sample_item, lens2),
                                     num_reflections=config.get('num_reflections', 2))

    # ===== COUPLING CALCULATIONS =====

    # Coupling s11_reflect, id_beam=0
    s11_refl = gbtc_compute_coupling(beams=beams_s11_refl, w0_tx=port1['w0'], w0_rx=port1['w0'],
                                              r_rx=pos1, u_rx=u1, max_radius=sensor_size, id_beam=0)

    # Coupling s22_reflect, id_beam=0
    s22_refl = gbtc_compute_coupling(beams=beams_s22_refl, w0_tx=port2['w0'], w0_rx=port2['w0'],
                                              r_rx=pos2, u_rx=u2, max_radius=sensor_size, id_beam=0) # 0.001 too small

    # Coupling s21_thru, id_beam=0
    s21_thru = gbtc_compute_coupling(beams=beams_s21_thru, w0_tx=port1['w0'], w0_rx=port2['w0'],
                                              r_rx=pos2, u_rx=u2, max_radius=sensor_size, id_beam=0) # 0.001 too small

    # Coupling s11, s21 with id_beam=0
    s11_raw = gbtc_compute_coupling(beams=beams_system, w0_tx=port1['w0'], w0_rx=port1['w0'],
                                             r_rx=pos1, u_rx=u1, max_radius=sensor_size, id_beam=0) # 0.001 too small

    s21_raw = gbtc_compute_coupling(beams=beams_system, w0_tx=port1['w0'], w0_rx=port2['w0'],
                                             r_rx=pos2, u_rx=u2, max_radius=sensor_size, id_beam=0) # 0.001 too small

    # Coupling s22, s12 with id_beam=1
    s22_raw = gbtc_compute_coupling(beams=beams_system, w0_tx=port2['w0'], w0_rx=port2['w0'],
                                             r_rx=pos2, u_rx=u2, max_radius=sensor_size, id_beam=1) # 0.001 too small

    s12_raw = gbtc_compute_coupling(beams=beams_system, w0_tx=port2['w0'], w0_rx=port1['w0'],
                                             r_rx=pos1, u_rx=u1, max_radius=sensor_size, id_beam=1) # 0.001 too small

    # Apply calibration
    if calibration['method'] == 'trl' and  not np.isnan(s21_thru) and not np.isnan(s11_refl):
        # Coupling s21_line, id_beam=0 (if necessary)
        line_offset = calibration['trl']['line_offset']
        pos2_line = pos2 - u2 * line_offset
        s21_line = gbtc_compute_coupling(beams=beams_s21_line, w0_tx=port1['w0'], w0_rx=port2['w0'],
                                                  r_rx=pos2_line, u_rx=u2, max_radius=sensor_size, id_beam=0)

        trl = TRLCalibration(calibration['trl'])
        trl.extract_error_terms(s21_thru, s11_refl, s21_line)
        s11_cal, s12_cal, s21_cal, s22_cal = trl.apply_correction(s11_raw, s12_raw, s21_raw, s22_raw)
        return s11_cal, s12_cal, s21_cal, s22_cal
    else:
        s11 = -s11_raw / s11_refl if not np.isnan(s11_refl) and abs(s11_refl) != 0 else nan
        s21 = s21_raw / s21_thru if not np.isnan(s21_thru) and abs(s21_thru) != 0 else nan
        s22 = -s22_raw / s22_refl if not np.isnan(s22_refl) and abs(s22_refl) != 0 else nan
        s12 = s12_raw / s21_thru if not np.isnan(s21_thru) and abs(s21_thru) != 0 else nan
        return s11, s12, s21, s22


# Example usage
if __name__ == "__main__":

    import matplotlib
    matplotlib.use('Qt5Agg')
    from matplotlib import pyplot as plt

    # Example with two ports
    config_two_ports = {
        'ports': [
            {
                'w0': 0.0023, 'z0': 0.0,
                'distance_lens_sample': 0.200,
                'attitude_deg': (0, 0, 0),
                'lenses': [
                    {'focal': 0.1, 'R1': 0.0, 'R2': -0.04, 'radius': 0.05,
                     'thickness': 0.0138, 'ior': 1.4, 'distance_from_previous': 0.095}
                ]
            },
            {
                'w0': 0.0023, 'z0': 0.0,
                'distance_lens_sample': 0.200,
                'attitude_deg': (0, 180, 0),
                'lenses': [
                    {'focal': 0.1, 'R1': 0.0, 'R2': -0.04, 'radius': 0.05,
                     'thickness': 0.0138, 'ior': 1.4, 'distance_from_previous': 0.095}
                ]
            }
        ],
        'sample_attitude_deg': (0.0, 0.0, 0.0),
        'mut': [
            {'epsilon_r': 2.53 - 0.005j, 'thickness': 0.012815}
        ],
        'calibration': {
            'method': 'trl',
            'trl': {
                'line_offset': 0.00025,
                'type_reflector': 'cc',
            }
        },
        'num_reflections': 4,
    }

    frequencies_GHz = linspace(220., 330., 1001)

    # Test two ports
    s11 = full_like(frequencies_GHz, np.nan, dtype=complex)
    s12 = full_like(frequencies_GHz, np.nan, dtype=complex)
    s21 = full_like(frequencies_GHz, np.nan, dtype=complex)
    s22 = full_like(frequencies_GHz, np.nan, dtype=complex)
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