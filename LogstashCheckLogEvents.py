# Импорт библиотеки регулярок
import re

Events = 0
current_line = ""
# Словарь со списком сообщений и их количеством
message_dict = {}
# Словарь со списком сообщений как выше, но с доп. инфой
add_info_dict = {}

# Функция для парсинга строк на составляющие
def checkAndParse(current_line):
    # Проверка сделана для первой строки лога, когда первая строка в current_line ещё не заполнена полностью
    if current_line != "":
        match_pattern = r'\[\d{4}-\d{2}-\d{2}T\d{2}\:\d{2}\:\d{2}\,\d{3}\]\[(?P<Type>\w+)\]\[(?P<Module>[^\]]+)\]\[\w+\](?P<Error>[\w\W]+?)\n +?\{"source": "(?P<Source>[^"]+)"'
        matches = re.search(match_pattern, current_line)
        Type = matches.group(1).strip()
        Module = matches.group(2).strip()
        Message = matches.group(3).strip()
        Source = matches.group(4).strip()
        # Проверка наличия сообщения в словаре message_dict
        # Если есть - увеличить count, если нет - создать новый ключ и заполнить параметры в словаре add_info_dict
        if (message_dict.get(Message) != None):
            message_dict.update({Message: (message_dict.get(Message) + 1)})
        else:
            message_dict.update({Message: 1})
            add_info_dict.update({Message: "Type: {0}\nModule: {1}\nSource: {2}".format(Type, Module, Source)})

# Открытие локального файла лога логстеша. Файл должен лежать в одной папке со скриптом
file = open("logstash-plain.log", "r", 1, "utf-8")

# Построчное чтение файла. Если строка начинатся с даты - считаем это новой строкой лога, иначе - прицепляем к прошлой
# Для первой строки обработка отдельная, поэтому заранее вызываем функцию checkAndParse
for line in file:
    if (re.match(r'\[\d{4}-\d{2}-\d{2}T\d{2}\:\d{2}\:\d{2}\,\d{3}\]', line)):
        checkAndParse(current_line)
        current_line = ""
        current_line = line + '\n'
        Events += 1
    else:
        current_line += line + '\n'

result_line = ''
i = 0
# Записываем все найденные сообщения в структурированный вид
# Ключи в словарях message_dict и add_info_dict совпадают, отличаются только значения
for key in message_dict:
    i += 1
    result_line += '{0}.\nMessage: {1}\nCount: {2}\n{3}\n\n'.format(i, key, message_dict.get(key), add_info_dict.get(key))
# Выводим структурированные результат в консоль
print("Completed!\nEvents: {0}\n\nMessage list:\n{1}".format(Events, result_line))