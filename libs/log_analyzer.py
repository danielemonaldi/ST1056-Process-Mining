from pm4py.statistics.traces.generic.log import case_statistics as cs

def basic_statistics(log):
    """
    === Basic statistics ===
    - Print the total number of cases (traces) in the log
    - Calculate and print the total number of events
    - Extract and print all unique activities sorted alphabetically
    """
    # Total number of cases (traces)
    print(f"\nNumber of cases (traces): {len(log)}")
    
    # Total number of events by summing the length of all traces
    total_events = sum(len(trace) for trace in log)
    print(f"Total number of events: {total_events}")
    
    # Extract and sort unique activities
    activities = sorted({event["concept:name"] for trace in log for event in trace})
    print(f"\nActivities ({len(activities)}):")
    for activity in activities:
        print(f"  - {activity}")

def variant_statistics(log, top_n=5):
    """
    === Variant statistics ===
    - Calculate variant statistics: each variant represents a unique sequence of activities in a case
    - Sort variants by frequency (number of cases) descending
    - Print the total number of distinct variants
    - Print the top_n most frequent variants with their case counts
    """
    # Get variant statistics
    variant_stats = cs.get_variant_statistics(log)
    # Sort variants by count descending
    variant_stats = sorted(variant_stats, key=lambda x: x["count"], reverse=True)
    
    # Print total number of distinct variants
    print(f"\nNumber of variants: {len(variant_stats)}")
    print(f"Top {top_n} variants:")
    for v in variant_stats[:top_n]:
        print(f"   - {v['variant']} → {v['count']} cases")

def case_duration_statistics(log):
    """
    === Case duration (if timestamps are available) ===
    - Calculate the duration of each case as the difference between the first and last event timestamps
    - Filter out any non-positive durations (invalid durations)
    - Calculate and print summary statistics of case durations (average, minimum, maximum) in minutes
    - If no valid timestamps are found, print a warning message
    """
    # Get the duration of each case as timedelta objects
    durations = cs.get_all_case_durations(log, parameters={"format": "timedelta"})
    # Filter only positive durations
    durations_sec = [d for d in durations if d > 0]

    # If there are valid durations, calculate and print summary statistics
    if durations_sec:
        print("\nCase duration statistics:")
        # Average duration in minutes (sum of durations divided by number of cases, converted from seconds)
        print(f"   - Average: {round(sum(durations_sec)/len(durations_sec)/60, 2)} minutes")
        # Minimum duration in minutes
        print(f"   - Minimum: {round(min(durations_sec)/60, 2)} minutes")
        # Maximum duration in minutes
        print(f"   - Maximum: {round(max(durations_sec)/60, 2)} minutes")
    else:
        # Warning message if no valid timestamps were found
        print("\nNo valid timestamps found in the cases.")

def analyze_log(log):
    """
    Main function that calls all the log analysis functions:
    - Basic statistics
    - Variant statistics
    - Case duration statistics
    """
    basic_statistics(log)
    variant_statistics(log)
    case_duration_statistics(log)
