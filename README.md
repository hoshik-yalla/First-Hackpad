# ⌨️ First-Hackpad: A 3-Key Mechanical Macro Pad

Welcome to **First-Hackpad**, a compact, custom-designed three-key mechanical macro pad built around the powerful **Seeed Studio XIAO RP2040** microcontroller. This project serves as an introductory hardware design and firmware implementation model, bridging the gap between PCB schematics, physical layouts, and CircuitPython scripting.

---

## 🌟 Key Features

*   **Microcontroller:** Powered by the dual-core ARM Cortex-M0+ Seeed Studio XIAO RP2040.
*   **Mechanical Switches:** Features 3 hot-swappable MX-compatible mechanical key switches.
*   **CircuitPython Firmware:** Rapid prototyping and easy customization with built-in USB HID support.
*   **Dynamic RGB Feedback:** On-board NeoPixel RGB LED indicator changes color to reflect active hotkey presses and idle states.
*   **Production-Ready PCB:** Complete KiCad 6+ schematic and layout files ready for fabrication.

---

## 🗺️ Pin Connection & Layout Mapping

The switches are wired directly to the XIAO RP2040 using internal pull-up resistors (active-low configuration).

| Switch Reference | XIAO RP2040 Pin | Net / Function | Default Action (CircuitPython) | LED Feedback Color |
| :---: | :---: | :---: | :---: | :---: |
| **SW1** | `D10` (GP4) | Key 1 | `Ctrl + C` (Copy) | 🌸 Pink / Magenta |
| **SW2** | `D9` (GP3) | Key 2 | `Ctrl + V` (Paste) | 🍃 Mint Green |
| **SW3** | `D8` (GP2) | Key 3 | `Ctrl + Z` (Undo) | 🌊 Cyan / Blue |

---

## 🛠️ Hardware Design

All design files are located in the `pcb_design-1/` directory. Created using KiCad, the project includes custom footprints for Cherry MX key switches and the XIAO form factor.

### 📐 Schematic Diagram
The switches connect on one side to their respective digital pins and on the other side to a common ground (`GND`).

![Schematic](progress-pics/Design1-SCH.png)

### 🗺️ PCB Layout Routing
A clean 2-layer board layout routing digital signals on the top layer and utilizing a bottom solid ground plane.

![PCB Layout](progress-pics/Design1-PCB.png)

### 📦 3D Render
A preview of the finished hardware showing the key switch positioning and the XIAO RP2040 mounting area.

![3D View Reference](progress-pics/Design1-3D.png)

---

## 💾 Firmware & Software Installation

The macro pad runs **CircuitPython**. Follow these simple steps to install the firmware and configure the macros:

1.  **Install CircuitPython:**
    *   Download the latest `.uf2` file for the Seeed Studio XIAO RP2040 from the [CircuitPython website](https://circuitpython.org/board/seeeduino_xiao_rp2040/).
    *   Connect your board to your computer while holding down the **BOOT** button, then press **RESET** to enter bootloader mode (a drive named `RPI-RP2` will mount).
    *   Drag and drop the downloaded `.uf2` file onto the `RPI-RP2` drive.

2.  **Add Required Libraries:**
    *   Download the CircuitPython library bundle.
    *   Copy the `adafruit_hid` folder and `neopixel.mpy` file into the `lib/` directory of your `CIRCUITPY` drive.

3.  **Upload the Code:**
    *   Copy the contents of [`source-code/main.py`](source-code/main.py) to a file named `code.py` or `main.py` in the root of the `CIRCUITPY` drive.
    *   The board will auto-reload and start acting as a USB Keyboard!

---

## ⚙️ Customizing Hotkeys

You can easily modify the macros in `main.py` by changing the `MACRO_CONFIG` dictionary. For example, to map a key to `Ctrl + Shift + T`, update the keys array:

```python
"SW1": {
    "name": "Reopen Tab",
    "keys": [Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.T],
    "color": (255, 255, 0) # Yellow feedback
}
```

---

## 📂 Project Structure

```
├── pcb_design-1/     # KiCad schematic, PCB layout, and project configuration
├── progress-pics/    # Schematics and PCB render images
├── source-code/      # CircuitPython macro pad source code
└── README.md         # Project documentation (this file)
```
