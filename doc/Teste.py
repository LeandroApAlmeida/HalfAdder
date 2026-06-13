import numpy as np
import matplotlib.pyplot as plt

# vetores base
zero = np.array([1, 0])
one  = np.array([0, 1])

plt.figure(figsize=(5,5))

# desenhar vetores
plt.quiver(0, 0, zero[0], zero[1], angles='xy', scale_units='xy', scale=1, color='blue', label='|0⟩')
plt.quiver(0, 0, one[0], one[1], angles='xy', scale_units='xy', scale=1, color='red', label='|1⟩')

# ajustes do gráfico
plt.xlim(-0.2, 1.2)
plt.ylim(-0.2, 1.2)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)

plt.gca().set_aspect('equal')
plt.legend()
plt.title("Estados base de um qubit")
plt.grid(True)

plt.show()