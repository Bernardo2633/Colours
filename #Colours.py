#Colours

import tkinter
import tkinter.simpledialog
import tkinter.messagebox
import ast
import operator as op
import math
import colorsys

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

def add_hex_colors(color1: str, color2: str) -> str:
    """
    Add two colors in hexadecimal format.
    
    Takes two hex colors (e.g., #FF5733 and #00A8E1), extracts RGB components,
    adds corresponding components, and caps each at 255.
    
    Args:
        color1: First color in hex format (e.g., '#FF5733')
        color2: Second color in hex format (e.g., '#00A8E1')
    
    Returns:
        Result color in hex format (e.g., '#FFFFFF')
    
    Example:
        >>> add_hex_colors('#FF5733', '#00A8E1')
        '#FFFFFF'
    """
    # Remove '#' from the hex strings
    color1 = color1.lstrip('#')
    color2 = color2.lstrip('#')
    
    # Extract RGB components from color1
    r1 = int(color1[0:2], 16)  # First 2 hex digits (Red)
    g1 = int(color1[2:4], 16)  # Next 2 hex digits (Green)
    b1 = int(color1[4:6], 16)  # Last 2 hex digits (Blue)
    
    # Extract RGB components from color2
    r2 = int(color2[0:2], 16)  # First 2 hex digits (Red)
    g2 = int(color2[2:4], 16)  # Next 2 hex digits (Green)
    b2 = int(color2[4:6], 16)  # Last 2 hex digits (Blue)
    
    # Add corresponding components and cap at 255
    r_sum = min(r1 + r2, 255)
    g_sum = min(g1 + g2, 255)
    b_sum = min(b1 + b2, 255)
    
    # Convert back to hexadecimal and format with '#' and zero padding
    return f"#{r_sum:02x}{g_sum:02x}{b_sum:02x}"

# Global calculator management
calculators = {}  # {window: {'id': identifier, 'label': label_widget}}
calc_counter = 0  # Counter for unique identifiers (a-z cycling)
max_calculators = 10

def create_calculator_window(calc_id):
    """Create a new calculator window with the given identifier."""
    window = tkinter.Tk()
    window.title(f"Secret Calculator - {calc_id}")
    
    # Store in global dict
    calculators[window] = {'id': calc_id}
    
    # Main frame
    frame = tkinter.Frame(window)
    
    # Top control row (packed)
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
        command=lambda w=window: show_modes(w)
    )
    coming_soon_button.pack(side="left", padx=5, pady=5)
    
    # Calculator frame (grid-based)
    calc_frame = tkinter.Frame(frame)
    calc_frame.pack()
    calculators[window]['calc_frame'] = calc_frame
    
    # Display label
    label = tkinter.Label(calc_frame, text="0", font=("Arial", 50), bg=rich_black, fg=white, anchor="e", width=column_count)
    label.grid(row=0, column=0, columnspan=column_count, sticky="ew")
    calculators[window]['display'] = label
    
    # Calculator buttons
    for row in range(row_count):
        for column in range(column_count):
            value = buttons[row][column]
            button = tkinter.Button(
                calc_frame, 
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
    
    # Handle window closing
    window.protocol("WM_DELETE_WINDOW", lambda w=window: close_calculator(w))
    
    frame.pack()
    return window


def create_scientific_calculator_window(calc_id):
    """Create a calculator window preconfigured with a left column for scientific buttons."""
    window = tkinter.Tk()
    window.title(f"Secret Calculator - {calc_id}")
    calculators[window] = {'id': calc_id}

    # Main frame
    frame = tkinter.Frame(window)

    # Top control row
    control_frame = tkinter.Frame(frame, bg=rich_black, height=60)
    control_frame.pack(fill="x", padx=5, pady=5)
    new_calc_button = tkinter.Button(control_frame, text="+", font=("Arial", 16), width=5, bg=rich_black, fg=neon_ligth_blue, activebackground=blueberry, command=lambda: add_new_calculator())
    new_calc_button.pack(side="left", padx=5, pady=5)
    id_label = tkinter.Label(control_frame, text=calc_id, font=("Arial", 14), bg=rich_black, fg=white, width=10, relief="solid", borderwidth=1)
    id_label.pack(side="left", padx=5, pady=5)
    id_label.bind("<Button-1>", lambda e, w=window, lbl=id_label: edit_calculator_id(w, lbl))
    calculators[window]['label'] = id_label
    coming_soon_button = tkinter.Button(control_frame, text="Coming soon", font=("Arial", 14), width=12, bg=rich_black, fg=white, activebackground=blueberry, command=lambda w=window: show_modes(w))
    coming_soon_button.pack(side="left", padx=5, pady=5)

    # Content: left column + grid
    content = tkinter.Frame(frame)
    content.pack()

    left = tkinter.Frame(content)
    left.pack(side='left', padx=(0,6), fill='y')
    # scientific buttons
    ops = ["sin", "cos", "tan", "ln", "exp"]
    display_dummy = tkinter.Label(left, text='')
    display_dummy.pack()
    for op_name in ops:
        btn = tkinter.Button(left, text=op_name, font=("Arial", 14), width=8, command=lambda n=op_name: None)
        btn.pack(pady=4, padx=2)

    # Grid frame
    calc_frame = tkinter.Frame(content)
    calc_frame.pack(side='left')
    calculators[window]['calc_frame'] = calc_frame

    label = tkinter.Label(calc_frame, text="0", font=("Arial", 50), bg=rich_black, fg=white, anchor="e", width=column_count)
    label.grid(row=0, column=0, columnspan=column_count, sticky="ew")
    calculators[window]['display'] = label

    for row in range(row_count):
        for column in range(column_count):
            value = buttons[row][column]
            button = tkinter.Button(calc_frame, text=value, font=("Arial", 25), width=column_count-1, height=1, command=lambda v=value, lbl=label: button_clicked(v, lbl))
            button.grid(row=row + 1, column=column)
            if value in rigth_buttons:
                button.config(bg=rich_black, fg=neon_ligth_blue, activebackground=blueberry)
            if value in numbers_buttons:
                button.config(bg=old_silver, fg=rich_black, activebackground=white)
            elif value not in rigth_buttons and value not in numbers_buttons:
                button.config(bg=rich_black, fg=white, activebackground=blueberry)

    # Now bind the actual scientific commands to left buttons (use existing scientific_op)
    # Replace left dummy buttons with real ones
    for child in left.winfo_children():
        t = getattr(child, 'cget', lambda x: None)('text')
        if t in ops:
            child.config(command=lambda n=t, lbl=label: scientific_op(lbl, n))

    window.protocol("WM_DELETE_WINDOW", lambda w=window: close_calculator(w))
    frame.pack()
    return window

def add_new_calculator():
    """Add a new calculator window, up to max_calculators."""
    global calc_counter
    if len(calculators) >= max_calculators:
        tkinter.messagebox.showerror("Max Calculators", f"Max. calculators reached ({max_calculators})")
        return
    
    # Cycle through a-z, then restart from a
    calc_id = get_next_calc_id()
    create_calculator_window(calc_id)


def get_next_calc_id():
    """Return the next calculator id cycling a-z and increment counter."""
    global calc_counter
    calc_id = chr(ord('a') + (calc_counter % 26))
    calc_counter += 1
    return calc_id


def show_modes(parent_window):
    """Show available calculator modes in a popup and create selected mode as a new calculator."""
    modes = [
        ("Scientific", apply_scientific_mode),
        ("Converter", apply_converter_mode),
        ("Color Calculator", apply_color_mode),
    ]
    menu = tkinter.Toplevel()
    menu.title("More calculators")
    menu.transient()
    menu.grab_set()
    tkinter.Label(menu, text="Select mode:", font=("Arial", 12)).pack(padx=8, pady=8)
    for name, handler in modes:
        btn = tkinter.Button(menu, text=name, width=20, command=lambda h=handler, m=menu: (h(), m.destroy()))
        btn.pack(padx=6, pady=4)


def apply_mode_to_new_window(handler_func):
    """Helper: create new calculator id and window, then apply handler to it."""
    if len(calculators) >= max_calculators:
        tkinter.messagebox.showerror("Max Calculators", f"Max. calculators reached ({max_calculators})")
        return
    calc_id = get_next_calc_id()
    w = create_calculator_window(calc_id)
    handler_func(w)
    return w


def apply_scientific_mode():
    calc_id = get_next_calc_id()
    w = create_scientific_calculator_window(calc_id)
    apply_scientific_mode_to_window(w)
    return w


def apply_converter_mode():
    apply_mode_to_new_window(apply_converter_mode_to_window)


def apply_color_mode():
    # Open a color-only window (no standard calculator UI)
    calc_id = get_next_calc_id()
    create_color_window(calc_id)


def create_color_window(calc_id):
    """Create a color picker window for adding two colors together."""
    window = tkinter.Tk()
    window.title(f"Color Picker - {calc_id}")
    window.geometry("600x800")
    
    try:
        calculators[window] = {'id': calc_id}
    except Exception:
        pass

    # Color dictionary with name and hex - Ordered by color spectrum
    colors = {
        'Red': '#FF0000',
        'Crimson': '#DC143C',
        'Orange': '#FFA500',
        'Gold': '#FFD700',
        'Yellow': '#FFFF00',
        'Lime': '#32CD32',
        'Green': '#00FF00',
        'Sea Green': '#2E8B57',
        'Cyan': '#00FFFF',
        'Sky Blue': '#87CEEB',
        'Blue': '#0000FF',
        'Navy': '#000080',
        'Indigo': '#4B0082',
        'Purple': '#800080',
        'Magenta': '#FF00FF',
        'Violet': '#EE82EE',
        'Pink': '#FFC0CB',
        'Brown': '#A52A2A',
        'Black': '#000000',
        'Gray': '#808080',
        'White': '#FFFFFF',
    }

    # Main container
    container = tkinter.Frame(window, bg=rich_black)
    container.pack(fill='both', expand=True, padx=10, pady=10)

    # State for storing selected colors
    selected_colors = {'color1': None, 'color2': None}

    # Color 1 Preview panel
    preview1_frame = tkinter.Frame(container, bg=rich_black)
    preview1_frame.pack(fill='x', pady=(0, 10))

    preview1_label = tkinter.Label(preview1_frame, text='Color 1:', font=("Arial", 10, "bold"), 
                                    bg=rich_black, fg=white)
    preview1_label.pack(anchor='w', pady=(0, 5))

    preview1_color = tkinter.Label(preview1_frame, bg='#FFFFFF', relief='sunken', height=2)
    preview1_color.pack(fill='x', pady=(0, 5))

    preview1_info = tkinter.Label(preview1_frame, text='Select first color', font=("Arial", 12), 
                                   bg=rich_black, fg=neon_ligth_blue)
    preview1_info.pack()

    # Color 2 Preview panel
    preview2_frame = tkinter.Frame(container, bg=rich_black)
    preview2_frame.pack(fill='x', pady=(0, 10))

    preview2_label = tkinter.Label(preview2_frame, text='Color 2:', font=("Arial", 10, "bold"), 
                                    bg=rich_black, fg=white)
    preview2_label.pack(anchor='w', pady=(0, 5))

    preview2_color = tkinter.Label(preview2_frame, bg='#FFFFFF', relief='sunken', height=2)
    preview2_color.pack(fill='x', pady=(0, 5))

    preview2_info = tkinter.Label(preview2_frame, text='Select second color', font=("Arial", 12), 
                                   bg=rich_black, fg=neon_ligth_blue)
    preview2_info.pack()

    # Result Preview panel
    result_frame = tkinter.Frame(container, bg=rich_black)
    result_frame.pack(fill='x', pady=(0, 20))

    result_label = tkinter.Label(result_frame, text='Result:', font=("Arial", 10, "bold"), 
                                  bg=rich_black, fg=white)
    result_label.pack(anchor='w', pady=(0, 5))

    result_color = tkinter.Label(result_frame, bg='#FFFFFF', relief='sunken', height=2)
    result_color.pack(fill='x', pady=(0, 5))

    result_info = tkinter.Label(result_frame, text='Add colors to see result', font=("Arial", 12), 
                                bg=rich_black, fg=neon_ligth_blue)
    result_info.pack()

    # Color grid
    colors_frame = tkinter.Frame(container, bg=rich_black)
    colors_frame.pack(fill='both', expand=True)

    def calculate_result():
        """Calculate and display the average (blend 50/50) of color1 and color2."""
        if selected_colors['color1'] and selected_colors['color2']:
            # Convert to uppercase for consistency
            c1 = selected_colors['color1'].upper()
            c2 = selected_colors['color2'].upper()
            
            # Extract RGB components
            r1 = int(c1[1:3], 16)
            g1 = int(c1[3:5], 16)
            b1 = int(c1[5:7], 16)

            r2 = int(c2[1:3], 16)
            g2 = int(c2[3:5], 16)
            b2 = int(c2[5:7], 16)

            # Calculate average (50/50 blend)
            r_avg = round((r1 + r2) / 2)
            g_avg = round((g1 + g2) / 2)
            b_avg = round((b1 + b2) / 2)

            result_hex = f"#{r_avg:02X}{g_avg:02X}{b_avg:02X}"
            result_color.config(bg=result_hex)
            result_info.config(text=result_hex)
            try:
                window.clipboard_clear()
                window.clipboard_append(result_hex)
            except Exception:
                pass

    def select_color(color_name, hex_code):
        # If we have a result, reset and use this color as color1
        if selected_colors['color1'] and selected_colors['color2']:
            selected_colors['color1'] = hex_code
            selected_colors['color2'] = None
            preview1_color.config(bg=hex_code)
            preview1_info.config(text=f"{color_name}: {hex_code}")
            preview2_color.config(bg='#FFFFFF')
            preview2_info.config(text='Select second color')
            result_color.config(bg='#FFFFFF')
            result_info.config(text='Add colors to see result')
        # If we only have color1, add as color2
        elif selected_colors['color1']:
            selected_colors['color2'] = hex_code
            preview2_color.config(bg=hex_code)
            preview2_info.config(text=f"{color_name}: {hex_code}")
            calculate_result()
        # If we have nothing, add as color1
        else:
            selected_colors['color1'] = hex_code
            preview1_color.config(bg=hex_code)
            preview1_info.config(text=f"{color_name}: {hex_code}")

    # Create color buttons in grid
    cols = 4
    for idx, (name, hex_code) in enumerate(colors.items()):
        btn_frame = tkinter.Frame(colors_frame, bg=rich_black)
        btn_frame.grid(row=idx // cols, column=idx % cols, padx=5, pady=5, sticky='nsew')

        btn = tkinter.Button(btn_frame, bg=hex_code, relief='raised', bd=2,
                            command=lambda n=name, h=hex_code: select_color(n, h),
                            height=3, width=12)
        btn.pack(fill='both', expand=True)

        label = tkinter.Label(btn_frame, text=name, font=("Arial", 9), 
                             bg=rich_black, fg=white)
        label.pack()

    # Configure grid weights for responsiveness
    for i in range(5):
        colors_frame.grid_rowconfigure(i, weight=1)
    for i in range(4):
        colors_frame.grid_columnconfigure(i, weight=1)

    window.protocol('WM_DELETE_WINDOW', window.destroy)
    return window

    window.protocol('WM_DELETE_WINDOW', window.destroy)
    return window

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


### Mode implementations: add functionality to newly created windows
def apply_scientific_mode_to_window(window):
    """Add scientific operation buttons to an existing calculator window."""
    info = calculators.get(window)
    if not info:
        return
    calc_frame = info.get('calc_frame')
    display = info.get('display')
    if not calc_frame or not display:
        return

    # Place scientific buttons in a left column (modular, non-destructive)
    # If a left column already exists, reuse it
    left = info.get('left_frame')
    if left is None or not str(left).startswith(str(calc_frame)):
        left = tkinter.Frame(calc_frame)
        left.grid(row=0, column= -1, rowspan=row_count+2, sticky='ns', padx=(0,6))
        info['left_frame'] = left

    ops = ["sin", "cos", "tan", "ln", "exp"]
    for i, op_name in enumerate(ops):
        def make_cmd(name):
            return lambda n=name: scientific_op(display, n)
        btn = tkinter.Button(left, text=op_name, font=("Arial", 14), width=8, command=make_cmd(op_name))
        btn.pack(pady=4, padx=2)


def scientific_op(display_label, op_name):
    try:
        cur = evaluate_expression(display_label["text"]) if any(c in display_label["text"] for c in '()+-*/×÷') else float(display_label["text"])
        if cur == "Error":
            update_display(display_label, "Error")
            return
        if op_name == "sin":
            res = math.sin(math.radians(cur))
        elif op_name == "cos":
            res = math.cos(math.radians(cur))
        elif op_name == "tan":
            res = math.tan(math.radians(cur))
        elif op_name == "ln":
            if cur <= 0:
                update_display(display_label, "Error")
                return
            res = math.log(cur)
        elif op_name == "exp":
            res = math.exp(cur)
        else:
            return
        update_display(display_label, str(res))
    except Exception:
        update_display(display_label, "Error")


def apply_converter_mode_to_window(window):
    info = calculators.get(window)
    if not info:
        return
    # Modular Converter UI (3 slots): selector (with filter), arrow, target + category selector
    w = tkinter.Toplevel(window)
    w.title("Converter")
    container = tkinter.Frame(w)
    container.pack(padx=8, pady=8)

    # Categories and units
    UNIT_CATEGORIES = {
        'Length': ['meter','kilometer','centimeter','millimeter','inch','foot','yard','mile'],
        'Weight': ['gram','kilogram','ounce','pound'],
        'Temperature': ['celsius','fahrenheit','kelvin'],
        'Area': ['square meter','square kilometer','hectare','acre'],
        'Time': ['second','minute','hour','day'],
        'Degrees': ['radian','degree']
    }

    # Helper to flatten units with category mapping
    unit_to_category = {}
    for cat, units in UNIT_CATEGORIES.items():
        for u in units:
            unit_to_category[u] = cat

    # Left slot: filter + listbox for source units
    left_slot = tkinter.Frame(container)
    left_slot.grid(row=0, column=0, padx=4)
    tkinter.Label(left_slot, text='Source', font=("Arial", 10)).pack()
    filter_var = tkinter.StringVar()
    filter_entry = tkinter.Entry(left_slot, textvariable=filter_var)
    filter_entry.pack(pady=4)
    src_listbox = tkinter.Listbox(left_slot, height=8, exportselection=False)
    src_listbox.pack()

    # Middle slot: arrow
    mid_slot = tkinter.Frame(container)
    mid_slot.grid(row=0, column=1, padx=8)
    tkinter.Label(mid_slot, text='').pack()
    arrow_label = tkinter.Label(mid_slot, text='→', font=("Arial", 18))
    arrow_label.pack(pady=20)

    # Right slot: target units and category selector
    right_slot = tkinter.Frame(container)
    right_slot.grid(row=0, column=2, padx=4)
    tkinter.Label(right_slot, text='Target', font=("Arial", 10)).pack()
    category_var = tkinter.StringVar(value='Length')
    category_menu = tkinter.OptionMenu(right_slot, category_var, *UNIT_CATEGORIES.keys(), command=lambda _ : populate_lists())
    category_menu.pack(pady=4)
    tgt_listbox = tkinter.Listbox(right_slot, height=8, exportselection=False)
    tgt_listbox.pack()

    # Populate function
    def populate_lists():
        q = filter_var.get().lower()
        cat = category_var.get()
        src_listbox.delete(0, 'end')
        tgt_listbox.delete(0, 'end')
        units = UNIT_CATEGORIES.get(cat, [])
        for u in units:
            if q == '' or q in u:
                src_listbox.insert('end', u)
                tgt_listbox.insert('end', u)

    # Conversion function (basic examples)
    def convert_selected():
        try:
            src = src_listbox.get(src_listbox.curselection())
            tgt = tgt_listbox.get(tgt_listbox.curselection())
        except Exception:
            tkinter.messagebox.showerror('Select units', 'Please select source and target units')
            return
        val = tkinter.simpledialog.askfloat('Value', f'Enter value in {src}:')
        if val is None:
            return
        # Very simple conversions for demo purposes (length and weight examples)
        result = None
        if unit_to_category.get(src) == 'Length' and unit_to_category.get(tgt) == 'Length':
            # convert via meters
            to_m = {
                'meter':1, 'kilometer':1000, 'centimeter':0.01, 'millimeter':0.001,
                'inch':0.0254, 'foot':0.3048, 'yard':0.9144, 'mile':1609.344
            }
            meters = val * to_m[src]
            result = meters / to_m[tgt]
        elif unit_to_category.get(src) == 'Weight' and unit_to_category.get(tgt) == 'Weight':
            to_g = {'gram':1,'kilogram':1000,'ounce':28.3495,'pound':453.592}
            grams = val * to_g[src]
            result = grams / to_g[tgt]
        elif unit_to_category.get(src) == 'Temperature' and unit_to_category.get(tgt) == 'Temperature':
            # basic temp conversions
            def to_c(u, v):
                if u == 'celsius': return v
                if u == 'fahrenheit': return (v - 32) * 5/9
                if u == 'kelvin': return v - 273.15
            def from_c(u, v):
                if u == 'celsius': return v
                if u == 'fahrenheit': return v * 9/5 + 32
                if u == 'kelvin': return v + 273.15
            c = to_c(src, val)
            result = from_c(tgt, c)
        elif unit_to_category.get(src) == 'Degrees' and unit_to_category.get(tgt) == 'Degrees':
            # Degrees <-> Radians conversion
            # Convert source to radians
            if src == 'degree':
                radians = val * math.pi / 180
            else:  # src == 'radian'
                radians = val
            # Convert radians to target
            if tgt == 'degree':
                result = radians * 180 / math.pi
            else:  # tgt == 'radian'
                result = radians
        else:
            tkinter.messagebox.showinfo('Unsupported', 'This demo supports length, weight, temperature, and degrees conversions')
            return
        tkinter.messagebox.showinfo('Result', f'{val} {src} = {result:.6g} {tgt}')

    # Bind filter changes
    filter_var.trace_add('write', lambda *a: populate_lists())
    populate_lists()

    # Convert button
    btn_convert = tkinter.Button(w, text='Convert', command=convert_selected)
    btn_convert.pack(pady=8)


def apply_color_mode_to_window(window):
    info = calculators.get(window)
    if not info:
        return
    # Color calculator: combine two hex colors by averaging RGB
    def combine_colors():
        c1 = tkinter.simpledialog.askstring("Color 1", "Enter first color (hex, e.g. #ff0000):")
        if not c1:
            return
        c2 = tkinter.simpledialog.askstring("Color 2", "Enter second color (hex, e.g. #00ff00):")
        if not c2:
            return
        try:
            c1 = c1.lstrip('#')
            c2 = c2.lstrip('#')
            r = (int(c1[0:2], 16) + int(c2[0:2], 16)) // 2
            g = (int(c1[2:4], 16) + int(c2[2:4], 16)) // 2
            b = (int(c1[4:6], 16) + int(c2[4:6], 16)) // 2
            res = f"#{r:02x}{g:02x}{b:02x}"
            out = tkinter.Toplevel(window)
            out.title("Color Result")
            lbl = tkinter.Label(out, text=res, bg=res, font=("Arial", 14), width=20)
            lbl.pack(padx=10, pady=10)
        except Exception:
            tkinter.messagebox.showerror("Error", "Invalid color format")

    w = tkinter.Toplevel(window)
    w.title("Color Calculator")
    tkinter.Label(w, text="Combine two colors", font=("Arial", 12)).pack(padx=8, pady=8)
    tkinter.Button(w, text="Combine", command=combine_colors).pack(padx=8, pady=6)

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

def update_display(label, text):
    """Update display text and adjust font size to fit within bounds."""
    # Round decimals to 5 decimal places if text is a number
    try:
        if '.' in text and text != "Error":
            num = float(text)
            # Check if it has more than 5 decimals
            text_parts = text.split('.')
            if len(text_parts[1]) > 5:
                num = round(num, 5)
                text = str(num)
    except Exception:
        pass
    
    label["text"] = text
    # Start with base font size of 50, reduce based on character count
    # 10 chars or less = 50pt, then scale down
    char_count = len(text)
    if char_count <= 7:
        font_size = 50
    else:
        # Reduce by ~2pt per extra character
        font_size = max(20, 50 - (char_count - 7) * 7)
    label.config(font=("Arial", font_size))


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
            update_display(label, value)
        else:
            update_display(label, label["text"] + value)
    # Special buttons: unary operations, parentheses, clear, sign
    elif value in special_buttons:
        if value == "+/-":
            # Try to toggle the entire displayed number
            try:
                current = evaluate_expression(label["text"]) if any(c in label["text"] for c in '()+-*/×÷') else float(label["text"])
                if current == "Error":
                    update_display(label, "Error")
                else:
                    update_display(label, str(-current))
            except Exception:
                update_display(label, "Error")
        elif value == ".":
            if "." not in label["text"]:
                update_display(label, label["text"] + ".")
        elif value == "AC":
            update_display(label, "0")
        elif value == "1/x":
            try:
                cur = evaluate_expression(label["text"]) if any(c in label["text"] for c in '()+-*/×÷') else float(label["text"])
                if cur == 0 or cur == "Error":
                    update_display(label, "Error")
                else:
                    update_display(label, str(1.0 / cur))
            except Exception:
                update_display(label, "Error")
        elif value == "x²":
            try:
                cur = evaluate_expression(label["text"]) if any(c in label["text"] for c in '()+-*/×÷') else float(label["text"])
                update_display(label, str(cur * cur))
            except Exception:
                update_display(label, "Error")
        elif value == "√x":
            try:
                cur = evaluate_expression(label["text"]) if any(c in label["text"] for c in '()+-*/×÷') else float(label["text"])
                if cur < 0:
                    update_display(label, "Error")
                else:
                    update_display(label, str(math.sqrt(cur)))
            except Exception:
                update_display(label, "Error")
        elif value in ['(', ')']:
            if label["text"] == "0" or label["text"] == "Error":
                update_display(label, value)
            else:
                update_display(label, label["text"] + value)
    # Right-side buttons: backspace, operators, equals
    elif value in rigth_buttons:
        if value == "←":
            update_display(label, label["text"][:-1])
            if label["text"] == "":
                update_display(label, "0")
        elif value == "=":
            result = evaluate_expression(label["text"])
            if result == "Error":
                update_display(label, "Error")
            else:
                # Normalize integer display when possible
                if isinstance(result, float) and result.is_integer():
                    update_display(label, str(int(result)))
                else:
                    update_display(label, str(result))
        elif value in ["÷", "×", "-", "+"]:
            if label["text"] == "Error":
                update_display(label, "0")
            if label["text"] == "0":
                update_display(label, "0" + value)
            else:
                update_display(label, label["text"] + value)




main_window.mainloop()

#Window container (End)