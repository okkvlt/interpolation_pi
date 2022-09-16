from sys import argv

import numpy as np
from PIL import Image


class Interpolation:
    def __init__(self, img: str):
        self.img = Image.open(img)

    def neighbor(self, operation: int = 1) -> None:
        """
        Realiza operações por meio
        da interpolação por vizinho
        mais próximo.

        Args:
            operation:
                1 - Ampliação [Padrão] | 
                2 - Redução

        Returns:
            None
        """

        column, line = self.img.size
        x = np.array(self.img)  # transforma a imagem em array

        if operation == 1:
            print("Ampliando...")

            x = np.repeat(x, 2, 1)  # duplica as colunas
            x = np.repeat(x, 2, 0)  # duplica as linhas
        else:
            print("Reduzindo...")

            for l in range(0, int(line / 2)):
                x = np.delete(x, l+1, 0)  # deleta as linhas ímpares

            for c in range(0, int(column / 2)):
                x = np.delete(x, c+1, 1)  # deleta as colunas ímpares

        img = Image.fromarray(x)  # converte o array em imagem
        img.save("output.jpg", "JPEG")  # salva a imagem

    def bilinear(self, operation: int = 1) -> None:
        """
        Realiza operações por meio
        da interpolação bilinear.

        Args:
            operation:
                1 - Ampliação [Padrão] | 
                2 - Redução

        Returns:
            None
        """

        column, line = self.img.size
        x = np.array(self.img)

        if operation == 1:
            print("Ampliando...")

            x = np.repeat(x, 2, 1)
            x = np.repeat(x, 2, 0)

            # duplica as linhas e colunas

            column = range(0, int(column * 2))
            line = range(0, int(line * 2))

            # multiplica por dois a altura e o comprimento
            # e cria uma lista com os valores de 0 até a altura/comprimento

            for l in line:
                if l % 2 == 0 and l + 2 in line:
                    for c in column:
                        if c % 2 == 0 and c + 2 in column:
                            c_r, c_g, c_b = x[l][c]  # pixel par
                            dr_r, dr_g, dr_b = x[l][c + 2]
                            db_r, db_g, db_b = x[l + 2][c]
                            drb_r, drb_g, drb_b = x[l + 2][c + 2]

                            middle_r = int(
                                (int(c_r) + int(dr_r) + int(db_r) + int(drb_r)) / 4)
                            middle_g = int(
                                (int(c_g) + int(dr_g) + int(db_g) + int(drb_g)) / 4)
                            middle_b = int(
                                (int(c_b) + int(dr_b) + int(db_b) + int(drb_b)) / 4)

                            right_r = int((int(c_r) + int(dr_r)) / 2)
                            right_g = int((int(c_g) + int(dr_g)) / 2)
                            right_b = int((int(c_b) + int(dr_b)) / 2)

                            bottom_r = int((int(c_r) + int(db_r)) / 2)
                            bottom_g = int((int(c_g) + int(db_g)) / 2)
                            bottom_b = int((int(c_b) + int(db_b)) / 2)

                            x[l + 1][c + 1] = middle_r, middle_g, middle_b
                            x[l][c + 1] = right_r, right_g, right_b
                            x[l + 1][c] = bottom_r, bottom_g, bottom_b

        else:
            print("Reduzindo...")

            lines = range(0, line)
            columns = range(0, column)

            for l in lines:
                if l % 2 == 0 and l + 1 in lines:
                    for c in columns:
                        if c % 2 == 0 and c + 1 in columns:
                            c_r, c_g, c_b = x[l][c]
                            right_r, right_g, right_b = x[l][c + 1]
                            bottom_r, bottom_g, bottom_b = x[l + 1][c]
                            right_bottom_r, right_bottom_g, right_bottom_b = x[l + 1][c + 1]

                            new_r = int(
                                (int(c_r) + int(right_r) + int(bottom_r) + int(right_bottom_r)) / 4)
                            new_g = int(
                                (int(c_g) + int(right_g) + int(bottom_g) + int(right_bottom_g)) / 4)
                            new_b = int(
                                (int(c_b) + int(right_b) + int(bottom_b) + int(right_bottom_b)) / 4)

                            x[l][c] = new_r, new_g, new_b

            line /= 2
            column /= 2

            for l in range(0, int(line)):
                if l + 1 in range(0, int(line)):
                    x = np.delete(x, l+1, 0)

            for c in range(0, int(column)):
                if c + 1 in range(0, int(column)):
                    x = np.delete(x, c+1, 1)

        img = Image.fromarray(x)
        img.save("output.jpg", "JPEG")


if len(argv) < 2:
    print("Passe a imagem por linha de comando!")
    print("Ex: \"python3 " + argv[0] + " image.jpg\"")

    exit(0)

print("Qual método deseja utilizar? ")
print("\n1 - Interpolação Bilinear")
print("2 - Interpolação por Vizinho")
method = input("\nMétodo [1-2]: ")

print("Qual operação deseja realizar? ")
print("\n1 - Ampliação")
print("2 - Redução")
op = input("\nOperação [1-2]: ")

functs = {
    "1": Interpolation(argv[1]).bilinear,
    "2": Interpolation(argv[1]).neighbor,
}

functs[str(method)](operation=int(op))
