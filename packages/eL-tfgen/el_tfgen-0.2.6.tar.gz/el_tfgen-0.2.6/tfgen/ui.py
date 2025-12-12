import customtkinter as ctk
import asyncio
import threading
import sys
import os
from .terraform_parser import (
    get_module_path,
    generate_module_with_gpt,
    split_and_save_outputs,
    validate_terraform_module,
    create_examples_with_ai
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TerraformGeneratorUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Terraform Module Generator")
        self.geometry("900x700")
        self.resizable(False, False)
        
        self.steps = ["FETCH", "GENERATE", "VALIDATE", "EXAMPLES", "VERIFY"]
        self.current_step = -1
        self.repair_attempts = 0
        self.last_message = ""
        
        self.center_window()
        self.setup_ui()
        sys.stdout = self
    
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 450
        y = (self.winfo_screenheight() // 2) - 350
        self.geometry(f'900x700+{x}+{y}')
    
    def setup_ui(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(frame, text="Terraform Module Generator", font=("Segoe UI", 28, "bold")).pack(pady=(0, 5))
        ctk.CTkLabel(frame, text="AI-Powered Infrastructure as Code", font=("Segoe UI", 12), text_color="gray").pack(pady=(0, 30))
        
        ctk.CTkLabel(frame, text="Resource URL", font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", pady=(0, 8))
        self.url_entry = ctk.CTkEntry(frame, height=45, font=("Segoe UI", 12), placeholder_text="https://registry.terraform.io/providers/...")
        self.url_entry.pack(fill="x", pady=(0, 20))
        
        self.generate_btn = ctk.CTkButton(frame, text="Generate Module", height=45, font=("Segoe UI", 13, "bold"), command=self.start_workflow)
        self.generate_btn.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(frame, text="Progress", font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", pady=(0, 15))
        
        steps_frame = ctk.CTkFrame(frame, fg_color="transparent")
        steps_frame.pack(fill="x", pady=(0, 20))
        
        self.step_labels = []
        self.step_indicators = []
        
        for i, step in enumerate(self.steps):
            container = ctk.CTkFrame(steps_frame, fg_color="transparent")
            container.grid(row=0, column=i, padx=10, sticky="ew")
            steps_frame.grid_columnconfigure(i, weight=1)
            
            ind = ctk.CTkLabel(container, text="", width=12, height=12, corner_radius=6, fg_color="gray30")
            ind.pack()
            self.step_indicators.append(ind)
            
            lbl = ctk.CTkLabel(container, text=step, font=("Segoe UI", 9), text_color="gray")
            lbl.pack(pady=(5, 0))
            self.step_labels.append(lbl)
        
        self.progress_bar = ctk.CTkProgressBar(frame, mode="determinate")
        self.progress_bar.pack(fill="x", pady=(0, 25))
        self.progress_bar.set(0)
        
        ctk.CTkLabel(frame, text="Console", font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", pady=(0, 8))
        
        self.tabview = ctk.CTkTabview(frame, height=250)
        self.tabview.pack(fill="both", expand=True)
        self.tabview.add("Output")
        self.tabview.add("Errors")
        
        self.console = ctk.CTkTextbox(self.tabview.tab("Output"), font=("Consolas", 11), fg_color="gray10", wrap="word")
        self.console.pack(fill="both", expand=True)
        self.console.configure(state="disabled")
        
        self.error_console = ctk.CTkTextbox(self.tabview.tab("Errors"), font=("Consolas", 10), fg_color="gray10", text_color="#f87171", wrap="word")
        self.error_console.pack(fill="both", expand=True)
        self.error_console.configure(state="disabled")
    
    def log(self, msg, level="info", to_errors=False):
        target = self.error_console if to_errors else self.console
        target.configure(state="normal")
        prefix = {"success": "✓ ", "error": "✗ ", "warning": "⚠ "}.get(level, "→ ")
        target.insert("end", f"{prefix}{msg}\n")
        target.see("end")
        target.configure(state="disabled")
    
    def update_step(self, idx, status):
        if idx < 0 or idx >= len(self.steps):
            return
        colors = {"pending": ("gray30", "gray"), "active": ("#3b82f6", "#3b82f6"), "success": ("#4ade80", "#4ade80"), "error": ("#f87171", "#f87171"), "warning": ("#fb923c", "#fb923c")}
        if status in colors:
            self.step_indicators[idx].configure(fg_color=colors[status][0])
            self.step_labels[idx].configure(text_color=colors[status][1])
            if status == "active":
                self.animate_indicator(self.step_indicators[idx])
            else:
                self.stop_animation(self.step_indicators[idx])
    
    def animate_indicator(self, ind):
        def pulse(o=1.0, d=-0.1):
            if not hasattr(ind, '_a'):
                return
            o += d
            if o <= 0.3:
                d, o = 0.1, 0.3
            elif o >= 1.0:
                d, o = -0.1, 1.0
            self.after(50, lambda: pulse(o, d))
        ind._a = True
        pulse()
    
    def stop_animation(self, ind):
        if hasattr(ind, '_a'):
            delattr(ind, '_a')
    
    def write(self, text):
        if not text.strip():
            return
        msg, lower = text.strip(), text.strip().lower()
        
        if "error" in lower or "failed" in lower or "stderr:" in lower or "stdout:" in lower:
            self.log(msg, "error", True)
            return
        
        s = self.simplify_message(msg, lower)
        if s and s != self.last_message:
            lvl = "success" if "success" in lower or "completed" in lower else ("warning" if "repair" in lower or "attempt" in lower else "info")
            self.log(s, lvl)
            self.last_message = s
        
        self.update_progress_from_log(msg)
    
    def simplify_message(self, msg, lower):
        m = {"initializing": "Fetching...", "generating terraform files": "Generating module...", "validating terraform module": "Validating...", "generating usage examples": "Generating example folder...", "generating examples": "Generating example folder...", "workflow completed": "✓ Workflow completed successfully"}
        for k, v in m.items():
            if k in lower:
                return v
        if "repair" in lower or "fix attempt" in lower:
            try:
                import re
                match = re.search(r'attempt[:\s]+(\d+)', lower)
                if match:
                    self.repair_attempts = int(match.group(1))
                    return f"Verifying (attempt {self.repair_attempts}/5)"
            except:
                pass
        return None
    
    def flush(self):
        pass
    
    def update_progress_from_log(self, msg):
        m = msg.lower()
        if "initializing" in m or "fetching" in m:
            self.set_step(0, "active")
        elif "generating terraform files" in m:
            self.set_step(0, "success")
            self.set_step(1, "active")
        elif "terraform files generated" in m:
            self.set_step(1, "success")
        elif "validating terraform module" in m and "examples" not in m:
            self.set_step(2, "active")
        elif "module validation" in m and ("passed" in m or "completed" in m):
            self.set_step(2, "success")
        elif "generating usage examples" in m or "generating examples" in m:
            self.set_step(3, "active")
        elif "examples folder created" in m or "examples generated" in m:
            self.set_step(3, "success")
        elif "validating terraform" in m and "examples" in m:
            self.set_step(4, "active")
        elif "examples validation completed" in m or ("examples" in m and "successful" in m):
            self.set_step(4, "success")
        elif "workflow completed" in m:
            self.set_step(4, "success")
            self.progress_bar.set(1.0)
            self.generate_btn.configure(state="normal", text="Generate Module")
            self.repair_attempts = 0
        elif ("repair" in m or "fix attempt" in m) and self.repair_attempts > 1:
            if self.current_step == 2:
                self.update_step(2, "warning")
            elif self.current_step == 4:
                self.update_step(4, "warning")
    
    def set_step(self, idx, status):
        self.current_step = idx
        self.update_step(idx, status)
        if status == "success":
            self.progress_bar.set((idx + 1) / len(self.steps))
    
    def start_workflow(self):
        url = self.url_entry.get().strip()
        if not url:
            self.log("Please enter a resource URL", "error")
            return
        
        for i in range(len(self.steps)):
            self.update_step(i, "pending")
        self.progress_bar.set(0)
        self.repair_attempts = 0
        self.last_message = ""
        
        for c in [self.console, self.error_console]:
            c.configure(state="normal")
            c.delete("1.0", "end")
            c.configure(state="disabled")
        
        self.generate_btn.configure(state="disabled", text="Generating...")
        threading.Thread(target=self.run_pipeline, args=(url,), daemon=True).start()
    
    def run_pipeline(self, url):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            print(f"Initializing workflow for: {url}")
            module_path = get_module_path(url)
            azapi_mode = url.startswith("https://learn.microsoft.com")
            
            print("Generating Terraform files...")
            gpt_output = loop.run_until_complete(generate_module_with_gpt("", azapi_mode=azapi_mode, url=url))
            if not gpt_output:
                return
            
            split_and_save_outputs(gpt_output, module_path)
            print("Terraform files generated successfully")
            
            print("Validating Terraform Module...")
            val_success, val_error = validate_terraform_module(module_path, context="Module")
            
            if not val_success:
                print("Validation failed. Starting AI repair...")
                for attempt in range(3):
                    print(f"Repair attempt {attempt + 1}...")
                    fixed_output = loop.run_until_complete(generate_module_with_gpt("", azapi_mode=azapi_mode, url=url, error_context=val_error))
                    if fixed_output:
                        split_and_save_outputs(fixed_output, module_path)
                        val_success, val_error = validate_terraform_module(module_path, context="Module")
                        if val_success:
                            print("Module repaired successfully")
                            break
                if not val_success:
                    print("Failed to repair module after 3 attempts")
                    return
            else:
                print("Module validation passed")
            
            print("Generating usage examples...")
            loop.run_until_complete(create_examples_with_ai(module_path, url))
            
            print("Workflow completed successfully")
        except Exception as e:
            print(f"Critical error: {str(e)}")
        finally:
            try:
                loop.close()
            except:
                pass

def main():
    """Entry point for the tfgen-ui command"""
    app = TerraformGeneratorUI()
    app.mainloop()

if __name__ == "__main__":
    main()