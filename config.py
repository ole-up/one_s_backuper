# Пользователь кластера
CLUSTER_USER = 'Администратор'

# Пароль пользователя кластера
CLUSTER_PASSWORD = 'test'

# Список пользователей БД ('название базы': {'имя пользователя': 'пароль'})
# INFOBASES_USER = {
#     'test': {'Администратор': 'test'},
#     'buh': {'Администратор': '1234'}
# }
INFOBASES_USER = {
    'test': {'Администратор': 'test'}
}

# Пользователь БД по умолчанию (используется, если имя базы не найдено в списке
# пользовтелей БД (см. параметр выше)
DEFAULT_INFOBASE_USERNAME = 'Администратор'

# Пароль пользователя БД по умолчанию
DEFAULT_INFOBASE_PASSWORD = 'test'

# Адрес сервера 1С
ONE_S_SERVER = 'localhost'

# Папка для формирования бэкапов
BACKUP_FOLDER = 'c:\\backup'

# Делать выгрузку на Я.Диск или нет
YADISK_UPLOAD = True

# Сохранять выгруженный бэкап после загрузки на Я.Диск или нет
SAVE_BACKUP_AFTER_YADISK_UPLOAD = False

# Токен Я.Диска
YADISK_TOKEN = 'y0_AgAEA7qkULv3AAjxkwAAAADXvzixOf0e6LtFT4eSyoZWe8fFUQUj9VU'

# В какую папку на Я.Диске выгружать бэкап
YADISK_FOLDER = 'test'

# Список имен баз, для которых не нужно выгружать бэкап
# EXCLUDE_BASE = ['test', 'buh', 'zup' ]
EXCLUDE_BASE = []

# Сколько дней хранить бэкапы. Если 0, то будут хранится все бэкапы
HOW_LONG_KEEP_BACKUP = 14

# Сохранять или нет бэкапы на начало квартала
KEEP_QUARTERLY_BACKUP = True

# Выключать компьютер по завершению бэкапа или нет
SHUTDOWN_AFTER_BACKUP = False
