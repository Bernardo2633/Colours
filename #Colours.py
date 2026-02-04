#Colours

import tkinter
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

#Window container (Start)
window = tkinter.Tk() #Line that creates window
window.title("Secret Calculator")

#Frames
frame = tkinter.Frame(window)  #Window is parent of frame
label = tkinter.Label(frame,text = "0", font = ("Arial",50), bg = rich_black, fg = white, anchor = "e", width = column_count)

label.grid(row = 0, column = 0,columnspan = column_count,sticky = "ew") #columnspan makes the label span across all columns
for row in range(row_count):
    for column in range(column_count):
        value = buttons[row][column]
        button = tkinter.Button(frame, text = value, font = ("Arial",25), width = column_count-1,height = 1, command =lambda value=value: button_clicked(value))
        button.grid(row = row + 1, column = column)
        if value in rigth_buttons:
            button.config(bg = rich_black, fg = neon_ligth_blue, activebackground = blueberry)
        if value in numbers_buttons:
            button.config(bg = old_silver, fg = rich_black, activebackground = white)
        elif value not in rigth_buttons and value not in numbers_buttons:
            button.config(bg = rich_black, fg = white, activebackground = blueberry)

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

def button_clicked(value):
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


frame.pack() 


window.mainloop()

#Window container (End)