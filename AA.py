# Simulate car driving in different pavement (dry, snow, ice)
import numpy as np
import random   
random.seed(99)

def Initial():
    
    global Acc_max_dict, DesSpeed_dict

    Acc_max_dict = {'100': 8.5, '101': 3.4, '102': 1.7}  

    DesSpeed_dict = {'100': 60, '101': 42, '102': 36}

    

def Dry_pavement():
    
    if Vissim.Net.Vehicles:
        for Vehicle in Vissim.Net.Vehicles:
            Speed_cur = Vehicle.AttValue('Speed')
            if Speed_cur == 0:
                WheelSpeed = 0
            else:
                WheelSpeed = max(Speed_cur + random.gauss(0, 0.3), 0)
            Vehicle.SetAttValue('WheelSpeed', WheelSpeed)

def Change_to_dry():
    global Vehicles_prev, VehType, Acc_max, DesSpeed
    
    VehType = '100'
    Acc_max = Acc_max_dict[VehType]
    DesSpeed = DesSpeed_dict[VehType]
      
    for Vehicle in Vissim.Net.Vehicles:
        Vehicle.SetAttValue('VehType', VehType)
        Vehicle.SetAttValue('DesSpeed', DesSpeed + max(min(random.gauss(0, 2),6),-6))
    

def Change_to_snow():
    global Vehicles_prev, VehType, Acc_max, DesSpeed
    
    VehType = '101'
    Acc_max = Acc_max_dict[VehType]
    DesSpeed = DesSpeed_dict[VehType]
      
    for Vehicle in Vissim.Net.Vehicles:
        Vehicle.SetAttValue('VehType', VehType)
        Vehicle.SetAttValue('DesSpeed', DesSpeed + max(min(random.gauss(0, 2),6),-6))
    
    Vehicles_prev = Save_vehicles_data()
    
def Change_to_ice():
    global Vehicles_prev, VehType, Acc_max, DesSpeed
    
    VehType = '102'
    Acc_max = Acc_max_dict[VehType]
    DesSpeed = DesSpeed_dict[VehType]
      
    for Vehicle in Vissim.Net.Vehicles:
        Vehicle.SetAttValue('VehType', VehType)
        Vehicle.SetAttValue('DesSpeed', DesSpeed + max(min(random.gauss(0, 2),6),-6))
    
    Vehicles_prev = Save_vehicles_data()

def Save_vehicles_data():
    vehicles_prev = Vissim.Net.Vehicles.GetMultipleAttributes(('No', 'Acceleration', 'Speed', 'WheelSpeed'))
    vehicles_prev = np.asarray(vehicles_prev)
    return vehicles_prev

   

def SnowIce_pavement():
    # Vehicles_prev['No', 'Acceleration', 'Speed', 'WheelSpeed']  No null values
    
    global Vehicles_prev

    if Vissim.Net.Vehicles:    
        for Vehicle in Vissim.Net.Vehicles:
            try:
                index = np.where(Vehicles_prev[:,0] == Vehicle.AttValue('No'))[0][0]
                Speed_cur = Vehicle.AttValue('Speed')
                Acc_prev = Vehicles_prev[index, 1]

                if abs(Acc_prev) <= Acc_max:             
                    if Speed_cur == 0:
                        WheelSpeed = 0
                    else:
                        WheelSpeed = max(Speed_cur + random.gauss(0, 1), 0)               
                else:
                    Speed_prev = Vehicles_prev[index, 2]
                    WheelSpeed_prev = Vehicles_prev[index, 3]
                    WheelSpeed = min(max(WheelSpeed_prev + Acc_prev * 0.1 * 3.6, 0), 100)
                    if WheelSpeed == 0:
                        Speed_cur = 0
                    else:
                        Speed_cur = max(Speed_prev + Acc_max * 0.1 * 3.6 * np.sign(Acc_prev), 0)
                    
                Vehicle.SetAttValue('WheelSpeed', WheelSpeed)
                Vehicle.SetAttValue('Speed', Speed_cur)

                if Vehicle.AttValue('DesSpeed') > DesSpeed + 6:
                    Vehicle.SetAttValue('DesSpeed', DesSpeed + max(min(random.gauss(0, 2),6),-6))
                
            except:
                Vehicle.SetAttValue('VehType', VehType)
                Vehicle.SetAttValue('DesSpeed', DesSpeed + max(min(random.gauss(0, 2),6),-6))
                Vehicle.SetAttValue('WheelSpeed', max(Vehicle.AttValue('Speed') + random.gauss(0, 0.3), 0))
    Vehicles_prev = Save_vehicles_data()


