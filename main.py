import argparse
import api
from ast import literal_eval

test = {
    "joueurs": [
        {"nom": "idul", "murs": 7, "pos": [5, 5]},
        {"nom": "automate", "murs": 3, "pos": [8, 6]},
    ],
    "murs": {
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
        "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]],
    },
}


def afficher_damier_ascii(board):
    print(f"Légende: 1={board['joueurs'][0]['nom']}, 2={board['joueurs'][1]['nom']}")
    coords_first_player = board["joueurs"][0]["pos"]
    coords_second_player = board["joueurs"][1]["pos"]
    horizontal_walls = board["murs"]["horizontaux"]
    vertical_walls = board["murs"]["verticaux"]
    print("   -----------------------------------")
    for y in range(9, 0, -1):
        current_line = f"{y} |"
        if [0, y] in horizontal_walls:
            current_line += "-"
        else:
            current_line += " "
        for x in range(1, 10):
            coords = [x, y]
            if coords == coords_first_player:
                current_line += str(1)
            elif coords == coords_second_player:
                current_line += str(2)
            else:
                current_line += "."
            if [coords[0] + 1, coords[1]] in vertical_walls or [
                coords[0] + 1,
                coords[1] - 1,
            ] in vertical_walls:
                current_line += " | "
            else:
                current_line += "   "
        current_line = current_line[:-2]
        current_line += "|"
        current_line += "\n  | "
        print_line = False
        for x in range(1, 10):
            if print_line:
                print_line = False
                continue
            print_line = False
            coords = [x, y]
            if [coords[0], coords[1] - 1] in vertical_walls:
                current_line = current_line[:-2]
                current_line += "| "
            if coords in horizontal_walls:
                if current_line[-1] != "|":
                    current_line = current_line[:-1]
                    current_line += "-------  "
                print_line = True

            if print_line is not True:
                current_line += "    "
        current_line = current_line[:-2]
        current_line += "|"
        print(current_line)
    print("--|-----------------------------------")
    print("  | 1   2   3   4   5   6   7   8   9")


def analyser_commande():
    parser = argparse.ArgumentParser(description="Jeu Quoridor - phase 1")
    parser.add_argument("idul", type=str, help="IDUL du joueur")
    parser.add_argument(
        "-l",
        "--lister",
        action="count",
        help="Lister les identifiants de vos 20 dernières parties",
    )
    return parser.parse_args()


def ask_type():
    type_coup = input("D, MH, MV : ")
    if type_coup not in ["D", "MH", "MV"]:
        return ask_type()
    return type_coup


def ask_coords():
    try:
        return literal_eval(input("coords (x,y) : "))
    except ValueError as _:
        return ask_coords()


if __name__ == "__main__":
    args = analyser_commande()
    if args.lister is not None:
        print(api.lister_parties(args.idul)[:20])

    id_game, board = api.initialiser_partie(args.idul)

    while True:
        try:
            afficher_damier_ascii(board)
            type_coup = ask_type()
            coords = ask_coords()
            board = api.jouer_coup(id_game, type_coup, coords)
        except StopIteration as e:
            print(e)
            break
        except RuntimeError as e:
            print(e)
            