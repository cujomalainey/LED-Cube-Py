LED-Cube-Py
===========

A python driver for a raspberry pi powered LED cube of any size, design must be of the format where all GPIOs are wired directly to each column and GPIOs controlling grounding switches are directly wired to transistors.

NOTE: NOT RECOMMENDED DESIGN.
Due to the speed of python and the unstable voltages of the raspberry pi it does not make a good contendor driving an LED cube. I attempted to implement Bit Angle Modulation (BAM) to allowing dimming of the LEDs and python is simply not fast enough. I have not attempted this with a PI 2 but I would guess the results would be the same considering the tests were only done a 4x4x4 cube. I recommend a dedicated AVR for powering you cube. If you need wireless or internet access I recommend checking out my future designs of this project which will include a raspberry pi controller but controller the AVR driver of the cube via Xbee.

