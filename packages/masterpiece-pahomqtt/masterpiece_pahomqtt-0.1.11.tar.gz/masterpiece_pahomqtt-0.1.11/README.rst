Paho MQTT Broker Plugin for MasterPiece
=======================================

Plugs in  MQTT broker functionality to `MasterPiece` applications.

**Note:** This is an alpha release; do not use it for anything critical at this stage.


Usage
-----

To install the module:

.. code-block:: bash

  pip install masterpiece-pahomqtt

Once installed, you can create `~/.yourapp/config/PahoMqtt.json` configuration file to specify
the server, port and other attributes Paho MQTT broker needs to run.

.. code-block:: text

  {"host": "your host",
   "port": 1883,
  }


To import and instantiate PahoMqtt for use:

.. code-block:: python

  from masterpiece_pahomqtt import PahoMqtt

  mqtt = PahoMqtt()


An example to write and read data:

.. code-block:: python

    mqtt.subscribe("your/topic")
    mqtt.publish("your/topic", your_msg)


Note
----

The `masterpiece_pahomqtt.PahoMqtt` class is an implementation of the abstract `masterpiece.mqtt.Mqtt` 
base class. By using the Mqtt interface your application remain implementation-independent.



License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.
