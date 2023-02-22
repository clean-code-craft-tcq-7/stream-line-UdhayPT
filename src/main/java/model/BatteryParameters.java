package model;

public class BatteryParameters {
	private double batteryLevel;
    private double chargingCurrent;

    public BatteryParameters(double batteryLevel, double chargingCurrent) {
        this.batteryLevel = batteryLevel;
        this.chargingCurrent = chargingCurrent;
    }

    public double getBatteryLevel() {
        return batteryLevel;
    }

    public double getChargingCurrent() {
        return chargingCurrent;
    }
}
