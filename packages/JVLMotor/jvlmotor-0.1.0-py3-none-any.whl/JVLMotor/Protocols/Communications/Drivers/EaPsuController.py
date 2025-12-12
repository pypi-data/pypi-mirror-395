from ea_psu_controller import PsuEA
import time
class EaPsuController(PsuEA):
    def __init__(self, comport=None, sn=None, desi=None, baudrate=115200,
                 v_1 = 24, i_1 = 1, v_2 = 24, i_2 = 1,
                 ovp_1 = 50, ocp_1 = 2, ovp_2 = 50, ocp_2 = 2):
        super().__init__(comport, sn, desi, baudrate)
        self.v_1 = v_1
        self.v_2 = v_2
        self.i_1 = i_1
        self.i_2 = i_2
        self.ovp_1 = ovp_1
        self.ovp_2 = ovp_2
        self.ocp_1 = ocp_1
        self.ocp_2 = ocp_2

    def setupPsu(self):
        
        self.set_ovp(self.ovp_1,0)
        self.set_ocp(self.ocp_1,0)

        self.set_ovp(self.ovp_2,1)
        self.set_ocp(self.ocp_2,1)

        self.set_voltage(self.v_1,0)
        self.set_current(self.i_1,0)

        self.set_voltage(self.v_2,1)
        self.set_current(self.i_2,1)

        self.output_on(0)
        self.output_on(1)

        time.sleep(6)


    def setupOutput(self,output_num,voltage=24,current=1,
                    ovp=50,ocp=2):
        self.set_ovp(ovp,output_num)
        self.set_ocp(ocp,output_num)
        self.set_voltage(voltage,output_num)
        self.set_current(current,output_num)
        self.output_on(output_num)

        time.sleep(5)

    def releasePsuControl(self):
        self.remote_off(0)
        self.remote_off(1)
        self.close(remote=True,output=False)

    def releaseControl(self,output_num):
        self.remote_off(output_num)
        #time.sleep(1)
        #self.close(remote=True,output=False,output_num=output_num)

    def closePsu(self):
        self.closeOutput(0)
        self.closeOutput(1)
    
    def offOutput(self):
        self.output_off(0)
        self.output_off(1)
        self.remote_off(0)
        self.remote_off(1)

    def closeOutput(self,output_num):
        self.output_off(output_num)
        self.remote_off(output_num)
        time.sleep(1)
        self.close(remote=True,output=True,output_num=output_num)

