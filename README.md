# identifyfood

Made by Victor Antonio Menuzzo and Paula Giovanna Rodrigues(gitlab.com/paula_portfolio)

1-para rodar o arquivo de visualização dos superpixels com mascara para
identificarmos o rótulo de cada superpixel abra o terminal do linux e digite:
python identificaSP.py --image [local e nome da imagem]
após o --image tem que ser informado o nome exato da imagem

2-para rodar o arquivo que extrai as features que serão inseridas no banco de
dados, coloque dentro do vetor de fundo, prato, alimentos os rotulos obtidos e
escreva no terminal do linux:
python criaDados.py
lembre de fornecer o nome da imagem dentro do código

3-para rodar o arquivo de classificação forneça a imagem de teste no código e
digite no terminal do linux:
python classifica.py

