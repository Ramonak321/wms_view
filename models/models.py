import json

class Status:
    __data = (
        "запланирован",
        "собирается",
        "выписка_документов",
        "отобран",
        "отгружен",
        "отменен",
    )

    def __init__(self, number: int):
        self.__value = self.__data[number]

    def value(self):
        return self.__value

    def find_index(self, value: str):
        if value.lower() in self.__data:
            return self.__data.index(value)


class Selection:
    def __init__(self, number: str, order: str, status=Status(0)):
        self.__number = number
        self.__status = status
        self.__order = order

    def status(self):
        return self.__status.value()

    def change_status(self, status):
        self.__status = Status(self.__status.find_index(status))

    def number(self):
        return self.__number

    def view(self):
        return {
            "ордер": self.__number,
            "заказ": self.__order,
            "статус": self.__status.value(),
        }


class Selections:
    def __init__(self):
        self.__data = dict()
        self.__path = "./bd/selections.json"

    def add(self, selection: Selection):
        self.__data[selection.number()] = selection

    def remove(self, number: str):
        del self.__data[number]

    def selection(self, number: str):
        if number in self.__data.keys():
            return self.__data[number]
        

    def api(self):
        return self.__data

    def view(self):
        return dict(
            (selection, self.selection(selection).view())
            for selection in self.__data.keys()
        )

    def save(self):
        with open(self.__path, "w", encoding="utf-8") as f:
            json.dump(self.view(), f, indent=4, ensure_ascii=False)

    def load(self):
        try:
            with open(self.__path, "r") as f:
                data = json.load(f)

            if data:
                self.__data = {}
                for number in data.keys():
                    s = data[number]
                    selection = Selection(number = s["ордер"], order = s["заказ"], status = Status(Status(0).find_index(s["статус"])))
                    self.add(selection)
        except:
            pass



class Union_selection:
    def __init__(self, number: str, numbers_selection, status=Status(0)):
        self.__number = number
        self.__numbers_selection = numbers_selection
        self.__status = status

    def status(self):
        return self.__status.value()

    def change_status(self, selections:Selections, status):
        self.__status = Status(self.__status.find_index(status))
        for number_selection in self.__numbers_selection:
            if selections.selection(number_selection):
                selections.selection(number_selection).change_status(status)

    def number(self):
        return self.__number

    def view(self):
        return {
            "ордер": self.__number,
            "ордера": self.__numbers_selection,
            "статус": self.__status.value(),
        }


class Union_selections:
    def __init__(self):
        self.__data = dict()
        self.__path = "bd/union_selections.json"

    def add(self, union_selection: Union_selection):
        self.__data[union_selection.number()] = union_selection

    def remove(self, number: str):
        del self.__data[number]

    def union_selection(self, number: str):
        return self.__data[number]

    def api(self):
        return self.__data

    def view(self):
        return dict(
            (union_selection, self.union_selection(union_selection).view())
            for union_selection in self.__data.keys()
        )

    def save(self):
        with open(self.__path, "w", encoding="utf-8") as f:
            json.dump(self.view(), f, indent=4, ensure_ascii=False)

    def load(self):
        try:
            with open(self.__path, "r") as f:
                data = json.load(f)

            if data:
                self.__data = {}
                for number in data.keys():
                    s = data[number]
                    selection = Selection(number = s["ордер"], order = s["ордера"], status = Status(Status(0).find_index(s["статус"])))
                    self.add(selection)
        except:
            pass

