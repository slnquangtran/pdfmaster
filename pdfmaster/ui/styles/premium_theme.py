"""
Premium Editorial Theme for PDF Master
Based on the Editorial Workspace design specification
"""


class PremiumTheme:
    """Premium editorial theme with Notion-like aesthetics"""

    # Color palette from design specification
    COLORS = {
        # Primary colors
        "primary": "#004f8f",
        "primary_container": "#0067b8",
        "primary_fixed": "#d3e3ff",
        "primary_fixed_dim": "#a3c9ff",
        "on_primary": "#ffffff",
        "on_primary_fixed": "#001c39",
        "on_primary_fixed_variant": "#004883",
        # Secondary colors
        "secondary": "#006e2c",
        "secondary_fixed": "#88fb99",
        "secondary_fixed_dim": "#6bde80",
        "secondary_container": "#88fb99",
        "on_secondary": "#ffffff",
        "on_secondary_fixed": "#002108",
        "on_secondary_fixed_variant": "#00531f",
        "on_secondary_container": "#00742f",
        # Tertiary colors
        "tertiary": "#494e55",
        "tertiary_fixed": "#dee3eb",
        "tertiary_fixed_dim": "#c2c7cf",
        "tertiary_container": "#61666d",
        "on_tertiary": "#ffffff",
        "on_tertiary_fixed": "#171c22",
        "on_tertiary_fixed_variant": "#42474e",
        "on_tertiary_container": "#e0e4ec",
        # Surface colors
        "surface": "#f7f9ff",
        "surface_dim": "#d6dae2",
        "surface_bright": "#f7f9ff",
        "surface_container_lowest": "#ffffff",
        "surface_container_low": "#f0f4fc",
        "surface_container": "#eaeef6",
        "surface_container_high": "#e4e8f0",
        "surface_container_highest": "#dee3eb",
        "surface_variant": "#dee3eb",
        "surface_tint": "#0060ab",
        # On surface colors
        "on_surface": "#171c22",
        "on_surface_variant": "#414751",
        "on_background": "#171c22",
        "on_error": "#ffffff",
        "on_error_container": "#93000a",
        # Other colors
        "background": "#f7f9ff",
        "error": "#ba1a1a",
        "error_container": "#ffdad6",
        "outline": "#717783",
        "outline_variant": "#c1c7d3",
        "inverse_surface": "#2c3137",
        "inverse_on_surface": "#edf1f9",
        "inverse_primary": "#a3c9ff",
    }

    LIGHT_THEME = f"""
    /* Global Styles */
    QMainWindow {{
        background-color: {COLORS["surface"]};
    }}
    
    QWidget {{
        font-family: 'Inter', 'Segoe UI', 'Microsoft YaHei', sans-serif;
        font-size: 14px;
        color: {COLORS["on_surface"]};
    }}
    
    /* Sidebar */
    QWidget#sidebarContainer {{
        background-color: {COLORS["surface"]};
        border-right: none;
        min-width: 260px;
        max-width: 260px;
    }}
    
    QWidget#logoContainer {{
        background-color: transparent;
        padding: 20px 16px;
    }}
    
    QLabel#logoLabel {{
        font-size: 18px;
        font-weight: 700;
        color: {COLORS["on_surface"]};
        letter-spacing: -0.02em;
    }}
    
    QLabel#logoSubtitle {{
        font-size: 12px;
        color: {COLORS["on_surface_variant"]};
        font-weight: 400;
    }}
    
    QPushButton#uploadPdfBtn {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 {COLORS["primary"]}, stop:1 {COLORS["primary_container"]});
        color: {COLORS["on_primary"]};
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        margin: 8px 16px;
    }}
    
    QPushButton#uploadPdfBtn:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 {COLORS["primary_container"]}, stop:1 {COLORS["primary"]});
    }}
    
    /* Navigation Items */
    QListWidget#navList {{
        background-color: transparent;
        border: none;
        padding: 8px;
    }}
    
    QListWidget#navList::item {{
        padding: 10px 16px;
        border-radius: 8px;
        margin: 2px 8px;
        color: {COLORS["on_surface_variant"]};
        font-weight: 500;
    }}
    
    QListWidget#navList::item:hover {{
        background-color: {COLORS["surface_container_low"]};
    }}
    
    QListWidget#navList::item:selected {{
        background-color: {COLORS["surface_container"]};
        color: {COLORS["primary"]};
        font-weight: 600;
    }}
    
    /* Quick Access Section */
    QLabel#sectionHeader {{
        font-size: 11px;
        font-weight: 700;
        color: {COLORS["on_surface_variant"]};
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 16px 24px 8px;
    }}
    
    /* Bottom Section */
    QWidget#bottomSection {{
        background-color: transparent;
        border-top: 1px solid {COLORS["outline_variant"]};
        padding: 8px;
    }}
    
    QWidget#userProfile {{
        background-color: {COLORS["surface_container_low"]};
        border-radius: 12px;
        padding: 12px;
        margin: 8px;
    }}
    
    QLabel#userName {{
        font-size: 14px;
        font-weight: 600;
        color: {COLORS["on_surface"]};
    }}
    
    QLabel#userRole {{
        font-size: 12px;
        color: {COLORS["on_surface_variant"]};
    }}
    
    /* Header / Top Bar */
    QWidget#headerContainer {{
        background-color: {COLORS["surface_container_lowest"]};
        border-bottom: 1px solid {COLORS["outline_variant"]};
        padding: 0 24px;
    }}
    
    QLineEdit#searchInput {{
        background-color: {COLORS["surface_container_highest"]};
        border: none;
        border-radius: 8px;
        padding: 10px 16px;
        color: {COLORS["on_surface"]};
        font-size: 14px;
    }}
    
    QLineEdit#searchInput:focus {{
        background-color: {COLORS["surface_container_lowest"]};
    }}
    
    /* Content Area */
    QWidget#contentContainer {{
        background-color: {COLORS["surface"]};
    }}
    
    /* Cards */
    QWidget#card {{
        background-color: {COLORS["surface_container_low"]};
        border-radius: 12px;
        padding: 20px;
    }}
    
    QWidget#card:hover {{
        background-color: {COLORS["surface_container_lowest"]};
    }}
    
    QWidget#cardHighlight {{
        background-color: {COLORS["primary_container"]};
        border-radius: 16px;
        padding: 24px;
    }}
    
    /* Buttons */
    QPushButton {{
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
    }}
    
    QPushButton#primaryBtn {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 {COLORS["primary"]}, stop:1 {COLORS["primary_container"]});
        color: {COLORS["on_primary"]};
    }}
    
    QPushButton#primaryBtn:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 {COLORS["primary_container"]}, stop:1 {COLORS["primary"]});
    }}
    
    QPushButton#secondaryBtn {{
        background-color: transparent;
        color: {COLORS["primary"]};
        border: 1px solid {COLORS["outline_variant"]};
    }}
    
    QPushButton#secondaryBtn:hover {{
        background-color: {COLORS["surface_container"]};
    }}
    
    QPushButton#ghostBtn {{
        background-color: transparent;
        color: {COLORS["primary"]};
    }}
    
    QPushButton#ghostBtn:hover {{
        background-color: {COLORS["surface_container_high"]};
    }}
    
    /* Labels */
    QLabel#pageTitle {{
        font-size: 32px;
        font-weight: 700;
        color: {COLORS["on_surface"]};
        letter-spacing: -0.02em;
    }}
    
    QLabel#pageSubtitle {{
        font-size: 16px;
        color: {COLORS["on_surface_variant"]};
    }}
    
    QLabel#sectionTitle {{
        font-size: 20px;
        font-weight: 700;
        color: {COLORS["on_surface"]};
        letter-spacing: -0.01em;
    }}
    
    QLabel#cardTitle {{
        font-size: 16px;
        font-weight: 600;
        color: {COLORS["on_surface"]};
    }}
    
    QLabel#cardDescription {{
        font-size: 14px;
        color: {COLORS["on_surface_variant"]};
    }}
    
    /* Badges */
    QLabel#badge {{
        font-size: 10px;
        font-weight: 700;
        padding: 4px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    QLabel#badgePrimary {{
        background-color: {COLORS["primary_container"]};
        color: {COLORS["primary"]};
    }}
    
    QLabel#badgeSecondary {{
        background-color: {COLORS["secondary_container"]};
        color: {COLORS["secondary"]};
    }}
    
    QLabel#badgeTertiary {{
        background-color: {COLORS["tertiary_container"]};
        color: {COLORS["on_tertiary"]};
    }}
    
    /* Storage Bar */
    QProgressBar {{
        background-color: {COLORS["surface_container"]};
        border: none;
        border-radius: 4px;
        height: 8px;
    }}
    
    QProgressBar::chunk {{
        background-color: {COLORS["primary"]};
        border-radius: 4px;
    }}
    
    /* Document List */
    QWidget#documentItem {{
        background-color: transparent;
        padding: 12px;
        border-radius: 8px;
    }}
    
    QWidget#documentItem:hover {{
        background-color: {COLORS["surface_container_lowest"]};
    }}
    
    /* Floating Toolbar */
    QWidget#floatingToolbar {{
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 24px;
        padding: 8px 16px;
    }}
    
    /* Icons (using text as placeholder for Material Icons) */
    QLabel#icon {{
        font-family: 'Material Symbols Outlined';
        font-size: 24px;
    }}
    
    /* Tables */
    QTableWidget {{
        background-color: transparent;
        border: none;
        gridline-color: transparent;
    }}
    
    QTableWidget::item {{
        padding: 12px;
        border-bottom: 1px solid {COLORS["outline_variant"]};
    }}
    
    QTableWidget::item:selected {{
        background-color: {COLORS["surface_container"]};
    }}
    
    QHeaderView::section {{
        background-color: transparent;
        padding: 12px;
        border: none;
        font-weight: 700;
        font-size: 11px;
        color: {COLORS["on_surface_variant"]};
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }}
    
    /* Scrollbar */
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0;
    }}
    
    QScrollBar::handle:vertical {{
        background: {COLORS["outline_variant"]};
        border-radius: 4px;
        min-height: 50px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {COLORS["outline"]};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    
    /* Status Bar */
    QStatusBar {{
        background-color: {COLORS["surface_container_low"]};
        border-top: 1px solid {COLORS["outline_variant"]};
        padding: 8px 16px;
        color: {COLORS["on_surface_variant"]};
        font-size: 12px;
    }}
    
    /* Menu */
    QMenu {{
        background-color: {COLORS["surface_container_lowest"]};
        border: 1px solid {COLORS["outline_variant"]};
        border-radius: 12px;
        padding: 8px;
    }}
    
    QMenu::item {{
        padding: 10px 16px;
        border-radius: 8px;
    }}
    
    QMenu::item:selected {{
        background-color: {COLORS["surface_container"]};
    }}
    
    /* Dialogs */
    QDialog {{
        background-color: {COLORS["surface"]};
    }}
    """

    DARK_THEME = f"""
    /* Global Styles */
    QMainWindow {{
        background-color: {COLORS["inverse_surface"]};
    }}
    
    QWidget {{
        font-family: 'Inter', 'Segoe UI', 'Microsoft YaHei', sans-serif;
        font-size: 14px;
        color: {COLORS["inverse_on_surface"]};
    }}
    
    /* Sidebar */
    QWidget#sidebarContainer {{
        background-color: #1a1f2e;
        border-right: none;
        min-width: 260px;
        max-width: 260px;
    }}
    
    QWidget#logoContainer {{
        background-color: transparent;
        padding: 20px 16px;
    }}
    
    QLabel#logoLabel {{
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
    }}
    
    QLabel#logoSubtitle {{
        font-size: 12px;
        color: #8b95a5;
        font-weight: 400;
    }}
    
    QPushButton#uploadPdfBtn {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #3b82f6, stop:1 #2563eb);
        color: #ffffff;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        margin: 8px 16px;
    }}
    
    QPushButton#uploadPdfBtn:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #2563eb, stop:1 #3b82f6);
    }}
    
    /* Navigation Items */
    QListWidget#navList {{
        background-color: transparent;
        border: none;
        padding: 8px;
    }}
    
    QListWidget#navList::item {{
        padding: 10px 16px;
        border-radius: 8px;
        margin: 2px 8px;
        color: #8b95a5;
        font-weight: 500;
    }}
    
    QListWidget#navList::item:hover {{
        background-color: rgba(255, 255, 255, 0.05);
    }}
    
    QListWidget#navList::item:selected {{
        background-color: rgba(59, 130, 246, 0.15);
        color: #3b82f6;
        font-weight: 600;
    }}
    
    /* Quick Access Section */
    QLabel#sectionHeader {{
        font-size: 11px;
        font-weight: 700;
        color: #6b7280;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 16px 24px 8px;
    }}
    
    /* Bottom Section */
    QWidget#bottomSection {{
        background-color: transparent;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 8px;
    }}
    
    QWidget#userProfile {{
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 12px;
        margin: 8px;
    }}
    
    QLabel#userName {{
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
    }}
    
    QLabel#userRole {{
        font-size: 12px;
        color: #8b95a5;
    }}
    
    /* Header / Top Bar */
    QWidget#headerContainer {{
        background-color: #1a1f2e;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0 24px;
    }}
    
    QLineEdit#searchInput {{
        background-color: rgba(255, 255, 255, 0.08);
        border: none;
        border-radius: 8px;
        padding: 10px 16px;
        color: #ffffff;
        font-size: 14px;
    }}
    
    QLineEdit#searchInput:focus {{
        background-color: rgba(255, 255, 255, 0.12);
    }}
    
    /* Content Area */
    QWidget#contentContainer {{
        background-color: {COLORS["inverse_surface"]};
    }}
    
    /* Cards */
    QWidget#card {{
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
    }}
    
    QWidget#card:hover {{
        background-color: rgba(255, 255, 255, 0.08);
    }}
    
    QWidget#cardHighlight {{
        background-color: rgba(59, 130, 246, 0.15);
        border-radius: 16px;
        padding: 24px;
    }}
    
    /* Buttons */
    QPushButton {{
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
    }}
    
    QPushButton#primaryBtn {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #3b82f6, stop:1 #2563eb);
        color: #ffffff;
    }}
    
    QPushButton#primaryBtn:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #2563eb, stop:1 #3b82f6);
    }}
    
    QPushButton#secondaryBtn {{
        background-color: transparent;
        color: #3b82f6;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    QPushButton#secondaryBtn:hover {{
        background-color: rgba(255, 255, 255, 0.05);
    }}
    
    QPushButton#ghostBtn {{
        background-color: transparent;
        color: #3b82f6;
    }}
    
    QPushButton#ghostBtn:hover {{
        background-color: rgba(255, 255, 255, 0.05);
    }}
    
    /* Labels */
    QLabel#pageTitle {{
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
    }}
    
    QLabel#pageSubtitle {{
        font-size: 16px;
        color: #8b95a5;
    }}
    
    QLabel#sectionTitle {{
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.01em;
    }}
    
    QLabel#cardTitle {{
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
    }}
    
    QLabel#cardDescription {{
        font-size: 14px;
        color: #8b95a5;
    }}
    
    /* Storage Bar */
    QProgressBar {{
        background-color: rgba(255, 255, 255, 0.1);
        border: none;
        border-radius: 4px;
        height: 8px;
    }}
    
    QProgressBar::chunk {{
        background-color: #3b82f6;
        border-radius: 4px;
    }}
    
    /* Document List */
    QWidget#documentItem {{
        background-color: transparent;
        padding: 12px;
        border-radius: 8px;
    }}
    
    QWidget#documentItem:hover {{
        background-color: rgba(255, 255, 255, 0.05);
    }}
    
    /* Floating Toolbar */
    QWidget#floatingToolbar {{
        background-color: rgba(26, 31, 46, 0.9);
        border-radius: 24px;
        padding: 8px 16px;
    }}
    
    /* Scrollbar */
    QScrollBar:vertical {{
        background: transparent;
        width: 8px;
        margin: 0;
    }}
    
    QScrollBar::handle:vertical {{
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
        min-height: 50px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: rgba(255, 255, 255, 0.3);
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    
    /* Status Bar */
    QStatusBar {{
        background-color: #1a1f2e;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 8px 16px;
        color: #8b95a5;
        font-size: 12px;
    }}
    
    /* Menu */
    QMenu {{
        background-color: #1a1f2e;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 8px;
    }}
    
    QMenu::item {{
        padding: 10px 16px;
        border-radius: 8px;
        color: #ffffff;
    }}
    
    QMenu::item:selected {{
        background-color: rgba(59, 130, 246, 0.15);
    }}
    
    /* Dialogs */
    QDialog {{
        background-color: {COLORS["inverse_surface"]};
    }}
    """

    @staticmethod
    def get_theme(theme_name):
        if theme_name.lower() == "dark":
            return PremiumTheme.DARK_THEME
        return PremiumTheme.LIGHT_THEME


def apply_premium_theme(app, theme_name="light"):
    """Apply the premium theme to the application"""
    theme = PremiumTheme.get_theme(theme_name)
    app.setStyleSheet(theme)
