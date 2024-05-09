import tkinter as tk
from configparser import ConfigParser

from main import generate_voucher  # Import the generate function from main.py
from generate_pdf import generate as generate_pdf_file  # Import the generate function from generate_pdf.py


class ConfigEditorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generate PDF")
        self.geometry("600x620")  # Increased width to accommodate both sections
        self.config_editor = tk.Frame(self)
        self.config_editor.pack(padx=10, pady=10)

        # Load and display only the printing section from config.ini
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.entries = {}

        # Generate Different Section
        self.generate_voucher_section(tk.LEFT)
        self.generate_pdf_section(tk.TOP)

    def generate_voucher_section(self, side):
        voucher_frame = tk.Frame(self.config_editor)
        voucher_frame.pack(side=side, padx=10, pady=10)

        generate_label = tk.Label(voucher_frame, text="Generate Voucher", font=("Arial", 16, "bold"))
        generate_label.pack()
        self.section_to_input_field('voucher_count', voucher_frame, 50)
        self.section_to_input_field('google_drive', voucher_frame, 50)
        self.section_to_input_field('google_spreadsheet', voucher_frame, 50)

        # Button frame
        button_frame = tk.Frame(voucher_frame)
        button_frame.pack(pady=10)

        # Save button
        save_button = tk.Button(button_frame, text="Save", command=self.save_config, bg="#9ACD32")
        save_button.pack(side=tk.LEFT, padx=5)

        # Generate button
        generate_button = tk.Button(button_frame, text="Generate", command=self.generate_voucher, bg="#ADD8E6")
        generate_button.pack(side=tk.LEFT, padx=5)

    def generate_pdf_section(self, side):
        pdf_frame = tk.Frame(self.config_editor)
        pdf_frame.pack(side=side, padx=10, pady=10)

        generate_label = tk.Label(pdf_frame, text="Generate PDF", font=("Arial", 16, "bold"))
        generate_label.pack()
        self.section_to_input_field('printing', pdf_frame)

        # Button frame
        button_frame = tk.Frame(pdf_frame)
        button_frame.pack(pady=10)

        # Save button
        save_button = tk.Button(button_frame, text="Save", command=self.save_config, bg="#9ACD32")
        save_button.pack(side=tk.LEFT, padx=5)

        # Generate button
        generate_button = tk.Button(button_frame, text="Generate", command=self.generate_pdf, bg="#ADD8E6")
        generate_button.pack(side=tk.LEFT, padx=5)

    def section_to_input_field(self, section, frame, width=30):
        tk.Label(frame, text=f"[{section.replace('_', ' ').title()}]", font=("Arial", 11, "bold")).pack(pady=(5, 0))
        for key in self.config.options(section):
            label = tk.Label(frame, text=f"{key.replace('_', ' ').title()}:")
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
                radio_frame = tk.Frame(frame)  # Create a frame for the radio buttons
                radio_frame.pack(anchor=tk.W)  # Pack the frame with respect to the left side

                for text in options:
                    tk.Radiobutton(radio_frame, text=text, variable=entry, value=text).pack(side=tk.LEFT)
            else:
                entry = tk.Entry(frame, width=width)
                entry.insert(0, self.config.get(section, key))
                entry.pack()

            self.entries[(section, key)] = entry

    def save_config(self):
        # Save edited config values back to config.ini
        for (section, option), entry in self.entries.items():
            self.config.set(section, option, entry.get())
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def generate_voucher(self):
        self.save_config()
        generate_voucher()

    def generate_pdf(self):
        self.save_config()
        generate_pdf_file()


if __name__ == "__main__":
    app = ConfigEditorWindow()
    app.mainloop()
