# F1 23 DigiFlags

Displays flags from the F1 23 game on [Pimoroni Cosmic Unicorn](https://shop.pimoroni.com/products/space-unicorns?variant=40842626596947)

> ⚠️ **This is incomplete and has major issues!** There are currently two different modes with their own issues, read about them in the [Control](#control) section.

## Usage

### Configure

To configure the application, create a copy of `config.example.json` and name it `config.json`. Then, update the WiFi credentials inside the file.

### Deploy to the Cosmic Unicorn

This part is probably the most tricky one, and will require some trial and error. You need to move every python file to the raspberry pi.

I've had success with use [mpbridge](https://github.com/AmirHmZz/mpbridge)

After you've moved the files, the `main.py` file should execute automatically on reboot.

### Control

You can adjust the brightness with the "LUX" buttons, and set the display to sleep with the "Zzz" button.

To switch mode press any of the "Program" buttons.

#### A - Async flag mode

This mode handles the connection and rendering asynchronously, which means smoother animations, that don't get stuck at specific frames. The tradeoff is that it drops a lot of events, which eg. causes the "lights outs" effect to lag and stutter.

#### B - Legacy flag mode

This mode handles the connection and rendering synchronously, which means that it doesn't drop any events, but the animations are not as smooth, and pauses if the connection (eg. the game) pauses.

It's also not possible to control anything while this mode is running, so you need to reset the device to switch back to the menu.

#### C - Demo mode

Cycle through all the flags, and display them for 5 seconds each.

#### D - Menu mode

Returns to the menu.

