from lxml import html
import requests

def get_clean_text_from_url(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    
    # Filtra apenas elementos de texto relevantes
    text_elements = tree.xpath('//p | //h1 | //h2 | //h3 | //h4 | //h5 | //h6 | //div[@style="text-align: center;"] | //div[@style="text-align: justify;"]')
    
    # Extrai e limpa o texto
    clean_text = "\n".join(
        [element.text_content().strip() for element in text_elements if element.text_content().strip()]
    )

    return clean_text

url = "https://brasilcristao-contra-o-comunismo.blogspot.com"
text = get_clean_text_from_url(url)
print(text)