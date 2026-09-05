STRINGS = {
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
        "log_express": "Launching express analysis via built-in database of popular passwords...",
        "log_deep_start": "Launching deep analyzer [A-Z, a-z, 0-9]...",
        "log_len_step": "Analyzing combinations with length of {} characters...",
        "log_mil_step": "Checked {} {}",
        "thousand": "thousand",
        "million": "million",
        "log_encryption_type": "🔐 Encryption type: {}",
        "log_crit_err": "❌ Critical error: {}",
        "log_found": "🎉 PASSWORD FOUND: '{}'",
        "log_stopped": "⚠️ Operation stopped by user.",
        "log_not_found": "❌ Nothing found within the 7-character limit.",
        "log_session_time": "Session time: {:.3f} sec.",
        "log_divider": "-" * 55,
        "log_empty_encrypted": "⚠️ Archive contains only empty encrypted files. Password check impossible.",
        "about_title": "About ZIP-Auditor",
        "about_version": "Version: V1.0",
        "about_author": "Author: KiziName",
        "github_link": "🔗 GitHub: https://github.com/KIziName/ZIP-Auditor/releases"
    }
}

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

MAX_PASSWORD_LENGTH = 7            
LOG_REPORT_STEP = 250_000            
CHECK_READ_SIZE_LEGACY = 1024  
CHECK_READ_SIZE_AES = 1              
BRUTE_CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
WINDOW_WIDTH = 580
WINDOW_HEIGHT = 560
