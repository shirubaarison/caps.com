# Jogo da Velha dos dotados

Um jogo da velha na web, que teoricamente tem uma IA.

Agora está no ar, só que guarda os dados temporariamente (eu acho)! https://jogodaveiaep.onrender.com/ (demora para carregar se não tiver alguém on)

## Descrição

Pequeno projeto que estou fazendo para testar meus conhecimentos.
Não é muito complexo, apenas usei algumas coisas que aprendi durante o curso do CS50. Sei que tá muito longe do ideal, mas é uma forma que achei de me divertir codando algo. (a parte de bancos de dados está porca)

## Como rodar

### Depedências

Está tudo no arquivo requirements.txt
* Flask
* SQLAlchemy
* Werkzeug
* python-dateutil
* flask-session 

### Execução

```
git clone https://github.com/shirubaarison/jogoDaVeiaEP.git
cd jogoDaVeiaEP
pip install -r requirements.txt
```

Quando acabar de instalar as depedências, você precisa reiniciar o ambiente virtual (não sei porque isso acontece, talvez seja porque ele modifica algumas pastas no ambiente virtual).
Depois disso, é só executar:

```
flask run
```