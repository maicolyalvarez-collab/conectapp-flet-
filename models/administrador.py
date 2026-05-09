from models.usuario import Usuario

class Administrador(Usuario):
    def __init__(self,nombre,correo):
        super().__init__(nombre,correo,"admin")
    
    def ver_reportes(self):
        print("Mostrando reportes")