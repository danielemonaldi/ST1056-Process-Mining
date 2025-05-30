from pm4py.statistics.traces.generic.log import case_statistics as cs
from tabulate import tabulate
from termcolor import colored

def basic_statistics(log):
    """
    === Basic statistics ===
    - Print the total number of cases (traces) in the log
    - Calculate and print the total number of events
    - Extract and print all unique activities sorted alphabetically
    """
    # Total number of cases (traces)
    num_cases = len(log)
    
    # Total number of events by summing the length of all traces
    total_events = sum(len(trace) for trace in log)
    
    # Extract and sort unique activities
    activities = sorted({event["concept:name"] for trace in log for event in trace})

    # Print summary table
    summary_data = [
        ["Number of cases (traces)", num_cases],
        ["Total number of events", total_events],
        ["Number of unique activities", len(activities)]
    ]

    print(colored("\n=========== Basic Statistics ===========", "green"))
    print(tabulate(summary_data, tablefmt="grid"))

    # Print activities as a table with a single column
    print(f"\nActivities ({len(activities)}):")
    activities_table = [[activity] for activity in activities]
    print(tabulate(activities_table, headers=["Activity"], tablefmt="grid"))

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

    # Prepare top variant data for table
    top_variants = variant_stats[:top_n]
    table_data = []
    for v in top_variants:
        table_data.append([v['variant'], v['count']])
    
    print(f"Top {top_n} variants:")
    print(tabulate(table_data, headers=["Variant (Activity Sequence)", "Number of Cases"], tablefmt="grid"))

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

    if durations_sec:
        avg_duration = round(sum(durations_sec)/len(durations_sec)/60, 2)
        min_duration = round(min(durations_sec)/60, 2)
        max_duration = round(max(durations_sec)/60, 2)

        duration_data = [
            ["Average duration (minutes)", avg_duration],
            ["Minimum duration (minutes)", min_duration],
            ["Maximum duration (minutes)", max_duration]
        ]

        print(colored("\n======= Case Duration Statistics =======", "green"))
        print(tabulate(duration_data, tablefmt="grid"))
    else:
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
