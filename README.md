<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=🎥%20YouTube%20Cloude&fontSize=80&fontAlignY=35&animation=fadeIn" />

<br>

> 🗂️ **Храни файлы в видео. Бесплатно. Надёжно. Красиво.**

<br>

[![Version](https://img.shields.io/badge/version-2.0-blue?style=for-the-badge)](https://github.com/Hinderchik/YouTube-Cloude-Fork)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-yellow?style=for-the-badge&logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=for-the-badge)](https://github.com/Hinderchik/YouTube-Cloude-Fork)

<br>

```

┌──────────────────────────────────────────┐
│                                          │
│   📁 secret.zip                          │
│        ↓                                │
│   🎨 Кодирование в видео                │
│        ↓                                │
│   📹 output.mp4                         │
│        ↓                                │
│   ☁️  YouTube (бесплатное облако)       │
│        ↓                                │
│   📹 video.mp4                          │
│        ↓                                │
│   🎨 Декодирование обратно              │
│        ↓                                │
│   📁 secret.zip ✅                       │
│                                          │
└──────────────────────────────────────────┘

```

<br>

[<kbd> <br> 🚀 Быстрый старт <br> </kbd>](#-быстрый-старт)
[<kbd> <br> 📖 Как работает <br> </kbd>](#-как-это-работает)
[<kbd> <br> ⭐ Поставить звезду <br> </kbd>](https://github.com/Hinderchik/YouTube-Cloude-Fork)

</div>

---

## ✨ Почему YouTube Cloude?

<table>
<tr>
<td width="50%">

### 🎨 Красивое шифрование
Ваши файлы превращаются в цветные мозаики Full HD. 16 ярких цветов кодируют данные в каждом кадре

### 🔐 Надёжная защита
XOR-шифрование с SHA-256 хешированием ключа. Создайте `key.txt` и ваши данные под надёжной защитой

### 🧩 Тройное дублирование
Каждый кадр содержит 3 копии данных. YouTube сжимает видео? Не страшно — данные продублированы

</td>
<td width="50%">

### 📦 Любые файлы
Фотографии, документы, архивы, пароли, криптокошельки — вообще что угодно до 100 МБ

### 🛡️ Защита от потерь
5 защитных кадров в конце и маркер завершения данных. YouTube ничего не обрежет

### 🚫 Минимум зависимостей
Только OpenCV и NumPy. Работает даже в Termux на телефоне без FFmpeg

</td>
</tr>
</table>

---

## 📦 Быстрый старт

```bash
# Клонируем репозиторий
git clone https://github.com/Hinderchik/YouTube-Cloude-Fork
cd YouTube-Cloude-Fork

# Устанавливаем зависимости
pip install opencv-python numpy

# Запускаем
python youtube_storage_fixed.py
```

<details>
<summary><b>📱 Установка на Termux (Android)</b></summary>

```bash
pkg update && pkg upgrade
pkg install python git
pip install opencv-python numpy
git clone https://github.com/Hinderchik/YouTube-Cloude-Fork
cd YouTube-Cloude-Fork
python youtube_storage_fixed.py
```

💡 FFmpeg на Termux: pkg install x11-repo && pkg install ffmpeg

</details>

---


## 📱 Установка на Termux (Android)

<details>
<summary><b>Пошаговая инструкция</b></summary>

```bash
# 1. Обновляем пакеты
pkg update && pkg upgrade

# 2. Ставим нужные репозитории
pkg install x11-repo

# 3. Устанавливаем зависимости
pkg install python opencv python-numpy ffmpeg

# 4. Клонируем проект
git clone https://github.com/Hinderchik/YouTube-Cloude-Fork
cd YouTube-Cloude-Fork

# 5. Запускаем
python youtube_storage_fixed.py
```

</details>

<details>
<summary><b>⚠️ Частые проблемы и решения</b></summary>

<br>

❌ ModuleNotFoundError: No module named 'cv2'

Причина: Python не видит OpenCV из репозитория.

```bash
# Проверь, установлен ли opencv
pkg list-installed | grep opencv

# Если нет — ставь
pkg install opencv opencv-python python-opencv-python

# Если есть, но не работает — проверь путь
find /data/data/com.termux/files/usr -name "cv2*" 2>/dev/null
python -c "import sys; print(sys.path)"
```

---

❌ ImportError: dlopen failed: library "libavif.so" not found

Причина: Не хватает системной библиотеки.

```bash
pkg install libavif
python -c "import cv2; print('OK')"
```

---

❌ pip install opencv-python падает с ошибкой CMake

Причина: pip пытается собрать пакет из исходников, но не хватает компилятора.

Не делай так. Используй готовые пакеты из репозитория Termux:

```bash
# Правильно
pkg install opencv python-numpy

# Неправильно
pip install opencv-python  # ❌ Будет собирать из исходников
```

Если очень нужно через pip — сначала поставь компилятор:

```bash
pkg install cmake ninja build-essential python-dev
pip install opencv-python-headless
```

---

❌ numpy не устанавливается / конфликтует

Причина: Python 3.13 ещё не полностью поддерживается.

```bash
# Удали pip-версию
pip uninstall numpy -y

# Поставь из репозитория Termux
pkg install python-numpy

# Проверь
python -c "import numpy; import cv2; print('OK')"
```

---

❌ Ошибка connection aborted при pip install

Причина: Нестабильное интернет-соединение или проблемы с DNS.

```bash
# Попробуй ещё раз
pip install --no-cache-dir имя_пакета

# Или смени DNS (в новом терминале)
echo "nameserver 8.8.8.8" > ~/../usr/etc/resolv.conf
```

---

❌ FFmpeg не устанавливается

```bash
pkg install x11-repo
pkg install ffmpeg

# Проверь
ffmpeg -version
```

💡 FFmpeg не обязателен. Скрипт работает и без него через OpenCV, просто видео будет больше.

---

💡 Общий совет

Если что-то не работает — всегда сначала:

```bash
pkg update && pkg upgrade
```

И ставь пакеты через pkg, а не через pip где это возможно.

</details>

---

🎮 Интерфейс

```
==================================================
🎥 YouTube File Storage
==================================================
🔑 Ключ загружен из key.txt

--------------------------------------------------
Выберите действие:
1. Закодировать файл в видео
2. Декодировать видео в файл
3. Выход
--------------------------------------------------

Введите номер (1-3): _
```

Закодировать файл:

```
--- Кодирование файла ---
Путь к файлу: secret.zip
Имя выходного видео [secret.mp4]: 
📤 Кодирование: secret.zip
📦 Размер: 5242880 байт
🔐 Данные зашифрованы
🎬 Кадров: 420 (70.0 сек)
✅ Видео сохранено: secret.mp4
```

Декодировать обратно:

```
--- Декодирование видео ---
Путь к видеофайлу: secret.mp4
Папка для сохранения [.]: 
📥 Декодирование: 420 кадров
✅ Найден маркер конца
🔓 Данные расшифрованы
✅ Файл восстановлен: secret.zip
📏 Размер: 5242880 байт
```

---

🔐 Шифрование

```bash
# С шифрованием (рекомендуется)
echo "мой-супер-секретный-ключ-2024" > key.txt
python youtube_storage_fixed.py

# Без шифрования
rm key.txt
python youtube_storage_fixed.py
```

🔑 Ключ хешируется через SHA-256 в 32 байта и используется для XOR-шифрования каждого байта данных

---

🔧 Как это работает

<table>
<tr>
<th>Шаг</th>
<th>Процесс</th>
<th>Детали</th>
</tr>

<tr>
<td align="center">1</td>
<td>📖 <b>Чтение файла</b></td>
<td>Файл читается побайтово в память</td>
</tr>

<tr>
<td align="center">2</td>
<td>🔐 <b>Шифрование</b></td>
<td>XOR каждого байта с ключом из key.txt</td>
</tr>

<tr>
<td align="center">3</td>
<td>🧬 <b>Битизация</b></td>
<td>Байты → биты → группы по 4 бита</td>
</tr>

<tr>
<td align="center">4</td>
<td>🎨 <b>Цветовое кодирование</b></td>
<td>4 бита → 1 из 16 цветов</td>
</tr>

<tr>
<td align="center">5</td>
<td>🖼️ <b>Отрисовка кадров</b></td>
<td>Блоки 24×16 пикселей на холсте 1920×1080</td>
</tr>

<tr>
<td align="center">6</td>
<td>🔄 <b>Дублирование</b></td>
<td>3 копии данных на каждом кадре</td>
</tr>

<tr>
<td align="center">7</td>
<td>🎞️ <b>Сборка видео</b></td>
<td>Все кадры → видеофайл 6 FPS</td>
</tr>

</table>

🎨 Таблица цветов (4 бита = 16 цветов)

<table>
<tr>
<td><code>0000</code></td>
<td bgcolor="#FF0000" width="40"></td>
<td>Красный</td>
<td><code>0001</code></td>
<td bgcolor="#00FF00" width="40"></td>
<td>Зелёный</td>
<td><code>0010</code></td>
<td bgcolor="#0000FF" width="40"></td>
<td>Синий</td>
<td><code>0011</code></td>
<td bgcolor="#FFFF00" width="40"></td>
<td>Жёлтый</td>
</tr>
<tr>
<td><code>0100</code></td>
<td bgcolor="#FF00FF" width="40"></td>
<td>Маджента</td>
<td><code>0101</code></td>
<td bgcolor="#00FFFF" width="40"></td>
<td>Циан</td>
<td><code>0110</code></td>
<td bgcolor="#FF8000" width="40"></td>
<td>Оранжевый</td>
<td><code>0111</code></td>
<td bgcolor="#8000FF" width="40"></td>
<td>Фиолетовый</td>
</tr>
<tr>
<td><code>1000</code></td>
<td bgcolor="#008080" width="40"></td>
<td>Бирюзовый</td>
<td><code>1001</code></td>
<td bgcolor="#808000" width="40"></td>
<td>Оливковый</td>
<td><code>1010</code></td>
<td bgcolor="#800080" width="40"></td>
<td>Пурпурный</td>
<td><code>1011</code></td>
<td bgcolor="#008000" width="40"></td>
<td>Зелёный Т</td>
</tr>
<tr>
<td><code>1100</code></td>
<td bgcolor="#800000" width="40"></td>
<td>Бордовый</td>
<td><code>1101</code></td>
<td bgcolor="#000080" width="40"></td>
<td>Синий Т</td>
<td><code>1110</code></td>
<td bgcolor="#C0C0C0" width="40"></td>
<td>Серый</td>
<td><code>1111</code></td>
<td bgcolor="#FFFFFF" width="40"></td>
<td>Белый</td>
</tr>
</table>

🖼️ Структура кадра

```
┌──────────────────────────────────────────┐
│ ██ Маркер                   ██ Маркер   │
│                                          │
│  🟥🟦🟩🟨🟪⬜🟫⬛  ДАННЫЕ  🟥🟦🟩🟨  │
│  🟥🟦🟩🟨🟪⬜🟫⬛  Область1 🟥🟦🟩🟨  │
│  🟥🟦🟩🟨🟪⬜🟫⬛           🟥🟦🟩🟨  │
│                                          │
│  🟥🟦🟩🟨🟪⬜🟫⬛  ДАННЫЕ  🟥🟦🟩🟨  │
│  🟥🟦🟩🟨🟪⬜🟫⬛  Область2 🟥🟦🟩🟨  │
│  🟥🟦🟩🟨🟪⬜🟫⬛  (дубль)  🟥🟦🟩🟨  │
│                                          │
│ ██ Маркер                   ██ Маркер   │
└──────────────────────────────────────────┘
```

---

📊 Характеристики

<table>
<tr>
<th>Параметр</th>
<th>Значение</th>
</tr>
<tr>
<td>📐 Разрешение</td>
<td>1920 × 1080 (Full HD)</td>
</tr>
<tr>
<td>🎞️ Частота кадров</td>
<td>6 FPS</td>
</tr>
<tr>
<td>🎨 Цветовая палитра</td>
<td>16 цветов (4 бита на блок)</td>
</tr>
<tr>
<td>📦 Размер блока</td>
<td>24 × 16 пикселей</td>
</tr>
<tr>
<td>🔲 Блоков в кадре</td>
<td>~200 блоков</td>
</tr>
<tr>
<td>💾 Данных на кадр</td>
<td>~100 байт</td>
</tr>
<tr>
<td>📁 Максимальный файл</td>
<td>100 МБ</td>
</tr>
<tr>
<td>⚡ Скорость кодирования</td>
<td>~50 КБ/сек</td>
</tr>
</table>

⏱️ Производительность

Файл Кадров Видео Длительность Время кодирования
1 МБ 84 ~3 МБ 14 сек ~20 сек
5 МБ 420 ~15 МБ 70 сек ~100 сек
10 МБ 840 ~30 МБ 140 сек ~200 сек
50 МБ 4200 ~150 МБ 700 сек ~17 мин

---

🎯 Идеи для использования

· ☁️ Облачное хранилище — YouTube как бесплатный хостинг файлов
· 🕵️ Стеганография — спрятать секретные данные в безобидном видео
· 🔐 Шифрованная передача — безопасный обмен через видеохостинги
· 🎨 Цифровое искусство — превратить данные в абстрактные картины
· 💾 Резервное копирование — бэкап важных файлов на YouTube

---

⚠️ Предупреждения

· ❗ Файл увеличивается примерно в 3 раза при кодировании
· ❗ YouTube может дополнительно сжимать видео (учтено тройным дублированием)
· ❗ Цвета могут незначительно искажаться при пережатии
· ❗ Максимальный размер файла: 100 МБ (можно увеличить в настройках)
· ❗ Для больших файлов требуется много свободного места и времени

---

🛡️ Безопасность

Защита Описание
🔐 Шифрование XOR с SHA-256 хешем ключа
🛡️ Path Traversal Защита от выхода за пределы рабочей директории
🧹 Санитизация Очистка имён файлов от опасных символов
📦 Целостность Маркер конца данных + хеш заголовка
🚫 Антивирус Блокировка исполняемых расширений при декодировании

---

🔄 Сравнение с аналогами

 YouTube Cloude Традиционное облако Физический носитель
💰 Цена Бесплатно $5-10/мес $10-50
📦 Объём ∞ (много видео) 15-100 ГБ 32-256 ГБ
🔐 Шифрование Встроенное Отдельно Вручную
🌍 Доступ Из любого браузера Из любого браузера Только физически
⚡ Скорость YouTube CDN CDN провайдера USB 3.0
🎭 Скрытность Выглядит как видео Файлы как файлы Флешка

---

🚧 TODO

· Поддержка 4K разрешения для большей плотности
· Коррекция ошибок Рида-Соломона
· Параллельная обработка кадров
· Поддержка YouTube Shorts формата
· Веб-интерфейс
· Мобильное приложение
· Автоматическая загрузка на YouTube через API

---

🤝 Вклад в проект

<div align="center">

Понравился проект? Поставь звезду! ⭐

https://img.shields.io/github/stars/KorocheVolgin/YouTube-Cloude?style=social

<br>

Нашли баг? Есть идея?

<kbd> 
 🐛 Создать Issue 
 </kbd>
<kbd> 
 🔀 Pull Request 
 </kbd>

</div>

---

👤 Автор

<div align="center">

KorocheVolgin

<br>

https://img.shields.io/badge/GitHub-KorocheVolgin-181717?style=for-the-badge&logo=github

</div>

---

## 👥 Благодарности

- [KorocheVolgin](https://github.com/KorocheVolgin) — автор оригинального проекта [YouTube-Cloude](https://github.com/KorocheVolgin/YouTube-Cloude)
- Этот форк добавляет исправления и улучшения для работы в Termux

---

📄 Лицензия

<div align="center">

```
MIT License

Copyright (c) 2024 KorocheVolgin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

</div>

---

<div align="center">

<br>

⭐ Не забудь поставить звезду, если проект оказался полезным!

<br>

![Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/Uses-OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Termux](https://img.shields.io/badge/Works%20on-Termux-000000?style=for-the-badge&logo=android&logoColor=white)

<br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" width="100%" />

</div>