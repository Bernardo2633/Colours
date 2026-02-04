#Colours

import tkinter
import tkinter.simpledialog
import tkinter.messagebox
import ast
import operator as op
import math

buttons = [
    ["AC","(",")","←"],
    ["1/x","x²","√x","÷"],
    ["7","8","9","×"],
    ["4","5","6","-"],
    ["1","2","3","+"],
    [".","0","+/-","="]
]

rigth_buttons = ["←","÷","×","-","+","="]
numbers_buttons =["0","1","2","3","4","5","6","7","8","9"]
special_buttons = ["AC","(",")","1/x","x²","√x",".","+/-"]

row_count = len(buttons) #Currently 6 rows
column_count = len(buttons[0]) #Currently 4 columns

#Colors
white  = "white"
rich_black = "#01032A"
old_silver = "#80868B"
blueberry = "#4285F4"
neon_ligth_blue = "#83EEFF"

# Global calculator management
calculators = {}  # {window: {'id': identifier, 'label': label_widget}}
calc_counter = 0  # Counter for unique identifiers (a-i)
max_calculators = 10

def create_calculator_window(calc_id):
    """Create a new calculator window with the given identifier."""
    window = tkinter.Tk()
    window.title(f"Secret Calculator - {calc_id}")
    
    # Store in global dict
    calculators[window] = {'id': calc_id}
    
    # Main frame
    frame = tkinter.Frame(window)
    
    # Top control row
    control_frame = tkinter.Frame(frame, bg=rich_black, height=60)
    control_frame.pack(fill="x", padx=5, pady=5)
    
    # Slot 1: New calculator button
    new_calc_button = tkinter.Button(
        control_frame, 
        text="+", 
        font=("Arial", 16), 
        width=5, 
        bg=rich_black, 
        fg=neon_ligth_blue, 
        activebackground=blueberry,
        command=lambda: add_new_calculator()
    )
    new_calc_button.pack(side="left", padx=5, pady=5)
    
    # Slot 2: Calculator identifier (editable)
    id_label = tkinter.Label(
        control_frame, 
        text=calc_id, 
        font=("Arial", 14), 
        bg=rich_black, 
        fg=white, 
        width=10,
        relief="solid",
        borderwidth=1
    )
    id_label.pack(side="left", padx=5, pady=5)
    id_label.bind("<Button-1>", lambda e, w=window, lbl=id_label: edit_calculator_id(w, lbl))
    calculators[window]['label'] = id_label
    
    # Slot 3: Coming soon button
    coming_soon_button = tkinter.Button(
        control_frame, 
        text="Coming soon", 
        font=("Arial", 14), 
        width=12, 
        bg=rich_black, 
        fg=white, 
        activebackground=blueberry,
        command=lambda: None
    )
    coming_soon_button.pack(side="left", padx=5, pady=5)
    
    # Display label
    label = tkinter.Label(frame, text="0", font=("Arial", 50), bg=rich_black, fg=white, anchor="e", width=column_count)
    label.grid(row=0, column=0, columnspan=column_count, sticky="ew")
    
    # Calculator buttons
    for row in range(row_count):
        for column in range(column_count):
            value = buttons[row][column]
            button = tkinter.Button(
                frame, 
                text=value, 
                font=("Arial", 25), 
                width=column_count-1, 
                height=1, 
                command=lambda v=value, lbl=label: button_clicked(v, lbl)
            )
            button.grid(row=row + 1, column=column)
            if value in rigth_buttons:
                button.config(bg=rich_black, fg=neon_ligth_blue, activebackground=blueberry)
            if value in numbers_buttons:
                button.config(bg=old_silver, fg=rich_black, activebackground=white)
            elif value not in rigth_buttons and value not in numbers_buttons:
                button.config(bg=rich_black, fg=white, activebackground=blueberry)
    
    frame.pack()
    
    # Handle window closing
    window.protocol("WM_DELETE_WINDOW", lambda w=window: close_calculator(w))
    
    return window

def add_new_calculator():
    """Add a new calculator window, up to max_calculators."""
    global calc_counter
    if len(calculators) >= max_calculators:
        tkinter.messagebox.showerror("Max Calculators", f"Max. calculators reached ({max_calculators})")
        return
    
    if calc_counter == 0:
        calc_id = 'a'
    else:
        calc_id = chr(ord('a') + calc_counter - 1)
    
    calc_counter += 1
    create_calculator_window(calc_id)

def edit_calculator_id(window, label):
    """Allow editing the calculator identifier by clicking the label."""
    new_id = tkinter.simpledialog.askstring("Edit ID", "Enter new calculator ID:", initialvalue=label.cget("text"))
    if new_id and len(new_id) <= 10:
        label.config(text=new_id)
        calculators[window]['id'] = new_id
        window.title(f"Secret Calculator - {new_id}")

def close_calculator(window):
    """Close a calculator window and clean up."""
    if window in calculators:
        del calculators[window]
    window.destroy()

#Window container (Start)
# Create main calculator with identifier 'x'
main_window = create_calculator_window('x')



# Safe expression evaluation using ast
# Allowed operators mapping
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.Pow: op.pow,
}

def _eval_ast(node):
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        oper = ALLOWED_OPERATORS.get(type(node.op))
        if oper is None:
            raise ValueError("Unsupported operator")
        return oper(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand)
        oper = ALLOWED_OPERATORS.get(type(node.op))
        if oper is None:
            raise ValueError("Unsupported unary operator")
        return oper(operand)
    raise ValueError("Unsupported expression")

def evaluate_expression(expr):
    try:
        # Normalize symbols
        expr = expr.replace('×', '*').replace('÷', '/')
        # Parse safely
        node = ast.parse(expr, mode='eval')
        result = _eval_ast(node)
        return result
    except Exception:
        return "Error"

def button_clicked(value, label):
    # Numbers and decimal point: append to expression
    if value in numbers_buttons or value == ".":
        if label["text"] == "0" or label["text"] == "Error":
            label["text"] = value
        else:
            label["text"] += value
    # Special buttons: unary operations, parentheses, clear, sign
    elif value in special_buttons:
        if value == "+/-":
            # Try to toggle the entire displayed number
            try:
                current = evaluate_expression(label["text"]) if any(c in label["text"] for c in '()+-*/×÷') else float(label["text"])
                if current == "Error":
                    label["text"] = "Error"
                else:
                    label["text"] = str(-current)
            except Exception:
                label["text"] = "Error"
        elif value == ".":
            if "." not in label["text"]:
                label["text"] += "."
        elif value == "AC":
            label["text"] = "0"
        elif value == "1/x":
            try:
                cur = evaluate_expression(label["text"]) if any(c in label["text"] for c in '()+-*/×÷') else float(label["text"])
                if cur == 0 or cur == "Error":
                    label["text"] = "Error"
                else:
                    label["text"] = str(1.0 / cur)
            except Exception:
                label["text"] = "Error"
        elif value == "x²":
            try:
                cur = evaluate_expression(label["text"]) if any(c in label["text"] for c in '()+-*/×÷') else float(label["text"])
                label["text"] = str(cur * cur)
            except Exception:
                label["text"] = "Error"
        elif value == "√x":
            try:
                cur = evaluate_expression(label["text"]) if any(c in label["text"] for c in '()+-*/×÷') else float(label["text"])
                if cur < 0:
                    label["text"] = "Error"
                else:
                    label["text"] = str(math.sqrt(cur))
            except Exception:
                label["text"] = "Error"
        elif value in ['(', ')']:
            if label["text"] == "0" or label["text"] == "Error":
                label["text"] = value
            else:
                label["text"] += value
    # Right-side buttons: backspace, operators, equals
    elif value in rigth_buttons:
        if value == "←":
            label["text"] = label["text"][:-1]
            if label["text"] == "":
                label["text"] = "0"
        elif value == "=":
            result = evaluate_expression(label["text"])
            if result == "Error":
                label["text"] = "Error"
            else:
                # Normalize integer display when possible
                if isinstance(result, float) and result.is_integer():
                    label["text"] = str(int(result))
                else:
                    label["text"] = str(result)
        elif value in ["÷", "×", "-", "+"]:
            if label["text"] == "Error":
                label["text"] = "0"
            if label["text"] == "0":
                label["text"] = "0" + value
            else:
                label["text"] += value




main_window.mainloop()

#Window container (End)