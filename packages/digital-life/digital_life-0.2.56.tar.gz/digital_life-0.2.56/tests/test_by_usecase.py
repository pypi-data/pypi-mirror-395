from pro_craft_infer.core import AsyncIntel
from pro_craft_infer.core import atest_by_use_case
from digital_life.core.memorycard import MemoryCardManager
from digital_life.core.user import UserInfo
import os

import pytest

class Test_UserInfo():
    @pytest.fixture
    def userinfo(self):
        return UserInfo(model_name="doubao-1-5-pro-32k-250115")

    async def test_relationship(self,userinfo):
        async def evals(result,inputs_dict):
            assert isinstance(result,dict)

        result,x = await atest_by_use_case(func=userinfo.auser_relationship_extraction,
                                eval=evals,
                                PASS_THRESHOLD_PERCENT=100,
                                database_url="mysql+aiomysql://" + os.getenv("log_database_url"))
        x and pytest.fail(f"测试 通过率不足 ")
        print(result)

    async def test_user_overview(self,userinfo):
        async def evals(result,inputs_dict):
            assert isinstance(result,str)

        result,x = await atest_by_use_case(func=userinfo.auser_overview,
                                eval=evals,
                                PASS_THRESHOLD_PERCENT=100,
                                database_url="mysql+aiomysql://" + os.getenv("log_database_url"))
        x and pytest.fail(f"测试 通过率不足 ")
        print(result)


from digital_life.core.memorycard import MemoryCardManager

class Test_MemoryCard():
    @pytest.fixture
    def manager(self):
        return MemoryCardManager(model_name="doubao-1-5-pro-32k-250115")

    async def test_ascore_from_memory_card(self,manager):
        async def evals(result,inputs_dict):
            try:
                assert isinstance(result,list)
            except AssertionError as e:
                raise AssertionError("测试未通过, 期望结果为 list")

        result,x = await atest_by_use_case(func=manager.ascore_from_memory_card,
                                eval=evals,
                                PASS_THRESHOLD_PERCENT=100,
                                database_url="mysql+aiomysql://" + os.getenv("log_database_url"))
        print(result)
        x and pytest.fail(f"测试 通过率不足 ")



    async def test_amemory_card_merge(self,manager):
        async def evals(result,inputs_dict):
            assert isinstance(result,dict)

        result,x = await atest_by_use_case(
                                func=manager.amemory_card_merge,
                                eval=evals,
                                PASS_THRESHOLD_PERCENT=100,
                                database_url="mysql+aiomysql://" + os.getenv("log_database_url"))
        print(result)
        x and pytest.fail(f"测试 通过率不足 ")
        

    async def test_amemory_card_polish(self,manager):
        async def evals(result,inputs_dict):
            assert isinstance(result,dict)
        
        result,x = await atest_by_use_case(
                                func=manager.amemory_card_polish,
                                eval=evals,
                                PASS_THRESHOLD_PERCENT=100,
                                database_url="mysql+aiomysql://" + os.getenv("log_database_url"))
        print(result)
        x and pytest.fail(f"测试 通过率不足 ")
        

    async def test_get_time(self,manager):
        async def evals(result,inputs_dict):
            assert isinstance(result,str)

        result,x = await atest_by_use_case(
                                func=manager.get_time,
                                eval=evals,
                                PASS_THRESHOLD_PERCENT=100,
                                database_url="mysql+aiomysql://" + os.getenv("log_database_url"))
        print(result)
        x and pytest.fail(f"测试 通过率不足 ")

    ##TODO

    async def test_agenerate_memory_card_by_text(self,manager):
        async def evals(result):
            assert isinstance(result,str)

        await atest_by_use_case(func=manager.agenerate_memory_card_by_text,
                                eval=evals,
                                PASS_THRESHOLD_PERCENT=100)


from digital_life.core.digital_avatar import DigitalAvatar


class Test_DigitalAvatar():
    @pytest.fixture
    def digital(self):
        return DigitalAvatar(model_name = "doubao-1-5-pro-32k-250115")

    async def test_desensitization(self,digital):
        async def evals(result):
            assert isinstance(result,dict)

        await atest_by_use_case(func=digital.desensitization,
                                eval=evals,
                                PASS_THRESHOLD_PERCENT=100)

    async def test_personality_extraction(self,digital):
        async def evals(result):
            assert isinstance(result,str)

        await atest_by_use_case(func=digital.personality_extraction,
                                eval=evals,
                                PASS_THRESHOLD_PERCENT=100)

    async def test_abrief(self,digital):
        async def evals(result):
            assert isinstance(result,str)

        await atest_by_use_case(func=digital.abrief,
                                eval=evals,
                                PASS_THRESHOLD_PERCENT=100)



async def test_1():
    MCmanager = MemoryCardManager(model_name="doubao-1-5-pro-32k-250115")
    async def evals(result):
        assert isinstance(result,str)

    x = await atest_by_use_case(func=MCmanager.get_time,
                               eval=evals,
                               PASS_THRESHOLD_PERCENT=90)
    


class Test_Evals:
    def __init__(self,model_name = "doubao-1-5-pro-256k-250115"):
        self.inters = AsyncIntel(model_name = model_name)



async def test_memory_card1():
    inters = AsyncIntel(model_name = "doubao-1-5-pro-32k-250115")
    await inters._evals(prompt_id="memorycard-generate-content",OutputFormat = Document,ExtraFormats_list = [Chapter])

    inters.df.to_csv("tests/memory_card.csv",index=False)
    inters.draw_data()

    

"""


    async def evals(self,save_path = None):
        await self.inters._evals(prompt_id="memorycard-score",OutputFormat = MemoryCardScore) # 单一型
        await self.inters._evals(prompt_id="memorycard-merge",OutputFormat = MemoryCard2)
        await self.inters._evals(prompt_id="memorycard-polish",OutputFormat = MemoryCard)
        
        await self.inters._evals(prompt_id="memorycard-format",OutputFormat = MemoryCardGenerate2)
   
        if save_path:
            self.inters.df.to_csv(save_path,index=False)
        
        self.inters.draw_data()
 


    async def evals(self,save_path = None):
        df = pd.DataFrame({"name":[],'status':[],"score":[],"total":[],"bad_case":[]})
        await self.inters._evals(prompt_id="user-overview",OutputFormat = ContentVer, df = df)
        await self.inters._evals(prompt_id="user-relationship-extraction",OutputFormat = CharactersData, df = df)
        await self.inters._evals(prompt_id="avatar-brief",OutputFormat = BriefResponse, df = df)
        # await self.inters._evals(prompt_id="avatar-personality-extraction",OutputFormat = "", df = df)
        await self.inters._evals(prompt_id="avatar-desensitization",OutputFormat = BriefResponse, df = df)



        
        if save_path:
            df.to_csv(save_path,index=False)
        
        self.draw_data(df=df)

    async def evals(self,save_path = None):
        df = pd.DataFrame({"name":[],'status':[],"score":[],"total":[],"bad_case":[]})
        await self.inters._evals(prompt_id="biograph_material_init",OutputFormat = "", df = df)
        await self.inters._evals(prompt_id="biograph_material_add",OutputFormat = "", df = df)
        await self.inters._evals(prompt_id="biograph-outline",OutputFormat = "what", df = df)
        await self.inters._evals(prompt_id="biograph-paid-title",OutputFormat = BiographPaidTitle, df = df)
        await self.inters._evals(prompt_id="biograph-brief",OutputFormat = "", df = df)
        await self.inters._evals(prompt_id="biograph-extract-person-name",OutputFormat = "", df = df)
        await self.inters._evals(prompt_id="biograph-extract-place",OutputFormat = "", df = df)
        await self.inters._evals(prompt_id="biograph-extract-material",OutputFormat = "", df = df)
        await self.inters._evals(prompt_id="biograph-writer",OutputFormat = "", df = df)
        await self.inters._evals(prompt_id="biograph-free-writer",OutputFormat = Biography_Free, df = df)
"""