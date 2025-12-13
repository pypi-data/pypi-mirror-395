import requests
import json
import re
import openai
import time
import logging
import base64
import jwt
from pydantic import BaseModel, ValidationError, field_validator
from typing import List, Dict, Any, Optional
from datetime import datetime

jerry_prompt = "Jerry: "

class JerryConfigValidator(BaseModel):
    """Validador para configurações do Jerry usando Pydantic V2"""
    username: str
    password: str
    verbose: bool = False
    api_base_url: str
    ia_model: str

    @field_validator('username', 'password', 'api_base_url', 'ia_model')
    @classmethod
    def validate_non_empty_string(cls, v: str) -> str:
        """Valida se o campo é uma string não vazia"""
        if not isinstance(v, str):
            raise ValueError('deve ser uma string')
        if not v.strip():
            raise ValueError('não pode estar vazio')
        return v.strip()

    @field_validator('api_base_url')
    @classmethod
    def validate_url_format(cls, v: str) -> str:
        """Valida se a URL tem formato básico"""
        v = v.strip()
        if not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('deve começar com http:// ou https://')
        return v

class InterpretarTextoValidator(BaseModel):
    """Validador para o método interpretar_texto"""
    system_prompt: str
    user_prompt: str
    
    @field_validator('system_prompt', 'user_prompt')
    @classmethod
    def validate_prompts(cls, v: str) -> str:
        """Valida se os prompts são strings válidas para interpretação"""
        if not isinstance(v, str):
            raise ValueError('prompt deve ser uma string')
        
        # Remove espaços em branco e caracteres de controle
        texto_limpo = v.strip()
        
        if not texto_limpo:
            raise ValueError('prompt não pode estar vazio')
        if len(texto_limpo) < 3:
            raise ValueError('prompt deve ter pelo menos 3 caracteres')
        if len(v) > 1000000:
            raise ValueError('prompt excede o limite máximo de 1.000.000 caracteres')
        
        # Validação adicional para caracteres especiais excessivos
        if len([c for c in texto_limpo if c.isalpha()]) < 2:
            raise ValueError('prompt deve conter pelo menos 2 caracteres alfabéticos')
            
        return texto_limpo
    
class JerryClient:
    def __init__(self, username: str, password: str, api_base_url: str = "https://cia-api-jerry.karavela-shared-stg.aws.karavela.run", ia_model: str = "databricks-llama-4-maverick", verbose: bool = False):
        """
        Inicializa o cliente Jerry com validação usando Pydantic V2.
        
        Args:
            username (str): Nome de usuário para autenticação
            password (str): Senha para autenticação  
            api_url (str): URL da API do Jerry
            ia_model (str): Modelo de IA a ser usado
            verbose (bool): Se o modulo vai fazer output de logs (default = False)
            
        Raises:
            ValueError: Se algum parâmetro for inválido
        """
        
        try:
            # Validação usando Pydantic V2
            config = JerryConfigValidator(
                username=username,
                password=password,
                verbose=verbose,
                api_base_url=api_base_url,
                ia_model=ia_model
            )
            
            # Atribuição dos valores validados
            self.verbose = verbose
            self.username = config.username
            self.password = config.password
            self.verbose = config.verbose
            if self.verbose:
                self.log = logging.getLogger("__main__")
            else:
                self.log = logging.getLogger(__file__)
                self.log.setLevel(logging.CRITICAL)

            self.api_base_url = config.api_base_url.rstrip('/')
            self.api_login_url = f"{self.api_base_url}/login"
            self.api_v1_url = f"{self.api_base_url}/v1/databricks"
            self.ia_model = config.ia_model
            self.is_connected = False
            self.error = None
            self.client = None
            self.headers_authenticated = None
            self.token_info = None
            self.token = self._autenticar()
            
        except ValidationError as e:
            self.is_connected = False
            error_details = []
            for error in e.errors():
                field = error['loc'][0] if error['loc'] else 'unknown'
                message = error['msg']
                error_details.append(f"{field}: {message}")
            
            error_msg = f"Erro na validação dos parâmetros do Jerry: {'; '.join(error_details)}"
            self.log.error(error_msg)
            self.is_connected = False
            self.error = error_msg

        except Exception as e:
            error_msg = f"Erro inesperado na inicialização do Jerry: {e}"
            self.log.error(error_msg)
            self.is_connected = False
            self.error = error_msg
    
    def _extrair_info_token(self, token: str) -> dict:
        """
        Decodifica o token JWT e extrai informações de expiração.
        
        Returns:
            dict: {
                "exp": datetime,  # Data/hora de expiração
                "iat": datetime,  # Data/hora de emissão
                "duracao_segundos": int,  # Duração em segundos
                "tempo_restante_segundos": int  # Tempo até expirar
            }
        """
        try:
            # Decodifica sem verificar assinatura (apenas para ler dados)
            decoded = jwt.decode(token, options={"verify_signature": False})
            agora = datetime.now()
            
            # Extrai timestamps
            exp_timestamp = decoded.get("exp")  # Expiration time
            iat_timestamp = decoded.get("iat")  # Issued at time
            
            if not exp_timestamp:
                self.log.error(f"{jerry_prompt}❌ Token JWT não contém campo 'exp' (expiração)")
                return None
            
            # Converte expiração para datetime
            exp_datetime = datetime.fromtimestamp(exp_timestamp)

            # CORREÇÃO: Se não tem iat, usa o momento atual como estimativa
            if iat_timestamp:
                iat_datetime = datetime.fromtimestamp(iat_timestamp)
            else:
                # Token foi emitido agora (estimativa)
                iat_datetime = agora
                iat_timestamp = int(agora.timestamp())

            # Calcula duração e tempo restante
            tempo_restante = (exp_datetime - agora).total_seconds()
            duracao = (exp_datetime - agora).total_seconds()
            
            return {
                "exp": exp_datetime,
                "iat": iat_datetime,
                "exp_timestamp": exp_timestamp,
                "iat_timestamp": iat_timestamp,
                "duracao_segundos": int(duracao) if duracao else None,
                "tempo_restante_segundos": int(tempo_restante),
                "expirado": tempo_restante <= 0
            }
            
        except Exception as e:
            self.log.error(f"{jerry_prompt}❌ Erro ao decodificar token: {e}")
            return None
    
    def _token_proximo_de_expirar(self, margem_segundos: int = 300) -> bool:
        """
        Verifica se o token está próximo de expirar (padrão: 5 minutos).
        
        Args:
            margem_segundos (int): Margem de segurança em segundos (default: 300 = 5 min)
        
        Returns:
            bool: True se token vai expirar em menos de margem_segundos
        """
        if not self.token_info:
            return True  # Se não tem info, considera expirado
        
        tempo_restante = self.token_info.get("tempo_restante_segundos", 0)
        return tempo_restante <= margem_segundos

    def _autenticar(self) -> Optional[dict]:
        try:
            headers_not_authenticated = {
                "Content-Type": "application/json"
            }
            response = requests.post(self.api_login_url, json={"email": self.username, "password": self.password}, headers=headers_not_authenticated, timeout=60)

            if response.status_code == 503:
                self.headers_authenticated = {
                    "Content-Type": "application/json"
                }
                self.is_connected = False
                self.error = "503 Service Temporarily Unavailable. Tente novamente mais tarde."
                return None

            # Request retornado
            token = response.json().get("access_token", None)

            if not token:
                self.headers_authenticated = {
                    "Content-Type": "application/json"
                }
                self.is_connected = False
                self.error = "Token de autenticação não recebido"
                return None
            
            # Token recebido com sucesso
            self.headers_authenticated = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            self.client = openai.OpenAI(
                base_url=self.api_v1_url,
                api_key=token,
                timeout=60
            )
            token_info = self._extrair_info_token(token)

            if token_info:
                self.log.info(f"{jerry_prompt}🔑 Token recebido:")
                self.log.info(f"{jerry_prompt}- Emitido em: {token_info['iat'].strftime('%Y-%m-%d %H:%M:%S')}")
                self.log.info(f"{jerry_prompt}- Expira em: {token_info['exp'].strftime('%Y-%m-%d %H:%M:%S')}")
                self.log.info(f"{jerry_prompt}- Duração: {token_info['duracao_segundos']}s ({token_info['duracao_segundos']//60} min)")
                self.log.info(f"{jerry_prompt}- Tempo restante: {token_info['tempo_restante_segundos']}s ({token_info['tempo_restante_segundos']//60} min)")

                # Salva info do token
                self.token_info = token_info

            self.is_connected = True
            self.error = None
            return token
        except Exception as e:
            self.is_connected = False
            self.error = f"Erro na autenticação: {e}"
            return None

    def v1_enviar_para_ia(self, system_prompt: str, user_prompt: str, arquivos: Optional[List[Dict[str, str]]] = None, tools: Optional[List[Dict[str, Any]]] = None, temperature: float = None, tool_choice: Optional[str] = None) -> Dict[str, Any]:
        """
        Envia prompts e opcionalmente múltiplas imagens para a IA via Databricks.
        
        IMPORTANTE: Este método aceita APENAS imagens. Outros tipos de arquivo serão rejeitados.
        
        Args:
            system_prompt (str): Prompt do sistema para configurar o comportamento da IA
            user_prompt (str): Prompt do usuário com a solicitação específica
            arquivos (Optional[List[Dict[str, str]]]): Lista de imagens, cada uma com:
                - base64: String base64 da imagem (sem prefixo data:)
                - mime_type: Tipo MIME da imagem (deve ser image/*)
                - name: Nome/descrição da imagem (opcional, para logs)
                - file_path: Caminho original da imagem (opcional, para logs)
            temperature (float): Temperatura para a geração de texto (default = None)
            tools (Optional[List[Dict[str, Any]]]): Lista de ferramentas (tools) para fornecer à IA
            tool_choice (Optional[str]): required, auto
        
        Tipos de imagem suportados:
            ✅ image/jpeg, image/jpg, image/png, image/gif, image/webp, image/bmp, image/tiff
            ❌ Qualquer outro tipo será rejeitado com erro específico
        
        Returns:
            Dict[str, Any]: Resultado da operação contendo:
                - success (bool): True se operação foi bem-sucedida
                - error (str|None): Mensagem de erro específica se houver falha
                - content (dict|None): Conteúdo processado da resposta da IA
                - input_tokens (int): Número de tokens de entrada utilizados
                - output_tokens (int): Número de tokens de saída gerados
                - total_tokens (int): Total de tokens utilizados
                - images_validated (dict): Estatísticas das imagens validadas
        
        Validações realizadas:
            1. Prompts não podem estar vazios
            2. Arquivos devem ter mime_type de imagem
            3. Base64 deve ser válido e decodificável
            4. Imagem decodificada deve ter conteúdo
            5. Tamanho total das imagens não deve exceder 50MB
        """
        
        def _validar_base64_formato(base64_string: str) -> bool:
            """Valida o formato da string base64"""
            try:
                # Remove espaços e quebras de linha
                base64_clean = base64_string.strip().replace('\n', '').replace('\r', '').replace(' ', '')
                
                if not base64_clean:
                    return False
                    
                # Verifica se tem apenas caracteres válidos de base64
                if not re.match(r'^[A-Za-z0-9+/]*={0,2}$', base64_clean):
                    return False
                    
                # Verifica se o comprimento é múltiplo de 4
                if len(base64_clean) % 4 != 0:
                    return False
                    
                return True
                
            except Exception:
                return False

        def _validar_cabecalho_imagem(data: bytes, mime_type: str) -> bool:
            """Valida se os bytes iniciais correspondem ao tipo de imagem"""
            try:
                if len(data) < 10:
                    return False
                    
                # Assinaturas de arquivo por tipo
                signatures = {
                    'image/jpeg': [b'\xff\xd8\xff'],
                    'image/jpg': [b'\xff\xd8\xff'], 
                    'image/png': [b'\x89PNG\r\n\x1a\n'],
                    'image/gif': [b'GIF87a', b'GIF89a'],
                    'image/webp': [b'RIFF', b'WEBP'],
                    'image/bmp': [b'BM'],
                    'image/tiff': [b'II*\x00', b'MM\x00*']
                }
                
                expected_sigs = signatures.get(mime_type.lower(), [])
                
                for sig in expected_sigs:
                    if data.startswith(sig):
                        return True
                        
                # Para WEBP, verificação adicional
                if mime_type.lower() == 'image/webp':
                    return data.startswith(b'RIFF') and b'WEBP' in data[:12]
                    
                return len(expected_sigs) == 0  # Se não tem assinatura conhecida, aceita
                
            except Exception:
                return False

        # 1. VALIDAÇÃO DOS PROMPTS
        try:
            validator = InterpretarTextoValidator(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
            system_prompt = validator.system_prompt
            user_prompt = validator.user_prompt
        except ValidationError as e:
            error_details = []
            for error in e.errors():
                field = error['loc'][0] if error['loc'] else 'unknown'
                message = error['msg']
                error_details.append(f"{field}: {message}")
            
            error_msg = f"❌ Validação dos prompts falhou: {'; '.join(error_details)}"
            self.log.error(error_msg)
            return {
                "success": False, 
                "error": error_msg, 
                "content": None, 
                "input_tokens": 0, 
                "output_tokens": 0, 
                "total_tokens": 0,
                "images_validated": {"total": 0, "valid": 0, "rejected": 0}
            }
        
        # 2. VALIDAÇÃO DOS ARQUIVOS/IMAGENS
        images_stats = {"total": 0, "valid": 0, "rejected": 0, "rejected_files": []}
        validated_images = []
        validation_errors = []
        
        if arquivos and len(arquivos) > 0:
            images_stats["total"] = len(arquivos)
            
            # Tipos de imagem suportados pelo Databricks
            tipos_imagem_suportados = {
                'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
                'image/webp', 'image/bmp', 'image/tiff', 'image/svg+xml'
            }
            
            self.log.info(f"{jerry_prompt}🔍 Validando {len(arquivos)} arquivo(s)...")
            
            total_size = 0
            
            for i, arquivo in enumerate(arquivos, 1):
                arquivo_name = arquivo.get("name", f"arquivo_{i}")
                arquivo_mime = arquivo.get("mime_type", "").lower().strip()
                arquivo_base64 = arquivo.get("base64", "")
                
                # 2.1 Validar se tem MIME type
                if not arquivo_mime:
                    error = f"Arquivo '{arquivo_name}': MIME type não informado"
                    validation_errors.append(error)
                    images_stats["rejected"] += 1
                    images_stats["rejected_files"].append({"filename": arquivo_name, "error": error})
                    self.log.error(f"{jerry_prompt}   ❌ {error}")
                    continue
                
                # 2.2 Validar se é imagem
                if not arquivo_mime.startswith('image/'):
                    error = f"Arquivo '{arquivo_name}': Tipo '{arquivo_mime}' não é imagem. Apenas imagens são aceitas."
                    validation_errors.append(error)
                    images_stats["rejected"] += 1
                    images_stats["rejected_files"].append({"filename": arquivo_name, "error": error})
                    self.log.error(f"{jerry_prompt}   ❌ {error}")
                    continue
                
                # 2.3 Validar se é tipo de imagem suportado
                if arquivo_mime not in tipos_imagem_suportados:
                    error = f"Imagem '{arquivo_name}': Tipo '{arquivo_mime}' não suportado. Tipos aceitos: {', '.join(sorted(tipos_imagem_suportados))}"
                    validation_errors.append(error)
                    images_stats["rejected"] += 1
                    images_stats["rejected_files"].append({"filename": arquivo_name, "error": error})
                    self.log.error(f"{jerry_prompt}   ❌ {error}")
                    continue
                
                # 2.4 Validar se tem base64
                if not arquivo_base64:
                    error = f"Imagem '{arquivo_name}': Base64 não informado"
                    validation_errors.append(error)
                    images_stats["rejected"] += 1
                    images_stats["rejected_files"].append({"filename": arquivo_name, "error": error})
                    self.log.error(f"{jerry_prompt}   ❌ {error}")
                    continue
                
                # 2.5 Validar formato do base64
                if not _validar_base64_formato(arquivo_base64):
                    error = f"Imagem '{arquivo_name}': Base64 com formato inválido"
                    validation_errors.append(error)
                    images_stats["rejected"] += 1
                    images_stats["rejected_files"].append({"filename": arquivo_name, "error": error})
                    self.log.error(f"{jerry_prompt}   ❌ {error}")
                    continue
                
                # 2.6 Validar se base64 pode ser decodificado
                try:
                    decoded_data = base64.b64decode(arquivo_base64, validate=True)
                    if len(decoded_data) == 0:
                        error = f"Imagem '{arquivo_name}': Base64 decodificado está vazio"
                        validation_errors.append(error)
                        images_stats["rejected"] += 1
                        images_stats["rejected_files"].append({"filename": arquivo_name, "error": error})
                        self.log.error(f"{jerry_prompt}   ❌ {error}")
                        continue
                except Exception as e:
                    error = f"Imagem '{arquivo_name}': Erro ao decodificar base64: {str(e)}"
                    validation_errors.append(error)
                    images_stats["rejected"] += 1
                    images_stats["rejected_files"].append({"filename": arquivo_name, "error": error})
                    self.log.error(f"{jerry_prompt}   ❌ {error}")
                    continue
                
                # 2.7 Validar tamanho da imagem
                image_size = len(decoded_data)
                total_size += image_size
                
                # Limite por imagem: 4MB
                if image_size > 4 * 1024 * 1024:
                    error = f"Imagem '{arquivo_name}': Tamanho muito grande ({image_size:,} bytes). Máximo: 4MB"
                    validation_errors.append(error)
                    images_stats["rejected"] += 1
                    images_stats["rejected_files"].append({"filename": arquivo_name, "error": error})
                    self.log.error(f"{jerry_prompt}   ❌ {error}")
                    continue
                
                # 2.8 Validar se é realmente uma imagem (verificação básica)
                if not _validar_cabecalho_imagem(decoded_data, arquivo_mime):
                    error = f"Imagem '{arquivo_name}': Arquivo não parece ser uma imagem válida do tipo {arquivo_mime}"
                    validation_errors.append(error)
                    images_stats["rejected"] += 1
                    images_stats["rejected_files"].append({"filename": arquivo_name, "error": error})
                    self.log.error(f"{jerry_prompt}   ❌ {error}")
                    continue
                
                # ✅ Imagem válida
                validated_images.append(arquivo)
                images_stats["valid"] += 1
                self.log.info(f"{jerry_prompt}   ✅ {arquivo_name} ({arquivo_mime}, {image_size:,} bytes)")
            
            # 2.9 Validar tamanho total
            if total_size > 4 * 1024 * 1024:  # 4MB total
                error = f"Tamanho total das imagens muito grande ({total_size:,} bytes). Máximo: 4MB"
                validation_errors.append(error)
                self.log.error(f"{jerry_prompt}❌ {error}")

            # 2.10 Verificar se há imagens válidas
            if images_stats["valid"] == 0 and images_stats["total"] > 0:
                error_summary = "Nenhuma imagem válida encontrada. Erros:\n" + "\n".join(validation_errors)
                self.log.error(f"{jerry_prompt}❌ {error_summary}")
                return {
                    "success": False, 
                    "error": error_summary, 
                    "content": None, 
                    "input_tokens": 0, 
                    "output_tokens": 0, 
                    "total_tokens": 0,
                    "images_validated": images_stats
                }
            
            # 2.11 Log do resumo da validação
            if validation_errors:
                self.log.warning(f"{jerry_prompt}⚠️ Resumo da validação:")
                self.log.warning(f"{jerry_prompt}   📁 Total de arquivos: {images_stats['total']}")
                self.log.warning(f"{jerry_prompt}   ✅ Imagens válidas: {images_stats['valid']}")
                self.log.warning(f"{jerry_prompt}   ❌ Rejeitadas: {images_stats['rejected']}")
                self.log.warning(f"{jerry_prompt}   📊 Tamanho total: {total_size:,} bytes")

                return {
                    "success": False, 
                    "error": "Algumas imagens foram rejeitadas. Veja os logs para detalhes.", 
                    "content": None, 
                    "input_tokens": 0, 
                    "output_tokens": 0, 
                    "total_tokens": 0,
                    "images_validated": images_stats
                }
            else:
                self.log.info(f"{jerry_prompt}✅ Todas as {images_stats['valid']} imagem(ns) passaram na validação")
        
        # 3. VERIFICAÇÃO DO TOKEN
        if not self.is_connected:
            error_msg = "Conexão com Jerry não estabelecida. Verifique as credenciais."
            self.log.error(f"{jerry_prompt}❌ {error_msg}")
            return {
                "success": False, 
                "error": error_msg, 
                "content": None, 
                "input_tokens": 0, 
                "output_tokens": 0, 
                "total_tokens": 0,
                "images_validated": images_stats
            }
        # Verificando se token esta proximo de expirar
        if self._token_proximo_de_expirar():
            self.log.info(f"{jerry_prompt}🔄 Token próximo de expirar. Renovando...")
            try:
                novo_token = self._autenticar()
                if novo_token:
                    self.token = novo_token
                    self.log.info(f"{jerry_prompt}✅ Token renovado com sucesso")
                else:
                    self.log.error(f"{jerry_prompt}❌ Falha na renovação do token")
            except Exception as auth_error:
                self.log.error(f"{jerry_prompt}❌ Erro durante renovação do token: {auth_error}")

        # 4. PREPARAÇÃO E ENVIO COM TOOLS (SE FORNECIDO)
        if tools:
            self.log.info(f"{jerry_prompt}🔧 Ferramentas fornecidas para a IA:")
            for tool in tools:
                self.log.info(f"{jerry_prompt}   - {tool['function']['name']}: {tool['function']['description']}")

        # 5. REQUISIÇÃO PARA O DATABRICKS
        max_retries = 3
        error_msg = None
        for attempt in range(max_retries):
            try:
                self.log.info(f"{jerry_prompt}🔄 Tentativa {attempt + 1}/{max_retries}")

                # Mensagem do sistema
                messages: List[Dict[str, Any]] = [
                    {"role": "system", "content": system_prompt}
                ]
                
                # Mensagem do usuário com imagens validadas
                if validated_images:
                    self.log.info(f"{jerry_prompt}Anexando {len(validated_images)} imagem(ns) validada(s)...")
                    
                    user_content = [{"type": "text", "text": user_prompt}]
                    
                    for imagem in validated_images:
                        image_content = {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{imagem['mime_type']};base64,{imagem['base64']}"
                            }
                        }
                        user_content.append(image_content)
                    
                    messages.append({"role": "user", "content": user_content})
                else:
                    # Apenas texto
                    self.log.info(f"{jerry_prompt}📝 Enviando apenas texto (sem imagens)")
                    messages.append({"role": "user", "content": user_prompt})

                # Requisição
                self.log.info(f"{jerry_prompt}🚀 Enviando para Databricks (modelo: {self.ia_model})...")

                # Parâmetros obrigatórios
                request_params = {
                    "model": self.ia_model,
                    "messages": messages,
                }

                # Parâmetros opcionais - só adiciona se não for None
                if tools is not None:
                    request_params["tools"] = tools
                    self.log.info(f"{jerry_prompt}🔧 Tools adicionadas: {len(tools)} ferramenta(s)")

                if tool_choice is not None:
                    request_params["tool_choice"] = tool_choice
                    self.log.info(f"{jerry_prompt}⚙️ Tool choice: {tool_choice}")

                if temperature is not None:
                    request_params["temperature"] = temperature
                    self.log.info(f"{jerry_prompt}🌡️ Temperature: {temperature}")

                response = self.client.chat.completions.create(**request_params)

                # ✅ SUCESSO
                self.log.info(f"{jerry_prompt}✅ Resposta recebida com sucesso!")
                self.log.info(f"{jerry_prompt}📊 Tokens - Entrada: {response.usage.prompt_tokens}, Saída: {response.usage.completion_tokens}, Total: {response.usage.total_tokens}")
                self.log.info(f"{jerry_prompt}📄 Resposta bruta: {json.dumps(response.model_dump(), ensure_ascii=False)}")

                content_processado = response.model_dump()

                return {
                    "success": True, 
                    "error": None, 
                    "content": content_processado, 
                    "input_tokens": response.usage.prompt_tokens, 
                    "output_tokens": response.usage.completion_tokens, 
                    "total_tokens": response.usage.total_tokens,
                    "images_validated": images_stats
                }

            # Tratamento de exceções

            except openai.BadRequestError as e:
                try:
                    # O body geralmente tem estrutura: {"error": {"message": "texto do erro"}}
                    body = e.body
                    if isinstance(body, dict):

                        # Tentar extrair message do error object
                        if "error" in body and isinstance(body["error"], dict):
                            if "message" in body["error"]:
                                error_msg = body["error"]["message"]

                        # Fallback: message diretamente no body
                        elif "message" in body:
                            error_msg = body["message"]
                        
                        # Fallback: detail diretamente no body
                        elif "detail" in body:
                            error_msg = body["detail"]
                        
                        # Fallback: converter body para string se não achar message
                        else:
                            error_msg = str(body)
                    else:
                        # Se body não for dict, converter para string
                        error_msg = str(body)

                except (AttributeError, KeyError, TypeError):
                    # Se falhar ao acessar body, usar mensagem padrão
                    error_msg = str(e)

                self.log.error(f"{jerry_prompt}❌ Requisição malformada: {e}")
                return {
                    "success": False,
                    "error": error_msg,
                    "content": None,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "total_tokens": 0,
                    "images_validated": images_stats
                }

            except openai.AuthenticationError as e:

                error_msg = str(e).lower()

                if any(keyword in error_msg for keyword in ['token inválido', 'token expirado', 'expired', 'invalid', 'unauthorized']):
                    if attempt < max_retries - 1:
                        self.log.info(f"{jerry_prompt}🔄 Token inválido/expirado detectado. Renovando...")
                        try:
                            novo_token = self._autenticar()
                            if novo_token:
                                self.token = novo_token
                                self.log.info(f"{jerry_prompt}✅ Token renovado com sucesso")
                                time.sleep(1)
                                continue
                            else:
                                self.log.error(f"{jerry_prompt}❌ Falha na renovação do token")
                                break
                        except Exception as auth_error:
                            self.log.error(f"{jerry_prompt}❌ Erro durante renovação do token: {auth_error}")
                            break
                    else:
                        self.log.error(f"{jerry_prompt}❌ Esgotaram as tentativas de renovação")
                        break
                else:
                    self.log.error(f"{jerry_prompt}❌ Erro de autenticação não relacionado ao token")
                    break
                    
            except openai.RateLimitError as e:
                self.log.warning(f"{jerry_prompt}⏱️ Rate limit atingido: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    self.log.info(f"{jerry_prompt}⏳ Aguardando {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    break
                    
            except openai.APITimeoutError as e:
                self.log.warning(f"{jerry_prompt}⏰ Timeout na requisição: {e}")
                if attempt < max_retries - 1:
                    self.log.info(f"{jerry_prompt}🔄 Tentando novamente...")
                    time.sleep(2)
                    continue
                else:
                    break
                    
            except openai.APIError as e:
                error_msg = str(e)
                self.log.error(f"{jerry_prompt}❌ Erro da API Databricks: {e}")
                
                if any(keyword in error_msg.lower() for keyword in ['temporary', 'temporarily', 'retry', 'server error', '500', '502', '503']):
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 3
                        self.log.info(f"{jerry_prompt}🔄 Erro temporário detectado. Tentando novamente em {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        break
                else:
                    break
                    
            except Exception as e:
                error_msg = f"Erro ao enviar requisição para Databricks: {e}"
                self.log.error(f"{jerry_prompt}❌ Erro ao enviar requisição para Databricks: {type(e).__name__}: {e}")

                if any(keyword in str(e).lower() for keyword in ['connection', 'network', 'timeout', 'connect']):
                    if attempt < max_retries - 1:
                        self.log.info(f"{jerry_prompt}🔄 Erro de conexão detectado. Tentando novamente...")
                        time.sleep(3)
                        continue
                    else:
                        break
                else:
                    break

        # Falha após todas as tentativas
        if not error_msg:
            error_msg = f"Falha ao completar a requisição após {max_retries} tentativas"
        self.log.error(f"{jerry_prompt}❌ {error_msg}")
        return {
            "success": False, 
            "error": error_msg, 
            "content": None, 
            "input_tokens": 0, 
            "output_tokens": 0, 
            "total_tokens": 0,
            "images_validated": images_stats
        }

    def v1_report(self, start_date:datetime, end_date:datetime) -> list:
        """
        Envio de requisição de relatório de uso de I.A. ao Jerry.
        
        Args:
            start_date (datetime): Data de início do período do relatório
            end_date (datetime): Data de fim do período do relatório
        
        Returns:
            Dict[str, Any]: Resultado da operação contendo:
                - success (bool): True se operação foi bem-sucedida
                - error (str|None): Mensagem de erro específica se houver falha
                - data (list|None): Dados do relatório retornados pela API
                
        Raises:
            ValidationError: Se os parâmetros não atenderem às validações
        """


        # 1. VALIDAÇÃO DOS PARÂMETROS DE ENTRADA
        try:
            # Verifica se são realmente objetos datetime
            if not isinstance(start_date, datetime):
                error_msg = f"start_date deve ser do tipo datetime, recebido: {type(start_date).__name__}"
                self.log.error(f"{jerry_prompt}❌ {error_msg}")
                return {"success": False, "error": error_msg, "data": None}
            
            if not isinstance(end_date, datetime):
                error_msg = f"end_date deve ser do tipo datetime, recebido: {type(end_date).__name__}"
                self.log.error(f"{jerry_prompt}❌ {error_msg}")
                return {"success": False, "error": error_msg, "data": None}
            
            # Obtém o datetime atual
            agora = datetime.now()
            
            # Valida se start_date é menor que end_date
            if start_date >= end_date:
                error_msg = f"start_date ({start_date.isoformat()}) deve ser menor que end_date ({end_date.isoformat()})"
                self.log.error(f"{jerry_prompt}❌ {error_msg}")
                return {"success": False, "error": error_msg, "data": None}
            
            # Valida se end_date é menor ou igual ao momento atual
            if end_date > agora:
                error_msg = f"end_date ({end_date.isoformat()}) não pode ser maior que o momento atual ({agora.isoformat()})"
                self.log.error(f"{jerry_prompt}❌ {error_msg}")
                return {"success": False, "error": error_msg, "data": None}
            
            self.log.info(f"{jerry_prompt}✅ Parâmetros validados:")
            self.log.info(f"{jerry_prompt}   📅 Período: {start_date.isoformat()} até {end_date.isoformat()}")
            self.log.info(f"{jerry_prompt}   ⏱️ Duração: {(end_date - start_date).days} dia(s)")
            
        except Exception as e:
            error_msg = f"Erro na validação dos parâmetros: {str(e)}"
            self.log.error(f"{jerry_prompt}❌ {error_msg}")
            return {"success": False, "error": error_msg, "data": None}
       
        # Convert start_date e end_data para formato ISO 8601
        start_date = start_date.isoformat()
        end_date = end_date.isoformat()
        
        # Montando payload
        payload = {
            "start_date": start_date,
            "end_date": end_date
        }

        try:
            resposta = requests.get(f"{self.api_base_url}/v1/report/costs", json=payload, headers=self.headers_authenticated, timeout=60)
            return {"success": True, "error": None, "data": resposta.json()}

        except Exception as e:
            error_msg = f"Erro ao enviar requisição de relatório: {str(e)}"
            self.log.error(f"{jerry_prompt}❌ {error_msg}")
            return {"success": False, "error": error_msg, "data": None}
