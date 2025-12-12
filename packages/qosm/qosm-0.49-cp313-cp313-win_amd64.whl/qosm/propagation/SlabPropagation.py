import matplotlib.pyplot as plt
from numpy import array
from qosm._core import field_expansion, VirtualSource, Medium, surface_beam_tracing, beam_tracing

from qosm.items.SlabMesh import SlabMesh
from qosm.utils.Pose import Frame, Vector, create_meshgrid


class MLS:

    def __init__(self, size_interfaces: tuple, h_mm: tuple, media: tuple, d_mm: float, kappa: float, frame: Frame,
                 external_medium: Medium = Medium(), display: bool = False):

        self._interfaces = []
        self._size = size_interfaces
        self._h = h_mm
        self._d = d_mm * 1e-3
        self._kappa = kappa
        length = 0
        i = 0

        list_h = []
        for h in h_mm:
            list_h.append(h)
        list_h.append(1e30)

        list_medium = [external_medium, ]
        for m in media:
            list_medium.append(m)
        list_medium.append(external_medium)

        for i in range(len(list_h)):
            h = list_h[i] * 1e-3
            obj = SlabMesh(frame)
            obj.load(element_size=self._d, shape='disk', size=size_interfaces, flip_normal=True,
                     offset=Vector(0, 0, length))
            obj.set_dioptre(list_medium[i], list_medium[i+1])
            length += h
            self._interfaces.append(obj)

        print('Created structure with %d interfaces' % len(self._interfaces))

        if display:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            for o in self._interfaces:
                o.plot(ax)
            plt.show()

    def propagation(self, source, d_mm: float, n_multi_reflections: int = 1) -> (VirtualSource, VirtualSource):

        geo = []
        for interface in self._interfaces:
            geo += interface.geometry

        su = self._size[0] * 1e3
        sv = self._size[1] * 1e3
        r_gbe, g = create_meshgrid(u_min_mm=-su/2, u_max_mm=su/2, u_step_mm=d_mm,
                                   v_min_mm=-sv/2, v_max_mm=sv/2, v_step_mm=d_mm,
                                   n_mm=45, plane='xy')
        beams_gbe = field_expansion(source, points=r_gbe, w0=d_mm * 1e-3, pw_threshold=1e-5)
        beams_gbt = beam_tracing(geometry=geo, beams=beams_gbe, bounces=(0, 2), pw_min=1e-5,
                                 increment_bouncing=False)
        vsrc_ref = VirtualSource(frequency_GHz=source.freq * 1e-9)
        vsrc_ref.init(beams=beams_gbt)

        vsrc_init = VirtualSource(frequency_GHz=source.freq * 1e-9)
        vsrc_fwd_list = array([VirtualSource(frequency_GHz=source.freq * 1e-9) for _ in self._interfaces])
        vsrc_bwd_list = array([VirtualSource(frequency_GHz=source.freq * 1e-9) for _ in self._interfaces])

        vsrc_fwd_last = source
        n_int = len(self._interfaces)

        # forward propagation
        print('==> Perform FWD propagation (%d interfaces)' % n_int)

        z_mm = self._interfaces[0].vertices[:, 2].mean() * 1e3
        r_gbe, g = create_meshgrid(u_min_mm=-su / 2, u_max_mm=su / 2, u_step_mm=d_mm,
                                   v_min_mm=-sv / 2, v_max_mm=sv / 2, v_step_mm=d_mm,
                                   n_mm=z_mm - 4, plane='xy')
        r_gbe = self._interfaces[0].frame.to_ref(r_gbe)

        print('     {GBE initialised with %d points}' % r_gbe.shape[0])
        for i in range(n_int):
            interface = self._interfaces[i]
            print('  -> Interface %d : %.2f -> %.2f' % (i, interface.dioptre.n1, interface.dioptre.n2))

            out_beams = beam_tracing(geometry=interface.geometry, beams=beams_gbe, bounces=(1, 1), pw_min=1e-7,
                                     increment_bouncing=False)

            z_mm = interface.vertices[:, 2].mean() * 1e3
            r_gbe, g = create_meshgrid(u_min_mm=-su / 2, u_max_mm=su / 2, u_step_mm=d_mm,
                                       v_min_mm=-sv / 2, v_max_mm=sv / 2, v_step_mm=d_mm,
                                       n_mm=z_mm+2, plane='xy')
            r_gbe = interface.frame.to_ref(r_gbe)
            vsrc_t = VirtualSource(frequency_GHz=source.freq*1e9)
            vsrc_t.init(beams=out_beams)
            vsrc_t = vsrc_t.filter(type=2)
            beams_gbe = field_expansion(vsrc_t, points=r_gbe, w0=d_mm * 1e-3, pw_threshold=1e-5)

            if i == 0:
                vsrc_init.init(beams=out_beams)
                vsrc_init = vsrc_init.filter(type=0)

        vsrc_fwd_list[n_int - 1] = VirtualSource(frequency_GHz=source.freq*1e9)
        vsrc_fwd_list[n_int - 1].init(beams=beams_gbe)

        # backward propagation
        """print('==> Perform BWD propagation (%d interfaces)' % n_int)
        i = n_int-2
        vsrc_bwd_last = vsrc_bwd_list[i+1]
        while i >= 0:
            print('  -> Interface %d' % i)
            interface = self._interfaces[i]
            z_mm = interface.vertices[:, 2].mean() * 1e3
            r_gbe, g = create_meshgrid(u_min_mm=-su/2, u_max_mm=su/2, u_step_mm=d_mm,
                                       v_min_mm=-sv/2, v_max_mm=sv/2, v_step_mm=d_mm,
                                       n_mm=z_mm + 0.5, plane='xy')
            r_gbe = interface.frame.to_ref(r_gbe)

            print('     {GBE initialised with %d points}' % r_gbe.shape[0])
            beams = field_expansion(vsrc=vsrc_bwd_last, points=r_gbe, w0=self._d, pw_threshold=1e-5)

            out_beams = beam_tracing(geometry=interface.geometry, beams=beams, bounces=(1, 1), pw_min=1e-5,
                                     increment_bouncing=False)
            vsrc_res = VirtualSource(frequency_GHz=source.freq * 1e-9)
            vsrc_res.init(beams=out_beams)

            vsrc_bwd_last = vsrc_res.filter(type=2).extends(vsrc_bwd_list[i])

            vsrc_bwd_list[i] = VirtualSource(frequency_GHz=source.freq * 1e-9)
            vsrc_fwd_list[i].extends(vsrc_res.filter(type=1))
            if i == 0:
                vsrc_bwd_list[i].extends(vsrc_bwd_last)

            i -= 1"""

        print('==> CREATE FINAL VIRTUAL SOURCE')
        res = VirtualSource(frequency_GHz=source.freq * 1e-9)
        res.init(beams=vsrc_init.beams + vsrc_fwd_list[n_int-1].beams)

        return res, vsrc_ref
