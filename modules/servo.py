import Adafruit_PCA9685

class ServoMotor:

    def __init__(self, Channel, ZeroOffset):
        self.mChannel = Channel
        self.m_ZeroOffset = ZeroOffset

        #initialize PCA9685
        self.mPwm = Adafruit_PCA9685.PCA9685(address=0x40)
        self.mPwm.set_pwm_freq(60) # 60Hz

    def setAngle(self, angle):
        pulse = int((650-150)*angle/180+150+self.m_ZeroOffset)
        self.mPwm.set_pwm(self.mChannel, 0, pulse)

    def cleanup(self):
        self.setAngle(10)

if __name__ == '__main__':
    servoMotor = ServoMotor(Channel=3, ZeroOffset=0)
    servoMotor.setAngle(0)
