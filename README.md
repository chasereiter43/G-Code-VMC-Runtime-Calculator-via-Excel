# G-Code-VMC-Runtime-Calculator-via-Excel
This program generates approximate runtimes for sections of G-code sharing one fixed feed rate. This is achieved by turning the toolpath into its respective line segments (where motion is linear), calculating the time it takes to traverse the line and recording this value line-by-line as the G-code is read. Some initial guidelines must be followed:

1. The G-code is generated for a VMC (Vertical Machining Center) with at least 3 axes
2. The file snippet.txt is where the desired G-code should be pasted. Python reads and parses this as a usual .txt file, not an .nc file.
3. The feed rate for the portion of G-code pasted into snippet.txt is unchanging for the entire portion.
4. The active tool used by the VMC is the same tool for the entirety of snippet.txt; no tool changes are allowed.
5. There are no optional stops or program stops in snippet.txt; the tool runs continuously for all of snippet.txt.
6. All modes of movement are either G00 (rapid traverse) or G01 (linear interpolation); that is to say, no circular interpolation (G02/G03) is permitted.

Download all files and save them to the same directory. Note that the speed that a tool moves when in rapid traverse (G00) varies by the VMC chosen. By default, these values are set to the rapid traverse speeds for an Okuma 650VB. **These values can be altered in** `defintions.py`.

To use the calculator, run `main.py`. Upon running, you will be asked to provide the current position and current mode (G00 or G01) of the tool directly prior to the first line of G-code in snippet.txt that provides instructions to travel to a position. You will also be asked to provide the feed rate for the given chunk provided in snippet.txt. Once this is done, a .csv file is saved to the user's Downloads folder whose columns record for each line in snippet.txt the N-number, tool position, full/raw G-code line, distance from the previous point, time (min.) to travel to the desired point, and cumulative runtime (min.) up to that line in the G-code. **The user must manually alter the variable** `output_dir` **to their Downloads folder.**



