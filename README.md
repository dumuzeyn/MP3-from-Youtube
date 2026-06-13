# YouTube to MP3 Downloader

Python-скрипт для скачивания аудио с одной или нескольких ссылок YouTube и сохранения результата в `.mp3`. Имя файла берется из названия видео на YouTube.

[English version](#engLL).

### Что делает программа

- Принимает одну или несколько ссылок на YouTube-видео или плейлист.
- Принимает путь к папке для сохранения.
- Скачивает лучшую доступную аудиодорожку.
- Конвертирует аудио в MP3 через FFmpeg.
- Сохраняет файл с названием видео YouTube.

> Используйте скрипт только для своих видео, видео с разрешающей лицензией или контента, который вы имеете право скачивать.

### Что нужно установить

- Python 3.9 или новее.
- `yt-dlp` из файла `requirements.txt`.
- FFmpeg, установленный и доступный через `PATH`.

### Установка Python-зависимостей

Откройте PowerShell в этой папке и выполните:

```powershell
pip install -r requirements.txt
```

Если `pip` относится к другой версии Python, используйте:

```powershell
python -m pip install -r requirements.txt
```

### Правильная установка FFmpeg на Windows

FFmpeg нужен, потому что `yt-dlp` скачивает аудио, а FFmpeg конвертирует его в MP3.

Официальная страница загрузки FFmpeg:

<https://ffmpeg.org/download.html>

Официальный сайт FFmpeg дает исходный код и ссылки на готовые Windows-сборки. Для Windows самый простой вариант - сборка `release essentials` с gyan.dev:

<https://www.gyan.dev/ffmpeg/builds/>

#### Вариант 1: Ручная установка

1. Откройте <https://www.gyan.dev/ffmpeg/builds/>.
2. Найдите раздел `release builds`.
3. Скачайте `ffmpeg-release-essentials.zip`.
4. Распакуйте ZIP-архив.
5. Переименуйте распакованную папку в `ffmpeg`, чтобы путь был короче и понятнее.
6. Переместите папку сюда:

```text
C:\ffmpeg
```

После распаковки важный файл должен находиться здесь:

```text
C:\ffmpeg\bin\ffmpeg.exe
```

Теперь добавьте FFmpeg в `PATH`:

1. Нажмите `Win + R`.
2. Введите `sysdm.cpl` и нажмите Enter.
3. Откройте вкладку `Дополнительно`.
4. Нажмите `Переменные среды`.
5. В блоке `Переменные среды пользователя` выберите `Path`.
6. Нажмите `Изменить`.
7. Нажмите `Создать`.
8. Добавьте:

```text
C:\ffmpeg\bin
```

9. Нажмите `OK` во всех окнах.
10. Закройте и заново откройте PowerShell.

Проверьте, что FFmpeg работает:

```powershell
ffmpeg -version
```

Если появилась информация о версии, FFmpeg установлен правильно.

#### Вариант 2: Установка через winget

Если у вас установлен Windows Package Manager, выполните:

```powershell
winget install "FFmpeg (Essentials Build)"
```

После установки закройте и заново откройте PowerShell, затем проверьте:

```powershell
ffmpeg -version
```

### Использование

Основная команда:

```powershell
python youtube_to_mp3.py "ПАПКА_ДЛЯ_СОХРАНЕНИЯ" "ССЫЛКА_YOUTUBE"
```

Пример:

```powershell
python youtube_to_mp3.py "C:\Users\Rasul\Music" "https://www.youtube.com/watch?v=VIDEO_ID"
```

Скачать несколько ссылок:

```powershell
python youtube_to_mp3.py "C:\Users\Rasul\Music" "https://youtu.be/VIDEO_1" "https://youtu.be/VIDEO_2" "https://youtu.be/VIDEO_3"
```

Скачать плейлист:

```powershell
python youtube_to_mp3.py "C:\Users\Rasul\Music" "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

Выбрать качество MP3:

```powershell
python youtube_to_mp3.py "C:\Users\Rasul\Music" "https://youtu.be/VIDEO_ID" --quality 320
```

Доступные значения качества:

- `128`
- `192`
- `256`
- `320`

По умолчанию используется `192`.

### Решение проблем

#### `ffmpeg is not recognized`

FFmpeg не добавлен в `PATH`. Добавьте эту папку в `Path`:

```text
C:\ffmpeg\bin
```

После этого закройте и заново откройте PowerShell.

#### `ModuleNotFoundError: No module named 'yt_dlp'`

Установите зависимости:

```powershell
python -m pip install -r requirements.txt
```

#### YouTube не скачивается

Обновите `yt-dlp`:

```powershell
python -m pip install -U yt-dlp
```

#### Папки для сохранения не существует

Скрипт создаст папку автоматически.

>**Автор проекта: Зейналов У.Р.о.**
---
<h2 id = engLL>
 English
</h2>

Python script for downloading audio from one or more YouTube links and saving it as `.mp3` files. The output file name is based on the YouTube video title.

### What this script does

- Accepts one or more YouTube video or playlist links.
- Accepts an output folder path.
- Downloads the best available audio stream.
- Converts the audio to MP3 through FFmpeg.
- Saves files using the YouTube video title.

> Use this only for videos that you own, videos with a license that allows downloading, or content you are otherwise legally allowed to download.

### Requirements

- Python 3.9 or newer.
- `yt-dlp`, installed from `requirements.txt`.
- FFmpeg installed and available in `PATH`.

### Install Python dependencies

Open PowerShell in this folder and run:

```powershell
pip install -r requirements.txt
```

If `pip` points to another Python installation, use:

```powershell
python -m pip install -r requirements.txt
```

### Correct FFmpeg installation on Windows

FFmpeg is required because `yt-dlp` downloads the audio and FFmpeg converts it to MP3.

Official FFmpeg download page:

<https://ffmpeg.org/download.html>

The official FFmpeg site provides source code and links to ready-made Windows builds. For Windows, a simple reliable choice is the `release essentials` build from gyan.dev:

<https://www.gyan.dev/ffmpeg/builds/>

#### Option 1: Manual installation

1. Open <https://www.gyan.dev/ffmpeg/builds/>.
2. Find the `release builds` section.
3. Download `ffmpeg-release-essentials.zip`.
4. Extract the ZIP file.
5. Rename the extracted folder to `ffmpeg` if you want a clean path.
6. Move it to:

```text
C:\ffmpeg
```

After extraction, the important file should be here:

```text
C:\ffmpeg\bin\ffmpeg.exe
```

Now add FFmpeg to `PATH`:

1. Press `Win + R`.
2. Type `sysdm.cpl` and press Enter.
3. Open the `Advanced` tab.
4. Click `Environment Variables`.
5. In `User variables`, select `Path`.
6. Click `Edit`.
7. Click `New`.
8. Add:

```text
C:\ffmpeg\bin
```

9. Click `OK` in all windows.
10. Close and reopen PowerShell.

Check that FFmpeg works:

```powershell
ffmpeg -version
```

If you see version information, FFmpeg is installed correctly.

#### Option 2: Install with winget

If you use Windows Package Manager, run:

```powershell
winget install "FFmpeg (Essentials Build)"
```

Then close and reopen PowerShell and check:

```powershell
ffmpeg -version
```

### Usage

Basic command:

```powershell
python youtube_to_mp3.py "OUTPUT_FOLDER" "YOUTUBE_LINK"
```

Example:

```powershell
python youtube_to_mp3.py "C:\Users\Rasul\Music" "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download several links:

```powershell
python youtube_to_mp3.py "C:\Users\Rasul\Music" "https://youtu.be/VIDEO_1" "https://youtu.be/VIDEO_2" "https://youtu.be/VIDEO_3"
```

Download a playlist:

```powershell
python youtube_to_mp3.py "C:\Users\Rasul\Music" "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

Choose MP3 quality:

```powershell
python youtube_to_mp3.py "C:\Users\Rasul\Music" "https://youtu.be/VIDEO_ID" --quality 320
```

Available quality values:

- `128`
- `192`
- `256`
- `320`

Default quality is `192`.

### Troubleshooting

#### `ffmpeg is not recognized`

FFmpeg is not in `PATH`. Add this folder to `Path`:

```text
C:\ffmpeg\bin
```

Then close and reopen PowerShell.

#### `ModuleNotFoundError: No module named 'yt_dlp'`

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

#### YouTube download fails

Update `yt-dlp`:

```powershell
python -m pip install -U yt-dlp
```

#### The output folder does not exist

The script creates the output folder automatically.

> **Author of poject: Zeynalov U.R.o.**
