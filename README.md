# PC-screen-ambient-light
Python and Arduino code for my screen ambient light and PC housing LED decorations (Windows, needs changes to work on real system: Linux).
# Informations
If you want more leds, you have to change in arduino code UART buffer size, every one more leds adds 3 bytes to buffer.
Code is not pretty because I made it for myself, it wil be hard for newbies to edit something.
# Connection
- Connect arduino to USB or if you have board without UART converter then connect arduino throught UART converter to PC.
- Attach decoration LED strip (if you want) to PIN 3, I used WS2812 so I used +5V from USB.
- Attach ambient LED strip (if you want) to PIN 5, I used WS2811 so I had to take +12V from PC PSU.
- Glue ambient LED strip to you monitor. First LED is in the right bottom corner and goes to left <- then up ^, right -> and down v.
# .bat file
You can run python app simply opening the .bat file. You can also create a shortcut to this file and put it to startup.

