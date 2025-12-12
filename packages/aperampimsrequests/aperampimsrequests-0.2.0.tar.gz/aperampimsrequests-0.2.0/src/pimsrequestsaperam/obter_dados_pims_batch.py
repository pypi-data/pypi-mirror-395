from typing import List
import pandas as pd
import datetime
import requests
import time
import pytz
import json

import urllib3 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================
# CACHE GLOBAL DE WEBIDs
# ============================
WEBID_CACHE = {}

# PIWEBAPI = "http://10.247.224.39/piwebapi"
PIWEBAPI = ["http://10.247.224.39/piwebapi"]


def get_webid(tag: str, piwebapi: int = 0):
    """Retorna o WebID da tag com cache + retry contra erro 429."""
    if tag in WEBID_CACHE:
        return WEBID_CACHE[tag]

    url = f"{PIWEBAPI[piwebapi]}/points?path=\\\\pims\\{tag}"

    for tentativas in range(10):
        resp = requests.get(url, verify=False)

        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 1))
            print(f"[429] Aguardando {wait}s para {tag}")
            time.sleep(wait)
            continue

        resp.raise_for_status()
        webid = resp.json()["WebId"]
        WEBID_CACHE[tag] = webid
        return webid

    raise Exception(f"Falha ao obter WebID da tag {tag} após múltiplas tentativas")


def montar_batch_streamset_pims(webids, start_time, timeZone, interval, pytz_timeZone, piwebapi=0):
    """
    versão FUNDIDA:
    - usa mesma lógica da montar_batch_pims (intervalos de 15 dias)
    - usa streamset GET com vários webids
    - retorna um batch igual ao antigo: { "1": {...}, "2": {...}, ... }
    """
    """
    StreamSet com arredondamento PARA BAIXO do start_time:
      - *-Nh  → hora cheia anterior
      - *-Nd  → início do dia
      - *-Nmo → primeiro dia do mês
      - *-Ny  → primeiro dia do ano
    """

    def arredondar_start(start_raw):
        tz = pytz.timezone(pytz_timeZone)
        agora = datetime.datetime.now(tz)

        # --- HORAS ---
        if start_raw.endswith("h"):
            horas = int(start_raw[2:-1])
            calc = agora - datetime.timedelta(hours=horas)
            # arredonda para BAIXO
            return calc.replace(minute=0, second=0, microsecond=0)

        # --- DIAS ---
        elif start_raw.endswith("d"):
            dias = int(start_raw[2:-1])
            calc = agora - datetime.timedelta(days=dias)
            # início do dia
            return calc.replace(hour=0, minute=0, second=0, microsecond=0)

        # --- MESES ---
        elif start_raw.endswith("mo"):
            meses = int(start_raw[2:-2])
            ano = agora.year
            mes = agora.month - meses

            # Se passar de janeiro, corrige ano/mês
            while mes <= 0:
                mes += 12
                ano -= 1

            # primeiro dia do mês
            return datetime.datetime(ano, mes, 1, tzinfo=tz)

        # --- ANOS ---
        elif start_raw.endswith("y"):
            anos = int(start_raw[2:-1])
            ano = agora.year - anos
            return datetime.datetime(ano, 1, 1, tzinfo=tz)

        else:
            raise ValueError("Formato inválido para start_time")

    # ------------------------------------------------------
    # 1) Calcula startTime arredondado
    # ------------------------------------------------------
    inicio = arredondar_start(start_time)

    tz = pytz.timezone(pytz_timeZone)
    agora = datetime.datetime.now(tz)

    # Normaliza o syncTime para zero segundos
    # sync_time = inicio.replace(second=0, microsecond=0)
    sync_time_str = inicio.strftime("%Y-%m-%dT%H:%M:%SZ")

    batch_body = {}
    id_counter = 1
    inicio_periodo = inicio

    # construção dos 15–30 day chunks
    while inicio_periodo < agora:
        fim_periodo = inicio_periodo + datetime.timedelta(days=20)
        if fim_periodo > agora:
            fim_periodo = agora

        inicio_str = inicio_periodo.strftime("%Y-%m-%dT%H:%M:%SZ")
        fim_str = fim_periodo.strftime("%Y-%m-%dT%H:%M:%SZ")

        # monta streamset GET
        base_url = f"{PIWEBAPI[piwebapi]}/streamsets/interpolated?"
        params_webids = "&".join([f"webId={w}" for w in webids])

        resource_url = (
            f"{base_url}{params_webids}"
            f"&startTime={inicio_str}&endTime={fim_str}"
            f"&interval={interval}&timeZone={timeZone}&timeType=Auto"
            f"&syncTime={sync_time_str}"
        )

        batch_body[str(id_counter)] = {
            "Method": "GET",                                                                                                                                                                                                                                                                     
            "Resource": resource_url
        }

        inicio_periodo = fim_periodo
        id_counter += 1

    return batch_body


class PimsRequest():
    def __init__(self, tag, starttime="*-1y", interval="1m",
                 timeZone="Tocantins Standard Time", endtime=None, typevalue="CONT", piwebapi=0):
        self.tag: List = tag
        self.startTime: str = starttime
        self.interval: str = interval
        self.timezone: str = timeZone
        self.endtime: str = endtime
        self.typevalue: str = typevalue
        self.piwebapi: int = piwebapi


def chunk_list(lista, tamanho_chunk):
    for i in range(0, len(lista), tamanho_chunk):
        yield lista[i:i + tamanho_chunk]


def obter_dados_pims(request_data: PimsRequest, max_tags_por_streamset=20):

    tags = request_data.tag
    start = request_data.startTime
    interval = request_data.interval
    timezone = request_data.timezone
    end = request_data.endtime or "*"

    # 1. Obter WebIDs
    webids = []
    tag_por_webid = {}

    for tag in tags:
        try:
            w = get_webid(tag, request_data.piwebapi)
            webids.append(w)
            tag_por_webid[w] = tag
        except:
            return print(f"[429] Erro ao obter WebID para {tag}")

    if not webids:
        return {"erro": "Nenhum WebID válido"}

    # 2. Criar chunks
    chunks = list(chunk_list(webids, max_tags_por_streamset))
    print(f"Total de streamsets: {len(chunks)}")

    df_final = None

    # 3. Para cada chunk → montar batch
    for idx, chunk in enumerate(chunks, start=1):
        print(f"Processando chunk {idx}/{len(chunks)}...")

        # monta o corpo do batch
        batch_body = montar_batch_streamset_pims(
            webids = chunk,
            start_time = start,
            timeZone = timezone,
            interval = interval,
            pytz_timeZone = "America/Sao_Paulo",
            piwebapi = request_data.piwebapi
        )

        # 4. Executar batch
        try:
            resp = requests.post(
                f"{PIWEBAPI[request_data.piwebapi]}/batch",
                headers={"Content-Type": "application/json"},
                data=json.dumps(batch_body),
                verify=False
            )
            resp.raise_for_status()
            retorno = resp.json()
        except Exception as e:
            print(f"Erro no chunk {idx}: {e}")
            continue

        # 5. Extrair os dados do streamset
        content = retorno["1"]["Content"]["Items"]

        colunas = {}

        for tag_item in content:
            tag_name = tag_item["Name"]
            registros = tag_item["Items"]

            ts = [r["Timestamp"] for r in registros]
            values = [r["Value"]["Value"] if isinstance(r["Value"], dict) else r["Value"] for r in registros]

            colunas[tag_name] = pd.Series(values, index=ts)

        df_chunk = pd.DataFrame(colunas)
        df_chunk.index = pd.to_datetime(df_chunk.index).tz_convert("America/Sao_Paulo")
        df_chunk.sort_index(inplace=True)
        df_chunk.reset_index(inplace=True)
        df_chunk.rename(columns={"index": "Timestamp"}, inplace=True)

        # merge incremental
        if df_final is None:
            df_final = df_chunk
        else:
            df_final = pd.merge(df_final, df_chunk, on="Timestamp", how="outer")

    if df_final is None:
        return {"erro": "Nenhum dado coletado"}

    df_final.sort_values("Timestamp", inplace=True)

    return df_final

