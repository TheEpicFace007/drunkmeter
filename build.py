import os

import pyshortcuts

root_dir = os.path.dirname(os.path.abspath(__file__))

pyshortcuts.make_shortcut(
    script="main.py",
    name="Drunkmeter",
    description="Calculate your alcohol dosage",
    icon=os.path.join(root_dir, "icon"),
    working_dir=root_dir,
    terminal=False,
    desktop=True
)
print("Shortcut created")