import crcmod
import qrcode
import os


class Payload():
    def __init__(self, name, pix_key, value, city, txt_id, directory=''):
        self.name = name
        self.pix_key = pix_key
        self.value = value.replace(',', '.')
        self.city = city
        self.txt_id = txt_id
        self.qr_code_directory = directory

        self.name_len = len(self.name)
        self.pix_key_len = len(self.pix_key)
        self.value_len = len(self.value)
        self.city_len = len(self.city)
        self.txt_id_len = len(self.txt_id)

        self.merchant_account_len = f'0014br.gov.bcb.pix01{self.pix_key_len:02}{self.pix_key}'
        self.transaction_amount_len = f'{self.value_len:02}{float(self.value):.2f}'

        self.add_data_field_len = f'05{self.txt_id_len:02}{self.txt_id}'

        self.name_len = f'{self.name_len:02}'
        self.city_len = f'{self.city_len:02}'

        self.payload_format = '000201'
        self.point_of_initiation_method = '010211'
        self.merchant_account = f'26{len(self.merchant_account_len):02}{self.merchant_account_len}'
        self.merchant_category_code = '52040000'
        self.transaction_currency = '5303986'
        self.transaction_amount = f'54{self.transaction_amount_len}'
        self.country_code = '5802BR'
        self.merchant_name = f'59{self.name_len:02}{self.name}'
        self.merchant_city = f'60{self.city_len:02}{self.city}'
        self.add_data_field = f'62{len(self.add_data_field_len):02}{self.add_data_field_len}'
        self.crc16 = '6304'

    def generate_payload(self):
        self.payload = f'{self.payload_format}{self.point_of_initiation_method}{self.merchant_account}{self.merchant_category_code}{self.transaction_currency}{self.transaction_amount}{self.country_code}{self.merchant_name}{self.merchant_city}{self.add_data_field}{self.crc16}'
        self.generate_crc16(self.payload)

    def generate_crc16(self, payload):
        crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)

        self.crc16_code = hex(crc16(str(payload).encode('utf-8')))

        self.crc16_code_formatted = str(self.crc16_code).replace('0x', '').upper().zfill(4)

        self.complete_payload = f'{payload}{self.crc16_code_formatted}'

        self.generate_qr_code(self.complete_payload, self.qr_code_directory)

    def generate_qr_code(self, payload, directory):
        dir = os.path.expanduser(directory)
        self.qr_code = qrcode.make(payload)
        self.qr_code.save(os.path.join(dir, 'pixqrcode.png'))

        return print(payload)
