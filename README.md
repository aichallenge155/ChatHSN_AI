# AI-Powered Discord Bot for IT Olympiad

Bu layihə, IT Olimpiadası üçün hazırlanmış AI ilə gücləndirilmiş Discord botudur. Bot, istifadəçilərə müxtəlif suallar verməyə və AI cavabları, istinadlar, təriflər və təhsil planları təqdim etməyə imkan verir.

## 📁 Layihə Struktur
```
DISCORD_AI_BOT/
├── .venv/                  # Virtual mühit qovluğu
├── ai/                     # AI ilə bağlı modul
│   ├── __init__.py
│   ├── ai_handler.py       # AI-dan cavab yaradan funksiyalar
│   └── ai_styles/          # Cavab tərzləri modulu
│       ├── __init__.py
│       └── response_styles.py
├── commands/               # Bot komandaları modulu
│   ├── __init__.py
│   ├── base_commands.py    # `!ask`, `!style`, `!help`, `!challenge` komandaları
│   └── special_commands.py # `!cite`, `!define`, `!studyplan`, `!users`, `!image`, `!convert`, `!analyse` komandaları
├── database/               # SQLite verilənlər bazası
│   ├── __init__.py
│   ├── db_manager.py       # DB əməliyyatları (init, CRUD funksiyaları)
│   ├── user_db.db          # İstifadəçi məlumat bazası
│   └── users.db            # İstifadəçi interaksiyaları bazası
├── utils/                  # Yardımçı funksiyalar
│   ├── __init__.py
│   └── error_handler.py    # Xətaların idarə olunması
├── .env                    # Mühit dəyişənləri (gitignore daxilindədir)
├── .gitignore              # Git-lə paylaşılmayan fayl nümunələri
├── config.py               # Konfiqurasiya və mühit dəyişənləri
├── main.py                 # Botun əsas giriş nöqtəsi
├── README.md               # Layihə sənədi
└── requirements.txt        # Layihə asılılıqları
```

---

## 🚀 Başlanğıc Təlimatları

1. **Layihəni klonlayın**
    ```bash
    git clone https://github.com/aichallenge155/ChatHSN_AI.git
    cd ChatHSN_AI
    ```

2. **Virtual mühit yaradın və aktiv edin**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux/macOS:
    source .venv/bin/activate
    ```

3. **Asılılıqları quraşdırın**
    ```bash
    pip install -r requirements.txt
    ```

4. **Mühit dəyişənlərini təyin edin**
    Layihənin kök qovluğunda `.env` faylı yaradın və aşağıdakı dəyərləri əlavə edin:
    ```dotenv
    DISCORD_TOKEN=your_discord_token_here
    AI_API_KEY=your_gemini_or_ai_api_key_here
    ```

5. **Verilənlər bazasını ilkin qurun**
    `main.py` faylını işə saldıqda DB avtomatik qurulur:
    ```bash
    python main.py
    ```

---

## ⚙️ Konfiqurasiya (`config.py`)

- **DISCORD_TOKEN**: Discord bot token.
- **AI_API_KEY**: AI model üçün API açarı.
- **COMMAND_PREFIX**: Bot əmrlərinin prefiksi (default `!`).
- **BOT_DESCRIPTION**: Botun qısa təsviri.
- **RESPONSE_STYLES**: `ai_styles/response_styles.py` faylında istifadə olunan cavab tərzləri:
  - `default`: Köməkçi, qısa cavablar.
  - `kid`: 8 yaşlı uşağa uyğun sadə dil.
  - `physics_teacher`: Fizika müəllimi tərzi.
  - `poet`: Poetik, metaforik tərz.
  - `historian`: Tarixi kontekstlərlə izah.

---

## ⚡ Əsas Funksionallıqlar

| Commands                               | Description                                                               |
|----------------------------------------|---------------------------------------------------------------------------|
| `!ask <prompt>`                        | Ask anything or get AI-generated answers.                                 |
| `!style [style_name]`                  | View and customize your response style.                                   |
| `!help`                                | Shows help information about the bot.                                     |
| `!cite <mövzu>`                        | Get a trusted citation on any topic.                                      |
| `!define <termin>`                     | Define any word or concept.                                               | 
| `!studyplan <mövzu>`                   | Generate a personalized study plan.                                       |
| `!users`                               | Shows list of bot users(only for admin).                                  |
| `!image [description]`                 | Create a picture based on the description.                                |
| `!convert [from_format] [to_format]`   | Convert an uploaded file into the desired format (e.g., PDF ➔ DOCX)      |
| `!challenge [language_code]`           | Start a challenge in specified language (e.g. en, az, ru, tr, fr, de, es) |
| `!analyse [file]`                      | Upload a file for analysis, text extraction, or format detection.         |

> **Qeyd:** `!users` command is only for adminstrator users.

---

## 🗄️ Verilənlər Bazası (`database/db_manager.py`)

- **init_db()**: `users` və `interactions` cədvəllərini yaradır.
- **add_user(user_id, username)**: Yeni istifadəçi əlavə edir və ya mövcud istifadəçini yeniləyir.
- **update_last_interaction(user_id)**: Son interaksiyanı qeyd edir.
- **log_interaction(user_id, interaction_type)**: Hər bir komanda çağırışını `interactions` cədvəlinə yazır.
- **get_all_users()**: Bütün istifadəçiləri geri qaytarır.
- **get_user_interactions(user_id, limit)**: Xüsusi istifadəçinin son interaksiyalarını alır.

---

## 💡 Gələcək İnkişaf İdeyaları

- `!history`: İstifadəçinin komanda tarixçəsini göstərmək.
- Analytics dashboard: İstifadəçi interaksiyalarını qrafiklərlə vizuallaşdırmaq.
- Multilingual dəstək: Cavabları bir neçə dildə təqdim etmək.
- Discord `Button` və `Select` komponentləri ilə zəngin UI.

---

## 📄 Lisenziya
Bu layihə [MIT Lisenziyası](LICENSE) ilə yayımlanır.

---

### Əlaqə
Hər hansı sual və ya təklif üçün: **ilkin3964@mail.ru**

