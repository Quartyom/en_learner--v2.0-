# организует функции и их вызов по имени и числу аргументов
# prepare() возвращает True в случае успешного выполнения, иначе False
# результат выполнения функции можно прочитать из get_message()

class Qu_parse:
    def __init__(self):
        self.is_active = True
        self._methods = {}
        self._methods_k_args = {}
        self._result = str(), str()
        self._method_to_method_data = None  # unsafe

    def method(self, name, k = None, k_to = None):
        def wrap(func):
            self._methods[name] = func
            if k or k_to:
                self._k_args(k, k_to, func)
            return func
        return wrap

    def k_args(self, k, k_to = None):
        def wrap(func):
            self._k_args(k, k_to, func)
            return func
        return wrap

    def _k_args(self, k, k_to, func):
        if k_to:
            self._methods_k_args[func] = { "k" : k, "k_to" : k_to }
        else:
            self._methods_k_args[func] = { "k" : k }

    def execute(self, name, *args):
        if name in self._methods: # есть ли метод в обработчике
            func = self._methods[name]

            if func in self._methods_k_args: # установлены ли ограниения на кол-во аргументов
                limits = self._methods_k_args[func]

                if "k_to" in limits:
                    if len(args) < limits["k"]:
                        self.set_result("error", "too_little_arguments")
                    elif len(args) > limits["k_to"]:
                        self.set_result("error", "too_much_arguments")
                    else:
                        func(*args)

                else:
                    if len(args) == limits["k"]:
                        func(*args)
                    else:
                        self.set_result("error", "wrong_number_of_arguments")

            else:
                func(*args)

        else:
            self.set_result("error", "method_not_found")

    def prepare_method(self, func):
        self.prepare = func

    def prepare(self, inp_str = None):
        if not inp_str: inp_str = input(">>> ")
        inp = inp_str.strip().split()

        if inp:
            self.execute(inp[0], *inp[1::])
        else:
            self.set_result("error", "empty_input")

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

    def set_method_to_method_data(self, data):
        self._method_to_method_data = data
