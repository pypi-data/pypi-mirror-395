import os
import json
import requests
import pandas as pd
import logging
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from typing import Optional

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class API:
    """
    Obtiene el url y token de acceso de la API-INVESTMENT-RISK desde las variables de entorno 
    y define la función de conexión.
    """
    api_url: Optional[str] = None
    api_token: Optional[str] = None
    timeout: int = 30

    def __post_init__(self):
        """Inicializa y valida las variables de entorno"""
        self.api_url = os.getenv('API_RISK_URL')
        self.api_token = os.getenv('API_RISK_TOKEN')
        
        if not self.api_url:
            raise ValueError("Variable de entorno API_RISK_URL no encontrada")
        if not self.api_token:
            raise ValueError("Variable de entorno API_RISK_TOKEN no encontrada")
        
        # Limpiar URL (remover slash final si existe)
        self.api_url = self.api_url.rstrip('/')

    def engine(self, url: str) -> pd.DataFrame:
        """
        Función principal para hacer la consulta a la url de la API.

        Args:
            url (str): url de consulta completa.
            
        Returns:
            pd.DataFrame: Datos normalizados en formato DataFrame
            
        Raises:
            Exception: Varios tipos de errores de conexión y API
        """
        if not url:
            raise ValueError("URL no puede estar vacía")
            
        logging.info(f"Consultando URL: {url}")
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            logging.info(f"Respuesta HTTP: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                df = pd.json_normalize(data)
                logging.info(f"Datos obtenidos: {len(df)} registros")
                return df
                
            elif response.status_code == 401:
                raise Exception("Token de acceso inválido o expirado")
            elif response.status_code == 403:
                raise Exception("Sin permisos para acceder a este endpoint")
            elif response.status_code == 404:
                raise Exception("Endpoint no encontrado")
            else:
                raise Exception(f"Error HTTP {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            logging.error("Timeout en la conexión")
            raise Exception("Timeout: La API no respondió en tiempo esperado")
        except requests.exceptions.ConnectionError:
            logging.error("Error de conexión")
            raise Exception("Error de conexión con la API")
        except json.JSONDecodeError:
            logging.error("Error al decodificar JSON")
            raise Exception("Respuesta de la API no es un JSON válido")
        except Exception as e:
            logging.error(f"Error en engine(): {str(e)}")
            raise


@dataclass
class Data(API):
    """
    Clase principal para interactuar con todos los endpoints de la API Investment Risk
    """

    def _validate_date_range(self, start: str, end: str) -> tuple:
        """
        Valida formato y rango de fechas
        
        Args:
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            tuple: (start_date, end_date) como objetos datetime
            
        Raises:
            ValueError: Si las fechas tienen formato incorrecto o rango inválido
        """
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d')
            end_date = datetime.strptime(end, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Las fechas deben estar en formato YYYY-MM-DD")
        
        if start_date > end_date:
            raise ValueError("La fecha de inicio no puede ser mayor que la fecha fin")
        
        return start_date, end_date

    def _validate_tipo(self, tipo: str) -> None:
        """Valida que el tipo sea 'bruto' o 'neto'"""
        if tipo not in ['bruto', 'neto']:
            raise ValueError("El parámetro 'tipo' debe ser 'bruto' o 'neto'")

    def get_available_endpoints(self) -> list:
        """
        Retorna una lista de todos los endpoints disponibles en la API
        
        Returns:
            list: Lista de nombres de métodos disponibles
        """
        endpoints = []
        for method_name in dir(self):
            if method_name.startswith('get_') and callable(getattr(self, method_name)):
                endpoints.append(method_name)
        return endpoints

    # ================== AFP ==================
    def get_afp_vc(self, start: str, end: str) -> pd.DataFrame:
        """
        Retorna los valores cuota de los fondos de las AFP
        
        Args:
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de valores cuota AFP
        """
        self._validate_date_range(start, end)
        api_url = f'{self.api_url}/AFP_ValoresCuota/{start}_{end}'
        return self.engine(url=api_url)
    
    def get_afp_patrimonio(self, start: str, end: str) -> pd.DataFrame:
        """
        Retorna el patrimonio de los fondos de las AFP
        
        Args:
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de patrimonio AFP
        """
        self._validate_date_range(start, end)
        api_url = f'{self.api_url}/AFP_Patrimonio/{start}_{end}'
        return self.engine(url=api_url)
    
    # ================== FONDOS MUTUOS ==================
    def get_lva_update(self, tipo: str) -> pd.DataFrame:
        """
        Retorna la última fecha de actualización de los valores cuota
        
        Args:
            tipo (str): 'bruto' o 'neto'
            
        Returns:
            pd.DataFrame: Fecha de última actualización
        """
        self._validate_tipo(tipo)
        api_url = f'{self.api_url}/LVA_Update/{tipo}'
        return self.engine(url=api_url)

    def get_fm_vc(self, tipo: str, start: str, end: str) -> pd.DataFrame:
        """
        Retorna los valores cuota de fondos mutuos
        
        Args:
            tipo (str): 'bruto' o 'neto'
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de valores cuota de fondos mutuos
        """
        self._validate_tipo(tipo)
        self._validate_date_range(start, end)
        api_url = f'{self.api_url}/FondosMutuos_ValoresCuota/{tipo}_{start}_{end}'
        return self.engine(url=api_url)
    
    def get_fm_vc_categ(self, categoria: str, tipo: str, start: str, end: str) -> pd.DataFrame:
        """
        Retorna los valores cuota de fondos mutuos por categoría
        
        Args:
            categoria (str): Categoría del fondo
            tipo (str): 'bruto' o 'neto'
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de valores cuota por categoría
        """
        self._validate_tipo(tipo)
        self._validate_date_range(start, end)
        if not categoria:
            raise ValueError("La categoría no puede estar vacía")
        api_url = f'{self.api_url}/FondosMutuos_ValoresCuota_Categ/{categoria}_{tipo}_{start}_{end}'
        return self.engine(url=api_url)

    def get_fm_vc_run(self, run: str, tipo: str, start: str, end: str) -> pd.DataFrame:
        """
        Retorna los valores cuota de fondos mutuos por RUN
        
        Args:
            run (str): RUN del fondo
            tipo (str): 'bruto' o 'neto'
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de valores cuota por RUN
        """
        self._validate_tipo(tipo)
        self._validate_date_range(start, end)
        if not run:
            raise ValueError("El RUN no puede estar vacío")
        api_url = f'{self.api_url}/FondosMutuos_ValoresCuota_Run/{run}_{tipo}_{start}_{end}'
        return self.engine(url=api_url)

    # ================== RIESGO ==================
    def get_risk_metrics(self, runsura: str, metrica: str, start: str, end: str) -> pd.DataFrame:
        """
        Retorna las métricas de riesgo
        
        Args:
            runsura (str): RUN SURA del fondo
            metrica (str): Tipo de métrica de riesgo
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de métricas de riesgo
        """
        self._validate_date_range(start, end)
        if not runsura or not metrica:
            raise ValueError("RUN SURA y métrica no pueden estar vacíos")
        api_url = f'{self.api_url}/Risk_Metrics/{runsura}_{metrica}_{start}_{end}'
        return self.engine(url=api_url)
    
    def get_metricas(self) -> pd.DataFrame:
        """
        Retorna la lista de métricas disponibles
        
        Returns:
            pd.DataFrame: Lista de métricas disponibles
        """
        api_url = f'{self.api_url}/Metricas'
        return self.engine(url=api_url)
    
    def get_metricas_absolutas(self, run: str, id_metrica: int, start: str, end: str) -> pd.DataFrame:
        """
        Retorna las métricas absolutas de riesgo
        
        Args:
            run (str): RUN del fondo
            id_metrica (int): ID de la métrica
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de métricas absolutas
        """
        self._validate_date_range(start, end)
        if not run:
            raise ValueError("El RUN no puede estar vacío")
        if not isinstance(id_metrica, int) or id_metrica <= 0:
            raise ValueError("El ID de métrica debe ser un entero positivo")
        api_url = f'{self.api_url}/Metricas_Absolutas/{run}_{id_metrica}_{start}_{end}'
        return self.engine(url=api_url)
    
    def get_competidores(self, definicion: str) -> pd.DataFrame:
        """
        Retorna el peer group de fondos competidores
        
        Args:
            definicion (str): Definición del grupo de competidores
            
        Returns:
            pd.DataFrame: Datos de fondos competidores
        """
        if not definicion:
            raise ValueError("La definición no puede estar vacía")
        api_url = f'{self.api_url}/Competidores/{definicion}'
        return self.engine(url=api_url)
    
    def get_alertas_run(self, runsura: str, start: str, end: str) -> pd.DataFrame:
        """
        Retorna las alertas de VaR por RUN SURA
        
        Args:
            runsura (str): RUN SURA del fondo
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de alertas por RUN
        """
        self._validate_date_range(start, end)
        if not runsura:
            raise ValueError("El RUN SURA no puede estar vacío")
        api_url = f'{self.api_url}/Alertas_Run/{runsura}_{start}_{end}'
        return self.engine(url=api_url)
    
    def get_alertas(self, start: str, end: str) -> pd.DataFrame:
        """
        Retorna todas las alertas de VaR
        
        Args:
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de todas las alertas
        """
        self._validate_date_range(start, end)
        api_url = f'{self.api_url}/Alertas/{start}_{end}'
        return self.engine(url=api_url)
    
    def get_nivel_riesgo(self, start: str, end: str) -> pd.DataFrame:
        """
        Retorna el modelo SRRI de niveles de riesgo
        
        Args:
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos del modelo SRRI
        """
        self._validate_date_range(start, end)
        api_url = f'{self.api_url}/Nivel_Riesgo/{start}_{end}'
        return self.engine(url=api_url)
    
    # ================== PERFORMANCE & ALPHA ==================
    def get_alpha(self, date: str) -> pd.DataFrame:
        """
        Retorna el rendimiento MTD y YTD de SURA
        
        Args:
            date (str): Fecha en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de rendimiento SURA
        """
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("La fecha debe estar en formato YYYY-MM-DD")
        api_url = f'{self.api_url}/Performance_SURA/{date}'
        return self.engine(url=api_url)
    
    def get_alpha_run(self, runsura: str, start: str, end: str) -> pd.DataFrame:
        """
        Retorna el rendimiento MTD y YTD por fondo SURA
        
        Args:
            runsura (str): RUN SURA del fondo
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de rendimiento por fondo
        """
        self._validate_date_range(start, end)
        if not runsura:
            raise ValueError("El RUN SURA no puede estar vacío")
        api_url = f'{self.api_url}/Performance_SURA_Run/{runsura}_{start}_{end}'
        return self.engine(url=api_url)

    def get_quartil(self, start: str, end: str) -> pd.DataFrame:
        """
        Retorna los quartiles de todos los fondos
        
        Args:
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de quartiles
        """
        self._validate_date_range(start, end)
        api_url = f'{self.api_url}/Quartil/{start}_{end}'
        return self.engine(url=api_url)
    
    def get_quartil_run(self, runsura: str, start: str, end: str) -> pd.DataFrame:
        """
        Retorna los quartiles por fondo
        
        Args:
            runsura (str): RUN SURA del fondo
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de quartiles por fondo
        """
        self._validate_date_range(start, end)
        if not runsura:
            raise ValueError("El RUN SURA no puede estar vacío")
        api_url = f'{self.api_url}/Quartil_Run/{runsura}_{start}_{end}'
        return self.engine(url=api_url)
    
    def get_quartil_categ(self, categoria: str, start: str, end: str) -> pd.DataFrame:
        """
        Retorna los quartiles por categoría
        
        Args:
            categoria (str): Categoría del fondo
            start (str): Fecha inicio en formato YYYY-MM-DD
            end (str): Fecha fin en formato YYYY-MM-DD
            
        Returns:
            pd.DataFrame: Datos de quartiles por categoría
        """
        self._validate_date_range(start, end)
        if not categoria:
            raise ValueError("La categoría no puede estar vacía")
        api_url = f'{self.api_url}/Quartil_Categoria/{categoria}_{start}_{end}'
        return self.engine(url=api_url)


# ================== EJEMPLO DE USO ==================
if __name__ == "__main__":
    """Ejemplo de uso del cliente API"""
    try:
        # Inicializar cliente
        api = Data()
        
        # Listar endpoints disponibles
        print("Endpoints disponibles:")
        for endpoint in api.get_available_endpoints():
            print(f"  - {endpoint}")
        
        # Ejemplo de consulta
        print("\nConsultando datos AFP...")
        afp_data = api.get_afp_vc('2024-01-01', '2024-01-31')
        print(f"Datos AFP obtenidos: {len(afp_data)} registros")
        
    except ValueError as e:
        print(f"Error de validación: {e}")
    except Exception as e:
        print(f"Error general: {e}")