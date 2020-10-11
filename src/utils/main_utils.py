import configparser
import logging
import os
import sys
from os.path import isdir, exists

from src.evaluacion_json import constantes_json
from src.utils.format_utils import FormatUtils

class UtilsMain:

    @staticmethod
    def verificacion_correcta_archivo_config(archivo_config: configparser.ConfigParser):
        """
        Funcion el cual permite verificar que el archivo config.ini contenga todos los parametros necesarios. En caso
        de que contenga las secciones y keys establecidos, la funcion devolvera True, en caso contrario regresara False

        :return:
        """
        validacion_total = True

        bool_ruta = archivo_config.has_option('Driver', 'ruta')
        bool_web_driver = archivo_config.has_option('Driver', 'driverPorUtilizar')
        bool_headless = archivo_config.has_option('Driver', 'headless')
        bool_log_path_dev_null = archivo_config.has_option('Driver', 'log_path_dev_null')

        if not bool_ruta:
            print('Favor de establecer el path del webdriver a utilizar dentro del archivo config.ini')
            validacion_total = False
        elif not bool_web_driver:
            print('Favor de establecer el tipo/nombre del webdriver a utilizar dentro del archivo config.ini')
            validacion_total = False
        elif not bool_headless:
            print('Favor de establecer la opcion/configuracion headless dentro del archivo config.ini')
            validacion_total = False
        elif not bool_log_path_dev_null:
            print('Favor de establecer la opcion/configuracion log_path_dev_null dentro del archivo config.ini')
            validacion_total = False

        return validacion_total

    @staticmethod
    def configuracion_log(correo_por_probar):
        # verifica si el folder del log existe
        if not os.path.isdir(constantes_json.DIR_BASE_LOG):
            try:
                os.mkdir(constantes_json.DIR_BASE_LOG)
            except OSError as e:
                print('sucedio un error al crear el directorio del log {} : {}'.format(constantes_json.DIR_BASE_LOG, e))
                print('Favor de establecer la carpeta Logs dentro del proyecto con los permisos necesarios, se procede a '
                      'terminar el script')
                sys.exit()

        # se verifica si el nombre del archivo existe, en caso contrario
        # crea el nuevo archivo log y sale del ciclo
        while True:

            # verifica que el archivo del log exista en caso contrario lo crea
            FormatUtils.generar_nombre_log(correo_por_probar)

            if not os.path.exists(constantes_json.PATH_ABSOLUTO_LOG):
                try:
                    log = open(constantes_json.PATH_ABSOLUTO_LOG, 'x')
                    log.close()
                    break
                except OSError as e:

                    print('Se tiene acceso denegado para escribir el archivo {}, favor de establecer los permisos '
                          'necesarios en el directorio Logs'.format(e))

                    print('Favor de establecer los permisos necesarios para escribir ficheros dentro del directorio '
                          'Logs. Se procede a finalizar el script')

                    sys.exit()
            else:
                print('El log {}, ya existe, se procede a generar un nuevo log'.format(constantes_json.PATH_ABSOLUTO_LOG))
                continue

        logging.basicConfig(level=logging.INFO,
                            filename=constantes_json.PATH_ABSOLUTO_LOG,
                            filemode='w+',
                            format='%(asctime)s %(lineno)d %(name)s  %(levelname)s: %(message)s',
                            datefmt='%d-%m-%YT%H:%M:%S')

        logging.info('Inicializando log: {}'.format(constantes_json.PATH_ABSOLUTO_LOG))

        # verifica si es necesario la depuracion del directorio en donde residen los logs
        FormatUtils.verificacion_depuracion_de_logs(constantes_json.DIR_BASE_LOG)

    @staticmethod
    def verificar_path_es_directorio(path_por_analizar):
        return isdir(path_por_analizar)

    @staticmethod
    def verificar_si_path_archivo_existe(path_por_analizar):
        return exists(path_por_analizar)