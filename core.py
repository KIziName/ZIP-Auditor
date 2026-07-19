import os
import time
import string
import itertools
import pyzipper as zipfile
from locales import BUILTIN_DATABASE

def check_password_fast(active_z_file, filename, pwd_str, is_old_crypto):
    try:
        with active_z_file.open(filename, pwd=pwd_str.encode('utf-8')) as f:
            if is_old_crypto:
                f.read(1024)
            else:
                f.read(1)
        return True
    except Exception:
        return False

def is_aes_encrypted(zipinfo):
    extra = zipinfo.extra
    i = 0
    while i < len(extra):
        if len(extra) - i < 4:
            break
        header_id = int.from_bytes(extra[i:i+2], 'little')
        data_size = int.from_bytes(extra[i+2:i+4], 'little')
        if header_id == 0x9901:
            return True
        i += 4 + data_size
    return False

def run_audit(zip_path, max_length, stop_event, log_callback, update_status_callback, on_finish_callback):
    start_time = time.time()
    found_password = None
    no_password_flag = False
    
    try:
        is_encrypted = False
        target_file = None

        with zipfile.AESZipFile(zip_path) as z_file:
            file_list = z_file.namelist()
            if not file_list:
                log_callback("log_crit_err", "Архив пуст.", True)
                on_finish_callback(time.time() - start_time, None, False)
                return
            
            for f_name in file_list:
                f_info = z_file.getinfo(f_name)
                if (f_info.flag_bits & 0x1) and f_info.file_size > 0:
                    is_encrypted = True
                    target_file = f_name
                    break
            
            if not target_file:
                for f_name in file_list:
                    f_info = z_file.getinfo(f_name)
                    if f_info.flag_bits & 0x1:
                        is_encrypted = True
                        target_file = f_name
                        break

            if not is_encrypted:
                no_password_flag = True
                log_callback("log_no_password", True)
                on_finish_callback(time.time() - start_time, None, True)
                return

            target_info = z_file.getinfo(target_file)
            is_legacy = not is_aes_encrypted(target_info)
            enc_type = "ZipCrypto" if is_legacy else "AES"
            log_callback("log_encryption_type", enc_type, True)

        with zipfile.AESZipFile(zip_path) as active_z_file:
            if not stop_event.is_set():
                log_callback("log_express", True)
            
            # 1. База частых паролей
            for common_pass in BUILTIN_DATABASE:
                if stop_event.is_set():
                    on_finish_callback(time.time() - start_time, None, False)
                    return
                if check_password_fast(active_z_file, target_file, common_pass, is_legacy):
                    found_password = common_pass
                    stop_event.set()
                    break

            # 2. Глубокий посимвольный Brute-force
            if not found_password and not stop_event.is_set():
                log_callback("log_deep_start", True)
                update_status_callback()
                
                chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
                tested = 0
                next_report = 250000

                for length in range(1, max_length + 1):
                    if stop_event.is_set():
                        on_finish_callback(time.time() - start_time, None, False)
                        return
                    log_callback("log_len_step", length, True)
                    
                    for combo in itertools.product(chars, repeat=length):
                        if stop_event.is_set():
                            on_finish_callback(time.time() - start_time, None, False)
                            return
                        
                        candidate = "".join(combo)
                        tested += 1
                        
                        if tested >= next_report:
                            next_report += 250000
                            log_callback("log_mil_step", tested, False)
                        
                        if check_password_fast(active_z_file, target_file, candidate, is_legacy):
                            found_password = candidate
                            stop_event.set()
                            break
                    
                    if found_password:
                        break
                                    
    except Exception as e:
        if not stop_event.is_set():
            log_callback("log_crit_err", str(e), True)
    finally:
        on_finish_callback(time.time() - start_time, found_password, no_password_flag)
