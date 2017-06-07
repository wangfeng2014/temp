#!/bin/bash
#
# this file is use to update application script from version 1.26.x to 1.26.8
#
echo upate begin 
echo ... ...
sudo cp ./temp.py ./sensorDev.py /home/pi/sensor
sudo cp ./default /etc/nginx/sites-available/

sudo sed -i '2 s/bxw2341150184.my3w.com/61.155.88.154/g' /home/pi/sensor/config.ini
sudo sed -i '3 s/80/1573/g' /home/pi/sensor/config.ini
sudo sed -i 's/1.26.*/1.26.8/g' /home/pi/sensor/config.ini


echo update end.
