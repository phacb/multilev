# Author Adrian C Barnes
#
#   June 2026: slave v2
#  Slave. This relies on the master pico running and outputing a 48MKz usb_pll clock on its pin GPIO21 pin
#
import time
import rp2
import uctypes
from machine import Pin
from machine import PWM
from machine import mem32


# Get the board address for the pico. Note this is 3 bit based on GPIO28 (LSB),GPIO27 and GPIO26 (HSB)
addr1 = machine.Pin(28,machine.Pin.IN)
addr2 = machine.Pin(27,machine.Pin.IN)
addr3 = machine.Pin(26,machine.Pin.IN)

offset=(addr1.value()+addr2.value()*2+addr3.value()*4+1)*8

# print(offset) for in situ debugging

# Set up the PIO outputs. Note there is no master just 8 slaves. The synchronized start of the PIOs should
# come from GPIO18 going low on the master pico, or by an external reset pin setting GPIO18 low on the Master and Slave
# picos.
#
# We're going to run thus slave using the clock signal from the master pico as its clock signal
# Note. the sequence is important, especially the setting initially to clk_ref as we need to change the
# clock in a non glitching way. Only when we've set up the external clock can we connect in a non-glitch way
# to the external clock. See RP2040 datasheet for details 
#
mem32[0x4000803c]=0x00000000  # set the clk_sys to clk_ref (non glitching)
#
# now switch to excternal oscillator
#
mem32[0x400140a4]=0x00000008   # GPIO20 set to clock in. NB it has to be GPIO20 or GPIO22. I've used GPIO20
mem32[0x40008030]=0x00000002   # make sure clk_ref is coming from XOSC (non-glitching)
mem32[0x4000803c]=0x00000000   # sets clk_sys to non glitching clk_ref
mem32[0x4000803c]=0x00000020   # sets to auxiliary input but keeping XOSC temporarily
mem32[0x4000803c]=0x00000081   # sets clock ref to gpin (GPIO20) on aux. The system clock should now be 48 MHZ
                               # usb_pll from the master pico 
mem32[0x40008048]=0x00000820   # Set the peripherals clock to run off  clksrc_pll_sys otherwise UART won't work
#
# set up UART. NB only the RX line should be connected. The slaves should not transmit to avoid contention.
#
uart = machine.UART(0, baudrate=921600, tx=16, rx=17)  # UART1, GP12 (TX) and GP13 (RX)while True:
#
# Set GPIO18 as configured as an input. Its state is read by the PIO.
#
trig = machine.Pin(18,machine.Pin.IN)


pio_clock=6666666   # set up the clock for the PIO assuming we have 48 MHz usb_pll clock from the master (see comments in master)

# Seup up the slave PIO code

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
#   deactivate all PIOs
#    trig.value(1)    # trigger pulse should come from the master pico
    slave0.active(0)
    slave1.active(0)
    slave2.active(0)
    slave3.active(0)
    slave4.active(0)
    slave5.active(0)
    slave6.active(0)
    slave7.active(0)
#   restart
    slave0.restart()
    slave1.restart()
    slave2.restart()
    slave3.restart()
    slave4.restart()
    slave5.restart()
    slave6.restart()
    slave7.restart()
#   restart and resynchronise
    print('Reset')
    slave0.active(1)
    slave1.active(1)
    slave2.active(1)
    slave3.active(1)
    slave4.active(1)
    slave5.active(1)
    slave6.active(1)
    slave7.active(1)
#   this should now wait for the trigger from the master to get going again

slave0 = rp2.StateMachine(0, slave, freq=pio_clock, set_base=Pin(1))
slave1 = rp2.StateMachine(1, slave, freq=pio_clock, set_base=Pin(3))
slave2 = rp2.StateMachine(2, slave, freq=pio_clock, set_base=Pin(5))
slave3 = rp2.StateMachine(3, slave, freq=pio_clock, set_base=Pin(7))
slave4 = rp2.StateMachine(4, slave, freq=pio_clock, set_base=Pin(9))
slave5 = rp2.StateMachine(5, slave, freq=pio_clock, set_base=Pin(11))
slave6 = rp2.StateMachine(6, slave, freq=pio_clock, set_base=Pin(13))
slave7 = rp2.StateMachine(7, slave, freq=pio_clock, set_base=Pin(15))
#
# Start the PIO outputs. No output will be seen until GP18 goes low
#
slave0.active(1)
slave1.active(1)
slave2.active(1)
slave3.active(1)
slave4.active(1)
slave5.active(1)
slave6.active(1)
slave7.active(1)

#Output should be triggered when GP18 goes low.
#
while True:
    if uart.any():
        phases=uart.read()
        print(phases)   # check if debugging
        if (phases[0]!=0):
            reset()
        slave0.put(phases[offset])
        slave1.put(phases[offset+1])
        slave2.put(phases[offset+2])
        slave3.put(phases[offset+3])
        slave4.put(phases[offset+4])
        slave5.put(phases[offset+5])
        slave6.put(phases[offset+6])
        slave7.put(phases[offset+7])