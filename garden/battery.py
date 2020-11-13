from machine import ADC

class Battery:
    def __init__(self):
        self.adc = ADC(0)
        
    def getADCReading(self):
        return self.adc.read()
        
    def getVoltage(self):
        return self.adc.read()/1024/10*57
