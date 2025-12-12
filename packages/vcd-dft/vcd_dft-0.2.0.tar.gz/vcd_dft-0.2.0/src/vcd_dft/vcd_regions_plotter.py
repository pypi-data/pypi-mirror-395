#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt

# --- Configuration for Highlighted Regions ---
# Add or modify the bond regions in this dictionary.
# 'Label': {'range': (start_cm-1, end_cm-1), 'color': 'color_name', 'alpha': transparency}
BOND_REGIONS = {
    '(C-F)': {
        'range': (1050, 1500),
        'color': 'purple',
        'alpha': 0.15
    },
    '(C=O)': {
        'range': (1750, 2000),
        'color': 'blue',
        'alpha': 0.15
    },
    '(O-H)': {
        'range': (3600, 3800),
        'color': 'red',
        'alpha': 0.15
    },
    '(C-H)': {
        'range': (2900, 3300),
        'color': 'green',
        'alpha': 0.15
    },
     '(C-Cl)': {
        'range': (480, 600),
        'color': 'orange',
        'alpha': 0.15
    },
}

def read_vcd_data(filename):
    """
    Reads VCD data from the summary file and returns a dictionary of molecules
    with their frequencies and intensities.
    """
    molecules = {}
    current_molecule = None
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('File:'):
                # Extract a clean name for the molecule
                current_molecule = line.split(':')[1].split('.')[0].strip()
                molecules[current_molecule] = {'frequencies': [], 'intensities': []}
            elif line.startswith('Frequencies (cm^-1)'):
                continue
            elif current_molecule and line:
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        freq = float(parts[0])
                        intensity = float(parts[1])
                        molecules[current_molecule]['frequencies'].append(freq)
                        molecules[current_molecule]['intensities'].append(intensity)
                    except ValueError:
                        # Skip lines that cannot be parsed
                        continue
    return molecules

def broaden_peaks(frequencies, intensities, width=20, x_min=0, x_max=4000, num_points=10000):
    """
    Broadens discrete peaks into a continuous spectrum using a Lorentzian lineshape.
    """
    x = np.linspace(x_min, x_max, num_points)
    y = np.zeros_like(x)
    
    # Create the spectrum by summing up Lorentzian peaks
    for freq, inten in zip(frequencies, intensities):
        y += inten * (width / 2)**2 / ((x - freq)**2 + (width / 2)**2)
    
    return x, y

def plot_vcd_spectrum_with_regions(molecule_name, frequencies, intensities, output_folder, width=15, bond_regions=BOND_REGIONS):
    """
    Plots the VCD spectrum for a single molecule, highlights specified regions,
    and saves the plot to a file.
    """
    x, y = broaden_peaks(frequencies, intensities, width=width)
    
    plt.figure(figsize=(14, 7))
    
    # Plot the VCD spectrum line
    plt.plot(x, y, 'b-', linewidth=1.5, label='VCD Spectrum')
    
    # Plot the original discrete peaks as vertical lines
    plt.vlines(frequencies, 0, intensities, colors='k', linestyles='--', linewidth=0.5, alpha=0.5, label='Discrete Peaks')
    
    # --- Highlight and Label Bond Regions ---
    y_min, y_max = plt.ylim()
    for label, region in bond_regions.items():
        start, end = region['range']
        color = region['color']
        alpha = region['alpha']
        
        # Use axvspan to create the highlighted vertical region
        plt.axvspan(start, end, color=color, alpha=alpha, zorder=0)
        
        # Add a text label for the region
        plt.text(
            (start + end) / 2,  # Horizontal center of the region
            y_max * 0.9,        # Position near the top of the plot
            label,
            horizontalalignment='center',
            verticalalignment='top',
            fontsize=12,
            fontweight='bold',
            color=color
        )

    # --- Final Plot Formatting ---
    plt.title(f'Predicted VCD Spectrum for {molecule_name}', fontsize=16)
    plt.xlabel('Wavenumber (cm⁻¹)', fontsize=12)
    plt.ylabel('VCD Intensity (1E-44*esu²*cm²)', fontsize=12)
    plt.gca().invert_xaxis()  # Invert x-axis for standard spectroscopy view
    plt.grid(linestyle='--', alpha=0.6)
    plt.axhline(0, color='black', linewidth=0.8) # Add a zero line
    plt.legend()

    # Save the figure to the specified output folder
    filename = os.path.join(output_folder, f"{molecule_name}_VCD_regions.png")
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot: {filename}")

def plot_all_from_summary(summary_file, output_folder, width=15):
    """
    Reads the summary file and plots VCD spectra for all molecules found.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")

    molecules = read_vcd_data(summary_file)
    
    if not molecules:
        print("No molecule data found in the summary file.")
        return

    for name, data in molecules.items():
        if data['frequencies'] and data['intensities']:
            plot_vcd_spectrum_with_regions(name, data['frequencies'], data['intensities'], output_folder, width=width)
        else:
            print(f"Skipping {name} due to missing data.")

# --- Main Execution Block ---
def gen_regions_plots():
    # The script will look for this file in the directory it is run from.
    summary_filename = "vcd_frequencies_intensities_summary.txt"
    
    # Define the folder where the output plots will be saved.
    output_plot_folder = os.path.join(os.getcwd(), 'VCD_Spectra_Plots_With_Regions')

    # Check if the summary file exists
    if os.path.exists(summary_filename):
        print(f"Found summary file: {summary_filename}")
        plot_all_from_summary(summary_filename, output_plot_folder, width=15)
        print("\nProcessing complete.")
    else:
        print(f"Error: The summary file '{summary_filename}' was not found in the current directory.")
        print("Please make sure the summary file is present before running this script.")
    


