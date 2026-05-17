# Shake Shake Boom

Shake Shake Boom is a multiplayer, hot potato-inspired game where players shake and pass around an explosive device. The 3D-printed can-shaped device tracks motion using a pedometer-derived system, and after a random number of shakes (20–40), it triggers an explosion by running extremely high voltage through a capacitor mounted on top. Don't be the one holding the can when it explodes!

---

## Features

- Motion detection using a piezoelectric accelerometer taken from a disassembled pedometer  
- Randomized shake threshold  
- Multiplayer gameplay  
- Handmade case design (via Onshape)  
- Number of shakes reflected by bubbles displayed on an OLED screen (more shakes = more bubbles!)

---

## Tech Stack

### Hardware

- Microcontroller Pico board (1x)  
- Digital pedometer (1x)  
- 0.96in OLED display (1x)  
- Relay (1x)  
- Battery 9V (6x)  
- Buck 10V to 5V converter (1x)  
- 3D-printed can and lid (1x)  
- Button (1x)  
- LEDs (1x, used for testing)  

### Software

- MicroPython (logic)  
- Wokwi (wiring diagram, simulation)  
- Pixart (OLED displays)  

---

## Purpose

We wanted to create an interactive experience that combines everyone's favorite things: gambling, drinking, and explosions!!!
