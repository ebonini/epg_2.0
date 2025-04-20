import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime

# URL da programação
url = "https://canalgoat.com.br/programacao/"

# Função para buscar e processar a programação
def fetch_programming(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar a URL. Código de status: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")

    # Substitua as classes ou tags abaixo conforme o site
    shows = soup.find_all("div", class_="show-item")  # Exemplo de classe
    
    programming = []
    for show in shows:
        title = show.find("h3").text.strip()  # Substitua pela tag ou classe correta
        time = show.find("span", class_="time").text.strip()  # Substitua pela tag ou classe correta
        programming.append({"title": title, "time": time})
    
    return programming

# Função para converter para XMLTV
def convert_to_xmltv(programming):
    tv = ET.Element("tv")
    channel = ET.SubElement(tv, "channel", id="canalgoat")
    ET.SubElement(channel, "display-name").text = "Canal Goat"

    for show in programming:
        program = ET.SubElement(tv, "programme", start=convert_time(show["time"]), channel="canalgoat")
        ET.SubElement(program, "title").text = show["title"]
    
    tree = ET.ElementTree(tv)
    tree.write("programacao.xml", encoding="utf-8", xml_declaration=True)
    print("Arquivo XMLTV gerado com sucesso!")

# Função para formatar o tempo no formato XMLTV
def convert_time(time_str):
    # Converta para o formato adequado, ex.: "20250420150000 +0000"
    dt = datetime.strptime(time_str, "%H:%M")  # Exemplo de formato de entrada
    return dt.strftime("%Y%m%d%H%M%S +0000")

# Execução do script
try:
    programming = fetch_programming(url)
    convert_to_xmltv(programming)
except Exception as e:
    print(f"Erro: {e}")
