# First-Hackpad - 3-Key CircuitPython Macro Pad Firmware
# Target Board: Seeed Studio XIAO RP2040
# Switches connected to D10 (SW1), D9 (SW2), and D8 (SW3)
# Active-low inputs with internal pull-up resistors.

import time
import board
import usb_hid
from digitalio import DigitalInOut, Direction, Pull

# Attempt to import adafruit_hid libraries for USB Keyboard functionality
try:
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
    HID_AVAILABLE = True
except ImportError:
    HID_AVAILABLE = False
    print("Adafruit HID library not found. Falling back to Serial output.")

# Attempt to import neopixel for RGB LED feedback
try:
    import neopixel
    NEOPIXEL_AVAILABLE = True
except ImportError:
    NEOPIXEL_AVAILABLE = False
    print("Neopixel library not found. RGB feedback will be disabled.")

# --- Configuration ---
DEBOUNCE_DELAY = 0.05  # Debounce delay in seconds

# Define RGB color presets (R, G, B)
COLOR_IDLE = (10, 0, 25)       # Soft purple/indigo
COLOR_SW1 = (255, 0, 100)      # Pink/Magenta
COLOR_SW2 = (0, 255, 150)      # Mint green
COLOR_SW3 = (0, 150, 255)      # Cyan/Blue
COLOR_OFF = (0, 0, 0)

# Define Key mapping (macro action list)
# If HID is available, pressing a key sends the respective key combinations.
# You can customize these keycodes as needed.
if HID_AVAILABLE:
    MACRO_CONFIG = {
        "SW1": {
            "name": "Copy",
            "keys": [Keycode.LEFT_CONTROL, Keycode.C],
            "color": COLOR_SW1
        },
        "SW2": {
            "name": "Paste",
            "keys": [Keycode.LEFT_CONTROL, Keycode.V],
            "color": COLOR_SW2
        },
        "SW3": {
            "name": "Undo",
            "keys": [Keycode.LEFT_CONTROL, Keycode.Z],
            "color": COLOR_SW3
        }
    }
else:
    MACRO_CONFIG = {
        "SW1": {"name": "SW1 (Copy)", "color": COLOR_SW1},
        "SW2": {"name": "SW2 (Paste)", "color": COLOR_SW2},
        "SW3": {"name": "SW3 (Undo)", "color": COLOR_SW3}
    }

# --- Initialization ---

# Initialize Switches
# SW1 -> D10 (board.D10)
# SW2 -> D9  (board.D9)
# SW3 -> D8  (board.D8)
switches = {}
switch_pins = {
    "SW1": board.D10,
    "SW2": board.D9,
    "SW3": board.D8
}

for name, pin in switch_pins.items():
    btn = DigitalInOut(pin)
    btn.direction = Direction.INPUT
    btn.pull = Pull.UP
    switches[name] = btn

# Keep track of switch states for debouncing
last_state = {name: True for name in switches}      # True = Released (Pull-up)
stable_state = {name: True for name in switches}    # True = Released
last_debounce_time = {name: 0.0 for name in switches}

# Initialize USB HID Keyboard
keyboard = None
if HID_AVAILABLE:
    try:
        keyboard = Keyboard(usb_hid.devices)
    except Exception as e:
        print(f"Could not initialize HID Keyboard: {e}")
        HID_AVAILABLE = False

# Initialize NeoPixel RGB LED
pixel = None
if NEOPIXEL_AVAILABLE:
    try:
        # XIAO RP2040 has an on-board NeoPixel at board.NEOPIXEL (GP11)
        # It's an addressable RGB LED. Power pin board.NEOPIXEL_POWER needs to be high for it to work.
        if hasattr(board, "NEOPIXEL_POWER"):
            pixel_power = DigitalInOut(board.NEOPIXEL_POWER)
            pixel_power.direction = Direction.OUTPUT
            pixel_power.value = True
        
        pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=True)
        pixel[0] = COLOR_IDLE
    except Exception as e:
        print(f"Failed to initialize NeoPixel: {e}")
        NEOPIXEL_AVAILABLE = False

print("Hackpad Initialized! Ready for input.")

# --- Main loop ---
while True:
    current_time = time.monotonic()
    active_pressed = None

    for name, btn in switches.items():
        # Read the raw physical pin (Active Low)
        reading = btn.value
        
        # If the pin state changed, reset the debounce timer
        if reading != last_state[name]:
            last_debounce_time[name] = current_time
            last_state[name] = reading
            
        # If the state has been stable for longer than the debounce delay, update the stable state
        if (current_time - last_debounce_time[name]) > DEBOUNCE_DELAY:
            if reading != stable_state[name]:
                stable_state[name] = reading
                
                # Check for state transition (Press event: True -> False)
                if not stable_state[name]:
                    print(f"{name} Pressed ({MACRO_CONFIG[name]['name']})")
                    
                    # Trigger hotkey/macro
                    if HID_AVAILABLE and keyboard:
                        try:
                            # Send key combo
                            keys = MACRO_CONFIG[name]["keys"]
                            keyboard.send(*keys)
                        except Exception as e:
                            print(f"Error sending keypress: {e}")
                    
                    # Store active pressed key for LED feedback
                    active_pressed = name
                
                # Release event (False -> True)
                elif stable_state[name]:
                    print(f"{name} Released")

    # Update NeoPixel color based on active button press
    if NEOPIXEL_AVAILABLE and pixel:
        # Find if any button is currently held down
        currently_held = None
        for name in switches:
            if not stable_state[name]:  # Active Low, so False means pressed
                currently_held = name
                break
                
        if currently_held:
            pixel[0] = MACRO_CONFIG[currently_held]["color"]
        else:
            pixel[0] = COLOR_IDLE

    # Tiny sleep to reduce CPU usage
    time.sleep(0.01)
