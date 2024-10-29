from fastapi import Depends, FastAPI, UploadFile, HTTPException, Response
from fastapi.responses import FileResponse
from typing import Annotated
from settings import config
import pandas as pd
from src.models import Base
from src.db import engine
from sqlalchemy import text
from datetime import date,timedelta
import time
import itertools
import datetime
import tempfile
import os
import pathlib




# correct time maker

def make_time(dt):
    start_time = date(1900,1,1)
    delta = timedelta(int(dt))
    offset = start_time + delta
    return offset





# P R E S E N T A T I O N    D A T A
contact_dict = dict(name=config['CONTACT_NAME'],
                    email=config['CONTACT_EMAIL'],
                    url=config['CONTACT_URL'],
                    resume=config['CONTACT_CV_FILE'],
                    phone=config['CONTACT_PHONE'],
                                  )
app = FastAPI(title=config['API_TITLE'],description=config['API_DESCRIPTION'],contact=contact_dict)

# params
async def common_parameters(contacts: dict = contact_dict):
    return contacts







# R E A D   E X C E L
@app.post("/upload-excel",tags=["Загрузите файл Excel и отправьте данные в БД "])
async def upload_file_route(file: UploadFile):
    """## Используя этот метод вы загрузите данные в базу данных \n
    #### Формат файла: xlsb  и xls\n
    #### Формат таблиц: dt - article - kg \n
    *
    Метод загрузки данных создан под формат файла выданного сотрудником службы подбора персонала\n
    Данные другого формата не актуальны для таблицы в существующей базе данных этого приложения\n
    ### * Качественная проверка, редактирование, и загрузка очень больших данных потребует времени. Подождите пожалуйста несколько минут пока крутиться "LOADING..."

    """
    start_t = time.time()
    try:
        processed = pd.read_excel(file.file)
        iterated = [i for i in processed.itertuples(index=True,name='Item')]
        async with engine.begin() as conn:
            for item in iterated:
                    if isinstance(item.dt,int) and isinstance(item.kg, int) and isinstance(item.article,int):
                        _date = make_time(item.dt)
                        await conn.execute(text(f"INSERT INTO item (dt,article,kg) VALUES ('{_date}',{item.article},{item.kg})"))
                    if isinstance(item.dt,date) and isinstance(item.kg, int) and isinstance(item.article,int):
                        await conn.execute(text(f"INSERT INTO item (dt,article,kg) VALUES ('{item.dt}',{item.article},{item.kg})"))
            await conn.commit()
            end_t = time.time()
            dur_t = (end_t - start_t)
        return Response(status_code=200,content=f"OK: time duration: {dur_t}")
        
    except Exception:
        raise HTTPException(status_code=404, detail="Wrong Excel File :")
    


# R E A D   E X C E L



@app.get("/between-dates/{start_date}/{end_date}",tags=[" Получите Excel таблицу с отчетом за указанный период + [ по артикулуу ]"],response_class=FileResponse)
async def between_dates_route(
    start_date: date ,
    end_date: date ,
    sheet_name: str | None = 'rep',
    file_name: str | None = 'flrpt', 
    article: int | None = None ,
    ):
    """## Метод который формирует отчеты в виде файлов таблиц Excel... \n
    Обязательные параметры выделены красной надписью *required \n
    ---------------\n
   
    #### Параметры:\n
    file_name: Имя файла на выходе - суфикс \n
    article: Артикул формат числовой - 1000000020\n
    -----------\n
    start_date: Отчет с ...\n
    end_date: ...по\n
    * Между этими двумя датами вы получите отчетный период
    ---------\n
    #### Не обязательный параметр - article \n
    В случае если указан параметр то поиск происходит по одной категории товара в период с .... по ...

    """
    detail_no_found = "Not Found Item"
    if article:
        try:
            with tempfile.TemporaryDirectory(delete=False) as tmp:
                path_tmp_dir = pathlib.Path(tmp)
            async with engine.begin() as conn:
                cursor = await conn.execute(text(f"SELECT * FROM item WHERE article ={article} AND dt BETWEEN '{start_date}' AND '{end_date}'"))
                fetched = cursor.fetchall()
                if fetched == []:
                    return Response(status_code=404,detail=detail_no_found)
                # lists with values
                dt = [ i[1] for i in fetched]
                article = [ y[2] for y in fetched ]
                kg = [ x[3] for x in fetched ]
                
            data_frame = pd.DataFrame({
                'dt': dt,
                'article': article,
                'kg': kg})
        
            path_to_file = f'{path_tmp_dir}/{file_name}.xlsx'
            with pd.ExcelWriter(path_to_file,) as writer:
                data_frame.to_excel(writer,sheet_name='Item')
                headers = {
                    'Content-Disposition': f'attachment; filename="{path_to_file}"',
                    "content-type": "application/vnd.ms-excel"
                    }
                return FileResponse(path_to_file,headers=headers)
        except Exception:
            raise HTTPException(status_code=404, detail=detail_no_found)
    if article is None:
        try:
            with tempfile.TemporaryDirectory(delete=False) as tmp:
                path_tmp_dir = pathlib.Path(tmp)
            async with engine.begin() as conn:
                cursor = await conn.execute(text(f"SELECT * FROM item WHERE dt BETWEEN '{start_date}' AND '{end_date}'"))
                fetched = cursor.fetchall()
                if fetched == []:
                    return Response(status_code=404,detail=detail_no_found)
                # lists with values
                dt = [ i[1] for i in fetched]
                article = [ y[2] for y in fetched ]
                kg = [ x[3] for x in fetched ]
                
            data_frame = pd.DataFrame({
                'dt': dt,
                'article': article,
                'kg': kg})
            path_to_file = f'{path_tmp_dir}/{file_name}.xlsx'
            with pd.ExcelWriter(path_to_file,) as writer:
                data_frame.to_excel(writer,sheet_name=sheet_name)
                headers = {
                    'Content-Disposition': f'attachment; filename="{path_to_file}"',
                    "content-type": "application/vnd.ms-excel"
                    }
                return FileResponse(path_to_file,headers=headers)
        except Exception:
            raise HTTPException(status_code=404, detail="Wrong connection:")
    
        






@app.on_event("startup")
async def create_db_and_tables():
    # creates tables in postgres pgdb1
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
