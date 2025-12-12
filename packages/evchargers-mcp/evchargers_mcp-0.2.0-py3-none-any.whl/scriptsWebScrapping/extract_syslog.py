from bs4 import BeautifulSoup
import logging
from pathlib import Path
from datetime import datetime, timedelta
import argparse
import json

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

INPUT_HTML = "syslog.html"
OUTPUT_TXT = "syslog.txt"

def parse_syslog_date(date_str: str) -> datetime:
    """
    Parsea diferentes formatos de fecha del syslog.
    Formatos soportados:
    - "Nov 27 06:12:19"
    - "Thu Nov 27 06:12:19 2025"
    """
    # Intentar formato con año
    try:
        return datetime.strptime(date_str.strip(), "%a %b %d %H:%M:%S %Y")
    except ValueError:
        pass
    
    # Intentar formato sin año (asume año actual)
    try:
        dt = datetime.strptime(date_str.strip(), "%b %d %H:%M:%S")
        dt = dt.replace(year=datetime.now().year)
        return dt
    except ValueError:
        logger.warning(f"No se pudo parsear fecha: {date_str}")
        return None

def extract_syslog(input_file: str, output_file: str = None, days: int = None, start_date: str = None, end_date: str = None, return_data: bool = False) -> dict | int:
    """
    Extrae logs del syslog de un archivo HTML y los guarda en TXT o devuelve los datos.
    
    Args:
        input_file: Ruta del archivo HTML
        output_file: Ruta del archivo TXT de salida (opcional si return_data=True)
        days: Últimos N días (ej: 7 para última semana)
        start_date: Fecha de inicio en formato "YYYY-MM-DD"
        end_date: Fecha de fin en formato "YYYY-MM-DD"
        return_data: Si True, devuelve dict con los datos; si False, guarda en TXT
    
    Returns:
        Si return_data=True: dict con keys 'count', 'filtered_count', 'data' (lista de strings)
        Si return_data=False: int con número de líneas de log extraídas
    
    Raises:
        FileNotFoundError: Si el archivo HTML no existe
        ValueError: Si no se encuentra el textarea del syslog
    """
    # Validar que el archivo existe
    if not Path(input_file).exists():
        logger.error(f"El archivo {input_file} no existe")
        raise FileNotFoundError(f"No se encontró {input_file}")
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        logger.error(f"Error al leer {input_file}: {str(e)}")
        raise
    
    soup = BeautifulSoup(html, "lxml")
    
    # Buscar el textarea del log
    textarea = soup.find("textarea", id="syslog")
    if textarea is None:
        logger.error("No se encontró <textarea id='syslog'> en el HTML")
        raise ValueError("No se encontró <textarea id='syslog'> en el HTML")
    
    log_text = textarea.get_text()
    lines = log_text.splitlines()
    
    if not lines:
        logger.warning("No se encontraron líneas de log en el textarea")
        if return_data:
            return {"count": 0, "filtered_count": 0, "data": []}
        return 0
    
    # Configurar rango de fechas
    cutoff_date = None
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        logger.info(f"Filtrando datos de los últimos {days} días (desde {cutoff_date.strftime('%Y-%m-%d')})")
    
    if start_date:
        try:
            cutoff_date = datetime.strptime(start_date, "%Y-%m-%d")
            logger.info(f"Filtrando datos desde {cutoff_date.strftime('%Y-%m-%d')}")
        except ValueError:
            logger.error(f"Formato de start_date inválido: {start_date}")
            raise
    
    if end_date:
        try:
            end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
            end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
            logger.info(f"Filtrando datos hasta {end_date}")
        except ValueError:
            logger.error(f"Formato de end_date inválido: {end_date}")
            raise
    else:
        end_datetime = datetime.now()
    
    logs_list = []
    filtered_count = 0
    
    for idx, line in enumerate(lines):
        try:
            line = line.strip()
            if not line:
                continue
            
            # Intentar extraer fecha del inicio de la línea
            # Formato típico: "Nov 27 06:12:19 device: message"
            parts = line.split(maxsplit=3)
            
            if len(parts) >= 3:
                try:
                    date_str = f"{parts[0]} {parts[1]} {parts[2]}"
                    parsed_date = parse_syslog_date(date_str)
                    
                    if parsed_date:
                        # Aplicar filtros de fecha
                        if cutoff_date and parsed_date < cutoff_date:
                            filtered_count += 1
                            continue
                        if parsed_date > end_datetime:
                            filtered_count += 1
                            continue
                except Exception as e:
                    logger.debug(f"No se pudo parsear fecha en línea {idx + 1}: {str(e)}")
            
            logs_list.append(line)
        
        except Exception as e:
            logger.error(f"Error procesando línea {idx + 1}: {str(e)}")
            continue
    
    # Devolver datos o guardar en TXT
    if return_data:
        result = {
            "count": len(logs_list),
            "filtered_count": filtered_count,
            "data": logs_list
        }
        logger.info(f"Extraídas {len(logs_list)} líneas de log. Filtradas {filtered_count} líneas por fecha")
        return result
    
    # Guardar a TXT
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(logs_list))
        
        logger.info(f"Extraídas {len(logs_list)} líneas de log a {output_file}")
        if filtered_count > 0:
            logger.info(f"Filtradas {filtered_count} líneas por fecha")
        return len(logs_list)
    
    except Exception as e:
        logger.error(f"Error al guardar {output_file}: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae logs del syslog de un HTML y los guarda en TXT o devuelve los datos")
    parser.add_argument("--input", default=INPUT_HTML, help="Archivo HTML de entrada (default: syslog.html)")
    parser.add_argument("--output", default=OUTPUT_TXT, help="Archivo TXT de salida (default: syslog.txt)")
    parser.add_argument("--days", type=int, help="Últimos N días a incluir (ej: 7, 30)")
    parser.add_argument("--start-date", help="Fecha de inicio (formato: YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Fecha de fin (formato: YYYY-MM-DD)")
    parser.add_argument("--return", dest="return_data", action="store_true", help="Devuelve los datos en JSON en lugar de guardar en TXT")
    
    args = parser.parse_args()
    
    try:
        result = extract_syslog(
            args.input, 
            args.output, 
            days=args.days, 
            start_date=args.start_date, 
            end_date=args.end_date,
            return_data=args.return_data
        )
        
        if args.return_data:
            print(json.dumps(result, indent=2))
        else:
            print(f"✓ Proceso completado: {result} líneas de log extraídas")
    except FileNotFoundError as e:
        print(f"✗ Error: {str(e)}")
    except ValueError as e:
        print(f"✗ Error: {str(e)}")
    except Exception as e:
        print(f"✗ Error inesperado: {str(e)}")