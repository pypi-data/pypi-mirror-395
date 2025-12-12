class Curso:

    def __init__(self, nombre, duracion, link):
        self.nombre = nombre
        self.duracion = duracion
        self.link = link

    def __repr__(self): #también podría ser '__str__', pero en ese caso no se pueden listar a través de 'print(cursos)' -> o sea, van a seguir apareciendo como objetos || lo que hace 'repr' es generar una 'representación' para ese objeto
        return f"[+] Nombre del curso: [{self.nombre}].\n[+] Duración del curso: [{self.duracion} horas].\n[+] Link al curso: [{self.link}].\n\n"

cursos = [
        Curso("Introducción al juego", 19, "https://ole.com.ar"),
        Curso("Cómo mejorar tu TP", 23, "https://ole.com.ar/boca"),
        Curso("Aprendé a sideckear", 7, "https://ole.com.ar/seleccion"),
]

def listar_cursos():
    for curso in cursos:
        print(curso)

def buscar_por_nombre(nombre):
    for curso in cursos:
        if curso.nombre == nombre:
            return curso
    return None

aber = input(f"Hola, dame el nombre del curso que querés consultar:\n\n[?] ")

print(buscar_por_nombre(aber))
