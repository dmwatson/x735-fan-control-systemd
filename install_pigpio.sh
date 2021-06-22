# Install pigpio
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make && sudo make install
sudo cp ./util/pigpiod.service /etc/systemd/system/pigpiod.service
sudo chown root:root /etc/systemd/system/pigpiod.service
sudo systemctl enable pigpiod 
sudo systemctl daemon-reload 
sudo systemctl start pigpiod 
printf "pigpiod installed" 