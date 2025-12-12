Example usage
=============

Example code for reading sensor data and printing the values. The raw values get translated to
calibrated values using the Touchlab library. You have to provide a calibration file for this
to work. If you omit the calibration file only raw values will be printed.

.. literalinclude:: ../examples/example.py

The following code will not connect to the Touchlab device, but it will translate raw data
provided by user into calibrated values using the Touchlab library. You have to provide a
calibration file for this to work. The calibration requires the model to be biased. We do this by
calling the zeroing function before translating the data. You have to choose one or more samples
that represent sensor values without any load.

.. literalinclude:: ../examples/example_translate.py
