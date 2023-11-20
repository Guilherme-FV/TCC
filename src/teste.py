from math import radians, cos, sin, sqrt, atan2, degrees

def calcular_media_cartesiana(localizacoes):
    # Converter de latitude e longitude para coordenadas cartesianas
    coordenadas_cartesianas = []
    for lat, lon in localizacoes:
        # Converter graus para radianos
        lat_rad = radians(lat)
        lon_rad = radians(lon)

        # Raio da Terra em km
        raio_terra = 6371.0

        # Converter para coordenadas cartesianas
        x = raio_terra * cos(lat_rad) * cos(lon_rad)
        y = raio_terra * cos(lat_rad) * sin(lon_rad)
        coordenadas_cartesianas.append((x, y))

    # Calcular a média das coordenadas cartesianas
    media_x = sum(x for x, _ in coordenadas_cartesianas) / len(coordenadas_cartesianas)
    media_y = sum(y for _, y in coordenadas_cartesianas) / len(coordenadas_cartesianas)

    # Converter a média de volta para latitude e longitude
    media_lon = atan2(media_y, media_x)
    media_lat = atan2(sqrt(media_x ** 2 + media_y ** 2), raio_terra)

    # Converter de radianos para graus
    media_lat = degrees(media_lat)
    media_lon = degrees(media_lon)

    return media_lat, media_lon

# Exemplo de uso
localizacoes = [(37.42, -122.08), (-27.61, -48.58)]
media = calcular_media_cartesiana(localizacoes)
print(f"A média cartesiana das localizações é: {media}")
