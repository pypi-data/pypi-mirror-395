
import sys
import traceback
import random
import argparse
import os
import json

try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
except ImportError:
    class DummyStyle:
        def __getattr__(self, name): return ""
    Style = DummyStyle()

COLOR_MAP = {
    "black": 0, "red": 1, "green": 2, "yellow": 3, "blue": 4, "magenta": 5, "cyan": 6, "white": 7,
    "bright_black": 8, "bright_red": 9, "bright_green": 10, "bright_yellow": 11, 
    "bright_blue": 12, "bright_magenta": 13, "bright_cyan": 14, "bright_white": 15,
}



def hsl_to_rgb(h, s, l):
    if s == 0: return l, l, l
    def hue_to_rgb(p, q, t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
        return p
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    return hue_to_rgb(p, q, h + 1/3), hue_to_rgb(p, q, h), hue_to_rgb(p, q, h - 1/3)

def rgb_to_ansi256(r, g, b):
    r_255, g_255, b_255 = int(r * 255), int(g * 255), int(b * 255)
    if r_255 == g_255 and g_255 == b_255:
        if r_255 < 8: return 16
        if r_255 > 248: return 231
        return round(((r_255 - 8) / 247) * 24) + 232
    return 16 + (int(round(r_255 / 255 * 5)) * 36) + (int(round(g_255 / 255 * 5)) * 6) + int(round(b_255 / 255 * 5))

def print_styled_text(text, color_code, bold=False, italic=False, underline=False):
    if 'colorama' in sys.modules:
        style_codes = []
        if bold: style_codes.append('1') # Bold
        if italic: style_codes.append('3') # Italic
        if underline: style_codes.append('4') # Underline
        
        style_prefix = f"\033[{';'.join(style_codes)}m" if style_codes else ""
        return f"{style_prefix}\033[38;5;{color_code}m{text}{Style.RESET_ALL}"
    else:
        return text

def main():

    parser = argparse.ArgumentParser(description="Display a colorful Anonymous banner.")
    parser.add_argument('--font', default=None, help='The pyfiglet font to use for the messages.')

    parser.add_argument('--pre-message-color', default=None, help='Color for the top messages.')
    parser.add_argument('--message-color', default=None, help='Color for the bottom messages.')
    parser.add_argument('--bold', action='store_true', help='Display messages in bold.')
    parser.add_argument('--italic', action='store_true', help='Display messages in italic.')
    parser.add_argument('--underline', action='store_true', help='Display messages underlined.')
    parser.add_argument('--custom-banner-file', default=None, help='Path to a file containing custom banner ASCII art.')
    parser.add_argument('--pre_messages', nargs='*', help='Optional messages to display above the banner.')
    parser.add_argument('--messages', nargs='*', help='Optional messages to display below the banner.')
    args = parser.parse_args()

    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80  # Default width if not running in a TTY

    config_file_path = os.path.join(os.path.dirname(__file__), "config.json")
    config_data = {}
    if os.path.exists(config_file_path):
        try:
            with open(config_file_path, 'r') as f:
                config_data = json.load(f)
        except json.JSONDecodeError:
            print(print_styled_text(f"[Error: Could not decode config.json. Using default settings.]", 1))

    # Apply config values if not provided via command line
    if args.font is None and config_data.get('font') is not None:
        args.font = config_data['font']
    if args.pre_message_color is None and config_data.get('pre_message_color') is not None:
        args.pre_message_color = config_data['pre_message_color']
    if args.message_color is None and config_data.get('message_color') is not None:
        args.message_color = config_data['message_color']

    if args.bold is False and config_data.get('bold') is not None: # bold is action='store_true', so default is False
        args.bold = config_data['bold']
    if args.italic is False and config_data.get('italic') is not None:
        args.italic = config_data['italic']
    if args.underline is False and config_data.get('underline') is not None:
        args.underline = config_data['underline']
    if args.custom_banner_file is None and config_data.get('custom_banner_file') is not None:
        args.custom_banner_file = config_data['custom_banner_file']
    if not args.pre_messages and config_data.get('pre_messages') is not None:
        args.pre_messages = config_data['pre_messages']
    if args.messages is None and config_data.get('messages') is not None:
        args.messages = config_data['messages']
    
    # Load custom banner content if specified
    custom_banner_content = None
    if args.custom_banner_file == "anon_banner.txt": # Special keyword for default
        pass # Will use the hardcoded default banner
    elif args.custom_banner_file and os.path.exists(args.custom_banner_file):
        try:
            with open(args.custom_banner_file, 'r') as f:
                custom_banner_content = f.read()
        except Exception as e:
            print(print_styled_text(f"[Error: Could not read custom banner file {args.custom_banner_file}. Using default banner. Error: {e}]", 1))

    # Use custom banner content if available, otherwise use default
    if custom_banner_content:
        banner_content = custom_banner_content
    else:
        banner_content = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⠶⠶⠶⠶⠶⠶⠶⢖⣦⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠞⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠻⠶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⡞⠁⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠈⠹⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣼⠋⠀⠀⠀⢀⣤⣾⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣷⣦⣀⠀⠀⠀⠈⢿⣄⠀⠀⠀⠀⠀
⠀⠀⠀⢀⡾⠁⠀⣠⡾⢁⣾⡿⡋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣆⠹⣦⠀⠀⢻⣆⠀⠀⠀⠀
⠀⠀⢀⡾⠁⢀⢰⣿⠃⠾⢋⡔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣿⠀⢹⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡌⠻⠆⢿⣧⢀⠀⢻⣆⠀⠀⠀
⠀⠀⣾⠁⢠⡆⢸⡟⣠⣶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣦⡸⣿⠀⣆⠀⢿⡄⠀⠀
⠀⢸⡇⠀⣽⡇⢸⣿⠟⢡⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣉⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⠙⢿⣿⠀⣿⡀⠘⣿⠀⠀
⡀⣿⠁⠀⣿⡇⠘⣡⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⣦⡙⠀⣿⡇⠀⢻⡇⠀
⢸⡟⠀⡄⢻⣧⣾⡿⢋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣴⣿⠉⡄⢸⣿⠀
⢾⡇⢰⣧⠸⣿⡏⢠⡎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠀⠓⢶⠶⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣆⠙⣿⡟⢰⡧⠀⣿⠀
\⡇⠰⣿⡆⠹⣠⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣿⡏⠀⠠⢺⠢⠀⠀⣿⣷⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣧⠸⠁⣾⡇⠀⣿⠀
⣿⡇⠀⢻⣷⠀⣿⡿⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⡅⠀⠀⢸⡄⠀⠀⣿⣿⣿⣿⣿⣿⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⡆⣰⣿⠁⠀⣿⠀
⢸⣧⠀⡈⢿⣷⣿⠃⣰⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⣇⠀⢀⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣸⡀⢿⣧⣿⠃⡀⢸⣿⠀
⠀⣿⡀⢷⣄⠹⣿⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⣿⣿⠀⣼⣿⣿⣿⣿⣿⣿⣿⡯⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⢸⡟⢁⣴⠇⣼⡇⠀
⠀⢸⡇⠘⣿⣷⡈⢰⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⣿⣿⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⢰⣿⡧⠈⣴⣿⠏⢠⣿⠀⠀
⠀⠀⢿⡄⠘⢿⣿⣦⣿⣯⠘⣆⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⡎⢸⣿⣣⣾⡿⠏⠀⣾⠇⠀⠀
⠀⠀⠈⢷⡀⢦⣌⠛⠿⣿⡀⢿⣆⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢀⣿⡁⣼⡿⠟⣉⣴⠂⣼⠏⠀⠀⠀
⠀⠀⠀⠈⢷⡈⠻⣿⣶⣤⡁⠸⣿⣆⠡⡀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⢀⣾⡟⠀⣡⣴⣾⡿⠁⣴⠏⠀⠀⠀⠀
⠀⠀⠀⠀⠈⢿⣄⠈⢙⠿⢿⣷⣼⣿⣦⠹⣶⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⢡⣾⣿⣶⣿⠿⢛⠉⢀⣾⠏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠹⣧⡀⠳⣦⣌⣉⣙⠛⠃⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠐⠛⠋⣉⣉⣤⡶⣰⡿⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡀⠙⠛⠿⠿⠿⠿⠟⠛⠛⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠙⠟⠛⠿⠿⠿⠿⠟⠛⠁⣠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢶⣄⠙⠶⣦⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⡶⠖⣁⣴⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣶⣄⡉⠉⠉⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠉⠉⠉⠉⣡⣴⡾⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠷⢦⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣠⣴⠶⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

    try:
        banner_lines = banner_content.strip().split('\n')
        max_width = max(len(line) for line in banner_lines)
        solid_line = "─" * max_width
        banner_padding = " " * ((terminal_width - max_width) // 2)

        start_hue = random.random()
        hue_sweep_range = random.uniform(0.05, 0.2) # Smaller range for hue change
        start_lightness = random.uniform(0.1, 0.2) # Tighter range
        end_lightness = random.uniform(0.8, 0.9)   # Tighter range
        saturation = random.uniform(0.8, 1.0) # Higher saturation

        r_top, g_top, b_top = hsl_to_rgb(start_hue, saturation, start_lightness)

        # Determine color for pre_messages (top messages)
        pre_message_color_code = rgb_to_ansi256(r_top, g_top, b_top)

        if args.pre_message_color: # Use new argument
            if args.pre_message_color.lower() in COLOR_MAP:
                pre_message_color_code = COLOR_MAP[args.pre_message_color.lower()]
            elif args.pre_message_color.isdigit() and 0 <= int(args.pre_message_color) <= 255:
                pre_message_color_code = int(args.pre_message_color)

        print(banner_padding + print_styled_text(solid_line, rgb_to_ansi256(r_top, g_top, b_top)))
        print() # This adds a blank line
        print() # Add another blank line for spacing

        if args.pre_messages:
            for msg in args.pre_messages:
                message_inner_padding = " " * ((max_width - len(msg)) // 2) # Center relative to banner width
                print(f"{banner_padding}{message_inner_padding}{print_styled_text(msg, pre_message_color_code, args.bold, args.italic, args.underline)}")
            print() # This adds a blank line after pre-messages

        for i, line in enumerate(banner_lines):
            factor = i / max(1, len(banner_lines) - 1)
            h = (start_hue + factor * hue_sweep_range) % 1.0
            l = start_lightness + factor * (end_lightness - start_lightness)
            r, g, b = hsl_to_rgb(h, saturation, l)
            print(banner_padding + print_styled_text(line, rgb_to_ansi256(r, g, b)))
        
        print()

        r_bot, g_bot, b_bot = hsl_to_rgb((start_hue + hue_sweep_range) % 1.0, saturation, end_lightness)
        default_color_code = rgb_to_ansi256(r_bot, g_bot, b_bot)
        
        # Determine color for messages_to_print (bottom messages)
        bottom_message_color_code = default_color_code
        if args.message_color: # Use new argument
            if args.message_color.lower() in COLOR_MAP:
                bottom_message_color_code = COLOR_MAP[args.message_color.lower()]
            elif args.message_color.isdigit() and 0 <= int(args.message_color) <= 255:
                bottom_message_color_code = int(args.message_color)


        print()


        messages_to_print = args.messages if args.messages is not None else []

        if args.font:
            try:
                from pyfiglet import Figlet, FontNotFound
                f = Figlet(font=args.font)
                for message in messages_to_print:
                    rendered_text = f.renderText(message)
                    for line in rendered_text.rstrip().split('\n'):
                        message_inner_padding = " " * ((max_width - len(line)) // 2) # Center relative to banner width
                        print(f"{banner_padding}{message_inner_padding}{print_styled_text(line, bottom_message_color_code, args.bold, args.italic, args.underline)}")
            except ImportError:
                print(print_styled_text(f"[pyfiglet not installed. Using plain text.]", 1))
                for msg in messages_to_print:
                    message_inner_padding = " " * ((max_width - len(msg)) // 2) # Center relative to banner width
                    print(f"{banner_padding}{message_inner_padding}{print_styled_text(msg, bottom_message_color_code, args.bold, args.italic, args.underline)}")
            except FontNotFound:
                print(print_styled_text(f"[Font '{args.font}' not found. Using plain text.]", 1))
                for msg in messages_to_print:
                    message_inner_padding = " " * ((max_width - len(msg)) // 2) # Center relative to banner width
                    print(f"{banner_padding}{message_inner_padding}{print_styled_text(msg, bottom_message_color_code, args.bold, args.italic, args.underline)}")
        else:
            for msg in messages_to_print:
                message_inner_padding = " " * ((max_width - len(msg)) // 2) # Center relative to banner width
                print(f"{banner_padding}{message_inner_padding}{print_styled_text(msg, bottom_message_color_code, args.bold, args.italic, args.underline)}")
        print() # Add a blank line after bottom messages
        print(banner_padding + print_styled_text(solid_line, default_color_code)) # Bottom line should keep the gradient color}

    except Exception as e:
        log_file_path = os.path.join(os.path.dirname(__file__), "logs", "anonbanner_error.log")
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, "a") as f:
            f.write(f"An error occurred: {e}\n")
            f.write(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
