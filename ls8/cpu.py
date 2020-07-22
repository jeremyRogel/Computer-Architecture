"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.sp = 7
        self.reg[self.sp] = 0xF4
        self.running = True
        self.ir = {
            0b10100010: 'MUL',
            0b00000001: 'HLT',
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b01000101: 'PUSH',
            0b01000110: 'POP'           
        }

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        program = []
        with open(file_name) as f:

            for address, line in enumerate(f):
                line = line.split("#")
                try:
                    v = int(line[0], 2)

                except ValueError:
                    continue
                self.ram[address] = v




        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""


        value = op >> 6 
        value = value + 0b00000001
        # print('value', value)
        op = self.ir[op]
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'MUL':
            print(self.reg[reg_a] * self.reg[reg_b])
            self.pc +=value
        elif op == 'LDI':
            self.ram_write(reg_a, reg_b)
            self.pc +=value  #3
        elif op == 'HLT':
            self.running = False
            self.pc += value
            sys.exit(1)
        elif op == 'PRN':
            print(self.reg[reg_a])
            self.pc += value
        elif op == 'PUSH':

            self.reg[self.sp] -= 1

            reg_value = self.reg[reg_a]

            stack_address = self.reg[self.sp]
            self.ram[stack_address] = reg_value
            self.pc += value
        elif op == 'POP':

            stack_address = self.reg[self.sp]

            reg_value = self.ram_read(stack_address)
            self.reg[self.sp] = self.reg[self.sp] + 1

            self.reg[reg_a] = reg_value

            self.pc += value

        else:
            raise Exception("Unsupported ALU operation")
        sys.exit(1)

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

    def ram_read(self, counter):
        return self.ram[counter]
    


    def ram_write(self, counter, value):
        self.reg[counter] = value

    def run(self):
        """Run the CPU."""
       
        while self.running:


            self.alu(self.ram_read(self.pc), self.ram_read(
                self.pc+1), self.ram_read(self.pc+2))

            # PUSH
# PUSH register

# # Push the value in the given register on the stack.

# # Decrement the SP.
# # Copy the value in the given register to the address pointed to by SP.
# # Machine code:

# # 01000101 00000rrr
# 45 0r

