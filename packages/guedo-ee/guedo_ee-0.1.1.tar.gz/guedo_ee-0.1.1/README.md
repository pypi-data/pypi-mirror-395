# Guedo - Electrical Engineering Program Library

A comprehensive Python library providing educational programs for electrical engineering concepts, including circuit analysis, Kirchhoff's laws, and signal processing demonstrations.

## Features

- **14 comprehensive programs** covering electrical engineering fundamentals
- Arithmetic calculations and mathematical operations
- Kirchhoff's Current Law (KCL) verification with simulation
- Kirchhoff's Voltage Law (KVL) verification and visualization
- Ohm's Law verification
- Power calculations (Active, Reactive, and Apparent Power)
- Logic gate implementations
- Circuit analysis (RL and RC circuits)
- Solar panel characteristics analysis
- Interactive visualizations with matplotlib

## Installation

Install the package from PyPI:

```bash
pip install guedo-ee
```

## Quick Start

```python
from guedo import dl

# Display program 1 (Arithmetic Calculations)
dl(1)

# Display program 6 (KCL Simulation)
dl(6)

# Display program 8 (KVL Simulation)
dl(8)
```

## Available Programs

| Program | Description |
|---------|-------------|
| 1 | Arithmetic Calculations |
| 2 | Multiplication Table |
| 3 | Ohm's Law Verification |
| 4 | KCL Verification |
| 5 | KCL Verification (Multiple Branches) |
| 6 | KCL Simulation with Random Currents |
| 7 | KCL Verification with Graphical Representation |
| 8 | KVL Simulation and Visualization |
| 9 | KVL Verification |
| 10 | Interactive KCL with Sliders |
| 11 | Active, Reactive, and Apparent Power |
| 12 | Logic Gates (AND, OR, NOT, NAND, NOR, XOR) |
| 13 | RL and RC Circuit Frequency Response |
| 14 | Solar Panel I-V and P-V Characteristics |

## Usage Examples

### Example 1: View a Specific Program
```python
from guedo import dl

# Get and display program 3 (Ohm's Law)
dl(3)
```

### Example 2: Run Interactive Programs
Some programs are interactive and will request user input:
```python
from guedo import dl

# Run program 9 (KVL with user input)
dl(9)
```

### Example 3: View Visualizations
Programs 7, 8, 10, 13, and 14 include matplotlib visualizations:
```python
from guedo import dl

# Display program 14 (Solar Panel Characteristics)
dl(14)
```

## Requirements

- Python 3.6 or higher
- matplotlib (for visualization programs)
- numpy (for numerical operations)
- ipywidgets (for interactive programs)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Your Name (your.email@example.com)

## Contributing

Contributions are welcome! Feel free to open issues and submit pull requests.

## Support

For support, issues, or questions, please visit the project repository or contact the author.
