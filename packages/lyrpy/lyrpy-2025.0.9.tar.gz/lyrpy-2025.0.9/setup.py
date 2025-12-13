# Импорт недавно установленного пакета setuptools.
import setuptools
import configparser  # импортируем библиотеку

# Открытие README.md и присвоение его long_description.
with open("README.md", "r") as fh:
    long_description = fh.read()

config = configparser.ConfigParser() # создаём объекта парсера
config.read(r'D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\TOOLS_SRC_PY\lyrpy.ini')  # читаем конфиг
# print (config.sections())
# print(config.get('general','name'))
# print(config.get('general','version'))
# print(config['general']['name'])  # обращаемся как к обычному словарю!
# print(config['general']['version'])  # обращаемся как к обычному словарю!

# Имя дистрибутива пакета. Оно должно быть уникальным, поэтому добавление вашего имени пользователя в конце является обычным делом.
# Gname=config.get('general','name')
Gname=config['general']['name']
print(Gname)
# Номер версии вашего пакета. Обычно используется семантическое управление версиями.
# Gversion=config.get('general','version')
Gversion=config['general']['version']
print(Gversion)

# Определение requests как requirements для того, чтобы этот пакет работал. Зависимости проекта.
# requirements = ["requests<=2.21.0"]

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setuptools.setup(
    # Имя дистрибутива пакета. Оно должно быть уникальным, поэтому добавление вашего имени пользователя в конце является обычным делом.
    name=Gname,
    # Номер версии вашего пакета. Обычно используется семантическое управление версиями.
    version=Gversion,
    # Имя автора.
    # author="lisitsinyr",
    # Его почта.
    # author_email="lisitsinyr@gmail.com",
    # Краткое описание, которое будет показано на странице PyPi.
    # description="lyrpy",
    # Длинное описание, которое будет отображаться на странице PyPi. Использует README.md репозитория для заполнения.
    # long_description="lyrpy",
    # Определяет тип контента, используемый в long_description.
    long_description_content_type="text/markdown",
    # URL-адрес, представляющий домашнюю страницу проекта. Большинство проектов ссылаются на репозиторий.
    url="https://github.com/lisitsinyr/TOOLS_SRC_PY",

    # Находит все пакеты внутри проекта и объединяет их в дистрибутив.
    # packages=setuptools.find_packages(),

    # Включить данные из MANIFEST.in
    # include_package_data=True,  # Включить данные из MANIFEST.in

    # package_data={
    #     # Если include_package_data=True, это дополнительно
    #     'lyrpy': ['*.json', '*.txt', 'data/*', 'templates/*.html', 'DOC/*.bat']
    # },
    # data_files=[
    #     ('config', ['config/settings.cfg']),
    #     ('docs', ['docs/README.md']),
    # ],

    # data_files=[
    #     ('config', ['config/*']),
    #     ('docs', ['docs/*']),
    # ],

    # package_data={
    #     'lyrpy': [
    #         '*.json',           # JSON файлы
    #         '*.yaml',           # YAML файлы
    #         'data/*.csv',       # CSV файлы
    #       'templates/*.html', # HTML шаблоны
    #         'static/css/*.css', # CSS файлы
    #         'static/js/*.js',   # JavaScript файлы
    #         'images/*.png',     # Изображения
    #         'models/*.pkl',     # Модели ML
    #     ]
    # },
    # data_files=[
    #     ('config', ['config/app.conf']),
    #     ('docs', ['README.md', 'CHANGELOG.md']),
    # ],

    # requirements или dependencies, которые будут установлены вместе с пакетом, когда пользователь установит его через pip.
    # install_requires=requirements,
    
    # Предоставляет pip некоторые метаданные о пакете. Также отображается на странице PyPi.
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # Требуемая версия Python.
    python_requires='>=3.13',
)
