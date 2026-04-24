import os
import warnings

# Suppress all warnings at the interpreter level
os.environ['PYTHONWARNINGS'] = 'ignore'
# Suppress deprecated protobuf warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=r"SymbolDatabase.GetPrototype\(\) is deprecated")

from fields import *
import tkinter as tk
import subprocess
import sys

def train_specific(page=0):
    # Clear the center_frame
    for widget in center_frame.winfo_children():
        widget.destroy()

    # Create a button for each label in a grid
    for i, sign in enumerate(sign_labels[page]):
        tk.Button(center_frame, text=f'{sign_labels[page][sign]}', width=3, command=lambda sign=sign: 
                  print(f'Training {sign}')).grid(row=i // 5, column=i % 5, sticky='ns', padx=5, pady=5)

    # Create a separate frame for navigation buttons
    nav_frame = tk.Frame(center_frame)
    nav_frame.grid(row=5, column=0, columnspan=5)

    # Add either a back button or main menu button at the bottom left
    if page > 0:
        back_button = tk.Button(nav_frame, text='Back', command=lambda: train_specific(page - 1))
    else:
        back_button = tk.Button(nav_frame, text='Main Menu', command=main_screen)
    back_button.pack(side='left', padx=5, pady=5)

    # Add a next button at the bottom right
    if page < len(sign_labels) - 1:
        next_button = tk.Button(nav_frame, text='Next', command=lambda: train_specific(page + 1))
        next_button.pack(side='right', padx=5, pady=5)

def run_detector():
    # Get the root directory (one level up from app/gui/)
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    script_path = os.path.join(root_dir, 'app', 'inference_classifier.py')
    
    # Use the project's virtual environment python
    venv_python = os.path.join(root_dir, '.venv', 'Scripts', 'python.exe')
        
    python_exe = venv_python if os.path.exists(venv_python) else sys.executable
    
    # Create environment with suppressed warnings
    env = os.environ.copy()
    env['PYTHONWARNINGS'] = 'ignore'
    
    subprocess.Popen([python_exe, script_path], cwd=root_dir, env=env)


def main_screen():
    # Clear the center_frame
    for widget in center_frame.winfo_children():
        widget.destroy()

    # Create the main screen buttons and label using grid
    train_all_btn = tk.Button(center_frame, text='Train All', command=train_all)
    train_all_btn.grid(row=0, column=0, pady=10)

    train_specific_btn = tk.Button(center_frame, text='Train Specific Sign', command=lambda: train_specific(0))
    train_specific_btn.grid(row=1, column=0, pady=10)

    total_signs_label = tk.Label(center_frame, text=f'Total Signs: {sum(len(page) for page in sign_labels.values())}')
    total_signs_label.grid(row=2, column=0, pady=10)

    run_detector_btn = tk.Button(center_frame, text='Open Camera', command=run_detector)
    run_detector_btn.grid(row=3, column=0, pady=10)

def train_all():
    print('test')

# Create the main window
root = tk.Tk()
root.geometry('400x300')  # Adjust the size as needed

# Create a frame for centered layout management
center_frame = tk.Frame(root)
center_frame.place(relx=0.5, rely=0.5, anchor='center')

# Call main screen function to display initial screen
main_screen()

# Start the main loop
root.mainloop()
