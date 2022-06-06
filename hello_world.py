import PySimpleGUI as sg
import adafruit_mcp3xxx.mcp3008 as MCP
from multiprocessing import Process

from moistureSensor import MoistureSensor


recalibration_layout = [
	[sg.Button("Press when probes are in the air")],
	[sg.Button("Press when probes are in water")]
]
layout = [
	[sg.Button("Re-Calibrate Moisture Sensors new")],
	[sg.Button("Restart Data Recording Software")],
	[sg.Column(recalibration_layout, visible=False, key='recalibrate')]
]

window = sg.Window("Vermi Compost Bin Monitoring System", layout, size = (800, 600))


layout = 1

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		break
	if event == "Re-Calibrate Moisture Sensors new": 
		if layout == 1:
			window['recalibrate'].update(visible=True)
			layout = 2
			
			
		else:
			window[f'recalibrate'].update(visible=False)
			layout = 1
		
		# exec(open("other.py").read())	
	if event == "Press when probes are in the air":
		# Calibrate the sensors
		moisture_one = MoistureSensor(MCP.P0)
		moisture_two = MoistureSensor(MCP.P1)
		moisture_three = MoistureSensor(MCP.P3)

		p1 = Process(target=moisture_one.calibrateAir())
		p1.start()
		p2 = Process(target=moisture_two.calibrateAir())
		p2.start()
		p3 = Process(target=moisture_three.calibrateAir())
		p3.start()
	
		p1.join()
		p2.join()
		p3.join()
	if event == "Press when probes are in water":
		# Calibrate the sensors
		moisture_one = MoistureSensor(MCP.P0)
		moisture_two = MoistureSensor(MCP.P1)
		moisture_three = MoistureSensor(MCP.P3)

		p1 = Process(target=moisture_one.calibrateWater())
		p1.start()
		p2 = Process(target=moisture_two.calibrateWater())
		p2.start()
		p3 = Process(target=moisture_three.calibrateWater())
		p3.start()
	
		p1.join()
		p2.join()
		p3.join()

window.close()
