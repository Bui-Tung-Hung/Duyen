import pandas as pd
import requests
import time
import random
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en,vi;q=0.9,vi-VN;q=0.8',
    'Referer': 'https://tiki.vn/nha-sach-tiki/c8322',
    'x-guest-token': '2eg3LBsfkKz7pVmEbIO0RGDJvyuAjq8P',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
    'cookies' : '_trackity=ed3a3fab-1c64-dc2a-90a8-1b295cf588de; TOKENS={%22access_token%22:%222eg3LBsfkKz7pVmEbIO0RGDJvyuAjq8P%22%2C%22expires_in%22:157680000%2C%22expires_at%22:1872394520776%2C%22guest_token%22:%222eg3LBsfkKz7pVmEbIO0RGDJvyuAjq8P%22}; delivery_zone=Vk4wNjcwMDcwMjY=; tiki_client_id=; TIKI_RECOMMENDATION=3c1cbf2a9169320a596dcef977415718; TKSESSID=f74f5d35109ffb184e445005d5f66241'
}
params = (
    ('platform', 'web'),
    ('spid','74021318'),
    ('version', '3')
)
    
def parser_product(json):
    d = dict()
    d['id'] =json.get('id')
    d['name'] =json.get('name')
    d['authors'] =json.get("authors", [{}])[0].get("name")
    d['original_price'] =json.get('original_price')
    d['price'] =json.get('price')
    d['categories'] = json.get("categories", {}).get("name")
    d['all_time_quantity_sold'] =json.get('all_time_quantity_sold')
    d['rating_average'] =json.get('rating_average')
    d['review_count'] =json.get('review_count')
    specifications = json.get("specifications", [])
    general_info = next((item for item in specifications if item.get("name") == "Thông tin chung"), {})
    attributes = general_info.get("attributes", [])
    d['pages'] = next((attr.get("value") for attr in attributes if attr.get("code") == "number_of_page"), None)
    d['manuafacture'] = next((attr.get("value") for attr in attributes if attr.get("code") == "manufacturer"), None)
    return d

df_id = pd.read_csv('productId_book.csv')
p_ids = df_id.id.to_list()
print(p_ids)
result =[]
for pid in tqdm(p_ids, total=len(p_ids)):
    response = requests.get('https://tiki.vn/api/v2/products/{}'.format(pid), headers=headers, params=params)
    if response.status_code == 200:
        try:
            # response.encoding = 'utf-8'
            print('Crawl data {} success !!!'.format(pid))
            result.append(parser_product(response.json()))
        except requests.exceptions.JSONDecodeError:
            print("Lỗi: Phản hồi không phải là JSON hợp lệ.")
            print("Nội dung phản hồi:", response.text) 
    else:
        print(f"Lỗi HTTP {response.status_code}: {response.reason}")

df_product = pd.DataFrame(result)
df_product.to_csv('productDetailData.csv', index = False)

