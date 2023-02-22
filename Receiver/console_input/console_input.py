import random

def create_sender_console_output():
    for i in range(50):
        BatteryLevel = format(random.randint(0,100)/100 + random.randint(0,100), ".2f")
        ChargingCurrent = format(random.randint(0,100)/100 + random.randint(0,5), ".2f")
        print("Sending Battery Stream line parameters, BatteryLevel: {}%, Charging Current: {} A".format(BatteryLevel, ChargingCurrent))

if __name__ == "__main__":
    create_sender_console_output()
