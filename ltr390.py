from datetime import datetime
from digitalio import DigitalInOut
import adafruit_ltr390
from adafruit_ltr390 import Gain,Resolution
import board
import busio
from time import sleep

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_ltr390.LTR390(i2c)
sensor.resolution = Resolution.RESOLUTION_20BIT
sensor.gain = Gain.GAIN_6X

def messure():
	data = {"uv": None, "lux": None}
	if sensor is None:
		print("Smth went wrong")
		return None
	try:
		uvi = sensor.uvi
		lux = sensor.lux
		data["uv"] = uvi
		data["lux"] = lux
	except Exception as e:
		print(e)
		return None
	return data

def main():
    while True:
        try:
            now = datetime.now()
            if now.minute > 37:
                break
            data = messure()
            with open("research/messurments.txt", "a") as file:
                if data:
                    file.write(f"{datetime.now().isoformat()} {data['uv']} {data['lux']}\n")
                else:
                    file.write(f"{datetime.now().isoformat()} Some error occured\n")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()