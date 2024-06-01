import pandas as pd
import numpy as np
import pyedflib
import mne

# Load the CSV file
csv_file_path = 'outputs/A01E.csv'  # Replace with your actual CSV file path
df = pd.read_csv(csv_file_path)

# Handle missing or non-numeric data by filling with the mean of the column
df = df.apply(pd.to_numeric, errors='coerce')
df = df.fillna(df.mean())

# Extract channel names (excluding the time column)
channel_names = df.columns[:-1].tolist()
n_channels = len(channel_names)

# Extract data and time
data = df[channel_names].values.T  # Transpose to get channels x samples
times = df['time'].values

# Calculate sample rate
sample_rate = int(1 / np.mean(np.diff(times)))

# Create EDF file
edf_file_path = 'outputs/A01EConvertedFromCSV.edf'  # Replace with your desired output EDF file path
f = pyedflib.EdfWriter(edf_file_path, n_channels, file_type=pyedflib.FILETYPE_EDFPLUS)

# Define channel parameters
channel_info = []
for ch in channel_names:
    ch_data = data[channel_names.index(ch)]
    ch_dict = {
        'label': ch,
        'dimension': 'uV',  # Adjust according to your data's units
        'sample_rate': sample_rate,
        'physical_min': np.min(ch_data),
        'physical_max': np.max(ch_data),
        'digital_min': -32768,
        'digital_max': 32767,
        'transducer': '',
        'prefilter': ''
    }
    channel_info.append(ch_dict)

# Set the channel information
try:
    f.setSignalHeaders(channel_info)
except Exception as e:
    print(f"Error setting signal headers: {e}")

# Write the data to the EDF file
try:
    f.writeSamples(data)
except Exception as e:
    print(f"Error writing samples: {e}")

# Close the EDF file
f.close()

print(f'Data successfully saved to {edf_file_path}')

# Load the EDF file as raw data
raw = mne.io.read_raw_edf(edf_file_path)

# Save the raw data as a .fif file
fif_file_path = 'outputs/A01EConvertedFromCSV.fif'  # Replace with your desired output .fif file path
raw.save(fif_file_path, overwrite=True)

print(f'Data successfully saved to {fif_file_path}')

# Load the .fif file
raw_fif = mne.io.read_raw_fif(fif_file_path)

# Save the .fif file as a GDF file
gdf_file_path = 'outputs/A01EConvertedFromCSV.gdf'  # Replace with your desired output GDF file path
raw_fif.save(gdf_file_path, fmt='gdf', overwrite=True)

print(f'Data successfully saved to {gdf_file_path}')
