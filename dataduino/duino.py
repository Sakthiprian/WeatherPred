import serial

class duinodata:
    def __init__(self, path: str):
        self.ser = serial.Serial(path, 9600)
        self.label = ('temperature', 'humidity', 'light')

    def read(self):
        self.ser.write(b'1')
        return dict(zip(self.label, [float(i) for i in self.ser.readline().decode('utf-8').strip().split(':')]))
