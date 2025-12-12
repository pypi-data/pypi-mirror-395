import tkinter as tk
import time
import threading
import webbrowser
import os
import requests  # For your API
import sys

class AnshikaResumeExperience:
    def __init__(self):
        self.root = tk.Tk()
        
        # --- CONFIGURATION ---
        self.resume_filename = "resume.pdf"
        self.bg_color = "#000000" 
        self.text_color = "#FFFFFF"
        
        # REPLACE THIS WITH YOUR JSON BIN URL (e.g., from npoint.io)
        self.api_url = "https://api.npoint.io/YOUR_ID_HERE" 
        
        # Fullscreen setup
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=self.bg_color)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        # Center Label
        self.label = tk.Label(
            self.root, text="", font=("Segoe UI Light", 28), 
            bg=self.bg_color, fg=self.bg_color
        )
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        # Default Messages (Fallback if API fails)
        self.messages = [
            "Building Up Resume for an Angel Without Wings...",
            "Loading Modules: Montserrat, Open Sans...",
            "Applying Theme: Premium Black & Grey...",
            "Deleting boring templates...",
            "Then why make it ugly like Ansh?", 
            "Beautifying the resume with the charm of Anshika...",
            "Cooking the 2nd most beautiful thing...",
            "(Since the first one is Anshika, of course)",
            "The Resume of Miss Enchanted Weaver of Dreams is Ready."
        ]

        # Fetch API Data before starting
        self.fetch_live_data()

        # Start Animation
        threading.Thread(target=self.play_sequence).start()
        self.root.mainloop()

    def fetch_live_data(self):
        """Tries to get new messages from your API"""
        try:
            # Expects JSON: {"messages": ["Line 1", "Line 2", ...]}
            r = requests.get(self.api_url, timeout=2)
            if r.status_code == 200:
                data = r.json()
                if "messages" in data:
                    self.messages = data["messages"]
        except:
            pass # Fail silently and use default messages

    def fade_in_text(self, text):
        self.label.config(text=text)
        steps = ["#111111", "#333333", "#555555", "#777777", "#999999", "#BBBBBB", "#DDDDDD", "#FFFFFF"]
        for color in steps:
            self.label.config(fg=color)
            time.sleep(0.04)
            self.root.update()

    def fade_out_text(self):
        steps = ["#DDDDDD", "#BBBBBB", "#999999", "#777777", "#555555", "#333333", "#111111", "#000000"]
        for color in steps:
            self.label.config(fg=color)
            time.sleep(0.04)
            self.root.update()

    def play_sequence(self):
        time.sleep(1)
        for msg in self.messages:
            self.fade_in_text(msg)
            hold_time = 3.5 if len(msg) > 30 else 2.5
            time.sleep(hold_time)
            self.fade_out_text()
            time.sleep(0.5)
        self.root.after(0, self.show_final_button)

    def show_final_button(self):
        self.label.config(text="")
        self.btn = tk.Button(
            self.root, text="View Resume", font=("Segoe UI Light", 18),
            bg="black", fg="white", activebackground="white", activeforeground="black",
            relief="flat", borderwidth=1, padx=30, pady=10, cursor="hand2",
            command=self.start_outro
        )
        self.btn.place(relx=0.5, rely=0.5, anchor="center")
        
        # Hover Logic
        def on_enter(e): self.btn.config(bg="#1a1a1a")
        def on_leave(e): self.btn.config(bg="black")
        self.btn.bind("<Enter>", on_enter)
        self.btn.bind("<Leave>", on_leave)

    def start_outro(self):
        self.btn.config(text="Opening...", state="disabled", cursor="watch")
        self.root.update()
        time.sleep(0.8)
        self.btn.place_forget()
        
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.fade_in_text("Have a nice day, Angel.")
        time.sleep(1)
        self.fade_out_text()

        # SMART PATH FINDER (Works in pip packages)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, self.resume_filename)
        
        if os.path.exists(file_path):
            webbrowser.open_new(r'file:///' + file_path)
        else:
            print(f"Error: Could not find {file_path}")
        
        time.sleep(0.5)
        self.root.destroy()

def start():
    AnshikaResumeExperience()