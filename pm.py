from pm4py.objects.log.importer.xes.importer import apply as import_xes
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.algo.evaluation.replay_fitness.variants import token_replay as token_fitness
from pm4py.algo.evaluation.replay_fitness.variants import alignment_based as alignment_fitness
from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
from tabulate import tabulate
from termcolor import colored
import os

from libs.log_analyzer import analyze_log

# === PATH setup ===
# Get the directory where the current script is located
base_dir = os.path.dirname(__file__)

# Define the full path to the input XES log file (inside a "logs" folder in the same directory)
file_path = os.path.join(base_dir, "logs", "log.xes")

# Directory to save all results (models, images, etc.)
results_dir = os.path.join(base_dir, "results")

# Create the results directory if it doesn't already exist
os.makedirs(results_dir, exist_ok=True)

# === Import the XES log ===
# Load the event log from the XES file into PM4Py's log object
print(colored("\n============= LOG parsing ==============", "yellow"))
log = import_xes(file_path)

# === Analyze LOG ===
print(colored("\n============= LOG analysis =============", "yellow"))
analyze_log(log)

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
print(colored("\n===== Executing Token based replay =====", "yellow"))
alpha_token = token_replay.apply(log, net_alpha, im_alpha, fm_alpha, variant=token_replay.Variants.TOKEN_REPLAY)
heur_token = token_replay.apply(log, net_heur, im_heur, fm_heur, variant=token_replay.Variants.TOKEN_REPLAY)

# Alignment-based conformance checking:
# Compute alignments between the log and the Petri nets (this gives a more precise conformance metric)
print(colored("\n========= Executing Alignments =========", "yellow"))
alpha_align = alignments.apply_log(log, net_alpha, im_alpha, fm_alpha)  # Uncomment if needed
heur_align = alignments.apply_log(log, net_heur, im_heur, fm_heur)

# ====== Fitness calculation ======

# Calculate token-based replay fitness values (how well the model can replay the log tokens)
alpha_token_fitness = token_fitness.evaluate(alpha_token)["log_fitness"]
heur_token_fitness = token_fitness.evaluate(heur_token)["log_fitness"]

# Calculate alignment-based fitness values (how well the model aligns with the log)
alpha_align_fitness = alignment_fitness.evaluate(alpha_align)["log_fitness"]
heur_align_fitness = alignment_fitness.evaluate(heur_align)["log_fitness"]

# ====== Additional metrics calculation ======
print(colored("\n========= Calculating metrics ==========", "yellow"))

# Calculate Precision (how precise the model is compared to the log behavior)
alpha_precision = precision_evaluator.apply(log, net_alpha, im_alpha, fm_alpha)
heur_precision = precision_evaluator.apply(log, net_heur, im_heur, fm_heur)

# Calculate Generalization (how well the model generalizes the log behavior)
alpha_generalization = generalization_evaluator.apply(log, net_alpha, im_alpha, fm_alpha)
heur_generalization = generalization_evaluator.apply(log, net_heur, im_heur, fm_heur)

# Calculate Simplicity (structural simplicity of the Petri net model)
alpha_simplicity = simplicity_evaluator.apply(net_alpha)
heur_simplicity = simplicity_evaluator.apply(net_heur)

# ====== Output results as formatted table ======

table = [
    ["Alpha Miner", alpha_token_fitness, alpha_align_fitness, alpha_precision, alpha_generalization, alpha_simplicity],
    ["Heuristic Miner", heur_token_fitness, heur_align_fitness, heur_precision, heur_generalization, heur_simplicity],
]

headers = ["Algorithm", "Fitness (Token-based)", "Fitness (Alignments)", "Precision", "Generalization", "Simplicity"]

print(colored("\n=========== Model Evaluation ===========", "green"))
print(tabulate(table, headers=headers, floatfmt=".4f", tablefmt="grid"))
