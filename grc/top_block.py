#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Dec 22 01:16:10 2017
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import cc1111
import math
import osmosdr
import time


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1024000
        self.decimation = decimation = 10
        self.symbol_rate = symbol_rate = 38400
        self.input_rate = input_rate = samp_rate/decimation
        self.window_symbols = window_symbols = 1
        self.symbol_taps_length = symbol_taps_length = int((float(input_rate)/ symbol_rate))
        self.samples_per_symbol = samples_per_symbol = float(input_rate) / symbol_rate
        self.grab_freq = grab_freq = 868200000
        self.symbol_taps = symbol_taps = (1,) * symbol_taps_length
        self.offset_sign2 = offset_sign2 = (-34780*grab_freq)/868200000
        self.offset_sign1 = offset_sign1 = (11600*grab_freq)/868200000
        self.gain_mu = gain_mu = 0.4 / samples_per_symbol
        self.average_window = average_window = int((input_rate* window_symbols / symbol_rate))

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(868283000, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.digital_correlate_access_code_bb_0 = digital.correlate_access_code_bb('11010011100100011101001110010001', 1)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(samples_per_symbol, 0.25*gain_mu*gain_mu, 0.5, gain_mu, 0.02)
        self.digital_binary_slicer_fb_0_0 = digital.binary_slicer_fb()
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, '/home/fraschi/packet.data', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(40, 1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)
        self.FXFIR1 = filter.freq_xlating_fir_filter_ccc(decimation, (1, ), -14e3, samp_rate)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.FXFIR1, 0), (self.analog_simple_squelch_cc_0, 0))    
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0_0, 0), (self.digital_correlate_access_code_bb_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0_0, 0))    
        self.connect((self.digital_correlate_access_code_bb_0, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.FXFIR1, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.set_input_rate(self.samp_rate/self.decimation)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_input_rate(self.samp_rate/self.decimation)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_samples_per_symbol(float(self.input_rate) / self.symbol_rate)
        self.set_symbol_taps_length(int((float(self.input_rate)/ self.symbol_rate)))
        self.set_average_window(int((self.input_rate* self.window_symbols / self.symbol_rate)))

    def get_input_rate(self):
        return self.input_rate

    def set_input_rate(self, input_rate):
        self.input_rate = input_rate
        self.set_samples_per_symbol(float(self.input_rate) / self.symbol_rate)
        self.set_symbol_taps_length(int((float(self.input_rate)/ self.symbol_rate)))
        self.set_average_window(int((self.input_rate* self.window_symbols / self.symbol_rate)))

    def get_window_symbols(self):
        return self.window_symbols

    def set_window_symbols(self, window_symbols):
        self.window_symbols = window_symbols
        self.set_average_window(int((self.input_rate* self.window_symbols / self.symbol_rate)))

    def get_symbol_taps_length(self):
        return self.symbol_taps_length

    def set_symbol_taps_length(self, symbol_taps_length):
        self.symbol_taps_length = symbol_taps_length
        self.set_symbol_taps((1,) * self.symbol_taps_length)

    def get_samples_per_symbol(self):
        return self.samples_per_symbol

    def set_samples_per_symbol(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol
        self.set_gain_mu(0.4 / self.samples_per_symbol)
        self.digital_clock_recovery_mm_xx_0.set_omega(self.samples_per_symbol)

    def get_grab_freq(self):
        return self.grab_freq

    def set_grab_freq(self, grab_freq):
        self.grab_freq = grab_freq
        self.set_offset_sign2((-34780*self.grab_freq)/868200000)
        self.set_offset_sign1((11600*self.grab_freq)/868200000)

    def get_symbol_taps(self):
        return self.symbol_taps

    def set_symbol_taps(self, symbol_taps):
        self.symbol_taps = symbol_taps

    def get_offset_sign2(self):
        return self.offset_sign2

    def set_offset_sign2(self, offset_sign2):
        self.offset_sign2 = offset_sign2

    def get_offset_sign1(self):
        return self.offset_sign1

    def set_offset_sign1(self, offset_sign1):
        self.offset_sign1 = offset_sign1

    def get_gain_mu(self):
        return self.gain_mu

    def set_gain_mu(self, gain_mu):
        self.gain_mu = gain_mu
        self.digital_clock_recovery_mm_xx_0.set_gain_omega(0.25*self.gain_mu*self.gain_mu)
        self.digital_clock_recovery_mm_xx_0.set_gain_mu(self.gain_mu)

    def get_average_window(self):
        return self.average_window

    def set_average_window(self, average_window):
        self.average_window = average_window


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
