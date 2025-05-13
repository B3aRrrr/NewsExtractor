import pandas as pd
import numpy as np

from utils.functions import *
from newscatcher import Newscatcher, describe_url
from trafilatura import html2txt
import os
from argparse import ArgumentParser
from typing import List

from config import config

def run(excel_data_path: str) -> None:
    # 1. Получаем pandas DataFrame c данными
    raw_data = pd.read_excel(excel_data_path, index_col=0) 
    # 2. Загружаем из Config  параметры  
    # 3. Проходим по всем 
    print(raw_data)

def parse() -> dict:
    parser = ArgumentParser(
        prog='GetDataset',
        description="Creating dataset from News-links",
        epilog='Version 0.0.1')
    parser.add_argument(
        '--excel_data_path',
        type=str,
        help="Excel-data file with URL for check")
    args = parser.parse_args()
    return vars(args)

def main() -> None:
    args = parse()
    
    # Если путь к файлу не был передан, открываем диалоговое окно
    if not args['excel_data_path']:
        args['excel_data_path'] = select_file()
    
    # Проверяем, был ли выбран файл
    if not args['excel_data_path']:
        print("Файл не был выбран. Завершение работы.")
        return
    
    run(**args)

if __name__ == '__main__':
    main()
