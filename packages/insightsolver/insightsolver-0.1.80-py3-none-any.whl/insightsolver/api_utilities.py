"""
* `Organization`:  InsightSolver Solutions Inc.
* `Project Name`:  InsightSolver
* `Module Name`:   insightsolver
* `File Name`:     api_utilities.py
* `Author`:        Noé Aubin-Cadot
* `Email`:         noe.aubin-cadot@insightsolver.com

Description
-----------
This file provides essential utility functions to secure and streamline client-server
communication within the API. It includes functions for data compression, encryption, 
decryption, and transformations of data structures, all designed to facilitate efficient 
and protected message exchange between the client and server.

While all communications are secured via HTTPS, this file goes a step further by adding
an additional layer of encryption, using RSA-4096 and ECDSA-SECP521R1 for secure key exchange 
and AES-256 for data encryption. These functions are particularly useful for scenarios 
requiring enhanced data privacy and integrity.

Functions provided
------------------

- ``hash_string``: Computes the hash of a string.
- ``convert_bytes_to_base64_string``: Convert bytes to a base64 string.
- ``convert_base64_string_to_bytes``: Convert a base64 string to bytes.
- ``compress_string``: Compress a string using gzip.
- ``decompress_string``: Decompress a gzip-compressed string.
- ``compress_and_encrypt_string``: Compress and encrypt a string for secure transmission.
- ``decrypt_and_decompress_string``: Decrypt an encrypted string.
- ``encode_obj``: Takes an object and encode it to a new object compatible with json serialization.
- ``convert_dict_to_json_string``: Convert a dict to a json string.
- ``decode_obj``: Inverse operation from ``encode_obj``.
- ``convert_json_string_to_dict``: Convert a json string to a dict.
- ``transform_dict``: Convert a dictionary for easier client-server communication.
- ``untransform_dict``: Reverse the dictionary transformation to restore the original data format.
- ``generate_keys``: Generate RSA and ECDSA private and public keys.
- ``compute_credits_from_df``: Compute the amount of credits consumed for a given DataFrame.
- ``request_cloud_credits_infos``: Request the server for informations about the credits available.
- ``request_cloud_public_keys``: Request the server for public keys.
- ``request_cloud_computation``: Request the server for computation.
- ``search_best_ruleset_from_API_dict``: Make the API call.

License
-------
Exclusive Use License - see `LICENSE <license.html>`_ for details.

----------------------------

"""

################################################################################
################################################################################
# Import some libraries

from typing import Optional, Union, Dict, Sequence, Any, Tuple
import requests

import pandas as pd
import numpy as np
import mpmath

################################################################################
################################################################################
# Defining a function for hashing a string

def hash_string(
	string,
):
	"""
	A function to compute the hash of a string using hashlib.
	"""
	import hashlib
	id_bytes = string.encode('utf-8')
	sha256_hash = hashlib.sha256(id_bytes).hexdigest()
	return sha256_hash

################################################################################
################################################################################
# Defining functions for converting between bytes and base64

def convert_bytes_to_base64_string(
	data : bytes, # The data to encode in base64
)->str:
	"""
	Convert a bytes object to a base64-encoded string.

	Parameters
	----------
	data : bytes
		The byte data to encode.

	Returns
	-------
	str
		The base64-encoded string.
	"""
	import base64
	return base64.b64encode(data).decode('utf-8')

def convert_base64_string_to_bytes(
	string : str,  # The base64-encoded string to decode
)->bytes:
	"""
	Convert a base64-encoded string to a bytes object.

	Parameters
	----------
	string : str
		The base64-encoded string.

	Returns
	-------
	bytes
		The decoded byte data.
	"""
	import base64
	return base64.b64decode(string)

################################################################################
################################################################################
# Defining some functions to handle compression and decompression of string

def compress_string(
	original_string: str,  # The string to compress
) -> str:
	"""
	Compress a string using gzip and then encode it to base64.

	Parameters
	----------
	original_string : str
		The original string to be compressed.

	Returns
	-------
	str
		The compressed string.

	Example
	-------
	::

		original_string = "This is a test string"
		compressed_string = compress_string(original_string)
		print(compressed_string)  # Example output: 'H4sIAA01/2YC/wvJyCxWAKJEhZLU4hKF4pKizLx0AG3zTmsVAAAA'
	"""
	# Convert the original string to bytes
	original_data = original_string.encode('utf-8') # A bytes object

	# Compress the original data by gzip
	import gzip
	compressed_data = gzip.compress(original_data) # A bytes object

	# Encode the compressed data to base64
	import base64
	compressed_data_base64 = base64.b64encode(compressed_data) # A bytes object

	# Decode the base64-encoded compressed data as a string
	compressed_string = compressed_data_base64.decode('utf-8') # A str object

	# Return the compressed string
	return compressed_string


def decompress_string(
	compressed_string : str, # The string to decompress.
)->str:
	"""
	Decompress a base64-encoded string that was previously compressed using gzip.

	This function takes a base64-encoded string, decodes it, and then decompresses
	the resulting data using gzip to return the original string.

	Parameters
	----------
	compressed_string : str
		The base64-encoded string that contains the compressed data.

	Returns
	-------
	str
		The original uncompressed string.

	Example
	-------
	::

		compressed_string = 'H4sIAA01/2YC/wvJyCxWAKJEhZLU4hKF4pKizLx0AG3zTmsVAAAA'
		original_string = decompress_string(compressed_string)
		print(original_string) # 'This is a test string'
	"""
	# Convert the compressed base64 string to bytes
	compressed_data = convert_base64_string_to_bytes(
		string = compressed_string,
	)

	# Decompress the data with gzip
	import gzip
	original_data = gzip.decompress(compressed_data) # A bytes object

	# Convert the data to string
	original_string = original_data.decode('utf-8') # A str object

	# Return the result
	return original_string

################################################################################
################################################################################
# Defining some functions to handle compression and encryption

def compress_and_encrypt_string(
	original_string : str,   # The original string to compress and encrypt
	symmetric_key   : bytes, # The symmetric key
)->tuple[str, str]:
	"""
	Compress and encrypt a string using AES-256-GCM.

	This function compresses the given string using gzip and then encrypts it using
	AES-256 in GCM mode. A nonce is used in the encryption process for AES-GCM, and
	the result is base64-encoded for easy transfer over networks.

	Security:
	- AES-256 encryption
	- GCM (Galois/Counter Mode) with authentication

	Parameters
	----------
	original_string : str
		The original string to be compressed and encrypted.
	symmetric_key : bytes
		The 32-byte symmetric key used for encryption.

	Returns
	-------
	tuple[str, str]
		A tuple containing the base64-encoded encrypted compressed string and the base64-encoded nonce used.

	Example
	-------
	::

		transformed_string, nonce_string = compress_and_encrypt_string(
			original_string = "Secret data",
			symmetric_key   = token_bytes(32),
		)
		print(transformed_string, nonce_string) # 'Base64_encoded_result', nonce_string
	"""
	import gzip
	import base64
	from cryptography.hazmat.primitives.ciphers.aead import AESGCM
	from secrets import token_bytes

	# Convert the string to bytes and compress it
	compressed_data_bytes = gzip.compress(original_string.encode('utf-8'))

	# Generate a random nonce for AES-GCM
	nonce_bytes = token_bytes(12)

	# Set up AES-GCM encryption
	aesgcm = AESGCM(symmetric_key)

	# Encrypt the compressed data
	compressed_encrypted_bytes = aesgcm.encrypt(
		nonce           = nonce_bytes,           # The nonce used to encrypt the data
		data            = compressed_data_bytes, # The compressed data to send
		associated_data = None                   # No additional authenticated data
	)

	# Convert the ciphertext from bytes to base64
	transformed_string = convert_bytes_to_base64_string(compressed_encrypted_bytes)

	# Convert the nonce from bytes to base64
	nonce_string = convert_bytes_to_base64_string(nonce_bytes)

	# Return the base64-encoded encrypted string and the nonce separately
	return transformed_string, nonce_string

def decrypt_and_decompress_string(
	transformed_string : str,   # The base64-encoded encrypted string
	symmetric_key      : bytes, # The symmetric key used for decryption
	nonce              : bytes, # The nonce used during encryption
)->str:
	"""
	Decrypt and decompress a string using AES-256-GCM.

	This function takes a base64-encoded encrypted string, decrypts it using AES-256 in GCM mode 
	with the provided symmetric key and nonce, and then decompresses the result using gzip.

	Security:
	- AES-256 encryption
	- GCM (Galois/Counter Mode) with authentication

	Parameters
	----------
	transformed_string : str
		The base64-encoded string that contains the encrypted and compressed data.
	symmetric_key : bytes
		The 32-byte symmetric key used for decryption.
	nonce : bytes
		The nonce used for AES-GCM during encryption.

	Returns
	-------
	str
		The original uncompressed and decrypted string.

	Raises
	------
	Exception
		If the decryption fails.

	Example
	-------
	::

		original_string = decrypt_and_decompress_string(
			transformed_string = encrypted_compressed_string,
			symmetric_key      = token_bytes(32),
			nonce              = nonce
		)
		print(original_string) # 'Secret data'
	"""

	# Decode the base64-encoded encrypted data
	encrypted_data = convert_base64_string_to_bytes(
		string = transformed_string,
	)

	# Set up AES-GCM decryption with the symmetric key and nonce
	from cryptography.hazmat.primitives.ciphers.aead import AESGCM
	aesgcm = AESGCM(symmetric_key)

	# Decrypt the data
	decrypted_compressed_data = aesgcm.decrypt(
		nonce           = nonce,
		data            = encrypted_data,
		associated_data = None  # No additional authenticated data
	)

	# Decompress the decrypted data
	import gzip
	decompressed_data = gzip.decompress(decrypted_compressed_data)

	# Decode the original string
	original_string = decompressed_data.decode('utf-8')

	# Return the original string
	return original_string

################################################################################
################################################################################
# Defining functions for transforming and untransforming dict

def encode_obj(
	obj,
):
	"""
	This function takes an object and encode it to a new object compatible with json serialization.
	"""
	if isinstance(obj, dict):
		return {str(k): encode_obj(v) for k, v in obj.items()}
	elif isinstance(obj, list):
		return [encode_obj(v) for v in obj]
	elif isinstance(obj, set):
		return {"__type__": "set", "items": [encode_obj(v) for v in sorted(obj, key=str)]}
	elif isinstance(obj, mpmath.mpf):
		return {"__type__": "mpf", "value": str(obj)}  # préserve toute la précision
	elif isinstance(obj, (np.integer, np.floating)):
		return obj.item()  # convertit np.int64/float64 -> int/float
	elif isinstance(obj, (int, float)):  # natifs, sûrs
		return obj
	else:
		return obj

def convert_dict_to_json_string(
	d:dict,
)->str:
	"""
	This function converts a dict to a json string.
	"""
	# Make a copy of the dict
	d = d.copy()
	# Modify the dict so that it's compatible with json
	import mpmath
	import numpy as np
	d = encode_obj(
		obj = d,
	)
	# Convert the modified dict to a json string
	import json
	string = json.dumps(d)
	# Return the result
	return string

def decode_obj(
	obj,
):
	"""
	This function does the inverse operation from the function ``encode_obj``.
	"""
	if isinstance(obj, dict):
		if "__type__" in obj:
			if obj["__type__"] == "mpf":
				return mpmath.mpf(obj["value"])
			elif obj["__type__"] == "set":
				return set(decode_obj(i) for i in obj["items"])
		return {k: decode_obj(v) for k, v in obj.items()}
	elif isinstance(obj, list):
		return [decode_obj(v) for v in obj]
	else:
		return obj

def convert_json_string_to_dict(
	string:str,
)->dict:
	"""
	This function takes a json string and converts it to a dict.
	"""
	# Convert the string to a dict
	import json
	d = json.loads(string)
	# Modify the dict to its original state
	import mpmath
	d = decode_obj(
		obj = d,
	)
	# Return the result
	return d

def transform_dict(
	d_original       : dict,                     # The dict to transform
	do_compress_data : bool            = False,  # If we want to compress the data
	symmetric_key    : Optional[bytes] = None,   # The symmetric key used to encrypt the data
	json_format      : str             = 'json', # The json format
)->dict:
	"""
	Transform the contents of a dictionary by optionally compressing and encrypting its data.

	This function takes a dictionary and converts it to a string. Depending on the options provided, 
	it can compress the data using gzip, encrypt it using AES-256, or both. The resulting string is 
	returned in a transformed dictionary format for easier transmission or storage.

	Parameters
	----------
	d_original : dict
		The original dictionary that needs to be transformed.
	do_compress_data : bool, optional
		Whether or not to compress the dictionary data (default is False).
	symmetric_key : bytes, optional
		A symmetric key. Typically generated using from secrets import token_bytes;symmetric_key = token_bytes(32). If provided, the data will be encrypted (default is None).
	json_format : str, optional
		The format to convert the dictionary to a string. Can be 'json' or 'json_extended' (default is 'json').

	Returns
	-------
	dict
		A dictionary containing the transformed string, the transformations applied, and the json format.

	Example
	-------
	::

		d_original = {'A':1, 'B':2, 'C':3}
		from secrets import token_bytes
		symmetric_key = token_bytes(32) # b'\\x1a\\xef&\\x0bR\\xe1\\x95\\xfa\\x90\\x10r\\x93\\x1a\\xaeN\\xc2\\xba\\x80\\xf1\\x1a\\x0fG\\xf4(\\x0e#\\xd4\\xaf`\\x81q\\xf4'
		d_transformed = transform_dict(
			d_original       = d_original,
			do_compress_data = True,
			symmetric_key    = symmetric_key,
			json_format      = 'json',
		)
		print(d_transformed)
		# {
		#	'transformations': 'encrypted_gzip_base64',
		#	'json_format': 'json',
		#	'transformed_string': 'q30qPkK19Z3sENnfk77t4CnpzWKV+gdHLLSpNNgU3DjdmEbLcZWj+AjZyFmUquuUmh6obZmTh8k=',
		#	'nonce_string': '7PpTvoc0Ksx8whRy',
		# }
	"""
	# Convert the dict to a string
	if json_format=='json':
		import json
		original_string = json.dumps(d_original)
	elif json_format=='json_extended':
		original_string = convert_dict_to_json_string(d_original)
	else:
		raise Exception(f"ERROR: json_format='{json_format}' must be in ['json', 'json_extended'].")
	# If a symmetric key is provided we'll encrypt the data
	if symmetric_key!=None:
		do_encrypt_data = True
	else:
		do_encrypt_data = False
	# If we want to encrypt the data, we compress it first
	if do_encrypt_data:
		do_compress_data = True
	# If we want to compress the data but not encrypt it
	if do_compress_data&(not do_encrypt_data):
		# Compress the data
		transformed_string = compress_string(
			original_string = original_string,
		)
		# Reformat the dictionary with the transformation
		d_transformed = {
			'transformations'    : 'gzip_base64',
			'json_format'        : json_format,
			'transformed_string' : transformed_string,
			'nonce_string'       : '',
		}
	elif do_encrypt_data: # If we want to compress and encrypt the data
		# Compress and encrypt the data
		transformed_string, nonce_string = compress_and_encrypt_string(
			original_string = original_string,
			symmetric_key   = symmetric_key,
		)
		# Reformat the dictionary with the encryption transformation
		d_transformed = {
			'transformations'    : 'encrypted_gzip_base64',
			'json_format'        : json_format,
			'transformed_string' : transformed_string,
			'nonce_string'       : nonce_string,
		}
	else: # If we do not want to compress or encrypt the data
		d_transformed = {
			'transformations'    : 'no_transformation',
			'json_format'        : json_format,
			'transformed_string' : original_string,
			'nonce_string'       : '',
		}
	# Return the result
	return d_transformed

def untransform_dict(
	d_transformed : dict,                    # The dict to untransform
	symmetric_key : Optional[bytes] = None,  # The symmetric key to use to decrypt the dict
	verbose       : bool            = False, # Verbosity
)->dict:
	"""
	Decompress and decrypt the contents of a transformed dictionary.

	This function takes a dictionary that has been transformed (e.g., compressed, encrypted),
	and restores its original contents by reversing the transformations. Depending on the 
	transformation type, it may decrypt and/or decompress the data.

	Parameters
	----------
	d_transformed : dict
		The transformed dictionary containing the compressed/encrypted string, 
		the transformations applied, and the json format used.
	symmetric_key : bytes, optional
		A symmetric key. Typically generated using ``from secrets import token_bytes;symmetric_key = token_bytes(32)``. If provided, the data will be decrypted using this key (default is None).
	verbose : bool, optional
		If True, additional debug information will be printed (default is False).

	Returns
	-------
	dict
		The original dictionary with its content restored.

	Raises
	------
	Exception
		If an invalid transformation type or JSON format is provided.

	Example
	-------
	::

		d_transformed = {
			'transformations'    : 'encrypted_gzip_base64',
			'json_format'        : 'json',
			'transformed_string' : 'q30qPkK19Z3sENnfk77t4CnpzWKV+gdHLLSpNNgU3DjdmEbLcZWj+AjZyFmUquuUmh6obZmTh8k='
			'nonce_string'       : '7PpTvoc0Ksx8whRy',
		}
		d_untransformed = untransform_dict(
			d_transformed = d_transformed,
			symmetric_key = symmetric_key, # b'\\x1a\\xef&\\x0bR\\xe1\\x95\\xfa\\x90\\x10r\\x93\\x1a\\xaeN\\xc2\\xba\\x80\\xf1\\x1a\\x0fG\\xf4(\\x0e#\\xd4\\xaf`\\x81q\\xf4'
		)
		print(d_untransformed) # {'A': 1, 'B': 2, 'C': 3}
	"""
	transformations    = d_transformed['transformations']
	json_format        = d_transformed['json_format']
	transformed_string = d_transformed['transformed_string']
	if transformations=='no_transformation': # If no transformations were applied
		original_string = transformed_string
	elif transformations=='gzip_base64': # If the data was compressed but not encrypted
		original_string = decompress_string(
			compressed_string = transformed_string
		)
	elif transformations=='encrypted_gzip_base64': # If the data was compressed and encrypted
		# Take the nonce in base64
		nonce_string = d_transformed['nonce_string']
		# Convert the nonce from base64 to bytes
		nonce_bytes = convert_base64_string_to_bytes(
			string = nonce_string,
		)
		original_string = decrypt_and_decompress_string(
			transformed_string = transformed_string,
			symmetric_key      = symmetric_key,
			nonce              = nonce_bytes,
		)
	else:
		raise Exception(f"ERROR: transformations='{transformations}' must be in ['no_transformation', 'gzip_base64', 'encrypted_gzip_base64'].")
	if json_format=='json':
		import json
		d_original = json.loads(original_string)
	elif json_format=='json_extended':
		d_original = convert_json_string_to_dict(original_string)
	else:
		raise Exception(f"ERROR: json_format='{json_format}' must be in ['json', 'json_extended'].")
	# Return the result
	return d_original


################################################################################
################################################################################
# Defining some cryptographic functions

def generate_keys():
	"""
	This function generates RSA and ECDSA private and public keys.
	The generated keys:

	- ``rsa_private_key``
	- ``ecdsa_private_key``
	- ``rsa_public_key_pem_bytes``
	- ``ecdsa_public_key_pem_bytes``

	Returns
	-------
	tuple
		A tuple containing four elements:

		- rsa_private_key: The generated RSA private key.
		- ecdsa_private_key: The generated ECDSA private key.
		- rsa_public_key_pem_bytes: The RSA public key serialized in PEM format.
		- ecdsa_public_key_pem_bytes: The ECDSA public key serialized in PEM format.
	"""
	# Import necessary libraries
	from cryptography.hazmat.primitives.asymmetric import rsa, ec
	from cryptography.hazmat.primitives import serialization
	# Generate the private RSA key
	# The RSA key allows the encrypted transfer of the AES symmetric key.
	# Highly secure fields (finance, healthcare, etc.) generally use 2048 bits.
	# Therefore, a 4096-bit key is highly secure and future-proof.
	# There's no need to go to 8192 bits, as it is too computationally expensive and overkill.
	rsa_private_key = rsa.generate_private_key(
		public_exponent = 65537, # Public exponent
		key_size        = 4096,  # RSA key size in bits
	)

	# Generate the private ECDSA key
	# The ECDSA key enables digital signatures (for authenticity and data integrity)
	# ECDSA: Elliptic Curve Digital Signature Algorithm
	# Based on the SECP521R1 elliptic curve
	# This curve is standardized by NIST and used in many high-security systems.
	ecdsa_private_key = ec.generate_private_key(
		curve = ec.SECP521R1(), # Elliptic curve used
	)

	# Generate the RSA public key
	rsa_public_key = rsa_private_key.public_key()

	# Generate the ECDSA public key
	ecdsa_public_key = ecdsa_private_key.public_key()
	
	# Serialize the RSA public key
	rsa_public_key_pem_bytes = rsa_public_key.public_bytes(
		encoding = serialization.Encoding.PEM,                     # PEM (Privacy-Enhanced Mail) encoding
		format   = serialization.PublicFormat.SubjectPublicKeyInfo # Format according to SubjectPublicKeyInfo standard
	)

	# Serialize the ECDSA public key
	ecdsa_public_key_pem_bytes = ecdsa_public_key.public_bytes(
		encoding = serialization.Encoding.PEM,                     # PEM (Privacy-Enhanced Mail) encoding
		format   = serialization.PublicFormat.SubjectPublicKeyInfo # Format according to SubjectPublicKeyInfo standard
	)

	# Return the keys
	return rsa_private_key,ecdsa_private_key,rsa_public_key_pem_bytes,ecdsa_public_key_pem_bytes

################################################################################
################################################################################
# Defining functions for specific requests to the server

def generate_url_headers(
	computing_source       : str,                  # A string to specify where the server is
	input_file_service_key : Optional[str] = None, # The service key of the client
)->Tuple[str, Optional[Dict[str, Any]]]:
	"""
	This function generates the url and the headers for the POST request.

	Parameters
	----------
	computing_source : str
		Where the server is.
	input_file_service_key : optional
		The client's service key, needed if the server is remote.
		Default is `None`.
	"""
	# Define the POST request parameters
	if computing_source=='local_cloud_function':
		# If we want to call a local server
		# This requires a local rule mining server
		# Define the POST request parameters
		url           = 'http://localhost:8080/'
		headers       = None
	elif computing_source in ['remote_cloud_function', 'remote_cloud_function_prod','remote_cloud_function_dev']:
		# Determine where the code is running
		import os
		if "K_SERVICE" not in os.environ:
			# If the API client is running outside a Google Cloud Run container, we need a service key
			if input_file_service_key==None:
				# If no service key is provided, raise an error
				raise Exception("ERROR: The InsightSolver API client is running outside a Google Cloud Run container and the service key is None, but it must be specified for remote cloud computing.")
			else:
				# If a service key is provided, put it in the environment variables
				import os
				os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = input_file_service_key
		project_name  = 'insightsolver'
		region        = 'northamerica-northeast1' # for 'insightsolver_cloud_run_function'        
		if computing_source in ['remote_cloud_function', 'remote_cloud_function_prod']:
			function_name = 'insightsolver_cloud_run_function_prod'
		elif computing_source=='remote_cloud_function_dev':
			function_name = 'insightsolver_cloud_run_function_dev'
		url           = f'https://{region}-{project_name}.cloudfunctions.net/{function_name}'
		import google.auth.transport.requests
		request       = google.auth.transport.requests.Request()
		import google.oauth2.id_token
		TOKEN         = google.oauth2.id_token.fetch_id_token(request, url)
		headers       = {
			'Authorization': f"Bearer {TOKEN}",
			"Content-Type": "application/json",
		}
	else:
		raise Exception(f"ERROR: computing_source='{computing_source}' is invalid. It must be ['local_cloud_function', 'remote_cloud_function', 'remote_cloud_function_prod', 'remote_cloud_function_dev'].")

	# Return the results
	return (
		url,     # Return the url
		headers, # Return the headers
	)

def compute_credits_from_df(
	df: pd.DataFrame,                       # The DataFrame that contains the data.
	columns_names_to_btypes: dict = dict(), # The dict that specifies how to handle the variables.
)->int:
	"""
	This function computes the number of credits consumed by a rule mining via the API.
	This number is based on the size of the DataFrame sent to the API.
	
	Remark:
	The amount of credits debited is m*n where:
	- m is the number of rows of df (excluding the header).
	- n is the number of features to explore (i.e. the number of columns less the index, less the target variable, less the ignored features).
	
	Parameters
	----------
	df : pd.DataFrame
		Input DataFrame whose size is used to compute credits.
	columns_names_to_btypes: dict
		The dict that specifies how to handle the variables.
	
	Returns
	-------
	int
		The computed number of credits consumed.
	"""
	# Take the size of df
	m,n = df.shape
	# Remove the target variable
	n -= 1
	# Remove the variables that are set to ignore
	ignored_cols = [column_name for column_name in df.columns if columns_names_to_btypes.get(column_name)=="ignore"]
	n -= len(ignored_cols)
	# Compute the amount of credits
	from math import ceil
	credits = ceil(m*n/10000)
	# Return the amount of credits
	return credits

def request_cloud_credits_infos(
	computing_source       : str,                  # A string to specify where the server is
	d_out_credits_infos    : dict,                 # Dict that specifies which infos about the credits are asked for
	input_file_service_key : Optional[str] = None, # The service key of the client
	user_email             : Optional[str] = None, # Email of the user (only for use inside a Google Cloud Run container)
	timeout                : int           = 60,   # No need for a big timeout because we're only asking for infos about the credits
)->dict:
	"""
	Send a dict that specifies which infos about the credits are asked for.

	Parameters
	----------
	computing_source : str
		Where the server is.
	d_out_credits_infos : dict
		A dictionary containing the infos about the credits that are asked for. The dictionary format is:

		- ``private_key_id``: private_key_id of the service_key.
		- ``user_email``: Email of the user.
		- ``do_compute_credits_available``: A boolean that specifies where the number of credits available is requested.
		- ``do_compute_df_credits_infos``: A boolean that specifies if a DataFrame containing all credits transactions is asked for.
	input_file_service_key : optional
		The client's service key, needed if the server is remote.
		Default is `None`.
	timeout : int, optional
		The timeout duration for the request, in seconds. Default is 60 seconds, as this operation is 
		typically fast and does not involve computation.

	"""

	# Make sure that the dict contains both keys
	if ('do_compute_credits_available' not in d_out_credits_infos.keys()):
		raise Exception("ERROR: the key 'do_compute_credits_available' is not in the outgoing dict.")
	elif ('do_compute_df_credits_infos' not in d_out_credits_infos.keys()):
		raise Exception("ERROR: the key 'do_compute_df_credits_infos' is not in the outgoing dict.")

	# Make sure that at least one is True
	if (not d_out_credits_infos['do_compute_credits_available'])&(not d_out_credits_infos['do_compute_df_credits_infos']):
		raise Exception("ERROR: the outgoing dict needs that at least one of the keys 'do_compute_credits_available' or 'do_compute_df_credits_infos' to be True.")

	# Make sure the private_key_id is in the dict
	if computing_source in ['remote_cloud_function', 'remote_cloud_function_prod','remote_cloud_function_dev']:
		# Determine where the code is running
		import os
		if "K_SERVICE" not in os.environ:
			# If the API client is running outside a Google Cloud Run container, we need a service key
			if (input_file_service_key==None)&('private_key_id' not in d_out_credits_infos.keys()):
				# If no service key is provided, raise an error
				raise Exception("ERROR: The InsightSolver API client is running outside a Google Cloud Run container and the service key is None, but it must be specified for remote cloud computing.")
			elif (input_file_service_key==None)&('private_key_id' in d_out_credits_infos.keys()):
				...
			elif (input_file_service_key!=None)&('private_key_id' not in d_out_credits_infos.keys()):
				# If a service key is provided, take the ID of the key
				import json
				# Open the key
				with open(input_file_service_key, 'r') as f:
					# Take the service_key
					d_out_credits_infos['private_key_id'] = json.load(f)['private_key_id']
			elif (input_file_service_key!=None)&('private_key_id' in d_out_credits_infos.keys()):
				...
		else:
			# If the API client is running inside a Google Cloud Run container
			if (user_email==None)&('user_email' not in d_out_credits_infos.keys()):
				# If there is no email, raise an error
				raise Exception("ERROR: The InsightSolver API client is running inside a Google Cloud Run container and the user email is None, but it must be specified for remote cloud computing.")
			elif (user_email==None)&('user_email' in d_out_credits_infos.keys()):
				...
			elif (user_email!=None)&('user_email' not in d_out_credits_infos.keys()):
				# We identify the user via its email instead of the private key id from the service key
				d_out_credits_infos['user_email'] = user_email
			elif (user_email!=None)&('user_email' in d_out_credits_infos.keys()):
				...

	# Make sure that the 'requested_action' key is specified
	if 'requested_action' not in d_out_credits_infos.keys():
		d_out_credits_infos['requested_action'] = 'cloud_credits_infos'

	# Generate the url and the headers of the POST request
	url,headers = generate_url_headers(
		computing_source       = computing_source,
		input_file_service_key = input_file_service_key,
	)
	
	# Make the POST request
	import requests
	response = requests.post(
		url            = url,                 # URL of the request
		headers        = headers,             # A dict of HTTP headers to send to the URL
		json           = d_out_credits_infos, # The dict of to send to the URL
		timeout        = timeout,             # Max number of seconds to wait for the server for a response.
	)
	
	# Make sure that the response is ok
	if response.status_code != 200:
		print(response.text)
		raise Exception(f"ERROR (request_cloud_credits_infos): Received status code {response.status_code}")
	
	# Take the incoming json dict
	try:
		d_in_credits_infos = response.json()
	except:
		raise Exception("ERROR: The incoming response does not contain a .json() method.")
	
	# Make sure the incoming dict contains the requested keys
	expected_incoming_keys = [
		'credits_available',
		'df_credits_infos_to_dict',
	]
	for key in expected_incoming_keys:
		if key not in d_in_credits_infos.keys():
			raise Exception(f"ERROR (request_cloud_credits_infos): The incoming dict does not contain the key '{key}'.")
	
	# Convert the DataFrame info from json to dict
	df_credits_infos_to_dict_str = d_in_credits_infos['df_credits_infos_to_dict']
	if df_credits_infos_to_dict_str is not None:
		# Convert the JSON string to a dict
		df_credits_infos_to_dict = json.loads(df_credits_infos_to_dict_str)
		# Convert the dict to a DataFrame
		df_credits_infos = pd.DataFrame(
			data = df_credits_infos_to_dict,
		)
		# Convert all None to NaN
		df_credits_infos = df_credits_infos.map(lambda x: np.nan if x is None else x)
	else:
		df_credits_infos = None
	d_in_credits_infos['df_credits_infos'] = df_credits_infos

	# Return the result
	return d_in_credits_infos

def request_cloud_public_keys(
	computing_source       : str,                  # A string to specify where the server is
	d_client_public_keys   : dict,                 # Dict of the public keys of the client
	input_file_service_key : Optional[str] = None, # The service key of the client
	timeout                : int           = 60,   # No need for a big timeout because we're only asking for keys and not computation
)->dict:
	"""
	Send the client's public keys to the server and receive the server's public keys in response.

	This function establishes a secure connection to the specified server (``computing_source``) and sends 
	the client's public keys (``d_client_public_keys``). The server responds with its own set of public keys, 
	which are returned in a dictionary format.

	Parameters
	----------
	computing_source : str
		Where the server is.
	d_client_public_keys : dict
		A dictionary containing the client's public keys to be sent to the server. The dictionary format is:

		- ``alice_rsa_public_key_pem_base64``: Client's RSA public key, encoded in base64.
		- ``alice_ecdsa_public_key_pem_base64``: Client's ECDSA public key, encoded in base64.
	input_file_service_key : optional
		The client's service key, needed if the server is remote.
		Default is `None`.
	timeout : int, optional
		The timeout duration for the request, in seconds. Default is 60 seconds, as this operation is 
		typically fast and does not involve computation.

	Returns
	-------
	dict
		A dictionary containing the server's public keys and a unique session identifier. The dictionary 
		format is as follows:

		- ``session_id``: A unique identifier for the session.
		- ``bob_rsa_public_key_pem_base64``: Server's RSA public key, encoded in base64.
		- ``bob_ecdsa_public_key_pem_base64``: Server's ECDSA public key, encoded in base64.

	Example
	-------
	::

		# Client's public keys
		d_client_public_keys = {
			'alice_rsa_public_key_pem_base64': '<base64-encoded RSA public key>',
			'alice_ecdsa_public_key_pem_base64': '<base64-encoded ECDSA public key>',
		}

		# Request server public keys
		d_server_public_keys = request_cloud_public_keys(
			computing_source='https://server-address.com',
			d_client_public_keys=d_client_public_keys,
			input_file_service_key='client_service_key'
		)

		# Access the session ID and server's public keys
		session_id = d_server_public_keys['session_id']
		bob_rsa_public_key = d_server_public_keys['bob_rsa_public_key_pem_base64']
		bob_ecdsa_public_key = d_server_public_keys['bob_ecdsa_public_key_pem_base64']

	Raises
	------
	Exception
		If the request fails or the server does not return the expected keys.
	"""

	# Make sure that the 'requested_action' key is specified
	if 'requested_action' not in d_client_public_keys.keys():
		d_client_public_keys['requested_action'] = 'cloud_public_keys'

	# Generate the url and the headers of the POST request
	url,headers = generate_url_headers(
		computing_source       = computing_source,
		input_file_service_key = input_file_service_key,
	)

	# Make the POST request
	import requests
	response = requests.post(
		url            = url,                  # URL of the request
		headers        = headers,              # A dict of HTTP headers to send to the URL
		json           = d_client_public_keys, # The dict of to send to the URL
		timeout        = timeout,              # Max number of seconds to wait for the server for a response.
	)
	# Make sure that the response is ok
	if response.status_code != 200:
		print(response.text)
		raise Exception(f"ERROR (request_cloud_public_keys): Received status code {response.status_code}")
	# Make sure that the response contains a dict
	try:
		d_server_public_keys = response.json()
	except:
		print(response.text)
		raise Exception("ERROR (request_cloud_public_keys): The incoming response does not contain a .json() method.")
	# Make sure the dict contains the requested keys
	expected_incoming_keys = [
		'session_id',
		'bob_rsa_public_key_pem_base64',
		'bob_ecdsa_public_key_pem_base64',
	]
	for key in expected_incoming_keys:
		if key not in d_server_public_keys.keys():
			raise Exception(f"ERROR (request_cloud_public_keys): The incoming dict does not contain the key '{key}'.")
	# Return the result
	return d_server_public_keys

def request_cloud_computation(
	computing_source       : str,                   # A string to specify where the server is
	d_out_transformed      : dict,                  # The transformed dict to send to the server
	input_file_service_key : Optional[str] = None,  # The service key
	timeout                : int           = 600,   # The timeout
	verbose                : bool          = False, # Verbosity
)->dict:
	"""
	Send the transformed dict to the server for it to compute the rule mining.

	Parameters
	----------
	computing_source : str
		The computing source.
	d_out_transformed : dict
		The transformed dict to send to the server.
	input_file_service_key : str, optional
		The client's service key, needed if the server is remote.
		Default is `None`.
	timeout : int, optional
		Timeout for the request, in seconds. Default is 600 seconds, as computation may take longer.

	Returns
	-------
	dict
		The dict that contains the rule mining results.
	"""

	# Make sure that the 'requested_action' key is specified
	if 'requested_action' not in d_out_transformed.keys():
		d_out_transformed['requested_action'] = 'cloud_computation'

	# Generate the url and the headers of the POST request
	url,headers = generate_url_headers(
		computing_source       = computing_source,
		input_file_service_key = input_file_service_key,
	)

	# Make the POST request
	import requests
	response = requests.post(
		url     = url,               # The URL of the request
		headers = headers,           # The dict of HTTP headers to send to the URL
		json    = d_out_transformed, # The dict to send to the URL as json
		timeout = timeout,           # Max number of seconds to wait for the server for a response.
	)

	if verbose:
		# Take a look at the computation time of the request
		print('Request time (h:mm:ss) :',response.elapsed)
		print('status_code :',response.status_code)
		print('reason      :',response.reason)
		#print('text        :',response.text)

	# Take a look at the error message
	if not response.ok:
		# status_code = '400'
		# reason      = 'BAD REQUEST'
		try:
			error_message = response.json()['error']
		except:
			error_message = response.text
		raise Exception(f"ERROR: The API call did not succeed. Here is the error message sent by the server :\n{error_message}")
	# status_code = '200'
	# reason      = 'OK'

	# Take the incoming response.
	try:
		d_in_transformed = response.json()
	except:
		raise Exception("ERROR: The incoming response does not contain a .json() method.")
	if isinstance(d_in_transformed,dict):
		...
	elif isinstance(d_in_transformed,str):
		raise Exception('ERROR: The content of the incoming .json() method is a string.')

	# Return the dict
	return d_in_transformed

################################################################################
################################################################################
# Defining a function to handle the whole communication with the server

def search_best_ruleset_from_API_dict(
	d_out_original          : dict,                                    # The original dict pre-transformation
	input_file_service_key  : Optional[str] = None,                    # The service key
	user_email              : Optional[str] = None,                    # Email of the user (only for use inside a Google Cloud Run container)
	computing_source        : str           = 'remote_cloud_function', # The computing source
	do_compress_data        : bool          = True,                    # If we want to compress the data
	do_compute_memory_usage : bool          = True,                    # If we want to compute the memory usage
	verbose                 : bool          = False,                   # Verbosity
)->dict:
	"""
	Search for the best ruleset where the computation is done from the server.

	Parameters
	----------
	d_out_original: dict
		The original dict, pre-transformation, that contains the necessary data for the server to do rule mining.
	input_file_service_key: str, optional
		The service key of the client.
	user_email: str, optional
		Email of the user (only for use inside a Google Cloud Run container).
	computing_source: str, optional
		The computing source.
	do_compress_data: bool, optional
		If we want to compress the data to reduce transmission size.
	do_compute_memory_usage: bool, optional
		If we want to compute the memory usage.
	verbose: bool, optional
		Verbosity.

	Returns
	-------
	dict
		The dict that contain the output of the rule mining from the server.
	"""
	# Generate the asymetric keys of the client
	alice_rsa_private_key, alice_ecdsa_private_key, alice_rsa_public_key_pem_bytes, alice_ecdsa_public_pem_key_bytes = generate_keys()
	# Encode the client's public keys from bytes to base64
	alice_rsa_public_key_pem_base64   = convert_bytes_to_base64_string(alice_rsa_public_key_pem_bytes)
	alice_ecdsa_public_key_pem_base64 = convert_bytes_to_base64_string(alice_ecdsa_public_pem_key_bytes)
	# Put the public keys of the client in a dict
	d_client_public_keys = {
		'alice_rsa_public_key_pem_base64'   : alice_rsa_public_key_pem_base64,  # La clé publique RSA d'Alice
		'alice_ecdsa_public_key_pem_base64' : alice_ecdsa_public_key_pem_base64 # La clé publique ECDSA d'Alice
	}
	# Send the public keys of the client to the server in exchange of the server's public keys
	d_server_public_keys = request_cloud_public_keys(
		input_file_service_key = input_file_service_key,
		computing_source       = computing_source,
		d_client_public_keys   = d_client_public_keys,
		timeout                = 600,
	)
	# Take the session_id
	session_id = d_server_public_keys['session_id']
	# Take the server's public keys
	bob_rsa_public_key_pem_base64   = d_server_public_keys['bob_rsa_public_key_pem_base64']
	bob_ecdsa_public_key_pem_base64 = d_server_public_keys['bob_ecdsa_public_key_pem_base64']
	# Decode the public keys of the server
	bob_rsa_public_key_pem_bytes   = convert_base64_string_to_bytes(
		string = bob_rsa_public_key_pem_base64,
	)
	bob_ecdsa_public_key_pem_bytes = convert_base64_string_to_bytes(
		string = bob_ecdsa_public_key_pem_base64,
	)
	# Load the server's public keys
	from cryptography.hazmat.primitives import serialization
	bob_rsa_public_key = serialization.load_pem_public_key(bob_rsa_public_key_pem_bytes)
	bob_ecdsa_public_key = serialization.load_pem_public_key(bob_ecdsa_public_key_pem_bytes)
	# Generate a random symmetric AES-256 key (32 bytes = 256 bits)
	from secrets import token_bytes
	symmetric_key = token_bytes(32) # AES-256 key
	# Transform the outgoing dict (compression+encryption)
	d_out_transformed = transform_dict(
		d_original       = d_out_original,
		do_compress_data = do_compress_data,
		symmetric_key    = symmetric_key,
		json_format      = 'json',
	)
	# Encrypt the symmetric key using the server's RSA public key
	from cryptography.hazmat.primitives.asymmetric import padding
	from cryptography.hazmat.primitives import hashes
	encrypted_symmetric_key_bytes = bob_rsa_public_key.encrypt(
		plaintext = symmetric_key,                                 # We encipher the symmetric key
		padding   = padding.OAEP(                                  # The padding used is OAEP (Optimal Asymmetric Encryption Padding).
			mgf       = padding.MGF1(algorithm = hashes.SHA256()), # MGF1 (Mask Generation Function) based on SHA-256. Used to make more secure OAEP.
			algorithm = hashes.SHA256(),                           # SHA-256 is used for the OAEP padding function.
			label     = None                                       # Leave this to None.
		)
	)
	# Convert the encrypted symmetric key from bytes to base64
	encrypted_symmetric_key_base64 = convert_bytes_to_base64_string(encrypted_symmetric_key_bytes)
	# Sign the encrypted symmetric key using the client's ECDSA private key (for authentication, integrity, non-repudiation)
	from cryptography.hazmat.primitives.asymmetric import ec
	encrypted_symmetric_key_signature_bytes = alice_ecdsa_private_key.sign(
		data                = encrypted_symmetric_key_bytes, # Sign the encrypted symmetric key
		signature_algorithm = ec.ECDSA(hashes.SHA256()),     # Sign using the ECDSA algorithm
	)
	# Convert the encrypted symmetric key signature from bytes to base64
	encrypted_symmetric_key_signature_base64 = convert_bytes_to_base64_string(encrypted_symmetric_key_signature_bytes)
	# Specify if we want to compute the memory usage
	d_out_transformed['do_compute_memory_usage'] = do_compute_memory_usage
	# Add the private_key_id in the dict
	if computing_source in ['remote_cloud_function', 'remote_cloud_function_prod','remote_cloud_function_dev']:
		# Determine where the code is running
		import os
		if "K_SERVICE" not in os.environ:
			# If the API client is running outside a Google Cloud Run container, we need a service key
			if input_file_service_key==None:
				# If no service key is provided, raise an error
				raise Exception("ERROR: The InsightSolver API client is running outside a Google Cloud Run container and the service key is None, but it must be specified for remote cloud computing.")
			else:
				# If a service key is provided, take the ID of the key
				import json
				# Open the key
				with open(input_file_service_key, 'r') as f:
					# Take the service_key
					d_out_transformed['private_key_id'] = json.load(f)['private_key_id']
		else:
			# If the API client is running inside a Google Cloud Run container
			if user_email==None:
				# If there is no email, raise an error
				raise Exception("ERROR: The InsightSolver API client is running inside a Google Cloud Run container and the user email is None, but it must be specified for remote cloud computing.")
			else:
				# We identify the user via its email's hash instead of the private key id from the service key
				d_out_transformed['user_email'] = user_email
	# Add other things
	d_out_transformed['session_id'] = session_id
	d_out_transformed['encrypted_symmetric_key_base64'] = encrypted_symmetric_key_base64
	d_out_transformed['encrypted_symmetric_key_signature_base64'] = encrypted_symmetric_key_signature_base64
	# Cloud computation
	d_in_transformed = request_cloud_computation(
		input_file_service_key = input_file_service_key,
		computing_source       = computing_source,
		d_out_transformed      = d_out_transformed,
		timeout                = 600,
		verbose                = verbose,
	)
	# Untransform the dict
	try:
		d_in_original = untransform_dict(
			d_transformed = d_in_transformed,
			symmetric_key = symmetric_key,
			verbose       = verbose,
		)
	except:
		raise Exception("ERROR: Cannot untransform the incoming dict.")
	# Convert the rules keys to integer
	try:
		d_in_original['rule_mining_results'] = {int(key):val for key,val in d_in_original['rule_mining_results'].items()}
	except:
		raise Exception("ERROR: Cannot convert the rules keys to integers.")
	# Return the result
	return d_in_original

################################################################################
################################################################################
