from pm4py.objects.log.importer.xes.importer import apply as import_xes
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments
from pm4py.algo.evaluation.replay_fitness.variants import token_replay as token_fitness
from pm4py.algo.evaluation.replay_fitness.variants import alignment_based as alignment_fitness
import os

# Setup percorsi
base_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(base_dir, ".."))
file_path = os.path.join(project_root, "logs", "log.xes")

results_dir = os.path.join(project_root, "results")
os.makedirs(results_dir, exist_ok=True)

# Carica log
log = import_xes(file_path)

# ====== Scoperta modelli ======
# Alpha Miner
net_alpha, im_alpha, fm_alpha = alpha_miner.apply(log)
gviz_alpha = pn_visualizer.apply(net_alpha, im_alpha, fm_alpha)
alpha_path = os.path.join(results_dir, "alpha_net.png")
pn_visualizer.save(gviz_alpha, alpha_path)

# Heuristics Miner
net_heur, im_heur, fm_heur = heuristics_miner.apply(log)
gviz_heur = pn_visualizer.apply(net_heur, im_heur, fm_heur)
heur_path = os.path.join(results_dir, "heuristics_net.png")
pn_visualizer.save(gviz_heur, heur_path)

# ====== Conformance checking ======

# Token-based replay
alpha_token = token_replay.apply(log, net_alpha, im_alpha, fm_alpha, variant=token_replay.Variants.TOKEN_REPLAY)
heur_token = token_replay.apply(log, net_heur, im_heur, fm_heur, variant=token_replay.Variants.TOKEN_REPLAY)

# Alignment-based fitness
#alpha_align = alignments.apply_log(log, net_alpha, im_alpha, fm_alpha)
heur_align = alignments.apply_log(log, net_heur, im_heur, fm_heur)

alpha_token_fitness = token_fitness.evaluate(alpha_token)["log_fitness"]
heur_token_fitness = token_fitness.evaluate(heur_token)["log_fitness"]

#alpha_align_fitness = alignment_fitness.evaluate(alpha_align)["log_fitness"]
heur_align_fitness = alignment_fitness.evaluate(heur_align)["log_fitness"]

# ====== Output ======
print("=== Token-based Fitness ===")
print(f"Alpha Miner:     {alpha_token_fitness:.4f}")
print(f"Heuristic Miner: {heur_token_fitness:.4f}")

print("\n=== Alignment-based Fitness ===")
#print(f"Alpha Miner:     {alpha_align_fitness:.4f}")
print(f"Heuristic Miner: {heur_align_fitness:.4f}")