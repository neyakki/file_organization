# File Organizer CLI

CLI утилита для организации файлов в указанной директории.

---

## Описание проекта

Python утилита для автоматической сортировки и перемещения файлов в указанной директории. Настройки считываются из конфигурационного файла формата **json**.

Пример:

```json
{
    "formats": {
        "tables": [".xlsx"]
        ....
    }
}
```

## Стек технологий

- Python 3.x
- argparse, os, pathlib, shutil, json, logging

## Запуск

Можно скачать утилиту `wget https://github.com/neyakki/file_organization/releases/download/v1.0.3/file_organizer.tar.gz`

И разархивировать в любое удобное место командой `tar xvf file_organizer.tar.gz`

Утилита уже собрана в исполняемый файл

## Установка и запуск из исходников

1. Скачать репозиторий к себе на ПК `git clone git@github.com:neyakki/file_organization.git`
2. Установите зависимости: `poetry install`
3. Запустите утилиту с помощью команды make: `poetry run file_organizer`

## Доступные опции утилиты

```plaintext
$ poetry run file_organizer -h
usage: FileOrganizer [-h] [--target-dir TARGET_DIR] [--recursive [RECURSIVE]] [--config-file CONFIG_FILE]

Утилита позволяет организовывать файлы в определенной папке, согласно заданным правилам

options:
  -h, --help            show this help message and exit
  --target-dir TARGET_DIR
                        Директория, в которой происходит сортировка. По умолчанию текущая директория
  --recursive [RECURSIVE]
                        Рекурсивный обход директории
  --config-file CONFIG_FILE
                        Путь к файлу конфигурации
```
