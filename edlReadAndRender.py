import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Create a custom style for the widgets
        style = ttk.Style(self.master)

        # Define colors for the custom theme
        bg_color = '#F0F0F0'
        fg_color = '#333333'
        highlight_color = '#FFC107'

        # Set the default font and background colors
        style.configure('.', font=('Helvetica', 12), background=bg_color, foreground=fg_color)

        # Set the colors for specific elements of the widgets
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', padding=10, foreground=highlight_color)
        style.configure('TEntry', padding=10)
        style.configure('TButton', padding=10, foreground=highlight_color, background=fg_color)

        # Create the filename label and entry widgets
        self.filename_label = ttk.Label(self, text="Filename:")
        self.filename_label.grid(row=0, column=0, sticky='w')

        self.filename_entry = ttk.Entry(self)
        self.filename_entry.grid(row=0, column=1, padx=5, pady=10, sticky='we')

        self.browse_button = ttk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=10)

        # Create the video format label and entry widgets
        self.video_format_label = ttk.Label(self, text="Video format:")
        self.video_format_label.grid(row=1, column=0, sticky='w')

        self.video_format_entry = ttk.Entry(self)
        self.video_format_entry.grid(row=1, column=1, padx=5, pady=10, sticky='we')

        # Create the convert button widget
        self.convert_button = ttk.Button(self, text="Convert", command=self.convert_file)
        self.convert_button.grid(row=2, column=1, pady=20, sticky='e')

        # Bind the <Return> event to the convert button
        self.master.bind('<Return>', lambda event: self.convert_file())

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=(("EDL files", "*.edl"),))
        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, filename)

    def convert_file(self):
        def get_sec(time_str):
            """Get Seconds from time."""
            h, m, s = time_str.split(':')
            return int(h) * 3600 + int(m) * 60 + int(s)

        filename = self.filename_entry.get()
        video_format = self.video_format_entry.get()

        filenameSimple, fileExtension = filename.split('.')
        outputFilename = filenameSimple + '.' + video_format

        with open(filename) as f:
            content = f.readlines()

        with open(f'{filenameSimple}.m3u', 'w') as f_out:
            f_out.write('#EXTM3U\n')
            for i, line in enumerate(content):
                start, stop = line.strip().split(' to ')
                f_out.write(f'#EXTINF:{get_sec(stop) - get_sec(start)},{outputFilename}\n')
                f_out.write(f'#EXTVLCOPT:start-time={get_sec(start)}\n')
                f_out.write(f'#EXTVLCOPT:stop-time={get_sec(stop)}\n')
                f_out.write(f'{outputFilename}\n')

root = tk.Tk()
root.title("EDL Converter")

# Set a custom theme for the application
style = ttk.Style()
style.theme_create('custom', parent='alt', settings={
    'TFrame': {
        'configure': {
            'background': '#8639c4'
        }
    },
    'TLabel': {
        'configure': {
            'foreground': '#8639c4'
        }
    },
    'TButton': {
        'configure': {
            'foreground': '#FFC107',
            'background': '#333333'
        }
    },
    'TEntry': {
        'configure': {
            'foreground': '#333333',
            'background': 'white'
        }
    }
})
style.theme_use('custom')

app = Application(master=root)
app.mainloop()

