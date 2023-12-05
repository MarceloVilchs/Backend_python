from datetime import datetime

def ejemplo_fecha_iso():
    fecha_iso = "dd-MM-yyyy"  # Ejemplo de fecha en formato ISO
    fecha_python = datetime.fromisoformat(fecha_iso)
    return fecha_python
