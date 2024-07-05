
# Raspberry Pi Self-Destruct Server

This project transforms your Raspberry Pi into a mock "self-destruct" server. It's perfect for educational purposes or simply having a bit of fun with your Raspberry Pi setup.

## Features

- **Countdown Mechanism**: Utilizes an LCD display to show a countdown to "explosion", creating a suspenseful self-destruct sequence.
- **Auditory Feedback**: Integrates a buzzer that turns on at the beginning of the countdown, enhancing the dramatic effect.
- **Visual Feedback**: An LED lights up when the self-destruct sequence is finished, signaling the "explosion".
- **Network Communication**: Sends a message back to the client over a network connection once the self-destruct sequence is completed, allowing for remote triggering and monitoring.

## How It Works

The server script runs on the Raspberry Pi, waiting for a trigger message from a client. Upon receiving the trigger, it starts a countdown, visually displayed on an LCD screen and audibly signaled by a buzzer. When the countdown reaches zero, it simulates a self-destruct "explosion" by turning on an LED and sending a confirmation message back to the client. The script handles network communication, ensuring the client is informed of the sequence's completion.

