import socket
import re

class FormatServer:

    formats = []
    inptxt = ""
    inpmask = []
    out = ""
    condition = {
        "id": "",
        "num_cond": 0,
        "elem": 0
    }
    filedata = "./out.txt"

    def updateFile(self):
        print("Сейчас логи сохраняются тут: '{0}'".format(self.filedata))
        fd = input("Новый пусть до файла (если оставить пустым, то будет использоваться старый путь): ")
        if fd: self.filedata = fd

    def cond(self, formats):
        if not self.condition["id"]:
            return True
        for f in formats:
            if self.condition["id"] == f["id"]:
                out = f.get("out", None)
                if out is None:
                    return False
                if self.condition["num_cond"] == 1: # ==
                    return True if out == self.condition["elem"] else False
                elif self.condition["num_cond"] == 2: # !=
                    return True if out != self.condition["elem"] else False
                elif self.condition["num_cond"] == 3: # >=
                    return True if out >= self.condition["elem"] else False
                elif self.condition["num_cond"] == 4: # <=
                    return True if out <= self.condition["elem"] else False
                elif self.condition["num_cond"] == 5: # >
                    return True if out > self.condition["elem"] else False
                elif self.condition["num_cond"] == 6: # <
                    return True if out < self.condition["elem"] else False
        else:
            return False 

    def updateCondition(self):
        m_id = ""
        while not m_id:
            m_id = input("Введите наименование маски для условия: ")
            if not m_id:
                print("Маска должна содержать хотябы 1 символ!")
            elif not fs.findFormat(m_id): 
                print("Такая маска не найден!")
                m_id = ""
        self.condition["id"] = m_id
        print('Выберите номер условия: \n'
                '1. Равно\n'
                '2. Не равно\n'
                '3. Больше или равно\n'
                '4. Меньше или равно\n'
                '5. Строго больше\n'
                '6. Строго меньшн')
        self.condition["num_cond"] = int(input("Номер: "))
        self.condition["elem"] = int(input('Введите число для условия: '))

    def addFormat(self, m_id, desc=None, out=None):
        self.formats.append({
            "id": m_id,
            "desc": "Описание отсутствует" if desc is None else desc,
            "out": out
        })
        if self.inptxt:
            self.resetInpmask()

    def findFormat(self, ff):
        for f in self.formats:
            if ff in f["id"]:
                return True
        return False

    def resetInpmask(self):
        inp = self.inptxt
        self.inpmask = []
        for k, i in enumerate(self.formats, 0):
            inp = inp.replace(i["id"], str(k))
        for i in inp:
            if i.isdigit():
                self.inpmask.append((len(self.formats[int(i)]["id"]), int(i)))
            else:
                self.inpmask.append((len(i), -1))

    def inpFormat(self):
        print("Допустимые маски: ")
        if len(self.formats) == 0:
            print("Маски отсутствуют")
        else:
            for f in self.formats:
                print("{0} - {1}".format(f["id"], f["desc"]))
        if len(fs.inptxt) != 0:
            print("Текущий входящий формат данных: '{0}'".format(self.inptxt))
            self.inptxt = input("Обновлённые входящие данные будут выглядет так: ")
        else:
            self.inptxt = input("Входящие данные будут выглядет так: ")
        self.resetInpmask()

    def outFormat(self):
        print("Допустимые маски: ")
        if len(self.formats) == 0:
            print("Маски отсутствуют")
        else:
            for f in self.formats:
                print("{0} - {1}".format(f["id"], f["desc"]))
        if len(fs.out) != 0:
            print("Текущий исходящий формат данных: '{0}'".format(self.out))
            self.out = input("Обновлённые исходящие данные будут выглядет так: ")
        else:
            self.out = input("Исходящие данные будут выглядет так: ")

    def logging(self, text):
        my_file = open(self.filedata, 'a')
        my_file.write(text+"\n")
        my_file.close()

    def formating(self, text):
        ff = self.formats
        ind = 0
        for i in self.inpmask:
            m_id = i[1] 
            if m_id != -1 and ff[m_id].get("out", None) is None:
                ff[m_id]["out"] = text[ind:ind+i[0]]
            ind+=i[0]
        t = self.out
        for f in ff:
            if f.get("out", None) is not None:
                t = re.sub(f["id"], f["out"], t)
        if self.cond(ff): print(t)
        self.logging(t)

fs = FormatServer()

while True:
    print('Введите число необходимой команды:\n'
            '1. Добавить новую маску\n'
            '2. {0} входящий формат данных\n'
            '3. {1} исходящий формат данных\n'
            '4. Обновить путь до файла логов!\n'
            '5. Установить условие для вывода!\n'
            '6. Запустить сервер!\n'
            '0. Тест'.format("Ввести" if len(fs.inptxt) == 0 else "Обновить", "Ввести" if len(fs.out) == 0 else "Обновить"))
    i = int(input("Номер команды: "))
    if i == 1:
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
    elif i == 2:
        fs.inpFormat()
    elif i == 3:
        fs.outFormat()
    elif i == 4:
        fs.updateFile()   
    elif i == 5:
        fs.updateCondition()    
    elif i == 6:
        if len(fs.inptxt) == 0:
            print("Сначала введите входящий формат данных!")
        elif len(fs.out) == 0:
            print("Сначала введите исходящий формат данных!")
        else:
            break
    elif i == 0:
        fs.formating(input("Входные данные: "))
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