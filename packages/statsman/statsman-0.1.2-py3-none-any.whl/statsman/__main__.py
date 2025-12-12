try:
    from .cli import main
except ImportError:
    print("Error: Could not import CLI module")
    import sys
    sys.exit(1)

if __name__ == "__main__":
    main()