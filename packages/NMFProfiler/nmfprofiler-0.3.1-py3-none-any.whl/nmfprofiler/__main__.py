from numpy import array
from nmfprofiler import NMFProfiler
from argparse import ArgumentParser


def main():
    # Create an argument parser object
    parser = ArgumentParser(
        prog="NMFProfiler",
        description="Run NMFProfiler"
    )

    # Add each argument to the parser
    parser.add_argument(
        "-x",
        "--omic1",
        type=array,
        help="First dataset (samples x features)"
    )

    parser.add_argument(
        "-z",
        "--omic2",
        type=array,
        help="Second dataset (samples x features)"
    )

    parser.add_argument(
        "-y",
        "--y",
        type=array,
        help="Group vector (samples x 1)"
    )

    parser.add_argument(
        "-p",
        "--params",
        type=dict,
        default={
            "gamma": 1e-2,
            "lambda": 1e-3,
            "mu": 1e-3,
            "eta1": 1.00,
            "eta2": 1.00,
            "alpha": 2,
            "sigma": 1e-9,
            "m_back": 1,
        },
        help="Hyperparameters of the method",
    )

    parser.add_argument(
        "-i",
        "--init_method",
        type=str,
        default="random2",
        help="Method of initialization",
    )

    parser.add_argument(
        "-s",
        "--solver",
        type=str,
        default="analytical",
        help="Solver to use"
    )

    parser.add_argument(
        "-a",
        "--as_sklearn",
        type=bool,
        default=True,
        help="Use MU as in sklearn or Proximal",
    )

    parser.add_argument(
        "-b",
        "--backtrack",
        type=bool,
        default=False,
        help="Use LineSearch Backtrack (for Proximal only)",
    )

    parser.add_argument(
        "-m",
        "--max_iter_back",
        type=int,
        default=100,
        help="Maximum number of interations for LineSearch Backtrack",
    )

    parser.add_argument(
        "-t",
        "--tol",
        type=float,
        default=1e-4,
        help="Tolerance threshold for declaring convergence",
    )

    parser.add_argument(
        "-r",
        "--max_iter",
        type=int,
        default=1000,
        help="Maximum number of iterations"
    )

    parser.add_argument(
        "-d",
        "--seed",
        type=int,
        default=None,
        help="Seed")

    parser.add_argument(
        "-v",
        "--verbose",
        type=bool,
        default=False,
        help="Print statements during execution",
    )

    # Get each argument from the command line
    args = parser.parse_args()

    # Run the method NMFProfiler
    res = NMFProfiler(
        omic1=args.omic1,
        omic2=args.omic2,
        y=args.y,
        params=args.params,
        init_method=args.init_method,
        solver=args.solver,
        as_sklearn=args.as_sklearn,
        backtrack=args.backtrack,
        max_iter_back=args.max_iter_back,
        tol=args.tol,
        max_iter=args.max_iter,
        seed=args.seed,
        verbose=args.verbose,
    ).fit()

    print(res)


if __name__ == "__main__":
    main()
