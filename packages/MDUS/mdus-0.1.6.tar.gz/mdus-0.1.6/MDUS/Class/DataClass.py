class Data:
    def __init__(self):
        self.info = {}
        self.value = None
    def Info(self):
        if len(self.info) == 0:
            print("No Data")
        else:
            for key in self.info:
                if key == "Data Type":
                        print("\033[31m" + key + "\033[0m")
                        print("\t" + str(self.info[key]))
                else:
                    if type(self.info[key]) == list:
                        print("\033[34m" + key + "\033[0m")
                        for value in self.info[key]:
                            print("\t" + str(value))
                    else:
                        print("\033[34m" + key + "\033[0m")
                        print("\t" + str(self.info[key]))