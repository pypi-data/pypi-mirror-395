import os
import time
import json
import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class RSAM:
    @staticmethod
    def rsacontent(filepath: str, noheader: bool=False) -> bytes:
        """
        获取RSA密钥文本
        @param filepath: RSA密钥文本
        @param noheader: 返回不携带 密钥头儿 的RSA密钥文本
        @return: RSA密钥文本
        """
        with open(filepath, mode='r') as f:
            content = f.read()
        print(content)
        print('-' * 50)
        rsaheader = "-----BEGIN PRIVATE KEY-----"
        rsafooter = "-----END PRIVATE KEY-----"
        text = "".join(content.split('\n')).strip(rsaheader).strip(rsafooter).strip()
        content = text if noheader else "\n".join([rsaheader, text, rsafooter])
        return content

    @staticmethod
    def rsac2obj(content: str, noheader: bool=False) -> bytes:
        """
        根据RSA密钥文本获取RSA密钥对象
        @param content: RSA密钥文本
        @param noheader: 传入的RSA密钥文本未携带RSA密钥头儿
        @return: RSA密钥对象
        """
        rsaheader = "-----BEGIN PRIVATE KEY-----"
        rsafooter = "-----END PRIVATE KEY-----"
        content = content if not noheader else "\n".join([rsaheader, content, rsafooter])
        return RSA.import_key(content.encode("utf-8"))

    @staticmethod
    def rsaobj(filepath: str) -> bytes:
        """
        获取RSA密钥对象
        @param filepath: RSA密钥文件路径
        @return: RSA密钥对象
        """
        with open(filepath, mode='rb') as f:
            return RSA.import_key(f.read())


    @staticmethod
    def signature(rsaKey: bytes, data: dict, ensure_ascii=False) -> str:
        """
        根据RSA私钥获取签名值
        """
        pkcs = PKCS1_v1_5.new(rsaKey)
        data_bytes = json.dumps(data, separators=(',', ':'), ensure_ascii=ensure_ascii).encode('utf-8')
        sha256 = SHA256.new(data_bytes)
        signature = base64.b64encode(pkcs.sign(sha256)).decode('utf-8')
        return signature

    @staticmethod
    def verify(rsaKey: bytes, data: dict, signature: str, ensure_ascii=False) -> bool:
        """
        根据RSA公钥获取签名验证结果
        """
        pkcs = PKCS1_v1_5.new(rsaKey)
        signature_hash = base64.b64decode(signature)
        data_bytes = json.dumps(data, separators=(',', ':'), ensure_ascii=ensure_ascii).encode('utf-8')
        sha256 = SHA256.new(data_bytes)
        result = pkcs.verify(sha256, signature_hash)
        return result

    @staticmethod
    def genRSAKey(savepath: str, key_size: int = 2048, pkcs=8, subdir: str = None, prefix: str = None):
        """
        生成RSA密钥
        @return: 返回生成的密钥内容
        """
        savepath = savepath if savepath.endswith("/") else savepath + "/"
        savepath = savepath + f'{str(int(time.time()))}/' if subdir is None else savepath + f"{subdir}/"
        try:
            os.makedirs(savepath, exist_ok=True)
            key = RSA.generate(key_size)
            private_key = key.export_key(format="PEM", pkcs=pkcs)
            public_key = key.publickey().export_key(format="PEM")

            prikeypath = f"{savepath}/prikey.pem" if prefix is None else f"{savepath}/{prefix}_prikey.pem"
            pubkeypath = f"{savepath}/pubkey.pem" if prefix is None else f"{savepath}/{prefix}_pubkey.pem"
            with open(prikeypath, "wb") as f:
                f.write(private_key)
            with open(pubkeypath, "wb") as f:
                f.write(public_key)

            return {
                "priKey": private_key,
                "pubKey": public_key
            }
        except Exception as e:
            raise RuntimeError(f"生成RSA密钥失败: {e}")
    

    


if __name__ == '__main__':
    # a = "/Users/lizhankang/Documents/shouqianba/pems/ka/beta/未命名文件夹/client/priKey.pem"
    # c1 = RSAM.rsacontent(a)
    # print(c1)
    # c2 = RSAM.rsacontent(a, noheader=True)
    # print(c2)

    # o1 = RSAM.rsac2obj(c1)
    # o2 = RSAM.rsac2obj(c2, noheader=True)
    # print(c1)
    # print(c2)

    RSAM.genRSAKey("/Users/lizhankang/Documents/shouqianba/pems/ka/beta/未命名文件夹 2")

