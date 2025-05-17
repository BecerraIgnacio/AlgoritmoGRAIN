from typing import List, Optional
from collections import deque

class Bit:
    def __init__(self, valor):
        self.valor = int(valor)

    def __add__(self, other):
        return Bit(self.valor ^ other.valor)

    def __mul__(self, other):
        return Bit(self.valor & other.valor)

    def __str__(self):
        return str(self.valor)


IV_STRING  = "0001110000001000110101111111011101001111111110110011001011101111111111000001001110110010111000011"  # 96 bits
KEY_STRING = "10000001110001011110111010101100000010011111101001000111100001100100101110110000111010001000111101110001101110010111001001010110"  # 128 bits

# Convertir a deque de Bits
IV_bits  = deque(Bit(int(c)) for c in IV_STRING)
KEY_bits = deque(Bit(int(c)) for c in KEY_STRING)

# LFSR: IV (96 bits) + 31 unos + un cero
lsfr_acc = deque(IV_bits)
lsfr_acc.extend([Bit(1)] * 31 + [Bit(0)])

# NFSR: toda la clave
nsfr_acc = deque(KEY_bits)

# Generamos mensaje de prueba
mensaje = [Bit(1)] * 1000

# Inicializamos Acumulador
A = deque([Bit(0)] * 64)

# Inicializamos registro
R = deque([Bit(0)] * 64)


# Calculo de funcion f
def fun_f(acc: deque[Bit]) -> Bit:
    return (acc[0] + acc[7] + acc[38] + acc[70] + acc[81] + acc[96])

# Calculo de funcion g
def fun_g(acc: deque[Bit]) -> Bit:
    return (acc[26] + acc[56] + acc[91] + acc[96] + acc[3]*acc[67]
            + acc[11]*acc[13] + acc[17]*acc[18] + acc[27]*acc[59]
            + acc[40]*acc[48] + acc[61]*acc[65] + acc[68]*acc[84]
            + acc[22]*acc[24]*acc[25] + acc[70]*acc[78]*acc[82]
            + acc[88]*acc[92]*acc[93]*acc[95])

# Calculo de funcion h
def fun_h(s_acc: deque[Bit], b_acc: deque[Bit]) -> Bit:
    return (b_acc[12]*s_acc[8] + s_acc[13]*s_acc[20]
            + b_acc[95]*s_acc[42] + s_acc[60]*s_acc[79]
            + b_acc[12]*b_acc[95]*s_acc[94])

# Calculo de funcion y
def fun_y(s_acc: deque[Bit], b_acc: deque[Bit], h: Bit) -> Bit:
    return (s_acc[93] + b_acc[2] + b_acc[15] + b_acc[36]
            + b_acc[45] + b_acc[64] + b_acc[73] + b_acc[89] + h)

# Actualizacion LSFR
def step_lsfr(acc: deque[Bit], y: Bit, key_bit: Optional[Bit] = None) -> Bit:
    s0 = acc.popleft()
    carry = fun_f(acc) + s0 + (y if key_bit is None else key_bit)
    acc.append(carry)
    return s0

# Actualizacion NSFR
def step_nsfr(acc: deque[Bit], s_t: Bit, y: Bit, key_bit: Optional[Bit] = None) -> Bit:
    b0 = acc.popleft()
    carry = b0 + fun_g(acc) +  s_t
    if key_bit is None: carry = carry + y
    acc.append(carry)
    return b0

# Ciclo de reloj
def clock_cycle(lsfr: deque[Bit], nsfr: deque[Bit], key_bit: Optional[Bit] = None) -> Bit:
    # Calculo h_t e y_t sobre estado actual
    h_t = fun_h(lsfr, nsfr)
    y_t = fun_y(lsfr, nsfr, h_t)

    # Actualizo LSFR
    s_t = step_lsfr(lsfr, y_t, key_bit)

    # Actualizo NSFR
    step_nsfr(nsfr, s_t, y_t, key_bit)

    return y_t


def main():

    # Calentamiento: 256 ciclos descartando salida
    for _ in range(256):
        clock_cycle(lsfr_acc, nsfr_acc)

    # Insertamos bits key (clave)
    for i, key_bit in enumerate(KEY_bits):
        y = clock_cycle(lsfr_acc, nsfr_acc, key_bit=key_bit)
        if i < 64: A[i] = y
        else: R[i - 64] = y

    print("\nMENSAJE")
    for i, m in enumerate(mensaje, 1): print(m, end="")

    print("\n\nMENSAJE ENCRIPTADO")
    q1 = q0 = 0

    # Recorremos bit a bit, actualizamos A y R en cada iteración
    for i, m in enumerate(mensaje, 1):
        # Generar siguiente bit de keystream
        y = clock_cycle(lsfr_acc, nsfr_acc)
        # Cifrar el bit
        c = m + y
        # Actualizar contadores
        if c.valor == 1: q1 += 1
        else: q0 += 1
        # Imprimir bit
        print(c, end="")

        # Actualizar R con y
        R.popleft()
        R.append(y)

        # Actualizar A con y + c
        A.popleft()
        A.append(y + c)


    print("\nCantidad\n")
    print(f"Cantidad 0: {q0}")
    print(f"Cantidad 1: {q1}")
    print(f"Chance of 0: {q0*100/(q0+q1)}")
    print(f"Chance of 1: {q1*100/(q0+q1)}")

    # 64 ciclos más para actualizar A y R con y_t
    for _ in range(64):
        y = clock_cycle(lsfr_acc, nsfr_acc)
        # desplazamos y añadimos al final
        A.popleft(); A.append(y)
        R.popleft(); R.append(y)

    # 5) Extracción del tag de autenticación: los 64 bits de R
    tag = "".join(str(b) for b in R)
    print("\nTAG (64 bits):", tag)



if __name__ == "__main__":
    main()



