# 📘 Grain-128AEAD Simulator

Este documento describe **paso a paso** el funcionamiento del algoritmo Grain-128AEAD, implementado en `simulacion.py`.

---

## 🔍 Visión General

Grain-128AEAD es un **cifrado de flujo autenticado** (AEAD) ligero, ideal para entornos con recursos limitados. Combina:

1. **Cifrado por flujo**: genera un *keystream* de bits pseudoaleatorios que se XORean con el mensaje.
2. **Autenticación**: produce un **tag** de 64 bits que garantiza integridad y autenticidad.

La implementación sigue estas **6 fases** principales:

---

## 1️⃣ Fase 0: Carga de IV y Clave

* **IV (nonce)** de 96 bits en LFSR:

  1. Carga los primeros 96 bits del LFSR con el vector de inicialización (`IV_STRING`).
  2. Rellena los siguientes 31 bits con `1` y el último con `0`.
* **Clave** de 128 bits en NFSR:

  * Todos los bits de `KEY_STRING` se cargan directamente en el NFSR.

```python
# Ejemplo
lsfr = deque(IV_bits)                # 96 bits IV
lsfr.extend([Bit(1)]*31 + [Bit(0)])  # 31 unos + 1 cero
snfr = deque(KEY_bits)               # 128 bits clave
```

---

## 2️⃣ Fase 1: Warm-up (256 ciclos)

Objetivo: "mezclar" IV y clave antes de generar keystream.

Por cada ciclo t = 0…255:

1. **Calcular pre-salida**:

   * `h_t = fun_h(lsfr, nsfr)` → filtro no lineal
   * `y_t = fun_y(lsfr, nsfr, h_t)` → suma XOR de taps ♻️
2. **Actualizar LFSR**: `s_{t+128} = f(lsfr) ⊕ s_t ⊕ y_t` (sin clave)
3. **Actualizar NFSR**: `b_{t+128} = b_t ⊕ g(nsfr) ⊕ s_t ⊕ y_t` (sin clave)

> ❗️ Los bits `y_t` **no** se guardan: solo se descarta la salida.

---

## 3️⃣ Fase 2: Reintroducción de clave (128 ciclos)

Objetivo: reforzar la mezcla inyectando la clave al final de la inicialización.

Por t = 256…383, por cada bit `key_bit` de la clave:

1. **Calcular** `h_t`, `y_t` como antes.
2. **Actualizar LFSR**:
   $s_{t+128} = f(lsfr) ⊕ s_t ⊕ key\_bit$ (ya **no** se usa `y_t`)
3. **Actualizar NFSR**:
   $b_{t+128} = b_t ⊕ g(nsfr) ⊕ s_t$ (ya **no** se usa `y_t`)
4. **Guardar** los primeros 64 `y_t` en **A** y los siguientes 64 en **R**:

   ```python
   if i < 64: A[i] = y_t
   else:      R[i-64] = y_t
   ```

---

## 4️⃣ Fase 3: Generación de Keystream y Cifrado

Para cada bit de mensaje `m_t`:

1. **Obtener** `y_t = clock_cycle(lsfr, nsfr)` en modo normal (inyecta `y` en registros).
2. **Cifrar**: `c_t = m_t ⊕ y_t`.
3. **Autenticación en vuelo**:

   * **R** ← desplaza y añade `y_t`:

     ```python
     R.popleft(); R.append(y_t)
     ```
   * **A** ← desplaza y añade `y_t ⊕ c_t`:

     ```python
     A.popleft(); A.append(y_t + c_t)
     ```

---

## 5️⃣ Fase 4: Finalización (64 ciclos)

Tras procesar todos los bits de mensaje:

* Ejecutar **64 ciclos** más sin datos ni clave:

  1. `y_t = clock_cycle(lsfr, nsfr)`
  2. **R** ← desplaza + `y_t`
  3. **A** ← desplaza + `y_t` (equivale a `y_t ⊕ 0`)

---

## 6️⃣ Fase 5: Extracción del Tag

El **tag** de autenticación son los 64 bits actuales del registro **R**:

```python
tag = "".join(str(b) for b in R)
print("TAG (64 bits):", tag)
```

Garantiza la **integridad** y **autenticidad** de IV, mensaje y datos asociados.

---

## 🔗 Documentación Oficial

Consulta más detalles en:
👉 [Grain-128AEAD Documentation](https://grain-128aead.github.io) 🌐
