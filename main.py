from definitions import * 
from util import *
import os
import pandas as pd 


output_dir = r"C:\Users\creiter\Downloads\\"
new_file_name = "dataframe.csv"
od_nfm_combined = output_dir + new_file_name

''' === Part 0: Getting the Path Name === '''
# path name of .txt file to be read
file_to_alter: str = "snippet.txt"

makeSureFileExists(file_to_alter)


''' === Part 1: Getting the Pre-File Position, Mode, and Feed Rate === '''


'''Goal:    Turn PREFILE_POSITION into start_position   

            PREFILE_POSITION does not get used after that!      '''


# get current position of spindle (e.g. "5,6,7")
PREFILE_POSITION: str = input("Enter the current position of the spindle " \
                              
                        "at the beginning of the .txt file. " \
                        "\n(use format 'X, Y, Z'): ") 

# turn it into a list as split by commas (e.g. "[5,6,7]")
PREFILE_POSITION: list = PREFILE_POSITION.split(",") # returns a list

while len(PREFILE_POSITION) != 3:
    print("Error: position must be 3D.")
    PREFILE_POSITION = input("Position: ")
    PREFILE_POSITION: list = PREFILE_POSITION.split(",")

# create an empty list for the starting position (of floats)
start_position: list[float] = []

# convert elements (str) of PREFILE_POSITION to floats
for num_as_str in PREFILE_POSITION:
    num = float(num_as_str)
    start_position.append(num) # put them in start_position list


PREFILE_MODE: str = input("Enter the current mode that the machine is in (G00/G01): ")

while PREFILE_MODE not in ['G00','G01']:
    PREFILE_MODE = input("Invalid choice. Please enter G00 or G01: ")


PREFILE_FEEDRATE = float(input("Feed rate for this portion: "))



''' === Part 2: Opening the File and Converting to a DataFrame === '''



''' --- Definitions ---
    n_number: the N number on a line of text
    position: the resulting position of the spindle designated by the line
    line: the line of text being read as a string
    mode: the mode on the line (G00/G01), either implicit or explicit
    dist_from_prev: distance to get to new position
    time: the time it takes to traverse the distance induced'''

starting_row: Instruction = Instruction(n_number='N/A',
                              position= PREFILE_POSITION, 
                              line= 'N/A',
                              mode= PREFILE_MODE,
                              dist_from_prev= 'N/A')
                              

# create a container for the Instructions, starting out with starting_row
list_of_rows: list[Instruction] = [starting_row]

# create a container for the distances 
distances: list = []


# set initial mode to be what the user chose 
current_mode = PREFILE_MODE

# open file and begin assigning attributes to Instruction object
with open(file_to_alter, 'r') as file:
    for current_line in file:
        # create an Instruction object
        row = Instruction()
        row.line = current_line # AttrAssign .line
        row.n_number = get_n_number(current_line) # AttrAssign .n_number

        coords_dict = extract(current_line) # extract coordinates from line of text
        # AttrAssign .position
        row.position = update_position(start_position, coords_dict) # update row.position from None to the converted position based on the line of text 

        # check for mode changes
        if 'G00' in current_line:
            current_mode = 'G00'
        elif 'G01' in current_line:
            current_mode = 'G01'
        
        row.mode = current_mode # sets the row's mode
        dist = norm(start_position, row.position) # calculate distance
        row.dist_from_prev = dist # AttrAssign .dist_from_prev
        row.time = row.dist_from_prev / PREFILE_FEEDRATE

        distMode = (row.dist_from_prev, row.mode)
        distances.append(distMode)

        # let the row's end position become the new start position forthe next ineration
        start_position = row.position 

        # store the row in the row container
        list_of_rows.append(row)


        
# split up distances. Note that: pair = (dist, mode)
# so pair[0] = dist, pair[1] = mode 

G01_times = [pair[0]/PREFILE_FEEDRATE for pair in distances if pair[1] == 'G01']
G00_times = [pair[0]/RAPID_Z for pair in distances if pair[1] == 'G00']

show_duration = False
if show_duration:

    total_run_time: float = round(sum(G00_times) + sum(G01_times), 3) 

    trt_in_sec = total_run_time * 60
    seconds = round(trt_in_sec % 60, 2)

    if total_run_time >= 1:
        minutes = math.floor(total_run_time)
    else:
        minutes = 0

    sleepprint(f"\nThe total run time is: {total_run_time} minutes"
        f" also known as {minutes} min. {seconds} sec.")
    
    sleepprint(f"\nTotal G01 time: {sum(G01_times):.3f} min."
        f"\nTotal G00: time: {sum(G00_times):.3f} min.")

    if PREFILE_FEEDRATE > 150:
        sleepprint(red_text("\nWarning: Unusually high feed rate.\n"))


# create DataFrame for tracking 
df = pd.DataFrame({
    "n_number" : [row.n_number for row in list_of_rows],
    "position" : [row.position for row in list_of_rows],
    "line" : [row.line for row in list_of_rows], 
    "mode" : [row.mode for row in list_of_rows],
    "dist_from_prev" : [row.dist_from_prev for row in list_of_rows],
    "time (min.)" : [0] + [round(row.time,3) for row in list_of_rows[1:]]
})

df['cumulative time (min.)'] = df['time (min.)'].cumsum()


save = input("Save to Downloads? (Y/N) ").upper() 
while save not in ['Y','N']:
    sleepprint()
    save = input("Error. Save to Downloads? (Y/N) ").upper() 



if save == 'Y':
    try:
        # Save the DataFrame as a CSV file to the Downloads folder
        df.to_csv(od_nfm_combined, index= False)
    except Exception as e:
        print(f"Error has occurred. Error: {e}")

elif save == 'N':
    sleepprint("\nFile not saved.")
save




if __name__ == '__main__':
    sleepprint(f"\nSuccessfully ran {os.path.basename(__file__)}")

























