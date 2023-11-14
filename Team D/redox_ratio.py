from pysb import *
from pysb.simulator import ScipyOdeSimulator
import numpy as np
import matplotlib.pyplot as plt

Model()

# Monomers (reactive species)
Monomer("NADH", ['b'])
Monomer("Ox", ['b'])
Monomer("NAD_plus", ['b'])

# Initial conditions (concentrations of species at the start)
Parameter("NADH_init", 100)
Parameter("Ox_init", 50)
Parameter("NAD_plus_init", 0)  # Assuming initially there's no NAD+
Initial(NADH(b=None), NADH_init)
Initial(Ox(b=None), Ox_init)
Initial(NAD_plus(b=None), NAD_plus_init)

# Reaction rates
Parameter("kp1", .01)  # Forward rate for NADH binding to Ox
Parameter("km1", 1)    # Reverse rate for NADH unbinding from Ox
Parameter("kp2", .01)  # Forward rate for NADH_Ox converting to NAD+
Parameter("km2", 1)    # Reverse rate for NAD+ binding to Ox

# Reaction rules
# NADH binding to Ox (reversible)
Rule("NADH_binds_Ox", NADH(b=None) + Ox(b=None) | NADH(b=1) % Ox(b=1), kp1, km1)
# NADH_Ox converting to NAD+ and free Ox (reversible)
Rule("NADH_Ox_to_NAD_plus", NADH(b=1) % Ox(b=1) | NAD_plus(b=None) + Ox(b=None), kp2, km2)

# Observables (for tracking concentration changes over time)
Observable("NADH_free", NADH(b=None))
Observable("Ox_free", Ox(b=None))
Observable("NADH_Ox_bound", NADH(b=1) % Ox(b=1))
Observable("NAD_plus_free", NAD_plus(b=None))
Observable("NAD_plus_Ox_bound", NAD_plus(b=1) % Ox(b=1))

# Simulation setup
tspan = np.linspace(0, 1, 101)
sim = ScipyOdeSimulator(model, tspan, verbose=True)
output = sim.run()

# Plotting results
for obs in model.observables:
    plt.plot(tspan, output.observables[obs.name], lw=2, label=obs.name)
plt.xlabel("Time")
plt.ylabel("Concentration")
plt.legend(loc=0)
plt.show()
