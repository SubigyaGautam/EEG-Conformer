import mne
import matplotlib.pyplot as plt

def plot_gdf_comparison(file1, file2):
    # Load the first GDF file
    raw1 = mne.io.read_raw_gdf(file1, preload=True)
    
    # Load the second GDF file
    raw2 = mne.io.read_raw_gdf(file2, preload=True)

    # Plot the data
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    # Plot data from the first file
    raw1.plot(scalings='auto', ax=axes[0], show=False)
    axes[0].set_title('File 1: ' + file1)

    # Plot data from the second file
    raw2.plot(scalings='auto', ax=axes[1], show=False)
    axes[1].set_title('File 2: ' + file2)

    plt.tight_layout()
    plt.show()

# Replace 'file1.gdf' and 'file2.gdf' with the paths to your GDF files
file1 = 'outputs\A01E_OG.gdf'
file2 = 'outputs\A01EConvertedFromCSV.gdf'
plot_gdf_comparison(file1, file2)
