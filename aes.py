import json
import base64

from Crypto.Cipher import AES
# import execjs
#
# def js_aes(key,iv,text):
#     """js 实现aes加密"""
#     jscode = """function encrypt(a, b, iv) {
#         var CryptoJS = require("crypto-js");
#         var c = CryptoJS.enc.Utf8.parse(b),
#             d = CryptoJS.enc.Utf8.parse(iv),
#             e = CryptoJS.enc.Utf8.parse(a),
#             f = CryptoJS.AES.encrypt(e, c, {
#                 iv: d,
#                 mode: CryptoJS.mode.CBC,
#                 padding: CryptoJS.pad.Pkcs7
#             });
#         return f.toString()
#     }"""
#     ctx = execjs.compile(jscode)
#     encrypt_text = ctx.call("encrypt",text,key,iv)
#     return encrypt_text


class MyCrypto():
    """ python aes 加密"""
    def encrypt(self, key, iv, instr):
        mystr = self._pad(instr)
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        ret = base64.b64encode(cipher.encrypt(mystr)).decode('utf-8')
        return ret

    def decrypt(self, key, iv, encryptedData):
        encryptedData = base64.b64decode(encryptedData)
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        ret = self._unpad(cipher.decrypt(encryptedData))
        ret = ret.decode(encoding="utf-8")
        return ret

    def _pad(self, s):
        BS = AES.block_size
        s = s.encode("utf-8")
        return s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode("utf-8")

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


if __name__ == "__main__":
    iv = "0102030405060708"
    key = "0CoJUm6Qyw8W8jud"
    data = {"ids":"[436514312]","level":"standard","encodeType":"aac","csrf_token":""}
    text = json.dumps(data).replace(' ','')

    # print(js_aes(key,iv,text))
    obj = MyCrypto()
    encrypt_text = obj.encrypt(key,iv,text)
    print(encrypt_text)
    print(obj.decrypt(key,iv,encrypt_text))