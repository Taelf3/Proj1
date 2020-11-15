class Player:
    def __init__(self, name, coords, number_walls, idx):
        self.name = name
        self.coords = tuple(coords)
        self.number_walls = number_walls
        self.idx = idx

    def __str__(self):
        return f"{self.idx}. {self.name} : {self.coords} - {self.number_walls}"

    @property
    def objective(self):
        return f"B{self.idx}"

    def to_json(self):
        self.coords = tuple(self.coords)
        return {"nom": self.name, "murs": self.number_walls, "pos": self.coords}
