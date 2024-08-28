import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap
from matplotlib.widgets import Slider

# Constants
N = 100  # Number of points on the string
t = np.linspace(0, 2 * np.pi, 200)

# Function to simulate string vibrations in 11D space
def vibrate_string_11d_real(t, modes=11, tension=1.0, gravity=9.81):
    dimensions = [np.sin(m * x + t) * tension - gravity * np.sin(t) for m in range(1, modes + 1)]
    return dimensions

# Project 11D to 3D using PCA, but ensure there are enough dimensions
def project_11d_to_3d_pca(vibrations):
    vibrations = np.array(vibrations).T
    if vibrations.shape[1] < 3:
        # If less than 3 dimensions, pad with zeros or replicate dimensions
        padding = np.zeros((vibrations.shape[0], 3 - vibrations.shape[1]))
        vibrations = np.hstack((vibrations, padding))
    pca = PCA(n_components=3)
    pca_projection = pca.fit_transform(vibrations)
    return pca_projection[:, 0], pca_projection[:, 1], pca_projection[:, 2]

# 3D Visualization setup
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Initial data setup
x = np.linspace(0, 2 * np.pi, N)
vibrations = vibrate_string_11d_real(0)
x_3d, y_3d, z_3d = project_11d_to_3d_pca(vibrations)
line, = ax.plot(x_3d, y_3d, z_3d, color='blue')
particle_positions = np.random.choice(np.arange(N), size=10, replace=False)  # Random particles

# Sliders for vibrational mode, tension, and gravity
ax_mode = plt.axes([0.2, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
mode_slider = Slider(ax_mode, 'Vibrational Mode', 1, 20, valinit=11, valstep=1)

ax_tension = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
tension_slider = Slider(ax_tension, 'String Tension', 0.1, 10.0, valinit=1.0)

ax_gravity = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
gravity_slider = Slider(ax_gravity, 'Gravity', 0.0, 20.0, valinit=9.81)

# Update function for animation
def update_with_real_physics(frame):
    mode = int(mode_slider.val)
    tension = tension_slider.val
    gravity = gravity_slider.val
    vibrations = vibrate_string_11d_real(frame, modes=mode, tension=tension, gravity=gravity)
    x_3d, y_3d, z_3d = project_11d_to_3d_pca(vibrations)
    
    ax.cla()
    ax.plot(x_3d, y_3d, z_3d, color='blue')
    for pos in particle_positions:
        ax.scatter(x_3d[pos], y_3d[pos], z_3d[pos], color='red')

    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    ax.set_title(f'11D Quantum Superstring Projection to 3D (Mode: {mode})')

    return line,

# Bind the sliders to the update function
ani = FuncAnimation(fig, update_with_real_physics, frames=t, blit=False, interval=30)
tension_slider.on_changed(lambda val: update_with_real_physics(0))
gravity_slider.on_changed(lambda val: update_with_real_physics(0))

plt.show()
