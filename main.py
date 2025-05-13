import pandas as pd
from utils.functions import *
import os
from argparse import ArgumentParser
from config import config

def run(excel_data_path: str) -> None:
    # 0. Получаем имя файла, путь директории в которой он находится
    excel_data_out_name= os.path.splitext(
        os.path.basename(excel_data_path))[0]
    dirname = os.path.dirname(excel_data_path)
    # 1. Получаем pandas DataFrame c данными
    raw_data = pd.read_excel(excel_data_path) 
    # 2. Загружаем из Config  параметры  
    headers = config['default'].HEADERS
    # 3. Обработка URL новостей
    # print(raw_data.columns.values) ['URL' 'lib_text']
    raw_data['gold_standard'] = ''
    raw_data['recall'] = ""
    raw_data['loss_significance'] = ""
    
    gold_standard_list = []
    recall_list = []
    loss_significance_list = []
    for index, row in raw_data.iterrows():
    # 3.1 Извлекаем текст из новости (эталоны)
        url = row['URL']
        result = extract_article(url=url,headers=headers)
    # 3.2 Высчитываем полноту извлечения новости
        evaluation_dict = evaluate_extraction(
            reference_text=result['text'],
            extracted_text=row['lib_text']
            ) 
        recall = evaluation_dict['recall']
    # 3.4. Оценка значимости пропущенного текста
        evaluation_significance_dict = evaluate_significance(
            reference_text=result['text'],
            extracted_text=row['lib_text']
        )
        loss_significance = evaluation_dict['recall']
        
        
        gold_standard_list.append(result['text'])
        recall_list.append(recall)
        loss_significance_list.append(loss_significance)
        
    raw_data['gold_standard'] = gold_standard_list
    raw_data['recall'] = recall_list
    raw_data['loss_significance'] = loss_significance_list
    # Сохранение файла с результатом
    raw_data.to_excel(os.path.join(dirname,f"{excel_data_out_name}_output.xlsx")) 

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
