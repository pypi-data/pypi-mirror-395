import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def rsa_encrypt(public_key_pem, data):
    """
    使用给定的RSA公钥加密数据
    :param public_key_pem: RSA公钥的PEM格式字符串
    :param data: 要加密的原始数据（字节类型）
    :return: 加密后的数据（字节类型，Base64编码后的结果方便展示和存储）
    """
    try:
        # 加载公钥
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode(), backend=default_backend()
        )
        # 使用OAEP填充方式进行加密（推荐用于RSA加密的填充方式）
        ciphertext = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        # 将加密后的字节数据进行Base64编码，方便后续存储、传输等处理
        return base64.b64encode(ciphertext)
    except Exception as e:
        print("rsa_encrypt error: {}".format(e))
        raise
