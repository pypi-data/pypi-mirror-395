Changelog
=========



[0.1.15] - December 8, 2025
---------------------------

- Bug in **ShellyMotion** on_message method fixed that caused it to ignore messages due to incorrect topic comparison.
- Potential bug in **ShellyPRO3EM** on_message method fixed, logging improved.


[0.1.14] - December 3, 2025
---------------------------

- Support for 'NotifyFullStatus' mqtt events
- Dependencies updated
- Obsolete make.bat and clean.py files removed


[0.1.11] - November 26, 2025
----------------------------

- **MQTT prefix support** added for `PowerMeter`, `ShellyMotion`, `Shelly1G3`, `ShellyPlus1`, and `ShellyPro3`.  
  This enables reliable instantiation of multiple devices of the same type within one home automation setup.
- All Shelly device classes now use a unified `shelly_device_topic` derived from the MQTT prefix and base topic.
- Improved internal handling of MQTT topic construction, eliminating prefix duplication issues and ensuring consistent subscription behavior.
- Updated dependency requirement: `juham-core >= 0.2.2`.
- Improved warning logs: unrecognized or malformed message structures now include device name and resolved device topic for easier debugging.
- `ShellyDS18B20`, `ShellyDHT22`, and `ShellyMotion` now correctly subscribe using their full MQTT-prefixed device topic.
- Resolved issues where tests expected single-prefix topics but code produced double-prefix topics.


[0.1.4] - November 25, 2025
---------------------------

- Bug in comparing msg.topic in **ShellyDS18B20** fixed.


[0.1.3] - November 8, 2025
--------------------------

- *ShellyDHT22* handles 'sys' message silently.
- *test_shellymotion.py* unit test added.



[0.1.0] - April 17, 2025
------------------------

- Updated to comply with the new SPDX expression for packaging standards
- Development Status elevated to Alpha
  

[0.0.9] - April 08, 2025
------------------------

- Fixed random crashes in the following shellydht22 class due to exception from float(humidity).
  
   .. code-block:: python

      sensor_id = key.split(":")[1]
      humidity = float(value[unit]) # sometimes None


[0.0.6] - March 16, 2025
------------------------

- Two new unit test classes added


[0.0.5] - January 19, 2025
--------------------------

- Documentation refactored

- GitLab migration


[0.0.1] - January 19, 2025
--------------------------

- **First release:** 

