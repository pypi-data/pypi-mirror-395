"""
TopoVision - Entry point for command-line execution
"""


def main() -> None:
    """Main entry point for the TopoVision application."""
    from topovision.app import main as app_main

    app_main()


if __name__ == "__main__":
    main()
