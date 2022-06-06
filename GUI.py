import PySimpleGUI as sg
import adafruit_mcp3xxx.mcp3008 as MCP
from multiprocessing import Process

from moistureSensor import MoistureSensor

sg.theme('DarkGreen')
sg.set_options(border_width=0,
               button_color=sg.COLOR_SYSTEM_DEFAULT)

recalibration_layout = [
    [sg.Button("Press when probes are in the air", size=(25, 3), font=('Arial', 15), button_color='white'), sg.Button("Press when probes are in water", size=(25, 3), font=('Arial', 15), button_color='lightblue')]
]

finished_air_layout = [
    [sg.Image('checkmark.png')]
]

finished_water_layout = [
    [sg.Image('checkmark.png')]
]

layout = [
    [sg.VPush()],
    [sg.Button("Re-Calibrate Moisture Sensors", size=(25, 3), font=('Arial', 30))],
    #[sg.Button("Restart Data Recording Software")],
    [sg.CButton("Close", button_color='red1', size=(8, 2), font=('Arial', 15))],
    [sg.Column(recalibration_layout, visible=False, key='recalibrate')],
    [sg.Column(finished_air_layout, visible=False, key='air')],
    [sg.Column(finished_water_layout, visible=False, key='water')],
    [sg.VPush()]
    
]

window = sg.Window("Vermi Compost Bin Monitoring System", layout, size=(720, 480), resizable=True, element_justification='c', finalize=True)

layout = 1

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Re-Calibrate Moisture Sensors": 
        if layout == 1:
            window['recalibrate'].update(visible=True)
            layout = 2
        else:
            window['recalibrate'].update(visible=False)
            layout = 1
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
        window['air'].update(visible=True)
        
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
        window['water'].update(visible=True)

window.close()
