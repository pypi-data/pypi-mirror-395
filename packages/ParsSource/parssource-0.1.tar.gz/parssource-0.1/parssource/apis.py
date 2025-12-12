import httpx
from typing import Optional,Union
from .async_sync import *

class apis:
    def __init__(
        self,
        timeout: Optional[int] = 30
    ):
        self.timeout = timeout
        self.base_url = "https://api.ParsSource.ir"
        self.httpx_requests = httpx.AsyncClient()
    async def send_requests(self,method:str,inputs: Optional[dict] = None) -> dict:
        requests_url = f"{self.base_url}/{method}?"
        if inputs:
            for key,value in inputs.items():
                requests_url += f"&{key}={value}"
        response = await self.httpx_requests.get(requests_url,timeout=self.timeout)
        return response.json()
    @async_to_sync
    async def jok(self) -> dict:
        "جوک"
        return await self.send_requests("jok")
    @async_to_sync
    async def jok2(self) -> dict:
        "جوک دو"
        return await self.send_requests("jok2")
    @async_to_sync
    async def jok_pnp(self) -> dict:
        "جوک پ ن پ"
        return await self.send_requests("jok_pnp")
    @async_to_sync
    async def tts(self,text:str) -> dict:
        "تبدیل متن به صدا"
        return await self.send_requests("tts",{"text":text})
    @async_to_sync
    async def arz(self,name:str) -> dict:
        "ارز دیجیتال"
        return await self.send_requests("arz",{"name":name})
    @async_to_sync
    async def rubino_downloader(self,url:str) -> dict:
        "روبینو دانلودر"
        return await self.send_requests("rubino_downloader",{"url":url})
    @async_to_sync
    async def proxy(self) -> dict:
        "پروکسی تلگرام"
        return await self.send_requests("proxy")
    @async_to_sync
    async def cryptocurrency(self) -> dict:
        "کریپتو کارنسی"
        return await self.send_requests("cryptocurrency")
    @async_to_sync
    async def dollor_eur(self) -> dict:
        "دلار و یورو"
        return await self.send_requests("dollor_eur")
    @async_to_sync
    async def code_valid(self,code:str) -> dict:
        "وضعیت کد ملی"
        return await self.send_requests("code_valid",{"code":code})
    @async_to_sync
    async def random_music(self) -> dict:
        "موزیک تصادفی"
        return await self.send_requests("random_music")
    @async_to_sync
    async def diyalog(self) -> dict:
        "دیالوگ"
        return await self.send_requests("diyalog")
    @async_to_sync
    async def challenge(self) -> dict:
        "چالش"
        return await self.send_requests("challenge")
    @async_to_sync
    async def spokesperson(self,text:str) -> dict:
        "سخنگو"
        return await self.send_requests("spokesperson",{"text":text})
    @async_to_sync
    async def poem(self) -> dict:
        "شعر"
        return await self.send_requests("poem")
    @async_to_sync
    async def font(self,text:str) -> dict:
        "فونت"
        return await self.send_requests("font",{"text":text})
    @async_to_sync
    async def bio(self) -> dict:
        "بیو"
        return await self.send_requests("bio")
    @async_to_sync
    async def about_birth(self,birth:str) -> dict:
        "درباره تاریخ تولد"
        return await self.send_requests("about_birth",{"birth":birth})
    @async_to_sync
    async def calculator(self,calcu:str) -> dict:
        "ماشین حساب"
        calcu = calcu.replace(" ","")
        return await self.send_requests("calculator",{"calcu":calcu})
    @async_to_sync
    async def phototext(self,text:str) -> dict:
        "عکس متنی"
        return await self.send_requests("phototext",{"text":text})
    @async_to_sync
    async def news(self) -> dict:
        "اخبار"
        return await self.send_requests("news")
    @async_to_sync
    async def weater(self,name_city : str) -> dict:
        "آب و هوا"
        return await self.send_requests("weater",{"name_city":name_city})
    @async_to_sync
    async def search_music(self,name_music:str) -> dict:
        "جستجو موزیک"
        return await self.send_requests("search_music",{"name_music":name_music})
    @async_to_sync
    async def number_to_words(self,number:Union[int,str]) -> dict:
        "عدد به حروف عدد"
        return await self.send_requests("number_to_words",{"number":str(number)})
    @async_to_sync
    async def fohsh(self,text:str) -> dict:
        "تشخیص فحش"
        return await self.send_requests("fohsh",{"text":text})
    @async_to_sync
    async def fal(self) -> dict:
        "فال"
        return await self.send_requests("fal")
    @async_to_sync
    async def date(self) -> dict:
        "تاریخ"
        return await self.send_requests("date")
    @async_to_sync
    async def danestani(self) -> dict:
        "دانستنی"
        return await self.send_requests("danestani")
    @async_to_sync
    async def courage_truth(self) -> dict:
        "جرات و حقیقت"
        return await self.send_requests("courage_truth")
    @async_to_sync
    async def clock(self) -> bytes:
        "ساعت تصویری"
        response = await self.httpx_requests.get("https://api.ParsSource.ir/clock",timeout=self.timeout)
        return response.content
    @async_to_sync
    async def azan(self,name_city) -> dict:
        "اذان"
        return await self.send_requests("azan",{"name_city":name_city})
    @async_to_sync
    async def challange_tc(self) -> dict:
        "چالش تکنولوژی"
        return await self.send_requests("challange_tc")
    @async_to_sync
    async def chanllange_gym(self) -> dict:
        "چالش ورزشی"
        return await self.send_requests("chanllange_gym")