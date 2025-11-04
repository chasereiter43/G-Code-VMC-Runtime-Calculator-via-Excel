import re 
import math 

# We're gonna open a text file and have it read segments of code.
# For simplicity, we can keep it so that the .txt file just contains segments of code. 
# This helps in situations where things like tool changes and other misc. codes
# might be hard to interpret.

''' ----- Section 1: Constants, Patterns, and Dictionaries ----------------------- '''
# Okuma 550VB / 650VB instruction manual says these are the rapid traverse
# rates in inches per minute
RAPID_XY = 1574.804 
RAPID_Z = 1181.103



# create patterns
pat_x = re.compile(r"\bX(-?\d*\.?\d+)\b")
pat_y = re.compile(r"\bY(-?\d*\.?\d+)\b")
pat_z = re.compile(r"\bZ(-?\d*\.?\d+)\b")
pat_n_number = re.compile(r"\bN\d+\b")



# create pattern dictionary
pat_dict: dict[str, re.Pattern[str]] = {
    "X" : pat_x,
    "Y" : pat_y,
    "Z" : pat_z
}


''' ----- Section 2: Functions, Classes ------------------------------------------------ '''


def makeSureFileExists(pathname: str) -> None:
    # EXCEPTION: check to make sure the file exists
    import os 
    if not os.path.exists(pathname):
        raise FileNotFoundError(f"File {pathname} was not found.")

    #  EXCEPTION: check to make sure the file is not empty
    if os.path.getsize(pathname) == 0:
        raise ValueError(f"File {pathname} exists but is empty.")


class Instruction:
    ''' --- Definitions ---
    n_number: the N number on a line of text
    position: the resulting position of the spindle designated by the line
    line: the line of text being read as a string
    mode: the mode on the line (G00/G01), either implicit or explicit
    dist_from_prev: distance to get to new position
    time: the time it takes to traverse the distance induced'''
    def __init__(self,
                 n_number: str = None,
                position: list[float] = None, 
                line: str = None, 
                mode: str = None, 
                dist_from_prev: float = None,
                time: float = None):
        
        self.n_number = n_number
        self.position = position
        self.line = line 
        self.mode = mode
        self.dist_from_prev =  dist_from_prev
        self.time = time


def get_n_number(line: str) -> str:
    # function for n-number extraction

    match = pat_n_number.search(line)

    if match:
        return match.group(0)

def extract(line: str) -> dict:
    # function for coordinate extraction 

    # Main Idea: create a dict that whose values will contain the coordinates of the
    #  line being read assuming a coordinate is stated. 
    # Keeps 'None' otherwise 
    coords_dict = {"X": None,
                   "Y": None,
                   "Z": None
                   }
    # For each of X, Y, and Z in pat_dict, check to see if line has any X, Y, or Z
    for axis, pattern in pat_dict.items():
        match = pattern.search(line)

        # if a match is found, assign the coordinate to coords_dict
        if match:
            coords_dict[axis] = float(match.group(1))

    # gives us our final dictionary in the end;
    # coordinates have now been extracted
    return coords_dict


def update_position(position: list[float],
                    coords_dict: dict[str, float]) -> list[float]:
    
    # Make a copy so the original position is not modified
    new_pos = position.copy()
    
    # Map axes to list indices
    axis_to_index = {"X": 0, "Y": 1, "Z": 2}
    
    # if coords_dict contains new information, update new_pos with those changes
    for axis, value in coords_dict.items():
        if value is not None:
            new_pos[axis_to_index[axis]] = value
    
    return new_pos


# euclidean distance function
def norm(start: list[float], end: list[float]) -> float:
    # flag for errors 
    if not (len(start) == len(end) == 3):
        raise ValueError(f"Norm Error: start {start} and end {end} differ in length.")
    
    # compute and return result
    return round(math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2 + (start[2] - end[2])**2),5)
     
if __name__ == '__main__':
    import os
    print(f"\n\nSuccessfully ran {os.path.basename(__file__)}")






