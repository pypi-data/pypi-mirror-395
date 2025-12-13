

def get_strategy(name, country):
    if name == "80/20/0/0 - local":
        res = {f'{country}_stocks': 0.8, f'{country}_bonds': 0.2}
    if name == "20/80/0/0 - local":
        res = {f'{country}_stocks': 0.2, f'{country}_bonds': 0.8}
    if name == "25/25/25/25 - local":
        res = {f'{country}_stocks': 0.25, f'{country}_bonds': 0.25, 
               f'{country}_realty': 0.25, f'{country}_money': 0.25}
    if name == "20/20/20/20/20 - local":
        res = {f'{country}_stocks': 0.2, f'{country}_bonds': 0.2, 
               f'{country}_realty': 0.2, f'{country}_money': 0.2,
               f'gold': 0.2}
    if name == "100/0/0/0 - local":
        res = {f'{country}_stocks': 1, f'{country}_bonds': 0, 
               f'{country}_realty': 0, f'{country}_money': 0}
    if name == "0/100/0/0 - local":
        res = {f'{country}_stocks': 0, f'{country}_bonds': 1, 
               f'{country}_realty': 0, f'{country}_money': 0}
    if name == "0/0/100/0 - local":
        res = {f'{country}_stocks': 0, f'{country}_bonds': 0, 
               f'{country}_realty': 1, f'{country}_money': 0}
    if name == "0/0/0/100 - local":
        res = {f'{country}_stocks': 0, f'{country}_bonds': 0, 
               f'{country}_realty': 0, f'{country}_money': 1}
    return {key+'_rt': val for key, val in res.items()}