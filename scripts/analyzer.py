from pm4py.objects.log.importer.xes.importer import apply as import_xes
from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.statistics.traces.generic.log import case_statistics as cs
import os

# === PATH setup ===
# Get the directory of the current script
base_dir = os.path.dirname(__file__)
# Navigate one level up assuming the project root is the parent directory
project_root = os.path.abspath(os.path.join(base_dir, ".."))
# Construct the full path to the XES log file
file_path = os.path.join(project_root, "logs", "log.xes")

# === STEP 1: Import the XES log ===
# Import the XES log file into a PM4Py log object
log = import_xes(file_path)

# === STEP 2: Basic statistics ===
# Print the total number of cases (traces) in the log
print(f"\nNumber of cases (traces): {len(log)}")

# Calculate the total number of events by summing the lengths of all traces
total_events = sum(len(trace) for trace in log)
print(f"Total number of events: {total_events}")

# Extract all unique activities (event["concept:name"]) from the log and sort them alphabetically
activities = sorted({event["concept:name"] for trace in log for event in trace})
print(f"\nActivities ({len(activities)}):")
# Print each activity on a new line as a bullet point list
for activity in activities:
    print(f"  - {activity}")

# === STEP 3: Variant statistics ===
# Get the variant statistics: each variant represents a unique sequence of activities in a case
variant_stats = cs.get_variant_statistics(log)
# Sort variants by their frequency (number of cases) in descending order
variant_stats = sorted(variant_stats, key=lambda x: x["count"], reverse=True)

# Print the total number of distinct variants
print(f"\nNumber of variants: {len(variant_stats)}")
print("🔝 Top 5 variants:")
# Print the top 5 most frequent variants along with their case counts
for v in variant_stats[:5]:
    print(f"   - {v['variant']} → {v['count']} cases")

# === STEP 4: Case duration (if timestamps are available) ===
# Calculate the duration of each case (difference between first and last event timestamps)
# This requires valid timestamps to be present in the log
durations = cs.get_all_case_durations(log, parameters={"format": "timedelta"})

# Filter out any non-positive durations (invalid durations)
durations_sec = [d for d in durations if d > 0]

# If there are valid durations, calculate and print summary statistics
if durations_sec:
    print("\n📈 Case duration statistics:")
    # Average duration in minutes (sum of durations divided by number of cases, converted from seconds)
    print(f"   - Average: {round(sum(durations_sec)/len(durations_sec)/60, 2)} minutes")
    # Minimum duration in minutes
    print(f"   - Minimum: {round(min(durations_sec)/60, 2)} minutes")
    # Maximum duration in minutes
    print(f"   - Maximum: {round(max(durations_sec)/60, 2)} minutes")
else:
    # Warning message if no valid timestamps were found
    print("\nNo valid timestamps found in the cases.")
