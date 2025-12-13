# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Cevrosat(KaitaiStruct):
    """:field uptime_total: id_one.type_check.uptime_total
    :field uptime_since_last: id_one.type_check.uptime_since_last
    :field reset_count: id_one.type_check.reset_count
    :field mcu_10mv: id_one.type_check.mcu_10mv
    :field batt: id_one.type_check.batt
    :field temp_cpu: id_one.type_check.temp_cpu
    :field temp_pa_ntc: id_one.type_check.temp_pa_ntc
    :field sig_rx_immediate: id_one.type_check.sig_rx_immediate
    :field sig_rx_avg: id_one.type_check.sig_rx_avg
    :field sig_rx_max: id_one.type_check.sig_rx_max
    :field sig_background_avg: id_one.type_check.sig_background_avg
    :field sig_background_immediate: id_one.type_check.sig_background_immediate
    :field sig_background_max: id_one.type_check.sig_background_max
    :field rf_packets_received: id_one.type_check.rf_packets_received
    :field rf_packets_transmitted: id_one.type_check.rf_packets_transmitted
    :field ax25_packets_received: id_one.type_check.ax25_packets_received
    :field ax25_packets_transmitted: id_one.type_check.ax25_packets_transmitted
    :field digipeater_rx_count: id_one.type_check.digipeater_rx_count
    :field digipeater_tx_count: id_one.type_check.digipeater_tx_count
    :field csp_received: id_one.type_check.csp_received
    :field csp_transmitted: id_one.type_check.csp_transmitted
    :field i2c1_received: id_one.type_check.i2c1_received
    :field i2c1_transmitted: id_one.type_check.i2c1_transmitted
    :field i2c2_received: id_one.type_check.i2c2_received
    :field i2c2_transmitted: id_one.type_check.i2c2_transmitted
    :field rs485_received: id_one.type_check.rs485_received
    :field rs485_transmitted: id_one.type_check.rs485_transmitted
    :field csp_mcu_received: id_one.type_check.csp_mcu_received
    :field csp_mcu_transmitted: id_one.type_check.csp_mcu_transmitted
    :field a: id_one.type_check.a
    :field tx1_telemetry: id_one.type_check.tx1_telemetry
    :field src_callsign: id_one.type_check.ax25_frame.ax25_header.dnxd_src_callsign_raw.callsign_ror.callsign
    :field src_ssid: id_one.type_check.ax25_frame.ax25_header.dnxd_src_ssid_raw.ssid
    :field dest_callsign: id_one.type_check.ax25_frame.ax25_header.dnxd_dest_callsign_raw.callsign_ror.callsign
    :field dest_ssid: id_one.type_check.ax25_frame.ax25_header.dnxd_dest_ssid_raw.ssid
    :field dnxd_message: id_one.type_check.ax25_frame.dnxd_message
    :field src_callsign: id_one.type_check.digi_ax25_frame.digi_ax25_header.digi_src_callsign_raw.callsign_ror.callsign
    :field src_ssid: id_one.type_check.digi_ax25_frame.digi_ax25_header.digi_src_ssid_raw.ssid
    :field dest_callsign: id_one.type_check.digi_ax25_frame.digi_ax25_header.digi_dest_callsign_raw.callsign_ror.callsign
    :field dest_ssid: id_one.type_check.digi_ax25_frame.digi_ax25_header.digi_dest_ssid_raw.ssid
    :field rpt_instance_callsign: id_one.type_check.digi_ax25_frame.digi_ax25_header.repeater.rpt_instance.rpt_callsign_raw.callsign_ror.callsign
    :field rpt_instance_ssid: id_one.type_check.digi_ax25_frame.digi_ax25_header.repeater.rpt_instance.rpt_ssid_raw.ssid
    :field digi_message: id_one.type_check.digi_ax25_frame.digi_message
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.id_one = Cevrosat.IdOneType(self._io, self, self._root)

    class IdOneType(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            _on = self.check
            if _on == 2259461217:
                self.type_check = Cevrosat.Tx1(self._io, self, self._root)
            elif _on == 2259461233:
                self.type_check = Cevrosat.Dnxd(self._io, self, self._root)
            else:
                self.type_check = Cevrosat.Digi(self._io, self, self._root)

        @property
        def check(self):
            if hasattr(self, '_m_check'):
                return self._m_check

            _pos = self._io.pos()
            self._io.seek(10)
            self._m_check = self._io.read_u4be()
            self._io.seek(_pos)
            return getattr(self, '_m_check', None)


    class Tx1(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.skip_ax25_header_1 = self._io.read_u8be()
            if not self.skip_ax25_header_1 == 9701387192009547934:
                raise kaitaistruct.ValidationNotEqualError(9701387192009547934, self.skip_ax25_header_1, self._io, u"/types/tx_1/seq/0")
            self.skip_ax25_header_2 = self._io.read_u8be()
            if not self.skip_ax25_header_2 == 10835808779503731696:
                raise kaitaistruct.ValidationNotEqualError(10835808779503731696, self.skip_ax25_header_2, self._io, u"/types/tx_1/seq/1")
            self.first_comma = self._io.read_u1()
            if not self.first_comma == 44:
                raise kaitaistruct.ValidationNotEqualError(44, self.first_comma, self._io, u"/types/tx_1/seq/2")
            self.tx_1 = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.tx_1 == u"TX-1":
                raise kaitaistruct.ValidationNotEqualError(u"TX-1", self.tx_1, self._io, u"/types/tx_1/seq/3")
            self.pass_uptime = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_uptime == u"U":
                raise kaitaistruct.ValidationNotEqualError(u"U", self.pass_uptime, self._io, u"/types/tx_1/seq/4")
            self.uptime_total_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uptime_since_last_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_resets = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_resets == u"R":
                raise kaitaistruct.ValidationNotEqualError(u"R", self.pass_resets, self._io, u"/types/tx_1/seq/7")
            self.reset_count_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_mcuv = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_mcuv == u"V":
                raise kaitaistruct.ValidationNotEqualError(u"V", self.pass_mcuv, self._io, u"/types/tx_1/seq/9")
            self.mcu_10mv_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_battv = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_battv == u"Ve":
                raise kaitaistruct.ValidationNotEqualError(u"Ve", self.pass_battv, self._io, u"/types/tx_1/seq/11")
            self.batt_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_temp = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_temp == u"T":
                raise kaitaistruct.ValidationNotEqualError(u"T", self.pass_temp, self._io, u"/types/tx_1/seq/13")
            self.temp_cpu_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.temp_pa_ntc_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_sig = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_sig == u"Sig":
                raise kaitaistruct.ValidationNotEqualError(u"Sig", self.pass_sig, self._io, u"/types/tx_1/seq/16")
            self.sig_rx_immediate_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sig_rx_avg_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sig_rx_max_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sig_background_immediate_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sig_background_avg_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sig_background_max_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_rf = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_rf == u"RX":
                raise kaitaistruct.ValidationNotEqualError(u"RX", self.pass_rf, self._io, u"/types/tx_1/seq/23")
            self.rf_packets_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.rf_packets_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_ax25 = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_ax25 == u"Ax":
                raise kaitaistruct.ValidationNotEqualError(u"Ax", self.pass_ax25, self._io, u"/types/tx_1/seq/26")
            self.ax25_packets_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.ax25_packets_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_digi = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_digi == u"Digi":
                raise kaitaistruct.ValidationNotEqualError(u"Digi", self.pass_digi, self._io, u"/types/tx_1/seq/29")
            self.digipeater_rx_count_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.digipeater_tx_count_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_csp = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_csp == u"CSP":
                raise kaitaistruct.ValidationNotEqualError(u"CSP", self.pass_csp, self._io, u"/types/tx_1/seq/32")
            self.csp_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.csp_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_i2c1 = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_i2c1 == u"I2C1":
                raise kaitaistruct.ValidationNotEqualError(u"I2C1", self.pass_i2c1, self._io, u"/types/tx_1/seq/35")
            self.i2c1_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.i2c1_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_i2c2 = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_i2c2 == u"I2C2":
                raise kaitaistruct.ValidationNotEqualError(u"I2C2", self.pass_i2c2, self._io, u"/types/tx_1/seq/38")
            self.i2c2_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.i2c2_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_rs485 = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_rs485 == u"RS485":
                raise kaitaistruct.ValidationNotEqualError(u"RS485", self.pass_rs485, self._io, u"/types/tx_1/seq/41")
            self.rs485_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.rs485_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_csp_mcu = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_csp_mcu == u"MCU":
                raise kaitaistruct.ValidationNotEqualError(u"MCU", self.pass_csp_mcu, self._io, u"/types/tx_1/seq/44")
            self.csp_mcu_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.csp_mcu_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_a = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            if not self.pass_a == u"A":
                raise kaitaistruct.ValidationNotEqualError(u"A", self.pass_a, self._io, u"/types/tx_1/seq/47")
            self.a_raw = (self._io.read_bytes_full()).decode(u"utf8")

        @property
        def sig_rx_max(self):
            if hasattr(self, '_m_sig_rx_max'):
                return self._m_sig_rx_max

            self._m_sig_rx_max = int(self.sig_rx_max_raw)
            return getattr(self, '_m_sig_rx_max', None)

        @property
        def temp_pa_ntc(self):
            if hasattr(self, '_m_temp_pa_ntc'):
                return self._m_temp_pa_ntc

            self._m_temp_pa_ntc = int(self.temp_pa_ntc_raw)
            return getattr(self, '_m_temp_pa_ntc', None)

        @property
        def csp_transmitted(self):
            if hasattr(self, '_m_csp_transmitted'):
                return self._m_csp_transmitted

            self._m_csp_transmitted = int(self.csp_transmitted_raw)
            return getattr(self, '_m_csp_transmitted', None)

        @property
        def batt(self):
            if hasattr(self, '_m_batt'):
                return self._m_batt

            self._m_batt = int(self.batt_raw)
            return getattr(self, '_m_batt', None)

        @property
        def sig_rx_avg(self):
            if hasattr(self, '_m_sig_rx_avg'):
                return self._m_sig_rx_avg

            self._m_sig_rx_avg = int(self.sig_rx_avg_raw)
            return getattr(self, '_m_sig_rx_avg', None)

        @property
        def sig_background_immediate(self):
            if hasattr(self, '_m_sig_background_immediate'):
                return self._m_sig_background_immediate

            self._m_sig_background_immediate = int(self.sig_background_immediate_raw)
            return getattr(self, '_m_sig_background_immediate', None)

        @property
        def uptime_total(self):
            if hasattr(self, '_m_uptime_total'):
                return self._m_uptime_total

            self._m_uptime_total = int(self.uptime_total_raw)
            return getattr(self, '_m_uptime_total', None)

        @property
        def rs485_received(self):
            if hasattr(self, '_m_rs485_received'):
                return self._m_rs485_received

            self._m_rs485_received = int(self.rs485_received_raw)
            return getattr(self, '_m_rs485_received', None)

        @property
        def i2c1_received(self):
            if hasattr(self, '_m_i2c1_received'):
                return self._m_i2c1_received

            self._m_i2c1_received = int(self.i2c1_received_raw)
            return getattr(self, '_m_i2c1_received', None)

        @property
        def a(self):
            if hasattr(self, '_m_a'):
                return self._m_a

            self._m_a = int(self.a_raw)
            return getattr(self, '_m_a', None)

        @property
        def temp_cpu(self):
            if hasattr(self, '_m_temp_cpu'):
                return self._m_temp_cpu

            self._m_temp_cpu = int(self.temp_cpu_raw)
            return getattr(self, '_m_temp_cpu', None)

        @property
        def ax25_packets_transmitted(self):
            if hasattr(self, '_m_ax25_packets_transmitted'):
                return self._m_ax25_packets_transmitted

            self._m_ax25_packets_transmitted = int(self.ax25_packets_transmitted_raw)
            return getattr(self, '_m_ax25_packets_transmitted', None)

        @property
        def ax25_packets_received(self):
            if hasattr(self, '_m_ax25_packets_received'):
                return self._m_ax25_packets_received

            self._m_ax25_packets_received = int(self.ax25_packets_received_raw)
            return getattr(self, '_m_ax25_packets_received', None)

        @property
        def digipeater_tx_count(self):
            if hasattr(self, '_m_digipeater_tx_count'):
                return self._m_digipeater_tx_count

            self._m_digipeater_tx_count = int(self.digipeater_tx_count_raw)
            return getattr(self, '_m_digipeater_tx_count', None)

        @property
        def csp_mcu_transmitted(self):
            if hasattr(self, '_m_csp_mcu_transmitted'):
                return self._m_csp_mcu_transmitted

            self._m_csp_mcu_transmitted = int(self.csp_mcu_transmitted_raw)
            return getattr(self, '_m_csp_mcu_transmitted', None)

        @property
        def tx1_telemetry(self):
            if hasattr(self, '_m_tx1_telemetry'):
                return self._m_tx1_telemetry

            self._m_tx1_telemetry = u",TX-1,U," + self.uptime_total_raw + u"," + self.uptime_since_last_raw + u",R," + self.reset_count_raw + u",V," + self.mcu_10mv_raw + u",Ve," + self.batt_raw + u",T," + self.temp_cpu_raw + u"," + self.temp_pa_ntc_raw + u",Sig," + self.sig_rx_immediate_raw + u"," + self.sig_rx_avg_raw + u"," + self.sig_rx_max_raw + u"," + self.sig_background_immediate_raw + u"," + self.sig_background_avg_raw + u"," + self.sig_background_max_raw + u",RX," + self.rf_packets_received_raw + u"," + self.rf_packets_transmitted_raw + u",Ax," + self.ax25_packets_received_raw + u"," + self.ax25_packets_transmitted_raw + u",Digi," + self.digipeater_rx_count_raw + u"," + self.digipeater_tx_count_raw + u",CSP," + self.csp_received_raw + u"," + self.csp_transmitted_raw + u",I2C1," + self.i2c1_received_raw + u"," + self.i2c1_transmitted_raw + u",I2C2," + self.i2c2_received_raw + u"," + self.i2c2_received_raw + u",RS485," + self.rs485_received_raw + u"," + self.rs485_transmitted_raw + u",MCU," + self.csp_mcu_received_raw + u"," + self.csp_mcu_transmitted_raw + u",A," + self.a_raw
            return getattr(self, '_m_tx1_telemetry', None)

        @property
        def csp_mcu_received(self):
            if hasattr(self, '_m_csp_mcu_received'):
                return self._m_csp_mcu_received

            self._m_csp_mcu_received = int(self.csp_mcu_received_raw)
            return getattr(self, '_m_csp_mcu_received', None)

        @property
        def i2c1_transmitted(self):
            if hasattr(self, '_m_i2c1_transmitted'):
                return self._m_i2c1_transmitted

            self._m_i2c1_transmitted = int(self.i2c1_transmitted_raw)
            return getattr(self, '_m_i2c1_transmitted', None)

        @property
        def mcu_10mv(self):
            if hasattr(self, '_m_mcu_10mv'):
                return self._m_mcu_10mv

            self._m_mcu_10mv = int(self.mcu_10mv_raw)
            return getattr(self, '_m_mcu_10mv', None)

        @property
        def uptime_since_last(self):
            if hasattr(self, '_m_uptime_since_last'):
                return self._m_uptime_since_last

            self._m_uptime_since_last = int(self.uptime_since_last_raw)
            return getattr(self, '_m_uptime_since_last', None)

        @property
        def sig_background_max(self):
            if hasattr(self, '_m_sig_background_max'):
                return self._m_sig_background_max

            self._m_sig_background_max = int(self.sig_background_max_raw)
            return getattr(self, '_m_sig_background_max', None)

        @property
        def sig_rx_immediate(self):
            if hasattr(self, '_m_sig_rx_immediate'):
                return self._m_sig_rx_immediate

            self._m_sig_rx_immediate = int(self.sig_rx_immediate_raw)
            return getattr(self, '_m_sig_rx_immediate', None)

        @property
        def reset_count(self):
            if hasattr(self, '_m_reset_count'):
                return self._m_reset_count

            self._m_reset_count = int(self.reset_count_raw)
            return getattr(self, '_m_reset_count', None)

        @property
        def rs485_transmitted(self):
            if hasattr(self, '_m_rs485_transmitted'):
                return self._m_rs485_transmitted

            self._m_rs485_transmitted = int(self.rs485_transmitted_raw)
            return getattr(self, '_m_rs485_transmitted', None)

        @property
        def rf_packets_received(self):
            if hasattr(self, '_m_rf_packets_received'):
                return self._m_rf_packets_received

            self._m_rf_packets_received = int(self.rf_packets_received_raw)
            return getattr(self, '_m_rf_packets_received', None)

        @property
        def rf_packets_transmitted(self):
            if hasattr(self, '_m_rf_packets_transmitted'):
                return self._m_rf_packets_transmitted

            self._m_rf_packets_transmitted = int(self.rf_packets_transmitted_raw)
            return getattr(self, '_m_rf_packets_transmitted', None)

        @property
        def digipeater_rx_count(self):
            if hasattr(self, '_m_digipeater_rx_count'):
                return self._m_digipeater_rx_count

            self._m_digipeater_rx_count = int(self.digipeater_rx_count_raw)
            return getattr(self, '_m_digipeater_rx_count', None)

        @property
        def sig_background_avg(self):
            if hasattr(self, '_m_sig_background_avg'):
                return self._m_sig_background_avg

            self._m_sig_background_avg = int(self.sig_background_avg_raw)
            return getattr(self, '_m_sig_background_avg', None)

        @property
        def i2c2_received(self):
            if hasattr(self, '_m_i2c2_received'):
                return self._m_i2c2_received

            self._m_i2c2_received = int(self.i2c2_received_raw)
            return getattr(self, '_m_i2c2_received', None)

        @property
        def i2c2_transmitted(self):
            if hasattr(self, '_m_i2c2_transmitted'):
                return self._m_i2c2_transmitted

            self._m_i2c2_transmitted = int(self.i2c2_transmitted_raw)
            return getattr(self, '_m_i2c2_transmitted', None)

        @property
        def csp_received(self):
            if hasattr(self, '_m_csp_received'):
                return self._m_csp_received

            self._m_csp_received = int(self.csp_received_raw)
            return getattr(self, '_m_csp_received', None)


    class Dnxd(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_frame = Cevrosat.Dnxd.Ax25Frame(self._io, self, self._root)

        class Ax25Frame(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.ax25_header = Cevrosat.Dnxd.Ax25Header(self._io, self, self._root)
                self.dnxd_message = (self._io.read_bytes_full()).decode(u"utf-8")


        class Ax25Header(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.dnxd_dest_callsign_raw = Cevrosat.Dnxd.CallsignRaw(self._io, self, self._root)
                self.dnxd_dest_ssid_raw = Cevrosat.Dnxd.SsidMask(self._io, self, self._root)
                self.dnxd_src_callsign_raw = Cevrosat.Dnxd.CallsignRaw(self._io, self, self._root)
                if self.dnxd_src_callsign_raw.callsign_ror.callsign == u"OK0CVR":
                    self.dnxd_src_ssid_raw = Cevrosat.Dnxd.SsidMask(self._io, self, self._root)

                if self.dnxd_src_ssid_raw.ssid == 8:
                    self.ctl_pid = self._io.read_u2be()



        class Callsign(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


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
                self.callsign_ror = Cevrosat.Dnxd.Callsign(_io__raw_callsign_ror, self, self._root)



    class Digi(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.digi_ax25_frame = Cevrosat.Digi.Ax25Frame(self._io, self, self._root)

        class Ax25Frame(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.digi_ax25_header = Cevrosat.Digi.Ax25Header(self._io, self, self._root)
                self.digi_message = (self._io.read_bytes_full()).decode(u"utf-8")


        class Ax25Header(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.digi_dest_callsign_raw = Cevrosat.Digi.CallsignRaw(self._io, self, self._root)
                self.digi_dest_ssid_raw = Cevrosat.Digi.SsidMask(self._io, self, self._root)
                self.digi_src_callsign_raw = Cevrosat.Digi.CallsignRaw(self._io, self, self._root)
                self.digi_src_ssid_raw = Cevrosat.Digi.SsidMask(self._io, self, self._root)
                if (self.digi_src_ssid_raw.ssid_mask & 1) == 0:
                    self.repeater = Cevrosat.Digi.Repeater(self._io, self, self._root)

                if self.repeater.rpt_instance.rpt_callsign_raw.callsign_ror.callsign == u"OK0CVR":
                    self.ctl = self._io.read_u1()

                if  ((self.repeater.rpt_instance.rpt_ssid_raw.ssid == 7) or (self.repeater.rpt_instance.rpt_ssid_raw.ssid == 8)) :
                    self.pid = self._io.read_u1()



        class Callsign(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


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


        class Repeaters(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.rpt_callsign_raw = Cevrosat.Digi.CallsignRaw(self._io, self, self._root)
                self.rpt_ssid_raw = Cevrosat.Digi.SsidMask(self._io, self, self._root)


        class Repeater(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.rpt_instance = Cevrosat.Digi.Repeaters(self._io, self, self._root)


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
                self.callsign_ror = Cevrosat.Digi.Callsign(_io__raw_callsign_ror, self, self._root)




