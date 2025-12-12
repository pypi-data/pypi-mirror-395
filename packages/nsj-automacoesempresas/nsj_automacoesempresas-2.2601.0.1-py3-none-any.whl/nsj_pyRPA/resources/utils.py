import uuid
from datetime import datetime

def is_uuid(value):
    try:
        uuid.UUID(str(value))

        return True
    except ValueError:
        return False

        
def to_bool(value : str, val_true : str = "true"):
    if value.lower() == val_true.lower():
        return True
    else:
        return False


def to_int(value : any, default=0): 
    try:
        _result = int(value)
        return _result
    except:
        return default
    

def ConvertValue(value):
    if str(value).lower() in ('true', 'false'):
        return to_bool(str(value))
    
    try:
        if '.' in str(value):
            return float(str(value))
        
        return int(str(value))
    except ValueError:
        pass

    date_formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%d/%m/%Y']
    for date_format in date_formats:
        try:
            date = datetime.strptime(str(value), date_format)
            return date
        except ValueError:
            pass

    return str(value)


def formatar_tempo(tempo_segundos):
    """
    Formata o tempo em segundo informado no formato hh:mm:ss.mmmm
    """

    horas, segundos_restantes = divmod(tempo_segundos, 3600)
    minutos, segundos = divmod(segundos_restantes, 60)
    microssegundos = int((tempo_segundos - int(tempo_segundos)) * 1000)
    
    return f"{int(horas):02d}:{int(minutos):02d}:{int(segundos):02d}.{microssegundos:03d}"


def get_version_number():
    """
    Retorna a versão de executável do utiltiário PyMeuRH.exe
    """

    import win32api
    try:
        info = win32api.GetFileVersionInfo('PyMeuRH.exe', "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"        
        return version
    except Exception as e:
        return "Não identificada"
    

def inc_data(data_base, dias=0, meses=0, anos=0):
    """
    Incrementa a data base informado em uma quantiade de dias, 
    meses e ou anos informados nos argumentos, se nenhuma incremento 
    for informado, o resulta será o mesmo da entrada
    """
    from dateutil.relativedelta import relativedelta  

    delta = relativedelta(days=dias, months=meses, years=anos)    
    return data_base + delta


def MsgErro(titulo, mensagem):
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal, mostrando apenas a messagebox
    messagebox.showerror(titulo, mensagem)