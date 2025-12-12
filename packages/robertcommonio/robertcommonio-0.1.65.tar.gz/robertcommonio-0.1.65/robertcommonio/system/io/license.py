from typing import Optional, Union

from robertcommonbasic.basic.os.path import create_dir_if_not_exist
from robertcommonbasic.basic.os.file import get_file_folder
from robertcommonbasic.basic.data.utils import base64_encode, base64_decode

from robertcommonbasic.basic.file.xml import xml_node_to_str, value_to_xml_str, read_xml_dict, xml_str_to_dict, value_to_xml
from robertcommonbasic.basic.encrypt.aes import aes_encrypt, aes_decrypt
from robertcommonbasic.basic.encrypt.rsa import generate_rsa_key, rsa_encrypt, rsa_sign, rsa_decrypt, rsa_verify
from robertcommonbasic.basic.encrypt.hash import value_hash


def gen_license_content(licenses: Union[str, dict], bits: Optional[int] = 1024, encoding: Optional[str] = None) -> str:
    if isinstance(licenses, dict):
        license_xml = value_to_xml(licenses)
        license_content = xml_node_to_str(license_xml, encoding)
    else:
        license_content = licenses
    aes_key = value_hash(license_content)

    # AES加密数据 Base64
    encrypt_text = aes_encrypt(license_content.encode(), aes_key)

    # 生成密钥对
    server_private_pem, server_public_pem, client_private_pem, client_public_pem = generate_rsa_key(bits=bits)

    # 使用服务端私钥对aes密钥签名
    signature = rsa_sign(server_private_pem, aes_key)

    # 使用客户端公钥加密aes密钥
    encrypt_key = rsa_encrypt(client_public_pem, aes_key)

    # 生成License
    license_value = {"encrypt": {'@type': 'RSA+AES', '@bit': bits, 'pem': [{'@name': 'client_private', '#text': client_private_pem.decode()}, {'@name': 'server_public', '#text': server_public_pem.decode()}, {'@name': 'encrypt_key', '#text': encrypt_key.decode()}], 'content': base64_encode(encrypt_text), 'signature': signature.decode()}}

    return value_to_xml_str(license_value)


def gen_license_file(path: str, licenses: Union[str, dict], bits: Optional[int] = 1024, encoding: Optional[str] = None):
    license_content = gen_license_content(licenses, bits, encoding)
    create_dir_if_not_exist(get_file_folder(path))
    with open(path, 'w', encoding=encoding) as f:
        f.write(license_content)


def show_license_file(path: str, encoding: Optional[str] = None) -> str:
    license_value = read_xml_dict(path, encoding=encoding)
    return value_to_xml_str(license_value, encoding=encoding)


def parse_license_file(path: str, encoding: Optional[str] = None, value_type: Optional[str] = ''):
    license_value = read_xml_dict(path, encoding=encoding)
    if isinstance(license_value, dict) is True:
        encrypt_value = license_value.get('encrypt', {})
        pem = encrypt_value.get('pem')
        content = encrypt_value.get('content')
        signature = encrypt_value.get('signature')
        if isinstance(pem, list) and isinstance(content, str) and isinstance(signature, str):
            client_private = server_public = encrypt_key = ''
            for p in pem:
                name = p.get('@name')
                value = p.get('#text')
                if name == 'client_private':
                    client_private = value
                elif name == 'server_public':
                    server_public = value
                elif name == 'encrypt_key':
                    encrypt_key = value

            if len(client_private) > 0 and len(server_public) > 0 and len(encrypt_key) > 0:

                # 使用客户端私钥对加密后的aes密钥解密
                aes_key = rsa_decrypt(client_private, encrypt_key)

                # 使用服务端公钥验签
                if rsa_verify(server_public, aes_key, signature) is False:
                    raise Exception(f"Invald License Signature")

                # 使用aes私钥解密密文
                license_content = aes_decrypt(base64_decode(content), aes_key).decode()

                # 校验秘钥
                if value_hash(license_content) != aes_key:
                    Exception(f"Invalid License File(Modified)")

                if value_type == 'json':
                    return xml_str_to_dict(license_content)
                elif value_type == 'xml':
                    return value_to_xml(license_content)
                return license_content
            else:
                raise Exception(f"Invalid License File(Param)")
        else:
            raise Exception(f"Invalid License File(Type)")
    raise Exception(f"Invalid License File")


def parse_license_content(content: str, value_type: Optional[str] = ''):
    license_value = xml_str_to_dict(content)
    if isinstance(license_value, dict) is True:
        encrypt_value = license_value.get('encrypt', {})
        pem = encrypt_value.get('pem')
        content = encrypt_value.get('content')
        signature = encrypt_value.get('signature')
        if isinstance(pem, list) and isinstance(content, str) and isinstance(signature, str):
            client_private = server_public = encrypt_key = ''
            for p in pem:
                name = p.get('@name')
                value = p.get('#text')
                if name == 'client_private':
                    client_private = value
                elif name == 'server_public':
                    server_public = value
                elif name == 'encrypt_key':
                    encrypt_key = value

            if len(client_private) > 0 and len(server_public) > 0 and len(encrypt_key) > 0:

                # 使用客户端私钥对加密后的aes密钥解密
                aes_key = rsa_decrypt(client_private, encrypt_key)

                # 使用服务端公钥验签
                if rsa_verify(server_public, aes_key, signature) is False:
                    raise Exception(f"Invald License Signature")

                # 使用aes私钥解密密文
                license_content = aes_decrypt(base64_decode(content), aes_key).decode()

                # 校验秘钥
                if value_hash(license_content) != aes_key:
                    Exception(f"Invalid License File(Modified)")

                if value_type == 'json':
                    return xml_str_to_dict(license_content)
                elif value_type == 'xml':
                    return value_to_xml(license_content)
                return license_content
            else:
                raise Exception(f"Invalid License File(Param)")
        else:
            raise Exception(f"Invalid License File(Type)")
    raise Exception(f"Invalid License File")
