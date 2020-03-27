"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8 # 8 general-purpose registers
        self.pc = 0
        self.ram = [0] * 256 # memory with 256 bytes
        self.fl = 7

        
    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mdr] = mar

    def load(self, program):
        """Load a program into memory."""

        address = 0

        try:
            with open(program) as p:
                for line in p:

                    # ignore comments
                    comment_split = line.split("#")

                    #Strip out whitespace
                    num = comment_split[0].strip()

                    if num == "":
                        continue

                    instruction = int(num, 2)
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print('FILE NOT FOUND')
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()


    def reg_write(self, reg, num): # implemented my own write to reg function
        self.reg[reg] = num

    def run(self):
        """Run the CPU."""
        sp = 255
        running = True

        while running:
            instruction = self.ram_read(self.pc)
            reg1 = self.ram_read(self.pc + 1)
            reg2 = self.ram_read(self.pc + 2)

            self.reg[7] = sp

            if instruction == 0b10000010 or instruction == 'LDI':
                self.reg_write(reg1, reg2) # should store num in reg
                self.pc += 3
            elif instruction == 0b01000111  or instruction == 'PRN':
                print(self.reg[reg1])
                self.pc += 2
            elif instruction == 0b00000001 or instruction == 'HLT':
                running == False
                sys.exit(0)
            elif instruction == 0b10100000 or instruction == "ADD":
                self.alu('ADD', reg1, reg2)
                self.pc += 3
            elif instruction == 0b10100010 or instruction == 'MUL': # MUL
                self.alu('MUL', reg1, reg2)
                self.pc += 3
            elif instruction == 0b01000101 or instruction == 'PUSH':
                sp -= 1
                self.ram_write(self.reg[reg1], sp)
                self.pc += 2
            elif instruction == 0b01010000 or instruction == 'CALL':
                sp -= 1
                self.ram_write(self.pc, sp)
                self.pc = self.reg[reg1]
            elif instruction == 0b00010001 or instruction == "RET":
                self.pc = self.ram_read(sp) + 2
                sp += 1
            elif instruction == 0b01000110 or instruction == 'POP':
                self.reg[reg1] = self.ram_read(sp)
                sp += 1
                self.pc += 2
            elif instruction == 0b10100111 or instruction == 'CMP':
                self.alu('CMP', reg1, reg2)
                self.pc += 3
            elif instruction == 0b01010100 or instruction == "JMP":
                self.pc = self.reg[reg1]
            elif instruction == 0b01010101 or instruction == 'JEQ':
                if self.fl == 0b00000001:
                    self.pc = self.reg[reg1]
                else:
                    self.pc += 2
            elif instruction == 0b01010110 or instruction == 'JNE':
                if self.fl == 0b00000010 or self.fl == 0b00000100:
                    self.pc = self.reg[reg1]
                else:
                    self.pc += 2

            else:
                print(f"Unknown instruction in {instruction}")
                sys.exit(1)
