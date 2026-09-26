import string

ABC = string.ascii_uppercase

# Wiring rotor Enigma
ROTOR_I = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
ROTOR_II = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
ROTOR_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"

ROTORS = {
    "I": ROTOR_I,
    "II": ROTOR_II,
    "III": ROTOR_III
}

# Notch masing-masing rotor
NOTCH = {
    "I": "Q",
    "II": "E",
    "III": "V"
}

# Reflector B
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# Ciphertext
ciphertext = "WTJMEJKJKZJNYRTGSUUNZXMSCDDMPITYCBBPXHVLU"


def inverse_wiring(wiring):
    inverse = [""] * 26

    for i, letter in enumerate(wiring):
        inverse[ord(letter) - ord("A")] = ABC[i]

    return "".join(inverse)


INVERSE = {
    "I": inverse_wiring(ROTOR_I),
    "II": inverse_wiring(ROTOR_II),
    "III": inverse_wiring(ROTOR_III)
}


# Plugboard
plugboard = {
    "L": "A",
    "A": "L",
    "I": "P",
    "P": "I"
}


def plug(letter):
    return plugboard.get(letter, letter)


def rotor_forward(letter, rotor, position, ring):
    x = ord(letter) - ord("A")

    shifted = (x + position - ring) % 26

    output = ROTORS[rotor][shifted]

    result = (ord(output) - ord("A")
              - position + ring) % 26

    return ABC[result]


def rotor_backward(letter, rotor, position, ring):
    x = ord(letter) - ord("A")

    shifted = (x + position - ring) % 26

    output = INVERSE[rotor][shifted]

    result = (ord(output) - ord("A")
              - position + ring) % 26

    return ABC[result]


# Posisi awal ditulis kanan ke kiri: W, L, F
# Maka kiri ke kanan menjadi: F, L, W
positions = [
    ord("F") - ord("A"),  # Rotor I
    ord("L") - ord("A"),  # Rotor II
    ord("W") - ord("A")   # Rotor III
]

# Ring setting kanan ke kiri: P, O, N
# Maka kiri ke kanan: N, O, P
rings = [
    ord("N") - ord("A"),  # Rotor I
    ord("O") - ord("A"),  # Rotor II
    ord("P") - ord("A")   # Rotor III
]


def at_notch(rotor, position):
    notch_position = ord(NOTCH[rotor]) - ord("A")
    return position == notch_position


plaintext = ""

for character in ciphertext:

    # Posisi rotor
    left = positions[0]
    middle = positions[1]
    right = positions[2]

    # Double stepping Enigma
    middle_at_notch = at_notch("II", middle)
    right_at_notch = at_notch("III", right)

    if middle_at_notch:
        positions[0] = (positions[0] + 1) % 26
        positions[1] = (positions[1] + 1) % 26

    elif right_at_notch:
        positions[1] = (positions[1] + 1) % 26

    # Rotor kanan selalu berputar
    positions[2] = (positions[2] + 1) % 26

    # Plugboard
    letter = plug(character)

    # Rotor kanan -> kiri
    letter = rotor_forward(
        letter, "III", positions[2], rings[2]
    )

    letter = rotor_forward(
        letter, "II", positions[1], rings[1]
    )

    letter = rotor_forward(
        letter, "I", positions[0], rings[0]
    )

    # Reflector
    letter = REFLECTOR_B[
        ord(letter) - ord("A")
    ]

    # Rotor kiri -> kanan
    letter = rotor_backward(
        letter, "I", positions[0], rings[0]
    )

    letter = rotor_backward(
        letter, "II", positions[1], rings[1]
    )

    letter = rotor_backward(
        letter, "III", positions[2], rings[2]
    )

    # Plugboard
    letter = plug(letter)

    plaintext += letter


print("Ciphertext :", ciphertext)
print("Plaintext  :", plaintext)