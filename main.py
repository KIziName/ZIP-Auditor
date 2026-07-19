import sys
import ctypes
import atexit
import os

def init_system_wide_mutex():
    """
    Проверяет, запущена ли уже копия приложения в системе.
    Если запущена, выводит предупреждение и мгновенно завершает процесс.
    """
    kernel32 = ctypes.windll.kernel32
    clean_name = os.path.basename(sys.argv[0]).replace('.', '_').replace(' ', '_')
    mutex_name = f"Global\\AutoGuard_{clean_name}_Mutex"
    mutex_handle = kernel32.CreateMutexW(None, False, mutex_name)
    
    if kernel32.GetLastError() == 183:
        if mutex_handle:
            kernel32.CloseHandle(mutex_handle)
            
        try:
            is_russian = ctypes.windll.kernel32.GetUserDefaultUILanguage() == 1049
        except Exception:
            is_russian = True
            
        if is_russian:
            msg = "Приложение уже запущено!\nРазрешена только одна активная копия."
            title = "Защита от повторного запуска"
        else:
            msg = "The application is already running!\nOnly one active instance is allowed."
            title = "Already Running"
            
        ctypes.windll.user32.MessageBoxW(0, msg, title, 0x10 | 0x00)
        sys.exit(0)
        
    atexit.register(lambda: kernel32.CloseHandle(mutex_handle) if mutex_handle else None)


if __name__ == "__main__":
    # Сначала проверяем мьютекс
    init_system_wide_mutex()
    
    # Импортируем GUI только при успешной проверке
    from gui import ZipAuditorApp
    
    app = ZipAuditorApp()
    app.mainloop()
