import inspect


class Exercise:
    def __init__(self, name: str, number_measures: int):
        self.name = name
        self.number_measures = number_measures

    def record(self):
        return self.name, self.number_measures

    def create_columns_string(self):
        type_conversion_dict = {"str": "TEXT", "int": "INT", "float": "REAL"}
        parameter_dict = inspect.signature(self.__init__).parameters
        columns_string = ""
        for parameter in parameter_dict:
            columns_string += parameter
            column_type = str(parameter_dict[parameter]).split(":")[1].strip()
            columns_string += f" {type_conversion_dict[column_type]}, "
        return columns_string[:-2]


