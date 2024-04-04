import json
import requests


from yandexgptlite import YandexGPTLite
account = YandexGPTLite('b1gd73t8icljbi3n5jnm',
                        'y0_AgAAAAA8mYxyAATuwQAAAAEA4VtUAACenuIdFgtGrKt6F_TFoBQ-tX8r2Q')

text = account.create_completion(update.message.text, '0.6', system_prompt = 'отвечай на русском')
print(text)

