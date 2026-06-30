# MP3 Ship

## Русская версия

### [Скачать готовый EXE: MP3Ship.exe](dist/MP3Ship.exe)

MP3 Ship скачивает одно или несколько видео YouTube или целые плейлисты и сохраняет результат в `.mp3`.

Готовая Windows-сборка лежит здесь:

```text
dist\MP3Ship.exe
```

Пользователю нужен только этот один файл:

- не нужно устанавливать Python;
- не нужно устанавливать `yt-dlp`;
- не нужно устанавливать FFmpeg.

FFmpeg уже встроен внутрь `.exe` через PyInstaller. Интерфейс поддерживает русский и английский языки, а в поле ссылок можно вставлять сразу несколько YouTube-ссылок: по одной на строку, через пробел или прямо списком из сообщения.

### Как пользоваться

1. Откройте `MP3Ship.exe`.
2. Вставьте одну или несколько ссылок YouTube.
3. Выберите папку для сохранения.
4. Выберите качество MP3: `128`, `192`, `256` или `320`.
5. Нажмите `Скачать MP3`.

Используйте приложение только для своих видео, видео со свободной лицензией или контента, который вы имеете право скачивать.

### Сборка из исходников

Установите зависимости:

```powershell
python -m pip install -r requirements.txt
```

Перед сборкой убедитесь, что файл FFmpeg находится здесь:

```text
C:\ffmpeg\bin\ffmpeg.exe
```

Соберите автономное Windows-приложение:

```powershell
python -m PyInstaller --clean --noconfirm MP3Ship.spec
```

Готовый файл появится здесь:

```text
dist\MP3Ship.exe
```

### Режим командной строки

Оригинальный скрипт тоже работает:

```powershell
python youtube_to_mp3.py "C:\Users\Rasul\Music" "https://www.youtube.com/watch?v=VIDEO_ID" --quality 320
```

---

## English Version

### [Download the ready EXE: MP3Ship.exe](dist/MP3Ship.exe)

MP3 Ship downloads one or more YouTube videos or playlists and saves them as `.mp3` files.

The ready Windows build is here:

```text
dist\MP3Ship.exe
```

Users only need this single file:

- no Python installation;
- no manual `yt-dlp` installation;
- no manual FFmpeg installation.

FFmpeg is bundled inside the `.exe` with PyInstaller. The interface supports Russian and English, and the links field accepts many YouTube links at once: one per line, separated by spaces, or pasted from a message/list.

### How To Use

1. Open `MP3Ship.exe`.
2. Paste one or more YouTube links.
3. Choose the output folder.
4. Choose MP3 quality: `128`, `192`, `256`, or `320`.
5. Press `Download MP3`.

Use this only for videos that you own, videos with a license that allows downloading, or content that you are otherwise legally allowed to download.

### Build From Source

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Make sure FFmpeg exists before building:

```text
C:\ffmpeg\bin\ffmpeg.exe
```

Build the self-contained Windows app:

```powershell
python -m PyInstaller --clean --noconfirm MP3Ship.spec
```

The output file will be:

```text
dist\MP3Ship.exe
```

### Command-Line Mode

The original script still works:

```powershell
python youtube_to_mp3.py "C:\Users\Rasul\Music" "https://www.youtube.com/watch?v=VIDEO_ID" --quality 320
```

## Author

Zeynalov U.R.o.
