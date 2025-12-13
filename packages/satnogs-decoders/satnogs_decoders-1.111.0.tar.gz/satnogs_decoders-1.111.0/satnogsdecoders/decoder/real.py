# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Real(KaitaiStruct):
    """:field callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field ssid_mask: ax25_frame.ax25_header.dest_ssid_raw.ssid_mask
    :field ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field src_callsign_raw_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field src_ssid_raw_ssid_mask: ax25_frame.ax25_header.src_ssid_raw.ssid_mask
    :field src_ssid_raw_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field ctl: ax25_frame.ax25_header.ctl
    :field ccsds_header_first: ax25_frame.ccsds_header.ccsds_header_first
    :field length: ax25_frame.ccsds_header.length
    :field ccsds_header_second: ax25_frame.ccsds_header.ccsds_header_second
    :field service_type: ax25_frame.real_header.service_type
    :field service_sub_type: ax25_frame.real_header.service_sub_type
    :field structure_id: ax25_frame.real_header.structure_id
    :field syncword: ax25_frame.real_header.syncword.syncword
    :field bat_charging_status: ax25_frame.payload.bat_charging_status
    :field v5_bat_current: ax25_frame.payload.v5_bat_current
    :field v3_3_bat_current: ax25_frame.payload.v3_3_bat_current
    :field vbat_bat_current: ax25_frame.payload.vbat_bat_current
    :field v3_3_bat_voltage: ax25_frame.payload.v3_3_bat_voltage
    :field v5_bat_voltage: ax25_frame.payload.v5_bat_voltage
    :field vbat_bat_voltage: ax25_frame.payload.vbat_bat_voltage
    :field bat_board_temperature: ax25_frame.payload.bat_board_temperature
    :field bat_cell_1_temperature: ax25_frame.payload.bat_cell_1_temperature
    :field bat_cell_2_temperature: ax25_frame.payload.bat_cell_2_temperature
    :field bat_cell_3_temperature: ax25_frame.payload.bat_cell_3_temperature
    :field bat_cell_4_temperature: ax25_frame.payload.bat_cell_4_temperature
    :field battery_heater_status_0: ax25_frame.payload.battery_heater_status_0
    :field battery_heater_status_1: ax25_frame.payload.battery_heater_status_1
    :field battery_heater_status_2: ax25_frame.payload.battery_heater_status_2
    :field battery_heater_status_3: ax25_frame.payload.battery_heater_status_3
    :field vbat_eps_voltage: ax25_frame.payload.vbat_eps_voltage
    :field v3_3_eps_voltage: ax25_frame.payload.v3_3_eps_voltage
    :field v5_eps_voltage: ax25_frame.payload.v5_eps_voltage
    :field v12_eps_voltage: ax25_frame.payload.v12_eps_voltage
    :field vbat_eps_current: ax25_frame.payload.vbat_eps_current
    :field v3_3_eps_current: ax25_frame.payload.v3_3_eps_current
    :field v5_eps_current: ax25_frame.payload.v5_eps_current
    :field v12_eps_current: ax25_frame.payload.v12_eps_current
    :field sw1_unused_voltage: ax25_frame.payload.sw1_unused_voltage
    :field sw2_unused_voltage: ax25_frame.payload.sw2_unused_voltage
    :field sw3_instrument_voltage: ax25_frame.payload.sw3_instrument_voltage
    :field sw4_li2_voltage: ax25_frame.payload.sw4_li2_voltage
    :field sw5_uhf_temp_sensor_voltage: ax25_frame.payload.sw5_uhf_temp_sensor_voltage
    :field sw6_unused_voltage: ax25_frame.payload.sw6_unused_voltage
    :field sw7_unused_voltage: ax25_frame.payload.sw7_unused_voltage
    :field sw8_xact_serial_voltage: ax25_frame.payload.sw8_xact_serial_voltage
    :field sw9_gps_voltage: ax25_frame.payload.sw9_gps_voltage
    :field sw10_instrument_lvds_voltage: ax25_frame.payload.sw10_instrument_lvds_voltage
    :field sw1_unused_current: ax25_frame.payload.sw1_unused_current
    :field sw2_unused_current: ax25_frame.payload.sw2_unused_current
    :field sw3_instrument_current: ax25_frame.payload.sw3_instrument_current
    :field sw4_li2_current: ax25_frame.payload.sw4_li2_current
    :field sw5_uhf_temp_sensor_current: ax25_frame.payload.sw5_uhf_temp_sensor_current
    :field sw6_unused_current: ax25_frame.payload.sw6_unused_current
    :field sw7_unused_current: ax25_frame.payload.sw7_unused_current
    :field sw8_xact_serial_current: ax25_frame.payload.sw8_xact_serial_current
    :field sw9_gps_current: ax25_frame.payload.sw9_gps_current
    :field sw10_instrument_lvds_current: ax25_frame.payload.sw10_instrument_lvds_current
    :field eps_mb_temperature: ax25_frame.payload.eps_mb_temperature
    :field eps_db_temperature: ax25_frame.payload.eps_db_temperature
    :field sa1_salw_inner_voltage: ax25_frame.payload.sa1_salw_inner_voltage
    :field sa2_salw_outer_voltage: ax25_frame.payload.sa2_salw_outer_voltage
    :field sa4_sarw_inner_voltage: ax25_frame.payload.sa4_sarw_inner_voltage
    :field sa5_sarw_outer_voltage: ax25_frame.payload.sa5_sarw_outer_voltage
    :field sa1_salw_inner_current: ax25_frame.payload.sa1_salw_inner_current
    :field sa2_salw_outer_current: ax25_frame.payload.sa2_salw_outer_current
    :field sa4_sarw_inner_current: ax25_frame.payload.sa4_sarw_inner_current
    :field sa5_sarw_outer_current: ax25_frame.payload.sa5_sarw_outer_current
    :field sa1_salw_inner_temperature: ax25_frame.payload.sa1_salw_inner_temperature
    :field sa2_salw_outer_temperature: ax25_frame.payload.sa2_salw_outer_temperature
    :field sa4_sarw_inner_temperature: ax25_frame.payload.sa4_sarw_inner_temperature
    :field sa5_sarw_outer_temperature: ax25_frame.payload.sa5_sarw_outer_temperature
    :field curr_boot_image: ax25_frame.payload.curr_boot_image
    :field image_valid: ax25_frame.payload.image_valid
    :field image_priority_0: ax25_frame.payload.image_priority_0
    :field image_priority_1: ax25_frame.payload.image_priority_1
    :field image_priority_2: ax25_frame.payload.image_priority_2
    :field image_is_stable: ax25_frame.payload.image_is_stable
    :field adc_enable: ax25_frame.payload.adc_enable
    :field last_reset_cause: ax25_frame.payload.last_reset_cause
    :field last_boot_count: ax25_frame.payload.last_boot_count
    :field version: ax25_frame.payload.version
    :field interface_baud_rate: ax25_frame.payload.interface_baud_rate
    :field rx_rf_baud_rate: ax25_frame.payload.rx_rf_baud_rate
    :field rx_modulation: ax25_frame.payload.rx_modulation
    :field rx_frequency: ax25_frame.payload.rx_frequency
    :field tx_power_amp_level: ax25_frame.payload.tx_power_amp_level
    :field tx_rf_baud_rate: ax25_frame.payload.tx_rf_baud_rate
    :field tx_modulation: ax25_frame.payload.tx_modulation
    :field tx_frequency: ax25_frame.payload.tx_frequency
    :field source_callsign_byte_0: ax25_frame.payload.source_callsign_byte_0
    :field source_callsign_byte_1: ax25_frame.payload.source_callsign_byte_1
    :field source_callsign_byte_2: ax25_frame.payload.source_callsign_byte_2
    :field source_callsign_byte_3: ax25_frame.payload.source_callsign_byte_3
    :field source_callsign_byte_4: ax25_frame.payload.source_callsign_byte_4
    :field source_callsign_byte_5: ax25_frame.payload.source_callsign_byte_5
    :field destination_callsign_byte_0: ax25_frame.payload.destination_callsign_byte_0
    :field destination_callsign_byte_1: ax25_frame.payload.destination_callsign_byte_1
    :field destination_callsign_byte_2: ax25_frame.payload.destination_callsign_byte_2
    :field destination_callsign_byte_3: ax25_frame.payload.destination_callsign_byte_3
    :field destination_callsign_byte_4: ax25_frame.payload.destination_callsign_byte_4
    :field destination_callsign_byte_5: ax25_frame.payload.destination_callsign_byte_5
    :field rssi: ax25_frame.payload.rssi
    :field vbat_obc_voltage: ax25_frame.payload.vbat_obc_voltage
    :field vbat_obc_current: ax25_frame.payload.vbat_obc_current
    :field vbat_plat_voltage: ax25_frame.payload.vbat_plat_voltage
    :field v3_3_plat_voltage: ax25_frame.payload.v3_3_plat_voltage
    :field v1_2_obc_voltage: ax25_frame.payload.v1_2_obc_voltage
    :field obc_temperature_1: ax25_frame.payload.obc_temperature_1
    :field v3_3_obc_voltage: ax25_frame.payload.v3_3_obc_voltage
    :field v3_3_obc_current: ax25_frame.payload.v3_3_obc_current
    :field v3_3_memory_voltage: ax25_frame.payload.v3_3_memory_voltage
    :field v3_3_memory_current: ax25_frame.payload.v3_3_memory_current
    :field vbat_periph_current: ax25_frame.payload.vbat_periph_current
    :field v3_3_periph_current: ax25_frame.payload.v3_3_periph_current
    :field v2_5_periph_current: ax25_frame.payload.v2_5_periph_current
    :field obc_temperature_2: ax25_frame.payload.obc_temperature_2
    :field obc_temperature_3: ax25_frame.payload.obc_temperature_3
    :field v3_3_gps_voltage: ax25_frame.payload.v3_3_gps_voltage
    :field v3_3_gps_current: ax25_frame.payload.v3_3_gps_current
    :field v2_5_obc_voltage: ax25_frame.payload.v2_5_obc_voltage
    :field v2_5_periph_voltage: ax25_frame.payload.v2_5_periph_voltage
    :field vbat_periph_voltage: ax25_frame.payload.vbat_periph_voltage
    :field v3_3_periph_voltage: ax25_frame.payload.v3_3_periph_voltage
    :field system_mode: ax25_frame.payload.system_mode
    :field startup_mode: ax25_frame.payload.startup_mode
    :field pass_in_progress: ax25_frame.payload.pass_in_progress
    :field digital_bus_voltage: ax25_frame.payload.digital_bus_voltage
    :field wheel_bus_voltage: ax25_frame.payload.wheel_bus_voltage
    :field rod_bus_voltage: ax25_frame.payload.rod_bus_voltage
    :field wheel_1_speed: ax25_frame.payload.wheel_1_speed
    :field wheel_2_speed: ax25_frame.payload.wheel_2_speed
    :field wheel_3_speed: ax25_frame.payload.wheel_3_speed
    :field adcs_mode: ax25_frame.payload.adcs_mode
    :field wheel_1_current: ax25_frame.payload.wheel_1_current
    :field wheel_2_current: ax25_frame.payload.wheel_2_current
    :field wheel_3_current: ax25_frame.payload.wheel_3_current
    :field imu_temp: ax25_frame.payload.imu_temp
    :field wheel_1_temperature: ax25_frame.payload.wheel_1_temperature
    :field wheel_2_temperature: ax25_frame.payload.wheel_2_temperature
    :field wheel_3_temperature: ax25_frame.payload.wheel_3_temperature
    :field crc: ax25_frame.payload.crc
    :field last_uptime: ax25_frame.payload.last_uptime
    :field time_fine_seconds: ax25_frame.payload.time_fine_seconds
    :field time_fine_fractional_seconds: ax25_frame.payload.time_fine_fractional_seconds
    :field time_onboard: ax25_frame.payload.time_onboard
    :field uptime: ax25_frame.payload.uptime
    :field mode_checkpoint_time: ax25_frame.payload.mode_checkpoint_time
    :field gps_time: ax25_frame.payload.gps_time
    :field tai_seconds: ax25_frame.payload.tai_seconds
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = Real.Ax25Frame(self._io, self, self._root)

    class HealthBeacon(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.bat_charging_status = self._io.read_bits_int_be(1) != 0
            self.v5_bat_current = self._io.read_bits_int_be(10)
            self.v3_3_bat_current = self._io.read_bits_int_be(10)
            self.vbat_bat_current = self._io.read_bits_int_be(10)
            self.v3_3_bat_voltage = self._io.read_bits_int_be(10)
            self.v5_bat_voltage = self._io.read_bits_int_be(10)
            self.vbat_bat_voltage = self._io.read_bits_int_be(10)
            self.bat_board_temperature = self._io.read_bits_int_be(10)
            self.bat_cell_1_temperature = self._io.read_bits_int_be(10)
            self.bat_cell_2_temperature = self._io.read_bits_int_be(10)
            self.bat_cell_3_temperature = self._io.read_bits_int_be(10)
            self.bat_cell_4_temperature = self._io.read_bits_int_be(10)
            self.battery_heater_status_0 = self._io.read_bits_int_be(10)
            self.battery_heater_status_1 = self._io.read_bits_int_be(10)
            self.battery_heater_status_2 = self._io.read_bits_int_be(10)
            self.battery_heater_status_3 = self._io.read_bits_int_be(10)
            self.vbat_eps_voltage = self._io.read_bits_int_be(10)
            self.v3_3_eps_voltage = self._io.read_bits_int_be(10)
            self.v5_eps_voltage = self._io.read_bits_int_be(10)
            self.v12_eps_voltage = self._io.read_bits_int_be(10)
            self.vbat_eps_current = self._io.read_bits_int_be(10)
            self.v3_3_eps_current = self._io.read_bits_int_be(10)
            self.v5_eps_current = self._io.read_bits_int_be(10)
            self.v12_eps_current = self._io.read_bits_int_be(10)
            self.sw1_unused_voltage = self._io.read_bits_int_be(10)
            self.sw2_unused_voltage = self._io.read_bits_int_be(10)
            self.sw3_instrument_voltage = self._io.read_bits_int_be(10)
            self.sw4_li2_voltage = self._io.read_bits_int_be(10)
            self.sw5_uhf_temp_sensor_voltage = self._io.read_bits_int_be(10)
            self.sw6_unused_voltage = self._io.read_bits_int_be(10)
            self.sw7_unused_voltage = self._io.read_bits_int_be(10)
            self.sw8_xact_serial_voltage = self._io.read_bits_int_be(10)
            self.sw9_gps_voltage = self._io.read_bits_int_be(10)
            self.sw10_instrument_lvds_voltage = self._io.read_bits_int_be(10)
            self.sw1_unused_current = self._io.read_bits_int_be(10)
            self.sw2_unused_current = self._io.read_bits_int_be(10)
            self.sw3_instrument_current = self._io.read_bits_int_be(10)
            self.sw4_li2_current = self._io.read_bits_int_be(10)
            self.sw5_uhf_temp_sensor_current = self._io.read_bits_int_be(10)
            self.sw6_unused_current = self._io.read_bits_int_be(10)
            self.sw7_unused_current = self._io.read_bits_int_be(10)
            self.sw8_xact_serial_current = self._io.read_bits_int_be(10)
            self.sw9_gps_current = self._io.read_bits_int_be(10)
            self.sw10_instrument_lvds_current = self._io.read_bits_int_be(10)
            self.eps_mb_temperature = self._io.read_bits_int_be(10)
            self.eps_db_temperature = self._io.read_bits_int_be(10)
            self.sa1_salw_inner_voltage = self._io.read_bits_int_be(10)
            self.sa2_salw_outer_voltage = self._io.read_bits_int_be(10)
            self.sa4_sarw_inner_voltage = self._io.read_bits_int_be(10)
            self.sa5_sarw_outer_voltage = self._io.read_bits_int_be(10)
            self.sa1_salw_inner_current = self._io.read_bits_int_be(10)
            self.sa2_salw_outer_current = self._io.read_bits_int_be(10)
            self.sa4_sarw_inner_current = self._io.read_bits_int_be(10)
            self.sa5_sarw_outer_current = self._io.read_bits_int_be(10)
            self.sa1_salw_inner_temperature = self._io.read_bits_int_be(10)
            self.sa2_salw_outer_temperature = self._io.read_bits_int_be(10)
            self.sa4_sarw_inner_temperature = self._io.read_bits_int_be(10)
            self.sa5_sarw_outer_temperature = self._io.read_bits_int_be(10)
            self.curr_boot_image = self._io.read_bits_int_be(8)
            self.image_valid = self._io.read_bits_int_be(3)
            self.image_priority_0 = self._io.read_bits_int_be(32)
            self.image_priority_1 = self._io.read_bits_int_be(32)
            self.image_priority_2 = self._io.read_bits_int_be(32)
            self.image_is_stable = self._io.read_bits_int_be(3)
            self.adc_enable = self._io.read_bits_int_be(1) != 0
            self.last_reset_cause = self._io.read_bits_int_be(2)
            self.last_boot_count = self._io.read_bits_int_be(32)
            self.version = self._io.read_bits_int_be(32)
            self.interface_baud_rate = self._io.read_bits_int_be(3)
            self.rx_rf_baud_rate = self._io.read_bits_int_be(2)
            self.rx_modulation = self._io.read_bits_int_be(2)
            self.rx_frequency = self._io.read_bits_int_be(32)
            self.tx_power_amp_level = self._io.read_bits_int_be(8)
            self.tx_rf_baud_rate = self._io.read_bits_int_be(2)
            self.tx_modulation = self._io.read_bits_int_be(2)
            self.tx_frequency = self._io.read_bits_int_be(32)
            self.source_callsign_byte_0 = self._io.read_bits_int_be(8)
            self.source_callsign_byte_1 = self._io.read_bits_int_be(8)
            self.source_callsign_byte_2 = self._io.read_bits_int_be(8)
            self.source_callsign_byte_3 = self._io.read_bits_int_be(8)
            self.source_callsign_byte_4 = self._io.read_bits_int_be(8)
            self.source_callsign_byte_5 = self._io.read_bits_int_be(8)
            self.destination_callsign_byte_0 = self._io.read_bits_int_be(8)
            self.destination_callsign_byte_1 = self._io.read_bits_int_be(8)
            self.destination_callsign_byte_2 = self._io.read_bits_int_be(8)
            self.destination_callsign_byte_3 = self._io.read_bits_int_be(8)
            self.destination_callsign_byte_4 = self._io.read_bits_int_be(8)
            self.destination_callsign_byte_5 = self._io.read_bits_int_be(8)
            self.rssi = self._io.read_bits_int_be(8)
            self.vbat_obc_voltage = self._io.read_bits_int_be(12)
            self.vbat_obc_current = self._io.read_bits_int_be(12)
            self.vbat_plat_voltage = self._io.read_bits_int_be(12)
            self.unused_a = self._io.read_bits_int_be(12)
            self.v3_3_plat_voltage = self._io.read_bits_int_be(12)
            self.v1_2_obc_voltage = self._io.read_bits_int_be(12)
            self.unused_b = self._io.read_bits_int_be(12)
            self.obc_temperature_1 = self._io.read_bits_int_be(12)
            self.v3_3_obc_voltage = self._io.read_bits_int_be(12)
            self.v3_3_obc_current = self._io.read_bits_int_be(12)
            self.v3_3_memory_voltage = self._io.read_bits_int_be(12)
            self.v3_3_memory_current = self._io.read_bits_int_be(12)
            self.vbat_periph_current = self._io.read_bits_int_be(12)
            self.v3_3_periph_current = self._io.read_bits_int_be(12)
            self.v2_5_periph_current = self._io.read_bits_int_be(12)
            self.obc_temperature_2 = self._io.read_bits_int_be(12)
            self.obc_temperature_3 = self._io.read_bits_int_be(12)
            self.v3_3_gps_voltage = self._io.read_bits_int_be(12)
            self.v3_3_gps_current = self._io.read_bits_int_be(12)
            self.v2_5_obc_voltage = self._io.read_bits_int_be(12)
            self.v2_5_periph_voltage = self._io.read_bits_int_be(12)
            self.vbat_periph_voltage = self._io.read_bits_int_be(12)
            self.v3_3_periph_voltage = self._io.read_bits_int_be(12)
            self.unused_c = self._io.read_bits_int_be(12)
            self.system_mode = self._io.read_bits_int_be(3)
            self.startup_mode = self._io.read_bits_int_be(3)
            self.pass_in_progress = self._io.read_bits_int_be(1) != 0
            self.digital_bus_voltage = self._io.read_bits_int_be(16)
            self.wheel_bus_voltage = self._io.read_bits_int_be(16)
            self.rod_bus_voltage = self._io.read_bits_int_be(16)
            self.wheel_1_speed = self._io.read_bits_int_be(16)
            self.wheel_2_speed = self._io.read_bits_int_be(16)
            self.wheel_3_speed = self._io.read_bits_int_be(16)
            self.adcs_mode = self._io.read_bits_int_be(8)
            self.wheel_1_current = self._io.read_bits_int_be(16)
            self.wheel_2_current = self._io.read_bits_int_be(16)
            self.wheel_3_current = self._io.read_bits_int_be(16)
            self.imu_temp = self._io.read_bits_int_be(16)
            self.wheel_1_temperature = self._io.read_bits_int_be(16)
            self.wheel_2_temperature = self._io.read_bits_int_be(16)
            self.wheel_3_temperature = self._io.read_bits_int_be(16)
            self.unused_j = self._io.read_bits_int_be(16)
            self.crc = self._io.read_bits_int_be(16)


    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = Real.Ax25Header(self._io, self, self._root)
            self.ccsds_header = Real.CcsdsHeader(self._io, self, self._root)
            self.real_header = Real.RealHeader(self._io, self, self._root)
            _on = self.ccsds_header.length
            if _on == 192:
                self.payload = Real.HealthBeacon(self._io, self, self._root)
            elif _on == 45:
                self.payload = Real.TimeBeacon(self._io, self, self._root)


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = Real.CallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = Real.SsidMask(self._io, self, self._root)
            self.src_callsign_raw = Real.CallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = Real.SsidMask(self._io, self, self._root)
            self.ctl = self._io.read_u2be()


    class CcsdsHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ccsds_header_first = self._io.read_u4be()
            self.length = self._io.read_u2be()
            self.ccsds_header_second = self._io.read_u1()


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")
            if not self.callsign == u"WR9XTX":
                raise kaitaistruct.ValidationNotEqualError(u"WR9XTX", self.callsign, self._io, u"/types/callsign/seq/0")


    class RealSyncword(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.syncword = (self._io.read_bytes(4)).decode(u"ASCII")
            if not self.syncword == u"REAL":
                raise kaitaistruct.ValidationNotEqualError(u"REAL", self.syncword, self._io, u"/types/real_syncword/seq/0")


    class RealHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.service_type = self._io.read_u1()
            self.service_sub_type = self._io.read_u1()
            self.structure_id = self._io.read_u1()
            self.syncword = Real.RealSyncword(self._io, self, self._root)


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


    class TimeBeacon(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.last_uptime = self._io.read_u4be()
            self.time_fine_seconds = self._io.read_u4be()
            self.time_fine_fractional_seconds = self._io.read_u4be()
            self.time_onboard = self._io.read_u4be()
            self.uptime = self._io.read_u4be()
            self.mode_checkpoint_time = self._io.read_u4be()
            self.gps_time = self._io.read_u4be()
            self.tai_seconds = self._io.read_f8be()
            self.crc = self._io.read_bits_int_be(16)


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
            self.callsign_ror = Real.Callsign(_io__raw_callsign_ror, self, self._root)



