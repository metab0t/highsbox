from . import highs_bin_path
import subprocess, sys


def main():
    # pass all args
    subprocess.run([highs_bin_path()] + sys.argv[1:], check=False)


if __name__ == "__main__":
    main()
