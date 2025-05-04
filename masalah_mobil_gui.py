import tkinter as tk
from tkinter import messagebox
from pyswip import Prolog

# Inisialisasi Prolog dan load knowledge base
prolog = Prolog()
prolog.consult("masalah_mobil.pl")

# Ambil semua gejala unik dari basis pengetahuan
symptoms = sorted({s['S'] for s in prolog.query("symptom(_, S)")})

class ExpertSystemGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistem Pakar Troubleshooting Mobil")
        self.index = 0

        # Label pertanyaan
        self.question_label = tk.Label(master, text="", font=("Arial", 14), wraplength=350)
        self.question_label.pack(pady=20)

        # Frame tombol Ya/Tidak
        btn_frame = tk.Frame(master)
        btn_frame.pack()
        self.yes_btn = tk.Button(btn_frame, text="Ya", width=10, state=tk.DISABLED, command=self.yes)
        self.yes_btn.pack(side=tk.LEFT, padx=10)
        self.no_btn = tk.Button(btn_frame, text="Tidak", width=10, state=tk.DISABLED, command=self.no)
        self.no_btn.pack(side=tk.LEFT, padx=10)

        # Tombol Mulai Diagnosa
        self.start_btn = tk.Button(master, text="Mulai Diagnosa", command=self.start)
        self.start_btn.pack(pady=10)

    def start(self):
        # Reset fakta gejala sebelumnya
        prolog.retractall("user_has(_)")
        self.index = 0
        self.start_btn.configure(state=tk.DISABLED)
        self.yes_btn.configure(state=tk.NORMAL)
        self.no_btn.configure(state=tk.NORMAL)
        self.next_question()

    def next_question(self):
        if self.index < len(symptoms):
            sym = symptoms[self.index]
            # Membuat pertanyaan berdasarkan nama gejala
            pertanyaan = f"Apakah mobil Anda mengalami '{sym.replace('_', ' ')}'?"
            self.question_label.config(text=pertanyaan)
        else:
            self.show_result()

    def yes(self):
        sym = symptoms[self.index]
        prolog.assertz(f"user_has({sym})")
        self.index += 1
        self.next_question()

    def no(self):
        self.index += 1
        self.next_question()

    def show_result(self):
        results = [r['Problem'] for r in prolog.query("diagnose(Problem)")]
        if results:
            # Format hasil dalam bahasa Indonesia
            problems = [p.replace('_', ' ') for p in results]
            msg = "Kemungkinan masalah: " + ", ".join(problems)
        else:
            msg = "Maaf, sistem tidak dapat menentukan masalah berdasarkan gejala."
        messagebox.showinfo("Hasil Diagnosa", msg)

        # Reset tombol dan label
        self.start_btn.configure(state=tk.NORMAL)
        self.yes_btn.configure(state=tk.DISABLED)
        self.no_btn.configure(state=tk.DISABLED)
        self.question_label.config(text="")

if __name__ == '__main__':
    root = tk.Tk()
    app = ExpertSystemGUI(root)
    root.mainloop()