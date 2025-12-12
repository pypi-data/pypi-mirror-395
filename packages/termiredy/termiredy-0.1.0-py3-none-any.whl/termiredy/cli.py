import subprocess
import argparse
import time
import sys
from .notifications import send_notification

def main():
    parser = argparse.ArgumentParser(
        prog="termiredy",
        description="A terminal tool that notifies you when your task is done."
    )

    parser.add_argument("command", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if not args.command:
        print("\n> You must provide a command to run.\nExample: termiredy python work.py")
        sys.exit(1)

    t1 = time.time()
    try:
        subprocess.run(" ".join(args.command), shell=True)
    except KeyboardInterrupt as e:
        print("\n> Command execution interrupted by user.")
    print(f"\n> Your command is done! It took {time.time() - t1:.2f} seconds.")
    send_notification("Termiredy", "Your command is done!")
