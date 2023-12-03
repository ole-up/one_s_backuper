# Включение логгирования
LOG = True

# Пользователь кластера
CLUSTER_USER = 'Администратор'

# Пароль пользователя кластера
CLUSTER_PASSWORD = 'test'

# Код блокировки базы (на время выгрузки)
PERMISSION_CODE = 'testt'

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
YADISK_UPLOAD = False

# Сохранять выгруженный бэкап папку для бэкапа
SAVE_BACKUP_ON_LOCAL_DISK = True

# Токен Я.Диска
YADISK_TOKEN = 'y0_AgAEA7qkULv3AAkNfQAAAADi9pRMF2Veau_LQQKv-cRhId4uKf6kADk'

# В какую папку на Я.Диске выгружать бэкап
YADISK_FOLDER = 'test'

# Список имен баз, для которых не нужно выгружать бэкап
# EXCLUDE_BASE = ['test', 'buh', 'zup' ]
EXCLUDE_BASE = ['sogl', 'gsz_ut', 'gsz_buh', 'test2']

# Сколько дней хранить бэкапы. Если 0, то будут хранится все бэкапы
HOW_LONG_KEEP_BACKUP = 14

# Сохранять или нет бэкапы на начало квартала
KEEP_QUARTERLY_BACKUP = True

# Выключать компьютер по завершению бэкапа или нет
SHUTDOWN_AFTER_BACKUP = False
