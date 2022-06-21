# Pegar formulário de inscrição do bingo que contenha email/nome. Gerar cartelas de bingo para cada
# participante, cada cartela deverá conter o nome do participante, as cartelas deverão ser enviadas para
# os respectivos donos por email.
import sys
import pandas as pd
import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = ""
password = ""


def main():
    players = get_bingo_players()
    for index, player in enumerate(players.itertuples()):
        card = create_card(player)
        send_email(player, card)
        progress_bar(len(players), index)


def get_bingo_players():
    # 1 Pegar o email/nome dos participantes.
    csv = pd.read_csv('bingo.csv', usecols=['NOME', 'EMAIL', 'BINGO'], chunksize=10)
    players = pd.concat((x.query("BINGO == 'SIM'") for x in csv), ignore_index=True)
    return players


def create_card(player):
    # 2 Gerar cartelas de bingo com o respectivo nome.
    resposta = requests.get(f"http://www.profcardy.com/artigos/bingo.php?frase={player.NOME}")
    return resposta.text


def send_email(player, card):
    # 3 Enviar a cartela por email para o respectivo dono da cartela.
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "test"
    msg["From"] = sender_email
    msg["To"] = player.EMAIL

    part = MIMEText(card, "html")
    msg.attach(part)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, msg["To"], msg.as_string()
        )


def progress_bar(total, progress):
    bar_length, status = 20, ""
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(bar_length * progress))
    text = "\r[{}] {:.0f}% {}".format(
        "#" * block + "-" * (bar_length - block), round(progress * 100, 0),
        status)
    sys.stdout.write(text)
    sys.stdout.flush()


if __name__ == '__main__':
    main()
