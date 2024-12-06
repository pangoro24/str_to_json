def yaml_to_dict(yaml_str):
    def parse_line(line):
        # Determina el nivel de indentación y la clave-valor
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            return indent, key, value
        return indent, stripped, None

    def parse_yaml(lines):
        parsed = {}
        stack = [(parsed, -1)]  # (current_dict, current_indent)
        for line in lines:
            if not line.strip() or line.strip().startswith("#"):  # Ignorar líneas vacías o comentarios
                continue
            indent, key, value = parse_line(line)
            while stack and stack[-1][1] >= indent:
                stack.pop()  # Salir del nivel de indentación
            current_dict = stack[-1][0]
            if value is None:  # Es un subnivel (lista o dict)
                if key.startswith("-"):  # Elemento de una lista
                    key = key[1:].strip()
                    if not isinstance(current_dict, list):
                        current_dict[key] = []
                    stack.append((current_dict[key], indent))
                else:  # Es un diccionario
                    current_dict[key] = {}
                    stack.append((current_dict[key], indent))
            else:  # Es un valor
                current_dict[key] = parse_value(value)
        return parsed

    def parse_value(value):
        # Convierte valores a su tipo Python
        if value.lower() in ("true", "false"):
            return value.lower() == "true"
        elif value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            pass
        if value.startswith('"') and value.endswith('"') or value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        return value

    yaml_lines = yaml_str.split("\\n")
    return parse_yaml(yaml_lines)

# Ejemplo de uso
yaml_str = (
    "nombre: Ejemplo\\n"
    "edad: 30\\n"
    "habilidades:\\n"
    "  - Python\\n"
    "  - Seguridad\\n"
    "configuracion:\\n"
    "  tema: oscuro\\n"
    "  notificaciones: true"
)

result = yaml_to_dict(yaml_str)
print(result)  # Imprime como diccionario

# Convertir a JSON (opcional)
import json
print(json.dumps(result, indent=2))  # Imprime como JSON
