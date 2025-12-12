from .Motor import *
NO_SCALING = 1.0

POS_FACTOR = 1.0/8192.0 
VEL16_FACTOR = 60.0/(16*8192*0.001300049) 
ACC_FACTOR = 60/(16 * 8192 * 0.001300049 * 0.001300049)
TORQ_FACTOR = 300.0/1023.0 
DEG_FACTOR = 360.0/8192.0 
LOAD_FACTOR = 1.0/65536
DEGC_FACTOR = 1.0/((4096/5)*0.01) 
ANINV_FACTOR = 10.0/2047 
ANIOMA_FACTOR = 1000.0/(65535*0.8) 
CURR_FACTOR = 0.013
CURR_GAIN_FACTOR = 1.0/256 
ELDEG_FACTOR = 360.0*4/8192
PWM_FACTOR = 100.0/3200 
BUSV_FACTOR = 0.888 

CNTS_REV_MAC = 8192

MACRegisterName = Literal[
    "a_reg_p",
    "a_soll",
    "abs_enc_pos",
    "acc_1",
    "acc_2",
    "acc_3",
    "acc_4",
    "acc_emerg",
    "aifilt_filtfact",
    "aifilt_maxslope",
    "amplitude",
    "aninp",
    "aninp1",
    "aninp1_offset",
    "aninp2",
    "aninp2_offset",
    "aninp3",
    "aninp3_offset",
    "aninp_offset",
    "anout1",
    "anout1_offset",
    "build_no",
    "capcom0",
    "capcom1",
    "capcom2",
    "capcom3",
    "capcom4",
    "capcom5",
    "capcom6",
    "capcom7",
    "chksum",
    "cntrl_bits",
    "comm_alive_tim",
    "comm_errs",
    "command",
    "counter_100us",
    "current_1",
    "current_2",
    "current_3",
    "current_4",
    "degc",
    "degcmax",
    "dummy",
    "ePLC_command",
    "ePLC_parameter",
    "ePLC_status_a",
    "ePLC_status_b",
    "eldeg_ist",
    "eldeg_offset",
    "emk_a",
    "emk_b",
    "emk_c",
    "enc_offset",
    "err_info",
    "err_stat_2",
    "err_value",
    "error_bits",
    "extenc_bits",
    "ff_out",
    "fieldbus_addr",
    "fieldbus_speed",
    "flex_reg",
    "fnc_err",
    "fnc_out",
    "fncerrmax",
    "follow_err",
    "follow_err_max",
    "fpga_version",
    "fw_version",
    "g_fnc",
    "g_fnc_hi",
    "gear1",
    "gear2",
    "gimp_rw_area",
    "gv_ext",
    "home_mode",
    "hw_plim",
    "hw_setup",
    "hw_version",
    "hwid0",
    "hwid1",
    "hwid10",
    "hwid11",
    "hwid2",
    "hwid3",
    "hwid4",
    "hwid5",
    "hwid6",
    "hwid7",
    "hwid8",
    "hwid9",
    "i2t",
    "i2tlim",
    "i_nom",
    "ia_ist",
    "ia_offset",
    "ia_soll",
    "ib_ist",
    "ib_offset",
    "ib_soll",
    "ic_ist",
    "ic_soll",
    "id_reserved",
    "in_pos_limit",
    "in_pos_retries",
    "index_ist",
    "index_off_hires",
    "index_offset",
    "input_levels",
    "inputs",
    "iosetup",
    "kff0",
    "kff1",
    "kff2",
    "kff3",
    "kff4",
    "kff5",
    "kia",
    "kib",
    "kib0",
    "kib1",
    "kifx1",
    "kifx2",
    "kify0",
    "kify1",
    "kvb0",
    "kvb1",
    "kvb2",
    "kvb3",
    "kvb4",
    "kvfx1",
    "kvfx2",
    "kvfx3",
    "kvfx4",
    "kvfx5",
    "kvfx6",
    "kvfy",
    "kvfy1",
    "kvfy2",
    "kvfy3",
    "kvfy4",
    "kvfy5",
    "kvout",
    "kvout_lo",
    "kvout_max_vel",
    "kvout_min_vel",
    "kvout_select",
    "l_reg_p",
    "load_1",
    "load_2",
    "load_3",
    "load_4",
    "mac00_10",
    "mac00_11",
    "mac00_12",
    "mac00_13",
    "mac00_14",
    "mac00_15",
    "mac00_2",
    "mac00_3",
    "mac00_4",
    "mac00_5",
    "mac00_6",
    "mac00_7",
    "mac00_9",
    "mac00_type",
    "man_alpha",
    "man_i_nom",
    "max_p_ist",
    "mb_rd_data",
    "mb_rd_reg",
    "mb_wr_data",
    "mb_wr_reg",
    "min_p_ist",
    "mode_1",
    "mode_2",
    "mode_3",
    "mode_4",
    "mode_reg",
    "mode_vist_tq",
    "motor_type",
    "my_addr",
    "outloopdiv",
    "outputs",
    "p_fnc",
    "p_home",
    "p_ist",
    "p_ist_turntab",
    "p_multiturn",
    "p_new",
    "p_offset",
    "p_quick",
    "p_reg_p",
    "p_soll",
    "phase_comp",
    "phi_soll",
    "pos_1",
    "pos_2",
    "pos_3",
    "pos_4",
    "pos_5",
    "pos_6",
    "pos_7",
    "pos_8",
    "prog_version",
    "pwr_dump_pause_10",
    "pwr_dump_pause_13",
    "pwr_dump_volt",
    "rec_cnt",
    "reg370",
    "rxp_comm_ecnt",
    "rxp_comm_res",
    "rxp_setup",
    "s_order",
    "sample1",
    "sample2",
    "sample3",
    "sample4",
    "sample5",
    "sample6",
    "sample7",
    "sample8",
    "serial_number",
    "setup_bits",
    "start_mode",
    "start_mode_val",
    "status_bits",
    "t_home",
    "t_reg_p",
    "t_soll",
    "task_time",
    "tc0_cv1",
    "tc0_cv2",
    "turntable_rev",
    "u_24v",
    "u_bus",
    "u_bus_offset",
    "ua_val",
    "uart0_setup",
    "uart1_setup",
    "ub_val",
    "uc_val",
    "uit",
    "uitlim",
    "umeas",
    "useroutval",
    "uv_handle",
    "v_eldeg",
    "v_ext",
    "v_home",
    "v_ist",
    "v_ist_16",
    "v_reg_p",
    "v_soll",
    "vb_out",
    "velocity_1",
    "velocity_2",
    "velocity_3",
    "velocity_4",
    "velocity_5",
    "velocity_6",
    "velocity_7",
    "velocity_8",
    "vf_out",
    "xreg_addr",
    "xreg_data",
    "z_reg_p",
    "zero_1",
    "zero_2",
    "zero_3",
    "zero_4",
    "zup2_bits",
]

class MACMotor(Motor):
    def __init__(self):
        super().__init__()
        self.registers = {
    'dummy': [0, NO_SCALING, None],
    'prog_version': [1, NO_SCALING, 0],
    'mode_reg': [2, NO_SCALING, 2],
    'p_soll': [3, POS_FACTOR, 2],
    'p_new': [4, POS_FACTOR, 2],
    'v_soll': [5, VEL16_FACTOR, 2],
    'a_soll': [6,ACC_FACTOR, 2],
    't_soll': [7, TORQ_FACTOR, 2],
    'p_fnc': [8, -1/(8192*16.0), 2],
    'index_offset': [9, DEG_FACTOR, 2],
    'p_ist': [10, POS_FACTOR, 2],
    'v_ist_16': [11,VEL16_FACTOR, 0],
    'v_ist': [12, 60/(8192*0.0013), 0],
    'kvout': [13, LOAD_FACTOR, 2],
    'gear1': [14, NO_SCALING, 2],
    'gear2': [15, NO_SCALING, 2],
    'i2t': [16, 100.0/125000, 0],
    'i2tlim': [17, NO_SCALING, 0],
    'uit': [18, 100.0/1080, 0],
    'uitlim': [19, NO_SCALING, 2],
    'follow_err': [20, POS_FACTOR, 2],
    'u_24v': [21, 107/8192.0 , 0],
    'follow_err_max': [22, POS_FACTOR, 2],
    'uv_handle': [23, NO_SCALING, 2],
    'fnc_err': [24, 100.0/1e9 , 2],
    'p_ist_turntab': [25, NO_SCALING, 0],
    'fncerrmax': [26, NO_SCALING, 2],
    'turntable_rev': [27, NO_SCALING, 2],
    'min_p_ist': [28, POS_FACTOR, 2],
    'degc': [29, NO_SCALING, 0],
    'max_p_ist': [30, POS_FACTOR, 2],
    'degcmax': [31, NO_SCALING, 0],
    'acc_emerg': [32, ACC_FACTOR, 2],
    'in_pos_limit': [33, NO_SCALING, 2],
    'in_pos_retries': [34, NO_SCALING, 2],
    'error_bits': [35, NO_SCALING, 2],
    'cntrl_bits': [36, NO_SCALING, 2],
    'start_mode': [37, NO_SCALING, 2],
    'start_mode_val': [37, NO_SCALING, 2],
    'p_home': [38, POS_FACTOR, 2],
    'hw_setup': [39, NO_SCALING, 2],
    'v_home': [40, VEL16_FACTOR, 2],
    't_home': [41, TORQ_FACTOR, 2],
    'home_mode': [42, NO_SCALING, 2],
    'p_reg_p': [43, NO_SCALING, 2],
    'v_reg_p': [44, NO_SCALING, 2],
    'a_reg_p': [45, NO_SCALING, 2],
    't_reg_p': [46, NO_SCALING, 2],
    'l_reg_p': [47, NO_SCALING, 2],
    'z_reg_p': [48, NO_SCALING, 2],

    'pos_1': [49, POS_FACTOR, 2],
    'capcom0': [50, NO_SCALING, 2],
    'pos_2': [51, POS_FACTOR, 2],
    'capcom1': [52, NO_SCALING, 2],
    'pos_3': [53, POS_FACTOR, 2],
    'capcom2': [54, NO_SCALING, 2],
    'pos_4': [55, POS_FACTOR, 2],
    'capcom3': [56, NO_SCALING, 2],
    'pos_5': [57, POS_FACTOR, 2],
    'capcom4': [58, NO_SCALING, 2],
    'pos_6': [59, POS_FACTOR, 2],
    'capcom5': [60, NO_SCALING, 2],
    'pos_7': [61, POS_FACTOR, 2],
    'capcom6': [62, NO_SCALING, 2],
    'pos_8': [63, POS_FACTOR, 2],
    'capcom7': [64, NO_SCALING, 2],

    'velocity_1': [65, VEL16_FACTOR, 2],
    'velocity_2': [66, VEL16_FACTOR, 2],
    'velocity_3': [67, VEL16_FACTOR, 2],
    'velocity_4': [68, VEL16_FACTOR, 2],
    'velocity_5': [69, VEL16_FACTOR, 2],
    'velocity_6': [70, VEL16_FACTOR, 2],
    'velocity_7': [71, VEL16_FACTOR, 2],
    'velocity_8': [72, VEL16_FACTOR, 2],

    'acc_1': [73, ACC_FACTOR, 2],
    'acc_2': [74, ACC_FACTOR, 2],
    'acc_3': [75, ACC_FACTOR, 2],
    'acc_4': [76, ACC_FACTOR, 2],

    'current_1': [77, TORQ_FACTOR, 2],
    'current_2': [78, TORQ_FACTOR, 2],
    'current_3': [79, TORQ_FACTOR, 2],
    'current_4': [80, TORQ_FACTOR, 2],

    'load_1': [81, LOAD_FACTOR, 2],
    'load_2': [82, LOAD_FACTOR, 2],
    'load_3': [83, LOAD_FACTOR, 2],
    'load_4': [84, LOAD_FACTOR, 2],

    'zero_1': [85, NO_SCALING, 2],
    'zero_2': [86, NO_SCALING, 2],
    'zero_3': [87, NO_SCALING, 2],
    'zero_4': [88, NO_SCALING, 2],

    'mode_1': [89, NO_SCALING, 2],
    'mode_2': [90, NO_SCALING, 2],
    'mode_3': [91, NO_SCALING, 2],
    'mode_4': [92, NO_SCALING, 2],

    'hwid0': [93, NO_SCALING, 2],
    'hwid1': [94, NO_SCALING, 2],
    'hwid2': [95, NO_SCALING, 2],
    'hwid3': [96, NO_SCALING, 2],
    'hwid4': [97, NO_SCALING, 2],
    'hwid5': [98, NO_SCALING, 2],
    'hwid6': [99, NO_SCALING, 2],
    'hwid7': [100, NO_SCALING, 2],
    'hwid8': [101, NO_SCALING, 2],
    'hwid9': [102, NO_SCALING, 2],
    'hwid10': [103, NO_SCALING, 2],
    'hwid11': [104, NO_SCALING, 2],

    'mac00_type': [105, NO_SCALING, 2],
    'inputs': [106, NO_SCALING, 2],
    'mac00_2': [107, NO_SCALING, 2],
    'mac00_3': [108, NO_SCALING, 2],
    'mac00_4': [109, NO_SCALING, 2],
    'mac00_5': [110, NO_SCALING, 2],
    'mac00_6': [111, NO_SCALING, 2],
    'mac00_7': [112, NO_SCALING, 2],
    'outputs': [113, NO_SCALING, 2],
    'mac00_9': [114, NO_SCALING, 2],
    'mac00_10': [115, NO_SCALING, 2],
    'mac00_11': [116, NO_SCALING, 2],
    'mac00_12': [117, NO_SCALING, 2],
    'mac00_13': [118, NO_SCALING, 2],
    'mac00_14': [119, NO_SCALING, 2],
    'mac00_15': [120, NO_SCALING, 2],

    'kff5': [121, NO_SCALING, 2],
    'kff4': [122, NO_SCALING, 2],
    'kff3': [123, NO_SCALING, 2],
    'kff2': [124, NO_SCALING, 2],
    'kff1': [125, NO_SCALING, 2],
    'kff0': [126, NO_SCALING, 2],

    'kvfx6': [127, NO_SCALING, 2],
    'kvfx5': [128, NO_SCALING, 2],
    'kvfx4': [129, NO_SCALING, 2],
    'kvfx3': [130, NO_SCALING, 2],

    'kvfx2': [131, NO_SCALING, 2],
    'kvfx1': [132, NO_SCALING, 2],

    'kvfy5': [133, NO_SCALING, 2],
    'kvfy4': [134, NO_SCALING, 2],
    'kvfy3': [135, NO_SCALING, 2],
    'kvfy2': [136, NO_SCALING, 2],
    'kvfy1': [137, NO_SCALING, 2],
    'kvfy': [138, NO_SCALING, 2],

    'kvb4': [139, NO_SCALING, 2],
    'kvb3': [140, NO_SCALING, 2],
    'kvb2': [141, NO_SCALING, 2],
    'kvb1': [142, NO_SCALING, 2],
    'kvb0': [143, NO_SCALING, 2],

    'kifx2': [144, NO_SCALING, 0],
    'kifx1': [145, NO_SCALING, 0],
    'kify1': [146, NO_SCALING, 0],
    'kify0': [147, NO_SCALING, 0],

    'kib1': [148, NO_SCALING, 0],
    'kib0': [149, NO_SCALING, 0],

    'id_reserved': [155, NO_SCALING, 2],
    's_order': [156, NO_SCALING, 2],
    'outloopdiv': [157, NO_SCALING, 2],

    'sample1': [158, NO_SCALING, 2],
    'sample2': [159, NO_SCALING, 2],
    'sample3': [160, NO_SCALING, 2],
    'sample4': [161, NO_SCALING, 2],

    'rec_cnt': [162, NO_SCALING, 2],
    'v_ext': [163, NO_SCALING, 0],
    'gv_ext': [164, NO_SCALING, 0],
    'g_fnc': [165, NO_SCALING, 0],
    'fnc_out': [166, NO_SCALING, 0],
    'ff_out': [167, NO_SCALING, 0],
    'vb_out': [168, NO_SCALING, 0],
    'vf_out': [169, TORQ_FACTOR, 0],
    'aninp': [170, ANINV_FACTOR, 0],
    'aninp_offset': [171, ANINV_FACTOR, 2],
    'eldeg_offset': [172, NO_SCALING, 0],
    'phase_comp': [173, NO_SCALING, 0],
    'amplitude': [174, NO_SCALING, 0],
    'man_i_nom': [175, 300.0/65536 , 2],
    'man_alpha': [176, ELDEG_FACTOR, 2],
    'umeas': [177, 1.0/1600, 2],
    'i_nom': [178, CURR_FACTOR, 0],
    'phi_soll': [179, 90.0/511, 0],

    'ia_soll': [180, CURR_FACTOR, 0],
    'ib_soll': [181, CURR_FACTOR, 0],
    'ic_soll': [182, CURR_FACTOR, 0],
    'ia_ist': [183, CURR_FACTOR, 0],
    'ib_ist': [184, CURR_FACTOR, 0],
    'ic_ist': [185, CURR_FACTOR, 0],
    'ia_offset': [186, CURR_FACTOR, 0],
    'ib_offset': [187, CURR_FACTOR, 0],

    'kia': [188, CURR_GAIN_FACTOR, 0],
    'kib': [189, CURR_GAIN_FACTOR, 0],
    'eldeg_ist': [190, ELDEG_FACTOR, 0],
    'v_eldeg': [191, 60/(8192*0.0001), 0],
    'ua_val': [192, PWM_FACTOR, 0],
    'ub_val': [193, PWM_FACTOR, 0],
    'uc_val': [194, PWM_FACTOR, 0],
    'emk_a': [195, NO_SCALING, 0],
    'emk_b': [196, NO_SCALING, 0],
    'emk_c': [197, NO_SCALING, 0],
    'u_bus': [198, BUSV_FACTOR, 0],
    'u_bus_offset': [199, BUSV_FACTOR, 0],
    'tc0_cv1': [200, NO_SCALING, 0],
    'tc0_cv2': [201, NO_SCALING, 0],
    'my_addr': [202, NO_SCALING, 2],
    'motor_type': [203, NO_SCALING, 0],
    'serial_number': [204, NO_SCALING, 2],
    'hw_version': [205, NO_SCALING, 0],
    'chksum': [206, NO_SCALING, 0],
    'useroutval': [207, NO_SCALING, 2],
    'comm_errs': [208, NO_SCALING, 2],
    'index_ist': [209, DEG_FACTOR, 0],
    'hw_plim': [210, NO_SCALING, 2],
    'command': [211, NO_SCALING, 2],
    'uart0_setup': [212, NO_SCALING, 2],
    'uart1_setup': [213, NO_SCALING, 2],
    'extenc_bits': [214, NO_SCALING, 2],
    'input_levels': [215, NO_SCALING, 2],
    'aninp1': [216, ANINV_FACTOR, 2],
    'aninp1_offset': [217, ANINV_FACTOR, 2],
    'aninp2': [218, ANINV_FACTOR, 2],
    'aninp2_offset': [219, ANINV_FACTOR, 2],
    'aninp3': [220, ANINV_FACTOR, 2],
    'aninp3_offset': [221, ANINV_FACTOR, 2],
    'iosetup': [222, NO_SCALING, 2],
    'anout1': [223, ANIOMA_FACTOR, 2],
    'anout1_offset': [224, ANIOMA_FACTOR, 2],
    'p_offset': [225, POS_FACTOR,2],
    'enc_offset': [225,NO_SCALING,2],
    'p_multiturn': [226, POS_FACTOR,2],
    'abs_enc_pos': [226,NO_SCALING,2],
    'aifilt_maxslope': [227, 170.0*0.0013, 2],
    'aifilt_filtfact': [228, NO_SCALING, 2],
    'p_quick': [229, POS_FACTOR, 2],
    'xreg_addr': [230, NO_SCALING, 2],
    'xreg_data': [231, NO_SCALING, 2],
    'fieldbus_addr': [232, NO_SCALING, 2],
    'fieldbus_speed': [233, NO_SCALING, 2],
    'rxp_setup': [234, NO_SCALING, 2],
    'err_stat_2': [235, NO_SCALING, 0],
    'setup_bits': [236, NO_SCALING, 2],
    'status_bits': [237, NO_SCALING, 0],
    'err_info': [242, NO_SCALING, 2],
    'err_value': [243, NO_SCALING, 2],
    'zup2_bits': [246, NO_SCALING, 2],
    'fw_version': [250, NO_SCALING, 2],
    'build_no': [253, NO_SCALING, 2],
    'fpga_version': [254, NO_SCALING, 0],
    'counter_100us': [255, NO_SCALING, 2],
    'sample5': [256, NO_SCALING, 2],
    'sample6': [257, NO_SCALING, 2],
    'sample7': [258, NO_SCALING, 2],
    'sample8': [259, NO_SCALING, 2],
    'mb_rd_reg': [262, NO_SCALING, 0],
    'mb_rd_data': [263, NO_SCALING, 0],
    'mb_wr_reg': [264, NO_SCALING, 0],
    'mb_wr_data': [265, NO_SCALING, 0],
    'rxp_comm_res': [266, NO_SCALING, 0],
    'rxp_comm_ecnt': [267, NO_SCALING, 2],
    'flex_reg': [268, NO_SCALING, 2],
    'mode_vist_tq': [269, NO_SCALING, 2],
    'comm_alive_tim': [270, NO_SCALING, 2],
    'gimp_rw_area': [271, NO_SCALING, 2],
    'kvout_min_vel': [272, VEL16_FACTOR, 2],
    'kvout_max_vel': [273, VEL16_FACTOR, 2],
    'kvout_lo': [274, NO_SCALING, 2],
    'kvout_select': [275, NO_SCALING, 2],
    'index_off_hires': [276, NO_SCALING, 2],
    'g_fnc_hi': [277, NO_SCALING, 2],
    'task_time': [278, NO_SCALING, 2],
    'pwr_dump_volt': [280, NO_SCALING, 2],
    'pwr_dump_pause_10': [281, NO_SCALING, 0],
    'pwr_dump_pause_13': [282, NO_SCALING, 0],

    "reg370": [370,NO_SCALING,2],

    'ePLC_parameter': [501,NO_SCALING,1],
    'ePLC_command': [502,NO_SCALING,1],
    'ePLC_status_a': [503,NO_SCALING,0],
    'ePLC_status_b': [504,NO_SCALING,0]
}
        
        self.ctl_mode = {
            "passive": 0,
            "velocity": 1,
            "position": 2,
            "gear": 3,
            "analog_trq": 4,
            "analog_vel": 5,
            "analog_vel_gear": 6,
            "manual_current": 7,
            "test_u": 8,
            "test_a": 9,
            "brake": 10,
            "stop": 11,
            "torque": 12,
            "forward": 13,
            "forward_backward": 14,
            "safe": 15,
            "analog_vel_deadband": 16,
            "analog_trq_vel_limited": 17,
            "analog_gear": 18,
            "coil": 19,
            "analog_bi_pos": 20,
            "analog_to_pos": 21,
            "test_ki": 22,
            "test_trq": 23,
            "gear_follow": 24,
            "index_slow": 25,
            "index_fast": 26,
            "highest": 27
        }
        # Reg 23 UV_HANDLE:
        self.uv_handle = {
    "set_uv_err": 0,
    "uv_contr_stop": 1,
    "uv_vsoll0": 2
        }
        # Reg 35 ERR_STAT
        self.error_bits = { 
    "i2t_err": 0,
    "flw_err": 1,
    "fnc_err": 2,
    "uit_err": 3,

    "in_pos": 4,
    "acc_flag": 5,
    "dec_flag": 6,
    "pos_limit": 7,

    "deg_c_err": 8,
    "uv_err": 9,
    "uv_detect": 10,
    "ov_err": 11,

    "ipeak_err": 12,
    "speed_err": 13,
    "dis_p_lim": 14,
    "index_err": 15,

    "oldfilt_err": 16,
    "u24v_err": 17,

    "vac_on": 19,

    "pwm_locked": 20,
    "comm_err": 21,
    "curloop_err": 22,
    "slave_err": 23,

    "any_err": 24,
    "init_err": 25,
    "flash_err": 26,
    "sto_alarm_err": 27,

    "fpga_err": 28,

    "out1_status": 30,
    "out2_status": 31
    }
        # Reg 36 CNTRL_BITS:
        self.ctl_bits = { 
    "recordbit": 0,
    "rewindbit": 1,
    "recinnerbit": 2,  # record in inner loop
    "relpospsoll": 3,
    "relpospfnc": 4,
    "syncposaauto": 5,
    "syncposman": 6,
    "man_no_brake": 7,
    "syncposrel": 8,
    "index_home": 9,
    "fwtrigbits": 10,  # 0x400 - 1024 when set, use the advanced sampling in record.s - when 0, use backwards compatible sampling
    "sampling_bit": 11,  # 0x800 - 2048 set when sampling is active after trigger has been detected
    "trigger_armed_bit": 12,  # 0x1000 - 4096 set when sampling is active but trigger has not been detected yet
    "advsample_bit": 13,  # 0x2000 - 8192 if set, enables div-shift, min/max/avg + bitfield sampling
    "commsample_bit": 14,  # 0x4000 - 16384 if set, enables sampling of fastmac+modbus communications to/from the motor
    "sample_started": 15,  # 0x8000 - 32768 set when trigger_armed_bit gets set, cleared on each macTalk readSample
    "uart0sample_bit": 16,  # 0x10000 - 65536 if set, enables sampling of UART0 modbus communications to/from the motor
    "encoder_startup0": 17,
    "encoder_startup1": 18  # encoder startup for MING3
    }
        #Reg 39 HW_SETUP:
        self.hw_setup_bits = {
    "diraw": 0,
    "dirbw": 1,
    "pulseout": 2,  # = altera.wrltchc[0]
    "xsel1": 3,  # = altera.wrltchc[1]
    "xprin": 4,  # = altera.wrltchc[2]
    "nofilt": 5,  # = altera.wrltchc[3]
    "invxdir": 6,  # = altera.wrltchc[4]
    "invrotdir": 7,
    "user_inpos": 8,
    "user_error": 9,  # error output pin is controlled by the user via register xx
    "inv_inpos_out": 10,
    "inv_error_out": 11,
    "system3r": 12,  # custom specific! Changes calculation in inposition and use of pos7/p8 and more
    "module_pwr_always": 13,  # keep 5v module transistor on, even though 5v module power detected. used for minimac control voltage
    "cmp_error_out": 14,  # if set, out2_pin is controlled by (p_ist > cmp_pos0)

    "dircdwr": 16,  # = altera.wrltchc[5] direction signal for the multifuncio2 a channel (or both a and b?)
    "altera_dircd": 5,  # ^ i.e.
    "selindex": 17,  # = altera.wrltchc[6] not used - prepared to select between encoder a or index signal -> multf
    "altera_selindex": 6,  # ^ i.e.
    "always_cool": 18,
    "position_capture_up": 19,  # used to enable sw position capture based on analog input rising edge
    "position_capture_dn": 20,  # used to enable sw position capture based on analog input falling edge
    "pulse_8000": 21,  # if set, rescale the 8192 encoder pulses to 8000 for mac800 compatibility and better vel-filter performance
    "enc_scaling": 22,  # reserved for freely selectable encoder scaling
    "sbuf_2048": 23,  # set to use a sample buffer length of 2048. use 512 if not set (backwards compatible)
    "turntable_mode": (24,2),  # turntable mode, 2 bits - 0=None, 1=CW, 2=CCW, 3=shortest path
    #"turntable_shift": 24,
    "turntable_multi": 26,  # turntable multiturn option
    "turntable_swap_pist": 27,  # <-- not implemented(!) turntable causes p_ist and p_ist_turntab to swap register numbers/places
    "sbuf_8_chan": 28,  # set to use 8 rather than 4 channels in the sbuf sample/scope function
    "capture_no_jitter": 29,  # set position capture to a (more) fixed point in timeslice tail at the cost of rxp
    "switch_10khz": 30  # use pwm switching frequency of 10 khz instead of the default 20 khz
    }
        self.turntable_mode = {
            "no_selection" : 0,
            "CW" : 1,
            "CCW" : 2,
            "shortest_path" : 3
        }

        # Reg 43 HOME_MODE
        self.home_done = {"home_done": 16 }

        #Reg 59 POS 5 in coil mode
        self.coil_bits = {
    "start_dir": 0,
    "pos_cmd": 1,
    "pwr_cmd": 2,
    "pos_accept": 3,
    "pwr_flash": 4
    }
        
        #Reg 207 
        self.user_out_bits = {
            "in_pos_val": 0,
            "error_val": 1
        }

        self.hw_plim = {
            "plim_neg": 0,
            "plim_pos": 1
        }

        #Reg 211 CMD_REG
        self.cmd_reg = { 
    "reset": 0x1,  # perform an immediate and unconditional CPU reset (!)
    "save2flash_reset": 0x2,  # ask main loop to save in flash (ignored if not in passive or safe mode)
    "pmultiturn_to_poffset": 0x200,  # set P_OFFSET = - P_MULTITURN
    "100": 100,  # used for debug/test of current filters, and help make speed/torque plots
    "101": 101,  # used for finding/evaluating FOC coefficients by a MANI_MODE step
    "999": 999,  # unlocks commands 100 and 101 and CMD_FORCE_BRAKE_xx
    "internal_use_first": 0x0FFF,  # 
    "tqtest_12h": 0x0FFF,  # Configure and start a 10-hour sampling of VF_OUT, DEGC, UBUS
    "auto_enc_adjust": 0x1000,  # calc ELDEG_OFFSET automatically using MANI mode
    "debug_1": 0x1001,  # general-purpose debug commands - meanings change over time..
    "debug_2": 0x1002,  # 
    "debug_3": 0x1003,  # 
    "debug_4": 0x1004,  # 
    "fixed_pwm_on": 0x1005,  # Sets a fixed PWM pattern on motor phases. Useful for service/test.
    "fixed_pwm_off": 0x1006,  # Stops fixed PWM signals. POS0/1/2 = -1600..+1600 => 0-100% PWM
    "mftest_prepare": 0x1007,  # sets up test direction and hardware port MF1/MF2 and A->B/B->A
    "mftest_execute": 0x1008,  # starts executing multifunction hardware tests - assumes signals looped.
    "mftest_done": 0x1009,  # no longer used - DO_TGT now autocompletes
    "set_jvl_modbus": 0x100A,  # Set Reg213, UART1_SETUP, to the fixed value 0x100b27.
    "mb_rxdump_on": 0x100B,  # User debug - dump bytes received in Modbus to (POS0..MODE3)->Reg350,352,353,...
    "mb_rxdump_off": 0x100C,  # User debug - dump bytes received in Modbus to (POS0..MODE3)->Reg350,352,353,...
    "random_on": 0x100D,  # Removed in v2.09 to free registers
    "random_off": 0x100E,  # Removed in v2.09 to free registers
    "go2mbit": 0x100F,  # Change Modbus baudrate to 2 Mbit after reply is sent
    "sample_hall": 0x1010,  # Sample Hall signals while rotating in MANI mode - also calc eldeg_offset
    "detect_enctype": 0x1011,  # Sample Hall signals while rotating in MANI mode - used to detect Sumtak/Quantum encoder type
    "zero_g_fn": 0x1012,  # Set G_FNC to zero
    "mani_turn_start": 0x1013,  # Start turning motor in MANI_MODE speed selected by negative values of TQ3
    "mani_turn_stop": 0x1014,  # Stop turning motor in MANI_MODE speed selected by negative values of TQ3
    "pid_off": 0x1015,  # Disables the general-purpose PID function
    "pid_on": 0x1016,  # Enables the general-purpose PID function
    "pid_on_debug2": 0x1017,  # Enables the general-purpose PID function with medium debug (POSx)
    "pid_on_debug3": 0x1018,  # Enables the general-purpose PID function with heavy debug (POSx+VELx)
    "cpu_id": 0x1019,  # copy the raw CPU_ID value to POS0 for service purposes
    "set_reg_scale": 0x101A,  # transfer read scaling for register <rec_cnt> from sample1..4
    "get_reg_scale": 0x101B,  # get read scaling for register <rec_cnt> to sample1..4
    "set_reg_scale_default": 0x101C,  # set read and write scaling of all registers to num=1, denom=1
    "filter_vfout_on": 0x101D,  # enable filtered VF_OUT into POS2 for testbox use
    "filter_vfout_off": 0x101E,  # disable filtered VF_OUT into POS2 for testbox use
    "comm_log_on": 0x101F,  # enable logging of fastmac/modbus communications into SBUF
    "comm_log_off": 0x1020,  # disable logging of fastmac/modbus communications into SBUF
    "unlock_i2tlim": 0x1021,  # remove write protect for register I2TLIM
    "enable_spi": 0x1022,  # enable SPI operation for Ethernet modules
    "meas_timeslice1": 0x1023,  # enable measurements/readout of timeslice durations BEFORE Modbus
    "meas_timeslice2": 0x1024,  # enable measurements/readout of timeslice durations AFTER Modbus
    "meas_timeslice3": 0x1025,  # enable measurements/readout of timeslice durations after eRxP
    "go_safe_reset": 0x1026,  # first enter safe mode - then save in flash and reset
    "index_homing_on": 0x1027,  # Set bit- in Reg36 CNTRL_BITS - this is to reduce number of registers in Ethernet Modbus PDO
    "index_homing_off": 0x1028,  # Clear bit- in Reg36 CNTRL_BITS
    "mactalk_9600": 0x1029,  # on-the-fly change baudrate for MacTalk
    "mactalk_19200": 0x102A,  # on-the-fly change baudrate for MacTalk
    "mactalk_38400": 0x102B,  # on-the-fly change baudrate for MacTalk
    "mactalk_57600": 0x102C,  # on-the-fly change baudrate for MacTalk
    "mactalk_115200": 0x102D,  # on-the-fly change baudrate for MacTalk
    "mactalk_230400": 0x102E,  # on-the-fly change baudrate for MacTalk
    "mactalk_444444": 0x102F,  # on-the-fly change baudrate for MacTalk
    "mactalk_1mega": 0x1030,  # on-the-fly change baudrate for MacTalk
    "pwm_sine_sweep": 0x1031,  # start and sample a PWM sweep - use POS0..3 for frequencies and amplitudes
    "mb0_rxdump_on": 0x1032,  # User debug - dump bytes received in Modbus0 to POS0..MODE3
    "mb0_rxdump_off": 0x1033,  # User debug - dump bytes received in Modbus0 to POS0..MODE3
    "uart0_log_on": 0x1034,  # enable logging of fastmac/modbus communications into SBUF
    "uart0_log_off": 0x1035,  # disable logging of fastmac/modbus communications into SBUF
    "enable_sync": 0x1036,  # enable SYNC operation for Ethernet modules (write to FPGA)
    "disable_spi": 0x1037,  # disable SPI FW operation for Ethernet modules (but keep IO1-4 routed for SPI)
    "save2flash_continue": 0x1038,  # save in flash while running with no reset afterwards
    "pwr_dump_pulse": 0x1039,  # Turn ON the power dump (int+ext) for a few ms - also if AC-sense(!)
    "wronly_cur_regs": 0x103A,  # Removes write protection for registers 144-149 - current loop coeffs
    "rw_cur_regs": 0x103B,  # Sets write protection for registers 144-149 - current loop coeffs
    "sine_mode_on": 0x103C,  # Starts motor moving short sine-waves - for development test only
    "sine_mode_off": 0x103D,  # Stops motor moving short sine-waves - for development test only
    "spi_point1": 0x103E,  # Selects in which time-slice the Ethernet<->motor comms happen
    "spi_point2": 0x103F,  # Selects in which time-slice the Ethernet<->motor comms happen
    "capture_off": 0x1040,  # Clear all captured data
    "capture_up1": 0x1041,  # Capture counter-up for data valid in buffer 1
    "capture_down1": 0x1042,  # Capture counter-down for data valid in buffer 1
    "capture_up2": 0x1043,  # Capture counter-up for data valid in buffer 2
    "capture_down2": 0x1044,  # Capture counter-down for data valid in buffer 2
    "calc_true_rms": 0x1045,  # Calculate RMS values of all active sampled data
    "snapshot_1": 0x1046,  # Start snapshot recording of 1 data sample of current and position
    "snapshot_2": 0x1047,  # Start snapshot recording of 2 data sample of current and position
    "mhm_ofscorr": 0x1048,  # Start MHM measurements for calibration
    "wiegand_test": 0x1049,  # Runs a quick test of the Wiegand sensor inputs
    "nerr_pin_on": 0x104B,  # Enable NERR pin (output)
    "nerr_pin_off": 0x104C,  # Disable NERR pin (output)
    "erase_encflash": 0x104D,  # Erase encoder flash data
    "unlock_pwr_dmp_time": 0x104E,  # Unlock power dump time in regulation for test/debug
    "unlock_pwm_freq": 0x104F,  # Unlock PWM frequency register
    "pwm_5khz": 0x1050,  # Set PWM frequency to 5kHz
    "pwm_10khz": 0x1051,  # Set PWM frequency to 10kHz
    "pwm_20khz": 0x1052,  # Set PWM frequency to 20kHz
    "long_true_rms": 0x1054,  # Calculate long-term true RMS values of all active sampled data
    "outl_enc_crc_cnt": 0x1055,  # Output encoder CRC counter for debugging
    "brake_force_ungrip": 0x1056,  # Apply brake force to release grip
    "brake_force_grip": 0x1057,  # Apply brake force to grip
    "fpga_test_vector": 0x1058,  # Execute FPGA test vectors
    "internal_use_last": 0x1063  # Reserved for internal use - always the highest value
        }

        #Reg 213 UART1_SETUP
        self.uart_setup ={
    "baudrate": (0,4),  # 0..8 => 9600, 19200, 38400, 57600, 115200, 230400, 444444, 1.000Mb, 2.000Mb
    "protocol": (4,4),  # 0=FastMac/1=Modbus/2=JvlModuleModbus/3=OMRON/4+=Reserved
    "modebits": (8,8),  # mask to combine bitsno+sync+parity+stopbits
    "bitsno": (8,2),    # 0..3 => 5..8 data bits
    "sync": (10,1),     # USART works in 0=Asynch mode 1=Synchr mode - only Asynch mode supported
    "parity": (11,3),   # 0..7 => Even/Odd/Space/Mark/None/None/MultiDrop/MultiDrop Parity (None could be 0 ?)
    "stopbits": (14,2), # 0..3 => 1/1.5/2/Reserved Stop bits
    "guardtime": (16,4),# 0..15 => extra bits between bytes (time-guard)
    "tristate": (20,1), # bit-20 enables Tx tranceiver tri-stating after any Modbus, +sometimes MacTalk, transmission has completed (DIRA signal).
    "fullduplex": (21,1),# if set, does NOT disable the UART receiver during transmission (default is to do so, to support 2-wire RS485).
    "reserved": (22,2), # - reserved for future use - (further option bits).
    "options": (24,8),  # Options depending on the protocol used. See below..
    "opt_sm": (24,2),   # For Modbus: Slave/Master selection. 0=Standard slave 1=SerialGear Slave 2=SerialGear Master, 3=RxP master
    "opt_slave": (24,1),# For Modbus: When set, motor is an Active slave that should go passive on comm time-out
    "opt_mst": (25,1),  # For Modbus: When set, motor is Master
    "opt_rxpmst": (24,2),# value to mean that embedded nanoPLC RxP is modbus master
    "opt_ms": (28,4)    # For Modbus: Timeout in MilliSeconds before COMM_ERR and slave goes passive.
    }
        
        # Reg 214 EXTENC BITS
        self.extenc_bits = {
    "nachlauf": (0,4),               # bitmask to isolate index to Px register used for nachlauf
    "nachlauf_shift": (0,0),         # not used
    "disp_startinput": (4,3),        # selects input 1..6 on B41 for the dispenser start signal
    "dispstart_edge": (7,1),         # 
    "disp_startinput_shift": 4,      # not a bitmask, direct shift value
    "disp_stopinput": (8,3),         # 
    "dispstop_edge": (11,1),         # 
    "disp_stopinput_shift": 8,       # not a bitmask, direct shift value
    "dispens_enabled": (12,1),       # when this bit is set, the extenc signal is gated
    "dispens_wait_jitter": (13,1),   # when this bit is set, FW will busy-wait (!) to reduce start/stop signal jitter
    "forlauf": (16,4),               # bitmask to isolate index to Px register used for forlauf in gear/dispenser mode
    "forlauf_shift": 16              # bit position of forlauf mask within extenc_bits
    }

        # Reg 222 IO_SETUP
        self.io_setup = {
    "iosetup_aninp": (0,4),           # 0=compatible (ANINP1 + old ANINP_OFFSET) 1=ANINP1 2=ANINP2 3=ANINP3 (from P5) etc..
    "iosetup_aninp_shift": 0          # Bitcount to shift IOSETUP_ANINP_MASK value down to bit 0
    }

        # Reg 234 RXP_SETUP
        self.rxp_setup = {
    "rxp_run_mode": (0,4),              # 0=do not run at all, 1=run one instruction every 100us - 2=run til (200?) timer ticks before end of timeslice - 3+=TBD
    "rxp_dont_start_program": 4,    # When set, prevents starting the program
    "rxp_option_a": 5,              # Other options
    "rxp_option_b": 6,              # Other options
    "rxp_option_c": 7,              # Other options
    "rxp_b41_to_rxp": 15,           # Convert B41 to virtual RxP for testing with old MacTalks
    "rxp_forced_not_used": 16       # Execute RxP for all module types (override auto detect)
    }
        
        # Reg 235 ERR_STAT_2
        self.err_stat_2_bit = 0

        # Reg 236
        self.setup_bits = {
    "pid_mode": (0,2), # PID_GENERAL_MODE 0=off, 1=on, 2=on+debug.
    "modbus_scale": 2,          # Use on-the-fly scaling of register R/W over Modbus
    "mactalk_scale": 3,         # Use on-the-fly scaling of register R/W over MacTalk
    "nanoplc_scale": 4,         # Use on-the-fly scaling of register R/W in RxP 
    "higher_max_speed": 5,      # Raises limit for speed error to 4000 RPM for MAC800 or 5000 RM for MAC400
    "pwm0_in_passive": 6,       # Keep all three PWM outputs at zero with no deadtime
    "absenc_flash_backup": 7,   # Save and restore P_IST using the absolute encoder to survive a power failure/reset
    "px_offset": 8,             # Make modbus-paired master on P4/P5 module send P_IST + POS5 instead of P_IST to slave
    "psoll_pair": 9,            # Transmit P_SOLL instead of P_IST from paired-master over Modbus
    "vsoll_pair": 10,           # Transmit V_SOLL to slaves V_SOLL from paired-master over Modbus
    "unused_2": 11,             # Unused
    "mem_read_write": 12,       # Vel6 is index and vel7 data to memory when r/w regs
    "ms1_0": 13,                # Select 1.0 ms outer cycle time rather than default 1.3 ms
    "lflash": 14,               # Override CPU type detection for large flash
    "classic_error_mask": 15,   # Use pre-v2_08 error mask
    "disable_curloop_err": 16,  # Exclude CURLOOP_ERROR from the error bits
    "vfout_passive": 17,        # Obsolete - Keep VF_OUT updated at zero in Passive mode 
    "user_aninp": 18,           # Prevent firmware from updating ANINP and remove write-protection
    "inpos_passive": 19,        # Keep INPOS bit in ERR_STAT updated at zero in Passive mode
    "clr_modechange": 20,       # Clear all outloop filter data on mode change
    "brake_in_passive": 21,     # Keep PWMs enabled at 50% in passive mode to brake the motor
    "pdtype_4x3x68_ohm": 22,    # Force system to assume this brake resistor type mounted
    "pdtype_wdmb_150_ohm": 23,  # Force system to assume this brake resistor type mounted
    "auto_start_mode": 24,      # MODE_REG = START_MODE whenever STO or AC returns
    "delayed_ac_ok": 25,        # UVhandling accepts 230Vac comes after 24V at startup
    "vsoll_hires": 26,          # V_SOLL is 1024x encoder resolution, standard=16x
    "disable_sto": 28,          # Disable STO monitor input in firmware
    "pwm_sine": 29,             # Debug function to generate measurement signals
    "flash_backup_18v": 30,         # Set threshold for position flash backup to 18V
    "ubus_compens": 30,         # Debug function to disable UBUS temperature compensation
    "debug": 31                 # General-purpose debug bit
        }

        # Reg 242 ERR_INFO
        self.err_info = {
    "late_pwm": 1,  # PWM values were delivered too late to the FPGA
    "hispeed": 2,   # Overspeed measured in OUT_PWM
    "miss_index": 3,  # Encoder count too large measured in OUT_PWM
    "hispeed_slow": 4,  # Overspeed measured in normal 1.x ms OUTLOOP
    "ia": 5,        # CHECK_IAB failed check of IA, too high/low
    "ib": 6,        # CHECK_IAB failed check of IB, too high/low
    "ic": 7,        # CHECK_IC failed check of IC, too high/low
    "icnt": 8,      # ALIM_CNT found too many limited current requests in a row
    "fpga_index": 9,  # FPGA detected an encoder index error more than N times in a row
    "adc_init": 10,  # The initial ADC conversion did not complete - HW +5V VCCAD missing?
    "prod_vers": 11,  # Presence of the 125 kHz signal does not match the BigDefEdit HW version
    "enc_over_35rpm": 12,  # Encoder velocity during startup over 35 RPM (or encoder invalid response)
    "cai_tail": 13,  # Index error detected in CALC_ALL_INNER tail
    "dma_area": 15,  # The combined size of DMA data is too large for the PMU xKB windows
    "sto_sensea": 20,  # STOA below threshold
    "sto_senseb": 21,  # STOB below threshold
    "sto_alarm": 22,  # STO ALARM pin set
    "biss": 23,      # BISS encoder error
    "productiondata": 24,  # Production data header not found
    "motortype": 25,  # Unknown motortype (RM4)
    "fpga": 26,      # FPGA failed to load
    "encoder": 27,   # Encoder initialization failed
    "invalid_enctype": 28,  # Invalid encoder type detected
    "hw_oc_latch": 29,  # Overcurrent trigger latched in hardware, powercycle to disable
    "i2c": 32,       # I2C error during startup
    "ix_offset": 33  # IX offset reached max value, probably caused by no PWM input from current sensor
        }

        self.zup2_bits = {
            "use_rec_div": 0, # bit-0 enable div-by-2 in record.s - Classic sampling - inner loop
            "pos_capture_up2": 1, # bit-1 arm trigger for position capture when ANINP2 gets above +5.00V
            "pos_capture_dn2": 2, #  bit-2 arm trigger for position capture when ANINP2 gets below +5.00V
            "edge_pos_capture": 3, # bit-3 select edge triggered position capture. Level triggered if zero
            "ifilt_fact_shift": 4, # bits [7:4] select scaling factor for CurFilter FOC coefficients
            "ifilt_fact": (4,4), # bits [7:4] for lower audible noise (for sound/film studios etc.)
            "next_to_use": 8 #  bit-8 not used yet
        }

        self.rxp_com_results = {
            "ok": 0,
            "busy": 1,
            "failed": 2
        }

        self.ePLC_cmd = {
            "nop": 0,
            "start": 1,
            "stop": 2,
            "pause": 3,
            "step": 4,
            "set_output":5,
            "set_pass": 6,
            "prepare_write": 7,
            "apply_pass": 8
        }

        self.ePLC_status = {
            "passive": 0,
            "running": 1,
            "single": 2,
            "paused": 3,
            "stack_overflow": 4,
            "program_overflow": 5,
            "invalid_cmd": 6,
            "stopped": 7,
            "com_error": 8,
            "starting_program": 9,
            "flash_error": 10,
            "flash_error_chk": 11
        }

        # I/O DEFINITIONS
        self.io_read_words = [self.registers["mode_reg"][0],
                              self.registers["p_ist"][0],
                              self.registers["v_ist"][0],
                              self.registers["vf_out"][0],
                              self.registers["error_bits"][0],
                              self.registers["pos_1"][0]]
        
        self.io_write_words = [self.registers["mode_reg"][0],
                               self.registers["p_soll"][0],
                               self.registers["v_soll"][0],
                               self.registers["t_soll"][0],
                               self.registers["pos_1"][0]]

