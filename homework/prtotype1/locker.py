from machine import Pin, UART, PWM
import utime

# RS-485 direction control (using pin 11)
TRANSMIT = 1
RECEIVE = 0
RT_PIN = Pin(11, Pin.OUT)
RT_PIN.value(RECEIVE)  # Start in receive mode

# Setup buzzer (using pin 21) with PWM
BUZZER_PIN = 21
buzzer = PWM(Pin(BUZZER_PIN, Pin.OUT))
buzzer.duty_u16(0)  # Buzzer off initially

# Initialize UART on port 0 with baudrate 9600
uart = UART(0, baudrate=9600)

def tone(freq, duration_ms):
    """Generate a beep sound with given frequency and duration."""
    buzzer.freq(freq)
    buzzer.duty_u16(15000)  # Set duty cycle to produce audible tone
    utime.sleep_ms(duration_ms)
    buzzer.duty_u16(0)  # Turn off the buzzer

def unlock_locker():
    """Function to unlock the locker."""
    print("Locker unlocked")
    tone(1000, 500)  # Beep to indicate the locker is unlocked

def lock_locker():
    """Function to lock the locker."""
    print("Locker locked")
    tone(500, 500)  # Beep to indicate the locker is locked

print("Unlock tone")
tone(1000, 500)
utime.sleep_ms(50)
print("Lock tone")
tone(500, 500)

print("Receiver ready...")

while True:
    if uart.any():
        data = uart.read().decode().strip()
        print("Received:", data)
        if data == "unlock":
            unlock_locker()
        elif data == "lock":
            lock_locker()
        else:
            print("Unknown command")
    utime.sleep(1)