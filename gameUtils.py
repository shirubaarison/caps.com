import random


jogadores = [
        "RianOli69",
        "ErikMaia15",
        "Alysson",
        "ErikGleyson",
        "Davi kwai",
        "Gusgabr",
        "Joao mito",
        "Tikonissin",
        "Thiago",
        "Kaue (KJ vlogs)",
        "Fabio Futsal",
        "Ian Marrom",
        "Hernandes",
        "Cainho"
    ]


def selecionarAdversario():
    jogador = random.choice(jogadores)

    return jogador


def selecionarFoto(jogador):
    fotos = {
        "RianOli69": "rian.jpg",
        "ErikMaia15": "erik.jpeg",
        "Alysson": "alison.webp",
        "ErikGleyson": "gleison.jpeg",
        "Davi kwai": "davi.jpg",
        "Gusgabr": "gusga.jpg",
        "Joao mito": "jv.webp",
        "Tikonissin": "vruan.jpeg",
        "Thiago": "thiago.jpeg",
        "Kaue (KJ vlogs)": "kaue.jpg",
        "Fabio Futsal": "fabio.jpg",
        "Ian Marrom": "ian.jpeg",
        "Hernandes": "hernandes.jpg",
        "Cainho": "caio.jpeg"
    }

    return fotos[jogador]