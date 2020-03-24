"""CPU functionality."""

import sys

# LDI = 10000010
# EIGHT = 00001000 # this is 8
# PRINT_NUM = 01000111 # PRN R0
# HALT = 00000001 # HLT

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8 # 8 general-purpose registers
        self.ram = [0] * 256 # memory with 256 bytes

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
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def reg_write(self, reg, num): # implemented my own write to reg function
        self.reg[reg] = num

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            instruction = self.ram[self.pc]
            reg1 = self.ram_read(self.pc + 1)
            reg2 = self.ram_read(self.pc + 2)

            if instruction == 0b10000010 or instruction == 'LDI':
                reg = self.ram_read(self.pc + 1)
                num = self.ram_read(self.pc + 2)
                self.reg_write(reg, num) # should store num in reg
                self.pc += 3

            elif instruction == 0b10100010 or instruction == 'MUL': # MUL
                self.alu('MUL', reg1, reg2)
                self.pc += 3

            elif instruction == 0b01000111  or instruction == 'PRN':
                # reg = self.ram_read(self.pc + 1)
                print(self.reg[reg1])
                self.pc += 2
            
            elif instruction == 0b00000001 or instruction == 'HLT':
                running == False
                sys.exit(0)

            else:
                print(f"Unknown instruction in {instruction}")
                sys.exit(1)
