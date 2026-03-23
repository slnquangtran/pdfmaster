class Theme:
    LIGHT_THEME = """
    QMainWindow {
        background-color: #F8F9FA;
    }
    
    QWidget {
        font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
        font-size: 14px;
    }
    
    /* Sidebar */
    QListWidget {
        background-color: #FFFFFF;
        border: none;
        border-right: 1px solid #E9ECEF;
        padding: 10px;
    }
    
    QListWidget::item {
        padding: 12px 15px;
        border-radius: 8px;
        margin: 2px 0;
        color: #495057;
        transition: all 0.2s ease;
    }
    
    QListWidget::item:hover {
        background-color: #F1F3F5;
    }
    
    QListWidget::item:selected {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #6366F1, stop:1 #8B5CF6);
        color: white;
    }
    
    /* Buttons */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #6366F1, stop:1 #8B5CF6);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #4F46E5, stop:1 #7C3AED);
        transform: translateY(-1px);
    }
    
    QPushButton:pressed {
        transform: translateY(0);
    }
    
    QPushButton:disabled {
        background: #E9ECEF;
        color: #ADB5BD;
    }
    
    QPushButton[secondary="true"] {
        background: transparent;
        border: 2px solid #6366F1;
        color: #6366F1;
    }
    
    QPushButton[secondary="true"]:hover {
        background: #EEF2FF;
    }
    
    /* Input fields */
    QLineEdit, QTextEdit, QComboBox {
        background-color: #FFFFFF;
        border: 2px solid #E9ECEF;
        border-radius: 8px;
        padding: 10px 15px;
        color: #212529;
        transition: all 0.2s ease;
    }
    
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
        border-color: #6366F1;
        background-color: #FAFBFF;
    }
    
    QLineEdit::placeholder, QTextEdit::placeholder {
        color: #ADB5BD;
    }
    
    /* Labels */
    QLabel {
        color: #212529;
    }
    
    QLabel[heading="true"] {
        font-size: 24px;
        font-weight: 700;
        color: #1F2937;
    }
    
    /* Progress Bar */
    QProgressBar {
        background-color: #E9ECEF;
        border-radius: 6px;
        height: 8px;
    }
    
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #6366F1, stop:1 #8B5CF6);
        border-radius: 6px;
    }
    
    /* Menu Bar */
    QMenuBar {
        background-color: #FFFFFF;
        border-bottom: 1px solid #E9ECEF;
        padding: 5px;
    }
    
    QMenuBar::item {
        padding: 8px 15px;
        border-radius: 6px;
    }
    
    QMenuBar::item:selected {
        background-color: #F1F3F5;
    }
    
    /* Menu */
    QMenu {
        background-color: #FFFFFF;
        border: 1px solid #E9ECEF;
        border-radius: 8px;
        padding: 5px;
    }
    
    QMenu::item {
        padding: 8px 20px;
        border-radius: 6px;
    }
    
    QMenu::item:selected {
        background-color: #EEF2FF;
        color: #6366F1;
    }
    
    /* List Widget */
    QListWidget {
        background-color: #FFFFFF;
        border: 1px solid #E9ECEF;
        border-radius: 8px;
    }
    
    QListWidget::item {
        padding: 10px 15px;
        border-radius: 6px;
    }
    
    QListWidget::item:selected {
        background-color: #EEF2FF;
        color: #6366F1;
    }
    
    /* Scrollbar */
    QScrollBar:vertical {
        background: transparent;
        width: 8px;
        border-radius: 4px;
    }
    
    QScrollBar::handle:vertical {
        background: #CBD5E1;
        border-radius: 4px;
        min-height: 50px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #94A3B8;
    }
    
    /* Status Bar */
    QStatusBar {
        background-color: #FFFFFF;
        border-top: 1px solid #E9ECEF;
        padding: 8px 15px;
    }
    
    /* Dialogs */
    QMessageBox {
        background-color: #FFFFFF;
    }
    
    QMessageBox QLabel {
        font-size: 14px;
        color: #212529;
    }
    """

    DARK_THEME = """
    QMainWindow {
        background-color: #0F172A;
    }
    
    QWidget {
        font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
        font-size: 14px;
        color: #E2E8F0;
    }
    
    /* Sidebar */
    QListWidget {
        background-color: #1E293B;
        border: none;
        border-right: 1px solid #334155;
        padding: 10px;
    }
    
    QListWidget::item {
        padding: 12px 15px;
        border-radius: 8px;
        margin: 2px 0;
        color: #94A3B8;
        transition: all 0.2s ease;
    }
    
    QListWidget::item:hover {
        background-color: #334155;
    }
    
    QListWidget::item:selected {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #6366F1, stop:1 #8B5CF6);
        color: white;
    }
    
    /* Buttons */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #6366F1, stop:1 #8B5CF6);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #4F46E5, stop:1 #7C3AED);
        transform: translateY(-1px);
    }
    
    QPushButton:pressed {
        transform: translateY(0);
    }
    
    QPushButton:disabled {
        background: #334155;
        color: #64748B;
    }
    
    QPushButton[secondary="true"] {
        background: transparent;
        border: 2px solid #6366F1;
        color: #818CF8;
    }
    
    QPushButton[secondary="true"]:hover {
        background: #312E81;
    }
    
    /* Input fields */
    QLineEdit, QTextEdit, QComboBox {
        background-color: #1E293B;
        border: 2px solid #334155;
        border-radius: 8px;
        padding: 10px 15px;
        color: #E2E8F0;
        transition: all 0.2s ease;
    }
    
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
        border-color: #6366F1;
        background-color: #1E1B4B;
    }
    
    QLineEdit::placeholder, QTextEdit::placeholder {
        color: #64748B;
    }
    
    /* Labels */
    QLabel {
        color: #E2E8F0;
    }
    
    QLabel[heading="true"] {
        font-size: 24px;
        font-weight: 700;
        color: #F8FAFC;
    }
    
    /* Progress Bar */
    QProgressBar {
        background-color: #334155;
        border-radius: 6px;
        height: 8px;
    }
    
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #6366F1, stop:1 #8B5CF6);
        border-radius: 6px;
    }
    
    /* Menu Bar */
    QMenuBar {
        background-color: #1E293B;
        border-bottom: 1px solid #334155;
        padding: 5px;
    }
    
    QMenuBar::item {
        padding: 8px 15px;
        border-radius: 6px;
        color: #E2E8F0;
    }
    
    QMenuBar::item:selected {
        background-color: #334155;
    }
    
    /* Menu */
    QMenu {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 5px;
    }
    
    QMenu::item {
        padding: 8px 20px;
        border-radius: 6px;
        color: #E2E8F0;
    }
    
    QMenu::item:selected {
        background-color: #312E81;
        color: #818CF8;
    }
    
    /* List Widget */
    QListWidget {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
    }
    
    QListWidget::item {
        padding: 10px 15px;
        border-radius: 6px;
        color: #E2E8F0;
    }
    
    QListWidget::item:selected {
        background-color: #312E81;
        color: #818CF8;
    }
    
    /* Scrollbar */
    QScrollBar:vertical {
        background: transparent;
        width: 8px;
        border-radius: 4px;
    }
    
    QScrollBar::handle:vertical {
        background: #475569;
        border-radius: 4px;
        min-height: 50px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #64748B;
    }
    
    /* Status Bar */
    QStatusBar {
        background-color: #1E293B;
        border-top: 1px solid #334155;
        padding: 8px 15px;
        color: #94A3B8;
    }
    
    /* Dialogs */
    QMessageBox {
        background-color: #1E293B;
    }
    
    QMessageBox QLabel {
        font-size: 14px;
        color: #E2E8F0;
    }
    """
    
    @staticmethod
    def get_theme(theme_name):
        if theme_name.lower() == "dark":
            return Theme.DARK_THEME
        return Theme.LIGHT_THEME


def apply_theme(app, theme_name="light"):
    theme = Theme.get_theme(theme_name)
    app.setStyleSheet(theme)