import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(expand=True, fill="both")
        self.create_widgets()
        self.full_filepath = ""

    def create_widgets(self):
        # Create a custom style for the widgets
        style = ttk.Style(self.master)

        # Status Label
        self.status_label = ttk.Label(self, text="Ready", style='TLabel')
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10, sticky='w')


        # Define colors for the custom theme
        bg_color = '#F5F5F5'  # Light Grey
        fg_color = '#333333'  # Dark Grey
        highlight_color = '#4CAF50'  # Green
        accent_color = '#FFC107'  # Amber
        button_bg = '#E0E0E0'  # Grey 300

        # Set the default font and background colors
        style.configure('.', font=('Helvetica', 12), background=bg_color, foreground=fg_color)

        # Set the colors for specific elements of the widgets
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', padding=10, foreground=fg_color)
        style.configure('TEntry', padding=10)
        style.configure('TButton', padding=10, foreground=fg_color, background=button_bg)

        # Highlighted elements
        style.configure('Highlight.TLabel', foreground=highlight_color)
        style.configure('Highlight.TButton', foreground=highlight_color)

        # Entry for Filename
        self.filename_label = ttk.Label(self, text="Filename:", style='Highlight.TLabel')
        self.filename_label.grid(row=0, column=0, sticky='w')

        self.filename_entry = ttk.Entry(self)
        self.filename_entry.grid(row=0, column=1, padx=5, pady=10, sticky='we')

        # Browse Button
        self.browse_button = ttk.Button(self, text="Browse", command=self.browse_file, style='Highlight.TButton')
        self.browse_button.grid(row=0, column=2, padx=5, pady=10)

        # Video Format Entry
        self.video_format_label = ttk.Label(self, text="Video format:")
        self.video_format_label.grid(row=1, column=0, sticky='w')

        self.video_format_entry = ttk.Entry(self)
        self.video_format_entry.grid(row=1, column=1, padx=5, pady=10, sticky='we')

        # Convert Button
        self.convert_button = ttk.Button(self, text="Convert", command=self.convert_file, style='Highlight.TButton')
        self.convert_button.grid(row=2, column=1, pady=20, sticky='e')

        # Bind the <Return> event to the convert button
        self.master.bind('<Return>', lambda event: self.convert_file())

    def browse_file(self):
        self.full_filepath = filedialog.askopenfilename(filetypes=(("EDL files", "*.edl"),))
        filename = os.path.basename(self.full_filepath)
        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, filename)

    def convert_file(self):
        self.status_label.config(text="Conversion in progress...")
        self.update_idletasks()  # Force update of the GUI

        def get_sec(time_str):
            """Get Seconds from time."""
            h, m, s = time_str.split(':')
            return int(h) * 3600 + int(m) * 60 + int(s)

        if not self.full_filepath:
            print("Please select a file first")
            self.status_label.config(text="Ready")
            return

        filename = os.path.basename(self.full_filepath)
        video_format = self.video_format_entry.get()

        filename_without_extension, file_extension = os.path.splitext(filename)
        output_filename = f"{filename_without_extension}.{video_format}"

        with open(self.full_filepath) as f:
            content = f.readlines()

        with open(f'{filename_without_extension}.m3u', 'w') as f_out:
            f_out.write('#EXTM3U\n')
            for i, line in enumerate(content):
                start, stop = line.strip().split(' to ')
                f_out.write(f'#EXTINF:{get_sec(stop) - get_sec(start)},{output_filename}\n')
                f_out.write(f'#EXTVLCOPT:start-time={get_sec(start)}\n')
                f_out.write(f'#EXTVLCOPT:stop-time={get_sec(stop)}\n')
                f_out.write(f'{output_filename}\n')

        self.status_label.config(text="Conversion complete!")


root = tk.Tk()
root.title("EDL Converter")

# Set the custom theme for the application
style = ttk.Style()
style.theme_create('custom', parent='alt', settings={
    'TFrame': {'configure': {'background': '#F5F5F5'}},  # Light Grey
    'TLabel': {'configure': {'foreground': '#333333'}},  # Dark Grey
    'TButton': {'configure': {'foreground': '#4CAF50', 'background': '#E0E0E0'}},  # Green, Grey 300
    'TEntry': {'configure': {'foreground': '#333333', 'background': 'white'}}
})
style.theme_use('custom')

app = Application(master=root)
app.mainloop()
