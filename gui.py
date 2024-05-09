import tkinter as tk
from configparser import ConfigParser

from generate_pdf import generate  # Import the generate function from generate_pdf.py


class ConfigEditorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generate PDF")
        self.geometry("300x400")
        self.config_editor = tk.Frame(self)
        self.config_editor.pack(padx=10, pady=10)

        # Load and display only the printing section from config.ini
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.entries = {}
        section = 'printing'
        for key in self.config.options(section):
            label = tk.Label(self.config_editor, text=f"{key.replace('_', ' ').title()}:")
            label.pack(anchor="w")

            mode = 'text'
            options = []
            if key == 'pdf_orientation':
                mode = 'radio'
                options = ['portrait', 'landscape']
            elif key == 'pdf_page_size':
                mode = 'radio'
                options = ['A3', 'A4']

            if mode == 'radio':
                entry = tk.StringVar(value=self.config.get(section, key))
                radio_frame = tk.Frame(self.config_editor)  # Create a frame for the radio buttons
                radio_frame.pack(anchor=tk.W)  # Pack the frame with respect to the left side

                for text in options:
                    tk.Radiobutton(radio_frame, text=text, variable=entry, value=text).pack(side=tk.LEFT)
            else:
                entry = tk.Entry(self.config_editor, width=30)
                entry.insert(0, self.config.get(section, key))
                entry.pack()

            self.entries[(section, key)] = entry

        # Generate button
        generate_button = tk.Button(self, text="Generate", command=self.generate_and_save_config, bg="#ADD8E6")
        generate_button.pack(side=tk.BOTTOM, pady=10)

        # Save button
        save_button = tk.Button(self, text="Save", command=self.save_config, bg="#9ACD32")
        save_button.pack(side=tk.BOTTOM)

    def save_config(self):
        # Save edited config values back to config.ini
        for (section, option), entry in self.entries.items():
            self.config.set(section, option, entry.get())
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def generate_and_save_config(self):
        self.save_config()
        generate()


if __name__ == "__main__":
    app = ConfigEditorWindow()
    app.mainloop()
