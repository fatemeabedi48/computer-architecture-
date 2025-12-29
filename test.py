import tkinter as tk
from tkinter import ttk, messagebox

# Global variables for storing the current values in the simulation
IR = None
AC = 0
DR = 0
PC = 0
AR = 0
E = 0
memory = {}

def assemble_code():
    """Assemble the code written in the Code Editor."""
    input_code = code_editor.get("1.0", tk.END).strip()
    if not input_code:
        messagebox.showerror("Error", "Code Editor is empty!")
        return

    # Mock assembling logic: convert each instruction to a mock machine code
    assembled_memory = {}
    lines = input_code.splitlines()
    for i, line in enumerate(lines):
        # Simplified machine code generation (for demonstration purposes)
        opcode = hash(line) % 0xFFFF  # Mock conversion to a 16-bit machine code
        assembled_memory[i] = f"0x{opcode:04X}"

    # Store the memory for use during simulation
    global memory
    memory = assembled_memory

    # Populate memory table with initial values
    for address, content in assembled_memory.items():
        memory_table.set(address, "Contents", content)

    instruction_label.config(text="Assembly complete!")

def reset_simulator():
    """Reset all fields in the simulator."""
    code_editor.delete("1.0", tk.END)
    instruction_label.config(text="")
    for i in range(4096):  # Reset memory table to support 4096 addresses
        memory_table.set(i, "Contents", "")
    
    # Reset global values
    global IR, AC, DR, PC, AR, E
    IR = None
    AC = 0
    DR = 0
    PC = 0
    AR = 0
    E = 0
    
    # Clear instruction table
    for row in instruction_table.get_children():
        instruction_table.delete(row)

    # Reset instruction table for Initial Values
    update_instruction_table("Initial Values")

def update_instruction_table(time_point):
    """Update the instruction table with current values at a specific time."""
    # Insert the time point and current values into the instruction table
    instruction_table.insert("", "end", values=(time_point, IR, AC, DR, PC, AR, f"M[{AR}]", E))

def run_simulation():
    """Run the simulation step by step."""
    global IR, AC, DR, PC, AR, E
    
    # T0: AR <- PC
    AR = PC
    update_instruction_table("T0: AR <- PC")
    
     
    # T1: IR <- M[AR], PC <- PC + 1
    IR = memory.get(AR, "0x0000")  # Mock fetch from memory
    PC += 1
    update_instruction_table("T1: IR <- M[AR], PC <- PC + 1")
    
    # T2: AR <- IR[0:11] (Taking bits 0 to 11 of IR as a mock address)
    AR = int(IR[2:], 16) & 0xFFF  # Mock interpretation of first 12 bits as address
    update_instruction_table("T2: AR <- IR[0:11]")
    
    # T3 to T6: Can be further steps based on the specific instruction set
    update_instruction_table("T3")
    update_instruction_table("T4")
    update_instruction_table("T5")
    update_instruction_table("T6")
    
    # After execution, update the table with final values
    update_instruction_table("After Execution")

# Create main window
root = tk.Tk()
root.title("Mano Simulator")
root.geometry("1200x700")
root.configure(bg="#DFF9FB")

# Create a frame for the left side to hold both Code Editor and Memory Table
left_frame = tk.Frame(root, bg="#DFF9FB")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)

# Code Editor Frame
code_editor_frame = tk.Frame(left_frame, bg="#DFF9FB")
code_editor_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10, expand=True)
code_editor_label = tk.Label(code_editor_frame, text="Code Editor", bg="#DFF9FB", font=("Arial", 14))
code_editor_label.pack(anchor=tk.W)
code_editor = tk.Text(code_editor_frame, height=30, width=50, font=("Courier", 12))
code_editor.pack(pady=5)

# Assemble Button
assemble_button = tk.Button(code_editor_frame, text="Assemble", command=assemble_code, font=("Arial", 14), bg="#00A8FF", fg="white")
assemble_button.pack(pady=5)

# Memory Table Frame
memory_frame = tk.Frame(left_frame, bg="#DFF9FB")
memory_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10, expand=True)
memory_label = tk.Label(memory_frame, text="Memory Table", bg="#DFF9FB", font=("Arial", 14, "bold"))
memory_label.pack(anchor=tk.W)

memory_table = ttk.Treeview(memory_frame, columns=("Decimal Address", "Hex Address", "Contents"), show="headings", height=30)
memory_table.heading("Decimal Address", text="Decimal Address")
memory_table.heading("Hex Address", text="Hex Address")
memory_table.heading("Contents", text="Contents")

memory_table.column("Decimal Address", width=120, anchor=tk.CENTER)
memory_table.column("Hex Address", width=120, anchor=tk.CENTER)
memory_table.column("Contents", width=150, anchor=tk.CENTER)

memory_table.pack(pady=5)

# Populate initial memory addresses (0 to 4095)
for i in range(4096):
    memory_table.insert("", "end", iid=i, values=(i, f"0x{i:03X}", ""))

# Instruction Details Frame
instruction_frame = tk.Frame(root, bg="#DFF9FB")
instruction_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
instruction_label = tk.Label(instruction_frame, text="Instructions Detail", bg="#DFF9FB", font=("Arial", 14, "bold"))
instruction_label.pack(anchor=tk.W)

instruction_table = ttk.Treeview(instruction_frame, columns=("Elements", "IR", "AC", "DR", "PC", "AR", "M(AR)", "E"), show="headings", height=15)
for col in ("Elements", "IR", "AC", "DR", "PC", "AR", "M(AR)", "E"):
    instruction_table.heading(col, text=col)
    instruction_table.column(col, width=100, anchor=tk.CENTER)
instruction_table.pack(pady=5)

# Reset Button
reset_button = tk.Button(root, text="Reset", command=reset_simulator, font=("Arial", 14), bg="#FF4B5C", fg="white")
reset_button.pack(side=tk.BOTTOM, pady=10)

# Simulate Button
simulate_button = tk.Button(root, text="Run Simulation", command=run_simulation, font=("Arial", 14), bg="#00A8FF", fg="white")
simulate_button.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
