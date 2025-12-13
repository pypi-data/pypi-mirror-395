import json
import logging
from zeep import Client
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth
from datetime import timedelta, datetime, time
from typing import List, Tuple, Union, Optional
from pydantic import BaseModel
log = logging.getLogger(__name__)
class PastasAutorizadas(BaseModel):
    MensagemErro: Optional[str] = None
    OcorreuErro: bool
    PastasAutorizadas: Optional[list] = None
    QuantidadePastasAutorizadas: int

class ItemListaCorreio(BaseModel):

    Assunto: str
    Data:datetime
    UnidadeDestinataria: str
    DependenciaDestinataria: Optional[str] = None
    UnidadeRemetente: str
    DependenciaRemetente: Optional[str] = None
    Grupo: Optional[str] = None
    Status: str
    TipoCorreio: str
    NumeroCorreio: int
    Pasta: dict
    Setor: Optional[str] = None
    Transicao: int
    Versao: int

class ItemMsgCorreio(ItemListaCorreio):
    
    OcorreuErro: bool
    MensagemErro: Optional[str] = None
    #NumeroCorreio = None
    #Transicao = None
    #Versao = None
    #Assunto = None
    Ementa: Optional[list] = None
    Conteudo: str
    #TipoCorreio = None
    De: str
    Para: str
    EnviadaPor: str
    EnviadaEm: datetime
    RecebidaPor: str
    RecebidaEm: datetime
    Despachos: Optional[list] = None
    Anexos: Optional[list] = None

class AnexoDict(BaseModel):

    IdAnexo: int
    NomeAnexo: str
    Conteudo: str

class BC_Correios:
    
    def __init__(self, wsdl_url:str, usuario:str, senha:str, correios_por_pasta_pasta_unidade_nome:str='40797', correios_por_pasta_pasta_unidade_ativa:bool=True, correios_por_pasta_pasta_unidade_tipo:str='InstituicaoFinanceira', correios_por_pasta_pasta_tipo:str='CaixaEntrada',correios_por_pasta_apenas_mensagens:bool=True, correios_por_pasta_pesquisar_em_todas_as_pastas:bool=True):
        """
        Inicializa a classe BC_Correios.
        Parâmetros:
        - wsdl_url (str): URL do WSDL do serviço dos Correios.
        - usuario (str): Nome de usuário para autenticação no serviço dos Correios.
        - senha (str): Senha para autenticação no serviço dos Correios.
        - correios_por_pasta_pasta_unidade_nome (str, opcional): Nome da unidade da pasta dos Correios. Valor padrão é '40797'.
        - correios_por_pasta_pasta_unidade_ativa (bool, opcional): Indica se a unidade da pasta dos Correios está ativa. Valor padrão é True.
        - correios_por_pasta_pasta_unidade_tipo (str, opcional): Tipo da unidade da pasta dos Correios. Valor padrão é 'InstituicaoFinanceira'.
        - correios_por_pasta_pasta_tipo (str, opcional): Tipo da pasta dos Correios. Valor padrão é 'CaixaEntrada'.
        - correios_por_pasta_apenas_mensagens (bool, opcional): Indica se deve retornar apenas mensagens da pasta dos Correios. Valor padrão é True.
        - correios_por_pasta_pesquisar_em_todas_as_pastas (bool, opcional): Indica se deve pesquisar em todas as pastas dos Correios. Valor padrão é True.
        """

        try:

            session = Session()
            session.auth = HTTPBasicAuth(usuario,senha)
            
            transport = Transport(session=session,timeout=120,operation_timeout=120)
            
            self.client = Client(wsdl_url, transport=transport)
            self.is_connected = True
            self.error = None
            self.CorreiosPorPastaPastaUnidadeNome = correios_por_pasta_pasta_unidade_nome
            self.CorreiosPorPastaPastaUnidadeAtiva = correios_por_pasta_pasta_unidade_ativa
            self.CorreiosPorPastaPastaUnidadeTipo = correios_por_pasta_pasta_unidade_tipo
            self.CorreiosPorPastaPastaTipo = correios_por_pasta_pasta_tipo
            self.CorreiosPorPastaApenasMensagens = correios_por_pasta_apenas_mensagens
            self.CorreiosPorPastaPesquisarEmTodasAsPastas = correios_por_pasta_pesquisar_em_todas_as_pastas
        
        except Exception as e:
            
            self.is_connected = False
            self.error = e

    def consultar_pastas_autorizadas(self)->Tuple[bool, Union[PastasAutorizadas, Exception]]:
        """
        Retorna as pastas de correio e os setores que o usuário tem permissão de acessar.
        """
        
        try:
        
            response = self.client.service.ConsultarPastasAutorizadas()
            
            if response.OcorreuErro:
            
                raise Exception(response.MensagemErro)
            
            pastas = PastasAutorizadas(MensagemErro=response.MensagemErro, OcorreuErro=response.OcorreuErro, QuantidadePastasAutorizadas=response.QuantidadePastasAutorizadas,PastasAutorizadas=response.PastasAutorizadas.PastaAutorizadaWSDTO)
            
            return True, pastas
        
        except Exception as e:
        
            return False, e

    def consultar_correios_por_pasta(self,ultimos_x_dias:int=None,data_inicial:datetime=None,data_final:datetime=None)->Tuple[bool, Union[List['ItemListaCorreio'], Exception]]:

        """
        Retorna uma lista com os cabeçalhos dos correios contidos em uma pasta.

        A consulta pode ser realizada de 2 maneiras:
        1. Especificando um intervalo de dias relativos ao dia atual (com `ultimos_x_dias`).
        2. Informando explicitamente uma `data_inicial` E `data_final`.

        Args:
            ultimos_x_dias (int, opcional): O número de dias a contar para trás a partir da data atual. Se especificado, ignorará `data_inicial` e `data_final`.
            data_inicial (datetime, opcional): Data inicial do intervalo para filtrar os correios.
            data_final (datetime, opcional): Data final do intervalo para filtrar os correios.

        Returns:
            tuple: Um par contendo:
                - bool: Indica se a operação foi bem-sucedida (True) ou falhou (False).
                - Union[list[ItemListaCorreio], Exception]: Retorna uma lista de objetos `ItemListaCorreio` contendo os detalhes dos correios encontrados, ou uma exceção em caso de erro.
        """

        try:
            
            if ultimos_x_dias is not None and isinstance(ultimos_x_dias,int):
                
                agora = datetime.now()
                
                # Pegando mensagens antigas, ja lidas, no desenvolvimento, para nao atrapalhar o time com as mensagens nao lidas atuais
                #logger.warning("VERIFICAR DATA DO 'AGORA'!")
                #agora = datetime.now() - timedelta(days=150)
                
                dt_inicial_iso_format = agora - timedelta(days=ultimos_x_dias)
                dt_inicial_iso_format = datetime.combine(dt_inicial_iso_format.date(), time.min)
                dt_inicial_iso_format = dt_inicial_iso_format.isoformat()
                
                dt_final_iso_format = datetime.combine(agora.date(), time.max)
                dt_final_iso_format = agora.isoformat()
            
            elif data_inicial is isinstance(data_inicial,datetime) and data_final is isinstance(data_final,datetime):
                
                dt_inicial_iso_format =  data_inicial.isoformat()
                dt_final_iso_format = data_final.isoformat()
            
            else:
                
                raise ValueError("ultimos_x_dias se for informado, precisa ser um numero inteiro. Ou entao se for informado data_inicial E data_final, esses 2 parametros precisam ser datetime")

            correios_filtrados = []
            correios_repetidos = []
            pagina_atual = 1
            
            def objeto_ja_existe_na_lista(novo_item, lista_de_correios):

                for item in lista_de_correios:

                    if (str(item.NumeroCorreio) == str(novo_item.NumeroCorreio)):

                        return True

                return False

            proxima_centena = 100
            while True:

                correios = None
                params = {
                    'Pasta': {
                        'Unidade': {
                            'Nome': self.CorreiosPorPastaPastaUnidadeNome,
                            'Ativa': self.CorreiosPorPastaPastaUnidadeAtiva,
                            'Tipo': self.CorreiosPorPastaPastaUnidadeTipo
                        },
                        'Tipo': self.CorreiosPorPastaPastaTipo
                    },
                    'ApenasMensagens': self.CorreiosPorPastaApenasMensagens,
                    'PesquisarEmTodasAsPastas': self.CorreiosPorPastaPesquisarEmTodasAsPastas,
                    'Pagina': pagina_atual,
                    'DataInicial': dt_inicial_iso_format,
                    'DataFinal': dt_final_iso_format,
                }
                
                response = self.client.service.ConsultarCorreiosPorPasta(params)
                
                if response.OcorreuErro:
                    raise Exception(f"Erro ao consultar correios: {response.MensagemErro}")
                
                # Verifica a quantidade total de correios na primeira iteração
                try:

                    # Acessa a lista de correios diretamente
                    correios = response.Correios.ResumoCorreioWSDTO
                    
                    if not correios:

                        # Se não houver mais itens, paramos a busca
                        break
                except:

                    # Fim da listagem de correios
                    break
                
                for correio in correios:
                    
                    item_de_lista_de_correios = ItemListaCorreio(
                        Assunto=correio.Assunto,
                        Data=correio.Data,
                        UnidadeDestinataria=correio.UnidadeDestinataria,
                        DependenciaDestinataria=correio.DependenciaDestinataria,
                        UnidadeRemetente=correio.UnidadeRemetente,
                        DependenciaRemetente=correio.DependenciaRemetente,
                        Grupo=correio.Grupo,
                        Status=correio.Status,
                        TipoCorreio=correio.TipoCorreio,
                        NumeroCorreio=correio.NumeroCorreio,
                        Pasta={
                            'Unidade': correio.Pasta.Unidade,
                            'Dependencia': correio.Pasta.Dependencia,
                            'Setor': correio.Pasta.Setor,
                            'Tipo': correio.Pasta.Tipo
                            },
                        Setor=correio.Setor,
                        Transicao=correio.Transicao,
                        Versao=correio.Versao
                        )
                    if objeto_ja_existe_na_lista(novo_item=item_de_lista_de_correios,lista_de_correios=correios_filtrados) == False:

                        correios_filtrados.append(item_de_lista_de_correios)
                    else:
                        correios_repetidos.append(item_de_lista_de_correios)

                if len(correios_filtrados) >= proxima_centena:

                    log.info(f"Página #{pagina_atual}: {len(correios_filtrados)} correios armazenados no total")
                    proxima_centena = proxima_centena + 100

                # Avança para a próxima página
                pagina_atual += 1

            #return True, correios_filtrados
            return {"success": True, "data": correios_filtrados, "error": None}

        except Exception as e:

            return {"success": False, "data": None, "error": str(e)}

    def ler_correio(self, numero:int,data_rebimento:datetime,tipo:str,transicao:int,versao:int,pasta:str)-> Tuple[bool, Union[ItemMsgCorreio, Exception]]:
        """
        Retorna o conteúdo de um correio.
        
        Args:
            correio (ItemListaCorreio): objeto da classe ItemListaCorreio (item da listagem de mensagens)
        
        Returns:
            tuple: Um par contendo:
                - bool: Indica se a operação foi bem-sucedida (True) ou falhou (False).
                - Union[ItemMsgCorreio, Exception]: Retorna um objeto da classe ItemMsgCorreio contendo os detalhes do correio lido, ou uma exceção em caso de erro.
        """

        try:

            # Substituir aspas simples por aspas duplas
            pasta = pasta.replace("'", '"').replace("None", "null")
            pasta = json.loads(pasta)
            #params = {
            #    'Correio': {
            #        'NumeroCorreio': correio.NumeroCorreio,
            #        'Data': correio.Data.isoformat(),
            #        'TipoCorreio': correio.TipoCorreio,
            #        'Transicao': correio.Transicao,
            #        'Versao': correio.Versao,
            #        'Pasta': correio.Pasta
            #    }
            #}

            params = {
                'Correio': {
                    'NumeroCorreio': numero,
                    'Data': data_rebimento.isoformat(),
                    'TipoCorreio': tipo,
                    'Transicao': transicao,
                    'Versao': versao,
                    'Pasta': {
                        'Unidade': pasta["Unidade"],
                        'Dependencia': pasta["Dependencia"],
                        'Setor': pasta["Setor"],
                        'Tipo': pasta["Tipo"],
                        }
                }
            }

            response = self.client.service.LerCorreio(params)
            
            if response.OcorreuErro:
                raise Exception(f"Erro ao detalhar correio: {response.MensagemErro}")
            
            AnexoWSDTO = getattr(response.DetalheCorreio.Anexos, 'AnexoWSDTO', [])

            msg_detail = {
                "OcorreuErro": response.OcorreuErro,
                "MensagemErro": response.MensagemErro,
                #msg_detail.NumeroCorreio = response.DetalheCorreio.NumeroCorreio
                #msg_detail.Transicao = response.DetalheCorreio.Transicao
                #msg_detail.Versao = response.DetalheCorreio.Versao
                #msg_detail.Assunto = response.DetalheCorreio.Assunto
                "Ementa": response.DetalheCorreio.Ementa,
                "Conteudo": response.DetalheCorreio.Conteudo,
                #msg_detail.TipoCorreio = response.DetalheCorreio.TipoCorreio
                "De": response.DetalheCorreio.De,
                "Para": response.DetalheCorreio.Para,
                "EnviadaPor": response.DetalheCorreio.EnviadaPor,
                "EnviadaEm": response.DetalheCorreio.EnviadaEm,
                "RecebidaPor": response.DetalheCorreio.RecebidaPor,
                "RecebidaEm": response.DetalheCorreio.RecebidaEm,
                "Despachos": response.DetalheCorreio.Despachos,
                "Anexos": AnexoWSDTO
            }

            return {"success": True, "data": msg_detail, "error": None}

            # Serializa o objeto SOAP em um dicionário Python
            #serialized_response = serialize_object(response)
            
            # Converte o dicionário em um JSON formatado
            #response_json = json.dumps(serialized_response, indent=4, default=str)

            #return True, response_json

        except Exception as e:

            #return False, e
            return {"success": False, "data": None, "error": str(e)}
        
    def obter_anexo(self, numero:int, versao:int, transicao:int,pasta:str,anexo_id:int,file_name:str,conteudo:str)-> Tuple[bool,Union[dict, Exception]]:
        """
        Obtém um anexo de um correio eletrônico.
        
        Args:
            correio (ItemListaCorreio): objeto da classe ItemListaCorreio (item da listagem de mensagens)
            anexo (AnexoDict): um item do dicionário da lista de anexos de ItemListaCorreio
        
        Returns:
            tuple: Um par contendo:
                - bool: Indica se a operação foi bem-sucedida (True) ou falhou (False).
                - Union[dict, Exception]: Retorna um dicionario com dados do anexo, ou uma exceção em caso de erro.

        """
        #logger.info("ANEXOS PARA OBTER")
        #print(correio.Anexos)
        try:
            
            pasta = pasta.replace("'", '"').replace("None", "null")
            pasta = json.loads(pasta)
            
            # Monta os parâmetros para a requisição SOAP
            params = {
                'NumeroCorreio': numero,
                'Versao': versao,
                'Transicao': transicao,
                #'Pasta': pasta,
                'Pasta': {
                        'Unidade': pasta["Unidade"],
                        'Dependencia': pasta["Dependencia"],
                        'Setor': pasta["Setor"],
                        'Tipo': pasta["Tipo"],
                        },
                #'Pasta': {
                #    'Unidade': {
                #        'Nome': pasta['Unidade']['Nome'],
                #        'Ativa': pasta['Unidade']['Ativa'],
                #        'Tipo': pasta['Unidade']['Tipo']
                #    },
                #    'Dependencia': pasta['Dependencia'],
                #    'Setor': {
                #        'Nome': pasta['Setor']['Nome'],
                #        'Ativo': pasta['Setor']['Ativo']
                #    },
                #    'Tipo': pasta['Tipo']
                #},
                'Anexo': {
                    'IdAnexo': anexo_id,
                    'NomeAnexo': file_name,
                    'Conteudo': conteudo  # Conteúdo em base64
                }
            }

            # Faz a requisição SOAP para o método ObterAnexo
            response = self.client.service.ObterAnexo(parametros=params)
            #logger.info("response")
            #logger.info(response)
            
            # Acessa os dados da resposta (IdAnexo, NomeAnexo, Conteudo)
            if response and hasattr(response, 'Anexo'):
                id_anexo = response.Anexo.IdAnexo
                nome_anexo = response.Anexo.NomeAnexo
                conteudo_anexo = response.Anexo.Conteudo
                
                # Retorna os dados capturados como um dicionário
                #return True, {
                #    'IdAnexo': id_anexo,
                #    'NomeAnexo': nome_anexo,
                #    'Conteudo': conteudo_anexo
                #}
                return {"success": True, "error": None, "data": conteudo_anexo}
            else:
                return {"success": True, "error": "Correio não possui anexo", "data": None}
                #return False, Exception("Correio não possui anexo")
        
        except Exception as e:
            
            return {"success": False, "error": str(e), "data": None}
            #return False, e

    def encerrar(self):
        """Fecha o cliente e libera a sessão."""
        
        try:
        
            self.client.transport.session.close()
        
        except:
            
            pass

