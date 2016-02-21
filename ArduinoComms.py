import serial
class ArduinoComms2:
  def __init__(self,port,baud):
      self.port=port
      self.baud=baud
      self.ser = serial.Serial(port, baud)

  def SendData(self,topLine,bottomLine,LEDStatus):
    x = self.ser.write(topLine+'|'+bottomLine+'|'+LEDStatus+'|')

  def ReadData(self):
    legalChars = ["1","2","3","4","5"]
    self.ser.flushInput()
    x=self.ser.read(1)
    self.ser.flushInput()
    if (x in legalChars):
      return int(x)
    return -1
