# G-Code-VMC-Runtime-Calculator-via-Excel
This program generates approximate runtimes for sections of G-code sharing one fixed feed rate. This is achieved by turning the toolpath into its respective line segments (where motion is linear), calculating the time it takes to traverse the line and recording this value line-by-line as the G-code is read.
