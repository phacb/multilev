## Author Adrian C Barnes
##
## Master version June 2026
## Includes option to reset phase with non zero first byte (master) in sent array.

import time
import rp2
import uctypes
from machine import Pin
from machine import PWM
from machine import mem32
phases=bytearray()
#
# Before doing anything get the pico to run off the usb pll
#
mem32[0x400140ac]=0x00000008  # set function for GPIO 21 (8 for clock gpout0) (GPIO_CNTL register)
mem32[0x40008000]=0x00000860  # this should put the usb PLL clock on GPIO21
mem32[0x4000803c]=0x00000000  # set the clk_sys to clk_ref
mem32[0x4000803c]=0x00000021  # now set clk_sys to the usb PLL clock
#
mem32[0x40008048]=0x00000820     # Set the peripherals clock to run off  clksrc_pll_sys otherwise UART won't work
#
# Now we've set the system clock let's setup the UART
#To check the UART is working uncomment the following line to return a statsus to the controlling computer
#uart.write("Hello, UART responding!\n\r") # if UART is set up properky this should be returned e.g on the putty screen
#
uart = machine.UART(0, baudrate=921600, tx=16, rx=17)
#
# Define Master PIO output (not phase shiftable and only on master pico) on pin 1.
# reset using signal on GP18 set GPIO18 high before starting PIO

#
# Set the multiplier for the PIO to get the 40000 kHz signal required

# Note this will change if we change the source of the system clock.
# With the usual system clock this is 2560000 to get a 40k Hz signal
# using the USB clock (running at 48MHz, the multiplier is 125/48*2560000=6666666
#
pio_clock=6666666
#
# Set GPIO18 high to start. When it goes low the PIO outputs should start simultaneously
#
# Assign 'trig' to GPIO18
#
trig = machine.Pin(18,machine.Pin.OUT)
trig.value(1)

#Define Master output - no phase shift possible.
#After activation clock starts on GPIO18 low.

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)

def master():
    wait(0,gpio,18)
    wrap_target()
    set(pins,0)
    pull(noblock)
    mov(y,osr)
    label("a")
    jmp(y_dec,"a")
    set(pins, 0)   [27]
    set(pins, 1)   [31]
    wrap()

# Define slave PIO output (phase shiftable)
# After activation clock starts on GPIO18 low.

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)

def slave():
    wait(0,gpio,18)
    wrap_target()
    set(pins,0)
    pull(noblock)
    mov(y,osr)
    label("a")
    jmp(y_dec,"a")
    set(pins, 0)   [27]
    set(pins, 1)   [31]
    wrap()

def reset():
#   resets all phase shifts to zero
#   deactivate all PIOs
    trig.value(1)    # put trigger pin high so PIOs wait for it to go low to synchronise
    master.active(0)
    slave1.active(0)
    slave2.active(0)
    slave3.active(0)
    slave4.active(0)
    slave5.active(0)
    slave6.active(0)
    slave7.active(0)
#   restart
    master.restart()
    slave1.restart()
    slave2.restart()
    slave3.restart()
    slave4.restart()
    slave5.restart()
    slave6.restart()
    slave7.restart()
#   restart and resynchronise
    print('Reset')
    master.active(1)
    slave1.active(1)
    slave2.active(1)
    slave3.active(1)
    slave4.active(1)
    slave5.active(1)
    slave6.active(1)
    slave7.active(1)
    time.sleep(1)   # Need to give some time for state machines on slaves to restart 2s shoild be ample
    trig.value(0)
    trig.value(1)   # set high again ready for next time PIOs are restarted. 

#
#  Now setup and start the master and slave PIOs. Output frequency is set by pio_clock.
#
master = rp2.StateMachine(0, master, freq=pio_clock, set_base=Pin(1))
slave1 = rp2.StateMachine(1, slave, freq=pio_clock, set_base=Pin(3))
slave2 = rp2.StateMachine(2, slave, freq=pio_clock, set_base=Pin(5))
slave3 = rp2.StateMachine(3, slave, freq=pio_clock, set_base=Pin(7))
slave4 = rp2.StateMachine(4, slave, freq=pio_clock, set_base=Pin(9))
slave5 = rp2.StateMachine(5, slave, freq=pio_clock, set_base=Pin(11))
slave6 = rp2.StateMachine(6, slave, freq=pio_clock, set_base=Pin(13))
slave7 = rp2.StateMachine(7, slave, freq=pio_clock, set_base=Pin(15))

#
# Start the PIO outputs. NB. These will wait for GPIO18 to go low before any output
#
master.active(1)
slave1.active(1)
slave2.active(1)
slave3.active(1)
slave4.active(1)
slave5.active(1)
slave6.active(1)
slave7.active(1)
#
# All PIOs now running but waiting for signal on GP18 to start oupput
# i.e. waiting for tirgger signal on GP18
#
#
# Wait a second s for slave to start up before sending sync signal 
#
time.sleep(1)
trig.value(0)
trig.value(1)  # set high again so that if a reset is given the PIOS will wait to synchronise
#
# At this point everything should be set up on the master
# There should be 8 synchronised 40 kHz signals on pins GP1,GP3,   GP15
# The UART on pins 16 and 17 should be responding at 921600 board.
#
# Now loop to look if any phase info has arrived and apply
#
while True:
    if uart.any():
#        uart.write("phases detected\n")
        phases=uart.read()
#        print(phases)          # output on Pico shell for debugging
#        uart.write(phases)     # returns phase array to computer - useful for debugging.
#        instead use a  non-zero value to do something else, i.e. reset the phases
        if (phases[0]!=0):
            reset()
        slave1.put(phases[1])
        slave2.put(phases[2])
        slave3.put(phases[3])
        slave4.put(phases[4])
        slave5.put(phases[5])
        slave6.put(phases[6])
        slave7.put(phases[7])



