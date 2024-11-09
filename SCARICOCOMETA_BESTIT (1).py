import requests
import os
from tqdm import tqdm
from urllib.parse import urlparse
from ftplib import FTP

# Definisci i link dei file XML da scaricare
xml_urls = [
    "http://dati.cometanet.net:20000/xml/AnagraficaArticoli.ashx?user=11106&pass=bnoinformatica",
    "http://dati.cometanet.net:20000/xml/Listino.ashx?user=11106&pass=bnoinformatica",
    "http://dati.cometanet.net:20000/xml/SchedeArticoli.ashx?user=11106&pass=bnoinformatica"
]

# Percorso della cartella di destinazione
destination_folder = r'c:\import\source'

# Crea la cartella se non esiste
os.makedirs(destination_folder, exist_ok=True)

# Scarica i file XML
for url in xml_urls:
    # Estrai il nome del file dal link
    file_name = os.path.basename(urlparse(url).path)
    file_name = os.path.splitext(file_name)[0] + ".xml"  # Aggiungi l'estensione .xml
    destination_file = os.path.join(destination_folder, file_name)

    # Effettua la richiesta HTTP per ottenere le informazioni sul file
    response = requests.head(url)
    total_size = int(response.headers.get('Content-Length', 0))

    # Download del file con una barra di avanzamento verde
    with requests.get(url, stream=True) as r, open(destination_file, 'wb') as file, tqdm(
            unit='B', unit_scale=True, unit_divisor=1024, total=total_size, desc=f"Download {file_name}", bar_format="{l_bar}{bar} \033[92m{percentage:3.0f}%\033[0m") as progress_bar:
        for data in r.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

    print(f"File scaricato e salvato: {destination_file}")

# Scarica il file tramite FTP
ftp_host = "ftp.thegarageassistenza.it"
ftp_user = "thegarageassistenza-6"
ftp_password = "L-7hUYbuA4Ng.80J"
ftp_file = "EsportaArticoli.txt"

# Connettiti al server FTP
ftp = FTP(ftp_host)
ftp.login(user=ftp_user, passwd=ftp_password)

# Scarica il file
ftp.cwd("/")
destination_file = os.path.join(destination_folder, ftp_file)
with open(destination_file, 'wb') as file:
    ftp.retrbinary(f"RETR {ftp_file}", file.write)

print(f"File scaricato e salvato: {destination_file}")

# Chiudi la connessione FTP
ftp.quit()
