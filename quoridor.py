import api
from player import Player
from graph import construire_graphe, nx


class QuoridorError(Exception):
    pass


class Quoridor:
    def __init__(self, players, walls):
        try:
            if isinstance(players[0], list):
                self.players = [
                    Player(players[0], (5, 1), 10, 1),
                    Player(players[1], (5, 9), 10, 2),
                ]
            else:
                self.players = []
                for player in players:
                    self.players.append(
                        Player(player["nom"], player["pos"], player["murs"], 0)
                    )
            self.players[0].idx = 1
            self.players[1].idx = 2
            walls["horizontaux"] = [tuple(wall) for wall in walls["horizontaux"]]
            walls["verticaux"] = [tuple(wall) for wall in walls["verticaux"]]
            self.walls = walls
        except Exception as e:
            raise QuoridorError(e)

    @property
    def board(self):
        first_player = self.players[0].to_json()
        second_player = self.players[1].to_json()
        return {"joueurs": [first_player, second_player], "murs": self.walls}

    def conversion(self):
        board = self.board
        string = (
            f"Légende: 1={board['joueurs'][0]['nom']}, 2={board['joueurs'][1]['nom']}\n"
        )
        coords_first_player = board["joueurs"][0]["pos"]
        coords_second_player = board["joueurs"][1]["pos"]
        horizontal_walls = board["murs"]["horizontaux"]
        vertical_walls = board["murs"]["verticaux"]
        string += "   -----------------------------------\n"
        for y in range(9, 0, -1):
            string += f"{y} |"
            if (0, y) in horizontal_walls:
                string += "-"
            else:
                string += " "
            for x in range(1, 10):
                coords = (x, y)
                if coords == coords_first_player:
                    string += str(1)
                elif coords == coords_second_player:
                    string += str(2)
                else:
                    string += "."
                if (coords[0] + 1, coords[1]) in vertical_walls or (
                    coords[0] + 1,
                    coords[1] - 1,
                ) in vertical_walls:
                    string += " | "
                else:
                    string += "   "
            string = string[:-2]
            string += "|"
            if y != 1:
                string += "\n  | "
            print_line = False
            for x in range(1, 10):
                if print_line:
                    print_line = False
                    continue
                print_line = False
                coords = (x, y)
                if (coords[0], coords[1] - 1) in vertical_walls:
                    string = string[:-2]
                    string += "| "
                if coords in horizontal_walls:
                    if string[-1] != "|":
                        string = string[:-1]
                        string += "-------  "
                    print_line = True

                if print_line is not True:
                    string += "    "
            string = string[:-2]
            string += "|\n"
        string += "--|-----------------------------------\n"
        string += "  | 1   2   3   4   5   6   7   8   9\n"
        return string

    def is_reachable(self, initial_coords, new_coords):
        reachable_neigbours = self.get_reachable_neigbours(initial_coords)
        return new_coords in reachable_neigbours

    def get_reachable_neigbours(self, coords):
        graph = self.get_graph()
        return list(graph.successors(coords))

    def déplacer_jeton(self, player_number, coords):
        try:
            if not self.is_reachable(self.players[player_number - 1].coords, coords):
                raise QuoridorError("Invalid Move")
            self.players[player_number - 1].coords = coords
            return "D", coords
        except Exception as e:
            raise QuoridorError(e)

    def état_partie(self):
        return self.board

    def jouer_coup(self, player_number):
        graph = self.get_graph()
        player = self.players[player_number - 1]
        path = nx.shortest_path(graph, player.coords, player.objective)
        if len(path) > 1:
            if path[1] == player.objective:
                raise StopIteration(player.name)
            return self.déplacer_jeton(player_number, path[1])
        return None

    def partie_terminée(self):
        graph = self.get_graph()
        first_player = self.players[0]
        second_player = self.players[1]
        path = nx.shortest_path(graph, first_player.coords, first_player.objective)
        if path[1] == first_player.objective:
            return first_player.name
        path = nx.shortest_path(graph, second_player.coords, second_player.objective)
        if path[1] == second_player.objective:
            return second_player.name
        return None

    def placer_mur(self, player_number, position, orientation):
        try:
            player = self.players[player_number - 1]
            if player.number_walls <= 0:
                raise QuoridorError("The player has not any wall")
            if (
                position in self.walls["horizontaux"]
                or position in self.walls["verticaux"]
            ):
                raise QuoridorError("Invalid Move")
            self.walls[orientation].append(position)
            player.number_walls -= 1
        except Exception as e:
            raise QuoridorError(e)

    def get_graph(self):
        coords = [self.players[0].coords, self.players[1].coords]
        hor = self.walls["horizontaux"]
        ver = self.walls["verticaux"]
        return construire_graphe(coords, hor, ver)
