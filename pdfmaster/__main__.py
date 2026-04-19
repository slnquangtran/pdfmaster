"""
PDF Master - Premium Editorial Workspace
Entry point for the application
"""

import sys


def main():
    """Launch PDF Master UI.

    Currently defaults to the premium UI. In the future, this can branch
    to a classic UI path if/when such a separation is implemented.
    """
    # Import and launch the premium UI module
    from pdfmaster.ui.main import main as premium_main
    premium_main()


if __name__ == "__main__":
    main()
