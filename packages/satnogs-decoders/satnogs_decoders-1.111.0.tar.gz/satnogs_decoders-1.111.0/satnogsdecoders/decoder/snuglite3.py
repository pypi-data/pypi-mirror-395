# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Snuglite3(KaitaiStruct):
    """:field destination_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field source_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field csp_header_priority: payload.csp_header_priority
    :field csp_header_source: payload.csp_header_source
    :field csp_header_destination: payload.csp_header_destination
    :field csp_header_destination_port: payload.csp_header_destination_port
    :field csp_header_source_port: payload.csp_header_source_port
    :field csp_header_reserved: payload.csp_header_reserved
    :field csp_header_flags: payload.csp_header_flags
    
    :field last_telecommand_number: payload.last_telecommand_number
    :field telecommand_counter: payload.telecommand_counter
    :field gpstime_itow: payload.gpstime_itow
    :field gpstime_ftow: payload.gpstime_ftow
    :field position_flag: payload.position_flag
    :field position_x: payload.position_x
    :field position_y: payload.position_y
    :field position_z: payload.position_z
    :field velocity_x: payload.velocity_x
    :field velocity_y: payload.velocity_y
    :field velocity_z: payload.velocity_z
    :field battery_mode: payload.battery_mode
    :field battery_voltage: payload.battery_voltage
    :field target_altitude_q1: payload.target_altitude_q1
    :field target_altitude_q2: payload.target_altitude_q2
    :field target_altitude_q3: payload.target_altitude_q3
    :field estimated_altitude_q1: payload.estimated_altitude_q1
    :field estimated_altitude_q2: payload.estimated_altitude_q2
    :field estimated_altitude_q3: payload.estimated_altitude_q3
    :field estimated_angular_rate_roll: payload.estimated_angular_rate_roll
    :field estimated_angular_rate_pitch: payload.estimated_angular_rate_pitch
    :field estimated_angular_rate_yaw: payload.estimated_angular_rate_yaw
    :field sun_measurement_x: payload.sun_measurement_x
    :field sun_measurement_y: payload.sun_measurement_y
    :field sun_measurement_z: payload.sun_measurement_z
    :field relnav_mode: payload.relnav_mode
    :field ocs_mode: payload.ocs_mode
    :field ocs_mode_sate: payload.ocs_mode_sate
    :field target_relative_distance: payload.target_relative_distance
    :field current_relative_vector_x: payload.current_relative_vector_x
    :field current_relative_vector_y: payload.current_relative_vector_y
    :field current_relative_vector_z: payload.current_relative_vector_z
    :field current_relative_velocity_x: payload.current_relative_velocity_x
    :field current_relative_velocity_y: payload.current_relative_velocity_y
    :field current_relative_velocity_z: payload.current_relative_velocity_z
    :field operational_mode: payload.operational_mode
    :field deploy_flag: payload.deploy_flag
    :field satellite_time: payload.satellite_time
    
    :field page_active_bitmask: payload.full_beacon_page_number.page_number.page_active_bitmask
    :field battery_current: payload.full_beacon_page_number.page_number.battery_current
    :field power_switch_status_gps_0: payload.full_beacon_page_number.page_number.power_switch_status_gps_0
    :field power_switch_status_gps_1: payload.full_beacon_page_number.page_number.power_switch_status_gps_1
    :field power_switch_status_gps_2: payload.full_beacon_page_number.page_number.power_switch_status_gps_2
    :field power_switch_status_deploy: payload.full_beacon_page_number.page_number.power_switch_status_deploy
    :field power_switch_status_sub_trx: payload.full_beacon_page_number.page_number.power_switch_status_sub_trx
    :field power_switch_status_main_trx: payload.full_beacon_page_number.page_number.power_switch_status_main_trx
    :field power_switch_current_1: payload.full_beacon_page_number.page_number.power_switch_current_1
    :field power_switch_current_2: payload.full_beacon_page_number.page_number.power_switch_current_2
    :field power_switch_current_3: payload.full_beacon_page_number.page_number.power_switch_current_3
    :field power_switch_current_4: payload.full_beacon_page_number.page_number.power_switch_current_4
    :field power_switch_current_5: payload.full_beacon_page_number.page_number.power_switch_current_5
    :field power_switch_current_6: payload.full_beacon_page_number.page_number.power_switch_current_6
    :field solar_panel_input_voltage_z: payload.full_beacon_page_number.page_number.solar_panel_input_voltage_z
    :field solar_panel_input_voltage_y: payload.full_beacon_page_number.page_number.solar_panel_input_voltage_y
    :field solar_panel_input_voltage_deployed_panel: payload.full_beacon_page_number.page_number.solar_panel_input_voltage_deployed_panel
    :field solar_panel_input_current_z: payload.full_beacon_page_number.page_number.solar_panel_input_current_z
    :field solar_panel_input_current_y: payload.full_beacon_page_number.page_number.solar_panel_input_current_y
    :field solar_panel_input_current_deployed_panel: payload.full_beacon_page_number.page_number.solar_panel_input_current_deployed_panel
    :field mode_1: payload.full_beacon_page_number.page_number.mode_1
    :field mode_2: payload.full_beacon_page_number.page_number.mode_2
    :field mode_entry_time: payload.full_beacon_page_number.page_number.mode_entry_time
    :field dgps_relative_vector_x: payload.full_beacon_page_number.page_number.dgps_relative_vector_x
    :field dgps_relative_vector_y: payload.full_beacon_page_number.page_number.dgps_relative_vector_y
    :field dgps_relative_vector_z: payload.full_beacon_page_number.page_number.dgps_relative_vector_z
    :field raf_relative_vector_x: payload.full_beacon_page_number.page_number.raf_relative_vector_x
    :field raf_relative_vector_y: payload.full_beacon_page_number.page_number.raf_relative_vector_y
    :field raf_relative_vector_z: payload.full_beacon_page_number.page_number.raf_relative_vector_z
    :field rtk_relative_vector_x: payload.full_beacon_page_number.page_number.rtk_relative_vector_x
    :field rtk_relative_vector_y: payload.full_beacon_page_number.page_number.rtk_relative_vector_y
    :field rtk_relative_vector_z: payload.full_beacon_page_number.page_number.rtk_relative_vector_z
    :field id2: payload.full_beacon_page_number.page_number.id2
    :field page_type: payload.full_beacon_page_number.page_number.page_type
    
    :field page_active_bitmask: payload.full_beacon_page_number.page_number.page_active_bitmask
    :field star_tracker_q1: payload.full_beacon_page_number.page_number.star_tracker_q1
    :field star_tracker_q2: payload.full_beacon_page_number.page_number.star_tracker_q2
    :field star_tracker_q3: payload.full_beacon_page_number.page_number.star_tracker_q3
    :field gyroscope_x: payload.full_beacon_page_number.page_number.gyroscope_x
    :field gyroscope_y: payload.full_beacon_page_number.page_number.gyroscope_y
    :field gyroscope_z: payload.full_beacon_page_number.page_number.gyroscope_z
    :field magnetometer_x: payload.full_beacon_page_number.page_number.magnetometer_x
    :field magnetometer_y: payload.full_beacon_page_number.page_number.magnetometer_y
    :field magnetometer_z: payload.full_beacon_page_number.page_number.magnetometer_z
    :field estimated_gyro_bias_roll: payload.full_beacon_page_number.page_number.estimated_gyro_bias_roll
    :field estimated_gyro_bias_pitch: payload.full_beacon_page_number.page_number.estimated_gyro_bias_pitch
    :field estimated_gyro_bias_yaw: payload.full_beacon_page_number.page_number.estimated_gyro_bias_yaw
    :field reaction_wheel_speed_x: payload.full_beacon_page_number.page_number.reaction_wheel_speed_x
    :field reaction_wheel_speed_y: payload.full_beacon_page_number.page_number.reaction_wheel_speed_y
    :field reaction_wheel_speed_z: payload.full_beacon_page_number.page_number.reaction_wheel_speed_z
    :field external_panel_plus_x: payload.full_beacon_page_number.page_number.external_panel_plus_x
    :field external_panel_plus_y: payload.full_beacon_page_number.page_number.external_panel_plus_y
    :field external_panel_minus_y: payload.full_beacon_page_number.page_number.external_panel_minus_y
    :field external_panel_plus_z: payload.full_beacon_page_number.page_number.external_panel_plus_z
    :field external_panel_minus_z: payload.full_beacon_page_number.page_number.external_panel_minus_z
    :field obc_main_1: payload.full_beacon_page_number.page_number.obc_main_1
    :field obc_main_2: payload.full_beacon_page_number.page_number.obc_main_2
    :field obc_sub_1: payload.full_beacon_page_number.page_number.obc_sub_1
    :field obc_sub_2: payload.full_beacon_page_number.page_number.obc_sub_2
    :field eps_board_1: payload.full_beacon_page_number.page_number.eps_board_1
    :field eps_board_2: payload.full_beacon_page_number.page_number.eps_board_2
    :field eps_board_3: payload.full_beacon_page_number.page_number.eps_board_3
    :field eps_board_4: payload.full_beacon_page_number.page_number.eps_board_4
    :field eps_battery_1: payload.full_beacon_page_number.page_number.eps_battery_1
    :field eps_battery_2: payload.full_beacon_page_number.page_number.eps_battery_2
    :field obc_gpio_1: payload.full_beacon_page_number.page_number.obc_gpio_1
    :field obc_gpio_2: payload.full_beacon_page_number.page_number.obc_gpio_2
    :field obc_pwm: payload.full_beacon_page_number.page_number.obc_pwm
    :field relnav_flag_1: payload.full_beacon_page_number.page_number.relnav_flag_1
    :field relnav_flag_2: payload.full_beacon_page_number.page_number.relnav_flag_2
    :field relnav_flag_3: payload.full_beacon_page_number.page_number.relnav_flag_3
    :field id2: payload.full_beacon_page_number.page_number.id2
    :field page_type: payload.full_beacon_page_number.page_number.page_type
    
    .. seealso::
       Source - https://gnss.snu.ac.kr/snuglite/251126/
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = Snuglite3.Ax25Frame(self._io, self, self._root)
        self.payload = Snuglite3.Payload(self._io, self, self._root)

    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = Snuglite3.Ax25Header(self._io, self, self._root)


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = Snuglite3.CallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = Snuglite3.SsidMask(self._io, self, self._root)
            self.src_callsign_raw = Snuglite3.CallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = Snuglite3.SsidMask(self._io, self, self._root)
            self.ctl = self._io.read_u1()
            self.pid = self._io.read_u1()


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")
            if not  ((self.callsign == u"DS0DH") or (self.callsign == u"DS0DH ") or (self.callsign == u"DS0DH0")) :
                raise kaitaistruct.ValidationNotAnyOfError(self.callsign, self._io, u"/types/callsign/seq/0")


    class Payload(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.csp_header_priority = self._io.read_bits_int_be(2)
            self.csp_header_source = self._io.read_bits_int_be(5)
            self.csp_header_destination = self._io.read_bits_int_be(5)
            self.csp_header_destination_port = self._io.read_bits_int_be(6)
            self.csp_header_source_port = self._io.read_bits_int_be(6)
            self.csp_header_reserved = self._io.read_bits_int_be(4)
            self.csp_header_flags = self._io.read_bits_int_be(4)
            self._io.align_to_byte()
            self.id1 = (self._io.read_bytes(7)).decode(u"UTF-8")
            if not self.id1 == u"SNUGL3>":
                raise kaitaistruct.ValidationNotEqualError(u"SNUGL3>", self.id1, self._io, u"/types/payload/seq/7")
            self.last_telecommand_number = self._io.read_u1()
            self.telecommand_counter = self._io.read_u1()
            self.time_year = self._io.read_u1()
            self.time_month = self._io.read_u1()
            self.time_day = self._io.read_u1()
            self.time_hour = self._io.read_u1()
            self.time_minute = self._io.read_u1()
            self.time_second = self._io.read_u1()
            self.gpstime_itow = self._io.read_s4be()
            self.gpstime_ftow = self._io.read_s4be()
            self.position_flag = self._io.read_u1()
            self.position_x = self._io.read_s4be()
            self.position_y = self._io.read_s4be()
            self.position_z = self._io.read_s4be()
            self.velocity_x = self._io.read_s4be()
            self.velocity_y = self._io.read_s4be()
            self.velocity_z = self._io.read_s4be()
            self.battery_mode = self._io.read_u1()
            self.battery_voltage = self._io.read_u2be()
            self.target_altitude_q1 = self._io.read_s2be()
            self.target_altitude_q2 = self._io.read_s2be()
            self.target_altitude_q3 = self._io.read_s2be()
            self.estimated_altitude_q1 = self._io.read_s2be()
            self.estimated_altitude_q2 = self._io.read_s2be()
            self.estimated_altitude_q3 = self._io.read_s2be()
            self.estimated_angular_rate_roll = self._io.read_f4be()
            self.estimated_angular_rate_pitch = self._io.read_f4be()
            self.estimated_angular_rate_yaw = self._io.read_f4be()
            self.sun_measurement_x = self._io.read_s2be()
            self.sun_measurement_y = self._io.read_s2be()
            self.sun_measurement_z = self._io.read_s2be()
            self.relnav_mode = self._io.read_u1()
            self.ocs_mode = self._io.read_u1()
            self.ocs_mode_sate = self._io.read_u1()
            self.target_relative_distance = self._io.read_s2be()
            self.current_relative_vector_x = self._io.read_f4be()
            self.current_relative_vector_y = self._io.read_f4be()
            self.current_relative_vector_z = self._io.read_f4be()
            self.current_relative_velocity_x = self._io.read_f4be()
            self.current_relative_velocity_y = self._io.read_f4be()
            self.current_relative_velocity_z = self._io.read_f4be()
            self.operational_mode = self._io.read_bits_int_le(3)
            self.skipping_rest_2 = self._io.read_bits_int_be(5)
            self._io.align_to_byte()
            self.deploy_flag = self._io.read_u1()
            self.full_beacon_page_number = Snuglite3.FullBeaconPageNumberT(self._io, self, self._root)

        @property
        def month(self):
            """only for calculation, do not display."""
            if hasattr(self, '_m_month'):
                return self._m_month

            self._m_month = (u"0" + str(self.time_month) if len(str(self.time_month)) == 1 else str(self.time_month))
            return getattr(self, '_m_month', None)

        @property
        def minute(self):
            """only for calculation, do not display."""
            if hasattr(self, '_m_minute'):
                return self._m_minute

            self._m_minute = (u"0" + str(self.time_minute) if len(str(self.time_minute)) == 1 else str(self.time_minute))
            return getattr(self, '_m_minute', None)

        @property
        def satellite_time(self):
            if hasattr(self, '_m_satellite_time'):
                return self._m_satellite_time

            self._m_satellite_time = u"20" + self.year + u"-" + self.month + u"-" + self.day + u"T" + self.hour + u":" + self.minute + u":" + self.second + u"Z"
            return getattr(self, '_m_satellite_time', None)

        @property
        def year(self):
            """only for calculation, do not display."""
            if hasattr(self, '_m_year'):
                return self._m_year

            self._m_year = (u"0" + str(self.time_year) if len(str(self.time_year)) == 1 else str(self.time_year))
            return getattr(self, '_m_year', None)

        @property
        def second(self):
            """only for calculation, do not display."""
            if hasattr(self, '_m_second'):
                return self._m_second

            self._m_second = (u"0" + str(self.time_second) if len(str(self.time_second)) == 1 else str(self.time_second))
            return getattr(self, '_m_second', None)

        @property
        def day(self):
            """only for calculation, do not display."""
            if hasattr(self, '_m_day'):
                return self._m_day

            self._m_day = (u"0" + str(self.time_day) if len(str(self.time_day)) == 1 else str(self.time_day))
            return getattr(self, '_m_day', None)

        @property
        def hour(self):
            """only for calculation, do not display."""
            if hasattr(self, '_m_hour'):
                return self._m_hour

            self._m_hour = (u"0" + str(self.time_hour) if len(str(self.time_hour)) == 1 else str(self.time_hour))
            return getattr(self, '_m_hour', None)


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

            self._m_ssid = ((self.ssid_mask & 31) >> 1)
            return getattr(self, '_m_ssid', None)


    class Page1(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.page_active_bitmask = self._io.read_bits_int_le(4)
            self.skipping_rest_0 = self._io.read_bits_int_be(2)
            self._io.align_to_byte()
            self.battery_current = self._io.read_u2be()
            self.power_switch_status_gps_0 = self._io.read_bits_int_le(1) != 0
            self.power_switch_status_gps_1 = self._io.read_bits_int_le(1) != 0
            self.power_switch_status_gps_2 = self._io.read_bits_int_le(1) != 0
            self.power_switch_status_deploy = self._io.read_bits_int_le(1) != 0
            self.power_switch_status_sub_trx = self._io.read_bits_int_le(1) != 0
            self.power_switch_status_main_trx = self._io.read_bits_int_le(1) != 0
            self.skipping_rest_1 = self._io.read_bits_int_be(2)
            self._io.align_to_byte()
            self.power_switch_current_1 = self._io.read_u2be()
            self.power_switch_current_2 = self._io.read_u2be()
            self.power_switch_current_3 = self._io.read_u2be()
            self.power_switch_current_4 = self._io.read_u2be()
            self.power_switch_current_5 = self._io.read_u2be()
            self.power_switch_current_6 = self._io.read_u2be()
            self.solar_panel_input_voltage_z = self._io.read_u2be()
            self.solar_panel_input_voltage_y = self._io.read_u2be()
            self.solar_panel_input_voltage_deployed_panel = self._io.read_u2be()
            self.solar_panel_input_current_z = self._io.read_u2be()
            self.solar_panel_input_current_y = self._io.read_u2be()
            self.solar_panel_input_current_deployed_panel = self._io.read_u2be()
            self.mode_1 = self._io.read_u1()
            self.mode_2 = self._io.read_u1()
            self.mode_entry_time = self._io.read_u4be()
            self.dgps_relative_vector_x = self._io.read_f4be()
            self.dgps_relative_vector_y = self._io.read_f4be()
            self.dgps_relative_vector_z = self._io.read_f4be()
            self.raf_relative_vector_x = self._io.read_f4be()
            self.raf_relative_vector_y = self._io.read_f4be()
            self.raf_relative_vector_z = self._io.read_f4be()
            self.rtk_relative_vector_x = self._io.read_f4be()
            self.rtk_relative_vector_y = self._io.read_f4be()
            self.rtk_relative_vector_z = self._io.read_f4be()
            self.id2 = (self._io.read_bytes(5)).decode(u"UTF-8")
            if not  ((self.id2 == u"<HANA") or (self.id2 == u"<DURI")) :
                raise kaitaistruct.ValidationNotAnyOfError(self.id2, self._io, u"/types/page1/seq/34")
            self.skipping_last_byte = self._io.read_u1()

        @property
        def page_type(self):
            if hasattr(self, '_m_page_type'):
                return self._m_page_type

            self._m_page_type = (u"1" if 0 == 0 else u"1")
            return getattr(self, '_m_page_type', None)


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
            self.callsign_ror = Snuglite3.Callsign(_io__raw_callsign_ror, self, self._root)


    class Page2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.page_active_bitmask = self._io.read_bits_int_le(4)
            self.skipping_rest = self._io.read_bits_int_be(2)
            self._io.align_to_byte()
            self.star_tracker_q1 = self._io.read_s2be()
            self.star_tracker_q2 = self._io.read_s2be()
            self.star_tracker_q3 = self._io.read_s2be()
            self.gyroscope_x = self._io.read_f4be()
            self.gyroscope_y = self._io.read_f4be()
            self.gyroscope_z = self._io.read_f4be()
            self.magnetometer_x = self._io.read_f4be()
            self.magnetometer_y = self._io.read_f4be()
            self.magnetometer_z = self._io.read_f4be()
            self.estimated_gyro_bias_roll = self._io.read_f4be()
            self.estimated_gyro_bias_pitch = self._io.read_f4be()
            self.estimated_gyro_bias_yaw = self._io.read_f4be()
            self.reaction_wheel_speed_x = self._io.read_s2be()
            self.reaction_wheel_speed_y = self._io.read_s2be()
            self.reaction_wheel_speed_z = self._io.read_s2be()
            self.external_panel_plus_x = self._io.read_u1()
            self.external_panel_plus_y = self._io.read_u1()
            self.external_panel_minus_y = self._io.read_u1()
            self.external_panel_plus_z = self._io.read_u1()
            self.external_panel_minus_z = self._io.read_u1()
            self.obc_main_1 = self._io.read_u1()
            self.obc_main_2 = self._io.read_u1()
            self.obc_sub_1 = self._io.read_u1()
            self.obc_sub_2 = self._io.read_u1()
            self.eps_board_1 = self._io.read_u1()
            self.eps_board_2 = self._io.read_u1()
            self.eps_board_3 = self._io.read_u1()
            self.eps_board_4 = self._io.read_u1()
            self.eps_battery_1 = self._io.read_u1()
            self.eps_battery_2 = self._io.read_u1()
            self.obc_gpio_1 = self._io.read_u1()
            self.obc_gpio_2 = self._io.read_u1()
            self.obc_pwm = self._io.read_u1()
            self.relnav_flag_1 = self._io.read_u1()
            self.relnav_flag_2 = self._io.read_u1()
            self.relnav_flag_3 = self._io.read_u1()
            self.id2 = (self._io.read_bytes(5)).decode(u"UTF-8")
            if not  ((self.id2 == u"<HANA") or (self.id2 == u"<DURI")) :
                raise kaitaistruct.ValidationNotAnyOfError(self.id2, self._io, u"/types/page2/seq/38")
            self.skipping_last_byte = self._io.read_u1()

        @property
        def page_type(self):
            if hasattr(self, '_m_page_type'):
                return self._m_page_type

            self._m_page_type = (u"2" if 0 == 0 else u"2")
            return getattr(self, '_m_page_type', None)


    class FullBeaconPageNumberT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self.check
            if _on == 0:
                self.page_number = Snuglite3.Page1(self._io, self, self._root)
            elif _on == 1:
                self.page_number = Snuglite3.Page2(self._io, self, self._root)

        @property
        def check(self):
            if hasattr(self, '_m_check'):
                return self._m_check

            self._m_check = self._io.read_bits_int_le(2)
            return getattr(self, '_m_check', None)



