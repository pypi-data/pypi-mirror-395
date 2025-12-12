import asyncio
from fastmcp import FastMCP, Context
import aiohttp
import os
import json
from dotenv import load_dotenv
import ssl
import re
import logging
import tempfile
from pathlib import Path
from bs4 import BeautifulSoup
from scriptsWebScrapping.extract_warnings import extract_warnings
from scriptsWebScrapping.extract_sessions import extract_sessions
from scriptsWebScrapping.extract_syslog import extract_syslog, parse_syslog_date
from scriptsWebScrapping.extract_device_info import extract_device_link_text, extract_device_info_summary

mcp = FastMCP("EV Charger MCP Server")

# Cargar el archivo .env (intentar varias rutas: cwd y directorio del script)
from pathlib import Path as _Path
_script_dir = _Path(__file__).resolve().parent
_cwd = _Path.cwd()
# Intentar cargar .env del cwd primero, luego del directorio del script
load_dotenv(dotenv_path=_cwd / ".env", override=False)
load_dotenv(dotenv_path=_script_dir / ".env", override=False)

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Bandera global para controlar impresión de env en tiempo de ejecución
DEBUG_PRINT_ENV = os.getenv("DEBUG_PRINT_ENV", "false").lower() in ("1", "true", "yes")


def _maybe_log_env(location: str = ""):
    """Si DEBUG_PRINT_ENV está activado, imprime un subset enmascarado del entorno actual.

    location: cadena que indica el punto desde donde se llama (p. ej. 'startup' o 'obtener_warnings')
    """
    if not DEBUG_PRINT_ENV:
        return

    keys_to_show = [
        "CHARGER_HOST",
        "CHARGER_USERNAME",
        "CHARGER_PASSWORD",
        "DEVICE_ID",
        "VERIFY_SSL",
        "MCP_HOST",
        "MCP_PORT",
        "SSL_CERT_PATH",
    ]
    shown = {k: _mask_val(k, os.getenv(k)) for k in keys_to_show}
    logger.info(f"ENV ({location}) (masked): {shown}")


def _mask_val(k: str, v: str | None):
    if v is None:
        return None
    lk = k.lower()
    if "pass" in lk or "secret" in lk or "token" in lk or "key" in lk or "pwd" in lk:
        return "***"
    return v

def get_ssl_context():
    """
    Crea y configura el contexto SSL basado en las variables de entorno.
    
    Variables de entorno:
    - VERIFY_SSL: "true" o "false" para habilitar/deshabilitar verificación SSL
    - SSL_CERT_PATH: Ruta al archivo de certificado de confianza (opcional)
    
    Returns:
        ssl.SSLContext configurado según las variables de entorno
    """
    verify_ssl = os.getenv("VERIFY_SSL", "false").lower() == "true"
    ssl_cert_path = os.getenv("SSL_CERT_PATH")
    
    ssl_context = ssl.create_default_context()
    
    if not verify_ssl:
        # Deshabilitar verificación SSL
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        logger.info("SSL verification deshabilitado")
    else:
        # Habilitar verificación SSL
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        
        if ssl_cert_path:
            if not Path(ssl_cert_path).exists():
                logger.error(f"Archivo de certificado no encontrado: {ssl_cert_path}")
                raise FileNotFoundError(f"Certificado SSL no encontrado: {ssl_cert_path}")
            
            ssl_context.load_verify_locations(ssl_cert_path)
            logger.info(f"Certificado SSL cargado desde: {ssl_cert_path}")
        else:
            logger.info("Usando certificados del sistema para verificación SSL")
    
    return ssl_context

class ChargerSession:
    """Maneja la sesión autenticada con el cargador"""
    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username
        self.password = password
        self.cookies = None
        self.stok = None
        self.device_id = None  # Se obtendrá mediante web scraping o fallback a env var
        self.ssl_context = get_ssl_context()
        self._client: aiohttp.ClientSession | None = None
        # Headers that mimic a browser to avoid simple UA-based blocking
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) EVChargers_MCP/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
    
    async def authenticate(self):
        """Autentica y obtiene las cookies de sesión"""
        url = f"https://{self.host}/cgi-bin/webmanager/{self.username}"  ###########
        payload = {
            "luci_username": self.username,
            "luci_password": self.password
        }
        
        # Primero, usar DEVICE_ID del .env como fallback
        fallback_device_id = os.getenv("DEVICE_ID")
        if fallback_device_id:
            self.device_id = fallback_device_id
            logger.info(f"✓ DEVICE_ID desde .env (fallback): {self.device_id}")
        
        stok_found = False
        try:
            # Create a persistent client session to preserve cookies and headers
            self._client = aiohttp.ClientSession(headers=self.headers)
            async with self._client.post(url, data=payload, ssl=self.ssl_context, allow_redirects=False, timeout=aiohttp.ClientTimeout(total=30)) as response:
                # aiohttp keeps cookies in the session's cookie_jar
                # Save a shallow mapping for legacy uses
                try:
                    self.cookies = {k: v.value for k, v in response.cookies.items()}
                except Exception:
                    self.cookies = response.cookies

                # Extraer stok del header Location
                location = response.headers.get("Location", "")
                if location:
                    # Buscar patrón stok=xxxxx en la URL
                    match = re.search(r"stok=([a-f0-9]+)", location)
                    if match:
                        self.stok = match.group(1)
                        logger.info(f"Token STOK obtenido: {self.stok}")
                        stok_found = True
                    else:
                        logger.warning(f"No se encontró STOK en Location header")
                        return False
                else:
                    logger.warning(f"No se encontró Location header en autenticación")
                    return False
        except Exception as e:
            logger.error(f"Error durante autenticación POST: {str(e)}")
            # Close client if it was partially created
            try:
                if self._client:
                    await self._client.close()
            except Exception:
                pass
            return False

        # Si no se encontró STOK, retornar False
        if not stok_found:
            return False

        # Después de obtener el STOK, hacer GET a la página operator para obtener el HTML y extraer el device_id
        # Esta sección SÍ se ejecuta después del POST exitoso
        try:
            operator_url = f"https://{self.host}/cgi-bin/webmanager/{self.username}"   ######
            async with self._client.get(operator_url, ssl=self.ssl_context, timeout=aiohttp.ClientTimeout(total=30)) as op_response:
                if op_response.status in [200, 403]:  # Aceptar 200 y 403
                    self.operator_html = await op_response.text()
                    logger.info(f"HTML operator descargado exitosamente ({len(self.operator_html)} bytes)")
                    
                    # Intentar extraer DEVICE_ID del HTML operator (mejorar el fallback)
                    try:
                        device_summary = extract_device_info_summary(self.operator_html, None)
                        logger.info(f"=== Device summary completo: {device_summary}")
                        logger.info(f"=== Device summary keys: {device_summary.keys() if device_summary else 'None'}")
                        logger.info(f"=== all_devices: {device_summary.get('all_devices') if device_summary else 'None'}")
                        logger.info(f"=== total_devices: {device_summary.get('total_devices') if device_summary else 'None'}")
                        
                        if device_summary and device_summary.get('all_devices'):
                            all_devices = device_summary.get('all_devices')
                            logger.info(f"=== Número de devices encontrados: {len(all_devices)}")
                            logger.info(f"=== Primeros 3 devices: {all_devices[:3] if len(all_devices) >= 3 else all_devices}")
                            
                            first_link = all_devices[0]
                            logger.info(f"=== First link: {first_link}")
                            logger.info(f"=== First link type: {type(first_link)}")
                            
                            if isinstance(first_link, dict) and first_link.get('text'):
                                device_text = first_link['text'].strip()
                                logger.info(f"=== Device text: '{device_text}'")
                                
                                device_id_match = re.match(r"([A-Z0-9]+)", device_text)
                                if device_id_match:
                                    extracted_id = device_id_match.group(1)
                                    self.device_id = extracted_id
                                    logger.info(f"✓ DEVICE_ID extraído mediante web scraping: {self.device_id}")
                                else:
                                    logger.info(f"=== No se pudo hacer match de regex con: {device_text}")
                            else:
                                logger.info(f"=== First link no es dict o no tiene 'text': {first_link}")
                        else:
                            logger.info(f"=== device_summary es None o no tiene 'all_devices': {device_summary}")
                    except Exception as e:
                        logger.error(f"=== Error al extraer DEVICE_ID del HTML: {e}", exc_info=True)
                        # El fallback ya está asignado arriba
                else:
                    logger.warning(f"GET a operator devolvió status {op_response.status}, usando fallback")
        except Exception as e:
            logger.debug(f"Error al obtener HTML operator: {e}")
            # El fallback ya está asignado arriba

        return True

    def fetch(self, url: str):
        """Return the coroutine for a GET request using the persistent session.

        Callers should use: `async with session.fetch(url) as response:`
        """
        if not self._client:
            # create a default client if authenticate wasn't called
            self._client = aiohttp.ClientSession(headers=self.headers)

        # Prepare headers: add Referer and X-Requested-With to mimic browser navigation
        headers = dict(self.headers)
        headers.setdefault("Referer", f"https://{self.host}/cgi-bin/webmanager/{self.username}")
        headers.setdefault("X-Requested-With", "XMLHttpRequest")

        # Prepare cookies: include known cookies and stok if present
        cookies = {}
        try:
            if isinstance(self.cookies, dict):
                cookies.update(self.cookies)
        except Exception:
            pass
        if self.stok:
            # Some devices expect stok both in URL and as a cookie
            cookies.setdefault("stok", self.stok)

        return self._client.get(url, ssl=self.ssl_context, timeout=aiohttp.ClientTimeout(total=30), headers=headers, cookies=cookies)

    async def close(self):
        try:
            if self._client:
                await self._client.close()
                # ensure connector is closed
                try:
                    conn = getattr(self._client, 'connector', None)
                    if conn is not None:
                        await conn.close()
                except Exception:
                    pass
                self._client = None
        except Exception:
            pass

@mcp.tool
async def obtener_warnings(ctx: Context, days: int = None, start_date: str = None, end_date: str = None):
    """
    Obtiene y procesa los warnings del cargador EV.
    
    Descarga el HTML, lo convierte a CSV y devuelve los datos procesados.
    
    Args:
        days: Últimos N días a incluir (ej: 7, 30) (opcional)
        start_date: Fecha de inicio (formato: YYYY-MM-DD) (opcional)
        end_date: Fecha de fin (formato: YYYY-MM-DD) (opcional)
    
    Returns:
        dict con status, count, filtered_count y lista de warnings
    """
    try:
        # Log environment for debugging (si está activado)
        _maybe_log_env("obtener_warnings")

        host = os.getenv("CHARGER_HOST")
        username = os.getenv("CHARGER_USERNAME")
        password = os.getenv("CHARGER_PASSWORD")
        
        logger.info("Iniciando obtener_warnings")
        
        if not host or not username or not password:
            error_msg = "Las variables CHARGER_HOST, CHARGER_USERNAME o CHARGER_PASSWORD no están definidas. Asegúrate de que .env exista en el directorio correcto o que el cliente esté pasando el entorno al proceso hijo. Puedes activar DEBUG_PRINT_ENV=true para que el servidor imprima las variables enmascaradas al arrancar."
            logger.error(error_msg)
            await ctx.error(error_msg)
            return
        
        session = ChargerSession(host, username, password)
        authenticated = await session.authenticate()
        
        if not authenticated or not session.stok:
            error_msg = "Falló la autenticación con el cargador o no se obtuvo stok"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return
        
        if not session.device_id:
            error_msg = "No se pudo obtener DEVICE_ID ni de web scraping ni de variable de entorno"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return
        
        url = f"https://{host}/cgi-bin/webmanager/;stok={session.stok}/{username}/charging/{session.device_id}/warnings"
        
        logger.info(f"Descargando warnings desde {url}")
        
        # Descargar HTML usando la sesión persistente para preservar cookies y cabeceras
        try:
            async with await session.fetch(url) as response:
                if response.status != 200:
                    # Log additional response info for debugging 403
                    body_snippet = await response.text()
                    logger.error(f"Error al descargar warnings: status {response.status}")
                    logger.debug(f"Response headers: {dict(response.headers)}")
                    logger.debug(f"Response body (snippet): {body_snippet[:1000]}")
                    await ctx.error(f"Error al descargar warnings: status {response.status}")
                    return

                html_content = await response.text()
                logger.info(f"HTML descargado exitosamente ({len(html_content)} bytes)")
        except Exception as e:
            logger.error(f"Exception al descargar warnings: {e}")
            await ctx.error(f"Exception al descargar warnings: {e}")
            return
        
        # Guardar HTML en archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
            tmp.write(html_content)
            temp_html_path = tmp.name
        
        try:
            # Procesar HTML con extract_warnings
            logger.info("Procesando HTML con extract_warnings")
            result = extract_warnings(
                input_file=temp_html_path,
                days=days,
                start_date=start_date,
                end_date=end_date,
                return_data=True
            )
            
            logger.info(f"Warnings procesados: {result['count']} registros extraídos")
            
            return {
                "status": 200,
                "count": result["count"],
                "filtered_count": result["filtered_count"],
                "data": result["data"]
            }
        
        finally:
            # Limpiar archivo temporal
            Path(temp_html_path).unlink(missing_ok=True)
            # Cerrar sesión HTTP del ChargerSession
            try:
                await session.close()
            except Exception:
                pass
    
    except Exception as e:
        logger.error(f"Error en obtener_warnings: {str(e)}")
        await ctx.error(f"Error: {str(e)}")

@mcp.tool
async def obtener_sessions(ctx: Context, days: int = None, start_date: str = None, end_date: str = None):
    """
    Obtiene y procesa las sesiones del cargador EV.
    
    Descarga el HTML, lo convierte a CSV y devuelve los datos procesados.
    
    Args:
        days: Últimos N días a incluir (ej: 7, 30) (opcional)
        start_date: Fecha de inicio (formato: YYYY-MM-DD) (opcional)
        end_date: Fecha de fin (formato: YYYY-MM-DD) (opcional)
    
    Returns:
        dict con status, count, filtered_count y lista de sesiones
    """
    try:
        # Log environment for debugging (si está activado)
        _maybe_log_env("obtener_sessions")

        host = os.getenv("CHARGER_HOST")
        username = os.getenv("CHARGER_USERNAME")
        password = os.getenv("CHARGER_PASSWORD")
        
        logger.info("Iniciando obtener_sessions")
        
        if not host or not username or not password:
            error_msg = "Las variables CHARGER_HOST, CHARGER_USERNAME o CHARGER_PASSWORD no están definidas. Asegúrate de que .env exista en el directorio correcto o que el cliente esté pasando el entorno al proceso hijo. Puedes activar DEBUG_PRINT_ENV=true para que el servidor imprima las variables enmascaradas al arrancar."
            logger.error(error_msg)
            await ctx.error(error_msg)
            return
        
        session = ChargerSession(host, username, password)
        authenticated = await session.authenticate()
        
        if not authenticated or not session.stok:
            error_msg = "Falló la autenticación con el cargador o no se obtuvo stok"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return
        
        if not session.device_id:
            error_msg = "No se pudo obtener DEVICE_ID ni de web scraping ni de variable de entorno"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return
        
        url = f"https://{host}/cgi-bin/webmanager/;stok={session.stok}/{username}/charging/{session.device_id}/sessions"
        
        logger.info(f"Descargando sessions desde {url}")
        
        # Descargar HTML usando la sesión persistente para preservar cookies y cabeceras
        try:
            async with await session.fetch(url) as response:
                if response.status != 200:
                    body_snippet = await response.text()
                    logger.error(f"Error al descargar sessions: status {response.status}")
                    logger.debug(f"Response headers: {dict(response.headers)}")
                    logger.debug(f"Response body (snippet): {body_snippet[:1000]}")
                    await ctx.error(f"Error al descargar sessions: status {response.status}")
                    return

                html_content = await response.text()
                logger.info(f"HTML descargado exitosamente ({len(html_content)} bytes)")
        except Exception as e:
            logger.error(f"Exception al descargar sessions: {e}")
            await ctx.error(f"Exception al descargar sessions: {e}")
            return
        
        # Guardar HTML en archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
            tmp.write(html_content)
            temp_html_path = tmp.name
        
        try:
            # Procesar HTML con extract_sessions
            logger.info("Procesando HTML con extract_sessions")
            result = extract_sessions(
                input_file=temp_html_path,
                days=days,
                start_date=start_date,
                end_date=end_date,
                return_data=True
            )
            
            logger.info(f"Sessions procesadas: {result['count']} registros extraídos")
            
            return {
                "status": 200,
                "count": result["count"],
                "filtered_count": result["filtered_count"],
                "data": result["data"]
            }
        
        finally:
            # Limpiar archivo temporal
            Path(temp_html_path).unlink(missing_ok=True)
            # Cerrar sesión HTTP del ChargerSession
            try:
                await session.close()
            except Exception:
                pass
    
    except Exception as e:
        logger.error(f"Error en obtener_sessions: {str(e)}")
        await ctx.error(f"Error: {str(e)}")

@mcp.tool
async def obtener_logs(ctx: Context, days: int = None, start_date: str = None, end_date: str = None, limit: int = None, keywords: str = None, margin: int = None):
    """
    Obtiene y procesa los logs del sistema (syslog) del cargador EV.
    
    Descarga el HTML, lo extrae del textarea y devuelve los datos procesados.
    
    Args:
        days: Últimos N días a incluir (ej: 7, 30) (opcional)
        start_date: Fecha de inicio (formato: YYYY-MM-DD) (opcional)
        end_date: Fecha de fin (formato: YYYY-MM-DD) (opcional)
        limit: Si se proporciona (int), devuelve únicamente los últimos `limit` registros
               más recientes dentro del rango filtrado (opcional)
        keywords: String con keywords separadas por comas para filtrar logs (ej: "error,warning,critical")
                 Los logs se filtraran para incluir solo aquellos que contengan alguno de estos keywords.
                 La búsqueda es case-insensitive (opcional)
        margin: Número de líneas hacia arriba y hacia abajo para incluir alrededor de cada match (default: 0).
               Solo se aplica si se proporciona keywords (opcional)
    
    Returns:
        Si keywords no se usa: dict con keys: "status", "count", "filtered_count", "data"
        Si keywords se usa: dict con keys: "status", "total_count", "filtered_count", "keyword_matches", "returned_count", "data"
           - "total_count": número total de líneas encontradas
           - "filtered_count": número de líneas en el rango de fechas
           - "keyword_matches": número de líneas que coinciden con los keywords
           - "returned_count": número de líneas devueltas (con márgenes)
           - "data": lista de líneas filtradas por keywords + márgenes
    
        Ejemplos:
           await session.call_tool("obtener_logs", {"days": 7, "limit": 100})
           await session.call_tool("obtener_logs", {"keywords": "error,ERROR", "margin": 2})
           await session.call_tool("obtener_logs", {"days": 7, "keywords": "critical", "margin": 3, "limit": 50})
    """
    try:
        # Log environment for debugging (si está activado)
        _maybe_log_env("obtener_logs")

        host = os.getenv("CHARGER_HOST")
        username = os.getenv("CHARGER_USERNAME")
        password = os.getenv("CHARGER_PASSWORD")
        
        logger.info("Iniciando obtener_logs")
        
        if not host or not username or not password:
            error_msg = "Las variables CHARGER_HOST, CHARGER_USERNAME o CHARGER_PASSWORD no están definidas. Asegúrate de que .env exista en el directorio correcto o que el cliente esté pasando el entorno al proceso hijo. Puedes activar DEBUG_PRINT_ENV=true para que el servidor imprima las variables enmascaradas al arrancar."
            logger.error(error_msg)
            await ctx.error(error_msg)
            return
        
        session = ChargerSession(host, username, password)
        authenticated = await session.authenticate()
        
        if not authenticated or not session.stok:
            error_msg = "Falló la autenticación con el cargador o no se obtuvo stok"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return
        
        if not session.device_id:
            error_msg = "No se pudo obtener DEVICE_ID ni de web scraping ni de variable de entorno"
            logger.error(error_msg)
            await ctx.error(error_msg)
            return
        
        url = f"https://{host}/cgi-bin/webmanager/;stok={session.stok}/{username}/system/syslog/{session.device_id}"
        
        logger.info(f"Descargando logs desde {url}")
        
        # Descargar HTML usando la sesión persistente para preservar cookies y cabeceras
        try:
            async with await session.fetch(url) as response:
                if response.status != 200:
                    body_snippet = await response.text()
                    logger.error(f"Error al descargar logs: status {response.status}")
                    logger.debug(f"Response headers: {dict(response.headers)}")
                    logger.debug(f"Response body (snippet): {body_snippet[:1000]}")
                    await ctx.error(f"Error al descargar logs: status {response.status}")
                    return

                html_content = await response.text()
                logger.info(f"HTML descargado exitosamente ({len(html_content)} bytes)")
        except Exception as e:
            logger.error(f"Exception al descargar logs: {e}")
            await ctx.error(f"Exception al descargar logs: {e}")
            return
        
        # Guardar HTML en archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
            tmp.write(html_content)
            temp_html_path = tmp.name
        
        try:
            # Procesar HTML con extract_syslog
            logger.info("Procesando HTML con extract_syslog")
            result = extract_syslog(
                input_file=temp_html_path,
                days=days,
                start_date=start_date,
                end_date=end_date,
                return_data=True
            )
            
            logger.info(f"Logs procesados: {result['count']} líneas extraídas")

            data_lines = result.get("data", [])
            
            # Aplicar filtrado por keywords si se proporciona
            if keywords:
                logger.info(f"Filtrado por keywords: {keywords}")
                margin = margin or 0
                
                # Parsear keywords
                keyword_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]
                
                if keyword_list:
                    # Encontrar índices de líneas que coinciden con keywords
                    match_indices = []
                    for idx, line in enumerate(data_lines):
                        line_lower = line.lower()
                        if any(kw in line_lower for kw in keyword_list):
                            match_indices.append(idx)
                    
                    # Expandir los índices con márgenes
                    result_indices = set()
                    for idx in match_indices:
                        # Agregar el rango [idx - margin, idx + margin]
                        start = max(0, idx - margin)
                        end = min(len(data_lines), idx + margin + 1)
                        for i in range(start, end):
                            result_indices.add(i)
                    
                    # Ordenar los índices y extraer las líneas
                    sorted_indices = sorted(result_indices)
                    filtered_lines = [data_lines[i] for i in sorted_indices]
                    
                    logger.info(f"Keywords encontrados: {len(match_indices)} líneas coincidentes, {len(filtered_lines)} líneas con márgenes")
                    
                    # Aplicar limit si se proporciona
                    if limit is not None and isinstance(limit, int) and limit > 0:
                        # Parsear fechas y ordenar descendente
                        parsed = []
                        for line in filtered_lines:
                            dt = None
                            try:
                                parts = line.split(maxsplit=3)
                                if len(parts) >= 3:
                                    date_str = f"{parts[0]} {parts[1]} {parts[2]}"
                                    dt = parse_syslog_date(date_str)
                            except Exception:
                                dt = None
                            parsed.append((dt, line))
                        
                        parsed_sorted = sorted(parsed, key=lambda x: (x[0] is None, x[0]), reverse=True)
                        final_lines = [ln for (_, ln) in parsed_sorted[:limit]]
                    else:
                        final_lines = filtered_lines
                    
                    return {
                        "status": 200,
                        "total_count": result.get("count", 0),
                        "filtered_count": result.get("filtered_count", 0),
                        "keyword_matches": len(match_indices),
                        "returned_count": len(final_lines),
                        "data": final_lines
                    }
            
            # Si limit se especifica sin keywords
            if limit is not None and isinstance(limit, int) and limit > 0:
                logger.info(f"Aplicando limit={limit}: seleccionando los {limit} logs más recientes dentro del rango filtrado")
                parsed = []
                for line in data_lines:
                    dt = None
                    try:
                        parts = line.split(maxsplit=3)
                        if len(parts) >= 3:
                            date_str = f"{parts[0]} {parts[1]} {parts[2]}"
                            dt = parse_syslog_date(date_str)
                    except Exception:
                        dt = None
                    parsed.append((dt, line))

                # Sort by datetime descending; None values go to the end
                parsed_sorted = sorted(parsed, key=lambda x: (x[0] is None, x[0]), reverse=True)
                selected = [ln for (_, ln) in parsed_sorted[:limit]]

                return {
                    "status": 200,
                    "total_count": result.get("count", 0),
                    "filtered_count": result.get("filtered_count", 0),
                    "returned_count": len(selected),
                    "data": selected
                }

            return {
                "status": 200,
                "count": result["count"],
                "filtered_count": result["filtered_count"],
                "data": result["data"]
            }
        
        finally:
            # Limpiar archivo temporal
            Path(temp_html_path).unlink(missing_ok=True)
            # Cerrar sesión HTTP del ChargerSession
            try:
                await session.close()
            except Exception:
                pass
    
    except Exception as e:
        logger.error(f"Error en obtener_logs: {str(e)}")
        await ctx.error(f"Error: {str(e)}")

def main():
    logger.info("Iniciando EV Charger MCP Server")
    # Si DEBUG_PRINT_ENV está activado, imprimir un subconjunto enmascarado de las variables de entorno
    try:
        debug_env = os.getenv("DEBUG_PRINT_ENV", "false").lower() in ("1", "true", "yes")
    except Exception:
        debug_env = False

    if debug_env:
        keys_to_show = [
            "CHARGER_HOST",
            "CHARGER_USERNAME",
            "CHARGER_PASSWORD",
            "DEVICE_ID",
            "VERIFY_SSL",
            "MCP_HOST",
            "MCP_PORT",
            "SSL_CERT_PATH",
        ]
        shown = {k: _mask_val(k, os.getenv(k)) for k in keys_to_show}
        logger.info(f"ENV at startup (masked): {shown}")
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Error fatal en MCP Server: {str(e)}")
        raise

if __name__ == "__main__":
    main()