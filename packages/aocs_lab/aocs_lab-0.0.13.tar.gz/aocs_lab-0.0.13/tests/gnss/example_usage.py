from excel_reader import ExcelReader
import pandas as pd
import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.append(parent_dir)
from aocs_lab.utils import lib

import numpy as np
import matplotlib.pyplot as plt

def example_read_excel():
    """Example of different ways to read Excel data"""
    
    # Replace with your actual Excel file path
    file_path = r"C:\Users\Administrator\Desktop\PIESAT02_C01-20250407-20250407_XXXX.xlsx"
    
    reader = ExcelReader(file_path)
    
    # Method 1: Read all data from default sheet
    print("=== Method 1: Read all data ===")
    all_data = reader.read_sheet_data()
    for i, row in enumerate(all_data[:3]):
        print(f"Row {i+1}: {row}")
    
    # Method 2: Read specific sheet
    print("\n=== Method 2: Read specific sheet ===")
    sheets = reader.get_sheet_names()
    if sheets:
        sheet_data = reader.read_sheet_data(sheets[0])
        print(f"Sheet '{sheets[0]}' has {len(sheet_data)} rows")
    
    # Method 3: Read specific range
    print("\n=== Method 3: Read specific range ===")
    if sheets:
        range_data = reader.read_range(sheets[0], 'A1', 'C5')
        print("Range A1:C5:")
        for row in range_data:
            print(row)
    
    # Method 4: Use pandas for advanced operations
    print("\n=== Method 4: Use pandas ===")
    df = reader.read_with_pandas()
    if not df.empty:
        print(f"DataFrame info:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst few rows:")
        print(df.head())

def read_excel():
    # Replace with your actual Excel file path
    file_path = r"PIESAT02_C01-20250407-20250407_XXXX.xlsx"
    
    reader = ExcelReader(file_path)
    
    all_data = reader.read_sheet_data()

    # print(all_data)

    timeline = []
    gnss_angles = []
    omega_norm = []
    for i, row in enumerate(all_data[1:]):
        # print(f"Row {i+1}: {row[3:7]}")
        q_BO = row[3:7]
        dcm_BO = lib.quat2dcm(q_BO)
        gnss_B = np.array([0, np.cos(np.deg2rad(60)), -np.sin(np.deg2rad(60))])
        gnss_O = dcm_BO.T @ gnss_B
        sky_vector_O = np.array([0, 0, -1])
        gnss_angles.append(lib.vector_angle(gnss_O, sky_vector_O))

        timeline.append(row[0])

        omega = np.array(row[7:10])
        omega_norm.append(np.linalg.norm(omega))


    time_data = pd.to_datetime(timeline)
    np.savetxt('gnss_angles.txt', np.rad2deg(gnss_angles), fmt='%.6f')

    fig, axs = plt.subplots(2, 1, figsize=(12, 10))
    axs[0].plot(time_data, np.rad2deg(gnss_angles) , marker='o', linestyle='-', color='b')
    axs[0].set_title('GNSS Angles Over Time')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Angle (degrees)')
    axs[0].grid()

    axs[1].plot(time_data, omega_norm, marker='o', linestyle='-', color='r')
    axs[1].set_title('Angular Velocity Norm Over Time')
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Angular Velocity Norm (rad/s)')
    axs[1].grid()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    read_excel()
