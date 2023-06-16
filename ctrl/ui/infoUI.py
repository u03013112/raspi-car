import tkinter as tk

class InfoUI:
    def __init__(self, left_frame):
        self.info_frame = tk.Frame(left_frame, bg="yellow", bd=1, relief="solid")

        left_frame.update_idletasks()
        left_frame_width = left_frame.winfo_width() - 10

        self.info_frame.place(relx=0.5, y=190, anchor="n", width=left_frame_width)

        title_label = tk.Label(self.info_frame, text="树莓派遥控车信息", font=("Arial", 14, "bold"), anchor="w")
        title_label.pack(pady=(10, 5), padx=(10, 0), anchor="w")

        self.info_text = tk.Text(self.info_frame, wrap="word", height=10, width=40)
        self.info_text.pack(padx=(10, 0), pady=(5, 10), anchor="w")

    def update_info(self, info):
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)
