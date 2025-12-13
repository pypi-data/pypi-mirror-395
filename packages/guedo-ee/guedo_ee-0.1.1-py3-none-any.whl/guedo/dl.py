def dl(n):
    programs = {
        1: """# Program 1
1.Write a python program for Arithmetic Calculations.

a=int(input("Enter a:"))
b=int(input("Enter b:"))
print("Sum:",a+b)
print("Diff:",a-b)
print("Prod:",a*b)
print("Quo:",a//b)

""",
        2: """# Program 2
2. Write a python program for multiplication table

a=int(input("Enter a:"))
b=1
for i in range(1,11,b):
    print(f"{a}x{i}:",a*i)

""" , 
        3: """# Program 3
        3.Write a python program for verification of Ohm’s law

#To find Voltage
i=int(input("Enter the value of current:"))
r=10
v=i*r
print("The Voltage is(in Volt):",v)

#To find Current
v=int(input("Enter the value of Voltage:"))
r=10
i=v/r
print("The Current is(in amp):",i) 
""" , 
        4: """# Program 4
        4.Write a python program for KCL verification 

I1=float(input("Enter current I1:"))
I2=float(input("Enter current I2:"))
I3=float(input("Enter current I3:"))
si=I1+I2
so=I3
print("\n KCL is:\n")
print(f"Total current entering={si} A ")
print(f"Total current leaving={so}A")
t=1e-6
if abs(si<so)<=t:
    print("KCL verified: sum of curr entering=sum of curr leaving")
else:
    print("KCL not verified.")
    """ , 
        5: """# Program 5
        5.Write a python program for KCL verification of any number of branches.

def Kcl_ver():
    n_in=int(input("Enter the no.of currents entering:"))
    entering=[]
    for i in range(n_in):
        v=float(input("Enter currentI{i+1} entering:"))
        entering.append(v)
    n_o=int(input("Enter the no. of currents leaving the node:"))
    leaving=[]
    for j in range(n_o):
        v=float(input(f"Enter current I{j+1} leaving (A):"))
        leaving.append(v)
    sum_in=sum(entering)
    sum_out=sum(leaving)
    print("\nKCL Verification\n")
    print(f"Total current entering={sum_in:4f}A")
    print(f"Total current leaving={sum_in:4f}A")
    tolerance=1e-6
    if abs(sum_in<sum_out)<=tolerance:
        print("KCL verified")
    else:
        print("KCL not verified")
Kcl_ver()
""",   
    6: """# Program 6
    6.Write a python program for KCL verification with random currents

import random
def kcl_simulation():
    n_in = random.randint(2, 4)   
    n_out = random.randint(2, 4)  
    entering = [round(random.uniform(0.5, 5.0), 2) for _ in range(n_in)]
    leaving = [round(random.uniform(0.5, 5.0), 2) for _ in range(n_out)]
    sum_in = sum(entering)
    sum_out_except_last = sum(leaving[:-1])
    leaving[-1] = round(sum_in - sum_out_except_last, 2)
    sum_out = sum(leaving)
    print("\n--- KCL Simulation ---")
    print(f"Currents entering the node  : {entering}")
    print(f"Currents leaving the node   : {leaving}")
    print(f"Total entering = {sum_in:.2f} A")
    print(f"Total leaving  = {sum_out:.2f} A")
    tolerance = 1e-6
    if abs(sum_in - sum_out) <= tolerance:
        print(" KCL Verified ")
    else:
        print(" KCL Not Verified")
kcl_simulation()""",

    7: """# Program 7
    7. Write a python program for KCL verification with graphical representation

import random
import matplotlib.pyplot as plt

def kcl_visualization():
    n_in = random.randint(2, 3)
    n_out = random.randint(2, 3)
    entering = [round(random.uniform(0.5, 5.0), 2) for _ in range(n_in)]
    leaving = [round(random.uniform(0.5, 5.0), 2) for _ in range(n_out)]
    sum_in = sum(entering)
    sum_out_except_last = sum(leaving[:-1])
    leaving[-1] = round(sum_in - sum_out_except_last, 2)
    sum_out = sum(leaving)
    plt.figure(figsize=(6,6))
    plt.plot(0, 0, 'ko', markersize=15)
    plt.text(0.1, 0.1, "Node", fontsize=12, weight="bold")
    angle_step = 180 / (n_in+1)
    for i, I in enumerate(entering, start=1):
        x = -4
        y = 2*i - n_in
        plt.arrow(x, y, 3.8, -y, head_width=0.2, head_length=0.3, color="green")
        plt.text(x-0.5, y+0.2, f"Iin{i}={I}A", color="green")

    angle_step = 180 / (n_out+1)
    for j, I in enumerate(leaving, start=1):
        x = 0.2
        y = 2*j - n_out
        plt.arrow(x, y, 3.8, -y, head_width=0.2, head_length=0.3, color="red")
        plt.text(x+4.2, y+0.2, f"Iout{j}={I}A", color="red")
    plt.title("Verification of Kirchhoff's Current Law (KCL)", fontsize=14, weight="bold")
    plt.axis("off")
    plt.show()

    # Print verification
    print("\n--- KCL Verification ---")
    print(f"Currents entering: {entering}")
    print(f"Currents leaving : {leaving}")
    print(f"Total entering = {sum_in:.2f} A")
    print(f"Total leaving  = {sum_out:.2f} A")

    if abs(sum_in - sum_out) < 1e-6:
        print("KCL Verified (Graph + Calculation)")
    else:
        print(" KCL Not Verified")

kcl_visualization()
""",

    8: """# Program 8
    8.Write  a python program for KVL simulation and visualization

import random
import matplotlib.pyplot as plt
def kvl_sim():
    Vs=round(random.uniform(5,20),2)
    n=random.randint(2,4)
    res=[round(random.uniform(1,10),2)for i in range(n)]
   
    I = round(random.uniform(0.5, 3.0), 2)

    vol_drop = [round(I * R, 2) for R in res]
    sum_drops = sum(vol_drop)
    plt.figure(figsize=(7,6))
    plt.plot([0,0],[0,4],'k',linewidth=2)
    plt.text(-0.5, 2, f"Vs={Vs}V", color="blue", fontsize=12)
    plt.plot([0,0],[0,4],'k',linewidth=2)

    for i,V in enumerate(vol_drop,start=1):
        y1=4-(i-1)*(4/n)
        
        y2 = 4 - i*(4/n)
        plt.plot([4, 4], [y1, y2], 'r', linewidth=2)
        plt.text(4.2, (y1+y2)/2, f"R{i}\n{V}V", color="red", fontsize=10)
        plt.plot([0,0],[0,4],'k',linewidth=2)
    plt.title("Verification of Kirchhoff's Voltage Law (KVL)", fontsize=14, weight="bold")
    plt.axis("off")
    plt.show()
    print("\n--- KVL Verification ---")
    print(f"Supply Voltage: {Vs} V")
    for i, (R, V) in enumerate(zip(res, vol_drop), start=1):
        print(f"Resistor R{i} = {R} Ω → Voltage drop = {V} V")

    print(f"\nSum of drops = {sum_drops:.2f} V")

    if abs(Vs - sum_drops) <= 1e-6:
        print("KVL Verified: Supply voltage = Sum of voltage drops")
    else:
        print("KVL Not Verified: Check values")

kvl_sim()
""",

    9: """# Program 9
    9. Write  a python program for KVL verification

Vs=float(input("Enter the supply voltage(V):"))
n=int(input("Enter the no. of resistor in the loop:"))
res=[]
cur=[]
print("\n Enter resistance value:")
for i in range(n):
    R=float(input(f"R{i+1}:"))
    res.append(R)
I=float(input("\n Enter the loop current:"))
voltage_drops = [I * R for R in res]
sum_drops = sum(voltage_drops)

print("---KVL VERIFICATION---")
for i, V in enumerate(voltage_drops,start=1):
    print(f"Voltage drop acrossR{i}={V:.2f}V")
print(f"\nSupply voltage  = {Vs:.2f} V")
print(f"Sum of drops    = {sum_drops:.2f} V")

tolerance = 1e-6
if abs(Vs - sum_drops) <= tolerance:
    print("KVL Verified: Supply voltage = Sum of voltage drops")
else:
    print("KVL Not Verified: Check values")

""",
    10: """# Program 10
    10. Write a python program for KCL simulation (with Sliders)

import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact

def kcl_interactive(I1=2.0, I2=3.0, I3=4.0):
    plt.figure(figsize=(6,6))

    # Node at center
    plt.plot(0, 0, 'ko', markersize=15)
    plt.text(0.1, 0.1, "Node", fontsize=12, weight="bold")

    # Entering currents (green arrows)
    plt.arrow(-4, 1, 4, -1, head_width=0.2, head_length=0.3, color="green")
    plt.text(-4.5, 1.2, f"I1={I1}A", color="green")

    plt.arrow(-4, -1, 4, 1, head_width=0.2, head_length=0.3, color="green")
    plt.text(-4.5, -0.8, f"I2={I2}A", color="green")

    # Leaving current (red arrow)
    plt.arrow(0.2, 0, 4, 0, head_width=0.2, head_length=0.3, color="red")
    plt.text(4.5, 0.2, f"I3={I3}A", color="red")

    # Formatting
    plt.title("Interactive KCL Verification", fontsize=14, weight="bold")
    plt.axis("off")
    plt.show()

    # Verification in console
    sum_in = I1 + I2
    sum_out = I3
    print("--- KCL Check ---")
    print(f"Total entering = {sum_in:.2f} A")
    print(f"Total leaving  = {sum_out:.2f} A")

    if abs(sum_in - sum_out) < 1e-6:
        print("✅ KCL Verified")
    else:
        print("❌ KCL Not Verified")
kcl_interactive()
""",

    11: """# Program 11
    11.Write a python program to find Active Power, Reactive Power and Apparent Power

from math import*
V=float(input("Enter the value of Voltage:"))
I=float(input("Enter the value of Currebt:"))
o=float(input("Enter the phase angle:"))
P=V*I*cos(o)
Q=V*I*sin(o)
S=V*I
print("The active power is:",P)
print("The reactive power is:",Q)
print("The apparent power is:",S)
""",    
    12: """# Program 12
    12. Write a python program to implement AND, OR, NOT, NAND, NOR and XOR

def AND(a, b):
    return a & b
def OR(a, b):
    return a | b
def NOT(a):
    return ~a & 1 
def NAND(a, b):
    return NOT(AND(a, b))
def NOR(a, b):
    return NOT(OR(a, b))
def XOR(a, b):
    return a ^ b

inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]

print("A B | AND OR NAND NOR XOR")
for a, b in inputs:
    print(f"{a} {b} |  {AND(a, b)}   {OR(a, b)}   {NAND(a, b)}    {NOR(a, b)}   {XOR(a, b)}")

print("\nNOT Gate:")
for a in [0, 1]:
    print(f"NOT {a} = {NOT(a)}")

""",

    13: """# Program 13
    13. Write a python program for analysis of RL and RC circuit(Frequency Response)

import numpy as np
import matplotlib.pyplot as plt


R = 100
L = 0.1 
C = 1e-6 

f = np.logspace(1, 6, 1000)  # 10 Hz to 1 MHz
omega = 2 * np.pi * f

Z_series = R + 1j * omega * L + 1 / (1j * omega * C)
mag_series = np.abs(Z_series)
phase_series = np.angle(Z_series, deg=True)

Y_parallel = 1/R + 1j * omega * C - 1j / (omega * L)
Z_parallel = 1 / Y_parallel
mag_parallel = np.abs(Z_parallel)
phase_parallel = np.angle(Z_parallel, deg=True)


plt.figure(figsize=(14, 10))

plt.subplot(2, 1, 1)
plt.loglog(f, mag_series, label='Series RLC')
plt.loglog(f, mag_parallel, label='Parallel RLC')
plt.title('Frequency Response - Magnitude of Impedance')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude |Z| (Ohms)')
plt.grid(True, which='both', ls='--')
plt.legend()

# Phase plot
plt.subplot(2, 1, 2)
plt.semilogx(f, phase_series, label='Series RLC')
plt.semilogx(f, phase_parallel, label='Parallel RLC')
plt.title('Frequency Response - Phase of Impedance')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (Degrees)')
plt.grid(True, which='both', ls='--')
plt.legend()

plt.tight_layout()
plt.show()

""",

    14: """# Program 14
    14. Write a Python program for I-V and P-V Characteristics of a Solar Panel.

#I-V and P-V Characteristics of a Solar Panel

import numpy as np
import matplotlib.pyplot as plt

# Constants (simplified for beginner understanding)
Voc = 20       # Open-circuit voltage (Volts)
Isc = 5        # Short-circuit current (Amps)
n_points = 100 # Number of data points

# Generate voltage values from 0 to Voc
V = np.linspace(0, Voc, n_points)

# Simple model: current decreases linearly with voltage
I = Isc * (1 - V / Voc)

# Power = Voltage × Current
P = V * I

# Plotting I-V curve
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(V, I, 'b', label='I-V Curve')
plt.xlabel('Voltage (V)')
plt.ylabel('Current (I)')
plt.title('I-V Characteristics')
plt.grid(True)
plt.legend()

# Plotting P-V curve
plt.plot(V, P, 'r', label='P-V Curve')
plt.xlabel('Voltage (V)')
plt.ylabel('Power (P)')
plt.title('P-V Characteristics')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
"""

  }
    print(programs.get(n, "Program not found!"))
