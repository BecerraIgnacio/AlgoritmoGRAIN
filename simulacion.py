mensaje =           list("1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
LSFR_accumulator =  list("00011100000010001101011111110111010011111111101100110010111011111111110000010011101100101110000110001001000001101010011000011001")
NSFR_accumulator =  list("10000001110001011110111010101100000010011111101001000111100001100100101110110000111010001000111101110001101110010111001001010110")

class Bit:
    def __init__(self, valor):
        self.valor = int(valor)

    def __add__(self, other):
        return Bit(self.valor ^ other.valor)

    def __mul__(self, other):
        return Bit(self.valor & other.valor)

    def __str__(self):
        return str(self.valor)


def calcLSFR(accumulator):
    s0 = Bit(accumulator[0])
    s7 = Bit(accumulator[7])
    s38 = Bit(accumulator[38])
    s70 = Bit(accumulator[70])
    s81 = Bit(accumulator[81])
    s96 = Bit(accumulator[96])
    return  str(s0 + s7 + s38 + s70 + s81 + s96)

def calcNSFR(accumulator, carryLSFR):
    s0 = Bit(carryLSFR)
    b0 = Bit(accumulator[0])
    b26 = Bit(accumulator[26])
    b56 = Bit(accumulator[56])
    b91 = Bit(accumulator[91])
    b96 = Bit(accumulator[96])
    b3 = Bit(accumulator[3])
    b67 = Bit(accumulator[67])
    b22 = Bit(accumulator[11])
    b13 = Bit(accumulator[13])
    b17 = Bit(accumulator[17])
    b18 = Bit(accumulator[18])
    b27 = Bit(accumulator[27])
    b59 = Bit(accumulator[59])
    b40 = Bit(accumulator[40])
    b48 = Bit(accumulator[48])
    b61 = Bit(accumulator[61])
    b65 = Bit(accumulator[65])
    b68 = Bit(accumulator[68])
    b84 = Bit(accumulator[84])
    b22 = Bit(accumulator[22])
    b24 = Bit(accumulator[24])
    b25 = Bit(accumulator[25])
    b70 = Bit(accumulator[70])
    b78 = Bit(accumulator[78])
    b82 = Bit(accumulator[82])
    b88 = Bit(accumulator[88])
    b92 = Bit(accumulator[92])
    b93 = Bit(accumulator[93])
    b95 = Bit(accumulator[95])

    return str(s0 + b0 + b26 + b56 + b91 + b96 + b3*b67 + b22*b13 + b17*b18 + b27*b59 + b40*b48 + b61*b65 + b68*b84 + b22*b24*b25 + b70*b78*b82 + b88*b92*b93*b95)


def LSFR():
    carry = calcLSFR(LSFR_accumulator)
    LSFR_accumulator.pop()
    LSFR_accumulator.insert(0,carry)
    return carry

def NSFR():
    carry = calcNSFR(NSFR_accumulator,LSFR())
    NSFR_accumulator.pop()
    NSFR_accumulator.insert(0,carry)
    return carry



def main():


    print("ENCRIPTACION")
    print("\n")

    encript = list("")
    for i in range(100):
        bit = NSFR()
        print(bit,end="")
        encript.append(bit)
        if (i+1)%10 == 0:
            print("")

    print("\n\n")
    print("MENSAJE")
    print("\n")

    for i in range(100):
        print(mensaje[i],end="")
        if (i+1)%10 == 0:
            print("")

    print("\n\n")
    print("MENSAJE ENCRIPTADO")
    print("\n")


    for i in range(100):
        print(str(Bit(mensaje[i])+Bit(encript[i])),end="")
        if (i+1)%10 == 0:
            print("")




if __name__ == "__main__":
    main()