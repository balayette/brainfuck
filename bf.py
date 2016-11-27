from time import sleep
from os import system


class Stack:
    def __init__(self):
        self.hidden_list = []

    def push(self, el):
        self.hidden_list.append(el)

    def pop(self):
        if self.length() > 0:
            return self.hidden_list.pop()
        else:
            return -1

    def last(self):
        return self.hidden_list[-1]

    def length(self):
        return len(self.hidden_list)


class BrainfuckInterpreter:
    def __init__(self, bf_script):
        self.bf_script = bf_script
        self.op_list = []
        self.memory_state = [0]
        self.ptr = 0
        self.script_index = -1
        self.output_buffer = []
        self.loop_stack = Stack()
        self.terminated = False
        self.wrapping = False
        self.op_count = 0
        self.op_actions = {
            "+": self.increment_value,
            "-": self.decrement_value,
            ">": self.increment_ptr,
            "<": self.decrement_ptr,
            ".": self.add_output,
            ",": self.add_input,
            "[": self.start_loop,
            "]": self.end_loop
        }

    def print_state(self):
        print("----")
        print("Index : {0}".format(self.script_index))
        print("Executing : {0}".format(self.op_list[self.script_index]))
        print("Pointer : {0}".format(self.ptr))
        print("Output buffer : {0}".format("".join(self.output_buffer)))
        print("Loop stack : ")
        print(self.loop_stack.hidden_list)
        print("{0} addresses".format(len(self.memory_state)))
        for i in range(0, len(self.memory_state)):
            print("{0} : {1}".format(i, str(self.memory_state[i])))
        print("----")

    def is_mem_def(self):
        return len(self.memory_state) > self.ptr

    def decrement_value(self):
        if self.is_mem_def():
            if self.memory_state[self.ptr] - 1 < -128:
                self.memory_state[self.ptr] = 127
            else:
                self.memory_state[self.ptr] -= 1
        else:
            raise Exception("Failed at decrementing the pointer")

    def add_input(self):
        self.memory_state[self.ptr] = ord(input()[0])

    def increment_value(self):
        if self.is_mem_def():
            if self.memory_state[self.ptr] + 1 > 127:
                self.memory_state[self.ptr] = -128
            else:
                self.memory_state[self.ptr] += 1
        else:
            raise Exception("Failed at incrementing the pointer")

    def increment_ptr(self):
        self.ptr += 1
        if not self.is_mem_def():
            self.memory_state.append(0)

    def decrement_ptr(self):
        if self.ptr == 0:
            if not self.wrapping:
                raise Exception("Pointer can't be < 0")
            else:
                self.memory_state.append(0)
                self.ptr = (len(self.memory_state) - 1)
        else:
            self.ptr -= 1

    def add_output(self):
        self.output_buffer.append(chr(self.memory_state[self.ptr % 128]))

    def start_loop(self):
        self.loop_stack.push(self.script_index)

    def end_loop(self):
        if self.loop_stack.length == 0:
            raise Exception("No opening loop")
        else:
            if self.memory_state[self.ptr] == 0:
                self.loop_stack.pop()
            else:
                self.script_index = self.loop_stack.last()

    def gen_op_list(self):
        self.op_list = [op for op in self.bf_script]

    def exec_op(self):
        if self.script_index < len(self.op_list):
            self.op_actions[self.op_list[self.script_index]]()
            self.op_count += 1
            return ((self.script_index) == (len(self.op_list) - 1))

    def exec_script(self):
        while not self.terminated:
            self.script_index += 1
            self.terminated = self.exec_op()
            #self.update_display()
            #sleep(0)
        self.update_display()


    def update_display(self):
        system("clear")
        print("SYSTEM STATE")
        print("{0} operations have been executed".format(self.op_count))
        print("Executing : {0}".format(self.op_list[self.script_index]))
        print("{0} memory slots used".format(len(self.memory_state)))
        print("Index in the program : {0}".format(self.script_index))
        '''
        for i in range(self.script_index - 10, self.script_index + 10):
            if i >= 0 and i < len(self.op_list):
                print("{0}".format(self.op_list[i]), end="")
        print("")
        for i in range(self.script_index - 10, self.script_index + 10):
            if i == self.script_index:
                print("^", end="")
            elif i >= 0:
                print(" ", end="")
        print("")
        for i in range(self.ptr - 5, self.ptr + 5):
            if i >= 0 and i < len(self.memory_state):
                if i == self.ptr:
                    print(" [{0}] ".format(self.memory_state[i]), end=" ")
                else:
                    print(" {0} ".format(self.memory_state[i]), end=" ")
        print("")
        '''
        for i in range(0, len(self.op_list)):
            print(self.op_list[i], end="")
        print("")
        for i in range(0, len(self.op_list)):
            if i == self.script_index:
                print("^", end="")
            else:
                print(" ", end="")
        print("")
        for i in range(0, len(self.memory_state)):
            if i == self.ptr:
                print("[{0}]".format(self.memory_state[i]), end=" ")
            else:
                print(self.memory_state[i], end=" ")
        print("\n")
        print("OUTPUT : {0}".format("".join(self.output_buffer)))


hw = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>." # works
hw_bug = ">++++++++[-<+++++++++>]<.>>+>-[+]++>++>+++[>[->+++<<+++>]<<]>-----.>->+++..+++.>-.<<+[>[+>+]>>]<--------------.>>.+++.------.--------.>+.>+." # doesn't work
eight_bit = "+[[->]-[-<]>-]>.>>>>.<<<<-.>>-.>.<<.>>>>-.<<<<<++.>>++." # works, so my custom 8 bits ints are working
overflow_test = "[-]+[+]"
short_hw = "--<-<<+[+[<+>--->->->-<<<]>]<<--.<++++++.<<-..<<.<+.>>.>>.<<<.+++.>>.>>-.<<<+."

a = BrainfuckInterpreter(eight_bit)
a.gen_op_list()
a.exec_script()
