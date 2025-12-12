"""
Extrae información del dispositivo desde la página operator del cargador EV.

Este script parsea el HTML de la página operator (obtenido después de autenticarse)
para extraer información del dispositivo como el link/texto que coincida con el DEVICE_ID.
"""

from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)


def extract_device_link_text(html_content: str, device_id: str) -> str | None:
    """
    Busca en el HTML un elemento que contenga el DEVICE_ID y devuelve su texto.

    Args:
        html_content: Contenido HTML de la página operator
        device_id: ID del dispositivo a buscar (ej: "6W0A19240050")

    Returns:
        Texto del elemento que contiene el DEVICE_ID, o None si no se encuentra.

    Raises:
        ValueError: Si el HTML no puede parsearse o está vacío.
    """
    if not html_content or not html_content.strip():
        logger.warning("HTML content está vacío")
        return None

    if not device_id:
        logger.warning("DEVICE_ID no proporcionado")
        return None

    try:
        soup = BeautifulSoup(html_content, "html.parser")

        # Buscar cualquier elemento (string) que contenga el DEVICE_ID
        pattern = re.compile(re.escape(device_id), re.IGNORECASE)
        matches = soup.find_all(string=pattern)

        if matches:
            # Retornar el primer match
            text = matches[0].strip()
            logger.info(f"Dispositivo encontrado en HTML: {text}")
            return text
        else:
            logger.debug(f"No se encontró elemento en HTML que contenga DEVICE_ID: {device_id}")
            return None

    except Exception as e:
        logger.error(f"Error al parsear HTML para extraer device info: {e}")
        raise ValueError(f"No se pudo parsear HTML: {e}")


def extract_all_device_links(html_content: str) -> dict:
    """
    Extrae todos los links de dispositivos disponibles en la página operator.

    Busca todos los elementos <a> con href que parecen ser dispositivos
    (generalmente URLs o IDs de dispositivos).

    Args:
        html_content: Contenido HTML de la página operator

    Returns:
        dict con:
            - "count": número de dispositivos encontrados
            - "devices": lista de dicts {"text", "href"} con los links encontrados
    """
    if not html_content or not html_content.strip():
        logger.warning("HTML content está vacío")
        return {"count": 0, "devices": []}

    try:
        soup = BeautifulSoup(html_content, "html.parser")

        devices = []
        # Buscar links (a href) que probablemente contengan dispositivos
        for link in soup.find_all("a", href=True):
            href = link.get("href", "").strip()
            text = link.get_text(strip=True)
            
            # Solo incluir links que tengan texto y href
            if href and text:
                logger.debug(f"Found link: text='{text}', href='{href}'")
                devices.append({
                    "text": text,
                    "href": href
                })

        logger.info(f"Se encontraron {len(devices)} dispositivos/links en HTML")
        if devices:
            logger.debug(f"Primeros 3 devices: {devices[:3]}")
        
        return {
            "count": len(devices),
            "devices": devices
        }

    except Exception as e:
        logger.error(f"Error al extraer links de dispositivos: {e}", exc_info=True)
        return {"count": 0, "devices": []}


def extract_device_info_summary(html_content: str, device_id: str = None) -> dict:
    """
    Extrae un resumen de información del dispositivo desde el HTML operator.

    Args:
        html_content: Contenido HTML de la página operator
        device_id: ID del dispositivo (opcional, para búsqueda específica)

    Returns:
        dict con:
            - "device_text": texto/nombre del dispositivo (si se proporciona device_id)
            - "all_devices": lista de todos los dispositivos encontrados
            - "total_devices": cantidad total de dispositivos
            - "page_title": título de la página
    """
    result = {
        "device_text": None,
        "all_devices": [],
        "total_devices": 0,
        "page_title": None,
    }

    if not html_content or not html_content.strip():
        logger.warning("HTML content está vacío")
        return result

    try:
        soup = BeautifulSoup(html_content, "html.parser")

        # Extraer título de la página
        title_tag = soup.find("title")
        if title_tag:
            result["page_title"] = title_tag.get_text(strip=True)

        # Si se proporciona device_id, buscar su texto
        if device_id:
            device_text = extract_device_link_text(html_content, device_id)
            result["device_text"] = device_text

        # Extraer todos los dispositivos disponibles
        devices_info = extract_all_device_links(html_content)
        result["all_devices"] = devices_info.get("devices", [])
        result["total_devices"] = devices_info.get("count", 0)

        logger.info(f"Resumen de info: página='{result['page_title']}', dispositivos={result['total_devices']}")
        return result

    except Exception as e:
        logger.error(f"Error al extraer resumen de info del dispositivo: {e}")
        return result
