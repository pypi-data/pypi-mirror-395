# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Rhoksat(KaitaiStruct):
    """:field callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field ssid_mask: ax25_frame.ax25_header.dest_ssid_raw.ssid_mask
    :field ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field value: ax25_frame.ax25_header.dest_ssid_raw.value
    :field src_callsign_raw_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field src_ssid_raw_ssid_mask: ax25_frame.ax25_header.src_ssid_raw.ssid_mask
    :field src_ssid_raw_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field src_ssid_raw_value: ax25_frame.ax25_header.src_ssid_raw.value
    :field ctl: ax25_frame.ax25_header.ctl
    :field pid: ax25_frame.payload.pid
    :field beacon_id: ax25_frame.payload.beacon.beacon_id
    :field num_reboots: ax25_frame.payload.beacon.num_reboots
    :field bat_voltage: ax25_frame.payload.beacon.bat_voltage
    :field rate_x: ax25_frame.payload.beacon.imtq.rate_x
    :field rate_y: ax25_frame.payload.beacon.imtq.rate_y
    :field rate_z: ax25_frame.payload.beacon.imtq.rate_z
    :field total: ax25_frame.payload.beacon.imtq.total
    :field num_of_sweeps: ax25_frame.payload.beacon.num_of_sweeps
    :field num_of_logs: ax25_frame.payload.beacon.num_of_logs
    :field time: ax25_frame.payload.beacon.time
    :field sdcard_id: ax25_frame.payload.beacon.sdcard_id
    :field gyro_x_raw: ax25_frame.payload.beacon.gyro.gyro_x_raw
    :field gyro_y_raw: ax25_frame.payload.beacon.gyro.gyro_y_raw
    :field gyro_z_raw: ax25_frame.payload.beacon.gyro.gyro_z_raw
    :field acc_x_raw: ax25_frame.payload.beacon.accelerometer.acc_x_raw
    :field acc_y_raw: ax25_frame.payload.beacon.accelerometer.acc_y_raw
    :field acc_z_raw: ax25_frame.payload.beacon.accelerometer.acc_z_raw
    :field tl: ax25_frame.payload.beacon.sun_sensor.tl
    :field bl: ax25_frame.payload.beacon.sun_sensor.bl
    :field br: ax25_frame.payload.beacon.sun_sensor.br
    :field tr: ax25_frame.payload.beacon.sun_sensor.tr
    :field pd_z_minus: ax25_frame.payload.beacon.panels.pd_z_minus
    :field pd_x_minus: ax25_frame.payload.beacon.panels.pd_x_minus
    :field pd_x_plus: ax25_frame.payload.beacon.panels.pd_x_plus
    :field pd_y_plus: ax25_frame.payload.beacon.panels.pd_y_plus
    :field pd_y_minus: ax25_frame.payload.beacon.panels.pd_y_minus
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = Rhoksat.Ax25Frame(self._io, self, self._root)

    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = Rhoksat.Ax25Header(self._io, self, self._root)
            _on = (self.ax25_header.ctl & 19)
            if _on == 0:
                self.payload = Rhoksat.IFrame(self._io, self, self._root)
            elif _on == 3:
                self.payload = Rhoksat.UiFrame(self._io, self, self._root)
            elif _on == 19:
                self.payload = Rhoksat.UiFrame(self._io, self, self._root)
            elif _on == 16:
                self.payload = Rhoksat.IFrame(self._io, self, self._root)
            elif _on == 18:
                self.payload = Rhoksat.IFrame(self._io, self, self._root)
            elif _on == 2:
                self.payload = Rhoksat.IFrame(self._io, self, self._root)


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = Rhoksat.CallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = Rhoksat.SsidMask(self._io, self, self._root)
            self.src_callsign_raw = Rhoksat.CallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = Rhoksat.SsidMask(self._io, self, self._root)
            self.ctl = self._io.read_u1()


    class UiFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self.beacon = Rhoksat.Beacon(self._io, self, self._root)


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")
            if not self.callsign == u"WP2XJL":
                raise kaitaistruct.ValidationNotEqualError(u"WP2XJL", self.callsign, self._io, u"/types/callsign/seq/0")


    class Accelerometer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.acc_x_raw = self._io.read_u2le()
            self.acc_y_raw = self._io.read_u2le()
            self.acc_z_raw = self._io.read_u2le()


    class Gyro(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.gyro_x_raw = self._io.read_u2le()
            self.gyro_y_raw = self._io.read_u2le()
            self.gyro_z_raw = self._io.read_u2le()


    class IFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self.beacon = Rhoksat.Beacon(self._io, self, self._root)


    class SsidMask(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ssid_mask = self._io.read_u1()

        @property
        def ssid(self):
            if hasattr(self, '_m_ssid'):
                return self._m_ssid

            self._m_ssid = ((self.ssid_mask & 15) >> 1)
            return getattr(self, '_m_ssid', None)


    class Beacon(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.beacon_id = self._io.read_u1()
            if not self.beacon_id == 253:
                raise kaitaistruct.ValidationNotEqualError(253, self.beacon_id, self._io, u"/types/beacon/seq/0")
            self.num_reboots = self._io.read_s4le()
            self.bat_voltage = self._io.read_s4le()
            self.imtq = Rhoksat.Imtq(self._io, self, self._root)
            self.num_of_sweeps = self._io.read_u4le()
            self.num_of_logs = self._io.read_u4le()
            self.time = self._io.read_u4le()
            self.sdcard_id = self._io.read_u1()
            if not  ((self.sdcard_id == 0) or (self.sdcard_id == 1)) :
                raise kaitaistruct.ValidationNotAnyOfError(self.sdcard_id, self._io, u"/types/beacon/seq/7")
            self.gyro = Rhoksat.Gyro(self._io, self, self._root)
            self.accelerometer = Rhoksat.Accelerometer(self._io, self, self._root)
            self.sun_sensor = Rhoksat.SunSensor(self._io, self, self._root)
            self.panels = Rhoksat.Panels(self._io, self, self._root)


    class SunSensor(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.tl = self._io.read_f4le()
            self.bl = self._io.read_f4le()
            self.br = self._io.read_f4le()
            self.tr = self._io.read_f4le()


    class Panels(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pd_z_minus = self._io.read_u4le()
            self.pd_x_minus = self._io.read_u4le()
            self.pd_x_plus = self._io.read_u4le()
            self.pd_y_plus = self._io.read_u4le()
            self.pd_y_minus = self._io.read_u4le()


    class Imtq(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rate_x = self._io.read_u2le()
            self.rte_y = self._io.read_u2le()
            self.rate_z = self._io.read_u2le()
            self.total = self._io.read_u2le()


    class CallsignRaw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw__raw_callsign_ror = self._io.read_bytes(6)
            self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
            _io__raw_callsign_ror = KaitaiStream(BytesIO(self._raw_callsign_ror))
            self.callsign_ror = Rhoksat.Callsign(_io__raw_callsign_ror, self, self._root)



