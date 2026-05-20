class Usuario:
    def __init__(self, nombre, email, password, rol, tipo_servicio=None, id=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.rol = rol
        self.tipo_servicio = tipo_servicio
        
    
    def __str__(self):
        return f"{self.nombre} - {self.email} - {self.rol}"