import requests
import os

def fromURL2HTML(url:str,output_path:str,name:str='test') -> None:
    """_summary_

    Args:
        url (str): _description_
        output_path (str): _description_
        name (str, optional): _description_. Defaults to 'test'.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(output_path,f'{name}.html'),'w',encoding='utf-8') as f:
            f.write(response.text)
    else:
        print("Could not find url: {url}")