# MP3 Ship

## Русская Версия

### [Скачать готовый EXE: MP3Ship.exe](dist/MP3Ship.exe)

MP3 Ship - автономное Windows-приложение для скачивания аудио с YouTube в MP3.

Что умеет приложение:

- скачивает одно видео, несколько ссылок или плейлист YouTube;
- принимает много ссылок сразу: по строкам, через пробел или списком из сообщения;
- сохраняет результат в выбранную папку;
- конвертирует аудио в `.mp3`;
- позволяет выбрать качество MP3: `128`, `192`, `256`, `320`;
- показывает журнал скачивания и конвертации;
- поддерживает остановку текущего скачивания кнопкой `Остановить`;
- поддерживает русский и английский интерфейс;
- использует `cookies.txt`, если YouTube просит подтвердить, что вы не бот;
- содержит внутри FFmpeg и Deno, поэтому пользователю не нужно ничего устанавливать.

Пользователю нужен только файл:

```text
dist\MP3Ship.exe
```

### Как Пользоваться

1. Откройте `MP3Ship.exe`.
2. Вставьте одну или несколько ссылок YouTube.
3. Выберите папку для сохранения.
4. Выберите качество MP3.
5. При необходимости выберите `cookies.txt`.
6. Нажмите `Скачать MP3`.
7. Чтобы прервать процесс, нажмите `Остановить`.

### Если YouTube Пишет, Что Вы Не Бот

Если появляется ошибка `Sign in to confirm you’re not a bot`, нажмите `Помощь с cookies`.

Общий порядок такой:

1. Откройте YouTube в браузере и войдите в аккаунт.
2. Установите расширение для экспорта cookies в формате `cookies.txt`.
3. На сайте YouTube экспортируйте cookies в файл.
4. В MP3 Ship нажмите `Выбрать` рядом с `cookies.txt` и укажите этот файл.
5. Повторите скачивание.

Это работает даже с открытым браузером: приложение читает выбранный файл `cookies.txt`, а не заблокированную базу Chrome/Edge.

### Почему Внутри Есть Deno

YouTube иногда требует решить JavaScript-подпись перед выдачей аудио. Если JavaScript runtime отсутствует, `yt-dlp` может видеть только изображения и писать `Signature solving failed` или `Only images are available`. В сборку встроен Deno, чтобы пользователь не устанавливал Node/Deno отдельно.

### Сборка Из Исходников

Установите зависимости:

```powershell
python -m pip install -r requirements.txt
```

Перед сборкой нужны:

```text
C:\ffmpeg\bin\ffmpeg.exe
vendor\deno\deno.exe
```

Соберите exe:

```powershell
python -m PyInstaller --clean --noconfirm MP3Ship.spec
```

Готовый файл появится здесь:

```text
dist\MP3Ship.exe
```

### Командная Строка

Скрипт тоже можно запускать напрямую:

```powershell
python youtube_to_mp3.py "C:\Users\Rasul\Music" "https://www.youtube.com/watch?v=VIDEO_ID" --quality 320
```

С cookies:

```powershell
python youtube_to_mp3.py "C:\Users\Rasul\Music" "https://www.youtube.com/watch?v=VIDEO_ID" --cookies "C:\Users\Rasul\Downloads\cookies.txt"
```

Используйте приложение только для своих видео, видео со свободной лицензией или контента, который вы имеете право скачивать.

---

## English Version

### [Download The Ready EXE: MP3Ship.exe](dist/MP3Ship.exe)

MP3 Ship is a self-contained Windows app for downloading YouTube audio as MP3.

What it does:

- downloads one video, many links, or a YouTube playlist;
- accepts many links at once;
- saves MP3 files to a chosen folder;
- lets the user choose MP3 quality;
- shows a download and conversion log;
- can stop the current download;
- supports Russian and English;
- accepts an exported `cookies.txt` when YouTube asks for bot confirmation;
- bundles FFmpeg and Deno, so users do not install anything else.

Build output:

```text
dist\MP3Ship.exe
```

## Author

Zeynalov U.R.o.
