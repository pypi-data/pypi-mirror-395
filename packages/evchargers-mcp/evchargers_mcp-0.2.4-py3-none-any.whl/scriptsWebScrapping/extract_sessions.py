from bs4 import BeautifulSoup
import csv
import logging
from pathlib import Path
from datetime import datetime, timedelta
import argparse
import json

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

INPUT_HTML = "sessions.html"
OUTPUT_CSV = "sessions.csv"

def parse_date(date_str: str) -> datetime:
    """
    Parsea diferentes formatos de fecha del HTML.
    Formatos soportados:
    - "Thu Nov 27 06:12:19 2025"
    - "Thu Nov 27 06:10:58 UTC 2025"
    - "Sun Jun 29 02:44:46 CEST 2025"
    """
    # Remover UTC/CEST si existe
    date_str = date_str.replace(" UTC", "").replace(" CEST", "")
    
    try:
        return datetime.strptime(date_str.strip(), "%a %b %d %H:%M:%S %Y")
    except ValueError:
        logger.warning(f"No se pudo parsear fecha: {date_str}")
        return None

def extract_sessions(input_file: str, output_file: str = None, days: int = None, start_date: str = None, end_date: str = None, return_data: bool = False) -> dict | int:
    """
    Extrae sesiones de un archivo HTML y las guarda en CSV o devuelve los datos.
    
    Args:
        input_file: Ruta del archivo HTML
        output_file: Ruta del archivo CSV de salida (opcional si return_data=True)
        days: Últimos N días (ej: 7 para última semana)
        start_date: Fecha de inicio en formato "YYYY-MM-DD"
        end_date: Fecha de fin en formato "YYYY-MM-DD"
        return_data: Si True, devuelve dict con los datos; si False, guarda en CSV
    
    Returns:
        Si return_data=True: dict con keys 'count', 'filtered_count', 'data' (lista de dicts)
        Si return_data=False: int con número de sesiones extraídas
    
    Raises:
        FileNotFoundError: Si el archivo HTML no existe
        ValueError: Si no se encuentra la tabla
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
    
    # Buscar la tabla de sesiones: id="sessions_dump"
    table = soup.find("table", id="sessions_dump")
    if table is None:
        logger.error("No se encontró la tabla con id 'sessions_dump'")
        raise ValueError("No se encontró la tabla con id 'sessions_dump'")
    
    rows = table.find_all("tr")
    
    # Primera fila suele ser títulos
    data_rows = rows[1:] if len(rows) > 1 else []
    
    if not data_rows:
        logger.warning("No se encontraron filas de datos en la tabla")
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
    
    sessions_list = []
    filtered_count = 0
    
    for idx, tr in enumerate(data_rows):
        try:
            tds = tr.find_all("td")
            # Filas válidas con 6 columnas (Serial, Connector, Start, End, Energy, User ID)
            if len(tds) >= 6:
                serial = tds[0].get_text(strip=True)
                connector = tds[1].get_text(strip=True)
                start_date_str = tds[2].get_text(strip=True)
                end_date_str = tds[3].get_text(strip=True)
                energy = tds[4].get_text(strip=True)
                user_id = tds[5].get_text(strip=True)
                
                # Parsear fecha de inicio para filtrado
                parsed_start_date = parse_date(start_date_str)
                
                # Aplicar filtros de fecha
                if parsed_start_date:
                    if cutoff_date and parsed_start_date < cutoff_date:
                        filtered_count += 1
                        continue
                    if parsed_start_date > end_datetime:
                        filtered_count += 1
                        continue
                
                sessions_list.append({
                    "Serial Number": serial,
                    "Connector": connector,
                    "Start Date": start_date_str,
                    "End Date": end_date_str,
                    "Energy": energy,
                    "User ID": user_id,
                })
            else:
                # Incluir filas incompletas
                serial = tds[0].get_text(strip=True) if len(tds) > 0 else ""
                connector = tds[1].get_text(strip=True) if len(tds) > 1 else ""
                start_date_str = tds[2].get_text(strip=True) if len(tds) > 2 else ""
                end_date_str = tds[3].get_text(strip=True) if len(tds) > 3 else ""
                energy = tds[4].get_text(strip=True) if len(tds) > 4 else ""
                user_id = tds[5].get_text(strip=True) if len(tds) > 5 else ""
                
                # Parsear fecha de inicio para filtrado
                parsed_start_date = parse_date(start_date_str) if start_date_str else None
                
                # Aplicar filtros de fecha
                if parsed_start_date:
                    if cutoff_date and parsed_start_date < cutoff_date:
                        filtered_count += 1
                        continue
                    if parsed_start_date > end_datetime:
                        filtered_count += 1
                        continue
                
                sessions_list.append({
                    "Serial Number": serial,
                    "Connector": connector,
                    "Start Date": start_date_str,
                    "End Date": end_date_str,
                    "Energy": energy,
                    "User ID": user_id,
                })
                logger.info(f"Fila {idx + 2} incompleta incluida con campos vacíos")
        except Exception as e:
            logger.error(f"Error procesando fila {idx + 2}: {str(e)}")
            continue
    
    # Devolver datos o guardar en CSV
    if return_data:
        result = {
            "count": len(sessions_list),
            "filtered_count": filtered_count,
            "data": sessions_list
        }
        logger.info(f"Extraídas {len(sessions_list)} sesiones. Filtradas {filtered_count} filas por fecha")
        return result
    
    # Guardar a CSV
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Serial Number", "Connector", "Start Date", "End Date", "Energy", "User ID"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(sessions_list)
        
        logger.info(f"Extraídas {len(sessions_list)} sesiones a {output_file}")
        if filtered_count > 0:
            logger.info(f"Filtradas {filtered_count} filas por fecha")
        return len(sessions_list)
    
    except Exception as e:
        logger.error(f"Error al guardar {output_file}: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrae sesiones de un HTML y las guarda en CSV o devuelve los datos")
    parser.add_argument("--input", default=INPUT_HTML, help="Archivo HTML de entrada (default: sessions.html)")
    parser.add_argument("--output", default=OUTPUT_CSV, help="Archivo CSV de salida (default: sessions.csv)")
    parser.add_argument("--days", type=int, help="Últimos N días a incluir (ej: 7, 30)")
    parser.add_argument("--start-date", help="Fecha de inicio (formato: YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Fecha de fin (formato: YYYY-MM-DD)")
    parser.add_argument("--return", dest="return_data", action="store_true", help="Devuelve los datos en JSON en lugar de guardar en CSV")
    
    args = parser.parse_args()
    
    try:
        result = extract_sessions(
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
            print(f"✓ Proceso completado: {result} sesiones extraídas")
    except FileNotFoundError as e:
        print(f"✗ Error: {str(e)}")
    except ValueError as e:
        print(f"✗ Error: {str(e)}")
    except Exception as e:
        print(f"✗ Error inesperado: {str(e)}")