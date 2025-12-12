_Bk="Twilio 'from' number not configured. Cannot send SMS."
_Bj='completedAt'
_Bi='Error: URL template evaluation failed.'
_Bh='contentType'
_Bg='token_type'
_Bf='client_credentials'
_Be='function_call'
_Bd='Error: AI client is not configured.'
_Bc='Cannot get Gemini response: AI client is not initialized.'
_Bb='Using environment credentials/IAM role for S3.'
_Ba='boto3 library is required for S3 operations.'
_BZ='Using Application Default Credentials for GCS.'
_BY='google-cloud-storage library is required for GCS operations.'
_BX='action_action_key'
_BW='__builtins__'
_BV='destinationVariable'
_BU='sourceVariable'
_BT='promptName'
_BS='unknown_intent'
_BR='Error: AI response was malformed (function call had no name).'
_BQ='resp_mime_type'
_BP='gemini-3-pro-preview'
_BO='safetySettings'
_BN='mime_type'
_BM='variables'
_BL='accountId'
_BK='Content-Encoding'
_BJ='DEEPSEEK_API_KEY'
_BI='ANTHROPIC_API_KEY'
_BH='OPENAI_API_KEY'
_BG='EMAIL_FROM_ADDRESS'
_BF='EMAIL_API_KEY'
_BE='GEMINI_API_KEY'
_BD='GCP_REGION'
_BC='GCP_PROJECT'
_BB='WEBSOCKET_URL'
_BA='user_input'
_B9='Journey token not available.'
_B8='Accept-Encoding'
_B7='client_secret'
_B6='client_id'
_B5='grant_type'
_B4='tool_choice'
_B3='max_tokens'
_B2='clientId'
_B1='action_event'
_B0='delivery_method'
_A_='format'
_Az='function'
_Ay='header'
_Ax='gemini-2.0-flash'
_Aw='model_provider'
_Av='agentDefaultIntent'
_Au='intentContainsPairsList'
_At='intentNameList'
_As='value'
_Ar='action_flow'
_Aq='action_type'
_Ap='iframeId'
_Ao='externalRef'
_An='uniqueId'
_Am='customer'
_Al='pipelineKey'
_Ak='assistant'
_Aj='actionFlow'
_Ai='deliveryMethod'
_Ah='privacy'
_Ag='prompt_type'
_Af='gcs_service_account'
_Ae='ragStoreVectorDistanceThreshold'
_Ad='ragStoreTopK'
_Ac='ragStoreResourceId'
_Ab='transferPasskeyFlag'
_Aa='transferAllowed'
_AZ='access_token'
_AY='TWILIO_NUMBER'
_AX='TWILIO_AUTH_TOKEN'
_AW='TWILIO_ACCOUNT_SID'
_AV='parameters'
_AU='Accept'
_AT='failureResponseMessage'
_AS='subject'
_AR='response'
_AQ='string'
_AP='enum'
_AO='required'
_AN='properties'
_AM='deepseek'
_AL='resp_schema'
_AK='maxTokens'
_AJ='candidates'
_AI='top_k'
_AH='temp'
_AG='file_uri_var'
_AF='resp_var'
_AE='startPrompt'
_AD='scope'
_AC='prompt'
_AB='action'
_AA='classification'
_A9='temperature'
_A8='json'
_A7='*/*'
_A6='result'
_A5='env'
_A4='command'
_A3='system'
_A2='anthropic'
_A1='messages'
_A0='var'
_z='inputFillerPrompt'
_y='input'
_x='actionKey'
_w='vectorDistanceThreshold'
_v='topK'
_u='resourceId'
_t='gzip'
_s='accept'
_r='object'
_q='mcp'
_p='journey_iframeId'
_o='delivery'
_n='clientSecret'
_m='grantType'
_l='agentConnector'
_k='message'
_j='openai'
_i='reasoning_effort'
_h='action_response_message'
_g='phoneNumber'
_f='method'
_e='google'
_d='language'
_c='expectedInput'
_b='user'
_a='resultVariable'
_Z='url'
_Y='top_p'
_X='model'
_W='body'
_V='error'
_U='connector'
_T=','
_S='role'
_R='content'
_Q='Content-Type'
_P='text'
_O='tools'
_N='utf-8'
_M='Authorization'
_L='description'
_K='application/json'
_J='agent'
_I='args'
_H='DEBUG'
_G=False
_F='type'
_E='session'
_D=True
_C='name'
_B='data'
_A=None
import asyncio,base64,datetime,json,logging,os,random,re,sys,secrets,time,uuid,websockets,xmltodict
from contextlib import asynccontextmanager
import zoneinfo
from io import StringIO
from typing import Any,Dict,List,Optional,Tuple,Union,TextIO,Type,TypeVar
from urllib.parse import quote
import gzip,grpc,grpc.aio as agrpc,httpx,Levenshtein,markdown,pandas as pd,xmltodict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth import credentials as auth_credentials
from google.oauth2 import service_account
from google.api_core import exceptions as google_api_exceptions
from google import genai
from google.genai import types as google_genai_types
from google.genai.types import FunctionDeclaration,GenerateContentConfig,GoogleSearch,HarmBlockThreshold,HarmCategory,Part,SafetySetting,ThinkingConfig,Tool,ToolCodeExecution,UrlContext,Retrieval,VertexRagStore,VertexRagStoreRagResource
from fastmcp.client import Client
from fastmcp.client.transports import StdioTransport
from jsonpath_ng.ext import parse as jsonpath_parse
from._crypto import EncryptionManager
try:import sendgrid;from sendgrid.helpers.mail import From,Mail,Personalization,To,Cc,Bcc,ReplyTo
except ImportError:sendgrid=_A;From=_A;Mail=_A;Personalization=_A;To=_A;Cc=_A;Bcc=_A;ReplyTo=_A;logging.info('sendgrid library not found. Email sending will not be available.')
try:from twilio.rest import Client as TwilioClient
except ImportError:TwilioClient=_A;logging.info('twilio library not found. SMS sending will not be available.')
try:from google.cloud import storage
except ImportError:storage=_A;logging.info('google-cloud-storage library not found. GCS file operations will not be available.')
try:import boto3;from botocore.exceptions import ClientError
except ImportError:boto3=_A;ClientError=_A;logging.info('boto3 library not found. AWS S3 file operations will not be available.')
try:from openai import AsyncOpenAI
except ImportError:AsyncOpenAI=_A;logging.info('openai library not found. OpenAI models will not be available.')
try:from anthropic import AsyncAnthropic
except ImportError:AsyncAnthropic=_A;logging.info('anthropic library not found. Anthropic models will not be available.')
try:from py_mini_racer import MiniRacer
except ImportError:MiniRacer=_A;logging.info('mini-racer not found. JavaScript script execution will not be available.')
try:from pinionai_extensions import*
except ImportError:pass
from.chatservice_pb2 import ChatClient,ChatMessageRequest
from.chatservice_pb2_grpc import ChatServiceStub
from.exceptions import PinionAIAPIError,PinionAIConfigurationError,PinionAIGrpcError,PinionAISessionError
T=TypeVar('T',bound='AsyncPinionAIClient')
logger=logging.getLogger(__name__)
def _json_datetime_serializer(obj):
	'JSON serializer for datetime objects.'
	if isinstance(obj,(datetime.datetime,datetime.date)):return obj.isoformat()
	raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
class AsyncPinionAIClient:
	'\n    An asynchronous client for interacting with the PinionAI platform.\n\n    This client leverages async/await to handle I/O-bound operations concurrently,\n    improving throughput and responsiveness for scalable AI agent development.\n    ';_create_key=object()
	def __init__(self,create_key,agent_id,host_url,client_id,client_secret=_A,version=_A,token=_A,session_id=_A,raw_session_data=_A,initial_engagement_data=_A,grpc_server_address=_A,gcp_project_id=_A,gcp_region=_A,gemini_api_key=_A,twilio_account_sid=_A,twilio_auth_token=_A,twilio_number=_A,email_api_key=_A,email_from_address=_A,openai_api_key=_A,anthropic_api_key=_A,deepseek_api_key=_A):
		'\n        Initializes the AsyncPinionAIClient.\n\n        NOTE: This __init__ is synchronous and should not be called directly.\n        You must use the async class method `AsyncPinionAIClient.create(...)`\n        to get a fully initialized instance.\n        '
		if create_key is not self._create_key:raise PinionAIConfigurationError('AsyncPinionAIClient must be created using the `create` classmethod.')
		self._agent_id=agent_id;self._host_url=host_url.rstrip('/');self._client_id=client_id;self._client_secret=client_secret;self._version=version;self._grpc_server_address=grpc_server_address or os.environ.get(_BB,'localhost:50051');self._encryption_manager=EncryptionManager(client_secret=agent_id);self._gcp_project_id=gcp_project_id or os.environ.get(_BC);self._gcp_region=gcp_region or os.environ.get(_BD);self._gemini_api_key=gemini_api_key or os.environ.get(_BE);self._twilio_account_sid=twilio_account_sid or os.environ.get(_AW);self._twilio_auth_token=twilio_auth_token or os.environ.get(_AX);self._twilio_number=twilio_number or os.environ.get(_AY);self._email_api_key=email_api_key or os.environ.get(_BF);self._email_from_address=email_from_address or os.environ.get(_BG);self._openai_api_key=openai_api_key or os.environ.get(_BH);self._anthropic_api_key=anthropic_api_key or os.environ.get(_BI);self._deepseek_api_key=deepseek_api_key or os.environ.get(_BJ);self._http_session=httpx.AsyncClient(base_url=self._host_url,timeout=12e1,follow_redirects=_D);self._token=token;self._session_id=session_id;self._raw_session_data=raw_session_data;self.var={};self.engagement=''
		if initial_engagement_data:self.var=initial_engagement_data;self.engagement='active'
		self._class_intent_data='';self._class_message='';self._sub_message='';self._fin_message='';self.transfer_requested='';self.transfer_accepted='';self._privacy_level='';self.current_pipeline='';self.unique_id='';self.phone_number='';self.stepup_authorized=_G;self.authorized=_G;self.next_intent='';self.last_session_post_modified=_A;self._grpc_listener_task=_A;self._grpc_channel=_A;self._grpc_stub=_A;self._grpc_last_update_time=time.time();self.chat_messages=[];self.grpc_sender_id=_b;self._genai_client=_A;self._journey_bearer_token=_A;self._account_id=_A;self._customer_id=_A;self._agent_id_from_api=_A;self._agent_description=_A
	@classmethod
	async def create(cls,*args,**kwargs):
		'\n        Factory method to create and asynchronously initialize the client.\n        This is the preferred way to instantiate the client.\n        ';client=cls(cls._create_key,*args,**kwargs)
		if not client.engagement:
			try:await client._initialize_session_and_vars()
			except(PinionAIAPIError,PinionAISessionError)as e:logger.error(f"Fatal error during client initialization: {e}");await client.close();raise PinionAIConfigurationError(f"Client initialization failed: {e}")from e
		return client
	@classmethod
	async def create_from_stream(cls,file_stream,host_url,key_secret=_A):
		"\n        Creates and initializes a client session by parsing and decrypting\n        credentials from a single-line stream with a specific 'aia_' header format.\n        This method avoids re-initialization by using the session and token\n        provided directly from the credential decryption API call.\n        ";C='API response missing required data (token, key, or session data).';B='Unknown API error during key retrieval.';A='key_secret';logger.info('Reading and parsing credentials from a single-line stream.')
		if isinstance(file_stream,str):file_stream=StringIO(file_stream)
		credential_line=file_stream.readline().strip()
		if not credential_line:raise ValueError('Credential stream is empty or contains no data.')
		try:
			parts=credential_line.split('_',4)
			if len(parts)<4 or parts[0]!='aia':raise ValueError('Invalid credential format.')
			version_name,key_id,date_time=parts[1],parts[2],parts[3];encrypted_payload=parts[4].strip()if len(parts)==5 and parts[4].strip()else'';has_payload=bool(encrypted_payload);logger.info(f"Parsed credentials: version={version_name}, key_id={key_id},  date_time={date_time}, has_payload={has_payload}")
		except(ValueError,IndexError)as e:raise ValueError("Credential stream is malformed. Expected format: 'aia_{version_name}_{key_id}_{datetimeiso}_{encrypted_payload}'")from e
		logger.info('Retrieving decryption key and session for credentials.')
		async with httpx.AsyncClient(base_url=host_url.rstrip('/'),timeout=12e1)as http_session:
			try:
				api_payload={'key_id':key_id,'version_name':version_name,'date_time':date_time,'payload':has_payload}
				if key_secret:api_payload[A]=key_secret
				compressed_data=gzip.compress(json.dumps(api_payload,default=_json_datetime_serializer).encode(_N));response=await http_session.post('/filesession',headers={_Q:_K,_BK:_t},content=compressed_data);response.raise_for_status();resp_json=response.json()
			except httpx.HTTPStatusError as e:resp_json=json.loads(e.response.text);error_msg=resp_json.get(_V,B);return'',error_msg
			except(httpx.RequestError,json.JSONDecodeError)as e:logger.error(f"API call failed for /filesession: {e}");raise PinionAIAPIError(f"API call failed for /filesession: {e}")from e
		if not resp_json.get('success'):error_msg=resp_json.get(_V,B);raise PinionAIAPIError(error_msg);return'',error_msg
		decryption_key=resp_json.get(A);access_token=resp_json.get(_AZ);version=resp_json.get('version_type')
		if not all([access_token,decryption_key]):raise PinionAIAPIError(C);return'',C
		if encrypted_payload:encryption_client=EncryptionManager(client_secret=decryption_key);decrypted_value=encryption_client.decrypt(encrypted_payload);decrypted_file_json=json.loads(decrypted_value);resp_json[_B][_E][_B]=decrypted_file_json
		agent_id=resp_json.get(_B,{}).get(_E,{}).get('agentId');session_id=resp_json.get(_B,{}).get(_E,{}).get('uid');client_id=resp_json.get(_B,{}).get(_E,{}).get(_BL)
		if not agent_id:raise ValueError('Could not determine agent_id from session data.')
		logger.info('Credentials processed. Instantiating client with retrieved session.');client=cls(cls._create_key,agent_id=agent_id,host_url=host_url,client_id=client_id,version=version,token=f"bearer {access_token}",session_id=session_id,raw_session_data=resp_json)
		try:client._configure_client_from_session_data()
		except(PinionAIAPIError,PinionAISessionError)as e:logger.error(f"Fatal error during client configuration from stream: {e}");await client.close();raise PinionAIConfigurationError(f"Client configuration failed: {e}")from e
		return client,''
	def _configure_client_from_session_data(self):
		'Populates client variables and configurations from existing raw session data.';B='transferTypes';A='accentColor'
		if not self._raw_session_data:raise PinionAISessionError('Cannot configure client without raw session data.')
		if _B in self._raw_session_data and self._raw_session_data[_B]:
			self.var=self._extract_data_from_session(self._raw_session_data[_B]);agent_data=self._raw_session_data[_B][_E][_B][_J];self.var['sessionId']=self._session_id;self.var['agentTitle']=agent_data.get('title');self.var['agentSubtitle']=agent_data.get('subtitle');self.var[A]=agent_data.get(A);self.var['userImage']=agent_data.get('userImagePath','').strip();self.var['assistImage']=agent_data.get('assistantImagePath','').strip();self.var[_Aa]=agent_data.get(_Aa);self.var[_Ab]=agent_data.get(_Ab);self.var[B]=agent_data.get(B);self.var['sessionDateTime']=datetime.datetime.now(zoneinfo.ZoneInfo('UTC')).astimezone().isoformat();self.var[_c]='';startStatement=self._clean_text(agent_data.get('startStatement'));self.var['agentStart']=self._evaluate_f_string(startStatement or'',self.var);self.var[_l]=agent_data.get(_l);stores_data=agent_data.get('stores',[]);self._rag_stores_by_name={}
			if stores_data and isinstance(stores_data,list)and len(stores_data)>0:
				for s in stores_data:
					try:
						name=s.get(_C)
						if not name:continue
						self._rag_stores_by_name[name]={_u:s.get(_u,''),_v:s.get(_v,10),_w:s.get(_w,.5)}
					except Exception:continue
			if self._rag_stores_by_name:first_store_cfg=next(iter(self._rag_stores_by_name.values()));self.var[_Ac]=first_store_cfg.get(_u,'');self.var[_Ad]=first_store_cfg.get(_v,10);self.var[_Ae]=first_store_cfg.get(_w,.5)
			else:self.var[_Ac]='';self.var[_Ad]=10;self.var[_Ae]=.5
			self._account_id=self._raw_session_data[_B][_E].get(_BL);self._customer_id=self._raw_session_data[_B][_E].get('customerId');self._agent_id_from_api=agent_data.get('agentId');self._agent_description=self._clean_text(agent_data.get(_L,''))
		else:logger.error('Session data is missing expected structure.');raise PinionAISessionError('Session data from API is missing expected structure.')
		self._genai_client=self._initialize_genai_client()
	async def _initialize_session_and_vars(self):
		'Initializes session, fetches token, and sets up initial variables.'
		if not self._token:self._token=await self._get_token_api(self._host_url,self._client_id,self._client_secret)
		if not self._session_id or not self._raw_session_data:
			if self._version:logger.info(f"Starting session with version: {self._version}");self._session_id,self._raw_session_data=await self._start_version_api(self._host_url,self._agent_id,self._token,self._version)
			else:logger.info('Starting session without version.');self._session_id,self._raw_session_data=await self._start_session_api(self._host_url,self._agent_id,self._token)
		if not self._session_id or not self._raw_session_data:raise PinionAISessionError('Failed to start session (no session_id or data returned).')
		self._configure_client_from_session_data()
	async def close(self):'Closes the underlying httpx client session.';await self._http_session.aclose()
	async def __aenter__(self):"Enables use of the client in an 'async with' statement.";return self
	async def __aexit__(self,exc_type,exc_val,exc_tb):"Ensures resources are cleaned up when exiting an 'async with' block.";logger.info('AsyncPinionAIClient exiting context, cleaning up resources...');await self.end_grpc_chat_session(send_goodbye=_G);await self.close()
	def _initialize_genai_client(self):
		'\n        Initializes the Gemini client (genai.Client) for Vertex AI or the Gemini API.\n        If a connector_name for a service account is provided, it will be used for\n        Vertex AI authentication. Otherwise, it falls back to Application Default\n        Credentials (ADC) or an API key.\n\n        Args:\n            connector_name: The name of the connector to use for authentication.\n\n        Returns:\n            An initialized genai.Client instance or None if configuration is missing.\n        ';creds=_A;GCP_SCOPES=['https://www.googleapis.com/auth/cloud-platform']
		if self.var[_l]:
			conn_config=self._get_connector_details(self.var[_l])
			if conn_config and conn_config.get(_m)==_Af:
				try:sa_info=json.loads(conn_config.get(_n,'{}'));creds=service_account.Credentials.from_service_account_info(sa_info,scopes=GCP_SCOPES);logger.info(f"Loaded service account from connector '{self.var[_l]}' for Gemini client.")
				except(json.JSONDecodeError,KeyError)as e:logger.error(f"Failed to load service account from connector '{self.var[_l]}': {e}")
		if self._gcp_project_id and self._gcp_region:
			if creds:logger.info(f"Initializing Gemini client for Vertex AI with specific credentials.")
			else:logger.info(f"Initializing Gemini client for Vertex AI using Application Default Credentials.")
			return genai.Client(project=self._gcp_project_id,location=self._gcp_region,vertexai=_D,credentials=creds)
		elif self._gemini_api_key:
			if creds:logger.warning('Connector credentials provided but initializing with an API key; credentials will be ignored.')
			logger.info('Initializing Gemini client with direct API key.');return genai.Client(api_key=self._gemini_api_key)
		else:logger.warning('Gemini client not initialized: Missing GCP_PROJECT/GCP_REGION or GEMINI_API_KEY.');return
	async def get_pinionai_version_info(self):
		'\n        Fetches PinionAI agent version information.\n        ';logger.info('Get Pinionai version info');token=await self._get_token_api(self._host_url,self._client_id,self._client_secret)
		if token:
			session_id,data=await self._start_session_api(self._host_url,self._agent_id,token)
			if not session_id:logger.error('Currently unavailable (session could not be started).');return{}
			data_only=data.get(_B,{}).get(_E,{}).get(_B,{});logger.info(f"Version data loaded.");return data_only
		else:logger.error('Currently unavailable (token could not be obtained).')
		return{}
	def _normalize_intent_vars(self,intent_vars):
		if not intent_vars:return[]
		is_new_format=all(key.isdigit()for key in intent_vars.keys())
		if is_new_format:
			normalized_list=[];sorted_keys=sorted(intent_vars.keys(),key=int)
			for key in sorted_keys:
				if intent_vars[key]and isinstance(intent_vars[key],dict):normalized_list.append(list(intent_vars[key].items())[0])
			return normalized_list
		else:return list(intent_vars.items())
	async def process_user_input(self,user_input='',sender=_b):
		'\n        Processes user input, interacts with AI, and determines the next response.\n        ';L='Transfer requested, but gRPC client is not connected.';K='authentication_step_up_pipeline';J='privacyAction';I='highly';H='finalprocess';G='subprocess';F='preprocess';E='contextFlow';D='final prompt';C='subprompt';B='inputVars';A='intent_resp';preprocess_response='';subprocess_response='';final_response='';self.grpc_sender_id=sender
		if not self.transfer_requested:
			prompt_resp_var_name=_A
			if self.next_intent:self.var['prompt_resp_var']=self.next_intent;prompt_type=self.var[_Ag]=_AA;user_input=self.next_intent;intent_data=self._get_intent_details(self.next_intent);self.next_intent=''
			else:
				self.var,prompt_resp_var_name=await self._classify_input(user_input)
				if not prompt_resp_var_name:return"I'm sorry, I couldn't understand that. Could you please start over or rephrase?"
				prompt_type=self.var.get(_Ag);intent_data=self._get_intent_details(self.var[prompt_resp_var_name])
			self.var[_c]=''
			if not intent_data:logger.error(f"Intent details not found for: {self.var[prompt_resp_var_name]}");return"I'm sorry, there was an issue processing your request (intent details missing)."
			intent_type=intent_data[_F];self.var[A]=intent_data[_C];self._privacy_level=self.var['privacy_resp']=intent_data[_Ah];self.current_pipeline=self.var['pipeline_resp']=intent_data[_x];delivery_method=intent_data[_Ai];language=intent_data[_d];intent_input_vars=self._normalize_intent_vars(intent_data.get(B,{}));context_flow=intent_data.get(E,{});intent_subprompt=context_flow.get(C,{});intent_finalprompt=context_flow.get(D,{});intent_preprocess=context_flow.get(F,{});intent_subprocess=context_flow.get(G,{});intent_finalprocess=context_flow.get(H,{});intent_actionprocess=intent_data.get(_Aj,{})
			if self.var.get(_H):logger.debug(f"Classification | {self.var[A]}");logger.debug(f"Sensitivity | {self._privacy_level}");logger.debug(f"Intent Type | {intent_type}")
			if intent_type!=_y:
				if intent_input_vars:
					agent_vars_config=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get(_BM,[])
					for(key,_)in intent_input_vars:
						for var_def in agent_vars_config:
							if var_def.get(_C)==key and var_def.get('reset',_G)is _D:self.var[key]='';break
					if self.var[_z]:self.var['required_input_list']=[item[0]for item in intent_input_vars];self.var=await self._input_variable_filler(user_input)
				if prompt_type==_AA:self._class_message=user_input;self._class_intent_data=intent_data
				elif prompt_type==C:self._sub_message=user_input
				elif prompt_type==D:self._fin_message=user_input
			elif intent_type==_y:
				action_key_for_input=intent_data.get(_x,'')
				if any(keyword in intent_data[_C]for keyword in['phone','mobile','cell']):_,self.unique_id,self.phone_number=format_phone(user_input);self.var[action_key_for_input]=self.phone_number
				else:self.var[action_key_for_input]=user_input
				if self._class_intent_data:intent_data=self._class_intent_data;user_input=self._class_message;intent_type=intent_data[_F];self.var[A]=intent_data[_C];delivery_method=intent_data[_Ai];language=intent_data[_d];intent_input_vars=self._normalize_intent_vars(intent_data.get(B,{}));context_flow=intent_data.get(E,{});intent_subprompt=context_flow.get(C,{});intent_finalprompt=context_flow.get(D,{});intent_preprocess=context_flow.get(F,{});intent_subprocess=context_flow.get(G,{});intent_finalprocess=context_flow.get(H,{});intent_actionprocess=intent_data.get(_Aj,{});self._privacy_level=intent_data[_Ah];self.current_pipeline=intent_data[_x]
			if intent_input_vars:
				intent_input_vars=self._normalize_intent_vars(intent_data.get(B,{}));self.var,collect_prompt,waiting_for_inputs=await self._collect_required_inputs(self.var,intent_input_vars)
				if waiting_for_inputs:
					final_response=collect_prompt
					if final_response:self.chat_messages.append({_S:_Ak,_R:final_response})
					return final_response
			if not final_response:
				if intent_preprocess:self.var,preprocess_response=await self._process_routing(self.var,intent_preprocess,user_input=user_input)
				if preprocess_response:final_response=preprocess_response
				if not final_response:
					if not self.authorized and'private'in self._privacy_level or I in self._privacy_level:
						_,self.unique_id,self.phone_number=format_phone(self.var.get('phone_number',self.phone_number))
						if intent_data[J]:
							current_var,step_response=await self._run_action_action(self.var,intent_data[J],'',user_input=user_input)
							if step_response and not self.authorized:final_response=step_response
						else:
							customer_id,enrolled,_=await self._journey_lookup(self.unique_id,self.var);auth_response_msg=''
							if customer_id and enrolled:
								pipeline_key=self.var[K]if I in self._privacy_level else self.var['authentication_pipeline'];json_payload={_Al:pipeline_key,_o:{_f:delivery_method,_g:self.phone_number},_Am:{_An:self.unique_id,_g:self.phone_number},_E:{_Ao:self._session_id},_d:language}
								if self.var.get(_p):json_payload[_Ap]=self.var[_p]
								execution_id,execution_url,error_msg=await self._journey_send_pipeline(self.var,json_payload,delivery_method)
								if error_msg:auth_response_msg=error_msg
								else:
									logger.info(f"Sent authentication for {self.unique_id} to complete.");is_authenticated,message=await self._journey_execution_status_check(execution_id,self.var,120);auth_response_msg=message;self.authorized=is_authenticated
									if pipeline_key==self.var[K]and self.authorized:self.stepup_authorized=_D
									if is_authenticated:logger.info('Authorization successful.')
							else:
								auth_response_msg=f"You are not enrolled. We are sending a link to {self.phone_number} so that you can enroll your device.";json_payload={_Al:self.var['enroll_pipeline'],_o:{_f:delivery_method,_g:self.phone_number},_Am:{_An:self.unique_id,_g:self.phone_number},_E:{_Ao:self._session_id},_d:language}
								if self.var.get(_p):json_payload[_Ap]=self.var[_p]
								_,execution_url,error_msg=await self._journey_send_pipeline(self.var,json_payload,delivery_method)
								if error_msg:auth_response_msg=error_msg
							if auth_response_msg and not self.authorized:final_response=auth_response_msg
			if not final_response:
				if intent_type=='fixed':fixed_message_template=self._clean_text(intent_data['fixedResponseMessage']);final_response=self._evaluate_f_string(fixed_message_template,self.var)
				elif intent_type==_AB:
					action_details_from_intent=self._map_to_standard_action_details(intent_data);action_type=action_details_from_intent.get(_Aq)
					if action_type=='journey':self.var,final_response=await self._run_journey_action(self.var,action_details_from_intent)
					elif action_type=='transfer':self.var,final_response=self._run_transfer_action(self.var,action_details_from_intent)
					else:
						action_flow=action_details_from_intent.get(_Ar)
						if action_flow:
							self.var,action_response=await self._process_routing(self.var,action_flow,user_input=user_input)
							if action_details_from_intent.get(_h):response_msg_template=self._clean_text(action_details_from_intent[_h]);final_response=self._evaluate_f_string(response_msg_template,self.var)
							elif action_response:final_response=action_response
							else:final_response='Actions triggered. :wrench:'
						else:final_response='No working actions configured. :wrench:'
			if not final_response:
				if intent_subprompt:self.var,self._sub_message=await self._run_prompt_action(user_input,intent_subprompt)
				if intent_subprocess:self.var,subprocess_response=await self._process_routing(self.var,intent_subprocess,user_input=user_input)
				if subprocess_response:final_response=subprocess_response
				if not final_response:
					if intent_finalprompt:
						for(_indx,item_config)in sorted(intent_finalprompt.items()):
							if isinstance(item_config,dict):
								if _AC in item_config:
									target_prompt=item_config[_AC];self.var,resp_var_name=await self._prompt_response(target_prompt,user_input)
									if resp_var_name and self.var.get(resp_var_name):final_response=self.var[resp_var_name]
								elif _q in item_config:
									mcp_name=item_config[_q];self.var,mcp_response=await self._run_mcp_action(self.var,mcp_name,user_input)
									if mcp_response:final_response=mcp_response
							elif isinstance(item_config,str):
								self.var,resp_var_name=await self._prompt_response(item_config,user_input)
								if resp_var_name and self.var.get(resp_var_name):final_response=self.var[resp_var_name]
			if intent_finalprocess and self.var.get(_c,'')=='':
				self.var,final_process_response=await self._process_routing(self.var,intent_finalprocess,final_response,user_input=user_input)
				if final_process_response:final_response=final_process_response
		elif self._grpc_stub:await self.send_grpc_message(user_input);final_response='Message sent to live agent. Waiting for reply...'
		else:final_response=L;logger.warning(L)
		if final_response:self.chat_messages.append({_S:_Ak,_R:final_response})
		return final_response
	async def update_pinion_session(self):
		'\n        Posts the current session data to the PinionAI backend.\n        '
		if not self._session_id or not self._token or not self._raw_session_data:logger.error('Cannot update session: session not properly initialized.');return
		data_to_post=json.loads(json.dumps(self._raw_session_data.get(_B,{})))
		if _E not in data_to_post:data_to_post[_E]={}
		data_to_post[_E][_A0]=self.var;messages_for_api=[{k:v for(k,v)in msg.items()if k!='avatar'}for msg in self.chat_messages];data_to_post[_E][_A1]=messages_for_api;response_obj,response_data=await self._post_session_api(self._host_url,self._token,self._session_id,data_to_post,self.transfer_requested,self.transfer_accepted)
		if response_obj and response_obj.status_code==200:
			try:last_modified_time=response_data[_B]['Lastmodified']['Time'];self.last_session_post_modified=last_modified_time;return last_modified_time
			except(KeyError,TypeError)as e:logger.error(f"Error parsing Lastmodified from session post response: {e} - Data: {response_data}");return
		elif response_obj:logger.error(f"Error posting session data: Status Code {response_obj.status_code}, Message: {response_data}");return
		else:logger.error(f"Network error posting session data: {response_data}");return
	async def get_latest_session_modification_time(self):
		'\n        Fetches the last modified timestamp for the current session.\n        '
		if not self._session_id or not self._token:return _A,'Session or token not initialized.'
		return await self._get_session_lastmodified_api(self._host_url,self._session_id,self._token)
	async def start_grpc_client_listener(self,sender_id=_b):
		'\n        Establishes a secure async gRPC connection to the Cloud Run service and starts the listener task.\n        '
		if not self._grpc_server_address:logger.error('gRPC server address not configured.');return _G
		if not self._session_id:logger.error('Session ID not available for gRPC client.');return _G
		self.grpc_sender_id=sender_id
		try:credentials=grpc.ssl_channel_credentials();self._grpc_channel=agrpc.secure_channel(self._grpc_server_address,credentials);self._grpc_stub=ChatServiceStub(self._grpc_channel);logger.info(f"gRPC client connected to {self._grpc_server_address} for session {self._session_id} as {sender_id}");self._grpc_listener_task=asyncio.create_task(self._grpc_read_handler(self.grpc_sender_id,self._session_id,self._grpc_stub));return _D
		except grpc.aio.AioRpcError as e:logger.error(f"gRPC connection failed: {e.code()} - {e.details()}",exc_info=_D);raise PinionAIGrpcError(f"Failed to connect to gRPC server: {e.details()}")from e
		except Exception as e:logger.error(f"An unexpected error occurred while starting gRPC client: {e}",exc_info=_D);raise PinionAIGrpcError(f"Failed to start gRPC client listener: {e}")from e
	async def _grpc_read_handler(self,client_id,session_id,stub):
		'Handles receiving messages from the server in an asyncio task.';logger.info(f"gRPC read_handler task started for client: {client_id}, session: {session_id}");request=ChatClient(recipient_id=client_id,session_id=str(session_id))
		try:
			read_stream=stub.ReceiveMessages(request)
			async for response in read_stream:logger.info(f"gRPC message received: {response.sender_id} ({response.timestamp}): {response.message}");self.chat_messages.append({_S:response.sender_id,_R:response.message});self._grpc_last_update_time=time.time()
		except agrpc.AioRpcError as e:
			if e.code()==grpc.StatusCode.CANCELLED:logger.info(f"gRPC read_handler stream cancelled: {e.details()}")
			else:logger.error(f"gRPC AioRpcError in read_handler: {e.code()} - {e.details()}")
		except Exception as e:logger.error(f"Unexpected error in gRPC read_handler: {e}",exc_info=_D)
		finally:logger.info(f"gRPC read_handler task for client {client_id} terminated.")
	async def send_grpc_message(self,message_text):
		'Sends a message via async gRPC.'
		if not self._grpc_stub or not self._session_id:logger.error('gRPC stub or session ID not available. Cannot send message.');return
		try:recipient_id=_Ak if self.grpc_sender_id==_b else _b;request=ChatMessageRequest(thread_id=1,message=message_text,sender_id=self.grpc_sender_id,recipient_id=recipient_id,session_id=str(self._session_id));await self._grpc_stub.SendMessage(request);logger.info(f"gRPC message sent by {self.grpc_sender_id}: {message_text}")
		except agrpc.AioRpcError as e:raise PinionAIGrpcError(f"Failed to send gRPC message: {e.details()}",grpc_code=e.code())from e
	async def end_grpc_chat_session(self,send_goodbye=_D):
		'Handles the end of a gRPC chat session logic.';logger.info('Ending gRPC chat session.')
		if self._grpc_listener_task and not self._grpc_listener_task.done():self._grpc_listener_task.cancel()
		if self._grpc_stub and self._session_id and send_goodbye:
			try:logger.info("Sending gRPC end message 'X'.");await self.send_grpc_message('X')
			except Exception as e:logger.error(f"Error sending 'X' message during gRPC end: {e}")
		if self._grpc_channel:await self._grpc_channel.close();logger.info('gRPC channel closed.')
		self._grpc_channel=_A;self._grpc_stub=_A;self._grpc_listener_task=_A;logger.info('gRPC chat session ended and resources cleaned up.')
	async def _process_routing(self,current_var,process_items,initial_final_response=_A,user_input=_A):
		'Handles routing activities from intent and action flows.';H='intent';G='element';F='file';E='rule';D='script';C='merger';B='parser';A='api'
		if current_var.get(_H):logger.debug(f"Process Routing | {process_items}")
		generated_final_response=initial_final_response
		for(_key,item_config)in sorted(process_items.items()):
			step_response=_A
			if A in item_config:current_var,step_response=await self._run_api_action(current_var,item_config[A])
			elif _AB in item_config:current_var,step_response=await self._run_action_action(current_var,item_config[_AB],generated_final_response,user_input=user_input)
			elif _q in item_config:current_var,step_response=await self._run_mcp_action(current_var,item_config[_q],user_input)
			elif B in item_config:current_var,step_response=self._run_parser_action(current_var,item_config[B])
			elif C in item_config:current_var,step_response=self._run_merger_action(current_var,item_config[C])
			elif D in item_config:current_var,step_response=await self._run_script_action(current_var,item_config[D])
			elif E in item_config:current_var,step_response=await self._run_rule_action(current_var,item_config[E],user_input=user_input)
			elif _o in item_config:current_var,step_response=await self._run_delivery_action(current_var,item_config[_o])
			elif F in item_config:current_var,step_response=await self._run_file_action(current_var,item_config[F])
			elif _y in item_config:current_var,step_response=await self._run_input_action(current_var,item_config[_y])
			elif G in item_config:current_var,step_response=await self._run_element_action(current_var,item_config[G])
			elif H in item_config:self.next_intent=item_config[H];logger.info(f"Next intent set to: {self.next_intent}")
			if step_response:generated_final_response=step_response
		return current_var,generated_final_response
	async def _run_async_prompts_for_list(self,prompt_list,user_input_val,shared_var_copy):
		tasks=[self._async_prompt_response(p_text,user_input_val,shared_var_copy)for p_text in prompt_list];gathered_results=await asyncio.gather(*tasks);current_batch_response_strings=[];updates_to_apply_to_shared_var={}
		for(resp_key_name,value_for_key)in gathered_results:
			if resp_key_name:updates_to_apply_to_shared_var[resp_key_name]=value_for_key
			if isinstance(value_for_key,str):current_batch_response_strings.append(value_for_key)
			elif value_for_key is not _A:current_batch_response_strings.append(str(value_for_key))
		return current_batch_response_strings,updates_to_apply_to_shared_var
	def _extract_data_from_session(self,session_data_root):
		'Extracts variables and agent configuration into the var dictionary.';var_dict={};agent_config=session_data_root.get(_E,{}).get(_B,{}).get(_J,{});global_to_self_attr_map={_BB:'_grpc_server_address',_BC:'_gcp_project_id',_BD:'_gcp_region',_BE:'_gemini_api_key',_AW:'_twilio_account_sid',_AX:'_twilio_auth_token',_AY:'_twilio_number',_BF:'_email_api_key',_BG:'_email_from_address',_BH:'_openai_api_key',_BI:'_anthropic_api_key',_BJ:'_deepseek_api_key'}
		for variable_def in agent_config.get(_BM,[]):
			name=variable_def[_C];value=variable_def[_As];var_type=variable_def.get(_F)
			if variable_def.get(_AD)=='global':
				os.environ[name]=str(value)
				if name in global_to_self_attr_map:attr_name=global_to_self_attr_map[name];setattr(self,attr_name,str(value));logger.info(f"Updated client attribute '{attr_name}' from global agent variable '{name}'.")
			elif var_type=='integer':
				try:var_dict[name]=int(value)
				except(ValueError,TypeError):var_dict[name]=value
			elif var_type=='boolean':var_dict[name]=str(value).lower()=='true'
			elif var_type=='float':
				try:var_dict[name]=float(value)
				except(ValueError,TypeError):var_dict[name]=value
			else:var_dict[name]=value
		intent_names,no_input_intent_names,input_intent_names=[],[],[];intent_privacy_pairs,intent_type_pairs=[],[];intent_contains_word_pairs,intent_action_key_pairs_raw=[],[]
		for intent in agent_config.get('intents',[]):
			intent_name=intent[_C];intent_names.append(intent_name)
			if intent[_F]=='information'or intent[_F]==_AB:no_input_intent_names.append(intent_name)
			if intent[_F]==_y:input_intent_names.append(intent_name)
			intent_privacy_pairs.append((intent_name,intent[_Ah]));intent_type_pairs.append((intent_name,intent[_F]));intent_contains_word_pairs.append((intent_name,intent.get('containsWord','')));intent_action_key_pairs_raw.append((intent_name,intent.get(_x,'')))
		var_dict[_At]=intent_names;var_dict['noInputIntentNameList']=no_input_intent_names;var_dict['inputIntentNameList']=input_intent_names;var_dict['intentPrivacyPairsList']=intent_privacy_pairs;var_dict['intentTypePairsList']=intent_type_pairs;var_dict[_Au]=intent_contains_word_pairs;resolved_action_key_pairs=[]
		for(intent,action_key_val_or_var)in intent_action_key_pairs_raw:
			if action_key_val_or_var in var_dict:resolved_action_key_pairs.append((intent,var_dict[action_key_val_or_var]))
			else:resolved_action_key_pairs.append((intent,action_key_val_or_var))
		var_dict['intentActionPairsList']=resolved_action_key_pairs;var_dict[_AE]=agent_config.get(_AE);var_dict[_Av]=agent_config.get('defaultIntent');var_dict[_z]=agent_config.get(_z);return var_dict
	async def _classify_input(self,user_input):
		if not self.var.get(_AE):logger.error('startPrompt not defined in agent configuration.');return self.var,_A
		_current_var_state,resp_var_name=await self._prompt_response(self.var[_AE],user_input)
		if not resp_var_name:logger.error('No response variable name set for classification prompt.');return self.var,_A
		return self.var,resp_var_name
	async def _input_variable_filler(self,user_input):
		B='filled_slots';A='```json'
		if not self.var.get(_z):logger.error('inputFillerPrompt not defined in agent configuration.');return self.var
		self.var,resp_var_name=await self._prompt_response(self.var[_z],user_input=user_input)
		if not resp_var_name or not self.var.get(resp_var_name):logger.error('No response or response variable name set for input filler prompt.');return self.var
		try:
			response_json_str=self.var[resp_var_name]
			if A in response_json_str:response_json_str=response_json_str.split(A)[1].split('```')[0]
			response_data=json.loads(response_json_str)
			if B in response_data:
				for(key,value)in response_data[B].items():self.var[key]=value;logger.info(f"Slot filled from user input: {key} = {value}")
		except(json.JSONDecodeError,KeyError)as e:logger.error(f"Failed to parse or process slot filling JSON response: {e}");logger.debug(f"Invalid JSON string: {self.var.get(resp_var_name)}")
		return self.var
	async def _collect_required_inputs(self,current_var,required_vars):
		'\n        required_vars: list of (variable_name, prompt_message).\n        Returns: (updated_current_var, prompt_message_or_None, waiting_bool)\n        If waiting_bool is True the caller should present the prompt_message to the user and pause further processing.\n        '
		if not required_vars:current_var[_c]='';return current_var,_A,_G
		for(key_req,prompt_msg)in required_vars:
			val=current_var.get(key_req)
			if val is _A or isinstance(val,str)and not val.strip()or isinstance(val,(list,dict))and not val:current_var[_c]=f"Strongly consider the expected input field should be {key_req}";final_prompt=prompt_msg or f"Please provide a value for {key_req}.";return current_var,final_prompt,_D
		current_var[_c]='';return current_var,_A,_G
	async def _prompt_response(self,target_prompt,user_input=''):
		prompt_config,direct_tool_configs,processed_fd_dicts=self._get_prompt_details(target_prompt)
		if not prompt_config:logger.error(f"Prompt '{target_prompt}' not found. Check configuration.");return self.var,_A
		self.var[_Ag]=prompt_config[_F];prompt_resp_var_name=prompt_config[_AF];prompt_body_template=self._clean_text(prompt_config[_W]);current_prompt_text=self._evaluate_f_string(prompt_body_template,self.var,user_input=user_input);model_provider=prompt_config.get(_Aw,_e).lower();model_name=prompt_config.get(_X);llm_response_text=_A;function_calls=_A;system_instruction=self._evaluate_f_string(self._agent_description or'',self.var)
		if model_provider==_e:
			content_parts=[]
			if prompt_config.get(_AG):
				file_uri_template=self._clean_text(prompt_config[_AG]);file_uri=self._evaluate_f_string(file_uri_template,self.var)
				if file_uri:content_parts.append(Part.from_uri(file_uri=file_uri,mime_type=prompt_config[_BN]))
			content_parts.append(current_prompt_text);gen_config=google_genai_types.GenerateContentConfig(system_instruction=system_instruction if system_instruction else _A,temperature=prompt_config[_AH],top_p=prompt_config[_Y],top_k=prompt_config[_AI],candidate_count=prompt_config[_AJ],max_output_tokens=prompt_config[_AK],stop_sequences=prompt_config.get('stop')or _A,safety_settings=prompt_config.get(_BO))
			if model_name in[_BP]and prompt_config.get(_i)is not _A:gen_config.thinking_config=google_genai_types.ThinkingConfig(thinking_level=prompt_config.get(_i))
			if prompt_config.get(_AL):gen_config.response_schema=prompt_config[_AL];gen_config.response_mime_type=prompt_config.get(_BQ,_K)
			gen_config.tools=self._configure_tools_for_request(direct_tool_configs,processed_fd_dicts,model_name);llm_response_text,_,function_calls=await self._get_gemini_response_async(model_name,content_parts,gen_config)
		elif model_provider in[_j,_A2,_AM]:
			messages=[]
			if system_instruction and model_provider in[_j,_AM]:messages.append({_S:_A3,_R:system_instruction})
			messages.append({_S:_b,_R:current_prompt_text});tools_for_provider=self._translate_tools_for_provider(model_provider,direct_tool_configs,processed_fd_dicts)
			if model_provider==_j:llm_response_text,function_calls=await self._get_openai_response_async(model_name,messages,prompt_config,tools_for_provider)
			elif model_provider==_A2:anthropic_messages=[m for m in messages if m[_S]!=_A3];llm_response_text,function_calls=await self._get_anthropic_response_async(model_name,system_instruction,anthropic_messages,prompt_config,tools_for_provider)
			elif model_provider==_AM:llm_response_text,function_calls=await self._get_deepseek_response_async(model_name,messages,prompt_config,tools_for_provider)
		else:logger.error(f"Unsupported model provider: {model_provider}");return self.var,f"Error: Unsupported model provider '{model_provider}'"
		if function_calls:
			function_call=function_calls[0];function_name=function_call.get(_C);function_args=function_call.get(_I,{})
			if not function_name:logger.error(f"LLM response contained a function call with no name: {function_call}");return self.var,_BR
			logger.info(f"LLM requested to call function '{function_name}' with args: {function_args}")
			if function_name in globals()and callable(globals()[function_name]):
				function_to_call=globals()[function_name]
				try:
					if asyncio.iscoroutinefunction(function_to_call):tool_response=await function_to_call(**function_args)
					else:tool_response=await asyncio.to_thread(function_to_call,**function_args)
					if isinstance(tool_response,(dict,list)):tool_response_str=json.dumps(tool_response,indent=2)
					else:tool_response_str=str(tool_response)
					if prompt_resp_var_name:self.var[prompt_resp_var_name]=tool_response_str
					return self.var,prompt_resp_var_name
				except Exception as e:
					logger.error(f"Error executing tool function '{function_name}': {e}",exc_info=_D);error_message=f"Error: Failed to execute tool '{function_name}': {e}"
					if prompt_resp_var_name:self.var[prompt_resp_var_name]=error_message
					return self.var,prompt_resp_var_name
			else:
				logger.error(f"Function '{function_name}' requested by LLM is not a defined callable function.");error_message=f"Error: The AI tried to call a function named '{function_name}' which is not available."
				if prompt_resp_var_name:self.var[prompt_resp_var_name]=error_message
				return self.var,prompt_resp_var_name
		if llm_response_text:
			if prompt_config[_F]==_AA:
				raw_response=llm_response_text.strip().lower()
				if self.var.get(_H):logger.debug(f"Raw Intent Response | {raw_response}")
				matched_intent_key=self._match_intent_from_text(raw_response,self.var.get(_Au,[]),self.var.get(_Av,_BS),self.var.get(_At,[]));self.var[prompt_resp_var_name]=matched_intent_key
			else:self.var[prompt_resp_var_name]=llm_response_text
		else:self.var[prompt_resp_var_name]=''
		return self.var,prompt_resp_var_name
	async def _async_prompt_response(self,target_prompt,user_input='',var_snapshot=_A):
		current_var=var_snapshot if var_snapshot is not _A else self.var.copy();prompt_config,direct_tool_configs,processed_fd_dicts=self._get_prompt_details(target_prompt,current_var)
		if not prompt_config:logger.error(f"Prompt '{target_prompt}' not found. Skipping async call.");return _A,_A
		prompt_resp_var_name=prompt_config[_AF];prompt_body_template=self._clean_text(prompt_config[_W]);current_prompt_text=self._evaluate_f_string(prompt_body_template,current_var,user_input=user_input);model_provider=prompt_config.get(_Aw,_e).lower();model_name=prompt_config.get(_X);llm_response_text=_A;function_calls=_A;system_instruction=self._evaluate_f_string(self._agent_description or'',current_var)
		if model_provider==_e:
			content_parts=[]
			if prompt_config.get(_AG):
				file_uri_template=self._clean_text(prompt_config[_AG]);file_uri=self._evaluate_f_string(file_uri_template,current_var)
				if file_uri:content_parts.append(Part.from_uri(file_uri=file_uri,mime_type=prompt_config[_BN]))
			content_parts.append(current_prompt_text);gen_config=google_genai_types.GenerateContentConfig(system_instruction=system_instruction if system_instruction else _A,temperature=prompt_config[_AH],top_p=prompt_config[_Y],top_k=prompt_config[_AI],candidate_count=prompt_config[_AJ],max_output_tokens=prompt_config[_AK],stop_sequences=prompt_config.get('stop')or _A,safety_settings=prompt_config.get(_BO))
			if model_name in[_BP]and prompt_config.get(_i)is not _A:gen_config.thinking_config=google_genai_types.ThinkingConfig(thinking_level=prompt_config.get(_i))
			if prompt_config.get(_AL):gen_config.response_schema=prompt_config[_AL];gen_config.response_mime_type=prompt_config.get(_BQ,_K)
			gen_config.tools=self._configure_tools_for_request(direct_tool_configs,processed_fd_dicts,model_name);llm_response_text,_,function_calls=await self._get_gemini_response_async(model_name,content_parts,gen_config)
		elif model_provider in[_j,_A2]:
			messages=[]
			if system_instruction and model_provider==_j:messages.append({_S:_A3,_R:system_instruction})
			messages.append({_S:_b,_R:current_prompt_text});tools_for_provider=self._translate_tools_for_provider(model_provider,direct_tool_configs,processed_fd_dicts)
			if model_provider==_j:llm_response_text,function_calls=await self._get_openai_response_async(model_name,messages,prompt_config,tools_for_provider)
			elif model_provider==_A2:anthropic_messages=[m for m in messages if m[_S]!=_A3];llm_response_text,function_calls=await self._get_anthropic_response_async(model_name,system_instruction,anthropic_messages,prompt_config,tools_for_provider)
		else:logger.error(f"Unsupported model provider: {model_provider}");return _A,f"Error: Unsupported model provider '{model_provider}'"
		if function_calls:
			function_call=function_calls[0];function_name=function_call.get(_C);function_args=function_call.get(_I,{})
			if not function_name:logger.error(f"LLM async response contained a function call with no name: {function_call}");return prompt_resp_var_name,_BR
			logger.info(f"LLM requested async call to function '{function_name}' with args: {function_args}")
			if function_name in globals()and callable(globals()[function_name]):
				function_to_call=globals()[function_name]
				try:
					if asyncio.iscoroutinefunction(function_to_call):tool_response=await function_to_call(**function_args)
					else:tool_response=await asyncio.to_thread(function_to_call,**function_args)
					if isinstance(tool_response,(dict,list)):tool_response_str=json.dumps(tool_response,indent=2)
					else:tool_response_str=str(tool_response)
					return prompt_resp_var_name,tool_response_str
				except Exception as e:logger.error(f"Error executing tool function '{function_name}' in async prompt: {e}",exc_info=_D);error_message=f"Error: Failed to execute tool '{function_name}': {e}";return prompt_resp_var_name,error_message
			else:logger.error(f"Function '{function_name}' requested by LLM is not a defined callable function.");error_message=f"Error: The AI tried to call a function named '{function_name}' which is not available.";return prompt_resp_var_name,error_message
		final_value_for_var=''
		if llm_response_text:
			if prompt_config[_F]==_AA:
				raw_response=llm_response_text.strip().lower()
				if current_var.get(_H):logger.debug(f"Async Raw Intent Response | {raw_response}")
				final_value_for_var=self._match_intent_from_text(raw_response,current_var.get(_Au,[]),current_var.get(_Av,_BS),current_var.get(_At,[]))
			else:final_value_for_var=llm_response_text
		return prompt_resp_var_name,final_value_for_var
	def _match_intent_from_text(self,response_text,intent_contains_pairs,default_intent,intent_name_list):
		'Helper to match intent from LLM response text.';threshold_ratio=.85
		if response_text in intent_name_list:return response_text
		matched_intent_key=default_intent;best_similarity_score=.0
		for(intent_key,search_phrases_str)in intent_contains_pairs:
			if not search_phrases_str:continue
			search_phrases=[phrase.strip()for phrase in str(search_phrases_str).split(_T)]
			for phrase in search_phrases:
				if phrase and phrase in response_text:return intent_key
		for(intent_key,search_phrases_str)in intent_contains_pairs:
			if not search_phrases_str:continue
			search_phrases=[phrase.strip()for phrase in str(search_phrases_str).split(_T)]
			for phrase in search_phrases:
				if not phrase:continue
				similarity=Levenshtein.ratio(response_text,phrase)
				if similarity>threshold_ratio and similarity>best_similarity_score:best_similarity_score=similarity;matched_intent_key=intent_key
		return matched_intent_key
	def _get_prompt_details(self,target_prompt_name,current_var_snapshot=_A):
		'Fetches prompt configuration, processing tools and functional declarations.';A='functionalDeclarations';var_to_use=current_var_snapshot if current_var_snapshot is not _A else self.var;direct_tool_configs=[];processed_fd_dicts=[];agent_prompts=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('prompts',[]);agent_tools_config=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get(_O,[])
		for prompt_config in agent_prompts:
			if target_prompt_name==prompt_config.get(_C):
				if prompt_config.get(_O):
					for tool_name_in_prompt_config in prompt_config[_O]:
						for actual_tool_def in agent_tools_config:
							if actual_tool_def.get(_C)==tool_name_in_prompt_config:
								if actual_tool_def.get(_O):direct_tool_configs.extend(actual_tool_def[_O])
								if actual_tool_def.get(A):
									declarations_data=actual_tool_def.get(A);declaration_templates=[]
									if isinstance(declarations_data,list):declaration_templates=declarations_data
									elif isinstance(declarations_data,dict):declaration_templates=[declarations_data]
									elif isinstance(declarations_data,str):
										try:
											cleaned_str=self._clean_text(declarations_data);parsed_json=json.loads(cleaned_str)
											if isinstance(parsed_json,list):declaration_templates=parsed_json
											elif isinstance(parsed_json,dict):declaration_templates=[parsed_json]
											else:logger.warning(f"Functional declaration string did not parse into a list or dictionary: {cleaned_str}")
										except json.JSONDecodeError:logger.warning(f"Could not parse functional declaration string as JSON: {declarations_data}")
									for template in declaration_templates:
										if isinstance(template,dict):processed_fd=self._evaluate_vars_in_structure(json.loads(json.dumps(template)),var_to_use,user_input=_A);processed_fd_dicts.append(processed_fd)
										else:logger.warning(f"Skipping item in functionalDeclarations because it is not a dictionary: {template}")
								break
				return prompt_config,direct_tool_configs,processed_fd_dicts
		return _A,[],[]
	def _get_intent_details(self,intent_name):
		'Fetches intent configuration.';intents=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('intents',[])
		for intent_config in intents:
			if intent_config.get(_C)==intent_name:return intent_config
	def _get_api_details(self,api_name):
		apis=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('apis',[])
		for api_config in apis:
			if api_config.get(_C)==api_name:return api_config
	def _get_parser_details(self,parser_name):
		parsers=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('parsers',[])
		for parser_config in parsers:
			if parser_config.get(_C)==parser_name:return parser_config
	def _get_merger_details(self,merger_name):
		mergers=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('mergers',[])
		for merger_config in mergers:
			if merger_config.get(_C)==merger_name:return merger_config
	def _get_script_details(self,script_name):
		scripts=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('scripts',[])
		for script_config in scripts:
			if script_config.get(_C)==script_name:return script_config
	def _get_rule_details(self,rule_name):
		rules=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('rules',[])
		for rule_config in rules:
			if rule_config.get(_C)==rule_name:return rule_config
	def _get_delivery_details(self,delivery_name):
		deliveries=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('deliveries',[])
		for delivery_config in deliveries:
			if delivery_config.get(_C)==delivery_name:return delivery_config
	def _get_action_details(self,action_name):
		actions=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('actions',[])
		for action_config in actions:
			if action_config.get(_C)==action_name:return action_config
	def _get_file_details(self,file_name):
		'Fetches file operation configuration.';files=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('files',[])
		for file_config in files:
			if file_config.get(_C)==file_name:return file_config
	def _get_connector_details(self,connector_name):
		connectors=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('connectors',[])
		for connector_config in connectors:
			if connector_config.get(_C)==connector_name:return connector_config
	def _get_element_details(self,element_name):
		elements=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('elements',[])
		for element_config in elements:
			if element_config.get(_C)==element_name:return element_config
	def _get_mcp_details(self,mcp_name,current_var):
		mcps=self._raw_session_data.get(_B,{}).get(_E,{}).get(_B,{}).get(_J,{}).get('mcps',[]);mcp_config=next((mcp_config for mcp_config in mcps if mcp_config.get(_C)==mcp_name),_A)
		if mcp_config:
			mcp_config=self._evaluate_vars_in_structure(mcp_config,current_var);mcp_config[_L]=self._clean_text(mcp_config.get(_L,''));mcp_config[_Z]=self._evaluate_f_string(mcp_config.get(_Z,''),current_var);mcp_config[_A4]=self._clean_text(mcp_config.get(_A4,''));mcp_config['cwd']=self._clean_text(mcp_config.get('cwd',''))
			if _I in mcp_config and isinstance(mcp_config.get(_I),dict):args_dict=mcp_config[_I];sorted_arg_list=[value for(key,value)in sorted(args_dict.items(),key=lambda item:int(item[0]))];mcp_config[_I]=[self._clean_text(arg)for arg in sorted_arg_list]
			if mcp_config.get(_A5):mcp_config[_A5]={k:self._clean_text(v)for(k,v)in mcp_config[_A5].items()}
		else:logger.warning(f"MCP configuration '{mcp_name}' not found in session data.")
		return mcp_config
	async def _run_prompt_action(self,user_input,intent_subprompt):
		if not intent_subprompt:return self.var,''
		all_individual_subprompt_responses=[]
		for(_indx,current_prompt_item)in sorted(intent_subprompt.items()):
			if _AC in current_prompt_item:
				prompt_value=current_prompt_item[_AC]
				if isinstance(prompt_value,list)and len(prompt_value)>1:batch_responses,updated_var=await self._run_async_prompts_for_list(prompt_value,user_input,self.var.copy());self.var.update(updated_var);all_individual_subprompt_responses.extend(batch_responses)
				else:
					target_prompt=prompt_value[0]if isinstance(prompt_value,list)else prompt_value;self.var,resp_var_name=await self._prompt_response(target_prompt,user_input)
					if resp_var_name and self.var.get(resp_var_name):all_individual_subprompt_responses.append(str(self.var[resp_var_name]))
			elif _q in current_prompt_item:
				self.var,step_response=await self._run_mcp_action(self.var,current_prompt_item[_q],user_input)
				if step_response:all_individual_subprompt_responses.append(step_response)
		self._sub_message=' '.join(filter(_A,all_individual_subprompt_responses)).strip();return self.var,self._sub_message
	@staticmethod
	@asynccontextmanager
	async def _websocket_client_context(uri):
		'A context manager for a WebSocket client connection that yields read/write callables.'
		try:
			async with websockets.connect(uri)as websocket:
				async def read():
					message=await websocket.recv()
					if isinstance(message,str):return message.encode(_N)
					return message
				async def write(data):await websocket.send(data.decode(_N))
				yield(read,write)
		except(websockets.exceptions.ConnectionClosedError,websockets.exceptions.InvalidURI,OSError)as e:logger.error(f"WebSocket connection to {uri} failed: {e}");raise PinionAIGrpcError(f"WebSocket connection failed: {e}")from e
	async def _select_mcp_config(self,mcp_group_names,current_var,user_input,mcp_group_config):
		'\n        Selects an MCP configuration from a group using an LLM.\n        ';C='mcp_descriptions';B='select_mcp';A='mcp_name';mcp_options=[]
		for name in mcp_group_names:
			config=self._get_mcp_details(name,current_var)
			if config:mcp_options.append(config)
		if not mcp_options:logger.warning('No valid MCP options found in the group.');return
		select_mcp_declaration=FunctionDeclaration(name=B,description="Select the most appropriate MCP from the list based on the user's request.",parameters={_F:_r,_AN:{A:{_F:_AQ,_L:'The name of the selected MCP.',_AP:[mcp.get(_C)for mcp in mcp_options]}},_AO:[A]});prompt_name=mcp_group_config.get(_BT,'');prompt_config=_A;prompt_resp_var_name=_A;current_prompt_text=user_input or''
		if prompt_name:
			logger.info(f"MCP '{mcp_name}' is using prompt '{prompt_name}'.");prompt_config,_,_=self._get_prompt_details(prompt_name,current_var)
			if not prompt_config:error_msg=f"Error: Prompt '{prompt_name}' for MCP '{mcp_name}' not found.";logger.error(error_msg);return current_var,error_msg
			prompt_model_provider=prompt_config.get('modelProvider',_e);prompt_model=_Ax
			if prompt_config.get(_X):prompt_model=prompt_config.get(_X)
			prompt_resp_var_name=prompt_config.get(_AF,'');prompt_body_template=self._clean_text(prompt_config.get(_W,''));mcp_group_prompt_text=self._evaluate_f_string(prompt_body_template,current_var,user_input=user_input)
		self.var[C]=' '.join([f"- {mcp.get(_C)}: {mcp.get(_L,'No description')}"for mcp in mcp_options]);prompt_text=f"Based on the user's request: '{user_input}', and the following available MCPs, which one should be used? {self.var[C]} Please select the closest match to the user's request for the MCP fit. Return Only the name of the MCP as a string.";config=google_genai_types.GenerateContentConfig(tools=[Tool(function_declarations=[select_mcp_declaration])]);selected_mcp_name,_,function_calls=await self._get_gemini_response_async(prompt_model,[mcp_group_prompt_text],config)
		if function_calls and function_calls[0][_C]==B:selected_mcp_name=function_calls[0][_I].get(A);logger.info(f"LLM selected MCP '{selected_mcp_name}' from the group.")
		if selected_mcp_name:
			for mcp_option in mcp_options:
				if mcp_option.get(_C)==selected_mcp_name:return mcp_option
		logger.warning('LLM did not select an MCP from the group. Cannot proceed.')
	async def _run_mcp_action(self,current_var,mcp_name,user_input=_A):
		"\n        Runs a multi-step process (MCP) action defined by the mcp_name.\n        This function retrieves the MCP configuration and executes it by connecting to a\n        local (stdio) or remote (http) MCP server using fastmcp.\n        Args:\n            current_var: The current variable dictionary to update.\n            mcp_name: The name of the MCP to execute.\n            user_input: The user's input to pass to the MCP.\n\n        Returns:\n            The updated variable dictionary and an optional final response message.\n        ";M='mcpServers';L='streamable-http';K='groupNames';J='get_mcp_prompt_handler';I='read_mcp_resource_handler';H='call_mcp_tool_handler';G='http';F='transport';E='prompt_args';D='prompt_name';C='resource_uri';B='tool_name';A='tool_args';mcp_config=self._get_mcp_details(mcp_name,current_var)
		if not mcp_config:logger.warning(f"MCP configuration '{mcp_name}' not found.");return current_var,f"Error: MCP configuration '{mcp_name}' not found."
		try:
			if mcp_config.get('serverGroup',_G)and mcp_config.get(K):
				logger.info(f"MCP Group '{mcp_name}' detected. Selecting a member to run...");group_names=mcp_config[K]
				if isinstance(group_names,str):group_names=[group_names]
				selected_config_from_group=await self._select_mcp_config(group_names,current_var,user_input,mcp_config)
				if not selected_config_from_group:logger.warning(f"Could not select an MCP from group '{mcp_name}'.");return current_var,f"Error: Could not decide which MCP to use from group '{mcp_name}'."
				mcp_config=selected_config_from_group;mcp_name=mcp_config.get(_C,mcp_name)
			prompt_name=mcp_config.get(_BT,'');prompt_config=_A;prompt_resp_var_name=_A;current_prompt_text=user_input or''
			if prompt_name:
				logger.info(f"MCP '{mcp_name}' is using prompt '{prompt_name}'.");prompt_config,_,_=self._get_prompt_details(prompt_name,current_var)
				if not prompt_config:error_msg=f"Error: Prompt '{prompt_name}' for MCP '{mcp_name}' not found.";logger.error(error_msg);return current_var,error_msg
				prompt_resp_var_name=prompt_config.get(_AF,'');prompt_body_template=self._clean_text(prompt_config.get(_W,''));current_prompt_text=self._evaluate_f_string(prompt_body_template,current_var,user_input=user_input)
			mcp_transport=mcp_config.get(F,'');mcp_url=mcp_config.get(_Z,'');mcp_description=mcp_config.get(_L,'');mcp_command=mcp_config.get(_A4,'');mcp_args=mcp_config.get(_I,{});mcp_cwd=mcp_config.get('cwd','');mcp_args=mcp_config.get(_I,[]);mcp_params=mcp_config.get('parametersJson',{});mcp_env=mcp_config.get(_A5,{});mcp_name=mcp_config.get(_C,'default');required_inputs=[]
			if mcp_params:
				for(param_key,param_value_template)in mcp_params.items():
					evaluated_value=self._evaluate_f_string(str(param_value_template),current_var)
					if not evaluated_value:
						logger.warning(f"MCP parameter '{param_key}' evaluated to an empty value.");required_inputs.append((param_key,f"Please provide a value for'{param_key}'."))
						if param_key not in current_var:current_var[param_key]=''
					else:mcp_params[param_key]=evaluated_value
			if required_inputs:
				normalized_required=[(it[0],it[1]if len(it)>1 else _A)for it in required_inputs];current_var,prompt_msg,waiting=await self._collect_required_inputs(current_var,normalized_required)
				if waiting:return current_var,prompt_msg
			session_context=_A;is_http_call=mcp_transport in[G,L]or not mcp_transport and mcp_url.startswith(('http://','https://'));is_stdio_call=mcp_transport=='stdio'or not mcp_transport and not mcp_url and mcp_config.get(_A4)
			if is_http_call:
				eval_mcp_url=mcp_url;http_headers=self._evaluate_vars_in_structure(mcp_config.get(_Ay,{}),current_var);mcp_connector=mcp_config.get(_U,'')
				if mcp_connector:
					connector_config=self._get_connector_details(mcp_connector)
					if connector_config:
						try:
							token=await self._get_token_for_connector(connector_config)
							if token:http_headers[_M]=token
						except PinionAIAPIError as e:logger.warning(f"Could not get token for connector '{mcp_connector}': {e}. Proceeding without token.")
					else:logger.warning(f"Connector '{mcp_connector}' not found for MCP '{mcp_name}'.")
				logger.info(f"Connecting to remote HTTP MCP '{mcp_name}' at URL: {eval_mcp_url}");logger.debug(f"  [MCP HTTP Headers]: {http_headers}");client_transport=mcp_config.get(F,G)
				if client_transport==L:client_transport=G
				client_config={M:{mcp_name:{F:client_transport,_Z:eval_mcp_url}}}
				if http_headers:client_config[M][mcp_name]['headers']=http_headers
				session_context=Client(client_config,timeout=18e1)
			elif is_stdio_call:
				command=self._evaluate_f_string(self._clean_text(mcp_config.get(_A4,'')),current_var)
				if not command or command.lower()=='python':command=sys.executable
				args=[self._evaluate_f_string(self._clean_text(arg),current_var)for arg in mcp_config.get(_I,[])]
				if command==sys.executable and args:
					script_path_arg=args[0];absolute_script_path=os.path.abspath(script_path_arg)
					if not os.path.exists(absolute_script_path):error_msg=f"MCP script file not found at path: {absolute_script_path}. Please check the 'args' in your MCP configuration for '{mcp_name}' and ensure the file exists.";logger.error(error_msg);return current_var,error_msg
				mcp_env_from_config=self._evaluate_vars_in_structure(mcp_config.get(_A5,{}),current_var);final_env=_A
				if mcp_env_from_config:final_env=os.environ.copy();str_mcp_env={k:str(v)for(k,v)in mcp_env_from_config.items()};final_env.update(str_mcp_env)
				cwd=self._evaluate_f_string(self._clean_text(mcp_config.get('cwd','')),current_var);transport=StdioTransport(command=command,args=args,env=final_env,cwd=cwd if cwd else _A,keep_alive=mcp_config.get('keepAlive',_D));session_context=Client(transport,timeout=18e1)
			else:error_msg=f"Unsupported or ambiguous transport for MCP '{mcp_name}'. Configure URL for http or command for stdio.";logger.error(error_msg);return current_var,error_msg
			if session_context:
				async with session_context as session:
					gemini_client=self._genai_client
					if not gemini_client:return current_var,'Error: Gemini AI client is not configured. Required for MCP.'
					mcp_tools,mcp_resources,mcp_prompts=[],[],[]
					for attempt in range(5):
						try:
							mcp_tools_resp=await session.list_tools()
							if hasattr(mcp_tools_resp,_O)and mcp_tools_resp.tools or isinstance(mcp_tools_resp,list)and mcp_tools_resp:mcp_tools=mcp_tools_resp.tools if hasattr(mcp_tools_resp,_O)else mcp_tools_resp;logger.info(f"MCP '{mcp_name}' is ready with tools after {attempt+1} attempt(s).");break
						except Exception as e:logger.warning(f"Could not list tools from MCP '{mcp_name}' on attempt {attempt+1}. Error: {e}")
						if is_stdio_call:await asyncio.sleep(.2*(attempt+1))
						else:break
					try:
						mcp_resources_resp=await session.list_resources()
						if hasattr(mcp_resources_resp,'resources')and mcp_resources_resp.resources:mcp_resources=mcp_resources_resp.resources
						elif isinstance(mcp_resources_resp,list):mcp_resources=mcp_resources_resp
					except Exception as e:logger.warning(f"Could not list resources from MCP '{mcp_name}'. This may be expected. Error: {e}")
					try:
						mcp_prompts_resp=await session.list_prompts()
						if hasattr(mcp_prompts_resp,'prompts')and mcp_prompts_resp.prompts:mcp_prompts=mcp_prompts_resp.prompts
						elif isinstance(mcp_prompts_resp,list):mcp_prompts=mcp_prompts_resp
					except Exception as e:logger.warning(f"Could not list prompts from MCP '{mcp_name}'. This may be expected. Error: {e}")
					llm_tools=[]
					if mcp_tools:llm_tools.append(FunctionDeclaration(name=H,description='Calls a specific tool available on the MCP server.',parameters={_F:_r,_AN:{B:{_F:_AQ,_AP:[t.name for t in mcp_tools],_L:'The name of the tool to call.'},A:{_F:_r,_L:'The arguments for the tool as a JSON object.'}},_AO:[B,A]}))
					if mcp_resources:llm_tools.append(FunctionDeclaration(name=I,description='Reads a specific resource (e.g., a file or data entry) from the MCP server.',parameters={_F:_r,_AN:{C:{_F:_AQ,_AP:[r.uri for r in mcp_resources],_L:'The URI of the resource to read.'}},_AO:[C]}))
					if mcp_prompts:llm_tools.append(FunctionDeclaration(name=J,description='Gets a pre-defined, rendered prompt template from the MCP server.',parameters={_F:_r,_AN:{D:{_F:_AQ,_AP:[p.name for p in mcp_prompts],_L:'The name of the prompt to get.'},E:{_F:_r,_L:'The arguments for rendering the prompt template.'}},_AO:[D]}))
					if not llm_tools:return current_var,f"Error: MCP '{mcp_name}' has no tools, resources, or prompts to use."
					logger.info(f"Asking LLM to choose a mcp activity: '{current_prompt_text[:100]}...'");model_provider=prompt_config.get(_Aw,_e)if prompt_config else _e;model_to_use=_Ax
					if prompt_config and prompt_config.get(_X):model_to_use=prompt_config.get(_X)
					selection_prompt_text=f"For {mcp_name}, decide which available tool, resource or prompt to use based on the user's request: '{user_input}' and consider the description {mcp_description} and the available parameters and arguments: {mcp_params} {mcp_args}. Which should be used? Please select the closest match to the user's request and available variables. Return only the name of the selected tool, resource or prompt."
					if model_provider==_e:config=google_genai_types.GenerateContentConfig(tools=[Tool(function_declarations=llm_tools)],temperature=mcp_config.get('initialTemperature',.5));selected_option,_,function_calls=await self._get_gemini_response_async(model_to_use,[selection_prompt_text],config);llm_response_text=selected_option
					else:logger.error(f"Unsupported model provider '{model_provider}' for MCP '{mcp_name}'. Only 'google' is supported.");return current_var,f"Error: Unsupported model provider '{model_provider}' for MCP '{mcp_name}'."
					mcp_result=_A;chosen_call=_A
					if function_calls:chosen_call=function_calls[0]
					elif selected_option:
						selected_name=selected_option.strip()
						if any(t.name==selected_name for t in mcp_tools):chosen_call={_C:H,_I:{B:selected_name,A:mcp_params}}
						elif any(r.uri==selected_name for r in mcp_resources):chosen_call={_C:I,_I:{C:selected_name}}
						elif any(p.name==selected_name for p in mcp_prompts):chosen_call={_C:J,_I:{D:selected_name,E:mcp_params}}
					if chosen_call:
						handler_name=chosen_call.get(_C);handler_args=chosen_call.get(_I,{})
						if handler_name==H:
							tool_to_call=handler_args.get(B);final_params=mcp_params.copy()
							if handler_args.get(A):final_params.update(handler_args.get(A,{}))
							mcp_result=await self._call_mcp_tool(session,tool_to_call,final_params)
						elif handler_name==I:resource_to_read=handler_args.get(C);mcp_result=await self._read_mcp_resource(session,resource_to_read)
						elif handler_name==J:
							prompt_to_get=handler_args.get(D);final_prompt_args=mcp_params.copy()
							if handler_args.get(E):final_prompt_args.update(handler_args.get(E,{}))
							mcp_result=await self._get_mcp_prompt(session,prompt_to_get,final_prompt_args)
						else:logger.warning(f"LLM chose an unknown handler: {handler_name}");mcp_result=f"Error: AI tried to call an unknown handler '{handler_name}'."
					else:logger.warning(f"LLM response '{selected_option}' did not result in a valid action.");mcp_result=selected_option
					final_result_value=mcp_result
					if hasattr(mcp_result,_A6)and getattr(mcp_result,_A6)is not _A:final_result_value=getattr(mcp_result,_A6)
					elif hasattr(mcp_result,_B)and getattr(mcp_result,_B)is not _A:final_result_value=getattr(mcp_result,_B)
					mcp_result_str=json.dumps(final_result_value,indent=2)if isinstance(final_result_value,(dict,list))else str(final_result_value)if final_result_value is not _A else _A;mcp_result_variable=mcp_config.get(_a)
					if mcp_result_variable:current_var[mcp_result_variable]=final_result_value
					if prompt_resp_var_name:current_var[prompt_resp_var_name]=final_result_value
					return current_var,mcp_result_str
			return current_var,f"Error: Could not establish session for MCP '{mcp_name}'."
		except Exception as e:logger.error(f"Error during MCP execution for '{mcp_name}': {e}",exc_info=_D);return current_var,f"Error in MCP execution: {e}"
	@staticmethod
	async def _call_mcp_tool(session,tool_name,args):
		'Helper to call a tool on the MCP session.'
		try:
			result=await session.call_tool(tool_name,args)
			if hasattr(result,_B)and result.data:return result.data
			if hasattr(result,_A6)and result.result is not _A:return result.result
			return result
		except Exception as e:logger.error(f"Error calling MCP tool '{tool_name}': {e}");return{_V:f"Failed to call tool '{tool_name}': {e}"}
	@staticmethod
	async def _read_mcp_resource(session,resource_uri):
		'Helper to read a resource from the MCP session.'
		try:
			result=await session.get_resource(resource_uri)
			if result and isinstance(result,list)and hasattr(result[0],_P):return result[0].text
			return result
		except Exception as e:logger.error(f"Error reading MCP resource '{resource_uri}': {e}");return{_V:f"Failed to read resource '{resource_uri}': {e}"}
	@staticmethod
	async def _get_mcp_prompt(session,prompt_name,args):
		'Helper to get a prompt from the MCP session.'
		try:
			result=await session.get_prompt(prompt_name,args)
			if hasattr(result,_B)and result.data:return result.data
			return result
		except Exception as e:logger.error(f"Error getting MCP prompt '{prompt_name}': {e}");return{_V:f"Failed to get prompt '{prompt_name}': {e}"}
	@staticmethod
	async def _execute_tool_calls(function_calls,session):
		"\n        Executes a list of function calls requested by the Gemini model via the session.\n\n        Args:\n            function_calls: A list of FunctionCall objects from the model's response.\n            session: The session object capable of executing tools via `call_tool`.\n\n        Returns:\n            A list of Part objects, each containing a FunctionResponse corresponding\n            to the execution result of a requested tool call.\n        ";tool_response_parts=[]
		for func_call in function_calls:
			tool_name=func_call.name;args=dict(func_call.args)if func_call.args else{};tool_result_payload:0
			try:
				tool_result=await session.call_tool(tool_name,args);result_text=''
				if hasattr(tool_result,_R)and tool_result.content and hasattr(tool_result.content[0],_P):result_text=tool_result.content[0].text or''
				if hasattr(tool_result,'isError')and tool_result.isError:error_message=result_text or f"Tool '{tool_name}' failed without specific error message.";tool_result_payload={_V:error_message}
				else:tool_result_payload={_A6:result_text}
			except Exception as e:error_message=f"Tool execution framework failed: {type(e).__name__}: {e}";tool_result_payload={_V:error_message}
			tool_response_parts.append(google_genai_types.Part.from_function_response(name=tool_name,response=tool_result_payload))
		return tool_response_parts
	async def _run_agent_loop(self,prompt,client,session,model_id,max_tool_turns,initial_temperature,tool_call_temperature,mcp_description=_A):
		'\n        Runs a multi-turn conversation loop with a Gemini model, handling tool calls \n        that occur after tool execution.\n\n        This function orchestrates the interaction between a user prompt, a Gemini\n        model capable of function calling, and a session object that provides\n        and executes tools. It handles the cycle of:\n        1. Sending the user prompt (and conversation history) to the model.\n        2. If the model requests tool calls, executing them via the `session`.\n        3. Sending the tool execution results back to the model.\n        4. Repeating until the model provides a text response or the maximum\n        number of tool execution turns is reached.\n\n        Args:\n            prompt: The initial user prompt to start the conversation.\n            client: An initialized Gemini GenerativeModel client object\n\n            session: An active session object responsible for listing available tools\n                    via `list_tools()` and executing them via `call_tool(tool_name, args)`.\n                    It\'s also expected to have an `initialize()` method.\n            model_id: The identifier of the Gemini model to use (e.g., "gemini-2.0-flash").\n            max_tool_turns: The maximum number of consecutive turns dedicated to tool calls\n                            before forcing a final response or exiting.\n            initial_temperature: The temperature setting for the first model call.\n            tool_call_temperature: The temperature setting for subsequent model calls\n                                that occur after tool execution.\n            mcp_description: An optional high-level description of the MCP\'s purpose,\n                             used as a system instruction for the model.\n\n        Returns:\n            The final text response from the Gemini model after the\n            conversation loop concludes (either with a text response or after\n            reaching the max tool turns). An empty string may be returned on error or no response.\n\n        Raises:\n            ValueError: If the session object does not provide any tools.\n            Exception: Can potentially raise exceptions from the underlying API calls\n                    or session tool execution if not caught internally by `_execute_tool_calls`.\n        ';contents=[google_genai_types.Content(role=_b,parts=[google_genai_types.Part(text=prompt)])]
		if hasattr(session,'initialize')and callable(session.initialize):await session.initialize()
		else:logger.debug('Session object does not have an initialize() method, proceeding anyway.')
		session_tool_list=await session.list_tools()
		if not session_tool_list or not session_tool_list.tools:raise ValueError('No tools provided by the session. Agent loop cannot proceed.')
		gemini_tool_config=google_genai_types.Tool(function_declarations=[types.FunctionDeclaration(name=tool.name,description=tool.description,parameters=tool.inputSchema)for tool in session_tool_list.tools]);base_gen_config_dict={_O:[gemini_tool_config]}
		if mcp_description:base_gen_config_dict['system_instruction']=mcp_description
		initial_config=google_genai_types.GenerateContentConfig(temperature=initial_temperature,**base_gen_config_dict);response=await client.aio.models.generate_content(model=model_id,contents=contents,config=initial_config)
		if not response.candidates:return''
		contents.append(response.candidates[0].content);turn_count=0;latest_content=response.candidates[0].content;has_function_calls=any(part.function_call for part in latest_content.parts)
		while has_function_calls and turn_count<max_tool_turns:
			turn_count+=1;function_calls_to_execute=[part.function_call for part in latest_content.parts if part.function_call];tool_response_parts=await self._execute_tool_calls(function_calls_to_execute,session);contents.append(google_genai_types.Content(role=_Az,parts=tool_response_parts));subsequent_config=google_genai_types.GenerateContentConfig(temperature=tool_call_temperature,**base_gen_config_dict);response=await client.aio.models.generate_content(model=model_id,contents=contents,config=subsequent_config)
			if not response.candidates:break
			latest_content=response.candidates[0].content;contents.append(latest_content);has_function_calls=any(part.function_call for part in latest_content.parts)
			if not has_function_calls:logger.debug('Model response contains text, no further tool calls requested this turn.')
		if turn_count>=max_tool_turns and has_function_calls:logger.debug(f"Maximum tool turns ({max_tool_turns}) reached. Exiting loop even though function calls might be pending.")
		elif not has_function_calls:logger.debug('Tool calling loop finished naturally (model provided text response).')
		logger.debug('Agent loop finished. Returning final response.');final_text_response=''
		if response.candidates:
			try:final_text_response=''.join(part.text for part in response.candidates[0].content.parts if hasattr(part,_P)and part.text)
			except(AttributeError,IndexError):logger.debug('Could not extract final text from response parts.')
		return final_text_response
	async def _run_api_action(self,current_var,api_name):
		B='GET';A='content_type'
		if current_var.get(_H):logger.debug(f"Run API | {api_name}")
		api_config=self._get_api_details(api_name)
		if not api_config:logger.warning(f"API configuration '{api_name}' not found.");return current_var,_A
		headers={}
		if api_config.get(_Ay):
			try:headers.update(json.loads(api_config[_Ay]))
			except json.JSONDecodeError:logger.warning(f"Invalid JSON in API header for {api_name}")
		else:headers[_s]=_A7
		if api_config.get(A):headers[_Q]=api_config[A]
		if api_config.get(_U):
			connector_config=self._get_connector_details(api_config[_U])
			if connector_config:
				try:
					token=await self._get_token_for_connector(connector_config)
					if token:headers[_M]=token
				except PinionAIAPIError as e:logger.warning(f"Could not get token for connector '{api_config[_U]}': {e}. Proceeding without token.")
			else:logger.warning(f"Connector '{api_config[_U]}' not found for API '{api_name}'.")
		method=api_config.get(_f,B).upper()
		try:
			if method in['POST','PUT']:current_var,_,_,final_response_message=await self._generic_api_post_put(current_var,api_config,headers,method)
			elif method==B:current_var,_,_,final_response_message=await self._generic_api_get(current_var,api_config,headers)
			else:logger.warning(f"Unsupported API method '{method}' for API '{api_name}'.")
		except PinionAIAPIError as e:
			logger.error(f"Failed to execute API action '{api_name}': {e}")
			if api_config.get(_a):current_var[api_config[_a]]={_V:str(e)}
		return current_var,final_response_message
	def _run_parser_action(self,current_var,parser_name):
		if current_var.get(_H):logger.debug(f"Run Parser | {parser_name}")
		parser_config=self._get_parser_details(parser_name)
		if not parser_config:logger.warning(f"Parser configuration '{parser_name}' not found.");return current_var,_A
		source_var_name=parser_config.get(_BU)
		if not source_var_name or source_var_name not in current_var:logger.warning(f"Parser source variable '{source_var_name}' not found in var for parser '{parser_name}'.");return current_var
		parser_source_data=current_var[source_var_name];parser_type=parser_config.get(_F);var_map=parser_config.get('varNameToValueMap',{})
		try:
			if parser_type==_A8:
				json_data=json.loads(parser_source_data)if isinstance(parser_source_data,str)else parser_source_data
				for(out_var_name,json_path_expr_str)in var_map.items():match=jsonpath_parse(json_path_expr_str).find(json_data);current_var[out_var_name]=match[0].value if match else _A
			elif parser_type=='xml':
				xml_data=xmltodict.parse(parser_source_data)
				for(out_var_name,xml_path_str)in var_map.items():
					value=xml_data
					try:
						for key_part in xml_path_str.split('.'):value=value.get(key_part)
						current_var[out_var_name]=value
					except AttributeError:current_var[out_var_name]=_A
			elif parser_type=='csv':
				csv_io=StringIO(parser_source_data);df=pd.read_csv(csv_io)
				for(out_var_name,column_name)in var_map.items():current_var[out_var_name]=df[column_name].tolist()if column_name in df.columns else _A
			elif parser_type==_P:
				method=parser_config.get(_f);delimiter=parser_config.get('delimiter')
				if method=='split'and delimiter is not _A:
					parts=str(parser_source_data).split(delimiter)
					for(out_var_name,index_str)in var_map.items():
						try:idx=int(index_str);current_var[out_var_name]=parts[idx].strip()if 0<=idx<len(parts)else _A
						except(ValueError,IndexError):current_var[out_var_name]=_A
				elif method=='partition'and delimiter is not _A:
					parts=str(parser_source_data).partition(delimiter)
					for(out_var_name,index_str)in var_map.items():
						try:idx=int(index_str);current_var[out_var_name]=parts[idx].strip()if 0<=idx<3 else _A
						except(ValueError,IndexError):current_var[out_var_name]=_A
				elif method=='regex':
					for(out_var_name,pattern_str)in var_map.items():match=re.search(pattern_str,str(parser_source_data));current_var[out_var_name]=match.group(0)if match else _A
				else:logger.warning(f"Unknown text parsing method '{method}' or missing delimiter for parser '{parser_name}'.")
			else:logger.warning(f"Unknown parser type '{parser_type}' for parser '{parser_name}'.")
		except Exception as e:
			logger.error(f"Error during parsing with '{parser_name}' on source '{source_var_name}': {e}",exc_info=_D)
			for out_var_name in var_map.keys():current_var[out_var_name]=_A
		return current_var,_A
	def _run_merger_action(self,current_var,merger_name):
		if current_var.get(_H):logger.debug(f"Run Merger | {merger_name}")
		merger_config=self._get_merger_details(merger_name)
		if not merger_config:logger.warning(f"Merger configuration '{merger_name}' not found.");return current_var,_A
		dest_var_name=merger_config.get(_BV)
		if not dest_var_name:logger.warning(f"Merger destination variable not specified for merger '{merger_name}'.");return current_var,_A
		template_str=self._clean_text(merger_config.get('mergerTemplate',''));merged_output_str=self._evaluate_f_string(template_str,current_var);output_type=merger_config.get('outputType',_P)
		try:
			if output_type==_A8:current_var[dest_var_name]=json.loads(merged_output_str)
			elif output_type=='xml':current_var[dest_var_name]=xmltodict.parse(merged_output_str)
			elif output_type=='csv':current_var[dest_var_name]=pd.read_csv(StringIO(merged_output_str))
			else:current_var[dest_var_name]=merged_output_str
		except Exception as e:logger.error(f"Error processing merged output for type '{output_type}' in merger '{merger_name}': {e}");current_var[dest_var_name]=_A
		return current_var,_A
	async def _run_script_action(self,var,script_name):
		if var.get(_H):logger.debug(f"Run Script | {script_name}")
		script_config=self._get_script_details(script_name)
		if not script_config:logger.warning(f"Script configuration '{script_name}' not found.");return var,_A
		script_type=script_config.get(_F);script_code=script_config.get(_W);result_var_name=script_config.get(_a)
		if not script_code:logger.warning(f"Script body is empty for script '{script_name}'.");return var,_A
		try:
			if script_type=='javascript':
				if not MiniRacer:raise PinionAIConfigurationError("The 'py-mini-racer' library is required to run JavaScript scripts. Please install it with 'pip install py-mini-racer'.")
				ctx=MiniRacer();pyvar=var.copy()
				try:ctx.eval(script_code)
				except Exception as e:logger.error(f"Error adding function into JS: {e}",exc_info=_D);return var,_A
				try:
					script_result=ctx.call('main',pyvar)
					if script_result and isinstance(script_result,str):
						try:script_result_obj=json.loads(script_result)
						except Exception:script_result_obj=script_result
					else:script_result_obj=script_result
					if result_var_name and script_result_obj is not _A:var[result_var_name]=script_result_obj
				except Exception as e:logger.error(f"Error executing JS script: {e}",exc_info=_D)
				return var,_A
			elif script_type=='python':
				local_script_vars=var.copy();logger.warning('Executing Python scripts from the database is a security risk and is currently disabled.');exec(script_code,{_BW:{}},local_script_vars)
				if result_var_name and result_var_name in local_script_vars:var[result_var_name]=local_script_vars[result_var_name]
			else:logger.warning(f"Unsupported script type '{script_type}' for script '{script_name}'.")
		except Exception as e:logger.error(f"Error executing script '{script_name}': {e}",exc_info=_D)
		return var,_A
	async def _run_rule_action(self,current_var,rule_name,user_input):
		if current_var.get(_H):logger.debug(f"Run Rule | {rule_name}")
		rule_config=self._get_rule_details(rule_name)
		if not rule_config:logger.warning(f"Rule configuration '{rule_name}' not found.");return current_var,_A
		expr=rule_config.get('condition')
		if not expr:logger.warning(f"Rule '{rule_name}' has no 'rule_condition' defined.");return current_var,_A
		result=await self._evaluate_rule(expr,current_var);logger.info(f"Rule '{rule_name}' triggered and evaluated. Result: {result}")
		if(result_variable:=rule_config.get(_a)):
			self.var[result_variable]=result
			if current_var.get(_H):logger.debug(f"Rule '{rule_name}' result ({result}) stored in var['{result_variable}']")
		outcome_key=_A
		if result is _D:outcome_key='trueOutcome';outcome_key_type='trueType'
		elif result is _G:outcome_key='falseOutcome';outcome_key_type='falseType'
		step_response=_A
		if outcome_key:
			if(outcome_statement:=rule_config.get(outcome_key)):
				outcome_type=rule_config.get(outcome_key_type)
				if current_var.get(_H):logger.debug(f"Executing {outcome_type} '{outcome_key}' for rule '{rule_name}'")
				current_var,step_response=await self._execute_outcome(outcome_statement,outcome_type,user_input=user_input)
		return current_var,step_response
	async def _evaluate_rule(self,expr,var):
		'\n        Evaluates a rule expression string by first formatting it with variable data.\n\n        The expression string can contain f-string-like placeholders that reference\n        the \'var\' dictionary, which holds the provided variable data.\n\n        Example:\n            expr = "{var[\'value\']} > 10 and \'{var[\'status\']}\' == \'active\'"\n            var = {"value": 20, "status": "active"}\n            result = evaluate_rule(expr, var)  # result will be True\n\n        Args:\n            expr: The rule expression string to evaluate.\n            var: A dictionary of variables to be used in the expression.\n\n        Returns:\n            The result of the evaluated expression. Returns None if an error occurs\n            during formatting or evaluation.\n        '
		if not isinstance(expr,str):logger.warning(f"Rule expression is not a string: {expr}");return
		formatted_expr=''
		try:
			cleaned_expr=self._clean_text(expr);formatted_expr=self._evaluate_f_string(cleaned_expr,var)
			try:return eval(formatted_expr,{_BW:{}},{_A0:var})
			except Exception as e:logger.error(f"Error evaluating rule expression: '{expr}'. Formatted: '{formatted_expr}'. Error: {e}");return
		except KeyError as e:logger.error(f"Error accessing variable in rule expression: '{expr}'. Missing key: {e}.");return
		except Exception as e:logger.error(f"Error evaluating rule expression: '{expr}'. Formatted: '{formatted_expr}'. Error: {e}");return
	async def _execute_outcome(self,outcome_statement,outcome_type,user_input):
		'\n        Executes an outcome statement.\n\n        An outcome can:\n        1. "Set a variable": Set a variable to a value or another variable.\n        2. "Set a final response": Set a final response to terminate execution.\n        3. "Execute a flow": Trigger an action flow.\n        4. "Set Authorization":  Set self.is_authorized \n\n        Args:\n            statement: An outcome statement dictionary.\n            var: The dictionary of variables.\n\n        Returns:\n            A var and step_response if one is set, otherwise None.\n        ';A='set';step_response=_A
		if outcome_type=='Set a variable'and outcome_statement.get(A):
			set_config=outcome_statement.get(A);variable_to_set=set_config.get('variable');value_to_set=set_config.get(_As)
			if variable_to_set and value_to_set:template_str=self._clean_text(value_to_set);resolved_value=self._evaluate_f_string(template_str,self.var);self.var[variable_to_set]=resolved_value
			else:logger.warning(f"Outcome 'set' statement missing 'value'.")
			return self.var,step_response
		elif outcome_type=='Set a response':
			response_template=self._clean_text(outcome_statement.get(_AR,''));step_response=self._evaluate_f_string(response_template,self.var)
			if self.var.get(_H):logger.debug(f"Setting step response: {step_response}")
			return self.var,step_response
		elif outcome_type=='Execute a flow':
			if outcome_statement:
				self.var,action_response=await self._process_routing(self.var,outcome_statement,user_input=user_input)
				if action_response:step_response=action_response
		elif outcome_type=='Set Authentication':
			auth_value=outcome_statement.get(_As)
			if auth_value.lower()=='true':self.authorized=_D
			if auth_value.lower()=='false':self.authorized=_G
		return self.var,step_response
	async def _run_element_action(self,current_var,element_name):
		"\n        Handle an 'element' step defined in routing.\n        This function returns a prompt message (step_response) when element is required. \n        If no element matches, returns (current_var, None).\n        ";J='variableIn';I='isEmpty';H='uuid';G='password';F='otp';E='trim';D='decrypt';C='encrypt';B='hash';A='variableOut'
		if current_var.get(_H):logger.debug(f"Run Element | {element_name}")
		element_config=self._get_element_details(element_name)
		if not element_config:logger.warning(f"Element configuration '{element_name}' not found.");return current_var,_A
		ELEMENT_TYPES=[F,G,'secret',H,B,C,D,E,I];element_type=element_config.get(_F)
		if element_type=='date':generated_date=self._generate_date(element_config.get(_A_,'%Y-%m-%d'));variable_out=element_config.get(A);current_var[variable_out]=generated_date;return current_var,_A
		elif element_type=='datetime':generated_datetime=self._generate_datetime(element_config.get(_A_,'%Y-%m-%d %H:%M:%S'));variable_out=element_config.get(A);current_var[variable_out]=generated_datetime;return current_var,_A
		elif element_type==F:generated_otp=self._generate_otp();variable_out=element_config.get(A);current_var[variable_out]=generated_otp;return current_var,_A
		elif element_type==H:generated_uuid=self._generate_uid();variable_out=element_config.get(A);current_var[variable_out]=generated_uuid;return current_var,_A
		elif element_type==I:variable_in=element_config.get(J);variable_out=element_config.get(A);is_empty=self._is_empty(current_var.get(variable_in));current_var[variable_out]=is_empty;return current_var,_A
		elif element_type==G:variable_out=element_config.get(A);password_value=self._generate_password(element_config.get('size',12));current_var[variable_out]=password_value;return current_var,_A
		elif element_type in[B,C,D,E]:
			variable_in=element_config.get(J);variable_out=element_config.get(A);input_value=current_var.get(variable_in);key=element_config.get('key','')
			if input_value is _A:logger.warning(f"Element '{element_name}' input variable '{variable_in}' not found in var.");return current_var,_A
			if element_type==B:hash_value=self._hash_value(input_value);current_var[variable_out]=hash_value
			elif element_type==C:
				if not key:encrypted_value=self._encryption_manager.encrypt(input_value)
				else:encryption_client=EncryptionManager(client_secret=key);encrypted_value=encryption_client.encrypt(input_value)
				current_var[variable_out]=encrypted_value
			elif element_type==D:
				if not key:decrypted_value=self._encryption_manager.decrypt(input_value)
				else:encryption_client=EncryptionManager(client_secret=key);decrypted_value=encryption_client.decrypt(input_value)
				current_var[variable_out]=decrypted_value
			elif element_type==E:trimmed_value=str(input_value).strip();current_var[variable_out]=trimmed_value
			return current_var,_A
		return current_var,_A
	async def _run_input_action(self,current_var,input_config):
		'\n        Handle an \'input\' step defined in routing. `input_config` may be:\n          - a dict mapping variable -> prompt message, e.g. {"email": "Please enter email"}\n          - a numbered dict like {"0": {"email": "prompt"}, "1": {"phone": "prompt"}}\n        This function normalizes the structure, checks for missing variables and returns\n        a prompt message (step_response) when input is required. If no input is required,\n        returns (current_var, None).\n        '
		try:normalized=self._normalize_intent_vars(input_config if input_config is not _A else{})
		except Exception as e:logger.error(f"Failed to normalize input config for _run_input_action: {e}");return current_var,_A
		if not normalized:return current_var,_A
		current_var,prompt_msg,waiting=await self._collect_required_inputs(current_var,normalized)
		if waiting:current_var[_c]=current_var.get(_c,'');return current_var,prompt_msg
		return current_var,_A
	async def _run_delivery_action(self,current_var,delivery_name):
		C='\\s+';B='<[^>]+>';A='email'
		if current_var.get(_H):logger.debug(f"Run Delivery | {delivery_name}")
		delivery_config=self._get_delivery_details(delivery_name)
		if not delivery_config or not delivery_config.get('to'):logger.warning(f"Delivery '{delivery_name}' not configured properly or 'to' field missing.");return current_var,_A
		template_eval_vars=current_var.copy()
		for(key,value)in template_eval_vars.items():
			if self._is_likely_markdown(value):
				try:template_eval_vars[key]=markdown.markdown(value)
				except Exception as e:logger.error(f"Error converting markdown for delivery var['{key}']: {e}")
		to_address=self._evaluate_f_string(self._clean_line(delivery_config['to']),template_eval_vars);html_body_template=self._clean_text(delivery_config.get(_W,''));html_body_content=self._evaluate_f_string(html_body_template,template_eval_vars);plain_text_body=re.sub(B,' ',html_body_content);plain_text_body=re.sub(C,' ',plain_text_body).strip();from_address_template=delivery_config.get('from');from_address=self._evaluate_f_string(self._clean_line(from_address_template),template_eval_vars)if from_address_template else self._email_from_address;subject_template=delivery_config.get(_AS,'Your AI Delivery');subject=self._evaluate_f_string(self._clean_line(subject_template),template_eval_vars);cc_template=delivery_config.get('cc');cc_address=self._evaluate_f_string(self._clean_line(cc_template),template_eval_vars)if cc_template else _A;bcc_template=delivery_config.get('bcc');bcc_address=self._evaluate_f_string(self._clean_line(bcc_template),template_eval_vars)if bcc_template else _A;reply_to_template=delivery_config.get('replyTo');reply_to_address=self._evaluate_f_string(self._clean_line(reply_to_template),template_eval_vars)if reply_to_template else _A;delivery_type=delivery_config.get(_F);delivery_method=delivery_config.get(_f);final_response_message=_A;token=_A;headers={}
		if delivery_config.get(_U):
			connector_config=self._get_connector_details(delivery_config[_U])
			if connector_config:
				try:
					token=await self._get_token_for_connector(connector_config)
					if token:headers[_M]=token
				except PinionAIAPIError as e:logger.warning(f"Could not get token for connector '{delivery_config[_U]}': {e}. Proceeding without token.")
			else:logger.warning(f"Connector '{delivery_config[_U]}' not found for delivery '{delivery_name}'.")
		if delivery_type==A and delivery_method=='SendGrid':await self._sendgrid_email(plain_text_body,html_body_content,to_address,subject,from_address,cc_address,bcc_address,reply_to_address);logger.info(f"Email sent to {to_address} for delivery '{delivery_name}' via SendGrid.")
		elif delivery_type==A and delivery_method=='infobip':await self._infobip_send_email(plain_text_body,html_body_content,to_address,subject,from_address,token,cc_address,bcc_address,reply_to_address);logger.info(f"Email sent to {to_address} for delivery '{delivery_name}' via Infobip.")
		elif delivery_type==A and delivery_method=='Microsoft Graph API':await self._ms_graph_send_email(plain_text_body,html_body_content,to_address,subject,from_address,token,cc_address,bcc_address,reply_to_address)
		elif delivery_type==A and delivery_method=='Gmail API':await self._gmail_send_email(plain_text_body,html_body_content,to_address,subject,from_address,token,cc_address,bcc_address,reply_to_address)
		elif delivery_type=='sms'and delivery_method=='Twilio':sms_body_template=self._clean_text(delivery_config.get(_W,''));sms_intermediate_content=self._evaluate_f_string(sms_body_template,template_eval_vars);sms_to_send=re.sub(B,' ',sms_intermediate_content);sms_to_send=re.sub(C,' ',sms_to_send).strip();await self._twilio_sms_message(sms_to_send,to_address,from_address);logger.info(f"Twilio SMS sent to {to_address} for delivery '{delivery_name}'.")
		else:logger.warning(f"Unsupported delivery type/method: {delivery_type}/{delivery_method} for '{delivery_name}'.")
		delivery_response=delivery_config.get('deliveryResponseMessage','')
		if delivery_response:final_response_message=self._evaluate_f_string(delivery_response,template_eval_vars)
		return current_var,final_response_message
	async def _run_journey_action(self,current_var,action_details):
		"Handles a 'journey' type action, from either an intent or an action entity.";B='configuration';A='payment_description';action_key_var_name=action_details.get(_BX);action_key=current_var.get(action_key_var_name)if action_key_var_name else _A
		if not action_key:logger.warning(f"Journey action '{action_details.get(_C)}' requires a value from variable '{action_key_var_name}', but it was not found or is empty in 'var'.");return current_var,'Configuration error for journey action.'
		delivery_method=action_details.get(_B0);language=action_details.get(_d);_,self.unique_id,self.phone_number=format_phone(self.phone_number);json_payload={_Al:action_key,_o:{_f:delivery_method,_g:self.phone_number},_Am:{_An:self.unique_id,_g:self.phone_number},_E:{_Ao:self._session_id},_d:language}
		if current_var.get(_p):json_payload[_Ap]=current_var[_p]
		if action_details.get(_B1)=='credit card payment'and current_var.get(A):json_payload[B]={'credit-card-payment':{'currency':current_var.get('payment_currency'),'lineItems':[{'title':current_var.get(A),'amount':current_var.get('payment_amount'),'quantity':current_var.get('payment_quantity')}]}}
		if action_details.get(_B1)=='one time passcode':json_payload[B]={'random-code':{'code':'6'}}
		if action_details.get(_B0)=='voice':json_payload[_o]={_f:delivery_method,_g:self.phone_number,'callOperator':'twilio'}
		execution_id,execution_url,error_msg=await self._journey_send_pipeline(current_var,json_payload,delivery_method);final_response=_A
		if error_msg:final_response=error_msg
		elif execution_url:final_response=execution_url
		else:
			logger.info(f"A {action_details.get(_C)} {delivery_method} request has been sent.");is_completed,fulfillment_msg=await self._journey_session_pipeline_status_check(self._session_id,current_var,action_key,120)
			if is_completed:
				response_msg_template=self._clean_text(action_details.get(_h))
				if response_msg_template:final_response=self._evaluate_f_string(response_msg_template,current_var)
				else:final_response=fulfillment_msg
			else:final_response=fulfillment_msg
		return current_var,final_response
	def _run_transfer_action(self,current_var,action_details):
		"Handles a 'transfer' type action."
		if current_var.get(_Aa):
			current_time_utc=datetime.datetime.now(tz=zoneinfo.ZoneInfo('UTC'));self.transfer_requested=current_time_utc.isoformat();current_var['transfer_requested']=self.transfer_requested;sms_message=''
			if current_var.get(_Ab):passkey=self._generate_password(6);current_var['transferPasskey']=passkey;sms_message=f"Your agent will validate themselves with the following shared passkey: {passkey}"
			response_msg_template=action_details.get(_h)
			if response_msg_template:final_response=self._evaluate_f_string(self._clean_text(response_msg_template),current_var)
			else:final_response=f"You have requested to transfer. Please let the agent know your question. {sms_message}"
		else:final_response='Sorry, I am unable to transfer you.'
		return current_var,final_response
	def _map_to_standard_action_details(self,data):'Maps fields from an intent or action entity to a standard action_details dictionary.';return{_C:data.get(_C),_Aq:data.get('actionType'),_BX:data.get(_x),_B0:data.get(_Ai),_d:data.get(_d),_B1:data.get('actionEvent'),_h:data.get('actionResponseMessage'),_Ar:data.get(_Aj,{})}
	async def _run_action_action(self,current_var,action_name,final_response_from_caller=_A,user_input=_A):
		if current_var.get(_H):logger.debug(f"Run Action | {action_name}")
		action_entity_data=self._get_action_details(action_name)
		if not action_entity_data:logger.warning(f"Action '{action_name}' not found in agent configuration.");return current_var,_A
		action_details=self._map_to_standard_action_details(action_entity_data);action_type=action_details.get(_Aq,'general')
		if action_type=='journey':
			if current_var.get(_H):logger.debug(f"Executing journey action '{action_name}'")
			return await self._run_journey_action(current_var,action_details)
		elif action_type=='transfer':
			if current_var.get(_H):logger.debug(f"Executing transfer action '{action_name}'")
			return self._run_transfer_action(current_var,action_details)
		action_flow=action_details.get(_Ar,{});action_produced_final_response=_A
		if action_flow:
			if current_var.get(_H):logger.debug(f"Executing actionFlow for '{action_name}': {action_flow}")
			current_var,action_produced_final_response=await self._process_routing(current_var,action_flow,final_response_from_caller,user_input=user_input)
		else:logger.warning(f"Action '{action_name}' has no 'actionFlow' to execute.")
		if action_details.get(_h):
			response_msg_template=self._clean_text(action_details[_h]);generated_response=self._evaluate_f_string(response_msg_template,current_var);current_var['last_action_response']=generated_response;action_produced_final_response=generated_response
			if current_var.get(_H):logger.debug(f"Action '{action_name}' generated a response and stored it in 'last_action_response': {generated_response}")
		return current_var,action_produced_final_response
	async def _gcs_write(self,bucket_name,file_path,content_bytes,connector_name):
		'Handles writing a file to Google Cloud Storage.'
		if not storage:raise ImportError(_BY)
		gcs_client=_A
		if connector_name:
			conn_config=self._get_connector_details(connector_name)
			if conn_config and conn_config.get(_m)==_Af:sa_info=json.loads(conn_config.get(_n,'{}'));gcs_client=storage.Client.from_service_account_info(sa_info);logger.info(f"Using GCS service account from connector '{connector_name}'.")
		if not gcs_client:gcs_client=storage.Client();logger.info(_BZ)
		bucket=gcs_client.bucket(bucket_name);blob=bucket.blob(file_path);await asyncio.to_thread(blob.upload_from_string,content_bytes);logger.info(f"Successfully wrote to GCS: gs://{bucket_name}/{file_path}")
	async def _gcs_read(self,bucket_name,file_path,connector_name):
		'Handles reading a file from Google Cloud Storage.'
		if not storage:raise ImportError(_BY)
		gcs_client=_A
		if connector_name:
			conn_config=self._get_connector_details(connector_name)
			if conn_config and conn_config.get(_m)==_Af:sa_info=json.loads(conn_config.get(_n,'{}'));gcs_client=storage.Client.from_service_account_info(sa_info);logger.info(f"Using GCS service account from connector '{connector_name}'.")
		if not gcs_client:gcs_client=storage.Client();logger.info(_BZ)
		bucket=gcs_client.bucket(bucket_name);blob=bucket.blob(file_path);read_content_bytes=await asyncio.to_thread(blob.download_as_bytes);logger.info(f"Successfully read from GCS: gs://{bucket_name}/{file_path}");return read_content_bytes
	async def _s3_write(self,bucket_name,file_path,content_bytes,connector_name):
		'Handles writing a file to AWS S3.'
		if not boto3:raise ImportError(_Ba)
		s3_client=_A
		if connector_name:
			conn_config=self._get_connector_details(connector_name)
			if conn_config and conn_config.get(_m)=='aws_iam':s3_client=boto3.client('s3',aws_access_key_id=conn_config.get(_B2),aws_secret_access_key=conn_config.get(_n));logger.info(f"Using AWS IAM credentials from connector '{connector_name}'.")
		if not s3_client:s3_client=boto3.client('s3');logger.info(_Bb)
		await asyncio.to_thread(s3_client.put_object,Bucket=bucket_name,Key=file_path,Body=content_bytes);logger.info(f"Successfully wrote to S3: s3://{bucket_name}/{file_path}")
	async def _s3_read(self,bucket_name,file_path,connector_name):
		'Handles reading a file from AWS S3.'
		if not boto3:raise ImportError(_Ba)
		s3_client=_A
		if connector_name:
			conn_config=self._get_connector_details(connector_name)
			if conn_config and conn_config.get(_m)=='aws_iam':s3_client=boto3.client('s3',aws_access_key_id=conn_config.get(_B2),aws_secret_access_key=conn_config.get(_n));logger.info(f"Using AWS IAM credentials from connector '{connector_name}'.")
		if not s3_client:s3_client=boto3.client('s3');logger.info(_Bb)
		response=await asyncio.to_thread(s3_client.get_object,Bucket=bucket_name,Key=file_path);read_content_bytes=response['Body'].read();logger.info(f"Successfully read from S3: s3://{bucket_name}/{file_path}");return read_content_bytes
	async def _local_write(self,file_path,content_bytes):
		'Handles writing a file to the local filesystem.'
		def _sync_write():
			os.makedirs(os.path.dirname(file_path),exist_ok=_D)
			with open(file_path,'wb')as f:f.write(content_bytes)
		await asyncio.to_thread(_sync_write);logger.info(f"Successfully wrote to local path: {file_path}")
	async def _local_read(self,file_path):
		'Handles reading a file from the local filesystem.'
		def _sync_read():
			with open(file_path,'rb')as f:return f.read()
		read_content_bytes=await asyncio.to_thread(_sync_read);logger.info(f"Successfully read from local path: {file_path}");return read_content_bytes
	async def _run_file_action(self,current_var,file_name):
		'\n        Executes a file operation (read/write) for local, GCS, or S3 storage.\n        ';B='binary';A='both'
		if current_var.get(_H):logger.debug(f"Run File Action | {file_name}")
		file_config=self._get_file_details(file_name)
		if not file_config:logger.warning(f"File operation configuration '{file_name}' not found.");return current_var,f"Error: File operation '{file_name}' not found."
		provider=file_config.get('provider');direction=file_config.get('direction');path_template=file_config.get('pathTemplate','');bucket_name=file_config.get('bucketName');source_var=file_config.get(_BU);dest_var=file_config.get(_BV);connector_name=file_config.get(_U);file_format=file_config.get(_A_,_P);file_path=self._evaluate_f_string(path_template,current_var)
		if not file_path:logger.error(f"File path template '{path_template}' evaluated to an empty string for file action '{file_name}'.");return current_var,f"Error: File path for '{file_name}' is missing."
		is_write_op=direction in['write',A]and source_var and source_var in current_var and current_var[source_var]is not _A;is_read_op=direction in['read',A]and dest_var
		if not is_read_op and not is_write_op:logger.warning(f"File action '{file_name}' is not actionable. Direction: '{direction}', Source Var: '{source_var}', Dest Var: '{dest_var}'.");return current_var,_A
		try:
			content_bytes_to_write=_A
			if is_write_op:
				content=current_var.get(source_var)
				if file_format==_A8:content_bytes_to_write=json.dumps(content,indent=2).encode(_N)
				elif file_format=='csv':
					if isinstance(content,list)and content and isinstance(content[0],dict):df=pd.DataFrame(content);csv_buffer=StringIO();df.to_csv(csv_buffer,index=_G);content_bytes_to_write=csv_buffer.getvalue().encode(_N)
					else:raise ValueError('For CSV format, the source variable must contain a list of dictionaries.')
				elif file_format=='xml':
					if isinstance(content,dict):content_bytes_to_write=xmltodict.unparse({'root':content},pretty=_D).encode(_N)
					else:raise ValueError('For XML format, the source variable must contain a dictionary.')
				elif file_format==B:
					if not isinstance(content,bytes):raise ValueError('For binary format, the source variable must contain raw bytes.')
					content_bytes_to_write=content
				else:content_bytes_to_write=str(content).encode(_N)
			read_content_bytes=_A
			if provider=='gcs':
				if is_write_op:await self._gcs_write(bucket_name,file_path,content_bytes_to_write,connector_name)
				if is_read_op:read_content_bytes=await self._gcs_read(bucket_name,file_path,connector_name)
			elif provider=='s3':
				if is_write_op:await self._s3_write(bucket_name,file_path,content_bytes_to_write,connector_name)
				if is_read_op:read_content_bytes=await self._s3_read(bucket_name,file_path,connector_name)
			elif provider=='local':
				if is_write_op:await self._local_write(file_path,content_bytes_to_write)
				if is_read_op:read_content_bytes=await self._local_read(file_path)
			else:logger.error(f"Unsupported file provider: '{provider}' for file action '{file_name}'.");return current_var,f"Error: Unsupported file provider '{provider}'."
			if is_read_op and read_content_bytes is not _A:
				try:
					if file_format==_A8:current_var[dest_var]=json.loads(read_content_bytes)
					elif file_format=='csv':csv_io=StringIO(read_content_bytes.decode(_N));current_var[dest_var]=pd.read_csv(csv_io).to_dict('records')
					elif file_format=='xml':current_var[dest_var]=xmltodict.parse(read_content_bytes)
					elif file_format==B:current_var[dest_var]=read_content_bytes
					else:current_var[dest_var]=read_content_bytes.decode(_N)
				except Exception as e:logger.warning(f"Could not deserialize file content for format '{file_format}'. Falling back to raw text. Error: {e}");current_var[dest_var]=read_content_bytes.decode(_N,errors='ignore')
		except(ImportError,ValueError)as e:logger.error(f"Error during file operation '{file_name}': {e}");return current_var,f"Error: {e}"
		except FileNotFoundError:logger.error(f"File not found for read operation: {file_path}");return current_var,f"Error: File not found at {file_path}."
		except Exception as e:logger.error(f"An error occurred during '{provider}' file operation for '{file_name}': {e}",exc_info=_D);return current_var,f"Error during file operation: {e}"
		return current_var,_A
	def _configure_tools_for_request(self,direct_tool_configs,processed_fd_dicts,model_name):
		'\n        Consolidates tool configuration logic for a generation request.\n\n        This helper method prepares the final list of Tool objects by:\n        1. Processing pre-defined tools (like GoogleSearch).\n        2. Creating FunctionDeclaration objects from dictionaries.\n        3. Handling model-specific restrictions, such as mixing tool types.\n\n        Args:\n            direct_tool_configs: A list of pre-defined tool configurations.\n            processed_fd_dicts: A list of dictionaries for function declarations.\n            model_name: The name of the model for the request.\n\n        Returns:\n            A list of Tool objects ready for the API, or None if no tools are configured.\n        ';final_tools_for_config=[]
		if direct_tool_configs:final_tools_for_config.extend(self._prepare_tools_for_genai_config(direct_tool_configs))
		function_declarations=[]
		if processed_fd_dicts:
			for fd_dict in processed_fd_dicts:
				declaration=self._create_function_declaration_from_dict(fd_dict)
				if declaration:function_declarations.append(declaration)
		RESTRICTED_MODELS_FOR_MIXED_TOOLS={_Ax};has_functions=bool(function_declarations);has_search=any(t.google_search for t in final_tools_for_config);model_is_restricted=model_name in RESTRICTED_MODELS_FOR_MIXED_TOOLS
		if has_functions and has_search and model_is_restricted:final_tools_for_config=[t for t in final_tools_for_config if not t.google_search]
		if function_declarations:final_tools_for_config.append(Tool(function_declarations=function_declarations))
		return final_tools_for_config if final_tools_for_config else _A
	def _resolve_rag_store(self,store_name):
		'Resolve a rag store by name (case-insensitive, trimmed).\n\n        Returns a tuple: (resource_id, top_k, vector_distance_threshold).\n        Falls back to legacy self.var values when no match or when store_name is None/empty.\n        ';default_resource=self.var.get(_Ac,'');default_top_k=self.var.get(_Ad,10);default_vector_distance_threshold=self.var.get(_Ae,.5)
		if not store_name:return default_resource,default_top_k,default_vector_distance_threshold
		normalized=store_name.strip().lower()
		if hasattr(self,'_rag_stores_by_name')and self._rag_stores_by_name:
			if store_name in self._rag_stores_by_name:cfg=self._rag_stores_by_name[store_name];return cfg.get(_u,default_resource),cfg.get(_v,default_top_k),cfg.get(_w,default_vector_distance_threshold)
			for(k,cfg)in self._rag_stores_by_name.items():
				if k.strip().lower()==normalized:return cfg.get(_u,default_resource),cfg.get(_v,default_top_k),cfg.get(_w,default_vector_distance_threshold)
		return default_resource,default_top_k,default_vector_distance_threshold
	def _prepare_tools_for_genai_config(self,tools_list_from_config):
		'Prepares Tool objects for GenerateContentConfig, handling GoogleSearch strings.';B='function_declarations';A='rag_store';prepared_tools=[]
		if not tools_list_from_config:return prepared_tools
		for tool_item in tools_list_from_config:
			if isinstance(tool_item,str)and'GoogleSearch'in tool_item:prepared_tools.append(Tool(google_search=GoogleSearch()))
			elif isinstance(tool_item,str)and'ToolCodeExecution'in tool_item:prepared_tools.append(Tool(code_execution=ToolCodeExecution()))
			elif isinstance(tool_item,str)and'UrlContext'in tool_item:prepared_tools.append(Tool(url_context=UrlContext()))
			elif isinstance(tool_item,str)and'RagStore'in tool_item or isinstance(tool_item,Tool)and getattr(tool_item,'retrieval',_A)and getattr(tool_item.retrieval,A,_A):
				store_name=_A
				if isinstance(tool_item,str):
					try:
						if'('in tool_item and')'in tool_item:start=tool_item.index('(')+1;end=tool_item.index(')',start);store_name=tool_item[start:end].strip()
						elif':'in tool_item:
							parts=tool_item.split(':',1)
							if len(parts)>1:store_name=parts[1].strip()
					except Exception:store_name=_A
				elif isinstance(tool_item,Tool):
					try:
						rs=getattr(tool_item.retrieval,A,_A)or getattr(tool_item.retrieval,'vertex_rag_store',_A)
						if rs:store_name=getattr(rs,_C,_A)or getattr(rs,'store_name',_A)
					except Exception:store_name=_A
				resource_id,top_k,vector_distance_threshold=self._resolve_rag_store(store_name)
				if resource_id:prepared_tools.append(Tool(retrieval=Retrieval(vertex_rag_store=VertexRagStore(rag_resources=[VertexRagStoreRagResource(rag_corpus=resource_id)],similarity_top_k=top_k,vector_distance_threshold=vector_distance_threshold))))
			elif isinstance(tool_item,Tool):prepared_tools.append(tool_item)
			elif isinstance(tool_item,dict):
				try:
					if B in tool_item:
						declarations=[]
						for fd_dict in tool_item[B]:
							declaration=self._create_function_declaration_from_dict(fd_dict)
							if declaration:declarations.append(declaration)
						if declarations:prepared_tools.append(Tool(function_declarations=declarations))
					elif'google_search'in tool_item:prepared_tools.append(Tool(google_search=GoogleSearch()))
					elif'url_context'in tool_item:prepared_tools.append(Tool(url_context=UrlContext()))
					else:logger.warning(f"Invalid tool dictionary format: {tool_item}. Skipping.")
				except Exception as e:logger.warning(f"Could not parse tool dictionary {tool_item}: {e}. Skipping.")
			else:logger.warning(f"Invalid tool format encountered: {tool_item}. Skipping.")
		return prepared_tools
	@staticmethod
	def _is_likely_markdown(text_content):
		'Heuristic to determine if a string is likely Markdown.'
		if not isinstance(text_content,str):return _G
		if re.search('^\\s*#{1,6}\\s+',text_content,re.MULTILINE):return _D
		if re.search('^\\s*[\\*\\-\\+]\\s+',text_content,re.MULTILINE):return _D
		if re.search('^\\s*\\d+\\.\\s+',text_content,re.MULTILINE):return _D
		if re.search('\\*\\*.*?\\*\\*|__.*?__',text_content):return _D
		if re.search('`.*?`',text_content):return _D
		if re.search('!?\\[.*?\\]\\(.*?\\)',text_content):return _D
		return _G
	def _get_gemini_response_sync(self,model_name,contents,config):
		'Synchronous call to Gemini/Vertex AI.'
		if not self._genai_client:logger.error(_Bc);return _Bd,[],_A
		try:
			if self._gcp_project_id and self._gcp_region:response=self._genai_client.models.generate_content(contents=contents,model=model_name,config=config)
			else:
				try:model_instance=genai.GenerativeModel(model_name);response=model_instance.generate_content(contents=contents,generation_config=config,tools=config.tools if hasattr(config,_O)and config.tools else _A)
				except Exception as e:logger.error(f"Failed to use direct Gemini API model '{model_name}': {e}",exc_info=_D);return f"Error: AI model '{model_name}' could not be used.",[]
			response_text=_A;function_calls=_A
			if response.candidates and len(response.candidates)>0:
				candidate=response.candidates[0]
				if candidate.content and candidate.content.parts:
					fc_parts=[part.function_call for part in candidate.content.parts if hasattr(part,_Be)and part.function_call]
					if fc_parts:
						function_calls=[]
						for fc in fc_parts:args_dict={key:value for(key,value)in fc.args.items()};function_calls.append({_C:fc.name,_I:args_dict})
					text_parts=[part.text for part in candidate.content.parts if hasattr(part,_P)and part.text]
					if text_parts:response_text=''.join(text_parts)
			if not response_text and not function_calls and hasattr(response,_P)and response.text:response_text=response.text
			return response_text,list(response.candidates)if hasattr(response,_AJ)else[],function_calls
		except Exception as e:logger.error(f"Error getting Gemini response for model {model_name}: {e}",exc_info=_D);return f"There was an error generating this response: {e}",[],_A
	async def _get_gemini_response_async(self,model_name,contents,config):
		'Asynchronous call to Gemini/Vertex AI.'
		if not self._genai_client:logger.error(_Bc);return _Bd,[],_A
		try:
			response=await self._genai_client.aio.models.generate_content(contents=contents,model=model_name,config=config);response_text=_A;function_calls=_A
			if response.candidates and len(response.candidates)>0:
				candidate=response.candidates[0]
				if candidate.content and candidate.content.parts:
					fc_parts=[part.function_call for part in candidate.content.parts if hasattr(part,_Be)and part.function_call]
					if fc_parts:
						function_calls=[]
						for fc in fc_parts:args_dict={key:value for(key,value)in fc.args.items()};function_calls.append({_C:fc.name,_I:args_dict})
					text_parts=[part.text for part in candidate.content.parts if hasattr(part,_P)and part.text]
					if text_parts:response_text=''.join(text_parts)
			if not response_text and not function_calls and hasattr(response,_P)and response.text:response_text=response.text
			return response_text,list(response.candidates)if hasattr(response,_AJ)else[],function_calls
		except google_api_exceptions.PermissionDenied as e:logger.error(f"Permission Denied during Gemini API call. Check IAM roles for the service account. Details: {e}",exc_info=_D);return'Error: Permission denied. Please check service account permissions.',[],_A
		except google_api_exceptions.NotFound as e:logger.error(f"Model or endpoint not found: '{model_name}'. Check model name and region. Details: {e}",exc_info=_D);return f"Error: The model '{model_name}' was not found.",[],_A
		except google_api_exceptions.InvalidArgument as e:logger.error(f"Invalid argument passed to Gemini API. Check contents and config. Details: {e}",exc_info=_D);return'Error: Invalid request sent to the model.',[],_A
		except Exception as e:logger.error(f"An unexpected error occurred in _get_gemini_response_async for model {model_name}: {e}",exc_info=_D);return f"There was an unexpected error generating this response: {e}",[],_A
	async def _get_openai_response_async(self,model_name,messages,prompt_config,tools=_A):
		'Asynchronous call to OpenAI API.'
		if not self._openai_api_key:raise PinionAIConfigurationError('OpenAI API key is not configured.')
		if not AsyncOpenAI:raise PinionAIConfigurationError("OpenAI library is not installed. Please install it with 'pip install openai'.")
		http_client=httpx.AsyncClient();client=AsyncOpenAI(api_key=self._openai_api_key);openai_params={_X:model_name,_A1:messages,_A9:prompt_config.get(_AH),_B3:prompt_config.get(_AK),_Y:prompt_config.get(_Y),'frequency_penalty':prompt_config.get('frequencyPenalty'),'presence_penalty':prompt_config.get('presencePenalty')}
		if prompt_config.get(_i):openai_params[_i]=prompt_config.get(_i)
		if tools:openai_params[_O]=tools;openai_params[_B4]='auto'
		openai_params={k:v for(k,v)in openai_params.items()if v is not _A}
		try:
			response=await client.chat.completions.create(**openai_params);response_message=response.choices[0].message;response_text=response_message.content;function_calls=_A
			if response_message.tool_calls:
				function_calls=[]
				for tool_call in response_message.tool_calls:
					try:arguments=json.loads(tool_call.function.arguments)
					except json.JSONDecodeError:logger.error(f"Failed to decode OpenAI tool arguments: {tool_call.function.arguments}");arguments={}
					function_calls.append({_C:tool_call.function.name,_I:arguments})
			return response_text,function_calls
		except Exception as e:logger.error(f"Error calling OpenAI API for model {model_name}: {e}",exc_info=_D);return f"Error from OpenAI: {e}",_A
	async def _get_anthropic_response_async(self,model_name,system_prompt,messages,prompt_config,tools=_A):
		'Asynchronous call to Anthropic API.';A='tool_use'
		if not self._anthropic_api_key:raise PinionAIConfigurationError('Anthropic API key is not configured.')
		if not AsyncAnthropic:raise PinionAIConfigurationError("Anthropic library is not installed. Please install it with 'pip install anthropic'.")
		client=AsyncAnthropic(api_key=self._anthropic_api_key);anthropic_params={_X:model_name,_A3:system_prompt,_A1:messages,_A9:prompt_config.get(_AH),_B3:prompt_config.get(_AK,4096),_Y:prompt_config.get(_Y),_AI:prompt_config.get(_AI)}
		if tools:anthropic_params[_O]=tools;anthropic_params[_B4]={_F:'auto'}
		anthropic_params={k:v for(k,v)in anthropic_params.items()if v is not _A}
		try:
			response=await client.messages.create(**anthropic_params);response_text=_A;function_calls=_A
			if response.stop_reason==A:
				function_calls=[]
				for content_block in response.content:
					if content_block.type==A:function_calls.append({_C:content_block.name,_I:content_block.input})
			else:
				text_blocks=[block.text for block in response.content if block.type==_P]
				if text_blocks:response_text=''.join(text_blocks)
			return response_text,function_calls
		except Exception as e:logger.error(f"Error calling Anthropic API for model {model_name}: {e}",exc_info=_D);return f"Error from Anthropic: {e}",_A
	async def _get_deepseek_response_async(self,model_name,messages,prompt_config,tools):
		'\n        Get response from a DeepSeek model.\n        ';A='max_output_tokens'
		try:from openai import AsyncOpenAI
		except ImportError:logger.error("OpenAI library not installed. Please install it with 'pip install openai'.");return'Error: OpenAI library not installed.',_A
		api_key=self._get_api_key(_AM)
		if not api_key:logger.error('DeepSeek API key not found.');return'Error: DeepSeek API key not found.',_A
		try:client=AsyncOpenAI(api_key=api_key,base_url='https://api.deepseek.com/v1')
		except Exception as e:logger.error(f"Failed to initialize DeepSeek client: {e}");return f"Error initializing DeepSeek client: {e}",_A
		request_params={_X:model_name,_A1:messages}
		if A in prompt_config:request_params[_B3]=prompt_config[A]
		if _A9 in prompt_config:request_params[_A9]=prompt_config[_A9]
		if _Y in prompt_config:request_params[_Y]=prompt_config[_Y]
		if tools:request_params[_O]=tools;request_params[_B4]='auto'
		try:
			logger.info(f"Sending request to DeepSeek model: {model_name}");response=await client.chat.completions.create(**request_params);response_message=response.choices[0].message;llm_response_text=response_message.content or'';function_calls=_A
			if response_message.tool_calls:
				function_calls=[]
				for tool_call in response_message.tool_calls:
					try:arguments=json.loads(tool_call.function.arguments);function_calls.append({_C:tool_call.function.name,'arguments':arguments})
					except json.JSONDecodeError as e:logger.error(f"Failed to decode function arguments from DeepSeek: {tool_call.function.arguments}. Error: {e}");return f"Error decoding tool arguments from DeepSeek: {e}",_A
			return llm_response_text,function_calls
		except Exception as e:logger.error(f"Error getting response from DeepSeek: {e}");return f"Error from DeepSeek: {e}",_A
	def _extract_function_calls_from_llm_response(self,llm_response):
		'Extracts function calls from a Gemini Function Call response.';function_calls_list=[]
		try:
			if llm_response.candidates and llm_response.candidates[0].content.parts:
				for part in llm_response.candidates[0].content.parts:
					if part.function_call:fc=part.function_call;call_dict={fc.name:dict(fc.args.items())};function_calls_list.append(call_dict)
		except(AttributeError,IndexError):logger.debug('No function calls found in LLM response or response structure unexpected.')
		return function_calls_list
	async def _get_token_api(self,host,client_id,client_secret):
		url='/token';headers={_Q:_K};data={_B5:_Bf,_B6:client_id,_B7:client_secret}
		try:response=await self._http_session.post(url,headers=headers,json=data);response.raise_for_status();auth_response=response.json();return f"{auth_response[_Bg]} {auth_response[_AZ]}"
		except httpx.RequestError as e:raise PinionAIAPIError(f"Network error getting token from {e.request.url}",details=str(e))from e
		except(KeyError,json.JSONDecodeError)as e:raise PinionAIAPIError('Invalid token response',details=str(e))from e
	async def _start_session_api(self,host,agent_id_to_start,token):
		url=f"/agent/{agent_id_to_start}";headers={_B8:_t,_s:_A7,_M:token}
		try:
			response=await self._http_session.get(url,headers=headers);response.raise_for_status();data=response.json();session_uid=data.get(_B,{}).get(_E,{}).get('uid')
			if session_uid:return session_uid,data
			raise PinionAISessionError('Session UID not found in API response.',details=data)
		except httpx.RequestError as e:raise PinionAISessionError(f"Network error starting session from {e.request.url}",details=str(e))from e
		except json.JSONDecodeError as e:raise PinionAISessionError('Invalid JSON response when starting session',details=str(e))from e
	async def _start_version_api(self,host,agent_id_to_start,token,version_str):
		url=f"/version/{agent_id_to_start}/{version_str}";headers={_B8:_t,_s:_A7,_M:token}
		try:
			response=await self._http_session.get(url,headers=headers);response.raise_for_status();data=response.json();session_uid=data.get(_B,{}).get(_E,{}).get('uid')
			if session_uid:return session_uid,data
			raise PinionAISessionError('Session UID not found in versioned API response.',details=data)
		except httpx.RequestError as e:raise PinionAISessionError(f"Network error starting versioned session from {e.request.url}",details=str(e))from e
		except json.JSONDecodeError as e:raise PinionAISessionError(f"Invalid JSON response when starting versioned session from {url}",details=str(e))from e
	async def _get_session_api(self,host,session_uid,token):
		url=f"/session/{session_uid}";headers={_s:_A7,_M:token,_B8:_t}
		try:
			response=await self._http_session.get(url,headers=headers);response.raise_for_status();data=response.json()
			if data.get(_B,{}).get(_E,{}).get('uid')==session_uid:return data
			raise PinionAISessionError('GET Session UID not found in API response.',details=data)
		except httpx.RequestError as e:raise PinionAISessionError(f"Network error getting session from {e.request.url}",details=str(e))from e
		except json.JSONDecodeError as e:raise PinionAISessionError(f"Invalid JSON response when getting session from {url}",details=str(e))from e
	async def _get_session_lastmodified_api(self,host,session_uid,token):
		url=f"/session/{session_uid}/lastmodified";headers={_s:_A7,_M:token}
		try:response=await self._http_session.get(url,headers=headers);response.raise_for_status();data=response.json();last_modified=data.get(_B,{}).get(_E,{}).get('lastmodified');return last_modified,'success'
		except httpx.RequestError as e:raise PinionAISessionError(f"Request error getting last modified in session from {e.request.url}",details=str(e))from e;return _A,e
		except(json.JSONDecodeError,KeyError)as e:raise PinionAISessionError(f"Error parsing lastmodified response from {url}",details=str(e))from e;return _A,e
	async def _post_session_api(self,host,token,session_uid,data_payload,transfer_req,transfer_acc):
		url=f"/session";headers={_Q:_K,_BK:_t,_M:token};full_payload={'sessionUid':session_uid,_B:data_payload,'transferRequested':transfer_req,'transferAccepted':transfer_acc}
		try:
			json_string_payload=json.dumps(full_payload,default=_json_datetime_serializer);compressed_data=gzip.compress(json_string_payload.encode(_N));response=await self._http_session.post(url,headers=headers,content=compressed_data)
			if response.status_code==200:return response,response.json()
			else:logger.warning(f"POST to {url} failed with status {response.status_code}: {response.text}");return response,response.text
		except httpx.RequestError as e:logger.error(f"API POST error for {url}: {e}");return _A,e
		except json.JSONDecodeError as e:logger.error(f"JSON decode error on 200 response from {url}: {e}");return response,e
	async def _get_token_for_connector(self,connector_config):
		'Gets auth token for a given connector configuration.';A='refresh_token';url=connector_config.get(_Z);client_id=connector_config.get(_B2);client_secret=connector_config.get(_n);grant_type=connector_config.get(_m,_Bf);content_type=connector_config.get(_Bh,_K);use_header_payload=connector_config.get('headerPayload',_G);scope=connector_config.get(_AD,_A);refresh_token=connector_config.get('refreshToken',_A)
		if not url or not client_id or not client_secret:logger.warning(f"Connector '{connector_config.get(_C)}' is missing URL, clientId, or clientSecret.");return
		headers={};data_to_send:0
		if use_header_payload:client_keys=f"{client_id}:{client_secret}";client_keys_b64=base64.b64encode(client_keys.encode()).decode();headers[_M]=f"Basic {client_keys_b64}";headers[_Q]='application/x-www-form-urlencoded';data_to_send=f"grant_type={grant_type}"
		else:
			headers[_Q]=content_type
			if _A8 in content_type.lower():
				data_to_send={_B5:grant_type,_B6:client_id,_B7:client_secret}
				if refresh_token:data_to_send[A]=refresh_token
				if scope:data_to_send[_AD]=scope
			elif'x-www-form-urlencoded'in content_type.lower():
				form_data=[(_B5,grant_type),(_B6,client_id),(_B7,client_secret)]
				if refresh_token:form_data.append((A,refresh_token))
				if scope:form_data.append((_AD,scope))
				data_to_send='&'.join([f"{k}={quote(str(v))}"for(k,v)in form_data])
			else:logger.warning(f"Unsupported content type for connector token request: {content_type}");return
		try:
			payload=json.dumps(data_to_send)if isinstance(data_to_send,dict)else data_to_send
			async with httpx.AsyncClient()as client:response=await client.post(url,headers=headers,content=payload);response.raise_for_status();auth_response=response.json();token_type=auth_response.get(_Bg,'Bearer').capitalize();return f"{token_type} {auth_response[_AZ]}"
		except httpx.RequestError as e:logger.error(f"Failed to obtain grant token for connector '{connector_config.get(_C)}' from {url}: {e}");raise PinionAIAPIError(f"Network error getting token for connector '{connector_config.get(_C)}'",details=str(e))from e
		except(KeyError,json.JSONDecodeError)as e:logger.error(f"Error parsing token response for connector '{connector_config.get(_C)}' from {url}: {e}");raise PinionAIAPIError(f"Invalid token response for connector '{connector_config.get(_C)}'",details=str(e))from e
	async def _generic_api_post_put(self,current_var,api_config,headers,method):
		'Handles generic POST/PUT API calls.';url_template=self._clean_line(api_config.get(_Z,''));url=self._evaluate_f_string(url_template,current_var)
		if not url:logger.error(f"URL could not be evaluated for API '{api_config.get(_C)}'. Template: {url_template}");return current_var,_A,_A,_Bi
		raw_body_template=api_config.get(_W,'');final_data_bytes=_A;content_type=headers.get(_Q,'').lower()
		try:
			if _K in content_type and raw_body_template.strip():parsable_template=raw_body_template.replace('["',"['").replace('"]',"']");json_structure_template=json.loads(parsable_template);evaluated_structure=self._evaluate_vars_in_structure(json_structure_template,current_var);final_data_bytes=json.dumps(evaluated_structure).encode(_N)
			elif raw_body_template.strip():evaluated_string=self._evaluate_f_string(raw_body_template,current_var);final_data_bytes=evaluated_string.encode(_N)
			else:final_data_bytes=b''
		except json.JSONDecodeError as e:logger.error(f"Invalid JSON in API body template for '{api_config.get(_C)}': {raw_body_template}. Error: {e}");return current_var,_A,_A,f"Invalid JSON in API body: {e}"
		except Exception as e:logger.error(f"Error processing body for API '{api_config.get(_C)}': {e}. Template: '{raw_body_template}'");return current_var,_A,_A,f"Error processing API body: {e}"
		if final_data_bytes is _A:return current_var,_A,_A,'Error: API body could not be prepared.'
		logger.debug(f"API {method} Request URL: {url}");logger.debug(f"API {method} Request Headers: {headers}");logger.debug(f"API {method} Request Body: {final_data_bytes.decode(_N)if final_data_bytes else'None'}")
		try:
			async with httpx.AsyncClient()as client:
				if method=='POST':response=await client.post(url,headers=headers,content=final_data_bytes,timeout=120)
				elif method=='PUT':response=await client.put(url,headers=headers,content=final_data_bytes,timeout=120)
				else:return current_var,_A,_A,f"Unsupported method {method} in _generic_api_post_put"
			parsed_response:0
			try:parsed_response=response.json()
			except json.JSONDecodeError:parsed_response=response.text
			if api_config.get(_a):current_var[api_config[_a]]=parsed_response
			final_response_message=_A
			if response.status_code>=400 or not parsed_response:
				logger.warning(f"API {method} to {url} failed with status {response.status_code}: {parsed_response}")
				if api_config.get(_AT):final_response_message=self._evaluate_f_string(api_config[_AT],current_var)
			return current_var,response,parsed_response,final_response_message
		except httpx.RequestError as e:status_code=e.response.status_code if hasattr(e,_AR)and e.response else _A;error_detail=e.response.text if hasattr(e,_AR)and e.response else str(e);raise PinionAIAPIError(f"API {method} request to {url} failed: {error_detail}",status_code=status_code,details=str(e))from e
	async def _generic_api_get(self,current_var,api_config,headers):
		'Handles generic GET API calls.';url_template=self._clean_line(api_config.get(_Z,''));url=self._evaluate_f_string(url_template,current_var)
		if not url:logger.error(f"URL could not be evaluated for API GET '{api_config.get(_C)}'. Template: {url_template}");return current_var,_A,_A,_Bi
		logger.debug(f"API GET Request URL: {url}");logger.debug(f"API GET Request Headers: {headers}")
		try:
			async with httpx.AsyncClient()as client:response=await client.get(url,headers=headers,timeout=120)
			parsed_response:0
			try:parsed_response=response.json()
			except json.JSONDecodeError:parsed_response=response.text
			if api_config.get(_a):current_var[api_config[_a]]=parsed_response
			final_response_message=_A
			if response.status_code>=400:
				logger.warning(f"API GET to {url} failed with status {response.status_code}: {parsed_response}")
				if api_config.get(_AT):final_response_message=self._evaluate_f_string(api_config[_AT],current_var)
			return current_var,response,parsed_response,final_response_message
		except httpx.RequestError as e:error_detail=e.response.text if hasattr(e,_AR)and e.response else str(e);raise PinionAIAPIError(f"API GET request to {url} failed: {error_detail}")from e
	async def _get_journey_token(self,current_var,user_input=_A):
		'Gets or refreshes Journey client credentials token.'
		if self._journey_bearer_token:return self._journey_bearer_token
		journey_connector=current_var.get('journey_connector_name','')
		if journey_connector:
			connector_config=self._get_connector_details(journey_connector)
			if connector_config:
				try:
					token=await self._get_token_for_connector(connector_config)
					if token:self._journey_bearer_token=token;return self._journey_bearer_token
				except PinionAIAPIError as e:logger.warning(f"Could not get token for connector '{journey_connector}': {e}. Proceeding without token.")
			else:logger.warning(f"Connector '{journey_connector}' not found.")
	async def _journey_lookup(self,unique_id_val,current_var,user_input=_A):
		'Performs a Journey customer lookup.';A='enrollments';account_id=current_var.get('journey_accountId');bearer_token=await self._get_journey_token(current_var)
		if not account_id or not bearer_token:return _A,_G,'error_config'
		headers={_AU:_K,_M:bearer_token};url=f"https://app.journeyid.io/api/system/customers/lookup?account_id={account_id}&unique_id={unique_id_val}"
		try:
			response=await self._http_session.get(url,headers=headers,timeout=60);response.raise_for_status();lookup_data=response.json();logger.debug(f"Journey lookup response: {json.dumps(lookup_data,indent=2)}");customer_id=lookup_data.get('id');enrolled=_G
			if customer_id and lookup_data.get(A):
				for enrollment in lookup_data[A]:
					if enrollment.get(_F)=='webauthn':enrolled=_D;break
			return customer_id,enrolled,'found'if customer_id else'empty'
		except httpx.HTTPStatusError as e:logger.error(f"Journey lookup failed with status {e.response.status_code} for unique_id {unique_id_val}. Response: {e.response.text}")
		except httpx.RequestError as e:logger.error(f"Journey lookup error for unique_id {unique_id_val}: {e}")
		except(json.JSONDecodeError,KeyError)as e:logger.error(f"Error parsing Journey lookup response for {unique_id_val}: {e}")
		return _A,_G,'error_request'
	async def _journey_send_pipeline(self,current_var,json_payload,delivery_method,user_input=_A):
		'Sends a pipeline execution request to Journey.';bearer_token=await self._get_journey_token(current_var)
		if not bearer_token:return _A,_B9
		post_url='https://app.journeyid.io/api/system/executions';headers={_s:_K,_Q:_K,_M:bearer_token}
		try:
			async with httpx.AsyncClient()as client:response=await client.post(post_url,headers=headers,content=json.dumps(json_payload),timeout=120)
			response_data=response.json()
			if 200<=response.status_code<300:
				if delivery_method==_Z:
					execution_url=response_data.get(_Z);execution_id=response_data.get('id')
					if execution_url and execution_id:return execution_id,execution_url,''
					else:return _A,_A,'Execution URL or ID not found in successful Journey response.'
				else:
					execution_id=response_data.get('id')
					if execution_id:return execution_id,_A,''
					else:return _A,_A,'ExecutionId not found in successful Journey response.'
			else:
				error_msg=response_data.get(_V,response.text)
				if'Token is expired'in str(error_msg):self._journey_bearer_token=_A;return _A,_A,'Your Journey session has expired. Please try again.'
				logger.warning(f"Journey send_pipeline failed ({response.status_code}): {error_msg}");return _A,_A,f"Journey pipeline error: {error_msg} {response.text}"
		except httpx.RequestError as e:logger.error(f"Journey send_pipeline request error: {e}");return _A,_A,'Error sending request to Journey.'
		except json.JSONDecodeError as e:logger.error(f"Error parsing Journey send_pipeline response: {e}");return _A,_A,'Error processing Journey response.'
	async def _journey_execution_status_check(self,execution_id,current_var,max_retries=12,delay_seconds=5,user_input=_A):
		'Checks the status of a Journey execution.';bearer_token=await self._get_journey_token(current_var)
		if not bearer_token:return _G,_B9
		url=f"https://app.journeyid.io/api/system/executions/{execution_id}";headers={_AU:_K,_M:bearer_token}
		for attempt in range(max_retries):
			try:
				async with httpx.AsyncClient()as client:response=await client.get(url,headers=headers,timeout=30)
				response.raise_for_status();status_data=response.json()
				if status_data.get(_Bj):return _D,status_data.get('outcome',{}).get(_k,'Task completed successfully.')
			except httpx.RequestError as e:logger.warning(f"Journey execution status check attempt {attempt+1} failed for {execution_id}: {e}")
			except(json.JSONDecodeError,KeyError)as e:logger.warning(f"Error parsing Journey execution status for {execution_id}: {e}")
			if attempt<max_retries-1:time.sleep(delay_seconds)
		return _G,'The Journey task was not completed in the allotted time or an error occurred.'
	async def _journey_session_pipeline_status_check(self,session_id_val,current_var,pipeline_key_to_check,max_retries=12,delay_seconds=5,user_input=_A):
		'Checks pipeline status within a Journey session.';A='pipeline';bearer_token=await self._get_journey_token(current_var)
		if not bearer_token:return _G,_B9
		url=f"https://app.journeyid.io/api/system/sessions/lookup?external_ref={session_id_val}";headers={_AU:_K,_M:bearer_token}
		for attempt in range(max_retries):
			try:
				async with httpx.AsyncClient()as client:response=await client.get(url,headers=headers,timeout=30)
				response.raise_for_status();session_lookup_data=response.json();executions=session_lookup_data.get('executions',[])
				for exec_item in executions:
					if exec_item.get(A,{}).get('key')==pipeline_key_to_check or exec_item.get(A,{}).get('id')==pipeline_key_to_check:
						if exec_item.get(_Bj):return _D,exec_item.get('outcome',{}).get(_k,'Pipeline completed.')
						break
			except httpx.RequestError as e:logger.warning(f"Journey session pipeline status check attempt {attempt+1} failed for session {session_id_val}, pipeline {pipeline_key_to_check}: {e}")
			except(json.JSONDecodeError,KeyError)as e:logger.warning(f"Error parsing Journey session pipeline status for {session_id_val}: {e}")
			if attempt<max_retries-1:time.sleep(delay_seconds)
		return _G,'The Journey pipeline action was not completed or timed out.'
	@staticmethod
	def _generate_uid():return str(uuid.uuid4())
	@staticmethod
	def _generate_secret(length=32):return secrets.token_urlsafe(length)
	@staticmethod
	def _generate_otp():return secrets.randbelow(900000)+100000
	@staticmethod
	def _hash_value(value):
		if value is _A:return 0
		hash_object=hashlib.sha256(value.encode());hash_hex=hash_object.hexdigest();return int(hash_hex,16)
	@staticmethod
	def _is_empty(value):
		if value is _A:return _D
		if isinstance(value,str)and not value.strip():return _D
		if hasattr(value,'__len__')and len(value)==0:return _D
		return _G
	@staticmethod
	def _get(obj,path,default=_A):
		keys=path.split('.');current=obj
		for key in keys:
			try:
				if isinstance(current,list)and key.isdigit():current=current[int(key)]
				elif isinstance(current,dict):current=current[key]
				else:return default
			except(KeyError,TypeError,IndexError):return default
		return current
	@staticmethod
	def _generate_password(length=12):
		if length<4:length=4
		digits_chars='0123456789';locase_chars='abcdefghijklmnopqrstuvwxyz';upcase_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ';symbols_chars='$%?!';combined_list=list(digits_chars+locase_chars+upcase_chars+symbols_chars);password_chars=[random.choice(digits_chars),random.choice(locase_chars),random.choice(upcase_chars),random.choice(symbols_chars)]
		for _ in range(length-4):password_chars.append(random.choice(combined_list))
		random.shuffle(password_chars);return''.join(password_chars)
	async def _encrypt_value(self,data):
		'Method that encrypts a field before sending it to the API.';A='sensitive_info';payload=data.copy()
		if A in payload:original_value=payload[A];encrypted_value=self._encryption_manager.encrypt(original_value);payload[A]=encrypted_value
		return payload
	async def _decrypt_value(self,response_payload):
		'Method that decrypts a field from an API response.';A='encrypted_data';processed_data=response_payload.copy()
		if A in processed_data:encrypted_value=processed_data[A];decrypted_value=self._encryption_manager.decrypt(encrypted_value);processed_data['decrypted_data']=decrypted_value;del processed_data[A]
		return processed_data
	async def _twilio_sms_message(self,sms_body,to_phone,from_phone_twilio=_A):
		if not self._twilio_account_sid or not self._twilio_auth_token:logger.error('Twilio credentials not configured. Cannot send SMS.');return
		_national_digits,_unique_id,to_phone_e164=format_phone(to_phone);twilio_from_number=from_phone_twilio or self._twilio_number
		if not twilio_from_number:logger.error(_Bk);return
		try:twilio_client=TwilioClient(self._twilio_account_sid,self._twilio_auth_token);message=await asyncio.to_thread(twilio_client.messages.create,body=sms_body,from_=twilio_from_number,to=to_phone_e164);logger.info(f"Twilio SMS sent via client. SID: {message.sid}")
		except Exception as e:logger.error(f"Error sending Twilio SMS via client to {to_phone_e164}: {e}")
	async def _sendgrid_email(self,plain_text_body,html_body,to_email,subject,from_email_addr=_A,cc_address=_A,bcc_address=_A,reply_to_address=_A):
		if not self._email_api_key:logger.error('Email API key not configured. Cannot send email.');return
		actual_from_email=from_email_addr or self._email_from_address
		if not actual_from_email:logger.error("Email 'from' address not configured. Cannot send email.");return
		p=Personalization()
		if to_email:
			to_address_list=to_email.split(_T)
			for addr in to_address_list:p.add_to(To(addr.strip()))
		if cc_address:
			cc_address_list=cc_address.split(_T)
			for addr in cc_address_list:p.add_cc(Cc(addr.strip()))
		if bcc_address:
			bcc_address_list=bcc_address.split(_T)
			for addr in bcc_address_list:p.add_bcc(Bcc(addr.strip()))
		if reply_to_address:
			reply_to_list=reply_to.split(_T)
			for addr in reply_to_list:p.add_reply_to(ReplyTo(addr.strip()))
		try:sg=sendgrid.SendGridAPIClient(self._email_api_key);message=Mail(from_email=From(actual_from_email),subject=subject,plain_text_content=plain_text_body,html_content=html_body);message.add_personalization(p);response=await asyncio.to_thread(sg.send,message)
		except Exception as e:logger.error(f"Error sending email to {to_email} via SendGrid: {e}")
	async def _infobip_send_email(self,plain_text_body,html_body_content,to_address,subject,from_address=_A,token=_A,cc_address=_A,bcc_address=_A,reply_to_address=_A):
		'Sends an email using the Infobip API.'
		if not token:logger.error('Infobip token not provided. Cannot send email.');return
		infobip_url='https://g9egk8.api.infobip.com/email/4/messages';headers={_M:token,_Q:_K,_AU:_K};payload={_A1:[{'sender':from_address,'destinations':[{'to':[{'destination':to_address}]}],_R:{_AS:subject,_P:plain_text_body,'html':html_body_content}}]}
		try:
			async with httpx.AsyncClient()as client:response=await client.post(infobip_url,headers=headers,json=payload);response.raise_for_status();logger.info(f"Email sent to {to_address} via Infobip. Response: {response.text}")
		except httpx.HTTPStatusError as http_err:logger.error(f"HTTP error occurred sending email via Infobip: {http_err} - {http_err.response.text}")
		except Exception as e:logger.error(f"An unexpected error occurred sending email via Infobip: {e}")
	async def _ms_graph_send_email(self,plain_text_body,html_body_content,to_address,subject,from_address=_A,token=_A,cc_address=_A,bcc_address=_A,reply_to_address=_A):
		'Sends an email using the Microsoft Graph API.';B='address';A='emailAddress'
		if not token:logger.error('Microsoft Graph API token not provided. Cannot send email.');return
		if not from_address:logger.error("Microsoft Graph API 'from' address not provided. Cannot send email.");return
		graph_api_endpoint='https://graph.microsoft.com/v1.0';url=f"{graph_api_endpoint}/users/{from_address}/sendMail";headers={_M:token,_Q:_K};email_payload={_k:{_AS:subject,_W:{_Bh:'HTML',_R:html_body_content}},'saveToSentItems':'true'}
		if to_address:to_address_list=to_address.split(_T);email_payload[_k]['toRecipients']=[{A:{B:addr.strip()}}for addr in to_address_list]
		if cc_address:cc_address_list=cc_address.split(_T);email_payload[_k]['ccRecipients']=[{A:{B:addr.strip()}}for addr in cc_address_list]
		if bcc_address:bcc_address_list=bcc_address.split(_T);email_payload[_k]['bccRecipients']=[{A:{B:addr.strip()}}for addr in bcc_address_list]
		if reply_to_address:reply_to_list=reply_to.split(_T);email_payload[_k]['replyTo']=[{A:{B:addr.strip()}}for addr in reply_to_list]
		try:
			async with httpx.AsyncClient()as client:response=await client.post(url,headers=headers,json=email_payload);response.raise_for_status();logger.info(f"Email sent to {to_address} via Microsoft Graph API. Response status: {response.status_code}")
		except httpx.HTTPStatusError as http_err:logger.error(f"HTTP error occurred sending email via Microsoft Graph API: {http_err} - {http_err.response.text}")
		except Exception as e:logger.error(f"An unexpected error occurred sending email via Microsoft Graph API: {e}")
	async def _gmail_send_email(self,plain_text_body,html_body_content,to_address,subject,from_address=_A,token=_A,cc_address=_A,bcc_address=_A,reply_to_address=_A):
		'\n        Sends an email using the Gmail API via raw REST HTTP requests.\n        This mirrors the implementation style of the MS Graph function.\n        '
		if not token:logger.error('Gmail API token not provided. Cannot send email.');return
		message=MIMEMultipart('alternative');message['to']=to_address;message[_AS]=subject
		if from_address:message['from']=from_address
		if cc_address:message['cc']=cc_address
		if bcc_address:message['bcc']=bcc_address
		if reply_to_address:message['reply-to']=reply_to_address
		part1=MIMEText(plain_text_body,'plain');part2=MIMEText(html_body_content,'html');message.attach(part1);message.attach(part2);raw_message=base64.urlsafe_b64encode(message.as_bytes()).decode(_N);url='https://gmail.googleapis.com/gmail/v1/users/me/messages/send';headers={_M:token,_Q:_K};payload={'raw':raw_message}
		try:
			async with httpx.AsyncClient()as client:response=await client.post(url,headers=headers,json=payload);response.raise_for_status();data=response.json();logger.info(f"Email sent to {to_address} via Gmail API. Message ID: {data.get('id')}")
		except httpx.HTTPStatusError as http_err:logger.error(f"HTTP error occurred sending email via Gmail API: {http_err} - {http_err.response.text}")
		except Exception as e:logger.error(f"An unexpected error occurred sending email via Gmail API: {e}")
	@staticmethod
	def _clean_line(text):
		if not text:return''
		return text.strip('\n')
	@staticmethod
	def _clean_text(text):
		if not text:return''
		return text.replace('\n','').replace('\r','').replace('\t','')
	def _evaluate_vars_in_structure(self,data_structure,context_vars,user_input=_A):
		'\n        Recursively traverses a dict or list, evaluating string templates like f"var[\'key\']".\n        Uses a provided context_vars for evaluation, not necessarily self.var.\n        ';D='context_vars';C='current_var';B='{current_var[';A='{var['
		if isinstance(data_structure,dict):
			for(key,value)in list(data_structure.items()):
				if isinstance(value,str):
					if A in value or B in value:
						try:eval_globals={_A0:context_vars,C:context_vars,D:context_vars,_BA:user_input};data_structure[key]=eval(f"f'''{value}'''",eval_globals,{})
						except Exception as e:logger.warning(f"Could not evaluate template for key '{key}': '{value}'. Error: {e}")
				elif isinstance(value,(dict,list)):self._evaluate_vars_in_structure(value,context_vars,user_input)
		elif isinstance(data_structure,list):
			for(i,item)in enumerate(data_structure):
				if isinstance(item,str):
					if A in item or B in item or user_input is not _A and'{user_input}'in item:
						try:eval_globals={_A0:context_vars,C:context_vars,D:context_vars,_BA:user_input};data_structure[i]=eval(f"f'''{item}'''",eval_globals,{})
						except Exception as e:logger.warning(f"Could not evaluate template in list item: '{item}'. Error: {e}")
				elif isinstance(item,(dict,list)):self._evaluate_vars_in_structure(item,context_vars,user_input)
		return data_structure
	def _evaluate_f_string(self,template_string,context_vars,user_input=_A):
		'Safely evaluates an f-string like template using provided context variables.'
		try:eval_namespace={_A0:context_vars,_BA:user_input or''};return eval(f"f'''{template_string}'''",eval_namespace,{})
		except Exception as e:logger.error(f"Error evaluating f-string template: '{template_string}'. Error: {e}");return template_string
	def _create_function_declaration_from_dict(self,declaration_dict):
		"\n        Safely creates a FunctionDeclaration object from a dictionary.\n\n        This function takes a dictionary that mirrors the structure of a JSON\n        function declaration and converts it into a valid FunctionDeclaration\n        object that can be used with the Vertex AI SDK.\n\n        Args:\n            declaration_dict: A dictionary with 'name', 'description', and\n                              'parameters' keys.\n\n        Returns:\n            A FunctionDeclaration object if the input is valid, otherwise None.\n        "
		if not isinstance(declaration_dict,dict):logger.error('Input must be a dictionary to create a FunctionDeclaration.');return
		name=declaration_dict.get(_C);description=declaration_dict.get(_L);parameters=declaration_dict.get(_AV)
		if not all([name,description,isinstance(parameters,dict)]):logger.error(f"The provided dictionary is missing required keys ('name', 'description') or 'parameters' is not a dictionary. Got: {declaration_dict}");return
		try:return FunctionDeclaration(name=name,description=description,parameters=parameters)
		except Exception as e:logger.error(f"Failed to instantiate FunctionDeclaration from dict {declaration_dict}: {e}");return
	def _translate_tools_for_provider(self,provider,direct_tool_configs,processed_fd_dicts):
		'Translates internal tool configuration to a model provider-specific format.'
		if not processed_fd_dicts:return
		translated_tools=[]
		if provider==_j:
			for fd in processed_fd_dicts:translated_tools.append({_F:_Az,_Az:{_C:fd.get(_C),_L:fd.get(_L),_AV:fd.get(_AV)}})
		elif provider==_A2:
			for fd in processed_fd_dicts:translated_tools.append({_C:fd.get(_C),_L:fd.get(_L),'input_schema':fd.get(_AV)})
		return translated_tools if translated_tools else _A
	def get_chat_messages_for_display(self):'Returns chat messages, suitable for display by an application.';return self.chat_messages
	def add_message_to_history(self,role,content):'Adds a message to the internal chat history.';self.chat_messages.append({_S:role,_R:content})
	@property
	def session_id(self):return self._session_id
	@property
	def current_var_data(self):return self.var.copy()
	def __repr__(self):return f"<PinionAIClient(agent_id='{self._agent_id}', session_id='{self._session_id}', host='{self._host_url}')>"
def format_phone(number_str):
	'\n    Formats a phone number to a consistent E.164 format.\n\n    This is a standalone utility function.\n\n    Args:\n        number_str: The phone number as a string.\n\n    Returns:\n        A tuple containing (national_digits, unique_id, e164_format).\n    ';A='1'
	if not isinstance(number_str,str):number_str=str(number_str)
	digits=re.sub('[^0-9]','',number_str)
	if digits.startswith(A)and len(digits)==11:0
	elif len(digits)==10:
		is_likely_us_short=_D
		if 650<=int(digits[0:3])<=659 and int(digits[0:3])!=657:is_likely_us_short=_G
		if is_likely_us_short:digits=f"1{digits}"
	unique_id=digits;phone_number_e164=f"+{digits}";national_digits=digits.removeprefix(A)if digits.startswith(A)and len(digits)>10 else digits;return national_digits,unique_id,phone_number_e164
def twilio_sms_message(sms_body,to_phone,from_phone_twilio=_A):
	'Sends an SMS using Twilio, reading credentials from environment variables.';twilio_account_sid=os.environ.get(_AW);twilio_auth_token=os.environ.get(_AX)
	if not twilio_account_sid or not twilio_auth_token:logger.error('Twilio credentials not configured in environment. Cannot send SMS.');return
	_national_digits,_unique_id,to_phone_e164=format_phone(to_phone);twilio_from_number=from_phone_twilio or os.environ.get(_AY)
	if not twilio_from_number:logger.error(_Bk);return
	try:client=Client(twilio_account_sid,twilio_auth_token);message=client.messages.create(body=sms_body,from_=twilio_from_number,to=to_phone_e164);logger.info(f"Twilio SMS sent. SID: {message.sid}")
	except Exception as e:logger.error(f"Error sending Twilio SMS to {to_phone_e164}: {e}")