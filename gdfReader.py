import mne
import os
import json
import matplotlib.pyplot as plt
import mpld3

# Define file paths
path = 'dataset/2a/BCICIV_2a_gdf/'
fileName = 'A01T.gdf'
inputFile = os.path.join(path, fileName)
output_json_path = os.path.join('outputs', f'{fileName}_info.json')
output_html_path = os.path.join('outputs', f'{fileName}_plot.html')

# Create output directory if it doesn't exist
os.makedirs('outputs', exist_ok=True)

# Load the GDF file
try:
    raw = mne.io.read_raw_gdf(inputFile, preload=True)
except Exception as e:
    print(f"Error loading GDF file: {e}")
    raise

# Plot the data
fig = raw.plot(show=False, title='GDF Data Plot')

# Fix for the warning: "Blended transforms not yet supported."
mpld3.plugins.connect(fig, mpld3.plugins.MousePosition(fontsize=14))

# Save the plot as an interactive HTML file using mpld3
html = mpld3.fig_to_html(fig)
with open(output_html_path, 'w') as html_file:
    html_file.write(html)
print(f"Plot successfully saved as interactive HTML to '{output_html_path}'")

# Show the plot interactively
mpld3.display(fig)
