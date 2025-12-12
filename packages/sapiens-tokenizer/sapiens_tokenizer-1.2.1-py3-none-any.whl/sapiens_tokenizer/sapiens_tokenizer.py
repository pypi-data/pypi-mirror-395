# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
# algorithm specialized in text tokenization in gpt and sapi standards
class SapiensTokenizer:
	def __init__(self):
		from urllib.request import urlopen
		from os.path import isfile
		from string import punctuation, digits
		from json import loads, dump
		from ast import literal_eval
		from os.path import dirname, abspath
		from tiktoken import encoding_for_model
		self.__possible_encoders = ('gpt2', 'gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo', 'text-davinci-001', 'text-davinci-002', 'text-davinci-003')
		self.__urlopen = urlopen
		self.__isfile = isfile
		self.__punctuation = punctuation
		self.__digits = digits
		self.__loads = loads
		self.__literal_eval = literal_eval
		self.__dump = dump
		self.__dirname = dirname
		self.__abspath = abspath
		self.__encoding_for_model = encoding_for_model
		self.vocabulary_size = 0
		self.token_to_index = {}
		self.index_to_token = {}
		self.encode = None
		self.decode = None
		self.pattern = ''
	def __validate_encoder_gpt(self, encoder='gpt-4'):
		if encoder not in self.__possible_encoders:
			encoder = 'gpt2'
			if encoder.startswith('gpt'):
				if '3' in encoder: encoder = 'gpt-3.5-turbo'
				elif '4' in encoder and 'turbo' in encoder: encoder = 'gpt-4-turbo'
				elif '4' in encoder: encoder = 'gpt-4'
			elif 'davinci' in encoder:
				encoder = 'text-davinci-003'
				if '1' in encoder: encoder = 'text-davinci-001'
				elif '2' in encoder: encoder = 'text-davinci-002'
		return encoder
	def __validate_encoder_sapi(self, encoder='sapi-4'):
		if not encoder.startswith('sapi'): return self.__validate_encoder_gpt(encoder=encoder)
		if '0' in encoder: encoder = 'sapi-0'
		elif '1' in encoder: encoder = 'sapi-1'
		elif '2' in encoder: encoder = 'sapi-2'
		elif '3' in encoder: encoder = 'sapi-3'
		elif '4' in encoder: encoder = 'sapi-4'
		else: encoder = 'sapi-5'
		return encoder
	def __is_web(self, file_path=''): return str(file_path).lower().strip().startswith(('http://', 'https://', 'www.'))
	def __validate_encoder_general(self, encoder='sapi-4'):
		encoder = str(encoder).lower().strip()
		if 'sapi' in encoder or 'sapi' in self.pattern:
			if not encoder: encoder = self.pattern
			encoder = self.__validate_encoder_sapi(encoder=encoder)
		else:
			if not encoder: encoder = 'gpt-4'
			self.pattern = encoder
			encoder = self.__validate_encoder_gpt(encoder=encoder)
		return encoder
	def __read_txt(self, file_path='', strip=False):
		file_text = ''
		file_path = str(file_path).strip()
		if self.__is_web(file_path=file_path):
			try:
				from os import environ
				from certifi import where
				environ['SSL_CERT_FILE'] = where()
				from logging import getLogger, ERROR
				getLogger('urlopen').setLevel(ERROR)
			except: pass
			try:
				connection = self.__urlopen(file_path)
				file_text = connection.read().decode('utf-8')
			except: file_text = ''
		if not file_text and file_path and self.__isfile(file_path):
			with open(file_path, 'r', encoding='utf-8') as text_file: file_text = rf'{text_file.read()}'
		return file_text.strip() if strip else file_text
	def __text_to_list(self, text='', tokens_length=1, is_sorted=True):
	    tokens_list = []
	    index = 0
	    while index < len(text):
	        if text[index] in self.__punctuation or text[index] in self.__digits or not text[index].isalnum():
	            tokens_list.append(text[index])
	            index += 1
	        else:
	            count, substring = 0, ''
	            while index < len(text) and count < tokens_length and not (text[index] in self.__punctuation or text[index] in self.__digits or not text[index].isalnum()):
	                substring += text[index]
	                count += 1
	                index += 1
	            tokens_list.append(substring)
	    tokens_list = sorted(list(set(tokens_list))) if is_sorted else tokens_list
	    return tokens_list
	def __text_to_list_sapi5(self, text='', tokens_length=None, is_sorted=True):
	    tokens_list = []
	    index = 0
	    while index < len(text):
	        if text[index] in self.__punctuation or text[index] in self.__digits or not text[index].isalnum():
	            tokens_list.append(text[index])
	            index += 1
	        else:
	            token = ''
	            while index < len(text) and (text[index].isalnum() or text[index] in 'áéíóúýàèìòùỳâêîôûãõñçäëïöüÿåæœÁÉÍÓÚÝÀÈÌÒÙỲÂÊÎÔÛÃÕÑÇÄËÏÖÜŸÅÆŒ'):
	                token += text[index]
	                index += 1
	            tokens_list.append(token)
	    tokens_list = sorted(list(set(tokens_list))) if is_sorted else tokens_list
	    return tokens_list
	def __load_json(self, string_content=''):
		json_content = {}
		string_content = str(string_content)
		try: json_content = self.__loads(string_content)
		except: json_content = self.__literal_eval(string_content)
		return json_content
	def __adjustment_embedding(self, embedding=[], length=None, pattern=''):
		if not embedding or length is None: return embedding
		pattern = self.__validate_encoder_general(encoder=pattern)
		embedding_length = len(embedding)
		if embedding_length > length: embedding = embedding[:length]
		elif embedding_length < length:
			if pattern.startswith('sapi'):
				if not self.encode: self.set_default_sapi_0()
				encode = self.encode
			else: encode = self.get_encode(pattern=pattern)
			scape = '\t ' if 'gpt' in pattern and ('3' in pattern or '4' in pattern) else None
			if not scape and 'davinci' in pattern and '3' in pattern: scape = '\t'
			embedding += encode(rf'{scape}' if scape is not None else chr(32))*(length-embedding_length)
			embedding_length = len(embedding)
			if embedding_length < length and embedding_length > 0: embedding += [embedding[-1]]*(length-embedding_length)
		return embedding
	def sapi_structure_processing(self, file_path='', text_data='', pattern='sapi-5', only_token_to_index=False, only_index_to_token=False):
		try:
			file_path = str(file_path).strip()
			text_data = rf'{text_data}'.strip()
			pattern = self.__validate_encoder_general(encoder=pattern)
			only_token_to_index = bool(only_token_to_index) if type(only_token_to_index) in (bool, int, float) else False
			only_index_to_token = bool(only_index_to_token) if type(only_index_to_token) in (bool, int, float) else False
			if file_path:
				text = self.__read_txt(file_path=file_path, strip=True)
				if text: text_data += '\n\n'+text
			text_data, tokens_length = text_data.strip(), 1
			if not text_data: return False
			if pattern == 'sapi-0': tokens_length = 1
			elif pattern == 'sapi-1': tokens_length = 2
			elif pattern == 'sapi-2': tokens_length = 3
			elif pattern == 'sapi-3': tokens_length = 4
			elif pattern == 'sapi-4': tokens_length = 5
			elif pattern == 'sapi-5': tokens_length = 0
			if tokens_length >= 1: text_to_list = self.__text_to_list
			else: text_to_list = self.__text_to_list_sapi5
			tokens = text_to_list(text=text_data, tokens_length=tokens_length)
			self.vocabulary_size = len(tokens)
			self.token_to_index = {} if only_index_to_token else {token: index for index, token in enumerate(tokens)}
			self.index_to_token = {} if only_token_to_index else {str(index): token for index, token in enumerate(tokens)}
			if pattern != 'sapi-0': self.encode = lambda strings: [self.token_to_index[token] for token in text_to_list(text=strings, tokens_length=tokens_length, is_sorted=False)]
			else: self.encode = lambda strings: [self.token_to_index[token] for token in strings]
			self.decode = lambda indexes: ''.join([self.index_to_token[str(index)] for index in indexes])
			self.pattern = pattern
			return True
		except Exception as error:
			print('ERROR in SapiensTokenizer.sapi_structure_processing: ' + str(error))
			return False
	def key_to_value(self, dictionary={}):
		try: return {value: key for key, value in dictionary.items()}
		except Exception as error:
			print('ERROR in SapiensTokenizer.key_to_value: ' + str(error))
			return dictionary
	def save_vocabulary(self, file_path=''):
		try:
			file_path = str(file_path).strip()
			if not file_path: file_path = 'vocabulary.json'
			if not file_path.endswith('.json'): file_path += '.json'
			vocabulary = {'vocabulary_size': self.vocabulary_size, 'pattern': self.pattern, 'token_to_index': self.token_to_index, 'index_to_token': self.index_to_token}
			with open(file_path, 'w', encoding='utf-8') as json_data: self.__dump(vocabulary, json_data, ensure_ascii=False)
			return True
		except Exception as error:
			print('ERROR in SapiensTokenizer.save_vocabulary: ' + str(error))
			return False
	def load_vocabulary(self, file_path=''):
		try:
			file_path = str(file_path).strip()
			if not file_path:
				if '__file__' in locals() or '__file__' in globals(): directory_path = self.__dirname(self.__abspath(__file__))
				else: directory_path = ''
				if chr(92) in directory_path and directory_path[-1] != chr(92): directory_path += chr(92)
				elif '/' in directory_path and directory_path[-1] != '/': directory_path += '/'
				file_path = directory_path+'vocabulary.json'
			if not file_path.endswith('.json'): file_path += '.json'
			if file_path and self.__is_web(file_path=file_path):
				json_data = self.__read_txt(file_path=file_path, strip=False)
				json_content = self.__load_json(string_content=json_data)
			else:
				if not file_path or not self.__isfile(file_path):
					if not file_path: file_path = './'
					print(f'The file {file_path} was not found.')
					return False
				with open(file_path, 'r', encoding='utf-8') as json_data: json_content = self.__load_json(string_content=json_data.read())
			self.vocabulary_size = int(json_content.get('vocabulary_size', 0))
			self.token_to_index = dict(json_content.get('token_to_index', {}))
			self.index_to_token = dict(json_content.get('index_to_token', {}))
			self.pattern = str(json_content.get('pattern', 'sapi-5')).lower().strip()
			if not self.token_to_index and self.index_to_token: self.token_to_index = self.key_to_value(dictionary=self.index_to_token)
			if not self.index_to_token and self.token_to_index: self.index_to_token = self.key_to_value(dictionary=self.token_to_index)
			if self.pattern != 'sapi-0':
				if self.pattern == 'sapi-1': tokens_length = 2
				elif self.pattern == 'sapi-2': tokens_length = 3
				elif self.pattern == 'sapi-3': tokens_length = 4
				elif self.pattern == 'sapi-4': tokens_length = 5
				else: tokens_length = 0
				if tokens_length >= 2: text_to_list = self.__text_to_list
				else: text_to_list = self.__text_to_list_sapi5
				self.encode = lambda strings: [self.token_to_index[token] for token in text_to_list(text=strings, tokens_length=tokens_length, is_sorted=False)]
			else: self.encode = lambda strings: [self.token_to_index[token] for token in strings]
			self.decode = lambda indexes: ''.join([self.index_to_token[str(index)] for index in indexes])
			return True
		except Exception as error:
			print('ERROR in SapiensTokenizer.load_vocabulary: ' + str(error))
			return False
	def set_default_sapi_0(self, only_token_to_index=False, only_index_to_token=False):
		try:
			maximum_unicode = 0x10FFFF
			vocabulary_size, token_to_index, index_to_token = 0, {}, {}
			for index in range(maximum_unicode+1):
			    try:
			        character = chr(index)
			        if not (0xD800 <= index <= 0xDFFF):
			        	token_to_index[character] = index
			        	index_to_token[index] = character
			        	vocabulary_size += 1
			    except: continue
			self.vocabulary_size = vocabulary_size
			self.token_to_index = {} if only_index_to_token else token_to_index
			self.index_to_token = {} if only_token_to_index else index_to_token
			self.encode = lambda strings: [self.token_to_index[token] for token in strings]
			self.decode = lambda indexes: ''.join([self.index_to_token[str(index)] for index in indexes])
			self.pattern = 'sapi-0'
			return True
		except Exception as error:
			print('ERROR in SapiensTokenizer.set_default_sapi_0: ' + str(error))
			return False
	def get_vocabulary_size(self, pattern=''):
		try:
			vocabulary_size = 0
			pattern = self.__validate_encoder_general(encoder=pattern)
			if pattern.startswith('sapi'):
				if not self.vocabulary_size: self.set_default_sapi_0()
				vocabulary_size = self.vocabulary_size
			else:
				encode = self.__encoding_for_model(pattern)
				vocabulary_size = encode.n_vocab
			return vocabulary_size
		except Exception as error:
			print('ERROR in SapiensTokenizer.get_vocabulary_size: ' + str(error))
			return 0
	def get_encode(self, pattern=''):
		try:
			pattern = self.__validate_encoder_general(encoder=pattern)
			if pattern.startswith('sapi'):
				if not self.encode: self.set_default_sapi_0()
				return self.encode
			else:
				encode = self.__encoding_for_model(pattern)
				return encode.encode
		except Exception as error:
			print('ERROR in SapiensTokenizer.get_encode: ' + str(error))
			return None
	def get_decode(self, pattern=''):
		try:
			pattern = self.__validate_encoder_general(encoder=pattern)
			if pattern.startswith('sapi'):
				if not self.decode: self.set_default_sapi_0()
				return self.decode
			else:
				decode = self.__encoding_for_model(pattern)
				return decode.decode
		except Exception as error:
			print('ERROR in SapiensTokenizer.get_decode: ' + str(error))
			return None
	def get_token_to_index(self):
		try:
			if not self.token_to_index and self.pattern == 'sapi-0': self.set_default_sapi_0()
			return self.token_to_index
		except Exception as error:
			print('ERROR in SapiensTokenizer.get_token_to_index: ' + str(error))
			return {}
	def get_index_to_token(self):
		try:
			if not self.index_to_token and self.pattern == 'sapi-0': self.set_default_sapi_0()
			return self.index_to_token
		except Exception as error:
			print('ERROR in SapiensTokenizer.get_index_to_token: ' + str(error))
			return {}
	def to_encode(self, text_data='', length=None, pattern=''):
		try:
			embedding = []
			if length is not None: length = max(0, int(length)) if type(length) in (bool, int, float) else 0
			if not text_data or length == 0: return embedding
			text_data = rf'{text_data}'
			pattern = self.__validate_encoder_general(encoder=pattern)
			if pattern.startswith('sapi'):
				if not self.encode: self.set_default_sapi_0()
				encode = self.encode
			else: encode = self.get_encode(pattern=pattern)
			embedding = encode(text_data)
			if length is not None: embedding = self.__adjustment_embedding(embedding=embedding, length=length, pattern=pattern)
			return embedding
		except Exception as error:
			print('ERROR in SapiensTokenizer.to_encode: ' + str(error))
			return []
	def to_decode(self, embedding=[], length=None, pattern=''):
		try:
			text_data = ''
			embedding = list(embedding) if type(embedding) in (tuple, list) else []
			if length is not None: length = max(0, int(length)) if type(length) in (bool, int, float) else 0
			if not embedding or length == 0: return text_data
			pattern = self.__validate_encoder_general(encoder=pattern)
			if length is not None: embedding = self.__adjustment_embedding(embedding=embedding, length=length, pattern=pattern)
			if pattern.startswith('sapi'):
				if not self.decode: self.set_default_sapi_0()
				text_data = self.decode(embedding)
			else: text_data = self.get_decode(pattern=pattern)(embedding)
			return text_data if length is not None else text_data.strip()
		except Exception as error:
			print('ERROR in SapiensTokenizer.to_decode: ' + str(error))
			return ''
	def count_tokens(self, text_data_or_embedding='', pattern=''):
		try:
			tokens_number = 0
			if not text_data_or_embedding: return tokens_number
			if type(text_data_or_embedding) in (tuple, list): tokens_number = len(text_data_or_embedding)
			else:
				text_data_or_embedding = rf'{text_data_or_embedding}'
				pattern = self.__validate_encoder_general(encoder=pattern)
				if pattern.startswith('sapi'):
					if not self.encode: self.set_default_sapi_0()
					embedding = self.encode(text_data_or_embedding)
				else: embedding = self.get_encode(pattern=pattern)(text_data_or_embedding)
				tokens_number = len(embedding)
			return tokens_number
		except Exception as error:
			print('ERROR in SapiensTokenizer.count_tokens: ' + str(error))
			return 0
	def to_encode_txt(self, file_path='', length=None, pattern=''):
		try:
			embedding = []
			file_path = str(file_path).strip()
			if length is not None: length = max(0, int(length)) if type(length) in (bool, int, float) else 0
			if not file_path or length == 0: return embedding
			pattern = self.__validate_encoder_general(encoder=pattern)
			text_data = self.__read_txt(file_path=file_path)
			embedding = self.to_encode(text_data=text_data, length=length, pattern=pattern)
			return embedding
		except Exception as error:
			print('ERROR in SapiensTokenizer.to_encode_txt: ' + str(error))
			return []
	def to_decode_txt(self, file_path='', length=None, pattern=''):
		try:
			text_data = ''
			file_path = str(file_path).strip()
			if length is not None: length = max(0, int(length)) if type(length) in (bool, int, float) else 0
			if not file_path or length == 0: return text_data
			pattern = self.__validate_encoder_general(encoder=pattern)
			embedding = self.__load_json(string_content=self.__read_txt(file_path=file_path, strip=False))
			text_data = self.to_decode(embedding=embedding, length=length, pattern=pattern)
			return text_data
		except Exception as error:
			print('ERROR in SapiensTokenizer.to_decode_txt: ' + str(error))
			return ''
	def count_tokens_txt(self, file_path='', pattern=''):
		try:
			tokens_number = 0
			file_path = str(file_path).strip()
			if not file_path: return tokens_number
			pattern = self.__validate_encoder_general(encoder=pattern)
			text_data = self.__read_txt(file_path=file_path)
			tokens_number = self.count_tokens(text_data_or_embedding=text_data, pattern=pattern)
			return tokens_number
		except Exception as error:
			print('ERROR in SapiensTokenizer.count_tokens_txt: ' + str(error))
			return 0
	def tokenizer(self, text_data='', pattern=''):
		try:
			list_of_tokens = []
			text_data = str(text_data).strip()
			if not text_data: return list_of_tokens
			pattern = self.__validate_encoder_general(encoder=pattern)
			tokens = self.to_encode(text_data=text_data, length=None, pattern=pattern)
			list_of_tokens = [self.to_decode(embedding=[token], length=None, pattern=pattern) for token in tokens]
			return list_of_tokens
		except Exception as error:
			print('ERROR in SapiensTokenizer.tokenizer: ' + str(error))
			return []
	def tokenizer_txt(self, file_path='', pattern=''):
		try:
			list_of_tokens = []
			file_path = str(file_path).strip()
			if not file_path: return list_of_tokens
			pattern = self.__validate_encoder_general(encoder=pattern)
			text_data = self.__read_txt(file_path=file_path)
			list_of_tokens = self.tokenizer(text_data=text_data, pattern=pattern)
			return list_of_tokens
		except Exception as error:
			print('ERROR in SapiensTokenizer.tokenizer_txt: ' + str(error))
			return []
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
