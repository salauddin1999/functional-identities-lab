import argparse
import json
from .inverse import solve

parser = argparse.ArgumentParser(description="Solve inverse identities on M_2(F_p).")
parser.add_argument("--prime", type=int, default=3)
parser.add_argument("--exponent", type=int, default=3)
parser.add_argument("--same-map", action="store_true", help="Impose f=g")
args = parser.parse_args()
print(json.dumps(solve(args.prime, args.exponent, args.same_map), indent=2))
