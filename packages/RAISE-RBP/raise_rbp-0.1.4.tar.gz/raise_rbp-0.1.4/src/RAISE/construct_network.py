import os
import pandas as pd
import networkx as nx
import argparse

def build_splicing_network(Target_dir, threshold, DE_dir, output_file):
    G = nx.DiGraph()

    for file_name in os.listdir(Target_dir):
        if not os.path.isdir(os.path.join(Target_dir, file_name)):
            continue  # 只处理目录
        try:
            cell_line, rbp = file_name.split('_')[:2]
        except ValueError:
            print(f"Skipping {file_name}: cannot parse cell line and RBP.")
            continue

        print(f"Processing: Cell line = {cell_line}, RBP = {rbp}")

        # 读取 target 文件
        target_path = os.path.join(Target_dir, file_name, file_name + '_target.txt')
        if not os.path.exists(target_path):
            print(f"Warning: Target file not found: {target_path}")
            continue

        target_data = pd.read_csv(target_path, sep='\t', low_memory=False)
        if 'P(T|S, M, C)' not in target_data.columns:
            print(f"Warning: 'P(T|S, M, C)' column missing in {target_path}. Skipping.")
            continue

        target_data['P(T|S, M, C)'] = pd.to_numeric(target_data['P(T|S, M, C)'], errors='coerce')

        # 默认表达变化因子
        rbp_change_factor = 1.0

        # 读取表达变化文件
        expr_file = os.path.join(DE_dir, f"{cell_line}_{rbp}_expr.txt")
        if os.path.exists(expr_file):
            expr_data = pd.read_csv(expr_file, sep='\t', header=0)
            if {'Gene', 'Ctrl', 'KD'}.issubset(expr_data.columns):
                rbp_row = expr_data[expr_data['Gene'] == rbp]
                if not rbp_row.empty:
                    try:
                        ctrl = float(rbp_row.iloc[0]['Ctrl'])
                        kd = float(rbp_row.iloc[0]['KD'])
                        rbp_change_factor = ctrl / kd if kd != 0 else 1.0
                    except Exception as e:
                        print(f"Warning: Failed to parse expression values for {rbp} in {cell_line}: {e}")
            else:
                print(f"Warning: Required columns not found in {expr_file}. Expected 'Gene', 'Ctrl', and 'KD'.")
        else:
            print(f"Warning: Expression file not found: {expr_file}. Using default factor = 1.")

        # 构建图
        for _, row in target_data.iterrows():
            if row['P(T|S, M, C)'] < threshold:
                continue

            event_id = row['event_id']
            inc_diff = row.get('IncLevelDifference', 0)
            adjusted_dpsi = inc_diff / rbp_change_factor

            # 添加节点
            if not G.has_node(rbp):
                G.add_node(rbp, type='RBP', role='source')
            if not G.has_node(event_id):
                G.add_node(event_id, type='SplicingEvent', role='target', event_id=event_id)

            # 添加或更新边
            if G.has_edge(rbp, event_id):
                existing_weight = G[rbp][event_id]['weight']
                if abs(adjusted_dpsi) > abs(existing_weight):
                    G[rbp][event_id]['weight'] = adjusted_dpsi
            else:
                G.add_edge(rbp, event_id, weight=adjusted_dpsi)

    # 保存图
    nx.write_gexf(G, output_file)
    print(f"✅ Splicing regulatory network saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a splicing regulatory network from target predictions and RBP expression changes.")
    parser.add_argument("--Target_dir", type=str, required=True, help="Directory containing RBP target result folders")
    parser.add_argument("--threshold", type=float, default=0.6, help="Minimum conditional probability P(T|S,M,C) to include interaction (default: 0.6)")
    parser.add_argument("--DE_dir", type=str, required=True, help="Directory containing RBP expression change files")
    parser.add_argument("--output", type=str, required=True, help="Path to output GEXF file for the constructed network")

    args = parser.parse_args()
    build_splicing_network(args.Target_dir, args.threshold, args.DE_dir, args.output)
