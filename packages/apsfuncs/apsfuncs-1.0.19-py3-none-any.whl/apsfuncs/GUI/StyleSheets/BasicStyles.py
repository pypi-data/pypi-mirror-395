"""This is a set of standard syles that can be called for a PyQt6 program"""

# Standard LineEdit
def basic_line_edit():
    return """
    QLineEdit { 
        border: 2px solid gray;
        border-radius: 10px;
        padding: 0 8px;
        background: rgba(206, 131, 214, 255);;
        selection-background-color: darkgray;
        color: black;
    }"""

# Standard Label
def basic_label():
    return """
    QLabel {
        color: white;
        background-color: purple;
        border: 2px solid purple;
        border-color: beige;
        border-radius: 10px;
        font: bold 14px;
        padding: 6px;
    }"""

# Standard Frame
def basic_frame():
    return """
    QFrame {
        background-color: rgba(125, 29, 181, 255)  
    }"""

# Standard button
def basic_button():
    return """
    QPushButton:enabled {
        color: white;
        background-color: rgba(168, 26, 184, 255);
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        border-color: beige;
        font: bold 14px;
        min-width: 10em;
        padding: 6px;
    }
        
    QPushButton:disabled {
        color: white;
        background-color: rgba(116, 106, 117, 255);
    }

    QPushButton:hover {
        color: white;
        background: rgba(206, 131, 214, 255);
        border-color: beige;
    }"""

# Title table
def title_label():
    return """
    QLabel#Title {
        color: white;
        background-color: purple;
        border: 2px solid purple;
        border-color: beige;
        border-radius: 10px;
        font: bold 21px;
        padding: 6px;
    }"""

# Standard QDialog
def basic_dialog():
    return """
    QDialog {
        background-color: rgba(125, 29, 181, 255)  
    }"""