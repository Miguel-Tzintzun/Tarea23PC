#! python3

import requests, bs4, os

def verificador_nav(url):
    if url.startswith("http://") or url.startswith("https://"):
        return url
    else:
        return "http://" + url
    
def conexion_request(url_nueva):
    os.makedirs('Imagenes', exist_ok=True)
    os.makedirs('PDFs', exist_ok=True)
    print('Descargando pagina %s...' % url_nueva)
    req = requests.get(url_nueva)
    sopa = bs4.BeautifulSoup(req.text, "html.parser")
    
    imagenes = sopa.find_all('img')
    if imagenes == []:
        print('No se encontró.')
    else:
        for img in imagenes:
            imagenesUrl = img.get('src')
            if imagenesUrl.startswith("http"):
                print('Descargando %s...' % (imagenesUrl))
                response = requests.get(imagenesUrl)
                if response.status_code == 200:
                    imageFile = open(os.path.join('Imagenes', os.path.basename(imagenesUrl)),'wb')
                    for chunk in response.iter_content(100000):
                        imageFile.write(chunk)
                    imageFile.close()
            else:
                print('Descargando %s...' % (imagenesUrl))
                imagenesUrl = url_nueva + imagenesUrl
                response = requests.get(imagenesUrl)
                if response.status_code == 200:
                    imageFile = open(os.path.join('Imagenes', os.path.basename(imagenesUrl)),'wb')
                    for chunk in response.iter_content(100000):
                        imageFile.write(chunk)
                    imageFile.close()
    
    hipervinculos = sopa.find_all('a')
    with open("hipervinculos.txt", "w") as f:
        for hi in hipervinculos:
            link = hi.get("href")
            if link:
                f.write(link + "\n")
        print("Se guardaron correctamente los hipervinculos")

    
    PDFs = sopa.find_all('a')
    for p in PDFs:
        if ('.pdf' in p.get('href', [])):
            response = requests.get(p.get('href'))
            nombre = p.get('href')
            pdf = open(os.path.join('PDFs', os.path.basename(nombre)), 'wb')
            pdf.write(response.content)
            pdf.close()
            print("archivo ", nombre , " fue descargado")
    print("Se descargaron todos los PDFs")

