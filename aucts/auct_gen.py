import argparse
import random


def parse_args():
    parser = argparse.ArgumentParser(
        description="Random instance generator for the Combinatorial Auction problem.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--n-agents", "-a", type=int, help="Number of agents", required=True
    )
    parser.add_argument(
        "--n-goods", "-g", type=int, help="Number of goods", required=True
    )
    parser.add_argument(
        "--min-bids-per-agent",
        type=int,
        help="Minimum number of bids per agent",
        default=1,
    )
    parser.add_argument(
        "--max-bids-per-agent",
        type=int,
        help="Maximum number of bids per agent",
        default=3,
    )
    parser.add_argument(
        "--max-bid-price", type=int, default=100, help="Maximum price on a bid"
    )
    parser.add_argument("--seed", "-s", type=int, help="RNG Seed", default=1)
    return parser.parse_args()


def main(args):
    # Initialize the random seed
    random.seed(args.seed)
    # Create the list of agents
    agents = [f"a{i}" for i in range(args.n_agents)]
    # Create the list of goods
    goods = [f"g{i}" for i in range(args.n_goods)]
    # Create the list of bids
    bids = []
    for a in agents:
        n_bids = random.randint(args.min_bids_per_agent, args.max_bids_per_agent)
        for _ in range(n_bids):
            # Select a random subset of goods
            n_goods = random.randint(2, int(len(goods) / 2))
            bid_goods = random.sample(goods, n_goods)
            # Compute the price
            price = random.randint(1, args.max_bid_price)
            # Add to the list of bids
            bids.append((a, bid_goods, price))
    # Print the resulting instance to stdout
    print(f"a {' '.join(agents)}")
    print(f"g {' '.join(goods)}")
    for agent, goods, price in bids:
        print(f"{agent} {' '.join(goods)} {price}")


if __name__ == "__main__":
    args = parse_args()
    main(args)
