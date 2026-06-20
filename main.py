import customtkinter as ctk
from customtkinter import filedialog
import threading
import asyncio
from core.username_checker import UsernameScanner
from core.report_generator import generate_pdf_report

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SentinelTraceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sentinel-Trace | Digital Footprint Auditor")
        self.geometry("900x650")
        self.minsize(850, 550)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Variables to hold data for exporting ---
        self.current_target = ""
        self.current_results = []
        self.current_score = 0

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Sentinel-Trace", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_scan = ctk.CTkButton(self.sidebar_frame, text="New Scan", fg_color="#3B8ED0")
        self.btn_scan.grid(row=1, column=0, padx=20, pady=10)

        # Export Button (Disabled by default until a scan is finished)
        self.btn_export = ctk.CTkButton(self.sidebar_frame, text="Export PDF Report", state="disabled", command=self.export_report)
        self.btn_export.grid(row=2, column=0, padx=20, pady=10)

        # --- Main Content Area ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(3, weight=1) 
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.input_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter target username (e.g., admin)", width=350, height=40, font=ctk.CTkFont(size=14))
        self.input_entry.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.start_btn = ctk.CTkButton(self.main_frame, text="Start Audit", command=self.start_scan, height=40, font=ctk.CTkFont(size=14, weight="bold"))
        self.start_btn.grid(row=0, column=0, padx=(390, 20), pady=(20, 10), sticky="w")

        self.status_label = ctk.CTkLabel(self.main_frame, text="Ready for audit.", text_color="gray", font=ctk.CTkFont(size=14))
        self.status_label.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        self.score_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.score_frame.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        self.score_label = ctk.CTkLabel(self.score_frame, text="Privacy Health: --%", font=ctk.CTkFont(size=16, weight="bold"))
        self.score_label.pack(side="left", padx=(0, 15))
        
        self.score_bar = ctk.CTkProgressBar(self.score_frame, height=12)
        self.score_bar.set(0) 
        self.score_bar.pack(side="left", fill="x", expand=True)

        self.results_box = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(family="Consolas", size=13), corner_radius=8)
        self.results_box.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")

        self.scanner = UsernameScanner()

    def start_scan(self):
        self.current_target = self.input_entry.get().strip()
        
        if not self.current_target:
            self.status_label.configure(text="Error: Please enter a username.", text_color="#E63946") 
            return

        # Lock UI
        self.start_btn.configure(state="disabled")
        self.btn_export.configure(state="disabled")
        self.status_label.configure(text=f"Auditing digital footprint for '{self.current_target}'...", text_color="#E59500") 
        self.score_label.configure(text="Privacy Health: Calculating...", text_color="gray")
        self.score_bar.set(0)
        self.score_bar.configure(progress_color="gray")
        
        self.results_box.delete("1.0", "end")
        self.results_box.insert("end", "[*] Initializing asynchronous OSINT scan...\n[*] Polling target databases...\n")

        threading.Thread(target=self.run_async_scan, args=(self.current_target,), daemon=True).start()

    def run_async_scan(self, username):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(self.scanner.scan(username))
        loop.close()
        self.after(0, self.display_results, results)

    def display_results(self, results):
        self.current_results = results
        self.start_btn.configure(state="normal")
        self.btn_export.configure(state="normal") # Enable export button
        self.results_box.delete("1.0", "end")
        
        num_found = len(results)
        
        if num_found == 0:
            self.current_score = 100
            color = "#2FA572" 
            status = "Audit complete. Excellent privacy posture."
        elif num_found <= 2:
            self.current_score = 75
            color = "#E59500" 
            status = f"Audit complete. Minor footprint detected ({num_found} exposures)."
        else:
            self.current_score = max(15, 100 - (num_found * 15)) 
            color = "#E63946" 
            status = f"Audit complete. Significant exposure detected ({num_found} exposures)."

        self.status_label.configure(text=status, text_color=color)
        self.score_label.configure(text=f"Privacy Health: {self.current_score}%", text_color=color)
        self.score_bar.configure(progress_color=color)
        self.score_bar.set(self.current_score / 100.0)

        if num_found == 0:
            self.results_box.insert("end", "\n[+] No linked accounts discovered on monitored platforms.\n")
        else:
            self.results_box.insert("end", "\n[!] COMPROMISED SURFACE AREA:\n")
            self.results_box.insert("end", "="*60 + "\n\n")
            for account in results:
                platform = account['site'].ljust(12)
                self.results_box.insert("end", f"  [>] {platform} : {account['url']}\n")
            self.results_box.insert("end", "\n" + "="*60 + "\n")
            self.results_box.insert("end", "ACTION REQUIRED: Consider reviewing the visibility of these profiles.\n")

    def export_report(self):
        """Opens a directory dialog and saves the PDF."""
        # Open the system's native "Save As" dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"Sentinel_Report_{self.current_target}.pdf",
            title="Save Intelligence Report",
            filetypes=[("PDF Documents", "*.pdf"), ("All Files", "*.*")]
        )
        
        # If the user selected a path (didn't click cancel)
        if file_path:
            try:
                generate_pdf_report(
                    save_path=file_path, 
                    target_username=self.current_target, 
                    score=self.current_score, 
                    results=self.current_results
                )
                self.status_label.configure(text=f"Success: Report saved to {file_path}", text_color="#2FA572")
            except Exception as e:
                self.status_label.configure(text=f"Error saving PDF: {e}", text_color="#E63946")

if __name__ == "__main__":
    app = SentinelTraceApp()
    app.mainloop()
