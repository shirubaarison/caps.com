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
        "Hernandes" 
    ]

def selecionarAdversario():
    jogador = random.choice(jogadores)

    return jogador

def selecionarFoto(jogador):
    fotos = {
        "RianOli69": "rian.jpg",
        "ErikMaia15": "erik.webp",
        "Alysson": "alison.webp",
        "ErikGleyson": "gleison.jpg",
        "Davi kwai": "davi.jpg",
        "Gusgabr": "gusga.jpg",
        "Joao mito": "jv.webp",
        "Tikonissin": "vruan.jpg",
        "Thiago": "thiago.jpg",
        "Kaue (KJ vlogs)": "kaue.jpg",
        "Fabio Futsal": "fabio.jpg",
        "Ian Marrom": "ian.jpg",
        "Hernandes": "hernandes.jpg" 
    }

    return fotos[jogador]