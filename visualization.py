import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Load your .mat file
from scipy.io import loadmat

# Load trial_types data from the .mat file
mat_data = loadmat('trial_types.mat')
trial_types = mat_data['trial_types'].flatten()  # Flatten into a 1D array

# Define boundaries and phase labels
boundaries = [0, 50, 440, 450, 610, 1450, 1610, 2450]  # Adjusted for Python indexing (start from 0)
phase_labels = [
    'Familiarisation', 'Training', 'Refam.',
    'Null 1', 'Null 2', 'Learning CF (early)', 'Learning CF (mid-late/generalisation)'
]

# Define trial type colors
trial_type_colors = {
    0: '#ffffff',  # NF (white)
    1: '#99ff99',  # FC
    2: '#ff9999',  # DF
    3: '#9999ff'   # CF/VF
}

# Parameters for perfect squares
square_size = 1  # Size of each square
rows_per_phase = 25  # Number of rows per phase
space_between_phases = 3  # Space (in square units) between phases
border_color = "#3070B3"  # Border color
border_width = 1.5  # Border width

# Plot the activity diagram
fig, ax = plt.subplots(figsize=(15, 6))

# Loop through each phase and plot the trials
x_offset = 0  # Keeps track of the x-axis offset
for i, (start, end) in enumerate(zip(boundaries[:-1], boundaries[1:])):
    # Extract trial types for the current phase
    phase_data = trial_types[start:end]

    # Calculate the number of columns needed for this phase
    num_trials = len(phase_data)
    num_columns = int(np.ceil(num_trials / rows_per_phase))

    # Plot each trial as a perfect square
    for j, trial_type in enumerate(phase_data):
        row = j % rows_per_phase
        col = j // rows_per_phase
        rect = Rectangle(
            (x_offset + col * square_size, rows_per_phase - row - 1),  # Bottom-left corner
            square_size, square_size,  # Width and height (perfect square)
            linewidth=border_width, edgecolor=border_color, facecolor=trial_type_colors[int(trial_type)]
        )
        ax.add_patch(rect)

    # Add phase label with white font
    ax.text(x_offset + (num_columns * square_size) / 2, -1.5, phase_labels[i],
            ha='center', fontsize=10, color='white')

    if phase_labels[i] == 'Training':
        x_offset += num_columns * square_size + (space_between_phases * 5)  # Bigger space after "Training"
    else:
        x_offset += num_columns * square_size + space_between_phases

legend_elements = [
    Rectangle((0, 0), 1, 1, color=trial_type_colors[trial], label=label, edgecolor=border_color, linewidth=border_width)
    for trial, label in zip(range(4), ['No Force (NF)', 'Force Channel (FC)', 'Divergent Force Field (DF)', 'Curl Force Field (CF/VF)'])
]
ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.05, 1.35), ncol=1, fontsize=10)

# Configure plot
ax.set_aspect('equal')  # Force equal aspect ratio for perfect squares
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(0, x_offset)
ax.set_ylim(-2, rows_per_phase + 1)
ax.axis('off')  # Remove axes for clean appearance

# Add title with white font
plt.title('Trial Setup', fontsize=14, pad=20, color='white')

# Save with transparent background
plt.tight_layout()
plt.savefig('visualization_white_fonts.png', dpi=600, transparent=True)
