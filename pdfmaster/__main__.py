"""
PDF Master - Premium Editorial Workspace
Entry point for the application
"""

import sys


def main():
    """Launch PDF Master with premium UI"""
    # Check for --classic flag to use legacy UI
    if "--classic" in sys.argv:
        from pdfmaster.ui.main import main as classic_main

        classic_main()
    else:
        # Default to premium UI
        from pdfmaster.ui.premium_main import main as premium_main

        premium_main()


if __name__ == "__main__":
    main()
