import datetime
import threading
import telebot
import RPi.GPIO as GPIO
import time

FSR_PIN = 17  # GPIO pin connected to the FSR
MOSFET_PIN = 18  # GPIO pin connected to the MOSFET
BUZZER_PIN = 21  # GPIO pin connected to the buzzer
TOKEN = '6792117338:AAGWKJEU5B0iw1AO43BsxXXd3_tZmtn2z44'
CHAT_ID = [5867382409, 1844173274]

class FSR(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.fflag = True
        self.resting_times = {}
        self.rduration = 0
        self.rintervals = []

    def run(self):
        try:
            while self.fflag:
                today = datetime.date.today()
                if GPIO.input(FSR_PIN) == GPIO.HIGH:
                    # FSR detects pressure (resting)
                    self.turn_on_fan()
                    start_time = time.time()  # Record start time
                    s = datetime.datetime.now()
                    while GPIO.input(FSR_PIN) == GPIO.HIGH:
                        # Wait for pressure to release
                        time.sleep(0.1)
                    else:
                        self.turn_off_fan()
                    end_time = time.time()  # Record end time
                    e = datetime.datetime.now()
                    self.rduration += end_time - start_time
                    self.rintervals.append((s, e))
                    if datetime.date.today() != today:
                        self.resting_times[datetime.date.today()] = (self.rduration, self.rintervals)
                    print("Resting duration so far: {:.2f} seconds".format(self.rduration))
                time.sleep(0.1)  # Polling interval
        except KeyboardInterrupt:
            # Clean up GPIO
            GPIO.cleanup()

    def turn_on_fan(self):
        GPIO.output(MOSFET_PIN, GPIO.HIGH)
        print("Fan turned on")

    def turn_off_fan(self):
        GPIO.output(MOSFET_PIN, GPIO.LOW)
        print("Fan turned off")

    def stop(self):
        self.fflag = False

class Button(threading.Thread):
    def __init__(self, bid, fsr_thread):
        threading.Thread.__init__(self)
        self.bid = bid
        self.fsr = fsr_thread
        self.pillow_active = False
        self.timer_active = False
        self.hourtime = 0
        self.mintime = 0

    def send_message(self):
        bot = telebot.TeleBot(TOKEN)
        message = "Emergency: Medical help required!"
        for chat_id in CHAT_ID:
            bot.send_message(chat_id, message)

    def start_pillow(self):
        if not self.pillow_active:
            print("FSR thread started")
            self.fsr.start()
            self.pillow_active = True

    def stop_pillow(self):
        if self.pillow_active:
            if self.fsr:
                self.fsr.stop()
            self.pillow_active = False

    def buzz(self, duration):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

    def run(self):
        while True:
            # Handle button press
            if GPIO.input(self.bid) == GPIO.LOW:
                if self.bid == 20:
                    t = time.time()
                    while GPIO.input(self.bid) == GPIO.LOW:
                        continue
                    k = time.time()
                    if k - t < 1:
                        if not self.pillow_active:
                            self.start_pillow()
                        else:
                            self.stop_pillow()
                    else:
                        self.send_message()
                elif self.bid == 21:
                    self.timer_active = not self.timer_active
                    if self.timer_active:
                        print(f"Timer set: {self.hourtime} hour(s) {self.mintime} minute(s)")
                        duration = self.hourtime * 3600 + self.mintime * 60
                        threading.Thread(target=self.buzz, args=(duration,)).start()
                    else:
                        print("Timer reset")
                elif self.bid == 22:
                    if self.timer_active:
                        self.hourtime += 1
                        print(f"Hours set to: {self.hourtime}")
                    else:
                        print("Timer not active, cannot set hours")
                elif self.bid == 23:
                    if self.timer_active:
                        self.mintime += 1
                        print(f"Minutes set to: {self.mintime}")
                    else:
                        print("Timer not active, cannot set minutes")

            # Polling interval
            time.sleep(0.1)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(FSR_PIN, GPIO.IN)
GPIO.setup(MOSFET_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Initialize FSR thread
fsr_thread = FSR()

# Initialize Button threads
buttons = []
button_ids = [20, 21, 22, 23]  # Button GPIO pin numbers
for bid in button_ids:
    buttons.append(Button(bid, fsr_thread))

try:
    # Start the FSR thread
    fsr_thread.start()

    # Start the Button threads
    for button in buttons:
        button.start()

    # Main loop
    while True:
        pass

except KeyboardInterrupt:
    # Clean up GPIO
    GPIO.cleanup()
