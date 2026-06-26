# micro:bit Getting Started

Notes and setup for developing with a BBC micro:bit connected over USB.

## What you need

- BBC micro:bit (v1 or v2)
- USB micro-B cable
- A code editor: [MakeCode](https://makecode.microbit.org/) (block/JS, browser-based) or Python via [Mu Editor](https://codewith.mu/) / `uflash`

## Connection overview

```mermaid
flowchart LR
    PC[Computer] -- USB cable --> MB[micro:bit]
    MB -- mass storage device --> PC
    PC -- drag & drop .hex file --> MB
    MB -- runs program --> LEDs[5x5 LED matrix]
    MB --> Buttons[Buttons A / B]
    MB --> Sensors[Accelerometer / Compass / Temp]
    MB --> Radio[Radio / Bluetooth]
```

When plugged in, the micro:bit shows up as a USB mass-storage drive named `MICROBIT`. Flashing a program means copying a `.hex` file onto that drive.

## Flashing workflow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Editor as MakeCode / Python Editor
    participant USB as USB Drive (MICROBIT)
    participant Board as micro:bit

    Dev->>Editor: Write/edit code
    Editor->>Editor: Compile to .hex
    Dev->>USB: Drag & drop .hex (or "Download" + flash)
    USB->>Board: Copy firmware
    Board->>Board: Auto-reset and flash
    Board->>Board: Run new program
```

## Verify the connection

```bash
# macOS: confirm the board is mounted
ls /Volumes | grep -i microbit

# Check serial device (for Python REPL / serial output)
ls /dev/tty.usbmodem*
```

## Programming options

```mermaid
flowchart TD
    Start([Start]) --> Choice{Choose language}
    Choice -->|Blocks / JavaScript| MakeCode[makecode.microbit.org]
    Choice -->|Python| Mu[Mu Editor or Thonny]
    Choice -->|C++| PlatformIO[PlatformIO / Arduino]

    MakeCode --> Compile1[Compile to .hex in browser]
    Mu --> Compile2[Flash via uflash / Mu]
    PlatformIO --> Compile3[Build & upload via CLI]

    Compile1 --> Flash[Copy/flash to MICROBIT drive]
    Compile2 --> Flash
    Compile3 --> Flash
    Flash --> Run[Program runs on board]
```

### Python quick start

```bash
pip install uflash
uflash my_script.py
```

```python
# my_script.py
from microbit import *

while True:
    display.scroll("Hello!")
    sleep(1000)
```

## More examples

Each example below is a standalone file in this repo. Flash one with:

```bash
uflash <file>.py
```

| File | Description |
| --- | --- |
| [my_script.py](my_script.py) | Minimal "Hello!" scroll on the LED matrix |
| [buttons.py](buttons.py) | Show a happy/sad face on button A / B |
| [accelerometer.py](accelerometer.py) | Shake gesture shows a heart |
| [temperature.py](temperature.py) | Print onboard temperature over serial |
| [radio_sender.py](radio_sender.py) | Send `"ping"` on button A press |
| [radio_receiver.py](radio_receiver.py) | Receive `"ping"` and show a checkmark |

### Temperature reading over serial

Read the output with:

```bash
screen /dev/tty.usbmodem* 115200
```

### Radio between two micro:bits

Flash [radio_sender.py](radio_sender.py) to one board and [radio_receiver.py](radio_receiver.py) to another.

```mermaid
sequenceDiagram
    participant A as micro:bit A (sender)
    participant B as micro:bit B (receiver)

    A->>A: radio.on()
    B->>B: radio.on()
    A->>B: radio.send("ping")
    B->>B: radio.receive() -> "ping"
    B->>B: display.show(Image.YES)
```

### MakeCode equivalent (JavaScript blocks export)

```javascript
input.onButtonPressed(Button.A, function () {
    basic.showIcon(IconNames.Happy)
})
input.onGesture(Gesture.Shake, function () {
    basic.showIcon(IconNames.Heart)
})
```

## AI on the micro:bit

[micro:bit CreateAI](https://createai.microbit.org/) lets you train a machine learning model from the board's built-in accelerometer data (x/y/z movement), then use it in MakeCode via auto-generated ML blocks. No coding is needed to train the model — you record example movements ("actions"), label them, and CreateAI builds the model for you.

### Requirements

- **micro:bit V2** (V1 can record data but cannot run a trained model on-device)
- Chrome or Edge browser (Chromebooks supported); iPads/iPhones are **not** supported
- micro:bit connected via **Bluetooth or radio link** (not just plain USB) for live data collection
- USB cable, and a battery pack or wearable holder if collecting motion data while moving around

### Workflow

```mermaid
flowchart LR
    Connect[Connect micro:bit V2<br/>via Bluetooth/radio] --> Record[Record movement samples<br/>1s per sample, 3+ per action]
    Record --> Clean[Clean data:<br/>remove outlier samples]
    Clean --> Train[Train model in CreateAI]
    Train --> Test[Test live: action,<br/>certainty %, recognition point]
    Test --> Refine{Accurate enough?}
    Refine -->|No| Record
    Refine -->|Yes| Export[Export as .hex<br/>data + model + code]
    Export --> MakeCode[Edit in MakeCode<br/>with ML blocks]
    MakeCode --> Flash[Download to micro:bit V2]
```

### Training data tips

- Use at least 2 actions, 3+ samples each — more samples generally improve accuracy
- Pick actions with obvious differences (e.g. clapping vs. waving), and include a "still"/"other" action to catch non-target movement
- Keep orientation/position consistent across samples (or vary deliberately if you want the model to generalize)
- Collect samples from multiple people if the model needs to work for everyone
- Good samples look like similar "wavy lines" on the data graph — flat or erratic samples are outliers to remove

### MakeCode ML blocks

CreateAI generates blocks based on the action names you trained, roughly:

```javascript
ml.onStart(ml.event.Wave, function () {
    // runs when "Wave" action starts
})
ml.onStop(ml.event.Wave, function () {
    // runs when "Wave" action stops
})
if (ml.isDetected(ml.event.Wave)) {
    // true while "Wave" is currently detected
}
ml.certainty(ml.event.Wave) // 0-100 confidence value
```

### Example: AI light switch

Train a model on a "clap" movement (the snap motion of clapping, captured by the accelerometer) vs. "still", then use the exported block in MakeCode:

```javascript
ml.onStart(ml.event.Clap, function () {
    led.toggle(0, 0) // simplified: toggle an LED/light on clap
})
```

### Example: AI sports data logger

Train gestures for `Running`, `Walking`, and `Still`, then log how long each one is detected:

```javascript
ml.onStart(ml.event.Running, function () {
    datalogger.log(datalogger.createCV("activity", "running"))
})
ml.onStart(ml.event.Walking, function () {
    datalogger.log(datalogger.createCV("activity", "walking"))
})
ml.onStart(ml.event.Still, function () {
    datalogger.log(datalogger.createCV("activity", "still"))
})
```

### Example: AI storytelling friend

Train gestures (e.g. `Wave`, `Nod`, `Spin`) and map each to a different story beat or sound, useful as a beginner-friendly intro to ML concepts:

```javascript
ml.onStart(ml.event.Wave, function () {
    music.playMelody("C E G", 120)
    basic.showIcon(IconNames.Happy)
})
ml.onStart(ml.event.Spin, function () {
    basic.showIcon(IconNames.Surprised)
})
```

> These `ml.*` blocks are generated automatically by CreateAI based on the action names you train — the exact block names match whatever you call your actions in CreateAI.

- micro:bit CreateAI: https://createai.microbit.org/
- AI projects overview: https://microbit.org/ai/
- CreateAI user guide: https://microbit.org/get-started/user-guide/microbit-createai/

## Useful links

- MakeCode editor: https://makecode.microbit.org/
- micro:bit Python docs: https://microbit-micropython.readthedocs.io/
- Hardware reference: https://tech.microbit.org/hardware/
