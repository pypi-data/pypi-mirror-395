"""
@author: M. Bernt
"""


class ParmFileNotExists(Exception):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.type = type

    def __str__(self):
        return "file %s passed as file paramter %s does not exist\n" % (
            repr(self.value),
            repr(self.name),
        )


class ParmValueError(Exception):
    def __init__(self, name, value, tpe):
        self.name = name
        self.value = value
        self.type = tpe

    def __str__(self):
        return "paramter %s = %s can not be passed as %s:\n" % (
            repr(self.name),
            repr(self.value),
            repr(self.tpe),
        )


class ParmRangeTypeError(Exception):
    def __init__(self, rng):
        self.range = rng

    def __str__(self):
        return "range must be given as list or tuple, but is %s\n" % repr(
            type(self.rng)
        )


class ParmRangeError(Exception):
    def __init__(self, rng, value):
        self.range = rng
        self.value = value

    def __str__(self):
        return "value %s not in %s\n" % repr(repr(self.value), type(self.range))


class StderrError(Exception):
    def __init__(self, prog, stderr):
        self.prog = prog
        self.stderr = stderr

    def __str__(self):
        return "%s has returned an error message:\n %s\n" % (
            repr(self.prog),
            repr(self.stderr),
        )


class cmdline:
    """
    class for wrapping command line parameters
    """

    def __init__(self, kw, param, param2=[]):
        """
        @param kw a dictionary of parameter value pairs
        @param param possible parameters
        @param param2 another list of possible parameters
        """
        self.__kw = kw
        self.__param = param
        self.__param += param2
        for p in self.__param:
            if p.getname() in list(self.__kw.keys()):
                self.__kw[p.getname()] = p.retype(self.__kw[p.getname()])

    def get(self, key):
        return self.__kw.get(key)

    def __str__(self):
        cl = ""
        for p in self.__param:
            if p.getname() in list(self.__kw.keys()):
                cl += p.render(self.__kw[p.getname()])

        return cl

    def __repr__(self):
        return self.__str__()


class parm:
    """
    class for wrapping command line parameters
    """

    def __init__(self, name, tpe, rng=[], infix=" "):
        """
        initialise one parameter
        param name the name of the parameter
        param tpe type of the parameter (bool, int, str, float, flag)
        param rng range of valid values; if [] everything is allowed
        """
        self.prefix = "-"
        self.infix = infix
        self.__true = " 1"
        self.__false = " 0"

        if name[0] == "_":
            self.__name = name[1:]
        else:
            self.__name = name
        self.__type = tpe
        if isinstance(rng, tuple) or isinstance(rng, list):
            self.__range = rng
        else:
            raise ParmRangeTypeError(rng)

        # tuples with more than 2 entries are interpreted like/as list
        if isinstance(self.__range, tuple) and len(self.__range) > 2:
            self.__range = [t for t in self.__range]

    def chkvalue(self, value):
        """
        check if a value is of (or can be used as) type 'specified by' __type
        """
        try:
            if self.__type == "int":
                value = int(value)
            elif self.__type == "str" or self.__type == "file":
                value = str(value)
            elif self.__type == "float":
                value = float(value)
            elif self.__type == "bool" or self.__type == "flag":
                value = bool(value)
        except Exception:
            raise ParmValueError(self.__name, value, self.__type)

        # if self.__type == 'file' and not os.path.exists(value):
        #    raise ParmFileNotExists(self.__name, value )

        return value

    def chkrange(self, value):
        """
        check if value is in range
        @param value the value to check
        """
        if len(self.__range) > 0:
            if isinstance(self.__range, tuple):
                for t in self.__range():
                    self.chkvalue(t)
                if not (self.__range[0] <= value and value <= self.__range[1]):
                    raise ParmRangeError(value, self.__range)

            elif isinstance(self.__range, list):
                for t in self.__range:
                    t = self.chkvalue(t)
                if value not in self.__range:
                    raise ParmRangeError(value, self.__range)

    def getname(self):
        return self.__name

    def render(self, value):
        """
        get the command line for this parameter
        """

        try:
            # sane value ?
            value = self.chkvalue(value)
            # valid value
            self.chkrange(value)
        except Exception as inst:
            print(inst)

        #        print "render", self.__name, self.__type, value
        if self.__type == "flag":
            if value:
                return "%s%s " % (self.prefix, self.__name)
            else:
                return ""
        if self.__type == "bool":
            if value:
                return "%s%s%s%s " % (self.prefix, self.__name, self.infix, self.__true)
            else:
                return "%s%s%s%s " % (
                    self.prefix,
                    self.__name,
                    self.infix,
                    self.__false,
                )
        else:
            return "%s%s%s%s " % (self.prefix, self.__name, self.infix, str(value))

    def retype(self, value):
        """
        given a value the function will return a value of type specified by type
        """
        #        try:
        # sane value ?
        value = self.chkvalue(value)
        # valid value
        self.chkrange(value)

        #        except Exception, inst:
        #            print inst

        return value


# short option -param X
class shortparm(parm):
    def __init__(self, name, tpe, rng=[]):
        parm.__init__(self, name, tpe, rng)
        self.infix = " "
        self.prefix = "-"


# long option --param X


class longparm(parm):
    def __init__(self, name, tpe, rng=[]):
        parm.__init__(self, name, tpe, rng)
        self.infix = " "
        self.prefix = "--"
