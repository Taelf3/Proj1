import requests

REQUEST_BASE = "https://python.gel.ulaval.ca"


def lister_parties(idul):
    url = REQUEST_BASE + "/quoridor/api/lister/"
    res = requests.get(url, params={"idul": idul}).json()
    if "message" in res:
        raise RuntimeError(res["message"])
    return res["parties"]


def initialiser_partie(idul):
    url = REQUEST_BASE + "/quoridor/api/initialiser/"
    res = requests.post(url, data={"idul": idul}).json()
    if "message" in res:
        raise RuntimeError(res["message"])
    return res["id"], res["état"]


def jouer_coup(id_partie, type_coup, position):
    url = REQUEST_BASE + "/quoridor/api/jouer/"
    res = requests.post(
        url, data={"id": id_partie, "type": type_coup, "pos": position}
    ).json()
    if "message" in res:
        raise RuntimeError(res["message"])
    if "gagnant" in res:
        raise StopIteration(res["gagnant"])
    return res["état"]
