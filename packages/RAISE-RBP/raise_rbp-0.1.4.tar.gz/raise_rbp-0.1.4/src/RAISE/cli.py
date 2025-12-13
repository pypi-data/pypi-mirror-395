import argparse
from RAISE import find_target, construct_network, calculate_activity

def main():
    parser = argparse.ArgumentParser(description="RAISE: RBP Activity Inference from Splicing Events")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subcommand: find_target
    parser_find = subparsers.add_parser("find_target", help="EM algorithm for inferring RBP targets using motif, CLIP peaks, and PSI changes.")
    parser_find.add_argument('--rmats', required=True)
    parser_find.add_argument('--clip_peaks', required=True)
    parser_find.add_argument('--ref_genome', required=True)
    parser_find.add_argument('--rbp_motif', required=True)
    parser_find.add_argument('--cell_line', required=True)
    parser_find.add_argument('--rbp', required=True)
    parser_find.add_argument('--output', required=True)
    parser_find.add_argument('--max_iter', type=int, default=1000)
    parser_find.add_argument('--tol', type=float, default=1e-4)

    # Subcommand: construct_network
    parser_net = subparsers.add_parser("construct_network", help="Build a splicing regulatory network from find target outputs and differential expression data.")
    parser_net.add_argument('--Target_dir', required=True)
    parser_net.add_argument('--threshold', type=float, default=0.6)
    parser_net.add_argument('--DE_dir', required=True)
    parser_net.add_argument('--output', required=True)

    # Subcommand: calculate_activity
    parser_act = subparsers.add_parser("calculate_activity", help="Estimate RBP activity")
    parser_act.add_argument('--diffAS', required=True)
    parser_act.add_argument('--network', required=True)
    parser_act.add_argument('--out', required=True)

    args = parser.parse_args()

    if args.command == "find_target":
        find_target.main(args)
    elif args.command == "construct_network":
        construct_network.main(args)
    elif args.command == "calculate_activity":
        calculate_activity.main(args)

if __name__ == "__main__":
    main()
