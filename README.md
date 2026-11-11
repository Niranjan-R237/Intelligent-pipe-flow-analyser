# Intelligent-pipe-flow-analyser
Python-based hydraulic analysis tool for calculating pressure drop, Reynolds number, friction factor, head loss and pump power in pipe flow systems.

## 1. Introduction to Fluid Mechanics

Fluid mechanics is the branch of engineering science that deals with the behaviour of fluids (liquids and gases) at rest and in motion. It is an important subject in mechanical, civil, chemical and environmental engineering.

In practical applications, fluids are transported through pipes in systems such as water-supply networks, industrial pipelines, cooling systems, irrigation networks and pumping installations.

When a fluid flows through a pipe, it experiences resistance due to friction between the fluid layers and between the fluid and the internal pipe surface. This resistance causes a reduction in pressure along the direction of flow. This phenomenon is known as **pressure drop**.

Understanding pressure drop is important because it helps engineers:
- Select suitable pipe diameters.
- Estimate the energy required to transport fluids.
- Determine the required pump power.
- Evaluate the efficiency of a piping system.
- Design safe and economical hydraulic systems.

## 2. Project Overview

The **Intelligent Pipe Flow & Hydraulic System Analyzer** is a Python-based engineering application developed to analyse the flow of fluid through a circular pipe.

The program accepts pipe dimensions, flow conditions and fluid properties as inputs. It uses fundamental fluid mechanics equations to calculate important hydraulic parameters, including:

- Average fluid velocity.
- Reynolds number.
- Flow regime.
- Darcy friction factor.
- Pressure drop.
- Head loss.
- Required pump power.

The application also generates graphs showing how pressure drop changes with flow rate and pipe diameter. Based on a user-defined maximum allowable pressure drop, it provides a recommended pipe diameter within the range investigated by the program.

The application uses a graphical user interface (GUI), allowing users to enter values and perform calculations through buttons rather than directly interacting with Python code.

## 3. Fundamental Concepts and Equations

### 3.1 Cross-Sectional Area of the Pipe

The cross-sectional area of a circular pipe is calculated using:

**A = πD² / 4**

Where:
- A = Cross-sectional area (m²)
- D = Internal pipe diameter (m)
- π = Mathematical constant (approximately 3.14159)

The area determines how much space is available for fluid flow.

### 3.2 Average Fluid Velocity

The average velocity of fluid flowing through the pipe is:

**V = Q / A**

Where:
- V = Average fluid velocity (m/s)
- Q = Volumetric flow rate (m³/s)
- A = Cross-sectional area (m²)

For a given flow rate, reducing the pipe diameter increases the average fluid velocity.

### 3.3 Reynolds Number

The Reynolds number is a dimensionless quantity used to identify the nature of fluid flow.

**Re = ρVD / μ**

Where:
- Re = Reynolds number
- ρ = Fluid density (kg/m³)
- V = Average fluid velocity (m/s)
- D = Pipe diameter (m)
- μ = Dynamic viscosity (Pa·s)

The program classifies the flow using the following ranges:

| Reynolds number | Flow regime |
|---|---|
| Re < 2300 | Laminar |
| 2300 ≤ Re < 4000 | Transitional |
| Re ≥ 4000 | Turbulent |

**Laminar flow:** Fluid particles move in relatively orderly layers, with limited mixing between adjacent layers.

**Transitional flow:** The flow is in an intermediate region where its behaviour may change between laminar and turbulent.

**Turbulent flow:** Fluid motion is irregular, with fluctuations and mixing within the fluid.

### 3.4 Darcy Friction Factor

The Darcy friction factor represents the resistance to flow caused by friction within a pipe. It is required for calculating pressure drop using the Darcy–Weisbach equation.

For laminar flow, the program uses:

**f = 64 / Re**

For turbulent flow, the program uses the Swamee–Jain explicit approximation:

**f = 0.25 / [log₁₀(ε/(3.7D) + 5.74/Re⁰·⁹)]²**

Where:
- f = Darcy friction factor
- ε = Absolute pipe roughness (m)
- D = Pipe diameter (m)
- Re = Reynolds number

The friction factor depends on the flow regime, Reynolds number and relative pipe roughness.

For transitional flow, the program uses a linear blend between the laminar and turbulent estimates. This is a simplified numerical approximation and should not be treated as a universally validated transitional-flow correlation.

### 3.5 Pressure Drop – Darcy–Weisbach Equation

The pressure drop due to friction along a straight pipe is calculated using the Darcy–Weisbach equation:

**ΔP = f × (L/D) × (ρV²/2)**

Where:
- ΔP = Pressure drop (Pa)
- f = Darcy friction factor
- L = Pipe length (m)
- D = Pipe diameter (m)
- ρ = Fluid density (kg/m³)
- V = Average fluid velocity (m/s)

The equation shows that pressure drop depends on pipe length, pipe diameter, fluid density, velocity and friction factor.

Pressure drop is an important design parameter because excessive pressure losses increase the energy required to transport fluid.

### 3.6 Head Loss

Pressure drop can also be expressed as the equivalent height of a fluid column. This is known as head loss.

**h = ΔP / (ρg)**

Where:
- h = Head loss (m)
- ΔP = Pressure drop (Pa)
- ρ = Fluid density (kg/m³)
- g = Gravitational acceleration (9.81 m/s²)

Head loss represents the energy loss per unit weight of fluid due to the friction considered in the calculation.

### 3.7 Pump Power

The program estimates the pump power required to overcome the calculated frictional pressure drop.

**P = (ΔP × Q) / η**

Where:
- P = Estimated pump input power (W)
- ΔP = Pressure drop (Pa)
- Q = Volumetric flow rate (m³/s)
- η = Pump efficiency

The program assumes a constant pump efficiency of 70%.

This calculation estimates the power associated with overcoming the calculated pipe-friction pressure drop. It does not include other system requirements such as elevation differences, valves, bends or other minor losses.

## 4. How the Python Program Works

The program is divided into several sections to make it organised, understandable and easier to maintain.

### Section 1: Imports and Constants

The program imports the libraries required for calculations, graphical plotting and the graphical user interface.

- **math:** Used for mathematical operations such as π and logarithms.
- **tkinter:** Used to create the graphical user interface.
- **messagebox:** Used to display input-error messages.
- **NumPy:** Used to generate arrays of flow rates and pipe diameters for analysis.
- **Matplotlib:** Used to generate pressure-drop graphs.

The program also defines gravitational acceleration and the assumed pump efficiency.

### Section 2: Core Calculation Functions

Individual functions perform specific engineering calculations.

These functions calculate:
1. Pipe cross-sectional area.
2. Average fluid velocity.
3. Reynolds number.
4. Flow regime.
5. Darcy friction factor.
6. Pressure drop.
7. Head loss.
8. Pump power.

Separating the calculations into functions makes the program easier to understand, test and modify.

### Section 3: Analysis and Diameter Recommendation

The `analyze()` function combines the individual calculation functions and returns the complete set of hydraulic results.

The `sweep()` function studies how pressure drop changes when either the flow rate or pipe diameter is varied. It generates 20 values over a range from 50% below to 50% above the entered value.

The `recommend_diameter()` function investigates 200 pipe-diameter values within the same ±50% range. It selects the smallest tested diameter for which the calculated pressure drop is less than or equal to the maximum allowable pressure drop.

If no tested diameter satisfies the pressure-drop limit, the program displays a message indicating that no suitable diameter was found in the investigated range.

### Section 4: Graph Generation

The `show_plot()` function uses Matplotlib to generate graphs.

The program provides two graph options:

- **Pressure Drop vs Flow Rate:** Shows how pressure drop changes when the volumetric flow rate is varied.
- **Pressure Drop vs Pipe Diameter:** Shows how pressure drop changes when the pipe diameter is varied.

These graphs help users understand the relationship between pipe design parameters and hydraulic performance.

### Section 5: GUI Callbacks

The callback functions control what happens when the user clicks the buttons.

- `read_inputs()` collects the values entered in the GUI and checks their validity.
- `on_calculate()` performs the hydraulic analysis and displays the results and diameter recommendation.
- `on_plot()` validates the inputs and generates the selected graph.

If invalid values are entered, the program displays an error message.

### Section 6: Graphical User Interface

The application is developed using Tkinter.

The interface contains input fields for:
- Pipe length.
- Pipe diameter.
- Flow rate.
- Fluid density.
- Dynamic viscosity.
- Pipe roughness.
- Maximum allowed pressure drop.

It also contains three buttons:

1. **CALCULATE:** Calculates and displays the hydraulic parameters.
2. **ΔP vs FLOW:** Generates the pressure-drop versus flow-rate graph.
3. **ΔP vs DIAMETER:** Generates the pressure-drop versus pipe-diameter graph.

The results are displayed in a text area within the application window.

### Section 7: Program Execution

The `root.mainloop()` statement starts the Tkinter event loop. This keeps the application window active and allows the user to interact with the input fields and buttons.

## 5. Input Parameters

The following parameters are entered by the user:

| Parameter | Symbol | Unit |
|---|---|---|
| Pipe length | L | m |
| Pipe diameter | D | m |
| Volumetric flow rate | Q | m³/s |
| Fluid density | ρ | kg/m³ |
| Dynamic viscosity | μ | Pa·s |
| Pipe roughness | ε | m |
| Maximum allowable pressure drop | ΔPmax | Pa |

The program provides default values in the input fields, which users can modify according to their requirements.

## 6. Output Parameters

After clicking the CALCULATE button, the program displays:

| Output | Description | Unit |
|---|---|---|
| Velocity | Average fluid velocity | m/s |
| Reynolds number | Identifies the flow regime | Dimensionless |
| Flow regime | Laminar, transitional or turbulent | — |
| Friction factor | Darcy friction factor | Dimensionless |
| Pressure drop | Frictional pressure loss along the pipe | Pa |
| Head loss | Equivalent fluid-column height | m |
| Pump power | Estimated power for the calculated frictional pressure drop | W |
| Recommended diameter | Smallest tested diameter meeting the pressure-drop limit | m |

## 7. Applications of the Project

The analyzer can be used as an educational and preliminary engineering tool for understanding pipe-flow behaviour.

Potential applications include:

- Water distribution systems.
- Industrial fluid transportation.
- Cooling-water circulation systems.
- Irrigation pipeline design.
- Preliminary hydraulic system design.
- Comparison of alternative pipe diameters.
- Understanding the effect of flow rate on pressure loss.

## 8. Assumptions and Limitations

The current version of the program uses the following assumptions and simplifications:

1. The pipe is circular and has a constant internal diameter.
2. The fluid properties are assumed to remain constant throughout the pipe.
3. The flow is treated as steady for the calculations.
4. The Darcy–Weisbach equation is used to calculate frictional pressure drop.
5. The Swamee–Jain approximation is used for turbulent-flow friction factor calculations.
6. Transitional flow friction factor is estimated using linear interpolation between laminar and turbulent values.
7. Pump efficiency is assumed to be constant at 70%.
8. Minor losses caused by bends, valves, fittings and entrances or exits are not included.
9. Elevation-related pressure changes are not included.
10. The recommended diameter is selected only from the tested ±50% diameter range and is not a complete economic pipe-sizing optimisation.

Therefore, the results should be considered preliminary estimates rather than a substitute for a complete hydraulic system design.

## 9. Future Scope

The project can be further developed by introducing:

- Analysis of different fluids such as water, oil and other liquids.
- Comparison of different pipe materials and surface roughness values.
- Inclusion of minor losses from valves, bends and fittings.
- Inclusion of elevation differences and total dynamic head.
- More detailed pipe-diameter optimisation.
- Exporting results to Excel and PDF reports.
- Additional graphs for velocity, Reynolds number and pump power.
- Improved engineering correlations and validation against reference calculations.
- An expanded graphical interface with more analysis options.

## 10. Conclusion

The Intelligent Pipe Flow & Hydraulic System Analyzer demonstrates how Python programming can be applied to fundamental fluid mechanics and hydraulic engineering problems.

By combining engineering equations with functions, numerical analysis, graphical plotting and a graphical user interface, the program provides an interactive method for calculating and understanding important pipe-flow parameters.

It helps users examine the influence of flow rate and pipe diameter on pressure drop and provides a preliminary pipe-diameter recommendation based on a specified pressure-drop limit.

The project connects theoretical fluid mechanics concepts with practical computational engineering and provides a foundation for developing more advanced hydraulic analysis tools.

## 11. Software and Libraries Used

- Programming language: Python
- Development environment: Spyder
- Mathematical calculations: Python `math` library
- Numerical analysis: NumPy
- Graph generation: Matplotlib
- Graphical user interface: Tkinter
