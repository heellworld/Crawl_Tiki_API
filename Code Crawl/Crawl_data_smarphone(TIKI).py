import pandas as pd
import requests
import time
import random
from tqdm import tqdm

cookies = {
    'TIKI_GUEST_TOKEN': '8jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY',
    'TOKENS': '{%22access_token%22:%228jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY%22%2C%22expires_in%22:157680000%2C%22expires_at%22:1763654224277%2C%22guest_token%22:%228jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY%22}',
    'amp_99d374': 'eSc-_0HT1um7cb57E7dwA0...1enloc6a2.1enlohtdv.3.2.5',
    'amp_99d374_tiki.vn': 'eSc-_0HT1um7cb57E7dwA0...1enloc6a2.1enlocds8.0.1.1',
    '_gcl_au': '1.1.559117409.1605974236',
    '_ants_utm_v2': '',
    '_pk_id.638735871.2fc5': 'b92ae025fbbdb31f.1605974236.1.1605974420.1605974236.',
    '_pk_ses.638735871.2fc5': '*',
    '_trackity': '70e316b0-96f2-dbe1-a2ed-43ff60419991',
    '_ga_NKX31X43RV': 'GS1.1.1605974235.1.1.1605974434.0',
    '_ga': 'GA1.1.657946765.1605974236',
    'ai_client_id': '11935756853.1605974227',
    'an_session': 'zizkzrzjzlzizqzlzqzjzdzizizqzgzmzkzmzlzrzmzgzdzizlzjzmzqzkznzhzhzkzdzhzdzizlzjzmzqzkznzhzhzkzdzizlzjzmzqzkznzhzhzkzdzjzdzhzqzdzizd2f27zdzjzdzlzmzmznzq',
    'au_aid': '11935756853',
    'dgs': '1605974411%3A3%3A0',
    'au_gt': '1605974227146',
    '_ants_services': '%5B%22cuid%22%5D',
    '__admUTMtime': '1605974236',
    '__iid': '749',
    '__su': '0',
    '_bs': 'bb9a32f6-ab13-ce80-92d6-57fd3fd6e4c8',
    '_gid': 'GA1.2.867846791.1605974237',
    '_fbp': 'fb.1.1605974237134.1297408816',
    '_hjid': 'f152cf33-7323-4410-b9ae-79f6622ebc48',
    '_hjFirstSeen': '1',
    '_hjIncludedInPageviewSample': '1',
    '_hjAbsoluteSessionInProgress': '0',
    '_hjIncludedInSessionSample': '1',
    'tiki_client_id': '657946765.1605974236',
    '__gads': 'ID=ae56424189ecccbe-227eb8e1d6c400a8:T=1605974229:RT=1605974229:S=ALNI_MZFWYf2BAjzCSiRNLC3bKI-W_7YHA',
    'proxy_s_sv': '1605976041662',
    'TKSESSID': '8bcd49b02e1e16aa1cdb795c54d7b460',
    'TIKI_RECOMMENDATION': '21dd50e7f7c194df673ea3b717459249',
    '_gat': '1',
    'cto_bundle': 'i6f48l9NVXNkQmJ6aEVLcXNqbHdjcVZoQ0k2clladUF2N2xjZzJ1cjR6WG43UTVaRmglMkZXWUdtRnJTNHZRbmQ4SDAlMkZwRFhqQnppRHFxJTJCSEozZXBqRFM4ZHVxUjQ2TmklMkJIcnhJd3luZXpJSnBpcE1nJTNE',
    'TIKI_RECENTLYVIEWED': '58259141',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Referer': 'https://tiki.vn/dien-thoai-oppo-a17k-3gb-64gb-hang-chinh-hang-p203853390.html?spid=203853394',
    'x-guest-token': '167AgdBpHNqmzc3Zai8EJjLQk4DuYXW9',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = (
    ('platform', 'web'),
    ('spid', 203853394)
    #('include', 'tag,images,gallery,promotions,badges,stock_item,variants,product_links,discount_tag,ranks,breadcrumbs,top_features,cta_desktop'),
)

def parser_product(json):
    d = dict()
    d['id'] = json.get('id')
    d['sku'] = json.get('sku')
    d['description'] = json.get('description')
    d['short_description'] = json.get('short_description')
    d['price'] = json.get('price')
    d['list_price'] = json.get('list_price')

    # Xử lý cho 'quantity_sold'
    quantity_sold = json.get('quantity_sold')
    d['quantity_sold'] = quantity_sold.get('value') if quantity_sold else None

    d['favourite_count'] = json.get('favourite_count')
    d['discount'] = json.get('discount')
    d['discount_rate'] = json.get('discount_rate')
    d['review_count'] = json.get('review_count')
    d['rating_average'] = json.get('rating_average')
    d['inventory_status'] = json.get('inventory_status')
    d['is_visible'] = json.get('is_visible')

    # Xử lý cho 'stock_item'
    stock_item = json.get('stock_item')
    d['stock_item_qty'] = stock_item.get('qty') if stock_item else None
    d['stock_item_max_sale_qty'] = stock_item.get('max_sale_qty') if stock_item else None

    d['product_name'] = json.get('meta_title')

    # Xử lý cho 'brand'
    brand = json.get('brand')
    d['brand_id'] = brand.get('id') if brand else None
    d['brand_name'] = brand.get('name') if brand else None

    return d


df_id = pd.read_csv('product_id_smarphone.csv')
p_ids = df_id.id.to_list()
print(p_ids)
result = []
for pid in tqdm(p_ids, total=len(p_ids)):
    response = requests.get('https://tiki.vn/api/v2/products/{}'.format(pid), headers=headers, params=params, cookies=cookies)
    if response.status_code == 200:
        print('Crawl data {} success !!!'.format(pid))
        result.append(parser_product(response.json()))
    time.sleep(random.randrange(3, 5))

df_product = pd.DataFrame(result)
df_product.to_csv('crawled_data_smarphones.csv', index=False, encoding='utf-8')
