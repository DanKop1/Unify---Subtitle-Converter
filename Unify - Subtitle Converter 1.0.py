import tkinter as tk
from tkinter import filedialog, messagebox
import os
import tempfile
import shutil
from PIL import Image, ImageTk  # Use PIL for handling the image and transparency
import sys
import requests
import webbrowser

# Import existing modules (assuming they are in the same directory or Python path)
import Rich_Converter as rich_converter
import ASS2YTT_Converter as ass2ytt_converter
import convert_ytt2vtt

# --- VERSION INFO ---
CURRENT_VERSION = "1.0.0"
VERSION_FILE_URL = "https://raw.githubusercontent.com/DanKop1/Unify-Subtitle-Converter/main/version.txt"
RELEASE_PAGE_URL = "https://github.com/DanKop1/Unify-Subtitle-Converter/releases/latest"

def get_latest_version():
    try:
        response = requests.get(VERSION_FILE_URL)
        return response.text.strip()
    except Exception as e:
        print("No update found:", e)
        return None

def is_update_available():
    latest = get_latest_version()
    if latest and latest != CURRENT_VERSION:
        return True, latest
    return False, None

def prompt_update_if_available():
    update, latest = is_update_available()
    if update:
        from tkinter import messagebox
        response = messagebox.askyesno(
            "Update available",
            f"A new version ({latest}) is available.\n\n"
            f"You are using version {CURRENT_VERSION}.\n\n"
            "Do you want to open the download page?"
        )
        if response:
            webbrowser.open(RELEASE_PAGE_URL)

class SubtitleConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Unify - Subtitle Converter")
        self.root.geometry("468x340")  # Set geometry size
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a40")

        # Load fonts from fonts.txt - IGNORE
        #self.fonts = self.load_fonts()

        # Set taskbar icon (iconbitmap for taskbar)
        icon_path = self.get_icon_path("Logo.ico")
        self.root.iconbitmap(icon_path)  # Set the icon for taskbar

        # Set the window applet icon (iconphoto works for the window icon)
        self.set_window_icon(icon_path)
        
        # Remove the default title bar
        self.root.overrideredirect(False)  # Remove the title bar
        
        """FUCK THIS"""
        # Create a custom title bar with flat relief
        #self.custom_title_bar = tk.Frame(self.root, bg="#2a2a6a", relief="flat", bd=2)
        #self.custom_title_bar.grid(row=0, column=0, sticky="ew")

        #self.title_label = tk.Label(self.custom_title_bar, text="Unify - Subtitle Converter", fg="white", bg="#2a2a6a", font=("Segoe UI", 10, "bold"))
        #self.title_label.grid(row=0, column=0, padx=10, sticky="w")

        # Add minimize button (using absolute positioning)
        #self.minimize_button = tk.Button(self.root, text="—", bg="#2a2a6a", fg="white", relief="flat", width=2, command=self.minimize_window, font=("Segoe UI", 9, "bold"))
        #self.minimize_button.place(x=419, y=0)  # Position at the right of the title bar

        # Add close button (using absolute positioning)
        #self.close_button = tk.Button(self.root, text="X", bg="#2a2a6a", fg="white", relief="flat", width=2, command=self.root.quit, font=("Segoe UI", 9, "bold"))
        #self.close_button.place(x=444, y=0)  # Position at the right of the title bar

        # Add drag functionality to move the window (custom title bar)
        #self.custom_title_bar.bind("<B1-Motion>", self.move_window_main)
        #self.custom_title_bar.bind("<ButtonRelease-1>", self.release_window_main)
        #self.custom_title_bar.bind("<ButtonPress-1>", self.press_window_main)

        #self.x = 0
        #self.y = 0

        # Define your window contents
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.keep_rich = tk.BooleanVar()
        self.keep_ytt = tk.BooleanVar()
        self.keep_xml = tk.BooleanVar()

        self.do_rich = tk.BooleanVar()
        self.do_ytt = tk.BooleanVar()
        self.do_vtt = tk.BooleanVar()

        self.skip_rich_text = tk.BooleanVar(value=False)  # Track if rich text conversion should be skipped

        # Create widgets
        self.create_widgets()
        self.setup_drag_and_drop()  # Adding drag-and-drop functionality

        # Add the image to the bottom left
        self.add_image()

        # Add a Help Button
        self.help_button = tk.Button(self.root, text="Help", command=self.open_help_popup, bg="#2a2a6a", fg="white", relief="flat", font=("Segoe UI", 10, "bold"))
        self.help_button.place(x=380, y=300)  # Adjust position to your preference

    def get_icon_path(self, icon_name):
        """ICON mapping to path."""
        if getattr(sys, 'frozen', False):  # If running as a bundled executable
            return os.path.join(sys._MEIPASS, icon_name)  # Use the temp path provided by PyInstaller
        else:
            return icon_name  # If running from source, use the normal file path

    def set_window_icon(self, icon_path):
        """Set the window's applet icon (iconphoto for window)."""
        try:
            icon_image = Image.open(icon_path)  # Open ICO image
            icon_photo = ImageTk.PhotoImage(icon_image)  # Convert to Tkinter compatible format
            self.root.iconphoto(True, icon_photo)  # Apply this icon to the window (applet)
        except Exception as e:
            print(f"Error loading window icon: {e}")

    """Don't touch"""
    #def load_fonts(self):
            #"""Load fonts from an external fonts.txt file."""
            #if getattr(sys, 'frozen', False):  # If running from a bundled executable
                #fonts_path = os.path.join(sys._MEIPASS, "fonts.txt")
            #else:
                #fonts_path = "fonts.txt"  # If running from source, look in the current directory

            # Check if the file exists before proceeding
            #if os.path.exists(fonts_path):
                #try:
                    #with open(fonts_path, 'r') as file:
                        #fonts = file.readlines()
                        #print("Fonts loaded successfully:", fonts)
                        #return fonts  # Return the fonts data
                #except Exception as e:
                    #print(f"Error reading fonts file: {e}")
            #else:
                #print(f"Error: fonts.txt not found at {fonts_path}")
            #return []

    #def setup_conversion(self):
            #"""Pass the fonts data to the Rich_Converter."""
            #if self.fonts:
                # Pass the loaded fonts to Rich_Converter
                #rich_converter.set_fonts(self.fonts)
            #else:
                #print("No fonts data available.")

    def get_image_path(self, image_name):
        """Get the correct path to the image depending on if it's bundled or not."""
        if getattr(sys, 'frozen', False):  # If running as a bundled executable
            return os.path.join(sys._MEIPASS, image_name)  # Use the temp path provided by PyInstaller
        else:
            return image_name  # If running from source, use the normal file path
        
    def create_widgets(self):
            # Add UI elements as before
            pass
        
    def add_image(self):
        # Ensure the path is correct
        image_path = self.get_image_path("Logo name.png")  # Use the correct image path
        try:
            self.image = Image.open(image_path)  # Open the image
            self.image = self.image.resize((150, 90))  # Resize image to fit in a small box
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.image_label = tk.Label(self.root, image=self.image_tk, bg="#1a1a40")
            self.image_label.place(x=0, y=245)  # Position at bottom-left corner (adjust as needed)
        except Exception as e:
            print(f"Error loading image: {e}")

    def open_help_popup(self):
        """Open a read-only popup window with help text attached to the main window."""
        help_text = """Welcome to Unify - Subtitle Converter!
        
This tool allows you to convert ASS format subtitles into rich tag based ASS Subtitles, then convert to YTT as well as VTT 
Choose the files and output folder or drag and drop for ease of use, then click 'Start Conversion' to proceed.
You can also keep rich text files or YTT files during the conversion process.
There is also the option to keep the XML for troubleshooting

If your .ass file is already in Rich Format, you can simply click on 'Is Rich Text?' and only do the converts.

For more info, visit my GITHUB page https://github.com/DanKop1/AI-Sponge-Rehydrated-Subtitle-Tools or contact me on the Discord Server under the user Dankop for further help."""

        # Create a Toplevel window for the help text (attached to the main window)
        self.help_popup = tk.Toplevel(self.root)  # Store the reference to the popup
        self.help_popup.title("Help")
        self.help_popup.geometry("400x400+{0}+{1}".format(self.root.winfo_x(), self.root.winfo_y() + 340))  # Position below the main window
        self.help_popup.overrideredirect(True)  # Remove taskbar
        
        # Set the background color of the entire popup window (Toplevel window)
        self.help_popup.configure(bg="#1a1a40")  # Set to same color as main UI
        
        # Create a custom title bar for the help popup
        help_popup_title_bar = tk.Frame(self.help_popup, bg="#2a2a6a", relief="flat", bd=2)
        help_popup_title_bar.pack(fill="x", side="top")

        help_popup_title_label = tk.Label(help_popup_title_bar, text="Help", fg="white", bg="#2a2a6a", font=("Segoe UI", 10, "bold"))
        help_popup_title_label.pack(side="left", padx=10)

        # Add drag functionality to move the help window (custom title bar)
        help_popup_title_bar.bind("<B1-Motion>", self.move_window_help)
        help_popup_title_bar.bind("<ButtonRelease-1>", self.release_window_help)
        help_popup_title_bar.bind("<ButtonPress-1>", self.press_window_help)

        # Create a Text widget (read-only, filling the entire window)
        text_box = tk.Text(self.help_popup, wrap="word", height=18, width=50, font=("Segoe UI", 10), bg="#1a1a40", fg="white")
        text_box.insert(tk.END, help_text)
        text_box.config(state=tk.DISABLED)  # Set to read-only
        
        # Create a Close Button at the bottom of the popup
        close_button = tk.Button(self.help_popup, text="Close", command=self.help_popup.destroy, bg="#2a2a6a", fg="white", relief="flat", font=("Segoe UI", 10, "bold"))
        close_button.pack(side="bottom", pady=5)

        # Pack the Text widget to take up remaining space
        text_box.pack(expand=True, padx=10, pady=10)

    def press_window_main(self, event):
        """Store the current position of the mouse for moving the main window."""
        self.x = event.x
        self.y = event.y

    def move_window_main(self, event):
        """Move the main window when the mouse is dragged."""
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.root.geometry(f"+{self.root.winfo_x() + deltax}+{self.root.winfo_y() + deltay}")

    def release_window_main(self, event):
        """Release the main window on mouse button release."""
        pass

    def press_window_help(self, event):
        """Store the current position of the mouse for moving the help popup."""
        self.x_help = event.x
        self.y_help = event.y

    def move_window_help(self, event):
        """Move the help popup window when the mouse is dragged."""
        deltax = event.x - self.x_help
        deltay = event.y - self.y_help
        self.help_popup.geometry(f"+{self.help_popup.winfo_x() + deltax}+{self.help_popup.winfo_y() + deltay}")

    def release_window_help(self, event):
        """Release the help window on mouse button release."""
        pass

    def minimize_window(self):
        """Minimize the window."""
        self.root.iconify()  # Minimize the window

    def create_widgets(self):
        tk.Label(self.root, bg="#1a1a40", fg="white", text="Select .ass Subtitle File:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        # Create a frame for input and browse button
        file_frame = tk.Frame(self.root, bg="#1a1a40")
        file_frame.grid(row=2, column=0, padx=10, pady=2, sticky="w")

        # First entry and browse button in the same row
        self.input_entry = tk.Entry(file_frame, bg="#2a2a6a", fg="white", insertbackground="white", textvariable=self.input_file, font=("Segoe UI", 10, "bold"), relief="flat", highlightthickness=0, borderwidth=0)
        self.input_entry.grid(row=0, column=0, padx=(0, 5))

        # Apply the active color change when clicked
        tk.Button(file_frame, bg="#2a2a6a", fg="white", activebackground="white", activeforeground="black", text="Browse", width=5, relief="flat", borderwidth=0, height=1, padx=5, pady=1, font=("Segoe UI", 10, "bold"), command=self.browse_file).grid(row=0, column=1)

        # "Is Rich Text" button next to the "Browse" button
        self.is_rich_button = tk.Button(file_frame, text="Is Rich Text?", command=lambda: self.toggle_button_color(self.is_rich_button, self.skip_rich_text), bg="#2a2a6a", fg="white", relief="flat", borderwidth=0, width=10, height=1, font=("Segoe UI", 10, "bold"))
        self.is_rich_button.grid(row=0, column=2, padx=5)

        tk.Label(self.root, bg="#1a1a40", fg="white", text="Select Output Folder:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

        # Output folder frame
        out_frame = tk.Frame(self.root, bg="#1a1a40")
        out_frame.grid(row=4, column=0, padx=10, pady=2, sticky="w")

        self.output_entry = tk.Entry(out_frame, bg="#2a2a6a", fg="white", insertbackground="white", textvariable=self.output_dir, font=("Segoe UI", 10, "bold"), relief="flat", highlightthickness=0, borderwidth=0)
        self.output_entry.grid(row=0, column=0, padx=(0, 5))

        tk.Button(out_frame, bg="#2a2a6a", fg="white", activebackground="white", activeforeground="black", text="Browse", width=5, relief="flat", borderwidth=0, padx=5, pady=1, font=("Segoe UI", 10, "bold"), command=self.browse_output).grid(row=0, column=1)

        # Option checkboxes and buttons
        option_frame = tk.Frame(self.root, bg="#1a1a40")
        option_frame.grid(row=5, column=0, padx=10, pady=10)

        convert_frame = tk.Frame(option_frame, bg="#1a1a40")
        convert_frame.grid(row=0, column=0, padx=5)
        keep_frame = tk.Frame(option_frame, bg="#1a1a40")
        keep_frame.grid(row=0, column=1, padx=5)

        # Convert buttons
        self.convert_rich_button = tk.Button(convert_frame, text="Convert to Rich Text", command=lambda: self.toggle_button_color(self.convert_rich_button, self.do_rich), bg="#2a2a6a", fg="white", relief="flat", borderwidth=0, width=26, font=("Segoe UI", 10, "bold"))
        self.convert_rich_button.grid(sticky="w")

        self.convert_ytt_button = tk.Button(convert_frame, text="Convert .ass to .ytt", command=lambda: self.toggle_button_color(self.convert_ytt_button, self.do_ytt), bg="#2a2a6a", fg="white", relief="flat", borderwidth=0, width=26, font=("Segoe UI", 10, "bold"))
        self.convert_ytt_button.grid(sticky="w")

        self.convert_vtt_button = tk.Button(convert_frame, text="Convert .ytt to .vtt", command=lambda: self.toggle_button_color(self.convert_vtt_button, self.do_vtt), bg="#2a2a6a", fg="white", relief="flat", borderwidth=0, width=26, font=("Segoe UI", 10, "bold"))
        self.convert_vtt_button.grid(sticky="w")

        # Keep buttons
        self.keep_rich_button = tk.Button(keep_frame, text="Keep Rich Text File", command=lambda: self.toggle_button_color(self.keep_rich_button, self.keep_rich), bg="#2a2a6a", fg="white", relief="flat", borderwidth=0, width=26, font=("Segoe UI", 10, "bold"))
        self.keep_rich_button.grid(sticky="w")

        self.keep_ytt_button = tk.Button(keep_frame, text="Keep YTT File", command=lambda: self.toggle_button_color(self.keep_ytt_button, self.keep_ytt), bg="#2a2a6a", fg="white", relief="flat", borderwidth=0, width=26, font=("Segoe UI", 10, "bold"))
        self.keep_ytt_button.grid(sticky="w")

        self.keep_xml_button = tk.Button(keep_frame, text="Keep XML File", command=lambda: self.toggle_button_color(self.keep_xml_button, self.keep_xml), bg="#2a2a6a", fg="white", relief="flat", borderwidth=0, width=26, font=("Segoe UI", 10, "bold"))
        self.keep_xml_button.grid(sticky="w")

        # Display message label for conversion status
        self.status_label = tk.Label(self.root, bg="#1a1a40", fg="green", text="", font=("Segoe UI", 10, "bold"))
        self.status_label.grid(row=6, column=0, padx=50, pady=10)

        tk.Button(self.root, text="Start Conversion", command=self.start_conversion, relief="flat", bg="green", fg="white", font=("Segoe UI", 10, "bold")).grid(row=7, column=0, padx=50, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("ASS Subtitle Files", "*.ass")])
        if file_path:
            self.input_file.set(file_path)
            self.output_dir.set(os.path.dirname(file_path))

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir.set(folder)

    def toggle_button_color(self, button, variable, active_color="green", inactive_color="#2a2a6a"):
        """Toggle the button color based on the variable's state."""
        variable.set(not variable.get())  # Toggle the variable value
        
        # Toggle the background color of the button
        if variable.get():  # If the button is clicked (variable is True)
            button.config(relief="flat", bg=active_color)  # Change background to active color (green)
        else:  # If the button is clicked again (variable is False)
            button.config(relief="flat", bg=inactive_color)  # Revert to inactive color (#2a2a6a)

    def setup_drag_and_drop(self):
        """Set up drag-and-drop functionality to drop files into the window."""
        def drop(event):
            file_path = event.data.strip("{}")  # Clean up any extra characters
            if file_path.lower().endswith(".ass"):
                self.input_file.set(file_path)
                self.output_dir.set(os.path.dirname(file_path))

        try:
            import tkinterdnd2 as tkdnd
            self.root.drop_target_register(tkdnd.DND_FILES)
            self.root.dnd_bind('<<Drop>>', drop)
        except Exception as e:
            print("Drag and drop not available:", e)

    def start_conversion(self):
        ass_path = self.input_file.get()
        output_dir = self.output_dir.get()

        # Check if nothing is selected
        if not ass_path or not os.path.exists(ass_path) or not output_dir:
            self.status_label.config(text="Nothing selected", fg="red")  # Display error in the status label
            return

        base_name = os.path.splitext(os.path.basename(ass_path))[0]

        # Temp working files
        rich_ass = os.path.join(tempfile.gettempdir(), f"{base_name}_rich.ass")
        ytt_file = os.path.join(tempfile.gettempdir(), f"{base_name}.ytt")
        vtt_file = os.path.join(output_dir, f"{base_name}.vtt")
        xml_file = os.path.join(output_dir, f"{base_name}.xml")

        try:
            # Step 1: Rich text (this will be skipped if "Is Rich Text" is enabled)
            source_ass = ass_path
            if not self.skip_rich_text.get() and self.do_rich.get():
                rich_converter.convert_ass_file(ass_path, rich_ass)
                source_ass = rich_ass
                if self.keep_rich.get():
                    shutil.copy(rich_ass, os.path.join(output_dir, os.path.basename(rich_ass)))

            # Step 2: .ass to .ytt
            if self.do_ytt.get():
                ass2ytt_converter.convert_ass_to_ytt(source_ass, ytt_file)
                if self.keep_ytt.get():
                    shutil.copy(ytt_file, os.path.join(output_dir, os.path.basename(ytt_file)))
            elif self.do_vtt.get():
                messagebox.showerror("Pipeline Error", ".ytt to .vtt conversion selected, but no .ytt will be generated.")
                return

            # Step 3: .ytt to .vtt
            if self.do_vtt.get():
                convert_ytt2vtt.convert_ytt_to_xml(ytt_file, xml_file)
                convert_ytt2vtt.convert_xml_to_vtt(xml_file, vtt_file)
                if not self.keep_xml.get():
                    os.remove(xml_file)

            # Show success message in the window
            self.status_label.config(text="✅ Conversion complete!", fg="green")

        except Exception as e:
            # Show error message in the window
            self.status_label.config(text=f"Conversion Error: {str(e)}", fg="red")

if __name__ == "__main__":
    from tkinterdnd2 import TkinterDnD
    root = TkinterDnD.Tk()
    app = SubtitleConverterGUI(root)
    root.after(500, prompt_update_if_available)
    root.mainloop()
