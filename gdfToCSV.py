import mne
import pandas as pd

# Load the GDF file without preloading data
file_path = 'dataset/2a/BCICIV_2a_gdf/A01E.gdf'  # Replace with your actual file path
raw = mne.io.read_raw_gdf(file_path, preload=False)

# Define chunk size (e.g., number of samples per chunk)
chunk_size = 10000
n_times = raw.n_times

# Create an empty CSV file and write the header
output_csv_path = 'outputs/A01E.csv'  # Replace with your desired output file path
with open(output_csv_path, 'w') as f:
    header = ','.join(raw.info['ch_names'] + ['time']) + '\n'
    f.write(header)

# Append chunks of data to the CSV file
for start in range(0, n_times, chunk_size):
    stop = min(start + chunk_size, n_times)
    data, times = raw[:, start:stop]
    df = pd.DataFrame(data.T, columns=raw.info['ch_names'])
    df['time'] = times
    df.to_csv(output_csv_path, mode='a', header=False, index=False)

print(f'Data successfully saved to {output_csv_path}')
