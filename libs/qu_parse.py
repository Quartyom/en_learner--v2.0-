# organizes methods and call them by their name, args count
# _[method_name] is hidden, can only be called from execute(), not prepare()
# methods execution result is in get_result()
# keep temporary(!) data in  _method_to_method_data (unsafe)

class Qu_parse:
    def __init__(self):
        self.is_active = True
        self._methods = {}
        self._methods_k_args = {}
        self._result = str(), str()
        self._method_to_method_data = None  # unsafe

    def method(self, name, k = None, k_to = None):
        def wrap(func):
            if name in self._methods: raise Exception(f'function "{name}": multiple initialisation is unavilable')
            self._methods[name] = func
            self._k_args(func, k, k_to)
            return func
        return wrap

    def _k_args(self, func, k = None, k_to = None):
        if type(k) == int:
            if k_to == None: k_to = k
            self._methods_k_args[func] = { "k" : k, "k_to" : k_to }

    def k_args(self, k = None, k_to = None):
        def wrap(func):
            self._k_args(func, k, k_to)
            return func
        return wrap

    #finds an apropriate method, calls it
    def execute(self, name, *args):
        if name in self._methods:
            func = self._methods[name]

            if func in self._methods_k_args: # limitations for args ammount
                limits = self._methods_k_args[func]

                if len(args) < limits["k"]:
                    self.set_result("error", "too little arguments")
                elif len(args) > limits["k_to"]:
                    self.set_result("error", "too much arguments")
                else:
                    func(*args)

            else:
                func(*args)

        else:
            self.set_result("error", "method is not found")

    def prepare_func(self):
        def wrap(func):
            self.prepare = func
            return func
        return wrap

    # gets input, calls execute()
    def prepare(self, inp_str = None):
        if not inp_str: inp_str = input(">>> ")
        inp = inp_str.strip().split()

        if inp:
            if (inp[0][0] == "_"): # hidden methods
                self.set_result("error", "method is not found")
            else:
                self.execute(inp[0], *inp[1::])
                if not self._result[0]: self._result = "success", self._result[1]
        else:
            self.set_result("error", "empty input")

    def get_result(self, to_save_result = False):
        outp = self._result
        if not to_save_result: self._result = str(), str()
        return outp

    def set_result(self, resl_type, resl_msg):
        self._result = resl_type, resl_msg

    def _get_method_to_method_data(self, to_save = False):
        outp = self._method_to_method_data
        if not to_save: self._method_to_method_data = None
        return outp

    def _set_method_to_method_data(self, data):
        self._method_to_method_data = data
