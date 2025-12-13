import pandas as pd
import numpy as np
import networkx as nx
from sklearn.linear_model import Ridge
import argparse

def infer_rbp_activity(diff_as_path, network_path, output_path):
    # Step 1: Read differential splicing results from rMATS
    ds = pd.read_csv(diff_as_path, sep='\t',dtype={'exonStart_0base': str,'exonEnd': str})
    ds['IncLevelDifference'] = ds['IncLevelDifference'] * 100  
    ds['name'] = (ds['geneSymbol'] + '_' + ds['exonStart_0base'].astype(str) + '_' + ds['exonEnd'].astype(str))
    
    # Step 2: Filter significant splicing events
    filtered_ds = ds[(ds['PValue'] <= 0.05)]

    # Step 3: Load splicing regulatory network
    G = nx.read_gexf(network_path)

    # Step 4: Identify RBP nodes and target splicing event nodes
    rbps = [node for node, data in G.nodes(data=True) if data.get('type') == 'RBP']
    targets = [node for node, data in G.nodes(data=True) if data.get('type') == 'SplicingEvent']
    all_targets = sorted(set(targets))

    # Step 5: Prepare the vector of observed splicing changes
    y = []
    for target in all_targets:
        if target in filtered_ds['name'].values:
            y.append(filtered_ds.loc[filtered_ds['name'] == target, 'IncLevelDifference'].values[0])
        else:
            y.append(0.0)
    y = np.array(y)

    # Step 6: Construct the design matrix from edge weights
    X = np.zeros((len(all_targets), len(rbps)))
    for i, target in enumerate(all_targets):
        for j, rbp in enumerate(rbps):
            if G.has_edge(rbp, target):
                X[i, j] = G[rbp][target].get('weight', 0.0)

    # Step 7: Fit ridge regression model
    model = Ridge(alpha=1.0)
    model.fit(X, y)

    # Step 8: Save and display RBP activity scores
    activity_scores = model.coef_
    ranked_rbps = sorted(zip(rbps, activity_scores), key=lambda x: x[1], reverse=True)

    with open(output_path, 'w') as f:
        for rbp, score in ranked_rbps:
            f.write(f"{rbp}\t{score:.4f}\n")

    # Optional: print to console
    for rbp, score in ranked_rbps:
        print(f"{rbp}: {score:.4f}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Infer RBP activity from a splicing regulatory network using ridge regression.")
    parser.add_argument('--diffAS', required=True, help='Path to the rMATS differential splicing results file')
    parser.add_argument('--network', required=True, help='Path to the splicing regulatory network')
    parser.add_argument('--output', required=True, help='Output file for inferred RBP activity scores')

    args = parser.parse_args()
    infer_rbp_activity(args.diffAS, args.network, args.output)
