import sys

PRINT_BEEJ      = 1
HALT            = 2
PRINT_NUM       = 3
SAVE            = 4 # save value to register
PRINT_REGISTER  = 5 # print the value in a register
ADD             = 6 # add 2 registers, store result in 1st register

memory = [
    PRINT_BEEJ,
    SAVE,
    65, # save 65 in register 2
    2, #register 2
    SAVE,
    20, # save 20 in register 3
    3, #register 3
    ADD, # ADD R2 += R3
    2,
    3,
    PRINT_REGISTER, # Print R2
    2,
    HALT
]

register = [0] * 8

pc = 0 # PROGRAM COUNTER


while True:
    command = memory[pc]

    if command == PRINT_BEEJ:
        print("beej")
        pc += 1
    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2
    elif command == SAVE:
        num = memory[pc+1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3
    elif command == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2
    elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3
    elif command == HALT:
        sys.exit(0)
    else:
        print ("I DID NOT UNDERSTAND THAT COMMAND")
        sys.exit(1)