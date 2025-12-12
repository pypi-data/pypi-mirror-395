import regex as re


class ParameterHelper:
    floatRe = re.compile(r"^[\d\.\-\+e]+$")
    intRe = re.compile(r"^\d+$")
    splitRe = re.compile(r"[ \t,]+")
    quotation = re.compile(r"^'(.*)'$")

    def __init__(self, parameters):
        if not isinstance(parameters, dict):
            raise Exception("Parameter argument must be of type dict")
        self.parameters = parameters

    @classmethod
    def isNumeric(cls, value):
        vtype = "str"
        if cls.floatRe.match(str(value)):
            if cls.intRe.match(str(value)):
                try:
                    value = int(value)
                    vtype = "int"
                except:
                    pass
            else:
                try:
                    value = float(value)
                    vtype = "float"
                except:
                    pass
        return value, vtype

    @classmethod
    def removeUnit(cls, value):
        if value == None:
            return "-"
        if not isinstance(value, str):
            return value
        v = cls.splitRe.split(value)
        v, _ = cls.isNumeric(v[0])
        return v

    def get(self, key, removeUnit=False):
        if key in self.parameters:
            if isinstance(self.parameters[key], list):
                return self.parameters[key]

            value = self.parameters[key]
            if isinstance(value, str):
                match = self.quotation.match(value)
                if match:
                    value = match.group(1)
            if removeUnit:
                value = self.removeUnit(value)
            return value
        return None
