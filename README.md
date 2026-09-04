# ZIP‑Auditor

***ZIP‑Auditor*** is a lightweight utility for recovering forgotten passwords from ZIP archives.
It runs entirely in RAM, creates no temporary files, and does not stress your disk.

🔐 Supports archives encrypted with ZipCrypto (Legacy) as well as AES‑256.

---

## 📋 Description

The audit runs in two stages:

1. ***Express Analysis*** – instant check against a built‑in database of the 100 most common passwords (based on leak statistics).
2. ***Deep Brute‑force*** – sequentially tries all combinations of letters (A‑Z, a‑z) and digits (0‑9) up to 7 characters long.

Progress notifications appear every 250,000 attempts.
You can interrupt the process at any time with the Stop button.

---

## ⚡ Features

· ✅ Instant check against a popular‑password database.

· 🔍 Deep brute‑force up to 7 characters (letters and digits).

· 🛑 Stop the process with one click; the log is cleared.

· 📜 Smart logging with progress updates.

· 🌐 Two interface languages: Russian and English (switch on the fly).

· 🌙 Dark theme based on `CustomTkinter`.

· 🔗 Built‑in GitHub link in the «About» section.

---

## 🧰 Requirements

· ***Python 3.7*** or higher

  · `pip install customtkinter`
  
  · `pip install pyzipper` (for ZIP archive handling, including AES)

# ZIP‑Auditor

**ZIP‑Auditor** — простая утилита для восстановления доступа к забытому паролю ZIP‑архива.  
Работает полностью в оперативной памяти, не создаёт временных файлов и не нагружает диск.

🔐 Поддерживает архивы, зашифрованные как **ZipCrypto (Legacy)**, так и **AES‑256**.

---

## 📋 Описание

Программа выполняет аудит пароля в два этапа:

1. **Экспресс‑анализ** — мгновенная проверка по встроенной базе из 100 самых популярных паролей (основано на статистике утечек).
2. **Глубокий перебор** — последовательный перебор всех комбинаций из букв (A‑Z, a‑z) и цифр (0‑9) длиной **до 7 символов**.

Каждые 250 000 попыток в логе появляется уведомление о прогрессе.  
Аудит можно прервать в любой момент кнопкой «Прервать».

---

## ⚡ Возможности

- ✅ Мгновенная проверка по базе популярных паролей.
- 🔍 Глубокий перебор до 7 символов (буквы и цифры).
- 🛑 Остановка процесса одной кнопкой с очисткой лога.
- 📜 Умное логирование с уведомлениями о прогрессе.
- 🌐 Два языка интерфейса: русский и английский (переключение в один клик).
- 🌙 Тёмная тема на основе `CustomTkinter`.
- 🔗 Встроенная ссылка на GitHub в разделе «О программе».

---

## 🧰 Требования

- **Python 3.7** или выше
  - `pip install customtkinter`
  - `pip install pyzipper` (для работы с ZIP‑архивами)
