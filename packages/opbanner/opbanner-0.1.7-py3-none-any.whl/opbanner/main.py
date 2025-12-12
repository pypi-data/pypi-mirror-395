import os
import re
import json
import sys
import shlex

# --- Constants ---
START_MARKER = "# ANONBANNER_START"
END_MARKER = "# ANONBANNER_END"
CONFIG_FILE = "config.json"
HOME_DIR = os.path.expanduser("~")
SHELL_CONFIGS = [".bashrc", ".zshrc"]

# --- Try importing prompt_toolkit ---
try:
    from prompt_toolkit import Application, prompt, HTML
    from prompt_toolkit.layout.containers import HSplit, Window, VSplit, DynamicContainer
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.layout.layout import Layout
    from prompt_toolkit.layout import WindowAlign
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.styles import Style as PtkStyle
    from prompt_toolkit.layout.dimension import D
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError as e:
    print(f"Debug: ImportError for prompt_toolkit: {e}")
    PROMPT_TOOLKIT_AVAILABLE = False

# --- Configuration Management ---
def load_config():
    """Loads configuration from config.json, returns defaults if not found."""
    defaults = {
        "messages": [],
        "font": None,
        "color": None,
        "pre_message_color": None,
        "message_color": None,
        "bold": False,
        "italic": False,
        "underline": False,
        "pre_messages": [],
        "custom_banner_file": None
    }
    if not os.path.exists(CONFIG_FILE):
        return defaults
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            for key, value in defaults.items():
                config.setdefault(key, value)
            return config
    except (json.JSONDecodeError, IOError):
        return defaults

def save_config(config):
    """Saves the configuration dictionary to config.json."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        print("\nConfiguration saved successfully.")
    except IOError as e:
        print(f"\nError saving configuration: {e}")

def get_yes_no_input(prompt_message, default_is_yes=False):
    """
    Prompts the user for a yes/no input.
    Returns True for 'y'/'Y' or empty (if default_is_yes), False for 'n'/'N' or empty (if not default_is_yes).
    Provides an error message for invalid input.
    """
    _input = prompt if PROMPT_TOOLKIT_AVAILABLE else input
    while True:
        default_str = "(Y/n)" if default_is_yes else "(y/N)"
        response = _input(f"{prompt_message} {default_str}: ").strip().lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        elif response == '':
            return default_is_yes # Return default based on argument
        else:
            print(f"Invalid input. Please enter 'y' for yes, 'n' for no, or press Enter for {'yes' if default_is_yes else 'no'}.")

COLOR_MAP = {
    "black": 0, "red": 1, "green": 2, "yellow": 3, "blue": 4, "magenta": 5, "cyan": 6, "white": 7,
    "bright_black": 8, "bright_red": 9, "bright_green": 10, "bright_yellow": 11, 
    "bright_blue": 12, "bright_magenta": 13, "bright_cyan": 14, "bright_white": 15,
}

def validate_color_input(color_choice):
    """
    Validates if the color_choice is a recognized color name or a valid ANSI 0-255 code.
    Returns the validated color string or None if invalid.
    """
    if not color_choice: # Empty input is valid for default
        return None
    if color_choice.lower() in COLOR_MAP:
        return color_choice.lower()
    if color_choice.isdigit():
        code = int(color_choice)
        if 0 <= code <= 255:
            return str(code) # Store as string to be consistent with named colors
    return False # Indicate invalid input

# --- Core Logic ---
def uninstall_from_file(config_path):
    """Helper to remove the banner from a single shell file."""
    if not os.path.exists(config_path): return 0
    try:
        with open(config_path, "r") as f: content = f.read()
        pattern = re.compile(f"\\n{START_MARKER}.*?{END_MARKER}\\n", re.DOTALL)
        new_content, count = pattern.subn("", content)
        if count > 0:
            with open(config_path, "w") as f: f.write(new_content)
        return count
    except IOError as e:
        print(f"Error processing {config_path}: {e}")
        return 0

def install_banner():
    """Installs the banner using the saved configuration."""
    print("\nInstalling banner...")
    config = load_config()
    
    command_parts_for_shell = []
    command_parts_for_shell.append("/usr/bin/python3")
    command_parts_for_shell.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "anonbanner.py"))

    if config.get("font"):
        command_parts_for_shell.append("--font")
        command_parts_for_shell.append(config["font"])

    if config.get("pre_message_color"):
        command_parts_for_shell.append("--pre-message-color")
        command_parts_for_shell.append(config["pre_message_color"])
    if config.get("message_color"):
        command_parts_for_shell.append("--message-color")
        command_parts_for_shell.append(config["message_color"])
    
    if config.get("bold"):
        command_parts_for_shell.append("--bold")
    if config.get("italic"):
        command_parts_for_shell.append("--italic")
    if config.get("underline"):
        command_parts_for_shell.append("--underline")

    if config.get("custom_banner_file"):
        command_parts_for_shell.append("--custom-banner-file")
        command_parts_for_shell.append(config["custom_banner_file"])
    if config.get("pre_messages"):
        command_parts_for_shell.append("--pre_messages")
        for msg in config["pre_messages"]:
            command_parts_for_shell.append(msg)
    if config.get("messages"):
        command_parts_for_shell.append("--messages")
        for msg in config["messages"]:
            command_parts_for_shell.append(msg)
    
    # Now, join these parts with spaces, and add line continuations
    command = shlex.join(command_parts_for_shell)

    code_block = (
        f"\n{START_MARKER}\n"
        f"        {command}\n"
        f"{END_MARKER}\n"
    )

    for shell_file in SHELL_CONFIGS:
        config_path = os.path.join(HOME_DIR, shell_file)
        if os.path.exists(config_path):
            uninstall_from_file(config_path)
            try:
                with open(config_path, "a") as f: f.write(code_block)
                print(f"Successfully installed anonbanner in {config_path}")
            except IOError as e:
                print(f"Error writing to {config_path}: {e}")
        else:
            print(f"{config_path} not found. Skipping.")

def configure_banner():
    """Gets custom settings from the user and saves them."""
    config = load_config()
    print("\n--- Configure Custom Banner ---")
    print("Enter new values or press Enter to keep the current setting.")

    _input = prompt if PROMPT_TOOLKIT_AVAILABLE else input

    # Clear existing styles - Moved to top
    if get_yes_no_input("Clear existing font and color settings?"):
        config["font"] = None
        config["pre_message_color"] = None
        config["message_color"] = None
        config["messages"] = []
        config["pre_messages"] = []
        config["bold"] = False
        config["italic"] = False
        config["underline"] = False
        config["custom_banner_file"] = None
        print("Font, color, and message settings cleared.")
    # Pre-Messages
    current_pre_messages = config.get('pre_messages', [])
    print(f"\nCurrent pre-messages: {current_pre_messages}")

    pre_msg1_input = _input("Enter the first line for top messages (Press Enter to keep the current line): ")
    pre_msg2_input = _input("Enter the second line for top messages (optional, Press Enter to keep the current line): ")

    final_pre_messages = []
    
    # Determine final pre-line 1
    pre_line1 = pre_msg1_input if pre_msg1_input else (current_pre_messages[0] if len(current_pre_messages) > 0 else None)
    if pre_line1:
        final_pre_messages.append(pre_line1)

    # Determine final pre-line 2
    pre_line2 = pre_msg2_input if pre_msg2_input else (current_pre_messages[1] if len(current_pre_messages) > 1 else None)
    if pre_line2:
        if final_pre_messages: # Only add a second line if a first line exists
            final_pre_messages.append(pre_line2)

    if not final_pre_messages or not any(m.strip() for m in final_pre_messages):
        config["pre_messages"] = []
    else:
        config["pre_messages"] = final_pre_messages

    # Messages
    messages = config.get('messages', [])
    print(f"\nCurrent messages: {messages}")

    msg1_input = _input("Enter the first line for bottom messages (Press Enter to keep the current line): ")
    msg2_input = _input("Enter the second line for bottom messages (optional, Press Enter to keep the current line): ")

    final_messages = []
    
    # Determine final line 1
    line1 = msg1_input if msg1_input else (messages[0] if len(messages) > 0 else None)
    if line1:
        final_messages.append(line1)

    # Determine final line 2
    line2 = msg2_input if msg2_input else (messages[1] if len(messages) > 1 else None)
    if line2:
        if final_messages: # Only add a second line if a first line exists
            final_messages.append(line2)

    config["messages"] = final_messages


    # Font
    print(f"\nCurrent font: {config.get('font') or 'default'}")
    print("Note: This uses pyfiglet fonts. If pyfiglet is not installed, plain text will be used.")
    if get_yes_no_input("Change font?"):
        try:
            import pyfiglet
            print("Enter a font name (e.g., standard, slant, big, digital")
            font_choice = _input("Font name (leave empty for default): ")
            config["font"] = font_choice if font_choice else None
        except ImportError:
            print("\033[91mWarning: pyfiglet is not installed.\033[0m Run 'pip install pyfiglet' to use custom fonts.")



    
    # Top Message Color
    print(f"\nCurrent top message color: {config.get('pre_message_color') or 'default'}")
    if get_yes_no_input("Change top message color?"):
        while True:
            print("Colors: red, green, yellow, blue, magenta, cyan, white (or ANSI 0-255 code)")
            color_choice = _input("Color name or code (leave empty for default): ").lower()
            validated_color = validate_color_input(color_choice)
            if validated_color is not False:
                config["pre_message_color"] = validated_color
                break
            else:
                print("Invalid color name or code. Please try again.")

    # Bottom Message Color
    print(f"\nCurrent bottom message color: {config.get('message_color') or 'default'}")
    if get_yes_no_input("Change bottom message color?"):
        while True:
            print("Colors: red, green, yellow, blue, magenta, cyan, white (or ANSI 0-255 code)")
            color_choice = _input("Color name or code (leave empty for default): ").lower()
            validated_color = validate_color_input(color_choice)
            if validated_color is not False:
                config["message_color"] = validated_color
                break
            else:
                print("Invalid color name or code. Please try again.")
    


    # Bold
    print(f"\nCurrent bold setting: {config.get('bold')}")
    if get_yes_no_input("Toggle bold?"):
        config["bold"] = not config.get("bold", False)

    # Italic
    print(f"\nCurrent italic setting: {config.get('italic')}")
    if get_yes_no_input("Toggle italic?"):
        config["italic"] = not config.get("italic", False)

    # Underline
    print(f"\nCurrent underline setting: {config.get('underline')}")
    if get_yes_no_input("Toggle underline?"):
        config["underline"] = not config.get("underline", False)

    # Custom Banner File
    print(f"\nCurrent custom banner file: {config.get('custom_banner_file') or 'anon_banner.txt'}")
    if get_yes_no_input("Change custom banner file?"):
        custom_banner_file_choice = _input("Enter path to custom banner file (leave empty for default banner): ")
        config["custom_banner_file"] = custom_banner_file_choice if custom_banner_file_choice else None



    if get_yes_no_input("Do you want to save these configuration changes?", default_is_yes=True):
        save_config(config)
        if get_yes_no_input("\nConfiguration saved. Do you want to install this banner now?", default_is_yes=True):
            install_banner()
    else:
        print("\nConfiguration changes not saved.")

def uninstall_banner():
    """Uninstalls the banner from all shell files."""
    print("\nUninstalling banner...")
    total_count = 0
    for shell_file in SHELL_CONFIGS:
        config_path = os.path.join(HOME_DIR, shell_file)
        total_count += uninstall_from_file(config_path)
    
    if total_count == 0:
        print("No anonbanner configuration found to remove.")
    else:
        print("Uninstallation complete.")

# --- Main Menu with prompt_toolkit ---
def run_interactive_menu():
    menu_items = [
        ("Install Banner", install_banner),
        ("Configure Banner", configure_banner),
        ("Uninstall Banner", uninstall_banner),
        ("Exit", lambda: None)
    ]
    
    class MenuState:
        def __init__(self):
            self.selected_index = 0

    menu_state = MenuState()

    kb = KeyBindings()

    @kb.add('up')
    def _(event):
        menu_state.selected_index = (menu_state.selected_index - 1) % len(menu_items)
        event.app.invalidate() # Crucial: tell the app to redraw

    @kb.add('down')
    def _(event):
        menu_state.selected_index = (menu_state.selected_index + 1) % len(menu_items)
        event.app.invalidate() # Crucial: tell the app to redraw

    @kb.add('enter')
    def _(event):
        event.app.exit(result=menu_state.selected_index)

    def get_current_menu_layout():
        title_text = """< https://github.com/ghostescript/opbanner >"""
        title_window = Window(content=FormattedTextControl(title_text), height=D.exact(1), always_hide_cursor=True, align=WindowAlign.CENTER)

        menu_windows = []
        for i, (label, _) in enumerate(menu_items):
            if i == menu_state.selected_index: # Use menu_state.selected_index
                menu_windows.append(Window(content=FormattedTextControl(HTML(f"> <ansiyellow>{label}</ansiyellow>")), height=D.exact(1), always_hide_cursor=True, align=WindowAlign.CENTER))
            else:
                menu_windows.append(Window(content=FormattedTextControl(HTML(f"  {label}")), height=D.exact(1), always_hide_cursor=True, align=WindowAlign.CENTER))
        
        menu_vbox = HSplit([title_window, Window(height=1)] + menu_windows)

        return HSplit([
            Window(), # Top spacer
            VSplit([
                Window(), # Left spacer
                menu_vbox,
                Window(), # Right spacer
            ]),
            Window()  # Bottom spacer
        ])

    application = Application(
        layout=Layout(DynamicContainer(get_current_menu_layout)),
        key_bindings=kb,
        full_screen=True,
        mouse_support=True,
        style=PtkStyle.from_dict({
            'ansiyellow': '#ffff00',
            'selected': 'bg:#000080 #ffffff',
        })
    )
    
    try:
        result = application.run()
        if result is not None:
            action = menu_items[result][1]
            if action:
                action()
    except KeyboardInterrupt:
        print("\n\033[91mAborted...\033[0m")
        return # Exit the function gracefully
    except Exception as e:
        print(f"\nAn error occurred during interactive menu: {e}")
        run_simple_menu()

def run_simple_menu():
    """Fallback simple menu using input()."""
    while True:
        print("\n< https://github.com/ghostescript/opbanner >")
        print()
        print("1. Install Banner")
        print("2. Configure Banner")
        print("3. Uninstall Banner")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            install_banner()
        elif choice == "2":
            configure_banner()
        elif choice == "3":
            uninstall_banner()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")
    print("Exiting.")

def main():
    if PROMPT_TOOLKIT_AVAILABLE:
        run_interactive_menu()
    else:
        print("\033[91mWarning: 'prompt_toolkit' is not installed.\033[0m")
        print("For arrow key navigation, please install it: pip install prompt_toolkit")
        run_simple_menu()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        install_banner()
    else:
        try:
            main()
        except KeyboardInterrupt:
            print("\n\033[91mAborted...\033[0m")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
