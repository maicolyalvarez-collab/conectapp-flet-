class Usuario:
    def __init__(self, nombre, email, password, rol, id=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.rol = rol
    
    def __str__(self):
        return f"{self.nombre} - {self.email} - {self.rol}"