import pymem
import pymem.process
import keyboard
import threading
import time
import json
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import sys
import win32api
import win32con
from tkinter import Tk, Label, Checkbutton, BooleanVar, Button, Frame, Entry, StringVar
from tkinter.ttk import Notebook
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import pygame

print("Elden Ring Loadout Manager — Make sure The game [eldenring.exe] is Running!")

PROFILE_FILE = "profile.json"
current_profile = "default"


temp_preset_before_mimic = {}
PROCESS_NAME = "eldenring.exe"
def get_file(name):
    return f"{name}_{current_profile}.json"

PRESET_FILE = get_file("presets")
SETTINGS_FILE = get_file("settings")
KEYBOARD_HOTKEYS_FILE = get_file("keyboard_hotkeys")
CONTROLLER_HOTKEYS_FILE = get_file("controller_hotkeys")
PROFILES_DIR = "Profiles"
os.makedirs(PROFILES_DIR, exist_ok=True)

MIMIC_SLOT_INDEX = 4

import os
import json

PROFILE_FILE = "profile.json"
current_profile = "default"

PRESET_FILE = f"{current_profile}_presets.json"
SETTINGS_FILE = f"{current_profile}_settings.json"
KEYBOARD_HOTKEYS_FILE = f"{current_profile}_keyboard_hotkeys.json"
CONTROLLER_HOTKEYS_FILE = f"{current_profile}_controller_hotkeys.json"

profiles = {
    "default": {},
}
if os.path.exists("profiles.json"):
    with open("profiles.json", 'r') as f:
        try:
            profiles = json.load(f)
        except json.JSONDecodeError:
            profiles = {"default": {}}
else:
    profiles = {"default": {}}





DEFAULT_HOTKEYS = {
    "save_preset_1": "shift+1",
    "save_preset_2": "shift+2",
    "save_preset_3": "shift+3",
    "save_preset_4": "shift+4",
    "save_mimic": "shift+0",
    "load_preset_1": "ctrl+1",
    "load_preset_2": "ctrl+2",
    "load_preset_3": "ctrl+3",
    "load_preset_4": "ctrl+4",
}

DEFAULT_CONTROLLER_HOTKEYS = {
    "save_preset_1": ("LT", "RT", "DPad Up"),
    "load_preset_1": ("RT", "DPad Up"),
    "save_preset_2": ("LT", "RT", "DPad Right"),
    "load_preset_2": ("RT", "DPad Right"),
    "save_preset_3": ("LT", "RT", "DPad Down"),
    "load_preset_3": ("RT", "DPad Down"),
    "save_preset_4": ("LT", "RT", "DPad Left"),
    "load_preset_4": ("RT", "DPad Left"),
    "save_mimic": ("LT", "RT", "LS")
}

CONTROLLER_BUTTONS = {
    "None": None,
    "A": 0,
    "B": 1,
    "X": 2,
    "Y": 3,
    "LB": 4,
    "RB": 5,
    "Back": 6,
    "Start": 7,
    "LS": 8,
    "RS": 9,
    "DPad Up": "hat_up",
    "DPad Down": "hat_down",
    "DPad Left": "hat_left",
    "DPad Right": "hat_right",
    "LT": "lt_axis",
    "RT": "rt_axis"
}
REVERSE_CONTROLLER_BUTTONS = {v: k for k, v in CONTROLLER_BUTTONS.items()}

hotkeys = {} 
keyboard_hotkeys = {}
controller_hotkeys = {}

def save_current_profile():
    with open(PROFILE_FILE, 'w') as f:
        json.dump({"profile": current_profile}, f)

def save_profiles():
    with open("profiles.json", 'w') as f:
        json.dump(profiles, f)
        
def set_file_paths_from_profile(profile_name):
    global PRESET_FILE, SETTINGS_FILE, KEYBOARD_HOTKEYS_FILE, CONTROLLER_HOTKEYS_FILE
    profile_folder = os.path.join("Profiles", profile_name)
    os.makedirs(profile_folder, exist_ok=True)
    PRESET_FILE = os.path.join(profile_folder, "presets.json")
    SETTINGS_FILE = os.path.join(profile_folder, "settings.json")
    KEYBOARD_HOTKEYS_FILE = os.path.join(profile_folder, "keyboard_hotkeys.json")
    CONTROLLER_HOTKEYS_FILE = os.path.join(profile_folder, "controller_hotkeys.json")

set_file_paths_from_profile(current_profile)

        
# Load keyboard hotkeys
if os.path.exists(KEYBOARD_HOTKEYS_FILE):
    with open(KEYBOARD_HOTKEYS_FILE, 'r') as f:
        try:
            keyboard_hotkeys = json.load(f)
        except json.JSONDecodeError:
            pass
else:
    keyboard_hotkeys = DEFAULT_HOTKEYS.copy()

# Load controller hotkeys
if os.path.exists(CONTROLLER_HOTKEYS_FILE):
    with open(CONTROLLER_HOTKEYS_FILE, 'r') as f:
        try:
            controller_hotkeys = json.load(f)
        except json.JSONDecodeError:
            pass
else:
    controller_hotkeys = {k: '+'.join(v) for k, v in DEFAULT_CONTROLLER_HOTKEYS.items()}

hotkeys.update(keyboard_hotkeys)
hotkeys.update(controller_hotkeys)


EQUIPMENT_SLOTS = {
    "Head": {"module": PROCESS_NAME, "base_offset": 0x03D5DF38, "offsets": [0x8, 0x3C8]},
    "Armor": {"module": PROCESS_NAME, "base_offset": 0x03D7BB28, "offsets": [0x168, 0x3CC]},
    "Gloves": {"module": PROCESS_NAME, "base_offset": 0x03D5DF38, "offsets": [0x8, 0x3D0]},
    "Legs": {"module": PROCESS_NAME, "base_offset": 0x03D5DF38, "offsets": [0x8, 0x3D4]},
    "Weapon_R1": {"module": PROCESS_NAME, "base_offset": 0x03D7BB28, "offsets": [0x168, 0x39C]},
    "Weapon_R2": {"module": PROCESS_NAME, "base_offset": 0x03D5DF38, "offsets": [0x8, 0x3A4]},
    "Weapon_R3": {"module": PROCESS_NAME, "base_offset": 0x03D5DF38, "offsets": [0x8, 0x3AC]},
    "Weapon_L1": {"module": PROCESS_NAME, "base_offset": 0x03D7BB28, "offsets": [0x168, 0x398]},
    "Weapon_L2": {"module": PROCESS_NAME, "base_offset": 0x03D5DF38, "offsets": [0x8, 0x3A0]},
    "Weapon_L3": {"module": PROCESS_NAME, "base_offset": 0x03D7BB28, "offsets": [0x168, 0x3A8]},
    "Talisman_1": {"module": PROCESS_NAME, "base_offset": 0x03B40818, "offsets": [0x180, 0x3DC]},
    "Talisman_2": {"module": PROCESS_NAME, "base_offset": 0x03B40818, "offsets": [0x180, 0x3E0]},
    "Talisman_3": {"module": PROCESS_NAME, "base_offset": 0x03B40818, "offsets": [0x180, 0x3E4]},
    "Talisman_4": {"module": PROCESS_NAME, "base_offset": 0x03B40818, "offsets": [0x180, 0x3E8]}
}

presets = [{} for _ in range(5)]
settings = {slot: True for slot in EQUIPMENT_SLOTS.keys()}
hotkeys = {}
hotkeys.update(keyboard_hotkeys)
hotkeys.update(controller_hotkeys)
radial_ui_active = False
mimic_enabled = True
exit_requested = False

# --- Load Files ---
for path, target, default in [
    (PRESET_FILE, presets, [{} for _ in range(5)]),
    (SETTINGS_FILE, settings, settings),
]:
    if os.path.exists(path):
        with open(path, 'r') as f:
            try:
                data = json.load(f)
                if isinstance(target, list):
                    for i, p in enumerate(data):
                        if i < len(target):
                            target[i] = p
                else:
                    target.update(data)
            except json.JSONDecodeError:
                pass


def show_popup(message):
    def popup():
        root = Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.geometry("250x50+50+50")
        label = Label(root, text=message, bg="#222", fg="white", font=("Segoe UI", 12))
        label.pack(fill="both", expand=True)
        root.after(1500, root.destroy)
        root.mainloop()
    threading.Thread(target=popup).start()

def resolve_pointer(pm, base, offsets):
    addr = pymem.process.module_from_name(pm.process_handle, base).lpBaseOfDll
    addr += offsets[0]
    for offset in offsets[1:]:
        addr = pm.read_ulonglong(addr)
        if addr == 0:
            return None
        addr += offset
    return addr

def is_slot_enabled(slot):
    return settings.get(slot, True)

def save_settings():
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

def save_hotkeys():
    with open(KEYBOARD_HOTKEYS_FILE, 'w') as f:
        json.dump(keyboard_hotkeys, f)
    with open(CONTROLLER_HOTKEYS_FILE, 'w') as f:
        json.dump(controller_hotkeys, f)
        
def capture_current_gear():
    pm = pymem.Pymem(PROCESS_NAME)
    current = {}
    for name, info in EQUIPMENT_SLOTS.items():
        addr = resolve_pointer(pm, info['module'], [info['base_offset']] + info['offsets'])
        if addr:
            current[name] = pm.read_int(addr)
    return current

def save_preset(slot_index):
    pm = pymem.Pymem(PROCESS_NAME)
    preset = {}
    for name, info in EQUIPMENT_SLOTS.items():
        if is_slot_enabled(name):
            addr = resolve_pointer(pm, info['module'], [info['base_offset']] + info['offsets'])
            if addr:
                preset[name] = pm.read_int(addr)
    if slot_index >= len(presets):
        presets.extend([{}] * (slot_index + 1 - len(presets)))
    presets[slot_index] = preset
    with open(PRESET_FILE, 'w') as f:
        json.dump(presets, f)
    show_popup(f"Saved preset {slot_index + 1 if slot_index != MIMIC_SLOT_INDEX else 'Mimic'}")

def load_preset(slot_index):
    pm = pymem.Pymem(PROCESS_NAME)
    if slot_index >= len(presets):
        show_popup(f"Preset slot {slot_index} not found.")
        return
    preset = presets[slot_index]
    if not preset:
        show_popup(f"Preset {slot_index + 1 if slot_index != MIMIC_SLOT_INDEX else 'Mimic'} is empty.")
        return
    for name, value in preset.items():
        if is_slot_enabled(name):
            info = EQUIPMENT_SLOTS.get(name)
            if info:
                addr = resolve_pointer(pm, info['module'], [info['base_offset']] + info['offsets'])
                if addr:
                    pm.write_int(addr, value)
    show_popup(f"Loaded preset {slot_index + 1 if slot_index != MIMIC_SLOT_INDEX else 'Mimic'}")

def simulate_keypress_vk(vk):
    win32api.keybd_event(vk, 0, 0, 0)
    time.sleep(0.02)
    win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)

def trigger_mimic_chain():
    simulate_keypress_vk(0x45)  # 'E'
    time.sleep(0.05)
    simulate_keypress_vk(win32con.VK_DOWN)

def delayed_restore_original_gear():
    time.sleep(2)
    pm = pymem.Pymem(PROCESS_NAME)
    for name, value in temp_preset_before_mimic.items():
        info = EQUIPMENT_SLOTS.get(name)
        if info:
            addr = resolve_pointer(pm, info['module'], [info['base_offset']] + info['offsets'])
            if addr:
                pm.write_int(addr, value)
    show_popup("Restored gear after Mimic summon")

def check_hotkey(action):
    keys = keyboard_hotkeys.get(action, "").lower().split('+')
    try:
        return all(keyboard.is_pressed(k.strip()) for k in keys if k.strip())
    except ValueError:
        return False


def check_keyboard():
    last_mimic_time = 0
    mimic_hotkey_pressed = False  # Track current hotkey state

    while not exit_requested:
        for i in range(4):
            if check_hotkey(f"save_preset_{i + 1}"):
                save_preset(i)
                time.sleep(0.5)
            elif check_hotkey(f"load_preset_{i + 1}"):
                load_preset(i)
                time.sleep(0.5)

        if check_hotkey("save_mimic"):
            save_preset(MIMIC_SLOT_INDEX)
            time.sleep(0.5)

        mimic_active = check_hotkey("load_mimic")
        current_time = time.time()

        if mimic_active and not mimic_hotkey_pressed:
            mimic_hotkey_pressed = True
            if mimic_enabled and current_time - last_mimic_time > 1.5:
                if presets[MIMIC_SLOT_INDEX]:
                    global temp_preset_before_mimic
                    temp_preset_before_mimic = capture_current_gear()
                    load_preset(MIMIC_SLOT_INDEX)
                    trigger_mimic_chain()
                    threading.Thread(target=delayed_restore_original_gear).start()
                else:
                    show_popup("Mimic preset is empty.")
                last_mimic_time = current_time

        elif not mimic_active:
            mimic_hotkey_pressed = False

        time.sleep(0.05)



def listen_gamepad():
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        return
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    rt = lt = y = False
    while not exit_requested:
        pygame.event.pump()
        rt = joystick.get_axis(5) > 0.5
        lt = joystick.get_axis(4) > 0.5
        y = joystick.get_button(3)
        ls = joystick.get_button(8) 

        hat_x, hat_y = joystick.get_hat(0)

        if hat_y == 1:
            if rt and lt:
                save_preset(0)
            elif rt:
                load_preset(0)
        elif hat_x == 1:
            if rt and lt:
                save_preset(1)
            elif rt:
                load_preset(1)
        elif hat_y == -1:
            if rt and lt:
                save_preset(2)
            elif rt:
                load_preset(2)
            elif y and mimic_enabled:
                global temp_preset_before_mimic
                temp_preset_before_mimic = capture_current_gear()
                load_preset(MIMIC_SLOT_INDEX)
                trigger_mimic_chain()
                threading.Thread(target=delayed_restore_original_gear).start()
        elif hat_x == -1:
            if rt and lt:
                save_preset(3)
            elif rt:
                load_preset(3)

        if rt and lt and ls:
            save_preset(MIMIC_SLOT_INDEX)
            time.sleep(0.5)

        time.sleep(0.002)



def show_settings_window():
    from tkinter import OptionMenu, StringVar, simpledialog, messagebox

    def build_window():
        global current_profile, PRESET_FILE, SETTINGS_FILE, KEYBOARD_HOTKEYS_FILE, CONTROLLER_HOTKEYS_FILE
        root = Tk()
        root.title("Settings")

        # --- Profile Switcher + Rename ---
        profile_frame = Frame(root)
        profile_frame.pack(pady=10)

        Label(profile_frame, text="Active Profile:").pack(side='left')

        profile_var = StringVar(value=current_profile)
        profile_menu = OptionMenu(profile_frame, profile_var, *profiles.keys())
        profile_menu.pack(side='left')

        def switch_profile(*args):
            global current_profile
            new_profile = profile_var.get()
            if new_profile != current_profile:
                current_profile = new_profile
                set_file_paths_from_profile(current_profile)
                save_current_profile()
                if root.winfo_exists():
                    root.after(100, root.destroy)  # Delayed close to avoid conflict



        profile_var.trace_add("write", switch_profile)

        def rename_profile():
            old_name = profile_var.get()
            new_name = simpledialog.askstring("Rename Profile", "Enter new profile name:", initialvalue=old_name)
            if not new_name or new_name == old_name:
                return
            if new_name in profiles:
                messagebox.showerror("Error", "Profile with that name already exists.")
                return

        def add_new_profile():
            new_name = simpledialog.askstring("New Profile", "Enter new profile name:")
            if new_name and new_name not in profiles:
                profiles[new_name] = {}
                save_profiles()

                folder = os.path.join("Profiles", new_name)
                os.makedirs(folder, exist_ok=True)
                default_data = [
                    ("presets.json", [{} for _ in range(5)]),
                    ("settings.json", {}),
                    ("keyboard_hotkeys.json", DEFAULT_HOTKEYS.copy()),
                    ("controller_hotkeys.json", {k: '+'.join(v) for k, v in DEFAULT_CONTROLLER_HOTKEYS.items()}),
                ]
                for filename, content in default_data:
                    with open(os.path.join(folder, filename), 'w') as f:
                        json.dump(content, f)

                profile_menu['menu'].add_command(label=new_name, command=lambda value=new_name: profile_var.set(value))
                profile_var.set(new_name)


        def remove_profile():
            name = profile_var.get()
            if name == "default":
                messagebox.showwarning("Cannot Remove", "You cannot remove the default profile.")
                return

            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the profile '{name}'?")
            if confirm:
                # Remove from profiles dict
                profiles.pop(name, None)
                save_profiles()

                # Delete associated folder and files
                folder = os.path.join("Profiles", name)
                if os.path.exists(folder):
                    for file in os.listdir(folder):
                        os.remove(os.path.join(folder, file))
                    os.rmdir(folder)

                # Switch back to default
                profile_var.set("default")
                current_profile = "default"
                set_file_paths_from_profile(current_profile)
                save_current_profile()
        
                # Rebuild dropdown menu
                profile_menu['menu'].delete(0, 'end')
                for pname in profiles.keys():
                    profile_menu['menu'].add_command(label=pname, command=lambda value=pname: profile_var.set(value))


        Button(profile_frame, text="Rename", command=rename_profile).pack(side='left', padx=5)
        Button(profile_frame, text="Add", command=add_new_profile).pack(side='left', padx=5)
        Button(profile_frame, text="Remove", command=remove_profile).pack(side='left', padx=5)



        # --- Tabs ---
        notebook = Notebook(root)
        notebook.pack(expand=True, fill='both')

        # --- Slot Toggle Tab ---
        slot_frame = Frame(notebook)
        toggles = {}
        for i, slot in enumerate(EQUIPMENT_SLOTS):
            var = BooleanVar(value=settings.get(slot, True))
            chk = Checkbutton(slot_frame, text=slot, var=var)
            chk.grid(row=i // 2, column=i % 2, sticky='w')
            toggles[slot] = var

        def save_slots():
            for slot, var in toggles.items():
                settings[slot] = var.get()
            save_settings()

        Button(slot_frame, text="Save", command=save_slots).grid(row=(len(EQUIPMENT_SLOTS)+1)//2, column=0, columnspan=2)
        notebook.add(slot_frame, text="Slot Toggles")

        # --- Keyboard Hotkeys Tab ---
        from tkinter.ttk import Combobox
        MODIFIER_OPTIONS = ['None', 'Shift', 'Ctrl', 'Alt']
        KEY_OPTIONS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                       'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                       'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                       'u', 'v', 'w', 'x', 'y', 'z', 'up', 'down', 'left', 'right',
                       'home', 'end', 'insert', 'delete', 'page_up', 'page_down',
                       'comma', 'period', 'semicolon', 'colon', 'slash', 'backslash', 'quote',
                       'numpad_0', 'numpad_1', 'numpad_2', 'numpad_3', 'numpad_4',
                       'numpad_5', 'numpad_6', 'numpad_7', 'numpad_8', 'numpad_9']

        hotkey_frame = Frame(notebook)
        hotkey_vars = {}
        row = 0
        for action, key_combo in keyboard_hotkeys.items():
            if action == "load_mimic":
                continue

            Label(hotkey_frame, text=action).grid(row=row, column=0, sticky='e')
            parts = key_combo.lower().split('+') if '+' in key_combo else ['None', key_combo]
            mod_val = parts[0].capitalize() if parts[0].lower() in [m.lower() for m in MODIFIER_OPTIONS] else 'None'
            mod_var = StringVar(value=mod_val)
            key_var = StringVar(value=parts[-1] if parts[-1] in KEY_OPTIONS else '')

            mod_menu = Combobox(hotkey_frame, values=MODIFIER_OPTIONS, textvariable=mod_var, width=7)
            key_menu = Combobox(hotkey_frame, values=KEY_OPTIONS, textvariable=key_var, width=10)

            mod_menu.grid(row=row, column=1, padx=2)
            key_menu.grid(row=row, column=2, padx=2)

            hotkey_vars[action] = (mod_var, key_var)
            row += 1

        def save_keys():
            for action, (mod_var, key_var) in hotkey_vars.items():
                mod = mod_var.get().lower()
                key = key_var.get().lower()
                combo = f"{mod}+{key}" if mod != 'none' else key
                keyboard_hotkeys[action] = combo
                hotkeys[action] = combo
                
            with open(KEYBOARD_HOTKEYS_FILE, 'w') as f:
                json.dump(keyboard_hotkeys, f)
                
               
            save_hotkeys()

        Button(hotkey_frame, text="Save", command=save_keys).grid(row=row, column=0, columnspan=3, pady=10)
        notebook.add(hotkey_frame, text="Keyboard Hotkeys")

        # --- Controller Hotkeys Tab ---
        controller_frame = Frame(notebook)
        controller_vars = {}
        
        controller_actions = [k for k in hotkeys.keys() if k != "load_mimic"]  # Skip "load_mimic"
        
        for i, action in enumerate(controller_actions):
            Label(controller_frame, text=action).grid(row=i, column=0, sticky='e')
            
            key_combo = hotkeys.get(action, "")
            parts = key_combo.split('+') if '+' in key_combo else [key_combo]
            
            btn1 = parts[0].strip().title() if parts[0].strip() in CONTROLLER_BUTTONS else "None"
            btn2 = parts[1].strip().title() if len(parts) > 1 and parts[1].strip() in CONTROLLER_BUTTONS else "None"
            btn3 = parts[2].strip().title() if len(parts) > 2 and parts[2].strip() in CONTROLLER_BUTTONS else "None"
            
            btn1_var = StringVar(value=btn1)
            btn2_var = StringVar(value=btn2)
            btn3_var = StringVar(value=btn3)
            
            btn1_menu = Combobox(controller_frame, values=["None"] + list(CONTROLLER_BUTTONS.keys()), textvariable=btn1_var, width=10)
            btn2_menu = Combobox(controller_frame, values=["None"] + list(CONTROLLER_BUTTONS.keys()), textvariable=btn2_var, width=10)
            btn3_menu = Combobox(controller_frame, values=["None"] + list(CONTROLLER_BUTTONS.keys()), textvariable=btn3_var, width=10)
            
            btn1_menu.grid(row=i, column=1, padx=2)
            btn2_menu.grid(row=i, column=2, padx=2)
            btn3_menu.grid(row=i, column=3, padx=2)
            
            controller_vars[action] = (btn1_var, btn2_var, btn3_var)
            
        def save_controller_keys():
            for action, (btn1_var, btn2_var, btn3_var) in controller_vars.items():
                parts = [b for b in (btn1_var.get(), btn2_var.get(), btn3_var.get()) if b != "None"]
                controller_hotkeys[action] = '+'.join(parts)
                hotkeys[action] = '+'.join(parts)
                
            with open(CONTROLLER_HOTKEYS_FILE, 'w') as f:
                json.dump(controller_hotkeys, f)
                
            save_hotkeys()
            
        Button(controller_frame, text="Save", command=save_controller_keys).grid(row=len(controller_actions), column=0, columnspan=3, pady=10)
        notebook.add(controller_frame, text="Controller Hotkeys")
        
        root.mainloop()

    threading.Thread(target=build_window).start()



def on_quit(icon, item):
    global exit_requested
    exit_requested = True
    icon.visible = False
    icon.stop()
    os._exit(0)

def toggle_mimic(icon, item):
    global mimic_enabled
    mimic_enabled = not mimic_enabled
    show_popup(f"Mimic is now {'Enabled' if mimic_enabled else 'Disabled'}")

def show_keybinds():
    show_popup("Keyboard: Shift+1–4 Save | Ctrl+1–4 Load | Shift+0 Save Mimic | E+Down Load Mimic\nController: LT+RT+DPad Save | RT+DPad Load | Y+DPad Down Mimic")

threading.Thread(target=check_keyboard, daemon=True).start()
threading.Thread(target=listen_gamepad, daemon=True).start()

image = Image.new('RGB', (64, 64), color='black')
d = ImageDraw.Draw(image)
d.text((10, 25), "ER", fill='white')
menu = (
    item("Settings", lambda icon, item: show_settings_window()),
    item(lambda text: f"Mimic: {'On' if mimic_enabled else 'Off'}", toggle_mimic),
    item("Exit", on_quit)
)
icon = pystray.Icon("eldenring", image, "Elden Ring Loadouts", menu)
icon.run_detached()

while not exit_requested:
    time.sleep(1)
