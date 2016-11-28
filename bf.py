#! /usr/bin/python3
from time import sleep
from os import system


class ScriptManager:
    def __init__(self, path):
        self.path = path
        self.f = open(self.path, "r")
        self.text = self.f.read()
        self.f.close()
        self.parse_progs()

    def parse_progs(self):
        self.progs = [x.strip().splitlines() for x in self.text.split("END")]

    def is_valid(self, char):
        return char == "+" or char == "-" or char == ">" or char == "<" or char == "." or char == "," or char == "[" or char == "]"

    def ask(self):
        print("WHICH PROGRAM SHOULD I RUN?")
        for x in range(0, len(self.progs) - 1):
            print("{0} : {1}".format(x, self.progs[x][0]))
        print("input : ", end="")
        return ''.join([x for x in self.progs[int(input())][1] if self.is_valid(x)])


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
        self.wrapping = True
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
                self.memory_state.insert(0, 0)
        else:
            self.ptr -= 1

    def add_output(self): 
        self.output_buffer.append(chr(self.memory_state[self.ptr]))

    def count_next(self):
        op_count = 1
        cl_count = 0
        for i in range(self.script_index + 1, len(self.op_list)):
            if self.op_list[i] == "]" and op_count == cl_count + 1:
                return i
            elif self.op_list[i] == "[":
                op_count += 1
            elif self.op_list[i] == "]":
                cl_count += 1

    def start_loop(self):
        if self.memory_state[self.ptr] != 0:
            self.loop_stack.push(self.script_index)
        else:
            self.script_index = self.count_next()
            
    def end_loop(self):
        if self.loop_stack.length() == 0:
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
            if(self.op_list[self.script_index] in self.op_actions):
                self.op_actions[self.op_list[self.script_index]]()
                self.op_count += 1
            return ((self.script_index) == (len(self.op_list) - 1))

    def exec_script(self):
        while not self.terminated:
            self.script_index += 1
            self.terminated = self.exec_op()
            self.update_display()
            sleep(0.025)
        self.update_display()

    def update_display(self):
        system("clear")
        print("SYSTEM STATE")
        print("{0} operations have been executed".format(self.op_count))
        print("Executing : {0}".format(self.op_list[self.script_index]))
        print("{0} memory slots used".format(len(self.memory_state)))
        print("Index : {0}".format(self.script_index))
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




s = ScriptManager("bfprogs.cbf")
a = BrainfuckInterpreter(s.ask())
a.gen_op_list()
a.exec_script()



s="[+[---[----][---[]]---]+]+++[---]"

