from .Motor import *
NO_SCALING = 1.0
CNTS_REV_MIS = 409600
MISRegisterName = Literal[
    "FDBUS_baud",
    "FDBUS_node_id",
    "a_soll",
    "abs_enc_pos",
    "acc_1",
    "acc_2",
    "acc_3",
    "acc_4",
    "acc_emerg",
    "accept_count",
    "accept_voltage",
    "actual_torque",
    "afzup_c_max",
    "afzup_c_min",
    "afzup_filter",
    "afzup_max_s",
    "afzup_r_idx",
    "afzup_w_bits",
    "ana_inp_1",
    "ana_inp_2",
    "ana_inp_3",
    "ana_inp_4",
    "ana_inp_5",
    "ana_inp_6",
    "ana_inp_7",
    "ana_inp_8",
    "anafilt_1",
    "anafilt_2",
    "anafilt_3",
    "anafilt_4",
    "anafilt_5",
    "anafilt_6",
    "anafilt_7",
    "anafilt_8",
    "available_io",
    "baud_rate",
    "baud_rate_uart4",
    "bootloader_ver",
    "bus_vol",
    "capcom0",
    "capcom1",
    "capcom2",
    "capcom3",
    "capcom4",
    "capcom5",
    "capcom6",
    "capcom7",
    "checksum_1",
    "checksum_2",
    "cl_catch_up",
    "cntrl_bits",
    "command",
    "control_voltage",
    "cur_scale_dec",
    "cur_scale_fac",
    "cur_scale_inc",
    "cur_scale_max",
    "cur_scale_min",
    "current_1",
    "current_2",
    "current_3",
    "current_4",
    "d_soll",
    "dmx_setup_1",
    "dmx_setup_10",
    "dmx_setup_11",
    "dmx_setup_12",
    "dmx_setup_2",
    "dmx_setup_3",
    "dmx_setup_4",
    "dmx_setup_5",
    "dmx_setup_6",
    "dmx_setup_7",
    "dmx_setup_8",
    "dmx_setup_9",
    "dummy",
    "enc_setup",
    "enc_type",
    "encoder_Pos",
    "encoder_Pos+",
    "error_bits",
    "error_mask",
    "ex_crc_err",
    "ex_cyc_setup",
    "ext_break_bit",
    "ext_enc",
    "ext_enc_decoded",
    "ext_enc_pos",
    "filter_status",
    "flex_led_set_1",
    "flex_led_set_2",
    "flex_reg",
    "flex_reg_set_1",
    "flex_reg_set_2",
    "flex_reg_set_3",
    "flex_reg_set_4",
    "flex_reg_set_5",
    "flex_reg_set_6",
    "flex_reg_set_7",
    "flex_reg_set_8",
    "follow_err",
    "follow_err+",
    "follow_err_max",
    "follow_err_max+",
    "fw_build",
    "gear1",
    "gear2",
    "group_id",
    "group_seq",
    "h3_data0",
    "h3_data1",
    "h3_data2",
    "h3_data3",
    "home_mask",
    "home_mode",
    "hw_revision",
    "hw_setup",
    "in_pos_limit",
    "in_pos_retries",
    "in_target_time",
    "index_offset",
    "inp_filt_cnt",
    "inp_filt_mask",
    "inpos_mask",
    "inputs",
    "io_setup_bits",
    "kphase",
    "low_bus_cvi_cnt",
    "max_tt_count",
    "max_tt_count+",
    "max_v_and_i",
    "min_bus_vol",
    "min_tt_count",
    "min_tt_count+",
    "modbus_setup",
    "mode_reg",
    "module_type",
    "motor_addr",
    "motor_rev",
    "motor_type",
    "n_limit_mask",
    "not_saved",
    "options_bits",
    "outputs",
    "p_home",
    "p_ist",
    "p_ist+",
    "p_limit_mask",
    "p_new",
    "p_soll",
    "p_soll+",
    "pos_1",
    "pos_1+",
    "pos_2",
    "pos_2+",
    "pos_3",
    "pos_3+",
    "pos_4",
    "pos_4+",
    "pos_5",
    "pos_5+",
    "pos_6",
    "pos_6+",
    "pos_7",
    "pos_7+",
    "pos_8",
    "pos_8+",
    "prog_version",
    "rec_cnt",
    "run_current",
    "sample1",
    "sample2",
    "sample3",
    "sample4",
    "sample_cnt",
    "sample_control",
    "sample_reg_1",
    "sample_reg_2",
    "sample_reg_3",
    "sample_reg_4",
    "sample_time",
    "save_voltage",
    "serialnumber",
    "settle_time",
    "setup_bits",
    "shadow2_rd_addr",
    "shadow2_rd_data",
    "shadow_rd_addr",
    "shadow_wd_addr",
    "ssi_setup_1",
    "ssi_setup_2",
    "stall_thresh",
    "standby_current",
    "standby_time",
    "start_mode",
    "start_mode_val",
    "status_bits",
    "t_home",
    "temp",
    "temp_highres",
    "temp_limits",
    "ticks",
    "turntable_mode",
    "turntable_rev",
    "turntable_size",
    "tx_delay",
    "tx_delay_uart4",
    "v_encoder",
    "v_encoder_settings",
    "v_ext_enc",
    "v_home",
    "v_home_crawl",
    "v_home_timeout",
    "v_ist",
    "v_ist_calc",
    "v_soll",
    "v_soll_auto",
    "v_start",
    "velocity_1",
    "velocity_2",
    "velocity_3",
    "velocity_4",
    "velocity_5",
    "velocity_6",
    "velocity_7",
    "velocity_8",
    "warning_bits",
    "z_search_bits",
]

class MISMotor(Motor):
    def __init__(self):
        super().__init__()
        #0: reg address, 1: scaling, 2: access (0: read, 1: write, 2: read and write)
        self.registers = {
    'dummy': [0, NO_SCALING,None],
    'prog_version': [1, NO_SCALING, 0],
    'mode_reg': [2, NO_SCALING, 2],
    'p_soll': [3, NO_SCALING, 2],
    'p_soll+': [4, NO_SCALING, 2],
    'v_soll': [5, 0.01, 2],
    'a_soll': [6, NO_SCALING, 2],
    'run_current': [7, [5.87e-3,3.91e-3,1.96e-3], 2],
    'standby_time': [8, NO_SCALING, 2],
    'standby_current': [9, NO_SCALING, 2],
    'p_ist': [10, NO_SCALING, 2],
    'p_ist+': [11, NO_SCALING, 2],
    'v_ist': [12, 0.01, 0],
    'v_start': [13, 0.01, 2],
    'gear1': [14, NO_SCALING, 2],
    'gear2': [15, NO_SCALING, 2],
    'encoder_Pos': [16, NO_SCALING, 2],
    'encoder_Pos+': [17, NO_SCALING, 2],
    'inputs': [18, NO_SCALING, 0],
    'outputs': [19, NO_SCALING, 2],
    'follow_err': [20, NO_SCALING, 0],
    'follow_err+': [21, NO_SCALING, 0],
    'follow_err_max': [22, NO_SCALING, 2],
    'follow_err_max+': [23, NO_SCALING, 2],
    'command': [24, NO_SCALING, 2],
    'status_bits': [25, NO_SCALING, 0],
    'temp': [26, 2.27, 0],
    'turntable_rev': [27, NO_SCALING, 2],
    'min_tt_count': [28, NO_SCALING, 2],
    'min_tt_count+': [29, NO_SCALING, 2],
    'max_tt_count': [30, NO_SCALING, 2],
    'max_tt_count+': [31, NO_SCALING, 2],
    'acc_emerg': [32, NO_SCALING, 2],
    'in_pos_limit': [33, NO_SCALING, 2],
    'in_pos_retries': [34, NO_SCALING, 2],
    'error_bits': [35, NO_SCALING, 2],
    'warning_bits': [36, NO_SCALING, 2],
    'start_mode': [37, NO_SCALING, 2],
    'start_mode_val': [37, NO_SCALING, 2],
    'p_home': [38, NO_SCALING, 2],
    'hw_setup': [39, NO_SCALING, 2],
    'v_home': [40, 0.01, 2],
    't_home': [41, NO_SCALING, 2],
    'home_mode': [42, NO_SCALING, 2],
    'abs_enc_pos': [46, NO_SCALING, 0],
    'ext_enc_pos': [47, NO_SCALING, 0],
    'flex_reg': [48, NO_SCALING, 0],
    'pos_1': [49, NO_SCALING, 2],
    'pos_1+': [50, NO_SCALING, 2],
    'pos_2': [51, NO_SCALING, 2],
    'pos_2+': [52, NO_SCALING, 2],
    'pos_3': [53, NO_SCALING, 2],
    'pos_3+': [54, NO_SCALING, 2],
    'pos_4': [55, NO_SCALING, 2],
    'pos_4+': [56, NO_SCALING, 2],
    'pos_5': [57, NO_SCALING, 2],
    'pos_5+': [58, NO_SCALING, 2],
    'pos_6': [59, NO_SCALING, 2],
    'pos_6+': [60, NO_SCALING, 2],
    'pos_7': [61, NO_SCALING, 2],
    'pos_7+': [62, NO_SCALING, 2],
    'pos_8': [63, NO_SCALING, 2],
    'pos_8+': [64, NO_SCALING, 2],
    'velocity_1': [65, 0.01, 2],
    'velocity_2': [66, 0.01, 2],
    'velocity_3': [67, 0.01, 2],
    'velocity_4': [68, 0.01, 2],
    'velocity_5': [69, 0.01, 2],
    'velocity_6': [70, 0.01, 2],
    'velocity_7': [71, 0.01, 2],
    'velocity_8': [72, 0.01, 2],
    'acc_1': [73, NO_SCALING, 2],
    'acc_2': [74, NO_SCALING, 2],
    'acc_3': [75, NO_SCALING, 2],
    'acc_4': [76, NO_SCALING, 2],
    'current_1': [77, 5.87e-3, 2],
    'current_2': [78, 5.87e-3, 2],
    'current_3': [79, 5.87e-3, 2],
    'current_4': [80, 5.87e-3, 2],
    'anafilt_1': [81, 1.221e-3, 0],
    'anafilt_2': [82, 1.221e-3, 0],
    'anafilt_3': [83, 1.221e-3, 0],
    'anafilt_4': [84, 1.221e-3, 0],
    'anafilt_5': [85, 1.221e-3, 0],
    'anafilt_6': [86, 1.221e-3, 0],
    'anafilt_7': [87, 1.221e-3, 0],
    'anafilt_8': [88, 1.221e-3, 0],
    'ana_inp_1': [89, 1.221e-3, 0],
    'ana_inp_2': [90, 1.221e-3, 0],
    'ana_inp_3': [91, 1.221e-3, 0],
    'ana_inp_4': [92, 1.221e-3, 0],
    'ana_inp_5': [93, 1.221e-3, 0],
    'ana_inp_6': [94, 1.221e-3, 0],
    'ana_inp_7': [95, 1.221e-3, 0],
    'ana_inp_8': [96, 1.221e-3, 0],
    'bus_vol': [97, 26.525e-3, 0],
    'min_bus_vol': [98, 26.525e-3, 2],
    'enc_type': [99, NO_SCALING, 0],
    'afzup_w_bits': [100, NO_SCALING, 2],
    'afzup_r_idx': [101, NO_SCALING, 2],
    'afzup_c_min': [102, 1.221e-3, 2],
    'afzup_c_max': [103, 1.221e-3, 2],
    'afzup_max_s': [104, 1.221e-3, 2],
    'afzup_filter': [105, NO_SCALING, 2],
    'filter_status': [106, NO_SCALING, 0],
    'ssi_setup_1': [107, NO_SCALING, 2],
    'settle_time': [110, NO_SCALING, 2],
    'ssi_setup_2': [111, NO_SCALING, 2],
    'sample_reg_1': [112, NO_SCALING, 2],
    'sample_reg_2': [113, NO_SCALING, 2],
    'sample_reg_3': [114, NO_SCALING, 2],
    'sample_reg_4': [115, NO_SCALING, 2],
    'sample_cnt': [116, NO_SCALING, 2],
    'sample_time': [117, NO_SCALING, 2],
    'sample_control': [118, NO_SCALING, 2],
    'index_offset': [120, NO_SCALING, 0],
    'modbus_setup': [121, NO_SCALING, 2],
    'z_search_bits': [122, NO_SCALING, 2],
    'setup_bits': [124, NO_SCALING, 2],
    'io_setup_bits': [125, NO_SCALING, 2],
    'turntable_mode': [126, NO_SCALING, 2],
    'turntable_size': [127, NO_SCALING, 2],
    'n_limit_mask': [129, NO_SCALING, 2],
    'p_limit_mask': [130, NO_SCALING, 2],
    'home_mask': [132, NO_SCALING, 2],
    'inp_filt_mask': [135, NO_SCALING, 2],
    'inp_filt_cnt': [136, NO_SCALING, 2],
    'inpos_mask': [137, NO_SCALING, 2],
    'error_mask': [138, NO_SCALING, 2],
    'accept_voltage': [139, 8.764e-3, 2],
    'accept_count': [140, NO_SCALING, 2],
    'save_voltage': [141, NO_SCALING, 2],
    'control_voltage': [143, 8.764e-3, 0],
    'p_new': [144, NO_SCALING, 2],
    'baud_rate': [146, NO_SCALING, 2],
    'tx_delay': [147, NO_SCALING, 2],
    'group_id': [148, NO_SCALING, 2],
    'group_seq': [149, NO_SCALING, 0],
    'motor_addr': [150, NO_SCALING, 2],
    'motor_type': [151, NO_SCALING, 0],
    'serialnumber': [152, NO_SCALING, 0],
    'checksum_1': [154, NO_SCALING, 0],
    'checksum_2': [155, NO_SCALING, 0],
    'hw_revision': [156, NO_SCALING, 0],
    'max_v_and_i': [157, NO_SCALING, 0],
    'available_io': [158, NO_SCALING, 0],
    'bootloader_ver': [159, NO_SCALING, 0],
    'not_saved': [160,NO_SCALING,2],
    'h3_data0' : [161,NO_SCALING,2],
    'h3_data1' : [162,NO_SCALING,2],
    'h3_data2' : [163,NO_SCALING,2],
    'h3_data3' : [164,NO_SCALING,2],
    'options_bits': [165, NO_SCALING, 0],
    'FDBUS_node_id': [166, NO_SCALING, 2],
    'FDBUS_baud': [167, NO_SCALING, 2],
    'module_type': [168, NO_SCALING, 0],
    'ext_enc': [170, NO_SCALING, 2],
    'ext_enc_decoded': [171, NO_SCALING, 2],
    'v_ext_enc': [172, NO_SCALING, 0],
    'stall_thresh': [173, NO_SCALING, 2],
    'd_soll': [174, NO_SCALING, 2],
    'enc_setup': [175, NO_SCALING, 2],
    'fw_build': [176, NO_SCALING, 0],
    'in_target_time': [177, NO_SCALING, 2],
    'ext_break_bit': [179, NO_SCALING, 2],
    'shadow2_rd_addr': [289, NO_SCALING, 2],
    'shadow2_rd_data': [290, NO_SCALING, 2],
    'ticks': [202, NO_SCALING, 2],
    'cur_scale_max': [212, NO_SCALING, 2],
    'cur_scale_min': [213, NO_SCALING, 2],
    'cur_scale_fac': [215, NO_SCALING, 2],
    'kphase': [216, NO_SCALING, 2],
    'actual_torque': [217, 100/2048, 0],
    'cur_scale_inc': [218, NO_SCALING, 2],
    'cur_scale_dec': [219, NO_SCALING, 2],
    'shadow_rd_addr': [220,NO_SCALING,0],
    'shadow_rd_addr': [221,NO_SCALING,0],
    'shadow_wd_addr': [222,NO_SCALING,1],
    'shadow_wd_addr': [223,NO_SCALING,1],
    'flex_reg_set_1': [224, NO_SCALING, 2],
    'flex_reg_set_2': [225, NO_SCALING, 2],
    'flex_reg_set_3': [226, NO_SCALING, 2],
    'flex_reg_set_4': [227, NO_SCALING, 2],
    'flex_reg_set_5': [228, NO_SCALING, 2],
    'flex_reg_set_6': [229, NO_SCALING, 2],
    'flex_reg_set_7': [230, NO_SCALING, 2],
    'flex_reg_set_8': [231, NO_SCALING, 2],
    'flex_led_set_1': [232, NO_SCALING, 2],
    'flex_led_set_2': [233, NO_SCALING, 2],
    'v_soll_auto': [236, NO_SCALING, 2],
    'v_ist_calc': [237, 0.01, 0],
    'motor_rev': [238, NO_SCALING, 0],
    'ex_cyc_setup': [239, NO_SCALING, 0],
    'ex_crc_err': [241, NO_SCALING, 0],
    'v_home_crawl': [242, NO_SCALING, 0.01],
    'v_home_timeout': [243, NO_SCALING, 2],
    'temp_limits': [244, NO_SCALING, 0],
    'cl_catch_up': [245, NO_SCALING, 2],
    'temp_highres': [246, 1/1000, 0],
    'low_bus_cvi_cnt': [252, NO_SCALING, 2],
    'v_encoder': [253, 0.01, 0],
    'v_encoder_settings': [254, NO_SCALING, 2],

    "sample1" : [256,NO_SCALING,2],
    "sample2" : [257,NO_SCALING,2],
    "sample3" : [258,NO_SCALING,2],
    "sample4" : [259,NO_SCALING,2],

    "rec_cnt" : [264,NO_SCALING,2],
    "cntrl_bits" : [265,NO_SCALING,2],
    "capcom0" : [266,NO_SCALING,2],
    "capcom1" : [267,NO_SCALING,2],
    "capcom2" : [268,NO_SCALING,2],
    "capcom3" : [269,NO_SCALING,2],
    "capcom4" : [270,NO_SCALING,2],
    "capcom5" : [271,NO_SCALING,2],
    "capcom6" : [272,NO_SCALING,2],
    "capcom7" : [273,NO_SCALING,2],

    "dmx_setup_1" : [274,NO_SCALING,2],
    "dmx_setup_2" : [275,NO_SCALING,2],
    "dmx_setup_3" : [276,NO_SCALING,2],
    "dmx_setup_4" : [277,NO_SCALING,2],
    "dmx_setup_5" : [278,NO_SCALING,2],
    "dmx_setup_6" : [279,NO_SCALING,2],
    "dmx_setup_7" : [280,NO_SCALING,2],
    "dmx_setup_8" : [281,NO_SCALING,2],
    "dmx_setup_9" : [282,NO_SCALING,2],
    "dmx_setup_10" : [283,NO_SCALING,2],
    "dmx_setup_11" : [284,NO_SCALING,2],
    "dmx_setup_12" : [285,NO_SCALING,2],

    "baud_rate_uart4": [286,NO_SCALING,2],
    "tx_delay_uart4" : [287,NO_SCALING,2],

    "shadow2_rd_addr" : [289,NO_SCALING,2],
    "shadow2_rd_data" : [290,NO_SCALING,2]
        }

        self.ctl_mode = {
            "passive": 0,
            "velocity": 1,
            "position": 2,
            "gear": 3,
            "gear_follow": 4,
            "stop": 5,
            "home_trq": 6,
            "home_1": 7,
            "home_2": 8,
            "safe": 9,
            "csp": 10,
            "set_default": 11
        }

        self.control_bits = {
    'stopped': 0,
    'direction': 1,
    'rel_pos': 2,
    'pos_mode': 3,
    'cl_enabled': 4,
    'passive': 5,
    'driver_pas': 6,
    'do_sync': 7,
    'gear_ena': 8,
    'bit9': 9,
    'standby': 10,
    'e_stop': 11,
    'bit12': 12,
    'slow_update': 13,
    'setup_update': 14,
    'bit15': 15,
    'output_act': 16,
    'safemode': 17,
    'hw_ver': (18,2),  # Note: 'hw_ver' covers indices 18-19
    'extenc_ena': 20,
    'bit21': 21,
    'enc_ena': 22,
    'bit23': 23,
    'bit24': 24,
    'dsp402_ena': 25,
    'homing_active': 26,
    'brake_ena': 27,
    'ten_ms_update': 28,
    'cvi_unstable': 29,
    'homing_timeout': 30,
    'ms_update': 31}
        
        self.status_bits = {
    # Byte 1
    'fpga_busy': 0,
    'auto_corr_active': 1,
    'in_phys_position': 2,
    'at_velocity': 3,
    'in_position': 4,
    'acc': 5,
    'dec': 6,
    'homing_done': 7,
    
    # Byte 2
    'passw_lock': 8,
    'mag_enc_error': 9,
    'msp430_cal_data_present': 10,
    'msp430_lin_data_present': 11,
    'error': 12,
    'msp430_cal_data_locked': 13,
    'brake_active': 14,
    'cl_lead_lag_detected': 15,
    
    # Byte 3
    'cl_active': 16,
    'cl_encoder_calibrated': 17,
    'standby': 18,
    'sto_enabled': 19,
    'encoder_mhm_ok': 20,
    'modbus_sync_enabled': 21,
    'at_target_pos': 22,
    'sto_sense_a': 23,
    
    # Byte 4
    'sto_sense_b': 24,
    'fram_size': (25,2),  # fram_size covers indices 25-26
    'ready': 27,
    'motor_homed_in_life_time': 28,
    'error_trigged': 29,
    'sto_alarm': 30,
    'initialized': 31}
        
        self.err_info = {
            "general":  0x0001,
            "follow": 0x0002,
            "output": 0x0004,
            "position": 0x0008,
            "lowbus": 0x0010,
            "overvoltage": 0x0020,
            "temperature": 0x0040,
            "internal": 0x0080,
            "enc_lost_pos": 0x0100,
            "enc_reed": 0x0200,
            "enc_com": 0x0400,
            "extenc2": 0x0800,
            "closed_loop": 0x1000
        }
        
        self.error_bits = { 
    'error': 0,
    'follow': 1,
    'io_driver': 2,
    'pos_limit': 3,
    'low_bus_v': 4,
    'high_bus_v': 5,
    'temperature': 6,
    'internal': 7,  # Changed 'Internal' to 'internal' to follow snake_case convention
    'ame_lostpos': 8,
    'ame_reed': 9,
    'ame_com': 10,
    'ssi': 11,
    'cl_err': 12,
    'memory': 13,
    'ase_cal': 14,
    'bit15': 15,
    'homing_timeout': 16,
    'cvi_unstable': 17,
    'overload': 18,  # Changed 'Overload' to 'overload' for consistency
    'ssi_encoder_speed_too_great': 19,
    'ssi_encoder_wrong_magnet_distance': 20,
    'slf_error': 21,  # Changed 'SlfError' to 'slf_error'
    'bit22': 22,
    'bit23': 23,
    'high_velocity': 24,
    'bit25': 25,
    'bit26': 26,
    'sto_alarm': 27,
    'dummy28': 28,
    'sto': 29,
    'dummy30': 30,
    'dummy31': 31}
        
        self.warning_info = {
            "pos_lim_act":  0x0001,
            "neg_lim_act":  0x0002,
            "pos_lim_hb_act":  0x0004,
            "neg_lim_hb_act": 0x0010,
            "dummy":  0x0020,
            "temperature":  0x0040,
            "ext_enc_2":  0x0080,
            "overload":  0x0100
        }
        
        self.warning_bits = {
    'pos_lim_act': 0,
    'neg_lim_act': 1,
    'pos_has_been': 2,
    'neg_has_been': 3,
    'low_bus': 4,
    'io_driver': 5,
    'temperature': 6,
    'ssi_encoder': 7,
    'overload': 8,  # Changed 'Overload' to 'overload' for consistency
    'sto': 9,
    'ssi_overflow': 10,
    'ssi_underflow': 11,
    'encoder_amplitude_clipping': 12,
    'unused': 13  # 'unused' covers indices 13-31
    }
        
        self.setup_bits = {
    'invert_dir': 0,                     # Inverse the motor direction.
    'prog_stop': 1,                      # Don't start ePLC program automatically when firmware starts.
    'extenc_mode': 2,                    # External encoder mode.
    'dsp402_en': 4,                      # Enable DSP402 mode.
    'enc_auto_sync': 5,                  # Encoder auto sync.
    'inphyspos_mode': 6,                 # If set, recalculate InPhysPos continuously. If 0, only after stop.
    'ssi_encoder_enabled': 7,            # SSI encoder enabled.

    'j1939_ena': 8,                      # Activate J1939 mode. (Disable CANopen)
    'psoll_sync_dis': 9,                 # Disables the P_SOLL sync in passive mode.
    'enc_to_p_ist': 10,                  # Automatically transfer the absolute encoder position to P_IST at power up.
    'multiturn': 11,                     # Automatically transfer the encoder-adjusted saved P_IST to actual P_IST at power up.
    'keep_ext_enc': 12,                  # Do not zero the external encoder count on startup (in CleanSetup()).
    'keep_ssi': 13,                      # Do not zero the SSI data register on startup (in CleanSetup()).
    'beckhoff_mode': 14,                 # Use the Beckhoff variant of CAN.
    'intenc_dis': 15,                    # Overrules the factory setting, useful for customers where the PCB is shipped with an encoder but isn't used in the application.

    'extenc_dir': 16,                    # Counting direction for the external encoder.
    'ignore_pos_limit_error': 17,        # If high, there will be no errors on position limits.
    'zup_mem_read_write': 18,            # Indirect addressing of all registers, including >255.
    'brake_disable': 19,                 # Temporarily disable the brake.
    'extenc_error_dis': 20,              # Disable errors from the SSI encoder.
    'lowbus_err': 21,                    # Set error in case of too low bus voltage ("under voltage").
    'lowbus_passive': 22,                # Go to passive mode in case of too low bus voltage ("under voltage").
    'lowbus_zero': 23,                   # Set V_SOLL=0 in case of too low bus voltage ("under voltage").

    'cl_enable': 24,                     # Enable the closed loop.
    'cl_cc_enable': 25,                  # Enable the current control (requires closed loop to be enabled).
    'multiturn_enc': 26,                 # Automatically transfer the encoder-adjusted saved encoder position to actual P_IST at power up.
    'cl_extenc': 27,                     # Enable closed loop with an external encoder.
    'pos_lim_simple': 28,                # Simple position limit.
    'sto_error': 29,                     # Set error bit 29 on STO.
    'sto_passive': 30,                   # Go to passive mode on STO.
    'sto_zero': 31                       # Set V_SOLL=0 on STO.
    }
        
        self.setup_bits_2 = {
    'slave_follow_slave': 0,          # SLF slave: 0 = None, 1 = Relative, 2 = Absolute.
    'slave_follow_master': 3,         # SLF master: 0 = None, 1 = Velocity master, 2 = Relative master position.
    'setup_bit6': 6,                  # Reserved.
    'setup_bit7': 7,                  # Reserved.

    'ext_enc_gearing': 8,             # Enable gearing of external encoder.
    'ext_enc_sync_enable': 9,         # Sync p_enc with p_axis.
    'stall_detection': 10,            # Enable stall detection. Stops motor when fwerr above error window.
    'stall_use_d_err': 11,            # Use d_error for stall deceleration.
    'console_on_usart1': 12,          # Enable console on USART1.
    'console_on_uart4': 13,           # Enable console on UART4.
    'ssi_dir_inverse': 14,            # Inverse the counting direction of the encoder.
    'units_mactalk': 15,              # Enable units for Mactalk.
    'units_modbus_slave': 16,         # Enable units for Modbus slave.
    'units_eplc': 17,                 # Enable unit for ePLC.
    'setup_bit18': 18,                # Reserved for units.
    'turntable_short_path': 19,       # Turntable. Use actual position reference for P_SOLL change.
    'setup_bit20': 20,                # Reserved.
    'setup_bit21': 21,                # Reserved.
    'setup_bit22': 22,                # Reserved.
    'setup_bit23': 23,                # Reserved.

    'setup_bit24': 24,                # Reserved.
    'setup_bit25': 25,                # Reserved.
    'setup_bit26': 26,                # Reserved.
    'setup_bit27': 27,                # Reserved.
    'setup_bit28': 28,                # Reserved.
    'setup_bit29': 29,                # Reserved.
    'setup_bit30': 30,                # Reserved.
    'setup_bit31': 31                 # Reserved.
    }
        
        self.slf_status_bits = {
    #Status bits
    'slaves_ready': 0,       # 0: Slave reported ready for running
    'slaves_homed': 1,       # 1: Slaves are all successfully homed
    'reserved_status': 2,    # 2-15: Reserved bits

    # Error bits
    'slave_passive': 17,      # 0: Slave went passive when active was expected
    'slave_offline': 18,      # 1: Slave went offline when active was expected
    'slave_f_error': 19,      # 2: Slave following error time exceeded
    'slave_can_error': 20,    # 3: Slave has a CAN error
    'reserved_error': 21,     # 4-15: Reserved bits
    }
        
        self.home_bits = {
    'use_index': 0,           # 0: After homing trigger point, move on to the next index position in the same direction.
    'bounce_on_limit': 1,     # 1: 
    'search_opposite': 2,     # 2: 
    'dummy_0': 3,             # 3: 
    'ignore_switch': 4,       # 4: Use the internal encoder for homing
    'no_time_out': 5,         # 5: Disable time out
    'dummy_1': 6,             # 6-12: Dummy bits
    'dummy_2': 13             # 13-15: Adjust to 32-bit struct size (16-bit dummy variable)
    }
        
        self.turntable_mode = {
    "mode": (0,8),                # 0-7: Turn table mode e.g. Singelturn CW
    "no_selection": 0,
    "singleturn_CW" : 1,
    "singleturn_CCW" : 2,
    "shortest_path" : 3,
    "multiturn_CW" : 4,
    "multiturn_CCW" : 5,
    "use_acc_pos": 8,         # 8: Use actual position instead of previous target position
    "unassigned": 9,          # 9-31: Unassigned
    }
        self.encoder_settings = {
    "filter_constant": (0,16),     # 0-15
    "use_Encoder_values": 16, # 16
    "unassigned": 17          # 17-31 : Unassigned          
    }
        self.modbus_setup = {
    'enabled_usart1': 0,          # 0: 0 = MacTalk protocol, 1 = Modbus protocol
    'type': 1,                    # 1: 0 = Uart1 RTU, 1 = ASCII
    'parity': 2,                  # 2-3: 0 = Uart1 None, 1 = Odd, 2 = Even
    'data_bits': 4,               # 4: 0 = Uart1 7 data bits, 1 = 8 data bits
    'stop_bits': 5,               # 5: 0 = Uart1 1 stop bit, 1 = 2 stop bits
    'dummy_1': 6,                 # 6-7: Not used
    'enabled_uart4': 8,           # 8: 1 = Enabled Modbus Uart4
    'ua4_type': 9,                # 9: Uart4 0 = RTU, 1 = ASCII
    'ua4_parity': (10,2),         # 10-11: Uart4 0 = None, 1 = Odd, 2 = Even
    'ua4_data_bits': 12,          # 12: Uart4 0 = 7 data bits, 1 = 8 data bits
    'ua4_stop_bits': 13,          # 13: Uart4 0 = 1 stop bit, 1 = 2 stop bits
    'dummy_2': 14                 # 14-15: Not used
    }
        self.ctl_setup_bits = {
    'enable': 0,                        # 0: Enable closed loop operation
    'data_latch': 1,                    # 1: Latch data in RAM
    'v_soll_zero': 2,                   # 2: Forces V_SOLL to 0
    'index_clr': 3,                     # 3: The index pulse is latched, but can be cleared
    'allow_enc_preset': 4,              # 4: Allows encoder position to be preset
    'disable_linearization': 5,         # 5: Disables linearization
    'dummy0': 6,                        # 6-9: Not used
    'load_enc_start_pos_scaled': 10,    # 10: Load scaled absolute encoder position
    'ext_encoder': 11,                  # 11: Use external encoder instead of internal
    'soft_gen_index_pulse': 12,         # 12: Emulates an index pulse
    'load_enc_start_pos': 13,           # 13: Load raw absolute encoder position
    'dummy1': 14,                       # 14: Not used
    'encoder_installed': 15,            # 15: Synchronize P_IST with P_ENCODER
    'encoder_pulse_a': 16,              # 16: Short pulse on channel A
    'encoder_pulse_b': 17,              # 17: Short pulse on channel B
    'var_cur_en': 18,                   # 18: Adjust max running current
    'ext_enc_scale': 19,                # 19: Scale external encoder
    'mcnt_load': 20,                    # 20:
    'dummy3': 21,                       # 21: Not used
    'encoder_resolution': 22,           # 22-24: Encoder resolution
    'dummy4': 25                        # 25-31: Not used
    }
        
        self.ssi_setup = {        
    'data_bit_count': (0, 5),             # 00-04: 0..31 bits of data
    'number_of_samples': (5, 3),          # 05-07: Number of samples within MaxSampleDeviation
    'clock_speed': (8, 8),                # 08-15: x10kHz clock frequency, max 2.55 MHz
    'max_sample_deviation': (16, 13),     # 16-28: 0..8191 encoder counts as deviation
    'retries': (29, 3)                    # 29-31: Max. measurement retries
    }
        
        self.ssi_setup_2 = {
    'prepare_time': (0, 8),               # 00-07: 0..256 in units of 1 µs
    'gray_code_not_binary': 8,            # 08: 1 = gray code, 0 = raw output
    'use_std_ssi_resultion': 9,           # 09: 1: Calculate multiturn and single turn pos
    'disable_interrupts': 10,             # 10: 1: Interrupts are disabled, 0: Interrupts are not disabled
    'wait_time': (11, 8),                 # 11-18: 0..255 in units of 1 µs
    'msb_first': 19,                      # 19: 1=MSB first, swap the incoming data bits
    'use_extended_ssi_format': 20,        # 20: 1=use extended SSI format for PA0260
    'singleturn_resolution': (21, 5),     # 21-25: Singleturn resolution (in bits)
    'multiturn_resolution': (26, 6)       # 26-31: Multiturn resolution (in bits)
        }

        self.dmx_options = {
    'auto_clear_errors': 0,      # Bit 0
    'bit1': 1,                   # Bit 1
    'send_acceleration': 2,      # Bit 2
    'no_homing': 3,              # Bit 3
    'bit4': 4,                   # Bit 4
    'bit5': 5,                   # Bit 5
    'enabled_usart1': 6,         # Bit 6
    'enabled_uart4': 7,          # Bit 7
    'dummy': 8                   # Bits 8-31: Reserved
        }

        self.cmd_reg = {
    'fast_mac_start': 0,
    'errors_clear': 97,
    'fast_mac_end': 255,
    'activate_baudrate': 256,
    'resync_position': 257,
    'calibrate_encoder': 258,
    'program_pld': 259,
    'show_resur': 260,
    'clear_backup_data': 264,
    'clear_all_backup_data': 265,
    'clear_resur_err': 266,
    'reset': 267,
    'save2flash_reset': 268,
    'save2flash': 269,
    'debug_start': 280,
    'resur_debug0': 280,
    'debug_end': 300,
    'encoder_preset': 316,
    'encoder_reedtest': 317,
    'encoder_halloffs': 318,
    'encoder_retnorm': 319,
    'init_ssi': 320,
    'read_ssi': 321,
    'read_ssi_cvt_gray_to_bin': 322,
    'enable_mb_sync': 325,
    'disable_mb_sync': 326,
    'resur_homed_clr': 327,
    'resur_homed_set': 328,
    'unlock_pw': 330,
    'zpassw': 331,
    'lock': 332,
    'srandom_tick': 337,
    'srandom_v7': 338,
    'random_v8': 339,
    'extenc': 340,
    'extenc_halfback': 341,
    'clear_rxp_flash': 342,
    'reset_encoder': 343,
    'restore_enc_cal': 345,
    'backup_enc_cal': 346,
    'backup_enc_lin': 347,
    'restore_enc_lin': 348,
    'mod_comm_spd_2m': 349,
    'linearize_intref': 350,
    'linearize_extref': 351,
    'enable_linearize': 352,
    'disable_linearize': 353,
    'mltenc_atomic_preset': 354,
    'check_sega_backup': 355,
    'clear_cal_data': 356,
    'sgtenc_atomic_preset': 357,
    'led_seq_play': 367,
    'led_seq_running': 368,
    'led_seq_indcation': 369,
    'led_seq_normal': 370,
    'h3_activate_testmode_1': 371,
    'h3_activate_testmode_2': 372,
    'h3_activate_testmode_3': 373,
    'led_seq_p0_control': 374,
    'cl_calibration': 383,
    'cl_offset_start': 385,
    'cl_offset_clear': 386,
    'cl_disable_linearization': 387,
    'cl_enable_linearization': 388,
    'protest_follow_error': 389,
    'protest_brake_on': 390,
    'protest_brake_off': 391,
    'protest_mhm_magnet_gain': 392,
    'protest_none': 393,
    'protest_cl_highspeed': 394,
    'mhm_clear_init': 395,
    'mhm_reset': 397,
    'do_estop_with_dec': 398,
    'do_estop_without_dec': 399,
    'factory_default': 405,
    'cl_settings_transfer': 406,
    'protest_mhm_cal_bias': 407,
    'protest_mhm_testmode': 408,
    'debug_mhm': 409,
    'debug_disable_sw_limits': 420,
    'debug_enable_sw_limits': 421,
    'vel_override': 423,
    'disable_hw_limit_pos': 424,
    'disable_hw_limit_neg': 425,
    'enable_hw_limits': 426,
    'read_mhm_status': 427,
    'read_mhm_status_and_setup': 428,
    'rs422_select_h2_out': 432,
    'rs422_select_stepgen_out': 433,
    'store_kphase': 720,
    'get_default_kphases': 721,
    'ssi_lintab_magoffset': 901,
    'ssi_get_kphase': 902,
    'ssi_get_lintab': 903,
    'ssi_get_magnetoffset': 904,
    'ssi_run_to_zero': 905,
    'ssi_manual_kphase': 906,
    'writescale': 4122,
    'readscale': 4123,
    'clearscale': 4124,
    'getscale_uom_addr': 4125,
    'getscale_addr': 4126,
    'scale_position': 4150,
    'scale_velocity': 4151,
    'scale_acceleration': 4152,
    'scale_auto': 4160,
    'show_error_counters': 4191,
    'temp_flwerr_disable': 20,
    'pwr_dump_test_timeout': 1000,
    'pwr_dump_test_pulse': 5000,
    'arm_power_dump_test': 0x401,
    'fire_power_dump_test': 0x402
}
        
        # STATIC I/O DEFINITIONS
        self.io_read_words = [self.registers["mode_reg"][0],
                              self.registers["p_ist"][0],
                              self.registers["v_ist"][0],
                              self.registers["flex_reg"][0],
                              self.registers["error_bits"][0]]
        
        self.io_write_words = [self.registers["mode_reg"][0],
                               self.registers["p_soll"][0],
                               self.registers["v_soll"][0],
                               self.registers["a_soll"][0]]
        
        # Remapping for EtherCAT DSP 
        self.dsp_map = {
            self.registers["inputs"][0] : (0x60FD,0x00),
            self.registers["outputs"][0] : (0x60FE,0x00),
            self.registers["in_pos_limit"][0] : (0x6067,0x00),
            self.registers["p_ist"][0] : (0x6064,0x00),
            self.registers["p_soll"][0] : (0x607A,0x00),
            self.registers["min_tt_count"][0] : (0x607D,0x01),
            self.registers["max_tt_count"][0] : (0x607D,0x02),
            self.registers["v_soll"][0] : ((0x6080,0x0),(0x60FF,0x00)),
            self.registers["follow_err"][0] : (0x60F4,0x00),
            self.registers["v_ist"][0] : (0x606C,0x00),       
        }
