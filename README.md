# Утила мониторинга сайтов

Скрипт проверяет работоспособность сайта и время до продления домена.

* Если сервер дает ответ `200` - True, в других случая False
* Если до конца аренды домена меньше 31 дня, вы получите False, в другом случае True

# Как работает 
```bash
$ python check_sites_health.py domains.txt
 
Домен                          | Ответ сервера | Проплачено более |
                                    HTTP 200          месяца
https://amazon.com             |     False     |       True       |
https://fbcdn.net              |     True      |       True       |
https://windowsupdate.com      |     False     |       True       |
https://mookie1.com            |     False     |      False       |
https://rfihub.com             |     False     |       True       |
......
```
# Требования
Совестимые OC:
* Linux,
* Windows
* MacOS

Скрипт требует для своей работы установленного интерпретатора Python версии 3.5 выше

И  пакетов из requirements.txt
```bash
pip install -r requirements.txt # или командой pip3
```

Список доменов должен быть в файле .txt. Каждый домен с новой строки.


# Как запустить
Стандатной командой `python` (на некоторых компьютерах `python3`)

```bash
$ python check_sites_health.py [-h] file_path

positional arguments:
  file_path   Адрес файла с доменами

optional arguments:
  -h, --help  show this help message and exit
```
> Запуск для всех ОС одинаковый

Помните, рекомендуется использовать [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) для лучшего управления пакетами.

# Цели проекта
Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)