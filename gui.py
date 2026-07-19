import os
import time
import threading
import webbrowser
import customtkinter as ctk
from tkinter import filedialog
from locales import LOCALIZATION
from core import run_audit

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ZipAuditorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_lang = "Русский"
        self.txt = LOCALIZATION[self.current_lang]
        self.log_history = []

        self.title("ZIP-Auditor")
        self.geometry("580x560")
        self.resizable(False, False)

        self.is_running = False
        self.is_deep_mode = False
        self.stop_event = threading.Event()
        self.found_password = None
        self.selected_zip_path = ""
        self.no_password_flag = False

        # --- Шапка ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(10, 0), padx=15, fill="x")
        self.lbl_title = ctk.CTkLabel(self.header_frame, text="🛡️ ZIP-Auditor", font=("Arial", 18, "bold"))
        self.lbl_title.pack(side="left", padx=5)
        self.lang_switch = ctk.CTkOptionMenu(self.header_frame, values=["Русский", "English"], width=100, command=self.change_language)
        self.lang_switch.pack(side="right", padx=5)
        self.lang_switch.set("Русский")

        # --- Вкладки ---
        self.tab_view = ctk.CTkTabview(self, width=560, height=480)
        self.tab_view.pack(pady=(5, 10), padx=10, fill="both", expand=True)
        self.tab_view.add("tab1")
        self.tab_view.add("tab2")
        self.tab_audit = self.tab_view.tab("tab1")
        self.tab_about = self.tab_view.tab("tab2")

        # --- Вкладка "Аудит" ---
        self.file_frame = ctk.CTkFrame(self.tab_audit)
        self.file_frame.pack(pady=10, padx=15, fill="x")
        self.lbl_file = ctk.CTkLabel(self.file_frame, text=self.txt["file_lbl"], font=("Arial", 12, "bold"))
        self.lbl_file.pack(anchor="w", padx=15, pady=(10, 2))
        self.entry_file_path = ctk.CTkEntry(self.file_frame, placeholder_text=self.txt["placeholder"], width=320, font=("Courier New", 11))
        self.entry_file_path.pack(side="left", padx=(15, 10), pady=(0, 15))
        self.entry_file_path.configure(state="disabled")
        self.btn_browse = ctk.CTkButton(self.file_frame, text=self.txt["browse_btn"], width=110, command=self.browse_file)
        self.btn_browse.pack(side="right", padx=(0, 15), pady=(0, 15))

        self.lbl_status = ctk.CTkLabel(self.tab_audit, text=self.txt["status_wait"], font=("Arial", 13, "bold"), text_color="#3498db")
        self.lbl_status.pack(pady=5)

        self.btn_action = ctk.CTkButton(self.tab_audit, text=self.txt["btn_start"], font=("Arial", 14, "bold"), height=42, command=self.toggle_brute)
        self.btn_action.pack(pady=5)

        self.txt_log = ctk.CTkTextbox(
            self.tab_audit, width=510, height=180,
            font=("Segoe UI", 13), text_color="#E0E0E0", fg_color="#1E1E1E"
        )
        self.txt_log.pack(pady=15, padx=15)
        self.txt_log.configure(state="disabled")

        # --- Вкладка "О программе" ---
        self.info_frame = ctk.CTkFrame(self.tab_about)
        self.info_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.lbl_desc = ctk.CTkLabel(
            self.info_frame, text=self.txt["desc"],
            font=("Segoe UI", 13),
            justify="left", anchor="nw", wraplength=500,
            text_color="#E0E0E0"
        )
        self.lbl_desc.pack(padx=15, pady=(15, 5), fill="x")

        self.link_label = ctk.CTkLabel(
            self.info_frame, text=self.txt["github_link"],
            font=("Segoe UI", 13, "underline"),
            text_color="#1f6aa5", cursor="hand2"
        )
        self.link_label.pack(padx=15, pady=(0, 15), anchor="w")
        self.link_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/KIziName/ZIP-Auditor/releases"))

        self.update_ui_texts()
        self.log("log_init", force_scroll=True)

    def change_language(self, choice):
        scroll_pos = self.txt_log.yview()[0] if self.txt_log.yview() else 0.0
        self.current_lang = choice
        self.txt = LOCALIZATION[self.current_lang]
        self.update_ui_texts()
        self.rebuild_translated_log()
        self.txt_log.yview_moveto(scroll_pos)

    def update_ui_texts(self):
        self.tab_view._segmented_button._value_list = [self.txt["tab_audit"], self.txt["tab_about"]]
        self.tab_view._segmented_button._buttons_dict["tab1"].configure(text=self.txt["tab_audit"])
        self.tab_view._segmented_button._buttons_dict["tab2"].configure(text=self.txt["tab_about"])
        self.lbl_file.configure(text=self.txt["file_lbl"])
        self.btn_browse.configure(text=self.txt["browse_btn"])
        self.lbl_desc.configure(text=self.txt["desc"])
        self.link_label.configure(text=self.txt["github_link"])
        if not self.selected_zip_path:
            self.entry_file_path.configure(placeholder_text=self.txt["placeholder"])

        if self.is_running:
            if self.stop_event.is_set():
                self.lbl_status.configure(text=self.txt["status_cancel"], text_color="#e74c3c")
            elif self.is_deep_mode:
                self.lbl_status.configure(text=self.txt["status_deep"], text_color="#f39c12")
            else:
                self.lbl_status.configure(text=self.txt["status_run"], text_color="#9b59b6")
            self.btn_action.configure(text=self.txt["btn_stop"])
        else:
            self.btn_action.configure(text=self.txt["btn_start"])
            if not self.selected_zip_path:
                self.lbl_status.configure(text=self.txt["status_wait"], text_color="#3498db")
            elif self.no_password_flag:
                self.lbl_status.configure(text=self.txt["status_no_password"], text_color="#3498db")
            else:
                self.lbl_status.configure(text=self.txt["status_ready"], text_color="#2ecc71")

    def clear_log(self):
        self.log_history.clear()
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.configure(state="disabled")

    def log(self, key, *args, force_scroll=False):
        if self.stop_event.is_set() and key in ("log_mil_step", "log_len_step", "log_express", "log_deep_start"):
            return

        timestamp = time.strftime("%H:%M:%S")
        self.log_history.append((timestamp, key, args))
        self.txt_log.configure(state="normal")
        was_at_end = self.txt_log.yview()[1] == 1.0
        translated_str = self.format_log_line(timestamp, key, args)
        self.txt_log.insert("end", translated_str + "\n")
        if force_scroll or was_at_end:
            self.txt_log.see("end")
        self.txt_log.configure(state="disabled")

    def format_log_line(self, timestamp, key, args):
        raw_text = self.txt.get(key, key)
        if args:
            try:
                if key == "log_mil_step":
                    count = args[0]
                    if count >= 1_000_000:
                        unit = self.txt["million"]
                        formatted_count = f"{count/1_000_000:.1f}"
                    else:
                        unit = self.txt["thousand"]
                        formatted_count = f"{count//1000}"
                    return f"[{timestamp}] {raw_text.format(formatted_count, unit)}"
                else:
                    return f"[{timestamp}] {raw_text.format(*args)}"
            except Exception:
                pass
        return f"[{timestamp}] {raw_text}"

    def rebuild_translated_log(self):
        self.txt_log.configure(state="normal")
        self.txt_log.delete("1.0", "end")
        for timestamp, key, args in self.log_history:
            self.txt_log.insert("end", self.format_log_line(timestamp, key, args) + "\n")
        self.txt_log.configure(state="disabled")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите ZIP-архив" if self.current_lang == "Русский" else "Select ZIP Archive",
            filetypes=[("ZIP Архивы", "*.zip"), ("Все файлы", "*.*")]
        )
        if file_path:
            self.selected_zip_path = file_path
            self.no_password_flag = False
            self.entry_file_path.configure(state="normal")
            self.entry_file_path.delete(0, "end")
            self.entry_file_path.insert(0, os.path.basename(file_path))
            self.entry_file_path.configure(state="disabled")
            self.lbl_status.configure(text=self.txt["status_ready"], text_color="#2ecc71")

    def toggle_brute(self):
        if self.is_running:
            self.stop_event.set()
            self.lbl_status.configure(text=self.txt["status_cancel"], text_color="#e74c3c")
            self.btn_action.configure(state="disabled")
            self.btn_browse.configure(state="normal")
            self.log("log_stopped", force_scroll=True)
            return

        if not self.selected_zip_path or not os.path.exists(self.selected_zip_path):
            self.log("log_error_select", force_scroll=True)
            return

        self.is_running = True
        self.is_deep_mode = False
        self.no_password_flag = False
        self.stop_event.clear()
        self.found_password = None

        self.clear_log()
        self.log("log_init", force_scroll=True)
        self.log("log_divider", force_scroll=True)

        self.btn_browse.configure(state="disabled")
        self.btn_action.configure(text=self.txt["btn_stop"], fg_color="#e74c3c", hover_color="#c0392b")
        self.lbl_status.configure(text=self.txt["status_run"], text_color="#9b59b6")

        # Передача коллбэков в поток логики для соблюдения потокобезопасности Tkinter
        threading.Thread(
            target=run_audit, 
            args=(
                self.selected_zip_path, 
                7, 
                self.stop_event, 
                lambda k, *a, fs=False: self.after(0, self.log, k, *a, fs),
                lambda: self.after(0, self.set_deep_status),
                lambda elapsed, pwd, no_pwd: self.after(0, self.brute_finished, elapsed, pwd, no_pwd)
            ), 
            daemon=True
        ).start()

    def set_deep_status(self):
        if not self.stop_event.is_set():
            self.is_deep_mode = True
            self.lbl_status.configure(text=self.txt["status_deep"], text_color="#f39c12")

    def brute_finished(self, elapsed, found_password, no_password_flag):
        self.is_running = False
        self.is_deep_mode = False
        self.found_password = found_password
        self.no_password_flag = no_password_flag

        self.btn_browse.configure(state="normal")
        self.btn_action.configure(state="normal")
        self.btn_action.configure(text=self.txt["btn_start"], fg_color="#1f538d", hover_color="#14375e")

        if self.found_password:
            self.lbl_status.configure(text=self.txt["status_success"], text_color="#2ecc71")
            self.log("log_found", self.found_password, force_scroll=True)
        elif self.no_password_flag:
            self.lbl_status.configure(text=self.txt["status_no_password"], text_color="#3498db")
        elif self.stop_event.is_set():
            self.lbl_status.configure(text=self.txt["status_cancel"], text_color="#e74c3c")
        else:
            self.lbl_status.configure(text=self.txt["status_fail"], text_color="#95a5a6")
            self.log("log_not_found", force_scroll=True)
            
        self.log("log_session_time", elapsed, force_scroll=True)
        self.update_idletasks()
