"""
=========================================================
  INTELLIGENT PIPE FLOW & HYDRAULIC SYSTEM ANALYZER
=========================================================
Features:
  1. Reynolds number, flow regime and friction factor
  2. Pressure drop (Darcy-Weisbach), head loss, pump power
  3. Graphs: pressure drop vs flow rate / vs pipe diameter
  4. Automatic pipe diameter recommendation

Run:  python pipe_flow_analyzer.py
"""

# =========================================================
# SECTION 1: IMPORTS & CONSTANTS
# =========================================================
import math                      # basic maths (pi, log10)
import tkinter as tk             # GUI window and widgets
from tkinter import messagebox   # popup for input errors
import numpy as np               # linspace for the parameter sweeps
import matplotlib.pyplot as plt  # graphs

G = 9.81            # gravitational acceleration (m/s^2)
PUMP_EFFICIENCY = 0.70   # assumed pump efficiency (70%)

# Input fields shown in the GUI: (label, default value)
FIELDS = [
    ("Pipe length (m)", "50"),
    ("Pipe diameter (m)", "0.05"),
    ("Flow rate (m³/s)", "0.002"),
    ("Fluid density (kg/m³)", "1000"),
    ("Dynamic viscosity (Pa·s)", "0.001"),
    ("Pipe roughness (m)", "0.000045"),
    ("Max allowed pressure drop (Pa)", "50000"),
]


# =========================================================
# SECTION 2: CORE CALCULATION FUNCTIONS
# Each function does exactly one engineering calculation
# =========================================================
def calculate_area(D):
    """Cross-sectional area of a circular pipe: A = pi*D^2/4 (m^2)."""
    return math.pi * D**2 / 4


def calculate_velocity(Q, A):
    """Average fluid velocity: V = Q/A (m/s)."""
    return Q / A


def calculate_reynolds(rho, V, D, mu):
    """Reynolds number: Re = rho*V*D/mu (dimensionless)."""
    return rho * V * D / mu


def calculate_flow_regime(Re):
    """Classify the flow using standard Reynolds number limits."""
    if Re < 2300:
        return "Laminar"
    if Re < 4000:
        return "Transitional"
    return "Turbulent"


def calculate_friction_factor(Re, D, epsilon):
    """Darcy friction factor for laminar, transitional and turbulent flow."""
    # Laminar flow: exact solution f = 64/Re
    if Re < 2300:
        return 64 / Re

    # Turbulent flow: Swamee-Jain explicit approximation of Colebrook
    f_turbulent = 0.25 / math.log10(epsilon / (3.7 * D) + 5.74 / (Re**0.9))**2

    # Transitional flow: smooth blend between laminar and turbulent values
    if Re < 4000:
        weight = (Re - 2300) / (4000 - 2300)
        return (64 / Re) * (1 - weight) + f_turbulent * weight

    return f_turbulent


def calculate_pressure_drop(f, L, D, rho, V):
    """Darcy-Weisbach equation: dP = f*(L/D)*(rho*V^2/2) (Pa)."""
    return f * (L / D) * (rho * V**2 / 2)


def calculate_head_loss(delta_P, rho):
    """Pressure drop expressed as a height of fluid: h = dP/(rho*g) (m)."""
    return delta_P / (rho * G)


def calculate_pump_power(delta_P, Q):
    """Power the pump must supply: P = dP*Q/efficiency (W)."""
    return delta_P * Q / PUMP_EFFICIENCY


# =========================================================
# SECTION 3: ANALYSIS HELPERS
# Combine the core functions into full analyses
# =========================================================
def analyze(L, D, Q, rho, mu, epsilon):
    """Run the full calculation chain and return every result in a dict."""
    A = calculate_area(D)
    V = calculate_velocity(Q, A)
    Re = calculate_reynolds(rho, V, D, mu)
    f = calculate_friction_factor(Re, D, epsilon)
    dp = calculate_pressure_drop(f, L, D, rho, V)
    return {
        "V": V,
        "Re": Re,
        "regime": calculate_flow_regime(Re),
        "f": f,
        "dp": dp,
        "head": calculate_head_loss(dp, rho),
        "power": calculate_pump_power(dp, Q),
    }


def sweep(vary, p, points=20):
    """Vary flow rate ('Q') or diameter ('D') by +/-50% and return (x, dP)."""
    base = p[vary]
    x_values = np.linspace(base * 0.5, base * 1.5, points)
    dp_values = []
    for x in x_values:
        trial = dict(p, **{vary: x})           # copy inputs, replace one value
        dp_values.append(analyze(**trial)["dp"])
    return x_values, dp_values


def recommend_diameter(p, dp_max):
    """Smallest diameter (cheapest pipe) in the +/-50% range that meets dp_max."""
    diameters, drops = sweep("D", p, points=200)   # fine resolution
    for d, dp in zip(diameters, drops):
        if dp <= dp_max:
            return d
    return None   # nothing in the tested range is good enough


# =========================================================
# SECTION 4: GRAPH FUNCTION
# =========================================================
def show_plot(vary, p):
    """Plot pressure drop against flow rate ('Q') or pipe diameter ('D')."""
    x, y = sweep(vary, p)
    name = "Flow Rate (m³/s)" if vary == "Q" else "Pipe Diameter (m)"

    plt.figure(figsize=(9, 6))
    plt.plot(x, y, marker="o")
    plt.xlabel(name)
    plt.ylabel("Pressure Drop (Pa)")
    plt.title(f"Pressure Drop vs {name.split(' (')[0]}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# =========================================================
# SECTION 5: GUI CALLBACKS
# What happens when the user clicks a button
# =========================================================
def read_inputs():
    """Read and validate all entry boxes; raise ValueError if invalid."""
    v = [float(e.get()) for e in entries]

    # Length, diameter, flow, density, viscosity and max dP must be > 0;
    # roughness may be 0 (perfectly smooth pipe)
    if any(x <= 0 for x in v[:5]) or v[5] < 0 or v[6] <= 0:
        raise ValueError

    params = dict(L=v[0], D=v[1], Q=v[2], rho=v[3], mu=v[4], epsilon=v[5])
    return params, v[6]


def on_calculate():
    """CALCULATE button: show all results and the diameter recommendation."""
    try:
        params, dp_max = read_inputs()
        r = analyze(**params)
        rec = recommend_diameter(params, dp_max)
    except (ValueError, ZeroDivisionError):
        messagebox.showerror("Invalid Input", "Please enter valid positive numbers.")
        return

    # Recommendation text depends on whether a suitable diameter was found
    if rec:
        advice = f"Recommended Diameter : {rec:.4f} m\n(smallest pipe with ΔP ≤ {dp_max:.0f} Pa)"
    else:
        advice = "No suitable diameter found in the tested range (±50%)."

    result_box.delete("1.0", tk.END)
    result_box.insert(
        tk.END,
        f"Velocity          : {r['V']:.3f} m/s\n"
        f"Reynolds Number   : {r['Re']:.0f}\n"
        f"Flow Regime       : {r['regime']}\n"
        f"Friction Factor   : {r['f']:.5f}\n"
        f"Pressure Drop     : {r['dp']:.2f} Pa\n"
        f"Head Loss         : {r['head']:.3f} m\n"
        f"Pump Power        : {r['power']:.2f} W\n\n"
        f"{advice}",
    )


def on_plot(vary):
    """Graph buttons: validate inputs, then draw the requested sweep."""
    try:
        params, _ = read_inputs()
        show_plot(vary, params)
    except (ValueError, ZeroDivisionError):
        messagebox.showerror("Invalid Input", "Please enter valid positive numbers.")


# =========================================================
# SECTION 6: GUI LAYOUT
# =========================================================
root = tk.Tk()
root.title("Intelligent Pipe Flow & Hydraulic System Analyzer")
root.geometry("620x700")

# --- Title ---
tk.Label(root, text="Intelligent Pipe Flow Analyzer",
         font=("Arial", 18, "bold")).pack(pady=15)

# --- Input rows: one label + entry box per field in FIELDS ---
entries = []
for label, default in FIELDS:
    row = tk.Frame(root)
    row.pack(pady=3)
    tk.Label(row, text=label, width=30, anchor="w").pack(side="left")
    entry = tk.Entry(row, width=15)
    entry.insert(0, default)          # pre-fill with a sample value
    entry.pack(side="left")
    entries.append(entry)

# --- Buttons: calculate + two graphs ---
button_row = tk.Frame(root)
button_row.pack(pady=15)
buttons = [
    ("CALCULATE", on_calculate),
    ("ΔP vs FLOW", lambda: on_plot("Q")),
    ("ΔP vs DIAMETER", lambda: on_plot("D")),
]
for text, command in buttons:
    tk.Button(button_row, text=text, command=command,
              font=("Arial", 11, "bold"), padx=12, pady=6).pack(side="left", padx=6)

# --- Results area ---
result_box = tk.Text(root, height=13, width=58, font=("Consolas", 10))
result_box.pack(pady=10)


# =========================================================
# SECTION 7: START THE PROGRAM
# =========================================================
root.mainloop()
