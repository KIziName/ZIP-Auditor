import sys
import os
import time
import string
import itertools
import threading
import ctypes
import webbrowser
import pyzipper as zipfile
import customtkinter as ctk
from tkinter import filedialog

# === МЬЮТЕКС ===
MUTEX_NAME = "Global\\ZIP_Auditor_V1.0_2026"
kernel32 = ctypes.windll.kernel32
if kernel32.CreateMutexW(None, False, MUTEX_NAME) is None or kernel32.GetLastError() == 183:
    ctypes.windll.user32.MessageBoxW(0, "Приложение уже запущено!\nРазрешена только одна копия.", "Ошибка", 0x10)
    sys.exit(0)

# === ЛОКАЛИЗАЦИЯ ===
LOCALIZATION = {
    "Русский": {
        "tab_audit": "Аудит",
        "tab_about": "О программе",
        "file_lbl": "Файл архива:",
        "placeholder": "Файл не выбран...",
        "browse_btn": "📁 Обзор...",
        "status_wait": "Статус: Ожидание файла",
        "status_ready": "Статус: Файл готов к аудиту",
        "status_run": "Статус: Выполнение аудита...",
        "status_deep": "Статус: Глубокий перебор...",
        "status_success": "Статус: Доступ восстановлен!",
        "status_cancel": "Статус: Процесс прерван",
        "status_fail": "Статус: Пароль не найден",
        "btn_start": "⚡ Запустить аудит [Лимит: 7 знаков]",
        "btn_stop": "🛑 Прервать audit",
        "log_init": "Лог: Оповещает каждые 250 000 комбинаций.",
        "log_no_password": "ℹ️ Архив не защищён паролем.",
        "status_no_password": "Статус: Без пароля",
        "log_error_select": "❌ Ошибка: Выберите архив через Обзор!",
        "log_express": "Запуск экспресс-анализа по базе 100 популярных паролей...",
        "log_deep_start": "Запуск глубокого анализатора [A-Z, a-z, 0-9]...",
        "log_len_step": "Анализ комбинаций длиной {} знаков...",
        "log_mil_step": "Проверено {}",
        "thousand": "тыс",
        "million": "млн",
        "log_crit_err": "❌ Критическая ошибка: {}",
        "log_found": "🎉 ПАРОЛЬ НАЙДЕН: '{}'",
        "log_stopped": "⚠️ Операция остановлена пользователем.",
        "log_not_found": "❌ В рамках лимита в 7 символов ничего не найдено.",
        "log_session_time": "Время сессии: {:.3f} сек.",
        "log_divider": "-" * 55,
        "desc": "📋 ОПИСАНИЕ ПРОГРАММЫ\nZIP-Auditor — это высокоскоростная утилита, созданная для экспресс-проверки устойчивости и восстановления доступа к зашифрованным ZIP-архивам.\n\n🧠 КАК ЭТО РАБОТАЕТ?\nАудит проходит полностью в оперативной памяти (ОЗУ) без нагрузки на диск:\n1. Экспресс-анализ: Мгновенная проверка по встроенной базе из 100 самых популярных паролей.\n2. Глубокий анализатор: Последовательный посимвольный перебор комбинаций [A-Z, a-z, 0-9].\n\n⚠️ ЛИМИТЫ И ПРОИЗВОДИТЕЛЬНОСТЬ\n• В программе жестко зашит максимальный лимит длины в 7 символов.\n• Если пароль короткий, утилита найдет его сразу и завершит работу.\n• Перебор до 7 знаков генерирует триллионы комбинаций. Время зависит от мощности процессора.\n\n-------------------------------------------------------------------------\n⚙️ ИНФОРМАЦИЯ О СБОРКЕ\n• Автор: KiziName\n• Версия: V1.0\n• Лицензия: BSD 3-Clause License",
        "github_link": "🔗 GitHub: https://github.com/KIziName/ZIP-Auditor/releases"
    },
    "English": {
        "tab_audit": "Audit",
        "tab_about": "About",
        "file_lbl": "Archive File:",
        "placeholder": "No file selected...",
        "browse_btn": "📁 Browse...",
        "status_wait": "Status: Waiting for file",
        "status_ready": "Status: Ready for audit",
        "status_run": "Status: Auditing...",
        "status_deep": "Status: Deep brute-force...",
        "status_success": "Status: Access restored!",
        "status_cancel": "Status: Process interrupted",
        "status_fail": "Status: Password not found",
        "btn_start": "⚡ Start Audit [Limit: 7 chars]",
        "btn_stop": "🛑 Interrupt Audit",
        "log_init": "Log: Notifies every 250,000 combinations.",
        "log_no_password": "ℹ️ Archive is not password protected.",
        "status_no_password": "Status: No password",
        "log_error_select": "❌ Error: Select an archive via Browse!",
        "log_express": "Launching express analysis via built-in database of 100 popular passwords...",
        "log_deep_start": "Launching deep analyzer [A-Z, a-z, 0-9]...",
        "log_len_step": "Analyzing combinations with length of {} characters...",
        "log_mil_step": "Checked {}",
        "thousand": "thousand",
        "million": "million",
        "log_crit_err": "❌ Critical error: {}",
        "log_found": "🎉 PASSWORD FOUND: '{}'",
        "log_stopped": "⚠️ Operation stopped by user.",
        "log_not_found": "❌ Nothing found within the 7-character limit.",
        "log_session_time": "Session time: {:.3f} sec.",
        "log_divider": "-" * 55,
        "desc": "📋 PROGRAM DESCRIPTION\nZIP-Auditor is a high-speed utility designed to test resilience and restore access to encrypted ZIP archives.\n\n🧠 HOW IT WORKS?\nThe audit runs entirely in Random Access Memory (RAM) without disk load:\n1. Express Analysis: Instant check against a built-in database of 100 most popular passwords.\n2. Deep Analyzer: Sequential character-by-character brute-force of [A-Z, a-z, 0-9] combinations.\n\n⚠️ LIMITS AND PERFORMANCE\n• The program has a hardcoded maximum length limit of 7 characters.\n• If the password is short, the utility will find it instantly and terminate.\n• Brute-forcing up to 7 chars generates trillions of combinations. Time depends on CPU power.\n\n-------------------------------------------------------------------------\n⚙️ BUILD INFO\n• Author: KiziName\n• Version: V1.0\n• License: BSD 3-Clause License",
        "github_link": "🔗 GitHub: https://github.com/KIziName/ZIP-Auditor/releases"
    }
}

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ZipAuditorApp(ctk.CTk):
    BUILTIN_DATABASE = [
        "123456", "password", "123456789", "12345", "12345678", "qwerty", "1234567",
        "111111", "123123", "1234567890", "000000", "555555", "666666", "123321",
        "654321", "7777777", "8888888", "9999999", "qwerty123", "password1", "abc123",
        "1234", "admin", "root", "letmein", "welcome", "monkey", "dragon", "master",
        "sunshine", "iloveyou", "princess", "shadow", "ashley", "superman", "michael", 
        "jordan", "hunter", "fuckyou", "trustno1", "batman", "hello", "daniel", "jessica", 
        "soccer", "charlie", "andrew", "thomas", "joshua", "george", "harry", "jackson", 
        "oliver", "william", "james", "robert", "john", "david", "joseph", "charles", 
        "christopher", "matthew", "anthony", "mark", "donald", "steven", "paul", "kevin", 
        "brian", "timothy", "ronald", "edward", "jason", "jeffrey", "ryan", "jacob", "gary", 
        "nicholas", "eric", "jonathan", "stephen", "larry", "justin", "scott", "brandon", 
        "benjamin", "samuel", "raymond", "gregory", "frank", "alexander", "patrick", "jack", 
        "dennis", "jerry", "tyler", "aaron", "jose", "nathan", "adam", "henry", "zachary", 
        "taylor", "emma", "olivia", "sophia", "ava", "isabella", "mia", "charlotte", "amelia", 
        "harper", "evelyn"
    ]

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

        threading.Thread(target=self.perf_core, args=(self.selected_zip_path, 7), daemon=True).start()

    def perf_core(self, zip_path, max_length):
        start_time = time.time()
        try:
            is_encrypted = False
            target_file = None

            with zipfile.AESZipFile(zip_path) as z_file:
                file_list = z_file.namelist()
                if not file_list:
                    self.after(0, self.log, "log_crit_err", "Архив пуст.", True)
                    return
                
                for f_name in file_list:
                    f_info = z_file.getinfo(f_name)
                    if f_info.flag_bits & 0x1:
                        is_encrypted = True
                        target_file = f_name
                        break
                
                if not is_encrypted:
                    self.no_password_flag = True
                    self.after(0, self.log, "log_no_password", True)
                    return

            with zipfile.AESZipFile(zip_path) as z_file:
                if not self.stop_event.is_set():
                    self.after(0, self.log, "log_express", True)
                
                # ИСПРАВЛЕННЫЙ ЭКСПРЕСС-ТЕСТ: Защита дескрипторов + точечная проверка
                for common_pass in self.BUILTIN_DATABASE:
                    if self.stop_event.is_set():
                        return
                    try:
                        with z_file.open(target_file, pwd=common_pass.encode('utf-8')) as f:
                            f.read(1)
                        self.found_password = common_pass
                        self.stop_event.set()
                        break
                    except:
                        continue

                if not self.found_password and not self.stop_event.is_set():
                    self.after(0, self.log, "log_deep_start", True)
                    self.after(0, lambda: self.lbl_status.configure(text=self.txt["status_deep"], text_color="#f39c12") if not self.stop_event.is_set() else None)
                    
                    self.is_deep_mode = True
                    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
                    tested = 0
                    
                    for length in range(1, max_length + 1):
                        if self.stop_event.is_set():
                            return
                        self.after(0, self.log, "log_len_step", length, True)
                        
                        for combo in itertools.product(chars, repeat=length):
                            if self.stop_event.is_set():
                                return
                            
                            candidate = "".join(combo)
                            tested += 1
                            
                            if tested % 250000 == 0:
                                count = tested
                                if count >= 1_000_000:
                                    display = f"{count/1_000_000:.1f} {self.txt['million']}"
                                else:
                                    display = f"{count//1000} {self.txt['thousand']}"
                                self.after(0, self.log, "log_mil_step", display, False)
                            
                            # ИСПРАВЛЕННЫЙ ГЛУБОКИЙ ПЕРЕБОР: Работает со всеми типами шифрования
                            try:
                                with z_file.open(target_file, pwd=candidate.encode('utf-8')) as f:
                                    f.read(1)
                                self.found_password = candidate
                                self.stop_event.set()
                                break
                            except:
                                continue
                                
        except Exception as e:
            if not self.stop_event.is_set():
                self.after(0, self.log, "log_crit_err", str(e), True)
        finally:
            self.after(0, self.brute_finished, time.time() - start_time)

    def brute_finished(self, elapsed):
        self.is_running = False
        self.is_deep_mode = False

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

if __name__ == "__main__":
    app = ZipAuditorApp()
    app.mainloop()
