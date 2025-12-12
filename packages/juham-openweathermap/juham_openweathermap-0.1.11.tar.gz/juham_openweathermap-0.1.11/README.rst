OpenWeatherMap forecast for Juham™
==================================

Description
-----------

Adds forecast support to Juham™ home automation.

.. image:: _static/images/openweathermap.png
    :alt: Solar and temperature forecasts
    :width: 640px
    :align: center

	  
Project Status
--------------

**Current State**: **Pre-Alpha (Status 2)**  

Please check out the `CHANGELOG <CHANGELOG.rst>`_ file for changes in this release.



Getting Started
---------------

### Installation

1. Install

  .. code-block:: bash

    pip install juham_openweathermap


2. Configure

  Create `OpenWeatherMap.json` configuration file in `~/.[yourapp]/config/` folder for Open Weathermap credentials.

   .. code-block:: text

    {
      "bucket": "OpenWeather",
      "appid": "[yourappid]",
      "location": "[yourlocation]",
      "url": "https://api.openweathermap.org/data/2.5/forecast",
      "update_interval": 43200
    }
