# KurodenwaPi
Bluetooth-HFP client with Kurodenwa and Raspberry-Pi written by Python. Kurodenwa means a rotary dial telephone in Japanese.  

## Hardware Requirement
* Raspberry Pi 1 B+ or 2 or 3
* USB Bluetooth Dongle (except for RPi-3)
* USB Audio Cable
* and, your handmade circuit, see circuit.png

## Need more files
* Sound Files (not include this repository)
  * sound/tone.wav     : 400Hz tone sound
  * sound/busy.wav     : Busy Tone
  * sound/ringback.wav : Ringback Tone

  * (Optional)
  sound/bunmeido.wav   : any wav file (^-^)

* Library
  * pigpio  
    GPIO library and daemon  
    http://abyz.me.uk/rpi/pigpio/  
  * AquesTalkPi  
    Japanese language speech synthesis software  
    https://www.a-quest.com/products/aquestalkpi.html  
    install at /home/pi/aquestalkpi/  

## Usage
`$ git clone https://github.com/tokieng/KurodenwaPi.git`  
`$ cd KurodenwaPi`  
`$ ./client`

## License
MIT License

## Copyright
2017 Yoshinori Tokimoto (tokieng)
