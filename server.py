import socket

from libFS import FormatServer 

fs = FormatServer()

fs.addFormat("BBBB", "Номер участника")
fs.addFormat("x", "Пробельный символ")
fs.addFormat("NN", "id канала")
fs.addFormat("HH", "Часы")
fs.addFormat("MM", "Минуты")
fs.addFormat("SS", "Секунды")
fs.addFormat("zhq", "Десятые, сотые, тысячные", 1) #Тут бы я всё же реализовал через раздбиение данной маски на отдельный элементы, но делаем строго по ТЗ
fs.addFormat("GG", "Номер группы")
fs.addFormat("CR", "Возврат каретки")
fs.setInpFormat("BBBBxNNxHH:MM:SS.zhqxGGCR")
fs.setOutFormat("Спортсмен, нагрудный номер BBBB прошёл отсечку NN в HH:MM:SS.zhq")
fs.setCondition("GG", 1, "00")
print("Установлены настройки необходимые для ТЗ!")

while True:
    print('Введите число необходимой команды:\n'
            '1. Запустить сервер!\n'
            '2. Изменить настройки')
    com = int(input("Номер команды: "))
    if com == 1:
        break
    elif com == 2:
        while True:
            print('Введите число необходимой команды:\n'
                    '1. Добавить новую маску\n'
                    '2. {0} входящий формат данных\n'
                    '3. {1} исходящий формат данных\n'
                    '4. Обновить путь до файла логов!\n'
                    '5. Установить условие для вывода!\n'
                    '6. Вернуться'.format("Ввести" if len(fs.inptxt) == 0 else "Обновить", "Ввести" if len(fs.out) == 0 else "Обновить"))
            com = int(input("Номер команды: "))
            if com == 1:
                m_id = ""
                while not m_id:
                    m_id = input("Введите наименование маски: ")
                    if not m_id:
                        print("Маска должна содержать хотябы 1 символ!")
                    elif fs.findFormat(m_id):
                        print("Подобная маска уже используется! Введите другую!")
                        m_id = ""
                desc = input("Введите описание маски (можно оставить пустым): ")
                out = input("Если хотите, чтобы маска постоянно заменялась на один и тот же символ, то введите его (можно оставить пустым): ")
                fs.addFormat(m_id, None if not desc else desc, None if not out else out)
            elif com == 2:
                fs.inpFormat()
            elif com == 3:
                fs.outFormat()
            elif com == 4:
                fs.updateFile()   
            elif com == 5:
                fs.updateCondition()    
            elif com == 6:
                break
            else:
                print("Ошибка ввода данных!")
    else:
        print("Ошибка ввода данных!")

print("Запускаем сервер..")

mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
buffer_size = 1024
mysocket.bind(('127.0.0.1', 9879))
mysocket.listen(5)

print("Сервер запущен!")

while True:
    (client, (ip,port)) = mysocket.accept()
    data = client.recv(buffer_size).decode()
    fs.formating(data)
mysocket.close()

print("Сервер остановлен!")




print("Настройки установлены в режим необходимый для ТЗ")
