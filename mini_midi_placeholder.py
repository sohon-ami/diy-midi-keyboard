# mini_midi_placeholder.py
import board
import digitalio
import keypad
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
import time
import displayio
from adafruit_st7735r import ST7735R
from fourwire import FourWire
import terminalio
from adafruit_display_text import label

# -----------------------------
# Key Matrix (3 octaves = 36 keys)
# -----------------------------
rows = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5]
cols = [board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11]
matrix = keypad.KeyMatrix(rows, cols, columns_to_anodes=True)

# -----------------------------
# Drum Pads (4 pads)
# -----------------------------
pad_pins = [board.GP12, board.GP13, board.GP14, board.GP15]
pads = []
for pin in pad_pins:
    pad = digitalio.DigitalInOut(pin)
    pad.direction = digitalio.Direction.INPUT
    pad.pull = digitalio.Pull.UP
    pads.append(pad)

# -----------------------------
# TFT Display Placeholder
# -----------------------------
displayio.release_displays()
spi = board.SPI()
display_bus = FourWire(
    bus=spi,
    command=board.GP16,
    chip_select=board.GP17,
    reset=board.GP18
)
display = ST7735R(display_bus, width=128, height=160, rotation=90)

splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(128, 160, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x0000FF  # Blue background
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

text_group = displayio.Group()
text_area = label.Label(
    font=terminalio.FONT,
    text="Mini MIDI Piano\n3 Octaves + 4 Pads",
    color=0xFFFFFF,
    x=10,
    y=10
)
text_group.append(text_area)
splash.append(text_group)

# -----------------------------
# USB MIDI Setup
# -----------------------------
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# -----------------------------
# Main Loop
# -----------------------------
while True:
    # Check key matrix
    event = matrix.events.get()
    if event:
        if event.pressed:
            print(f"Key pressed: {event.key_number}")
            # Send placeholder MIDI note (C4 + key_number)
            midi.send(NoteOn(60 + event.key_number, 127))
        else:
            print(f"Key released: {event.key_number}")
            midi.send(NoteOff(60 + event.key_number, 0))
    
    # Check drum pads
    for i, pad in enumerate(pads):
        if not pad.value:  # pressed
            print(f"Drum pad {i+1} pressed")
            # Example: send a different note for each pad
            midi.send(NoteOn(36 + i, 127))  # MIDI drum notes
        else:
            midi.send(NoteOff(36 + i, 0))
    
    time.sleep(0.01)  # small delay to reduce CPU usage
