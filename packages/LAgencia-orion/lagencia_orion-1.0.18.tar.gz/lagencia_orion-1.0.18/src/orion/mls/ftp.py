import io
import os
from ftplib import FTP, error_perm
from typing import Tuple

import pandas as pd
from loguru import logger

from orion import config

"""_summary_: Extrae archivos MLS de un servidor ftp y los almacena
                en un directorio
"""


class CredentialsFTP:
    host: str
    user: str
    password: str


class CredentialsFTPMLS(CredentialsFTP):
    host: str = config.HOST_SERVER_FTP
    user: str = config.USER_SERVER_FTP
    password: str = config.PASSWORD_SERVER_FTP


def extract_files_server_ftp(date: str, path_save: str = "", credential: CredentialsFTP = CredentialsFTPMLS):
    # date: 20240604 # formato de la fecha, resYYYYMMDD.csv, comYYYYMMDD.csv

    with FTP(host=credential.host) as ftp:
        ftp.login(user=credential.user, passwd=credential.password)

        files = []
        ftp.retrlines("LIST", callback=files.append)

        filename_res = f"res{date}.csv"
        path_save_ = os.path.join(path_save, filename_res)
        print("path_save: ", path_save)
        print("path_save_: ", path_save_)
        with open(path_save_, mode="wb") as file:
            ftp.retrbinary(f"RETR {filename_res}", file.write)

        filename_com = f"com{date}.csv"
        path_save_ = os.path.join(path_save, filename_com)
        with open(path_save_, mode="wb") as file:
            ftp.retrbinary(f"RETR {filename_com}", file.write)


class FTPMLS:
    def __init__(self, credential: CredentialsFTP = CredentialsFTPMLS):
        self.credential = credential

    def extract_files_com_and_res_from_server_ftp(self, date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Descarga un archivo CSV del servidor FTP y lo devuelve como un DataFrame."""

        filename_com = f"com{date}.csv"
        filename_res = f"res{date}.csv"

        with FTP(host=self.credential.host) as ftp:
            df_com = self.search_file(ftp=ftp, filename=filename_com)
            def_res = self.search_file(ftp=ftp, filename=filename_res)
            df_com.rename(columns={"commercial_type": "property_type"}, inplace=True)
            return (df_com, def_res)

        return (pd.DataFrame(), pd.DataFrame())

    def search_file(self, ftp: FTP, filename: str) -> pd.DataFrame:
        try:
            logger.debug(f"Conectando al servidor FTP: {self.credential.host}")
            ftp.login(user=self.credential.user, passwd=self.credential.password)
            logger.info("Login al servidor FTP exitoso")

            # Crear buffer en memoria
            bio = io.BytesIO()

            logger.debug(f"Intentando recuperar archivo {filename} desde el servidor")
            logger.info(f"Iniciando descarga del archivo: {filename}")
            ftp.retrbinary(f"RETR {filename}", bio.write)
            logger.info(f"Archivo {filename} descargado correctamente")

            bio.seek(0)

            # Cargar CSV en DataFrame
            df = pd.read_csv(bio)
            logger.debug(f"Archivo {filename} convertido exitosamente a DataFrame")
            return df

        except error_perm as ex:
            msg = str(ex)
            if "Login incorrect" in msg:
                logger.error("Error de autenticación: usuario o contraseña incorrectos")
                logger.critical("Credenciales del servicio FTP no funcioanan, pudieron haber cambiado.")
                raise ValueError("Credenciales del servicio FTP no funcioanan, pudieron haber cambiado.")
            elif "No such file or directory" in msg or "550" in msg:
                logger.warning(f"Archivo no encontrado en el servidor: {filename}")
            else:
                logger.error(f"Error de permisos en FTP: {msg}")

        except Exception as ex:
            logger.exception(f"Ocurrió un error inesperado al procesar {filename}: {ex}")

        return pd.DataFrame()


if __name__ == "__main__":
    # 530 Login incorrect.
    # No such file or directory
    ...
