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
            elif not self.findFormat(m_id): 
                print("Такая маска не найден!")
                m_id = ""
        print('Выберите номер условия: \n'
                '1. Равно\n'
                '2. Не равно\n'
                '3. Больше или равно\n'
                '4. Меньше или равно\n'
                '5. Строго больше\n'
                '6. Строго меньшн')
        num_cond = int(input("Номер: "))
        elem = input('Введите элемент для условия: ')
        self.setCondition(m_id, num_cond, elem)

    def setCondition(self, m_id, num_cond, elem):
        self.condition["id"] = m_id
        self.condition["num_cond"] = num_cond
        self.condition["elem"] = elem

    def addFormat(self, m_id, desc=None, out=None, reduc=None):
        self.formats.append({
            "id": m_id,
            "desc": "Описание отсутствует" if desc is None else desc,
            "out": out,
            "reduc": reduc
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
        if len(self.inptxt) != 0:
            print("Текущий входящий формат данных: '{0}'".format(self.inptxt))
            txt = input("Обновлённые входящие данные будут выглядет так: ")
        else:
            txt = input("Входящие данные будут выглядет так: ")
        self.setInpFormat(txt)

    def setInpFormat(self, txt):
        self.inptxt = txt
        self.resetInpmask()

    def outFormat(self):
        print("Допустимые маски: ")
        if len(self.formats) == 0:
            print("Маски отсутствуют")
        else:
            for f in self.formats:
                print("{0} - {1}".format(f["id"], f["desc"]))
        if len(self.out) != 0:
            print("Текущий исходящий формат данных: '{0}'".format(self.out))
            txt = input("Обновлённые исходящие данные будут выглядет так: ")
        else:
            txt = input("Исходящие данные будут выглядет так: ")
        self.setOutFormat(txt)

    def setOutFormat(self, txt):
        self.out = txt

    def logging(self, text):
        my_file = open(self.filedata, 'a', encoding="utf-8")
        my_file.write(text+"\n")
        my_file.close()

    def getFormats(self):
        new_formats = []
        for f in self.formats:
            new_formats.append(dict(f))
        return new_formats

    def formating(self, text):
        ff = self.getFormats()
        ind = 0
        for i in self.inpmask:
            m_id = i[1] 
            if m_id != -1 and ff[m_id].get("out", None) is None:
                txt = text[ind:ind+i[0]]
                if ff[m_id]["reduc"] is not None:
                    ff[m_id]["out"] = txt[0:int(ff[m_id]["reduc"])]
                else:
                    ff[m_id]["out"] = txt
            ind+=i[0]
        t = self.out
        for f in ff:
            if f.get("out", None) is not None:
                t = re.sub(str(f["id"]), str(f["out"]), t)
        if self.cond(ff): 
            print(t)
        self.logging(t)