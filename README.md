# diy-midi-keyboard
This project is a DIY USB MIDI controller inspired by the YouTuber, https://www.youtube.com/watch?v=DS3cwTbc7yc
# Mini MIDI Piano + Drum Pad

## Overview
3-octave MIDI piano with 4 drum pads, TFT display showing notes/chords, rotary encoder, and MIDI over USB.

## Features
- 36-key matrix (3 octaves)
- 4 drum pads
- TFT screen (ST7735R)
- Rotary encoder (volume/instrument)
- PCM5100 DAC for audio output
- USB MIDI output

## Journal
See /journal/journal.md for a full step log.

## BOM
See /BOM/bom.csv for all components used.

## Code
- /code/key_matrix.py → Key matrix + MIDI
- /code/midi_demo.py → MIDI chord demo
