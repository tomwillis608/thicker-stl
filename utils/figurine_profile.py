"""Profile some figures to study base thickness.
Use only figures with licences that allow them to be included
in the data folder."""

import csv
import os

import matplotlib.pyplot as plt
import numpy as np
from stl import mesh


def plot_figurine_radii(stl_file, label, output_csv):
    # Load STL file
    figure_mesh = mesh.Mesh.from_file(stl_file)
    vertices = figure_mesh.vectors.reshape(-1, 3)

    # Determine z bounds
    z_min, z_max = vertices[:, 2].min(), vertices[:, 2].max()
    total_height = z_max - z_min

    # Define height intervals
    z_intervals = np.linspace(z_min, z_max, 100)
    max_radii = []

    # Calculate max radius at each interval
    for z in z_intervals:
        slice_vertices = vertices[
            (vertices[:, 2] >= z) & (vertices[:, 2] < z + (total_height / 100))
        ]
        if len(slice_vertices) > 0:
            radii = np.sqrt(slice_vertices[:, 0] ** 2 + slice_vertices[:, 1] ** 2)
            max_radii.append(radii.max())
        else:
            max_radii.append(None)  # No data for this height slice

    # Normalize data
    normalized_height = (z_intervals - z_min) / total_height
    normalized_radii = [
        r / max(filter(None, max_radii)) if r is not None else None for r in max_radii
    ]

    # Save data to CSV
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Normalized Height", "Normalized Radius"])
        for h, r in zip(normalized_height, normalized_radii):
            writer.writerow([h, r] if r is not None else [h, "No Data"])

    # Plot data
    plt.plot(
        normalized_height, normalized_radii, label=label, linestyle="-", marker="o"
    )


def generate_plots_from_test_data(data_folder):
    """
    Generates plots and CSVs for STL files in a given folder with the 'test_' prefix.

    Parameters:
        data_folder (str): Path to the folder containing test STL files.
    """
    for file_name in os.listdir(data_folder):
        if file_name.startswith("test_") and file_name.endswith(".stl"):
            stl_path = os.path.join(data_folder, file_name)
            csv_name = file_name.replace(".stl", ".csv")
            csv_path = os.path.join(data_folder, csv_name)
            label = file_name.replace("test_", "").replace(".stl", "").capitalize()

            # Plot and save data
            plot_figurine_radii(stl_path, label, csv_path)
            print(f"Processed: {file_name} -> {csv_name}")


# Usage
plt.figure()
generate_plots_from_test_data("utils/data")
plt.xlabel("Normalized Height (z)")
plt.ylabel("Normalized Radius")
plt.legend()
plt.grid()
plt.title("Radius vs. Height for Figurines")
plt.savefig("utils/data/radius_vs_height_for_figures.png")
plt.show()
