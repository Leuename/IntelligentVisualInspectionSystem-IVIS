import re

with open("frontend.py", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the block comment at the top
content = re.sub(r'# -\*- coding: utf-8 -\*-\n+', '', content)
content = re.sub(r'#+[\s\S]*?#+\n+', '', content)

# Remove all end-of-line comments like # setupUi and # retranslateUi
content = re.sub(r'\s*#\s*(setupUi|retranslateUi).*', '', content)

# Remove the CSS comments in strings like /* dark blue header */
content = re.sub(r'/\*.*?\*/', '', content)

docstring = '''"""
Purpose: Houses the auto-generated PyQt6 layout classes defining the visual structure of the IVIS application.
Classes:
- Ui_MainWindow(object): Translates Qt Designer UI properties to fully-functional PyQt6 widgets and geometries.
Functions/Methods:
- Ui_MainWindow.setupUi: Generates all structural UI elements (frames, buttons, placeholders, sizes) precisely.
- Ui_MainWindow.retranslateUi: Configures the texts, tooltips, and translations for all UI interactables.
Workflows/Interactions:
- Completely static definition. Used exclusively by `backend.py` via instantiation to render the core visual interface.
"""
'''
with open("frontend.py", "w", encoding="utf-8") as f:
    f.write(docstring + content.lstrip())

print("Successfully cleaned frontend.py")
