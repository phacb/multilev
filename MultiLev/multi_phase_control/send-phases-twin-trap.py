import pandas as pd
import serial
import time

def write_phases(phases):
    print(phases)
    ser.write(phases)
    print("done writing")

    time.sleep(0.1)

# Update COM_PORT with the Serial port for the USB-UART serial device
COM_PORT = 'COM7'

# Provide the full file path for the phased array data
phaseFile = 'c:/MultiLev/phase_array_data.xlsx'

ser = serial.Serial(COM_PORT, 115200)
ser.flush()

df = pd.read_excel(phaseFile, sheet_name='new spin')
columns_to_process = [df.columns[1]]

current_phases = bytearray(72)
new_phases = bytearray(72)
for i, row in df.iterrows():
    gpio = int(row['GPIO'])
    phase_value = row[columns_to_process[0]] * 32
    rounded_value = round(phase_value)

    if rounded_value < 0:
        rounded_value = (rounded_value + 64) % 64
    else:
        rounded_value = rounded_value % 64

    new_phases[gpio] = rounded_value
    print(new_phases)

phase_difference = bytearray(((new_phases[gpio] - current_phases[gpio]) + 64) % 64 for gpio in range(72))

write_phases(phase_difference)

current_phases = new_phases

input("Press Enter to continue with the rest of the spreadsheet...")
columns_to_process = df.columns[2:]

try:
    while True:
        for column in columns_to_process:
            new_phases = bytearray(72)
            
            for i, row in df.iterrows():
                gpio = int(row['GPIO'])
                phase_value = row[column] * 32
                rounded_value = round(phase_value)

                if rounded_value < 0:
                    rounded_value = (rounded_value + 64) % 64
                else:
                    rounded_value = rounded_value % 64

                new_phases[gpio] = rounded_value

            phase_difference = bytearray(((new_phases[gpio] - current_phases[gpio]) + 64) % 64 for gpio in range(72))

            write_phases(phase_difference)
            current_phases = new_phases
        
except KeyboardInterrupt:
    ser.close()
    pass
ser.close()