# rp2354-fido2-key

A FIDO2 security key firmware customized for a custom RP2354 based board. 
This project is a fork and adaptation of the pico-fido repository by Pol Henarejos.

## Hardware Overview

This project is designed to run on a custom-built PCB powered by the Raspberry Pi RP2354 microcontroller. The board is engineered to be compact and cost-effective, utilizing standard surface-mount components and a male USB-C plug that allows it to connect directly into a host device. 

The core hardware design includes:
- An RP2354 microcontroller handling the USB interface and cryptographic operations.
- A 3.3V LDO voltage regulator stepping down the USB 5V supply.
- An ESD protection diode to shield the sensitive USB data lines from static discharge during physical handling.
- A 12MHz crystal oscillator for accurate USB timing.
- A tactile push button for user presence verification during authentication.
- An indicator LED to show device status.

## How to Flash

To save physical space on the board, there is no dedicated physical BOOTSEL button. Instead, you must force the microcontroller into its USB bootloader mode manually using the exposed test pads.

1. Locate test pads TP1 and TP2 on the PCB.
2. Using metal tweezers or a small piece of wire, firmly short TP1 and TP2 together.
3. While keeping the pads shorted, plug the USB-C connector into your computer.
4. Once plugged in, you can remove the tweezers. The board will mount as a mass storage device (like a USB flash drive) on your computer.
5. Drag and drop the compiled firmware `.uf2` file into this drive.
6. The board will automatically reboot, disconnect the mass storage drive, and start acting as a FIDO2 security key.

## How to Use

Once flashed, the key functions out-of-the-box as a standard FIDO2 WebAuthn authenticator. 
- You can register it on any website or service that supports hardware security keys.
- When prompted by your browser or operating system during login or registration, simply press the tactile switch on your board to confirm your physical presence.

## License

MIT License. See the LICENSE file for details.
