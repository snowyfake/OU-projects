import math
import time


def main():
    print("BIENVENIDO AL TRES EN RAYA: ")
    rows, columns = 3, 3
    play_exit = True
    while play_exit:
        n = int(input("\nPulse 1 para jugar, 0 para salir: "))
        if n == 1:
            game_board = init_board(rows, columns)
            print("")
            show_board(game_board, rows, columns)
            player_one, player_two = "X", "O"
            print("RONDA 1: ")
            rounds = 1
            while not is_win(game_board, player_one) and not is_win(game_board, player_two) and not is_draw(game_board):
                print("\nTURNO DEL JUGADOR 1: ")
                movement1 = False
                while not movement1:
                    cX, cY = (input("Introduzca donde quiera colocar su ficha (coordenadas x y): ").split())
                    if make_movement(game_board, player_one, int(cX), int(cY)):
                        make_movement(game_board, player_one, int(cX), int(cY))
                        movement1 = True
                    else:
                        print("La posicion esta ocupada. Pruebe otra vez: ")
                print("")
                show_board(game_board, rows, columns)
                if is_win(game_board, player_one):
                    print("ENHORABUENA JUGADOR 1! HA GANADO!")
                elif is_draw(game_board):
                        print("No hay mas movimientos posibles: EMPATE.")
                else:
                    print("\nTURNO DE LA IA: ")
                    if rounds == 1:
                        rounds += 1
                        if not make_movement(game_board,player_two, 1, 1):
                            ai_movermaker(game_board, player_two,player_one)
                        else:
                            make_movement(game_board,player_two, 1, 1)
                        show_board(game_board, rows, columns)
                    else:
                        ai_movermaker(game_board, player_two,player_one)
                        show_board(game_board, rows, columns)
                        print("")
                        if is_win(game_board, player_two):
                            print("OH VAYA! PARECE QUE HAS PERDIDO.")
                        elif is_draw(game_board):
                            print("No hay mas movimientos posibles: EMPATE.")
                        else:
                            rounds += 1
                            print("RONDA "+str(rounds)+": ")
        else:
            play_exit = False

    print("Hasta pronto!")


def init_board(rows, columns):
     board = [["_" for j in range(columns)] for i in range(rows)]
     return board

def show_board(matrix, r, c):
    for i in range(r):
        for j in range(c):
            print(str(matrix[i][j])+"       ", end = "")
        print("\n\n\n")

def make_movement(matrix, player, r, c):
    if matrix[r][c] != 'X' and matrix[r][c] != "O":
        matrix[r][c] = player
        return True
    else:
        return False

def is_win(matrix, player): #3
    r, c, pD, rD = 0, 0, 0, 0
    aux = 2
    result = False
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == player:
                r += 1
            else:
                r = 0
            if matrix[j][i] == player:
                c += 1
            else:
                c = 0
            if matrix[j][j] == player:
                pD += 1
            else:
                pD = 0
            if matrix[j][aux] == player:
                rD += 1
                aux -= 1
            else:
                rD = 0
                aux = 2
        if r == 3 or c == 3 or pD == 3 or rD == 3:
            return True
        else:
            r, c, pD, rD = 0, 0, 0, 0
    return result

def is_draw(matrix):
    for i in range(3):
        for j in range(3):
            if matrix[i][j] != 'X' and matrix[i][j] != 'O':
                return False
    return True

def ai_movermaker(matrix, ai, player):

    heuristic = 0
    selected_row, selected_colmn = 0,0

    for i in range(3):
        for j in range(3):
            if matrix[i][j] == '_':
                aux = count_points(matrix, player, ai, i, j) - count_points(matrix, ai, player, i, j)
                if aux > heuristic:
                    heuristic = aux
                    selected_colmn = j
                    selected_row = i
    make_movement(matrix, ai, selected_row, selected_colmn)

def count_points(matrix, playerA, playerB, r, c):

    pointsR, pointsC, points_PD,points_RD, aux = 0,0,0,0,2
    validR, validC, valid_PD, valid_RD = True, True, True, True

    for i in range(3):
        if matrix[i][c] != playerB and matrix[i][c] != matrix[r][c]:
            if matrix[i][c] != "_" and validC:
             pointsC += 1
        elif matrix[i][c] == playerB:
            validC = False
        if matrix[r][i] != playerB and matrix[r][i] != matrix[r][c]:
             if matrix[r][i] != "_" and validR:
                pointsR += 1
        elif matrix[r][i] == playerB:
            validR = 0
        if (r%2 == 0 and c%2 == 0) or (r == 1 and c == 1):
            if r == c:
                if matrix[i][i] != playerB and matrix[i][i] != matrix[r][c]:
                    if matrix[i][i] != "_" and valid_PD:
                        points_PD += 1
                elif matrix[i][i] == playerB:
                    valid_PD = False
            if (r == 0 and c == 2) or (r == 1 and c == 1) or (r == 2 and c == 0):
                if matrix[i][aux] != playerB and matrix[i][aux] != matrix[r][c]:
                    if matrix[i][aux] != "_" and valid_RD:
                        points_RD += 1
                elif matrix[i][aux] == playerB:
                    valid_RD = False
                aux -= 1
    if not valid_PD: points_PD = 0
    elif not valid_RD: points_RD = 0
    elif not validC: pointsC = 0
    elif not validR: pointsR = 0

    if points_PD == 2 or points_RD == 2 or pointsC == 2 or pointsR == 2:
        if playerA == 'X':
            total_points = 50 #1
        elif playerA == 'O':
            total_points = -50 #2
    else:
        total_points = points_PD + points_RD + pointsC + pointsR + 1

    return total_points

main()

#DOCUMENTACION

#1: Valor de parcheado, en caso de que un puntuaje de una fila llegue a dos,->
#->la siguiente jugada daria la victoria al jugador, por lo que asigno un valor->
#-> de puntuaje muy alto para darle maxima prioridad a esa posicion.

#2: Valor de parcheado, en caso de que un puntuaje de una fila llegue a doss,->
#->la posicion daria victoria a la IA, por lo que se le asigna un valor muy bajo para darle->
#-> maxima prioridad

#3: Bug en la funcion is_win, cuando hay empate o no es victoria salta la funcion como->
#-> TRUE

