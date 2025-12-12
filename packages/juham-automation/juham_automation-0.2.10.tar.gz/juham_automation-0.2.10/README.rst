Welcome to Juham™ - Juha's Ultimate Home Automation Masterpiece
===============================================================

Project Description
-------------------

Beyond its super-cool name, this package provides essential home automation building blocks that address most common needs.

It consists of two main sub-modules:

``automation``:

This folder contains automation classes that listen to Juham™ MQTT topics and control various home automation tasks.

- **watercirculator**: Automates a water circulator pump based on hot water temperature and motion detection.
- **heatingoptimizer**: Controls hot water radiators based on temperature sensors and electricity price data.
- **energycostcalculator**: Monitors power consumption and electricity prices, and computes the energy balance in euros.
- **energybalancer**: Handles real-time energy balancing and net billing.

``ts``:

This folder contains time series recorders that listen for Juham™ topics and store the data in a time series database for later inspection.

- **electricityprice_ts** : publishes electricity prices to timeseries database.
- **energybalancer_ts**: for monitoring the operation of energy balancer.
- **energycostcalculator_ts**: publishes actualized energy prices per hour and per day.
- **forecast_ts**: publishes the forecast datat to timeseries database.
- **log_ts**: Writes log events to timeseries datbase.
- **powerplan_ts**: publishes power plan data to timeseries database, when relays are planned to be switched on/off.
- **powermeter_ts**: publishes powermeter data to timeseries database.


Project Status
--------------

**Current State**: **Beta (Status 4)**

All classes have been tested to some extent, and no known bugs have been reported. 


Project Links
-------------

- **Source code:** https://gitlab.com/juham/juham/juham-automation
- **Issue tracker:** https://gitlab.com/juham/juham/juham-automation/-/issues
- **Documentation:** https://juham-automation-c6383e.gitlab.io
- **PyPI page:** https://pypi.org/project/juham-automation

  

Features
--------

**HeatingAutomater** listens to the power meter to compute the net energy balance.

  .. image:: _static/images/juham_powermeter.png
     :alt: Powermeter
     :width: 400px

  Powermeter is needed to measure the real-time energy consumption


**Energy Revenue** is computed based on the electricity price and transmission costs. This is the total cost one has to pay for consuming energy.
  
  .. image:: _static/images/juham_energyrevenue.png
     :alt: Energy Revenue
     :width: 400px

  Energy revenue per hour and per day


**Real-time temperature** trends monitored by the **Shelly Plus Add-on** and **DS18B20** sensors
  
  .. image:: _static/images/juham_boilertemperatures.png
     :alt: Energy Revenue
     :width: 400px

  Temperature time series.


**Real-time humidity** trends monitored by the **Shelly Plus Add-on** and **DHT22** sensors
  
  .. image:: _static/images/juham_humiditysensors.png
     :alt: Energy Revenue
     :width: 400px

  Relative humidity time series.


  
**Utilization Optimization Index**: The Utilization Optimization Index predicts the optimal hours for energy consumption by factoring in electricity prices, temperature, and forecasts for wind and solar energy. It identifies the best times to activate heating systems. The cheapest hours within the current period may be skipped if the solar forecast predicts free electricity in the next period.period.

  .. image:: _static/images/juham_uoi.png
     :alt: Power Plan
     :width: 400px

  UOI cast for heating the primary and sun pre-heating boilers for two types of solar panels and boilers: electric-based panels and solar thermal panels, which use water circulation. The primary one is electrically heated, while the secondary ‘pre-heating’ boiler is heated by the hot water from the solar thermal panels, or by electricity when there's a positive energy balance.


**Power Plan** is computed for the next 12 hours based on the electricity price and solar energy forecast. If no solar energy is available, the power plan determines power consumption, e.g., when the hot water radiators are enabled.

  .. image:: _static/images/juham_powerplan.png
     :alt: Power Plan
     :width: 400px

  Powerplan optimizing consumers to use the cheapest hours


**Energy Balancer**: When the energy balance is positive (e.g., when solar panels produce more energy than is currently being consumed), the energy balancer is activated. It monitors the energy balance in 15-minute (or one-hour) intervals and computes when a consumer with a specific power demand should be activated to consume all the energy produced so far.

  .. image:: _static/images/juham_automation_energybalancer.png
     :alt: Energy Balancer
     :width: 400px

  Energy balancer activating consumers based on the actual real-time net energy


**Power Diagnosis**: All controlled relays are monitored to ensure their correct operation. This ensures that relays are enabled according to the power plan and energy balancer commands.

  .. image:: _static/images/juham_automation_relays.png
     :alt: Relays
     :width: 400px

  The operation of the relays for diagnosis.


Installing
----------

Juham™ ships with a minimal yet fully functional home automation application that can be found in the **examples** folder.
It creates a **PowerMeterSimulator** and **ShellyMotionSimulator** objets to generate simulated motion sensor and power meter readings.
Later, you can replace it with your actual power meter, as well as plug in other input sensors to read and relays to control.

1. Set up a Mosquitto MQTT broker service. For more information read the manuals.

   .. code-block:: bash

      sudo apt install mosquitto mosquitto-clients

2. Configure Juham to talk to Mosquitto.

   In ``PahoMqtt.json``:

   .. code-block:: json

      {"paho_version" : 2}

   In ``Juham.json``:

   .. code-block:: json

      {"mqtt_class_id": "PahoMqtt", "mqtt_root_topic": "myapp", "mqtt_host": "localhost", "mqtt_port": 1883}

   In ``Timeseries.json``:

   .. code-block:: json

      {
         "token": "your-influx-token",
         "org": "your-organization",
         "host": "https://us-east-1-1.aws.cloud2.influxdata.com",
         "database": "your-database"
      }

3. In the ``juham/examples`` folder, run:

   .. code-block:: bash

      python3 myapp.py

The application will start and time series data will show up in your InfluxDB database,
which you can then visualize with tools such as Grafana.
