from pm4py.objects.log.importer.xes.importer import apply as import_xes
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.algo.evaluation.replay_fitness.variants import token_replay as token_fitness
from pm4py.algo.evaluation.replay_fitness.variants import alignment_based as alignment_fitness
import os

# === PATH setup ===
# Get the directory where the current script is located
base_dir = os.path.dirname(__file__)
# Move one directory up to set the project root (assumes this structure)
project_root = os.path.abspath(os.path.join(base_dir, ".."))
# Define the full path to the input XES log file
file_path = os.path.join(project_root, "logs", "log.xes")

# Directory to save all results (models, images, etc.)
results_dir = os.path.join(project_root, "results")
# Create the results directory if it doesn't already exist
os.makedirs(results_dir, exist_ok=True)

# === Import the XES log ===
# Load the event log from the XES file into PM4Py's log object
log = import_xes(file_path)

# ====== Model Discovery ======

# Alpha Miner algorithm:
# Discover a Petri net model from the log using Alpha Miner
net_alpha, im_alpha, fm_alpha = alpha_miner.apply(log)
# Visualize the Petri net
gviz_alpha = pn_visualizer.apply(net_alpha, im_alpha, fm_alpha)
# Save the visualization as a PNG image in the results directory
alpha_path = os.path.join(results_dir, "alpha_net.png")
pn_visualizer.save(gviz_alpha, alpha_path)

# Heuristics Miner algorithm:
# Discover a Petri net model from the log using Heuristics Miner
net_heur, im_heur, fm_heur = heuristics_miner.apply(log)
# Visualize the Petri net
gviz_heur = pn_visualizer.apply(net_heur, im_heur, fm_heur)
# Save the visualization as a PNG image in the results directory
heur_path = os.path.join(results_dir, "heuristics_net.png")
pn_visualizer.save(gviz_heur, heur_path)

# ====== Conformance Checking ======

# Token-based replay conformance checking:
# Replay the log on the Petri net models using token-based replay technique
alpha_token = token_replay.apply(log, net_alpha, im_alpha, fm_alpha, variant=token_replay.Variants.TOKEN_REPLAY)
heur_token = token_replay.apply(log, net_heur, im_heur, fm_heur, variant=token_replay.Variants.TOKEN_REPLAY)

# Alignment-based conformance checking:
# Compute alignments between the log and the Petri nets (this gives a more precise conformance metric)
# Note: alpha miner alignment computation is commented out, possibly due to performance or errors
# alpha_align = alignments.apply_log(log, net_alpha, im_alpha, fm_alpha)
heur_align = alignments.apply_log(log, net_heur, im_heur, fm_heur)

# Calculate token-based replay fitness values (how well the model can replay the log tokens)
alpha_token_fitness = token_fitness.evaluate(alpha_token)["log_fitness"]
heur_token_fitness = token_fitness.evaluate(heur_token)["log_fitness"]

# Calculate alignment-based fitness values (how well the model aligns with the log)
# alpha_align_fitness = alignment_fitness.evaluate(alpha_align)["log_fitness"]
heur_align_fitness = alignment_fitness.evaluate(heur_align)["log_fitness"]

# ====== Output results ======
print("=== Token-based Fitness ===")
print(f"Alpha Miner:     {alpha_token_fitness:.4f}")
print(f"Heuristic Miner: {heur_token_fitness:.4f}")

print("\n=== Alignment-based Fitness ===")
# Uncomment if alpha miner alignment fitness is computed
# print(f"Alpha Miner:     {alpha_align_fitness:.4f}")
print(f"Heuristic Miner: {heur_align_fitness:.4f}")
