import pathlib
import pickle
import secrets
from dataclasses import dataclass, asdict
from checklib import *
from typing import List




@dataclass
class Merch:
    # id          : int = 0
    name        : str = ''
    description : str = ''
    price       : int = ''
    NFTToken    : str = ''
    picture     : str = ''
    
    def __eq__(self, other):
        if self.name == other.name \
            and self.description == other.description \
                and self.price == other.price \
                        and self.picture == other.picture:
                            return True
                    
   
@dataclass
class Cart:
    total_quantity : int
    price          : int
    Goods          : List[Merch] = None
    
@dataclass
class Order:
    status : str
    cart_id : int

@dataclass
class User:
    username  : str
    password  : str
    cash      : int = 0
    flag      : str = ''
    status    : str = ''

class CheckMachine:
    
    def __init__(self, host, *, port = 80):
        self.url = f'http://{host}:{port}'
    
    def __enter__(self) -> 'CheckMachine':
        self.s = get_initialized_session()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.s.close()
    
    def register(self, user : User, *, status = Status.MUMBLE):
        return self.s.post(f'{self.url}/api/v1/register', json=asdict(user))
            
        
    def login(self, user : User, *, status = Status.MUMBLE):
        return self.s.post(f'{self.url}/api/v1/login', json={"username": user.username, "password": user.password})
    
	# router.HandleFunc("/api/v1/change-password", h.ChangePassword).Methods(http.MethodPost)
	# router.HandleFunc("/api/v1/profile", h.UpdateProfile).Methods(http.MethodPut)
	# router.HandleFunc("/api/v1/catalogue/{page}", h.GetPage).Methods(http.MethodGet)
    def add_merch(self, merch : Merch):
        return self.s.post(f'{self.url}/api/v1/my_merchandise', json=asdict(merch))
    
    def get_my_merch(self, id : int):
        return self.s.get(f'{self.url}/api/v1/my_merchandise?id={id}')
    
    def get_merch(self, id : int):
        return self.s.get(f'{self.url}/api/v1/merchandise?id={id}')
    
    def get_profile(self):
        return self.s.get(f'{self.url}/api/v1/profile')
    
    def create_order(self, cartID):
        return self.s.post(f'{self.url}/api/v1/order', json=asdict(Order("created", cartID)))
    
    def get_order(self, orderID):
        return self.s.get(f'{self.url}/api/v1/order?id={orderID}')
    
    def add_to_cart(self, id):
        return self.s.put(f'{self.url}/api/v1/cart?id={id}')
    
    def get_cart(self):
        return self.s.get(f'{self.url}/api/v1/cart')

    def buy(self, order):
        return self.s.post(f'{self.url}/api/v1/buy', json=order)
    
    def get_main_page(self, page_num):
        return self.s.get(f'{self.url}/api/v1/catalogue/page={page_num}')
    
    @staticmethod
    def generate_user(*, flag = None):
        username = rnd_username()
        password = rnd_password()
        if flag:
            return User(username, password, 0, flag, "keeping secrets")
        return User(username=username, password=password, flag='No flag here!')
    
    @staticmethod
    def generate_merch(*, flag = 'No flag in this one!'):
        images = [
            "https://avatars.mds.yandex.net/get-shedevrum/12365046/6efcae0ab6f211ee8efed65bcdbc3dcb/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/11465050/8dfd36e8b53d11ee8f7e5a76f5576984/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/12994731/3f419831ccdd11ee872126d079e580b2/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/12423216/img_6b9ce9b0eab611eea24dbe62f04505c7/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/12365046/acc5f6b2ccdb11ee9543aa2339796401/orig",
            "https://masterpiecer-images.s3.yandex.net/a68ff01798a511eeae815601f9285731:upscaled",
            "https://masterpiecer-images.s3.yandex.net/8ddfc95a6dc711ee96827a2f0d1382ba:upscaled",
            "https://avatars.mds.yandex.net/get-shedevrum/12370990/876ea293ccd911eeb988a66c16f5f670/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/11509417/img_23503c40f0d311eeac743e2976af6506/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/12933433/74f17ab3ccd811ee92e70a0d9f74bed2/orig",
            "https://masterpiecer-images.s3.yandex.net/f43cf11c7b4a11eeb55ad659965eed18:upscaled",
            "https://avatars.mds.yandex.net/get-shedevrum/11270697/5b013fb5be9b11ee8a3c7ab0f2fccf97/orig",
            "https://masterpiecer-images.s3.yandex.net/f2ad590071a011eeb09daaafe6635749:upscaled",
            "https://avatars.mds.yandex.net/get-shedevrum/11473245/49fbffc6de4911eebd771ad242dc1d78/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/12363575/02c82459cdc411eeae86f64e44184dca/orig",
            "https://masterpiecer-images.s3.yandex.net/37b8fa8d628711eebc9a363fac71b015:upscaled",
            "https://masterpiecer-images.s3.yandex.net/f3ea707c429511ee9e9a3a7ca4cc1bdc:upscaled",
            "https://masterpiecer-images.s3.yandex.net/9a9f516742b811eebbcc3e94d70b2e0e:upscaled",
            "https://masterpiecer-images.s3.yandex.net/e15ca706429211ee80636e855efad8a9:upscaled",
            "https://masterpiecer-images.s3.yandex.net/6af6468f443811ee80c89a793c1e62bc:upscaled",
            "https://masterpiecer-images.s3.yandex.net/1d2a8b56429a11ee9ac206311dffedfc:upscaled",
            "https://masterpiecer-images.s3.yandex.net/c2e792fe2b4411ee80b756181a0358a2:upscaled",
            "https://masterpiecer-images.s3.yandex.net/f0080f5a896a11eeb80b2ab2a9c6ab46:upscaled",
            "https://masterpiecer-images.s3.yandex.net/22c24bdf74cb11ee8ab32aa0df1cd6e5:upscaled",
            "https://masterpiecer-images.s3.yandex.net/5fb34d2d1e7c5ce:upscaled",
            "https://masterpiecer-images.s3.yandex.net/adf78186630c11ee8c6d168cdf1572ce:upscaled",
            "https://masterpiecer-images.s3.yandex.net/1cae3f8e5bb911ee9f394659bdca6a39:upscaled",
            "https://masterpiecer-images.s3.yandex.net/43f348a2976811ee85b4b646b2a0ffc1:upscaled",
            "https://masterpiecer-images.s3.yandex.net/ee6c5de9835e11eeb51d222e7fa838a6:upscaled",
            "https://avatars.mds.yandex.net/get-shedevrum/12933433/img_de40eed1ec7d11eeb8cd3259d2b46770/orig",
            "https://masterpiecer-images.s3.yandex.net/152821df7bb111ee9eb2ceda526c50ab:upscaled",
            "https://masterpiecer-images.s3.yandex.net/4641f3d8322d11ee9c0c56181a0358a2:upscaled",
            "https://avatars.mds.yandex.net/get-shedevrum/12423216/img_6b9ce9b0eab611eea24dbe62f04505c7/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/12367607/7c1cf3d5c6c211ee9dde5e32ab44ab44/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/11270697/7931f114e87411ee85932aac36e16415/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/12154803/1b03b714d7ac11ee9af71e2d0b427d15/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/11425623/89016ebedabf11ee8784568224083d35/orig",
            "https://masterpiecer-images.s3.yandex.net/c2fd94aa6f6211ee8bacaaafe6635749:upscaled",
            "https://masterpiecer-images.s3.yandex.net/df3591fe786d11eea0445696910b1137:upscaled",
            "https://masterpiecer-images.s3.yandex.net/8b5e5dbc87e711eeb91a429f31467427:upscaled",
            "https://avatars.mds.yandex.net/get-shedevrum/12165876/b3a950c0cf4c11ee9db2faa0c08f8d07/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/12151221/e414f154de9011ee9f63aa8321cbabb8/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/12151221/img_6bd5d313f2a311ee8aee0272250bcc9d/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/12368819/0059cef4d24f11eeb109c62cc9ee863f/orig",
            "https://avatars.mds.yandex.net/get-shedevrum/11509417/203f0a23bbfa11ee8ad7ced9e91a1749/orig",
            "https://masterpiecer-images.s3.yandex.net/cba3e530981411ee8799c66dc44e86ec:upscaled",
            "https://masterpiecer-images.s3.yandex.net/c9c3e40a84b811ee8c79363fac71b015:upscaled",
            "https://avatars.mds.yandex.net/get-shedevrum/10502823/7f47bb26c0d411eea5f95e02d8de8a56/orig",
            "https://masterpiecer-images.s3.yandex.net/aea5814a82d911ee8852261105627a54:upscaled",
            "https://masterpiecer-images.s3.yandex.net/8d0d9e5b378b11ee910f8e6d7e0d9e35:upscaled",
            "https://masterpiecer-images.s3.yandex.net/39ddbf8d9d9611ee87a52e52115ec7ec:upscaled",
            "https://masterpiecer-images.s3.yandex.net/6227d129495411ee9d558e3ad859c919:upscaled",
            "https://masterpiecer-images.s3.yandex.net/a191dbf7680011ee80aab646b2a0ffc1:upscaled",
            "https://masterpiecer-images.s3.yandex.net/457087bd8a7911eea1491ad242dc1d78:upscaled"
        ]
        price = {'mythical': 1000, 
                 'uncommon': 200, 
                 'rare' : 500, 
                 'legendary' : 1500, 
                 'common' : 100, 
                 'discontinued' : 8000, 
                 'ancient' : 2000}
        PATH = pathlib.Path(__file__).parent.resolve()
        with open(f"{PATH}/skins.pickle", 'rb') as f:
            skins_info =  pickle.load(f)
        s = secrets.choice(skins_info)
        i = secrets.choice(images)
        if flag:
            return Merch(s[1], f'Get this {s[0]} skin and you would not regret it!', price[s[0]], flag, i)
        return Merch(s[1], f'Get this {s[0]} skin and you would not regret it!', price[s[0]], "No flag here!", i)