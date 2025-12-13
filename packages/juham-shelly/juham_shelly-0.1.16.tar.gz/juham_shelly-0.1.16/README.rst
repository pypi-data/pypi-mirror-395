Shelly IoT plugin plugin for Juham™
===================================

Description
-----------

**Note:** this module is under construction. Do not try to use it for anything serious at this stage.

The plugin brings support of various Shelly devices into JuhaM:

* Shelly1G3
* Shelly Plus1
* ShellyPro3
* ShellyPro3Em energy meter
* Shelly Motion sensor

  
All shelly devices interact with JuhaM via MQTT.

.. image:: _static/images/shellyplus1_addon_ds18B20.png
   :alt: Shellyplus1 with addon and DS18B20 temperature sensors
   :width: 640px
   :align: center  

.. image:: _static/images/shellypro3em.png
   :alt: Shelly Pro3EM powermeter
   :width: 640px
   :align: center  

.. image:: _static/images/shellyplus1_addon.png
   :alt: Shelly temperature and humidity sensors
   :width: 640px
   :align: center  



Getting Started
---------------

### Installation

1. Install 

   .. code-block:: bash

      pip install juham-shelly


2. Configure

To adjust update interval and other attributes edit `Shelly*.json` configuration files.

