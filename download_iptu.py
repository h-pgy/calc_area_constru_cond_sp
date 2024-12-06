from typing import Any
from requests import Session
from zipfile import ZipFile
import os
from config import ORIGINAL_DATA_FOLDER, ID_SESSAO

class DownloadIptu:

    domain = 'http://download.geosampa.prefeitura.sp.gov.br/'
    endpoint = 'PaginasPublicas/downloadArquivo.aspx?orig=DownloadCamadas&arq={fname}&arqTipo=XLS_CSV'
    
    def __init__(self, data_folder:str=ORIGINAL_DATA_FOLDER)->None:

        self.folder = data_folder

        self.session = Session()
    
    def config_session(self)->None:

        self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            })

        self.session.cookies.set('ASP.NET_SessionId', ID_SESSAO)
        self.session.get('https://geosampa.prefeitura.sp.gov.br/PaginasPublicas/_SBC.aspx')

        
    def solve_iptu_file_param(self, year:int):

        return f'12_Cadastro%5C%5CIPTU_INTER%5C%5CXLS_CSV%5C%5CIPTU_{year}'
    
       
    def solve_uri(self, year:int):

        fname = self.solve_iptu_file_param(year)
        

        return self.domain + self.endpoint.format(fname=fname)

    
    def download_iptu_file(self, year:int) -> bytes:

        url = self.solve_uri(year)
        
        with self.session.get(url) as r:
            return r.content

    def gen_fname(self, year:int, format:str)->str:

        fname = f'iptu_{year}.{format}'
        fpath = os.path.join(self.folder, fname)

        return fpath
        
    def save_zip_file(self, year:int, content:bytes)->str:

        fname = self.gen_fname(year, 'zip')
        with open(fname, 'wb') as f:
            f.write(content)
        return fname

    def get_iptu_file_from_zip(self, year:int, file_list:list[str])->str:

        for file in file_list:
            if file.lower() == f'iptu_{year}.csv':
                return file
        else:
            raise RuntimeError(f'Não foi encontrado nenhum arquivo para deszipar. Arquivos: {file_list}')

    def unzip_file(self, zip_fpath:str, year:int)->str:

        dest_fpath = self.gen_fname(year, 'csv')
        with ZipFile(zip_fpath, 'r') as zip_ref:
            # List all the files in the zip archive
            file_list = zip_ref.namelist()
            file_to_extract = self.get_iptu_file_from_zip(year, file_list)
            zip_ref.extract(file_to_extract, dest_fpath)

        return dest_fpath

    
    def pipeline(self, year:int)->str:

        dest_fpath = self.gen_fname(year, 'csv')

        if os.path.exists(dest_fpath):
            return dest_fpath
        
        zip_content = self.download_iptu_file(year)
        zip_path = self.save_zip_file(year, zip_content)
        dest_fpath = self.unzip_file(zip_path, year)

        return dest_fpath

    def __call__(self, year:int)->str:

        return self.pipeline(year)
    

download_iptu = DownloadIptu()