import numpy as np
import aocs_lab.utils.constants as const
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.dates as mdates
from datetime import timedelta, datetime
import re

def calc_du(a, da, da_dot, t):
    n = np.sqrt(const.GM_EARTH / a**3)
    k = -3*n / (2*a)
    du = k * (da * t + 0.5 * da_dot * t**2)

    return du

def law_of_cosines(a, b, gamma):
    """
    https://en.wikipedia.org/wiki/Law_of_cosines
    """
    return np.sqrt(a**2 + b**2 - 2*a*b*np.cos(gamma))

def main():
    a = 6913e3
    da = 0
    # a_dot_C01 = -(6904.1e3 - 6901.7e3) / (30 * 86400)
    a_dot_C01 = 0
    a_dot_TJY01 = -(6904.9e3 - 6901.7e3) / (30 * 86400)
    da_dot = a_dot_TJY01 - a_dot_C01
    t = 30 * 86400
    du = calc_du(a, da, da_dot, t)
    print(np.rad2deg(du))

    du_init = np.deg2rad(-12)
    du_final = du_init + du
    distance = law_of_cosines(a, a, du_final)
    print(f"星间距离: {distance/1e3:.2f} km")


def plot_beta_angle(file_path):
    # File path to beta angle data
    
    # Read the data from the file
    dates = []
    beta_angles = []
    
    with open(file_path, 'r') as file:
        # Skip header lines
        for _ in range(4):
            next(file)
        
        # Read each line of data
        for line in file:
            line = line.strip()
            if not line or "Time (UTCG)" in line or "---------" in line:
                continue
            
            parts = line.split()
            if len(parts) >= 5:  # Ensure line has enough data
                # Parse date and beta angle
                date_str = f"{parts[0]} {parts[1]} {parts[2]} {parts[3]}"
                beta_angle = float(parts[4])
                
                # Convert date string to datetime object
                date = datetime.strptime(date_str, "%d %b %Y %H:%M:%S.%f")
                
                dates.append(date)
                beta_angles.append(beta_angle)
    
    # Convert to numpy arrays for easier processing
    dates = np.array(dates)
    beta_angles = np.array(beta_angles)
    
    # Find the minimum and maximum beta angle values and their corresponding dates
    min_idx = np.argmin(beta_angles)
    max_idx = np.argmax(beta_angles)
    
    min_beta = beta_angles[min_idx]
    max_beta = beta_angles[max_idx]
    min_date = dates[min_idx]
    max_date = dates[max_idx]
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    
    # Set the style of the plot
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Arial']
    
    # Plot the data
    plt.plot(dates, beta_angles, 'b-', linewidth=1.5)
    
    # Mark the minimum and maximum points
    plt.plot(min_date, min_beta, 'ro', markersize=8, label=f'Min: {min_beta:.2f}° ({min_date.strftime("%d %b %Y")})')
    plt.plot(max_date, max_beta, 'go', markersize=8, label=f'Max: {max_beta:.2f}° ({max_date.strftime("%d %b %Y")})')
    
    # Format the x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    
    # Add labels and title
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Beta Angle (degrees)', fontsize=12)
    plt.title('Solar Beta Angle Variation (2026-2027)', fontsize=14)
    
    # Add grid and legend
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='best', fontsize=10)
    
    # Rotate date labels for better readability
    plt.gcf().autofmt_xdate()
    
    # Add text annotations for min and max values
    plt.annotate(f'{min_beta:.2f}°', 
                 xy=(min_date, min_beta),
                 xytext=(10, -20),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle='->'))
    
    plt.annotate(f'{max_beta:.2f}°', 
                 xy=(max_date, max_beta),
                 xytext=(10, 20),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle='->'))
    
    plt.tight_layout()
    plt.savefig('beta_angle_plot.png', dpi=300)
    plt.show()


def plot_umbra_times(file_path):
    """
    Plot umbra times data from the given text file.
    
    Args:
        file_path (str): Path to the text file containing lighting times data
    """
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Extract the Umbra Times section, excluding the Global Statistics part
    umbra_section_match = re.search(r'Umbra Times\s*-+\s*(.*?)(?:\n\s*Global Statistics|$)', content, re.DOTALL)
    
    if not umbra_section_match:
        print("Umbra Times section not found in the file.")
        return
    
    umbra_section = umbra_section_match.group(1)
    
    # Extract data using regex
    # Looking for lines with start date/time, stop date/time, and duration
    pattern = r'(\d{1,2} [A-Za-z]+ \d{4} \d{2}:\d{2}:\d{2}\.\d+)\s+(\d{1,2} [A-Za-z]+ \d{4} \d{2}:\d{2}:\d{2}\.\d+)\s+(\d+\.\d+)'
    matches = re.findall(pattern, umbra_section)
    
    if not matches:
        print("No umbra times data found in the file.")
        return
    
    # Process regular matches
    dates = []
    durations = []
    
    # Convert matches to a list of dictionaries for easier processing
    parsed_matches = [
        {
            "start": datetime.strptime(match[0], "%d %b %Y %H:%M:%S.%f"),
            "end": datetime.strptime(match[1], "%d %b %Y %H:%M:%S.%f"),
            "duration": float(match[2])
        }
        for match in matches
    ]
    
    # Sort by start time
    parsed_matches.sort(key=lambda x: x["start"])
    
    # Remove the earliest start time and the latest end time
    if len(parsed_matches) > 2:
        filtered_matches = parsed_matches[1:-1]
        print(f"Removed earliest and latest umbra times entries. Processing {len(filtered_matches)} entries.")
    else:
        filtered_matches = parsed_matches
        print("Not enough entries to remove first and last. Using all available data.")
    
    for match in filtered_matches:
        dates.append(match["start"])
        durations.append(match["duration"])
    
    # Convert to numpy arrays
    dates = np.array(dates)
    durations = np.array(durations)
    
    # Find significant time gaps in the data (periods with no data)
    # Sort dates if they aren't already
    sort_idx = np.argsort(dates)
    sorted_dates = dates[sort_idx]
    sorted_durations = durations[sort_idx]
    
    # Define what constitutes a significant gap (e.g., more than 30 days)
    gap_threshold = timedelta(days=30)
    gaps = []
    
    for i in range(1, len(sorted_dates)):
        date_diff = sorted_dates[i] - sorted_dates[i-1]
        if date_diff > gap_threshold:
            gaps.append((sorted_dates[i-1], sorted_dates[i]))
    
    # Find min and max durations
    min_idx = np.argmin(durations)
    max_idx = np.argmax(durations)
    
    min_duration = durations[min_idx]
    max_duration = durations[max_idx]
    min_date = dates[min_idx]
    max_date = dates[max_idx]
    
    # Convert seconds to minutes for better readability
    durations_minutes = durations / 60
    min_duration_minutes = min_duration / 60
    max_duration_minutes = max_duration / 60
    
    # Create the plot
    plt.figure(figsize=(12, 7))
    
    # Set plot style
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Arial']
    
    # Plot the data using scatter points instead of lines
    plt.scatter(dates, durations_minutes, c='blue', s=30, alpha=0.7, 
                edgecolor='none', label='Umbra Duration')
    
    # Mark the minimum and maximum points
    plt.scatter(min_date, min_duration_minutes, c='red', s=100, marker='o', 
                label=f'Min: {min_duration_minutes:.2f} minutes ({min_date.strftime("%d %b %Y")})')
    plt.scatter(max_date, max_duration_minutes, c='green', s=100, marker='o', 
                label=f'Max: {max_duration_minutes:.2f} minutes ({max_date.strftime("%d %b %Y")})')
    
    # Highlight significant data gaps (periods with no data)
    gap_labels_added = False
    for i, (gap_start, gap_end) in enumerate(gaps):
        # Use semi-transparent yellow to highlight the gap area
        plt.axvspan(gap_start, gap_end, color='yellow', alpha=0.3)
        
        # Add the gap label just once to avoid cluttering the legend
        if not gap_labels_added:
            plt.axvspan(gap_start, gap_end, color='yellow', alpha=0.3, label='No Umbra Period')
            gap_labels_added = True
        
        # Calculate y position for annotations to avoid overlapping
        y_pos = max_duration_minutes * (0.9 - i * 0.1)
        if y_pos < min_duration_minutes:
            y_pos = min_duration_minutes * (1.1 + i * 0.1)
        
        # Annotate the gap start date
        plt.annotate(f'Gap Start: {gap_start.strftime("%d %b %Y")}', 
                     xy=(gap_start, y_pos),
                     xytext=(10, 20),
                     textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                     bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="red", alpha=0.8))
        
        # Annotate the gap end date
        plt.annotate(f'Gap End: {gap_end.strftime("%d %b %Y")}', 
                     xy=(gap_end, y_pos),
                     xytext=(-10, -20),
                     textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', color='green', lw=1.5),
                     bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", alpha=0.8))
    
    # Format the x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    
    # Add labels and title
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Umbra Duration (minutes)', fontsize=12)
    plt.title('Satellite Umbra Duration Over Time (2026-2027)', fontsize=14)
    
    # Add grid and legend
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='best', fontsize=10)
    
    # Rotate date labels for better readability
    plt.gcf().autofmt_xdate()
    
    # Add text annotations for min and max values
    plt.annotate(f'{min_duration_minutes:.2f} mins', 
                 xy=(min_date, min_duration_minutes),
                 xytext=(10, -20),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle='->'))
    
    plt.annotate(f'{max_duration_minutes:.2f} mins', 
                 xy=(max_date, max_duration_minutes),
                 xytext=(10, 20),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle='->'))
    
    plt.tight_layout()
    plt.savefig('umbra_duration_plot.png', dpi=300)
    plt.show()


if __name__ == "__main__":
    # main()

    # plot_beta_angle(r"d:\dev\aocs_lab\tests\orbit\C01 Beta Angle.txt")
    plot_umbra_times(r"d:\dev\aocs_lab\tests\orbit\D01 Lighting Times.txt")

