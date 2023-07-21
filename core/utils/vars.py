import random


class Variables:

    def __init__(self):
        
        self.used_strings = []

    def random_string(self, str_range: list = None):

        start = "UwU_" + "".join(random.choice("_") for i in range(random.randint(0,3)))
        base = "UwuWOo0_"

        while True:

            if str_range == None:
                string = start + "".join(random.choice(base) for i in range(random.randint(15,40)))
            else:
                string = start + "".join(random.choice(base) for i in range(random.randint(str_range[0],str_range[1])))

            if not string in self.used_strings:
                self.used_strings.append(string)
                return string