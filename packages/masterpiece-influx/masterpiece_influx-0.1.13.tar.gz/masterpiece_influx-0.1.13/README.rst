InfluxDB V3 Plugin for MasterPiece
==================================

Adds InfluxDB V3 timeseries recording functionality to `MasterPiece` framework.


Usage
-----

Pre-requisities:

- Create Influx cloud account, or install local Influx instance. Please consult the Influx site for
  more information on this.


To install the 'masterpiece_influx' plugin:

.. code-block:: bash

  pip install masterpiece-influx

Once installed, you can create `~/.yourapp/config/Influx.json` configuration file to specify
information needed for reading and writing time series data to your Influx database. 

.. code-block:: text

  {
    "token": "your token",
    "org": "your organization",
    "host": "https://eu-central-1-1.aws.cloud2.influxdata.com",
    "database": "your database"
  }


To import and instantiate Influx database for use:

.. code-block:: python

  from masterpiece_influx import Influx

  db = Influx()


An example to write and read data:

.. code-block:: python


  db.write_dict(name="temperature", tags={"sensor": "A1"}, fields={"value": 23.4}, ts="2024-12-14T12:00:00Z")
  data = db.read_dict(measurement="temperature", start_time="2024-12-01T00:00:00Z")


Note
----

The `masterpiece_influx.Influx` class is an implementation of the abstract `masterpiece.TimeSeries` 
base class,  designed for reading and writing time series data.
The TimeSeries interface allows  all time series operations  in your application to remain 
implementation-independent. 



License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.
