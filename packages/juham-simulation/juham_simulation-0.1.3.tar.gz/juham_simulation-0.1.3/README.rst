Simulation plugin for Juham™
============================

Overview
--------
This package provides simulation classes for water and power meters. 
It is designed for testing and development of IoT applications that use
MQTT-based sensors. The simulations generate realistic, time-based 
data that can be published to a broker without requiring physical devices.


WaterMeterSim
-------------

**Description:** Simulates a water meter sensor.  
**Functionality:**
- Generates water consumption readings (`active_liter_lpm` and cumulative `total_liter`).
- Publishes readings to a configurable MQTT topic at a specified interval.
- Supports integration into threaded applications.

  
PowerMeterSim
-------------
**Description:** Simulates a power/energy meter sensor.  
**Functionality:**
- Generates active power readings for three phases and total consumption.
- Publishes readings to a configurable MQTT topic at a specified interval.
- Supports integration into threaded applications.


Installation
------------

1. Install 

   .. code-block:: bash

      pip install juham-simulation

      
2. Configure

To configure edit the `*.json` configuration files to match your network and
desired reading frequency in seconds.

   .. code-block:: json

      {
	"update_interval": 60
      }

