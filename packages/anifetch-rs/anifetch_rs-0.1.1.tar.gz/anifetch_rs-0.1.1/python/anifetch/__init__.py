import sys
import anifetch_rs

def main():
    """Entry point for the anifetch command"""
    try:
        anifetch_rs.run_cli(sys.argv)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()