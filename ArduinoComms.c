import serial
class ArduinoComms:
  def __init__(port,baud):
      self.port=port

      def
      def PrintWelcome():
        ser = serial.Serial(port, baud)
        x = ser.write('SettingUp\n...\n000')
        ser.close()

      def SendData(topLine,bottomLine,LEDStatus,ser):
        ser = serial.Serial(port, baud)
        x = ser.write('SettingUp\n...\n000')
        ser.close()
