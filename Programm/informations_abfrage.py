import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle
import os
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CSVQueryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Abfrage")
        self.attributes("-fullscreen", True)
        self.geometry("800x500")

        self.filename = None
        self.csv_data = None
        self.available_columns = []
        self.wedges = None
        self.labels = None

        self.style = ThemedStyle(self)
        self.style.theme_use('xpnative')

        self.create_widgets()

    def create_widgets(self):
        # Beenden- und Minimieren-Symbole
        current_script_path = os.path.realpath(__file__)
        icon_path = os.path.join(current_script_path, '/icon.png')
        minimize_path = os.path.join(current_script_path, "/minimize.png")
        self.icon_img = tk.PhotoImage(file="C:/Johannes_Braun/Logs Analyse/Programm/icons/icon.png")        
        self.minimize_img = tk.PhotoImage(file="C:/Johannes_Braun/Logs Analyse/Programm/icons/minimize.png")
        self.close_img = tk.PhotoImage(file="C:/Johannes_Braun/Logs Analyse/Programm/icons/close.png")
        self.title("CSV Abfrage")
        self.iconphoto(True, self.icon_img)

        # Minimieren- und Beenden-Schaltflächen hinzufügen
        self.minimize_button = ttk.Button(self, image=self.minimize_img, command=self.minimize_window, style="IconButton.TButton")
        self.minimize_button.place(x=self.winfo_screenwidth() - 80, y=5)
        self.close_button = ttk.Button(self, image=self.close_img, command=self.quit, style="IconButton.TButton")
        self.close_button.place(x=self.winfo_screenwidth() - 40, y=5)
        self.load_button = ttk.Button(self, text="CSV-Datei laden", command=self.load_csv_file)
        self.load_button.pack(pady=10)

        self.csv_filename_label = ttk.Label(self, text="")
        self.csv_filename_label.pack(pady=5)

        self.query_frame = ttk.LabelFrame(self, text="Abfrageoptionen")
        self.query_frame.pack(pady=10)

        self.column_label = ttk.Label(self.query_frame, text="Welche Spalte möchtest du abfragen?")
        self.column_label.grid(row=0, column=0, padx=10, pady=5)

        self.column_choice = ttk.Combobox(self.query_frame, values=self.available_columns, state="readonly")
        self.column_choice.grid(row=0, column=1, padx=10, pady=5)

        self.num_entries_label = ttk.Label(self.query_frame, text="Wie viele Einträge möchtest du abfragen?")
        self.num_entries_label.grid(row=1, column=0, padx=10, pady=5)

        self.num_entries_entry = ttk.Entry(self.query_frame)
        self.num_entries_entry.grid(row=1, column=1, padx=10, pady=5)

        self.record_index_label = ttk.Label(self.query_frame, text="Möchtest du einen bestimmten Datensatz abfragen? Gib den Index ein (1-x)")
        self.record_index_label.grid(row=2, column=0, padx=10, pady=5)

        self.record_index_entry = ttk.Entry(self.query_frame)
        self.record_index_entry.grid(row=2, column=1, padx=10, pady=5)

        self.search_text_label = ttk.Label(self.query_frame, text="Möchtest du nach einer bestimmten Zeichenfolge suchen?")
        self.search_text_label.grid(row=3, column=0, padx=10, pady=5)

        self.search_text_entry = ttk.Entry(self.query_frame)
        self.search_text_entry.grid(row=3, column=1, padx=10, pady=5)

        self.sort_order_label = ttk.Label(self.query_frame, text="Möchtest du die Ergebnisse aufsteigend oder absteigend sortieren?")
        self.sort_order_label.grid(row=4, column=0, padx=10, pady=5)

        self.sort_order_choice = ttk.Combobox(self.query_frame, values=["", "aufsteigend", "absteigend"], state="readonly")
        self.sort_order_choice.grid(row=4, column=1, padx=10, pady=5)

        self.run_query_button = ttk.Button(self, text="Abfrage durchführen", command=self.run_query)
        self.run_query_button.pack(pady=10)

        self.output_text = tk.Text(self, wrap=tk.WORD)
        self.output_text.pack(padx=10, pady=5)

        self.save_button = ttk.Button(self, text="Ergebnisse speichern", command=self.save_results)
        self.save_button.pack(pady=10)

        self.repeat_button = ttk.Button(self, text="Erneut abfragen", command=self.repeat_query)
        self.repeat_button.pack(pady=10)

    def load_csv_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("CSV Dateien", "*.csv")])
        if self.filename:
            self.csv_data = self.get_csv_data(self.filename)
            self.available_columns = list(self.csv_data.keys())
            self.column_choice["values"] = self.available_columns
            self.column_choice.set("")
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "CSV-Datei erfolgreich geladen.\n")
            self.csv_filename_label.config(text=f"CSV-Datei: {self.filename}")

    def get_csv_data(self, filename):
        csv_data = {}
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for key, value in row.items():
                    if key not in csv_data:
                        csv_data[key] = []
                    csv_data[key].append(value)
        return csv_data

    def run_query(self):
        if not self.csv_data:
            messagebox.showerror("Fehler", "Bitte laden Sie zuerst eine CSV-Datei.")
            return

        column_name = self.column_choice.get()
        num_entries = self.num_entries_entry.get()
        record_index = self.record_index_entry.get()
        search_text = self.search_text_entry.get()
        sort_order = self.sort_order_choice.get()

        try:
            num_entries = int(num_entries) if num_entries.isdigit() else None
            record_index = int(record_index) if record_index.isdigit() else None
        except ValueError:
            messagebox.showerror("Fehler", "Ungültige Eingabe für Anzahl der Einträge oder Datensatzindex.")
            return

        column_data = self.read_csv_column(self.csv_data, column_name, num_entries, record_index, search_text, sort_order)

        if column_data is not None:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Anzahl der Vorkommen in der 'RowKey'-Spalte:\n{self.get_rowkey_counts()}\n\n")
            self.output_text.insert(tk.END, f"Abfrageergebnisse für Spalte '{column_name}':\n")

            # Add numbering to each entry in column_data
            for idx, entry in enumerate(column_data, 1):
                self.output_text.insert(tk.END, f"{idx}. {entry}\n")

            if column_name == 'RowKey':
                self.analyze_rowkey_column()

    def get_rowkey_counts(self):
        if 'RowKey' not in self.csv_data:
            return "Die 'RowKey'-Spalte ist nicht in der CSV-Datei vorhanden."

        rowkey_column_data = self.csv_data['RowKey']
        rowkey_counts = Counter([entry.split('|')[0] for entry in rowkey_column_data])

        result = []
        for key in ["ERROR", "EXCEPTION", "WARNING"]:
            count = rowkey_counts.get(key, 0)
            result.append(f"{key}: {count}")

        return "\n".join(result)

    def read_csv_column(self, csv_data, column_name, num_entries=None, record_index=None, search_text=None, sort_order=None):
        if column_name not in csv_data:
            return None
        
        column_data = csv_data[column_name]

        if record_index is not None:
            if 1 <= record_index <= len(column_data):
                column_data = [column_data[record_index - 1]]
            else:
                messagebox.showerror("Fehler", f"Ungültiger Datensatzindex. Es gibt insgesamt {len(column_data)} Einträge.")
                return None

        if search_text:
            column_data = [entry for entry in column_data if search_text in entry]

        if sort_order:
            column_data.sort(reverse=sort_order == 'absteigend')
            
        if search_text:
            column_data = [entry for entry in column_data if search_text in entry]

        # After filtering for search_text, remove duplicate entries based on the first 30 characters.
        column_data = self.get_unique_entries_based_on_first_characters(column_data, 30)

        if sort_order:
            column_data.sort(reverse=sort_order == 'absteigend')

        return column_data[:num_entries]
    
    def analyze_rowkey_column(self):
        rowkey_column_data = self.csv_data['RowKey']
        rowkey_counts = Counter([entry.split('|')[0] for entry in rowkey_column_data])

        filtered_counts = {
            'WARNING': rowkey_counts.get('WARNING', 0),
            'ERROR': rowkey_counts.get('ERROR', 0),
            'EXCEPTION': rowkey_counts.get('EXCEPTION', 0)
        }

        self.create_chart(filtered_counts)
        
    def create_chart(self, data_counts):
        self.labels = list(data_counts.keys())
        values = data_counts.values()

        color_map = {
            'WARNING': 'orange',
            'ERROR': 'red',
            'EXCEPTION': 'purple'
        }
        colors = [color_map[label] for label in self.labels]

        fig, ax = plt.subplots(figsize=(8, 8))
        self.wedges, texts, autotexts = ax.pie(values, labels=self.labels, colors=colors, autopct='%1.1f%%', textprops={'color': 'w'})

        plt.title("Verteilung der 'RowKey'-Werte")
        plt.axis('equal')
        plt.tight_layout()

        plt.legend(self.labels, title="Labels", loc="best")

        # Enable the pick event on pie wedges
        for wedge in self.wedges:
            wedge.set_picker(True)

        chart_window = tk.Toplevel(self)
        chart_window.title("Kreisdiagramm")
        chart_canvas = FigureCanvasTkAgg(fig, master=chart_window)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack()
        chart_canvas.mpl_connect('pick_event', self.on_pick)

        save_button = ttk.Button(chart_window, text="Diagramm speichern", command=lambda: self.save_chart(chart_window))
        save_button.pack(pady=10)

    def on_pick(self, event):
        wedge = event.artist
        index = self.wedges.index(wedge)
        label = self.labels[index]
        self.open_detail_window(label)

    def open_detail_window(self, label):
        detail_window = tk.Toplevel(self)
        detail_window.title(f"Details for {label}")
        listbox = tk.Listbox(detail_window)
        listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Filter content based on the selected label (RowKey type)
        content_set = set()
        for index in range(len(self.csv_data["RowKey"])):
            if self.csv_data["RowKey"][index].split('|')[0] == label:
                content_set.add(self.csv_data["Content"][index])

        for content_entry in content_set:
            listbox.insert(tk.END, content_entry)
            
    def get_unique_entries_based_on_first_characters(self, entries, num_characters=30):
        seen = set()
        unique_entries = []
        for entry in entries:
            # Slice the string to the first num_characters
            sliced_entry = entry[:num_characters]
            if sliced_entry not in seen:
                seen.add(sliced_entry)
                unique_entries.append(entry)
        return unique_entries

    
    def save_chart(self, chart_window):
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG-Dateien", "*.png")])
        if filename:
            plt.savefig(filename)
            messagebox.showinfo("Erfolg", f"Diagramm erfolgreich in '{filename}' gespeichert.")
        chart_window.destroy()

    def save_results(self):
        if not self.csv_data:
            messagebox.showerror("Fehler", "Es wurden noch keine Abfragen durchgeführt oder CSV-Datei nicht geladen.")
            return

        results = self.output_text.get(1.0, tk.END)
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Textdateien", "*.txt")])
        if filename:
            with open(filename, "w") as outfile:
                outfile.write(results)
            messagebox.showinfo("Erfolg", f"Ergebnisse erfolgreich in '{filename}' gespeichert.")

    def repeat_query(self):
        self.column_choice.set("")
        self.num_entries_entry.delete(0, tk.END)
        self.record_index_entry.delete(0, tk.END)
        self.search_text_entry.delete(0, tk.END)
        self.sort_order_choice.set("")
        self.output_text.delete(1.0, tk.END)

    def minimize_window(self):
        self.attributes("-fullscreen", False)
        self.iconify()

if __name__ == "__main__":
    app = CSVQueryApp()
    app.mainloop()
    
