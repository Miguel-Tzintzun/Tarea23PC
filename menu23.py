import tarea23PC

def menu():
    url = input("Ingrese la URL: ")
    url_nueva = tarea23PC.verificador_nav(url)
    html = tarea23PC.conexion_request(url_nueva)
    
    print(html)


if __name__=='__main__':
    menu()
