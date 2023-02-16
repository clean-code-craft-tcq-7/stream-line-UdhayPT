package service;

import java.util.Random;

import model.BatteryParameters;

public class BatterySender {
	public static void main(String[] args) {
		for(int i=1;i<50;i++) {
	        BatteryParameters parameters = BatterySender.generateStreamData();
	        BatterySender.sendStreamData(parameters);
		 }
	}

	public static void sendStreamData(BatteryParameters parameters) {
		System.out.println("Sending Battery Stream line parameters, BatteryLevel: " + parameters.getBatteryLevel() + "%, " + "Charging Current: " + parameters.getChargingCurrent() + " A");
	}

	public static BatteryParameters generateStreamData() {
		Random random = new Random();
	    float batteryLevel = random.nextFloat() * 100.0f;
	    float chargingCurrent = random.nextFloat() * 5.0f;
	    return new BatteryParameters(batteryLevel, chargingCurrent);
	}
}
