from modusched.core import ArkAdapter
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
# import biography_data
import re
import json
import asyncio
import httpx

from digital_life.redis_ import get_redis_client, store_with_expiration, get_value
from pydantic import BaseModel, Field
from pro_craft_infer.core import AsyncIntel, create_async_session
from digital_life import logger
from digital_life.log import log_func
# === 主题映射 ===
THEME_MAP = {
    "1": "出身与童年",
    "2": "学习与成长",
    "3": "事业与成就",
    "4": "家庭与情感",
    "5": "生活与体验"
}

#数字映射表
num_to_chinese = {
    1: "一", 2: "二", 3: "三", 4: "四", 5: "五",
    6: "六", 7: "七", 8: "八", 9: "九", 10: "十",
    11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五",
    16: "十六", 17: "十七", 18: "十八", 19: "十九",
    20: "二十", 21: "二十一", 22: "二十二", 23: "二十三", 24: "二十四", 25: "二十五",
    26: "二十六", 27: "二十七", 28: "二十八", 29: "二十九",
    30: "三十", 31: "三十一", 32: "三十二", 33: "三十三", 34: "三十四", 35: "三十五",
    36: "三十六", 37: "三十七", 38: "三十八", 39: "三十九",
    40: "四十", 41: "四十一", 42: "四十二", 43: "四十三", 44: "四十四", 45: "四十五",
    46: "四十六", 47: "四十七", 48: "四十八", 49: "四十九",
    50: "五十", 51: "五十一", 52: "五十二", 53: "五十三", 54: "五十四", 55: "五十五",
    56: "五十六", 57: "五十七", 58: "五十八", 59: "五十九",
    60: "六十", 61: "六十一", 62: "六十二", 63: "六十三", 64: "六十四", 65: "六十五",
    66: "六十六", 67: "六十七", 68: "六十八", 69: "六十九",
    70: "七十", 71: "七十一", 72: "七十二", 73: "七十三", 74: "七十四", 75: "七十五",
    76: "七十六", 77: "七十七", 78: "七十八", 79: "七十九",
    80: "八十", 81: "八十一", 82: "八十二", 83: "八十三", 84: "八十四", 85: "八十五",
    86: "八十六", 87: "八十七", 88: "八十八", 89: "八十九",
    90: "九十", 91: "九十一", 92: "九十二", 93: "九十三", 94: "九十四", 95: "九十五",
    96: "九十六", 97: "九十七", 98: "九十八", 99: "九十九",
    100: "一百"
}



async def aget_(url = ""):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # 如果状态码是 4xx 或 5xx，会抛出 HTTPStatusError 异常
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.json()}") # 假设返回的是 JSON
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    return None


def extract_from_text(text: str):
    matches = []
    for match in re.finditer(r'!\[\]\(([^)]+)\)', text):
        url = match.group(1).strip()
        position = match.start()
        matches.append((url, position))
    return matches



user_callback_url = os.getenv("user_callback_url")


class BiographGenerateError(Exception):
    pass

def remove_urls_from_text(text: str) -> str:
    """
    检测文本中的 Markdown 格式图片链接 (![]()) 并将其剔除。

    Args:
        text: 待处理的字符串。

    Returns:
        剔除了 Markdown 格式图片链接的字符串。
    """
    # 使用 re.sub 替换所有匹配的模式为空字符串
    # r'!\[\]\([^)]+\)' 匹配 ![]() 结构，其中括号内的内容是 URL
    cleaned_text = re.sub(r'!\[\]\([^)]+\)', '', text)
    return cleaned_text


def extract_json(text: str) -> str:
    """从文本中提取python代码
    Args:
        text (str): 输入的文本。
    Returns:
        str: 提取出的python文本
    """
    pattern = r"```json([\s\S]*?)```"
    matches = re.findall(pattern, text)
    if matches:
        return matches[0].strip()  # 添加strip()去除首尾空白符
    else:
        return ""  # 返回空字符串或抛出异常，此处返回空字符串

#筛选对应模块函数
def filter_memory_cards_by_theme(data, theme_id):
    """
    从 data 中筛选出指定 theme_id 的记忆卡片

    参数:
        data (dict): 包含 'memory_cards' 键的字典
        theme_id (str 或 int): 要筛选的主题 ID

    返回:
        list: 所有指定 theme_id 的记忆卡片
    """
    # 确保 theme_id 为字符串（因为 data 里是字符串）
    theme_id_str = str(theme_id)

    # 获取 memory_cards 列表
    cards = data.get("memory_cards", [])

    # 筛选符合条件的卡片
    return [card for card in cards if card.get("theme_id") == theme_id_str]



class BiographyAgent():
    def __init__(self,memory_cards,username,vitae,intels = None,
                 api_key: str = None, 
                 model_name: str = ""):
        self.ark = ArkAdapter(model_name, api_key=api_key or os.getenv("ARK_API_KEY"))
        self.model_name = model_name
        self.inters = AsyncIntel(model_name = model_name,logger=logger)

        #***输入参数***
        # self.intels = intels
        #记忆卡片
        self.memory_cards = memory_cards
        #用户姓名
        self.username = username
        #用户简历
        self.vitae = vitae

        #***中间参数****
        #传记整体素材
        self.biography_material_all = ""
        #传记核心主题
        self.biography_theme = ""
        #传记目录
        # self.TOC = [{"juanming":"neirong","juanneirong":[str0,str1]},{"juanming":"neirong","juanneirong":[str0,str1]}]
        self.TOC =[]


        #整理素材-分类
        self.expand_result = {}

        #撰写计划-卷名-章节名-每章撰写概要
        #传记撰写计划
        self.plan = []

        #撰写事件-以时间顺序排序。
        self.event = {}

        #提示词目录
        current_dir = os.path.dirname(os.path.abspath(__file__))  # core目录
        self.prompt_uri = os.path.join(current_dir, "prompt")

        #章节数量
        self .text_id = 0

        #****输出参数****
        #传记题目
        self.biography_title = ""
        #传记中人名
        self.biography_name = []
        #传记中地名
        self.biography_place = []
        #输出传记
        self.biography_text_json = {}
        self.biography_prologue_json = {}
        self.biography_final_json = {}
        self.biography_json = {}
        #传记概要
        self.biography_brief = ""

        #输出结构体
        self.biography = {}

    async def llm_run(self, user_prompt: str = "",system_prompt: str = "") -> str:
        """
        运行大模型推理任务（LLM Run）。

        参数:
            user_prompt (str): 用户提示词，用于存储用户输入模板。

        返回:
            str: 模型输出结果。
        """
        try:
            # 模拟或扩展实际 LLM 调用逻辑
            data = {
                "model": self.model_name,
                "messages": [
                            {"role": "system", "content":system_prompt},
                            {"role": "user", "content": user_prompt},],
            }
            result = await self.ark.client.arequest(data)
            return result.choices[0].message.content

        except Exception as e:
            # 错误处理：打印日志并返回安全提示
            raise Exception(f"Error running LLM: {e}")

    async def material_all_agent(self):
        """
        传记整体素材获取，

        输入全部记忆卡片，
        输出
            人物介绍
                基本信息
                人物标签
                核心愿景
            人生主线
            人物思想历程

        """

        async with create_async_session(self.inters.engine) as session:
            result_obj = await self.inters.get_prompt(prompt_id="人物信息素材整理",session=session)
            material_all_prompt = result_obj.prompt


        #输入参数
        user_prompt = "用户姓名："+str(self.username)+",用户简历："+str(self.vitae)+",记忆卡片："+str(self.memory_cards)
        self.biography_material_all = await self.llm_run(str(user_prompt),system_prompt= material_all_prompt)

        return self.biography_material_all

    async def theme_agent(self):
        """
        传记主题获取，

        输入传记整体素材

        输出传记主题
        Returns:

        """

        async with create_async_session(self.inters.engine) as session:
            result_obj = await self.inters.get_prompt(prompt_id="传记主题获取",session=session)
            biography_theme_prompt = result_obj.prompt

        #输入参数
        user_prompt = str(self.biography_material_all)
        self.biography_theme = await self.llm_run(str(user_prompt),system_prompt= biography_theme_prompt)

        return self.biography_theme

    async def expand_cards_agent(self):
        """
        用法：
            扩展记忆卡片，对每个记忆卡片补充背景信息，并根据核心主题判断撰写程度。
            自动匹配对应主题的提示词文件，多线程并行处理以加速执行。

        输入参数：
            self.memory_cards: List[Dict] 记忆卡片
            self.biography_theme: str 传记主题
            self.biography_material_all: List[Dict] 所有素材

        返回参数：
            expand_result: Dict[str, List[Dict]]
                {
                  "出身与童年": [ {...}, {...} ],
                  "学习与成长": [ {...} ],
                  "事业与成就": [],
                  "家庭与情感": [],
                  "生活与体验": []
                }
        """

        # === 1. 初始化结果结构 ===
        self.expand_result = {theme_name: [] for theme_name in THEME_MAP.values()}

        # === 2. 定义处理单张卡片的函数 ===
        async def process_card(card):
            theme_id = card.get("theme_id")
            theme_name = THEME_MAP.get(theme_id)

            if not theme_name:
                print(f"未识别的 theme_id={theme_id}，跳过该卡片。")
                return None, None

            # === 3. 自动构建提示词文件路径 ===
            prompt_file = f"{theme_name}卡片补充"

            # === 4. 读取系统提示词 ===
            async with create_async_session(self.inters.engine) as session:
                result_obj = await self.inters.get_prompt(prompt_id=prompt_file,session=session)
                system_prompt = result_obj.prompt

            # === 6. 构建输入参数 ===
            user_prompt = (
                f"记忆卡片：{card}\n"
                f"整体素材：{self.biography_material_all}\n"
                f"传记主题：{self.biography_theme}"
            )

            # === 7. 调用模型，生成扩展结果 ===
            #有个坑需要处理一下，输出的json可能解析不了。
            expand_card = await self.llm_run(user_prompt,  system_prompt=system_prompt)
            try:
                print(f"补充记忆卡片xvvb：{expand_card}")
                expand_card = json.loads(extract_json(expand_card))

            except:
                print(f"记忆卡片背景补充格式错误：{expand_card},输出原始记忆卡片")
                #输出原始的记忆卡片，处理失败则输出原始卡片，不要让数据丢失
                expand_card = card


            return theme_name, expand_card

        tasks = []
        for card in self.memory_cards:
            tasks.append(
                process_card(card)
            )
        results = await asyncio.gather(*tasks, return_exceptions=False)
        for theme_name, expand_card in results:
            if theme_name and expand_card:
                self.expand_result[theme_name].append(expand_card)

        # # === 3. 并行执行所有卡片扩展 ===
        # with ThreadPoolExecutor(max_workers=5) as executor:
        #     future_to_card = {executor.submit(process_card, card): card for card in self.memory_cards}

        #     for future in as_completed(future_to_card):
        #         theme_name, expand_card = future.result() if future.result() else (None, None)
        #         if theme_name and expand_card:
        #             self.expand_result[theme_name].append(expand_card)

        # === 4. 返回统一结构 ===
        return self.expand_result

    async def event_sort_agent(self):
        """
        功能：事件排序代理
        输入：
            - self.expand_result：记忆卡片（已按模块分类整理补充）
            - self.resume_info：用户简历（用于辅助排序）
        输出：
            {
                "出身与童年": "",
                "学习与成长": "",
                "事业与成就": "",
                "家庭与情感": "",
                "生活与体验": ""
            }
        """

        # # === 初始化输出结构 ===
        self.event = {name: "" for _, name in THEME_MAP.items()}

        # === 遍历每个模块 ===
        for theme_id, theme_name in THEME_MAP.items():
            # 如果没有对应的卡片，跳过
            if not self.expand_result or theme_name not in self.expand_result:
                continue

            # 取出该模块的记忆卡片
            cards = self.expand_result[theme_name]
            if not cards:
                continue

            # === 构建提示词路径 ===
            prompt_file = f"{theme_name}事件梳理"

            # 读取提示词文件
            
            async with create_async_session(self.inters.engine) as session:
                result_obj = await self.inters.get_prompt(prompt_id=prompt_file,session=session)
                system_prompt = result_obj.prompt

            # 初始化本卷 LLM

            # 构建user_prompt
            prompt = (
                f"主人公简历：{self.vitae}简历只需要参考，用于计算事件的时间\n"
                f"记忆卡片：{cards}\n"
            )

            # 执行大模型
            Event_LLM_out = await self.llm_run(prompt,  system_prompt=system_prompt)
            # Event_LLM_out结构为 "[ {"发生时间":"","事件具体内容":""}, ... ]"
            self.event[theme_name] = Event_LLM_out

        return self.event


    async def biography_plan_agent(self, theme_ids=None):
        """
        异步整理撰写规划。
        输入：
            传记主题、整体素材、扩展完成的记忆卡片（self.expand_result）。
            可通过 theme_ids 指定要处理的主题编号列表（如 ["1", "2"]）。
        输出：
            写作规划（卷名、章节概要、补充的记忆卡片、每章要写的概要）。
            返回格式：
            {
                "出身与童年": { "卷名": "童年与成长", "章节列表": [ {"章节名": "", "撰写内容概要": ""}, {"章节名": "", "撰写内容概要": ""} ] },
                "学习与成长": {...},
                "事业与成就": {...},
                "家庭与情感": {...},
                "生活与体验": {...}
            }
        """

        # === 1. 默认处理全部主题 ===
        if theme_ids is None:
            theme_ids = list(THEME_MAP.keys())
        # === 2. 读取系统提示词 ===
        async with create_async_session(self.inters.engine) as session:
            result_obj = await self.inters.get_prompt(prompt_id="卷名与章节规划",session=session)
            biography_Plan_prompt = result_obj.prompt

        # === 3. 构建基础提示内容 ===
        user_prompt_base = (
                f"整体素材：{self.biography_material_all}\n"
                f"传记核心主题：{self.biography_theme}\n"
        )

        # === 4. 初始化结果结构 ===
        self.plan = {theme_name: {} for theme_name in THEME_MAP.values()}
        # === 5. 定义处理单个主题的函数 ===
        async def process_theme(theme_id):
            theme_name = THEME_MAP.get(theme_id)
            if not theme_name:
                print(f"未识别的主题编号：{theme_id}")
                return None, None

            theme_material = self.expand_result.get(theme_name, [])
            event_sort = self.event.get(theme_name)
            user_prompt = (
                f"辅助素材：{user_prompt_base}\n"
                f"本卷核心素材：{theme_material}\n"
                f"本卷的事件排序：{event_sort}本卷规划要按照这个时间排序进行\n"
                f"卷名主题为：{theme_name}创作的本卷题目要符合这个主题，字数不超过12个汉字\n"
            )

            plan_result = await self.llm_run(user_prompt,system_prompt=biography_Plan_prompt)
            plan_result = json.loads(extract_json(plan_result))
            return theme_name, plan_result
        
        
        tasks = []
        for tid in theme_ids:
            tasks.append(
                process_theme(tid)
            )
        results = await asyncio.gather(*tasks, return_exceptions=False)
        for theme_name, plan_result in results:
            if theme_name and plan_result:
                self.plan[theme_name] = plan_result
        # === 6. 并行处理所有主题 ===
        # with ThreadPoolExecutor(max_workers=5) as executor:
        #     future_to_theme = {executor.submit(process_theme, tid): tid for tid in theme_ids}

        #     for future in as_completed(future_to_theme):
        #         theme_name, plan_result = future.result() if future.result() else (None, None)
        #         if theme_name and plan_result:
        #             self.plan[theme_name] = plan_result

        # === 7. 返回总规划 ===
        return self.plan



    async def biography_plan_TOC(self):
        """
        整理传记目录，根据写作计划整理章节目录。
        输入：
            plan:写作计划
        返回：
            格式化的目录文本，例如：
            出身与童年(卷名)
            ├─ 出生背景（章节名）
            └─ 童年记忆
            学习与成长
            ├─ 求学经历
            └─ 成长心路
        """
        lines = []
        plan = self.plan

        for theme_name, theme_content in plan.items():
            theme_dict = theme_content
            # 添加卷名，优先使用 JSON 里的卷名
            volume_name = theme_dict.get("卷名", theme_name)
            lines.append(volume_name)

            # 获取章节列表
            chapters = theme_dict.get("章节列表", [])
            for i, ch in enumerate(chapters):
                chapter_name = ch.get("章节名", f"未命名章节{i + 1}")
                prefix = "├─" if i < len(chapters) - 1 else "└─"
                lines.append(f"  {prefix} {chapter_name}")

            lines.append("")  # 每卷之间空一行

        text_content = "\n".join(lines)
        self.TOC = text_content
        return text_content

    async def biography_write_agent(self):
        """
        按主题顺序撰写传记，每卷可使用不同系统提示词。

        输入当前要写的整体计划结构
        plan_structure: {
            "出身与童年": {
                "卷名": "童年与成长",
                "章节列表": [
                    {"章节名": "", "撰写内容概要": ""},
                    {"章节名": "", "撰写内容概要": ""}
                ]
            },
            "学习与成长": {...},
            "事业与成就": {...},
            "家庭与情感": {...},
            "生活与体验": {...}
        }

        expand_result: Dict[str, List[Dict]] 可选，每卷的记忆卡片列表

        Returns:
        输出：
        {
            "卷名": [
                "# 章节名\n正文 ",
                "# 章节名\n正文 "
            ],
            ...
        }
        """

        write_result = {}


        # === 审查函数 ===
        async def review_chapter(chapter,chapter_text, review_system_prompt,  roll_cards):
            """
            输入
            1、审查大模型
            2、生成的章节内容
            3、相关记忆卡片

            输出
                {
                    "is_approved": true,
                    "review_comment": "传记在****方面存在幻觉"
                }
            """
            prompt = (
                f"本章内容：{chapter_text}\n"
                f"相关记忆卡片：{roll_cards}\n"
                f"章节名：{chapter['章节名']}\n"
                f"章节概要：{chapter['撰写内容概要']}\n"
            )

            # rewiew_LLM = BaseModel(system_prompt=review_system_prompt)
            # review_result = await rewiew_LLM.run(prompt)
            review_result = await self.llm_run(prompt,system_prompt=review_system_prompt)
            review_result = json.loads(extract_json(review_result))
            return review_result

        # === 内部函数：单章撰写 ===
        async def biography_Plan_Write_Chapter_LLM(chapter, roll_structure, roll_cards, system_prompt, Previous_chapter,
                                             review_system_prompt):
            """
            单章传记撰写
            输入
                1. 本章: {"章节名": "", "撰写内容概要": ""}
                2. 本卷的记忆卡片
                3. 本卷结构
            Returns:
                "# 章节名\n章节正文"
            """
            # Chapter_LLM = BaseModel(system_prompt=system_prompt)
            # 初始化本卷 监督LLM
            retry_count = 0
            max_retries = 3
            self.text_id += 1
            while retry_count < max_retries:
                prompt = (
                    f"主人公姓名：{self.username}\n"
                    f"主人公简历：{self.vitae}\n"
                    f"卷名：{roll_structure['卷名']}\n"
                    f"章节名：{chapter['章节名']}\n"
                    f"章节概要：{chapter['撰写内容概要']}\n"
                    f"相关记忆卡片：{roll_cards}\n"
                    f"本卷整体结构：{roll_structure}\n"
                    f"上一章内容：{Previous_chapter}\n"
                    "请根据以上信息撰写连贯、真实、逻辑自洽的章节正文。"
                )

                print(f"开始撰写章节：{chapter['章节名']}")
                
                # chapter_text = await Chapter_LLM.run(prompt)
                chapter_text = await self.llm_run(prompt,system_prompt=system_prompt)
                # print("传记内容："+chapter_text)
                # === 调用审查模型 ===
                review_out = await review_chapter(chapter, chapter_text, review_system_prompt, roll_cards)
                print(f"审查内容{review_out}")
                # === 校验通过则直接返回 ===
                if review_out.get("is_approved", True):
                    print(f"章节审查通过：{chapter['章节名']}")
                    return f"第{num_to_chinese[self.text_id]}章 {chapter['章节名']}\n\n{chapter_text}"
                # === 若不通过则重写 ===
                retry_count += 1
                print(f"第 {retry_count} 次重写章节：{chapter['章节名']}，原因：{review_out.get('review_comment')}")

                feedback_prompt = (
                    f"核心参考意见：必须根据以下反馈修改：{review_out.get('review_comment')}不可以再重复类似的错误\n"
                    f"章节名：{chapter['章节名']}\n"
                    f"章节概要：{chapter['撰写内容概要']}\n"
                    f"(需要修改的版本)上一版，本章正文：{chapter_text}\n"
                    f"相关记忆卡片：{roll_cards}\n"
                    f"上一章内容：{Previous_chapter}\n"
                    "请改写为逻辑清晰、叙事合理的新版本。"
                )
                chapter_text = await self.llm_run(feedback_prompt,system_prompt=system_prompt)
                # print("修改完传记："+chapter_text)
                # 再次复审
                review_out = await review_chapter(chapter, chapter_text, review_system_prompt, roll_cards)
                if review_out.get("is_approved", True):
                    print(f"重写后章节通过：{chapter['章节名']}")
                    return f"第{num_to_chinese[self.text_id]}章 {chapter['章节名']}\n\n{chapter_text}"

            # 超过重试次数仍不通过
            print(f"审查多次未通过：{chapter['章节名']}")
            # return f"{chapter['章节名']}\n\n（本章生成失败）"
            self.text_id -= 1
            raise Exception(f"章节撰写失败: {review_out}")

        # === 内部函数：卷撰写 ===
        async def biography_Plan_Write_roll_LLM(roll_structure, roll_cards, theme_name):
            """
            卷传记撰写，每卷使用的提示词不一样。 输入
            1、本卷结构{ "卷名": "童年与成长", "章节列表": [ {"章节名": "", "撰写内容概要": ""}, {"章节名": "", "撰写内容概要": ""} ] }
            2、本卷的记忆卡片 循环章节列表逐章节撰写
            Returns:
                章节名/n 内容
            """

            #上一章内容
            Previous_chapter = ""
            review_prompt_file = f"{theme_name}内容监督"
            prompt_file = f"{theme_name}内容撰写"

            async with create_async_session(self.inters.engine) as session:
                result_obj = await self.inters.get_prompt(prompt_id=review_prompt_file,session=session)
                review_system_prompt = result_obj.prompt

            async with create_async_session(self.inters.engine) as session:
                result_obj = await self.inters.get_prompt(prompt_id=prompt_file,session=session)
                system_prompt = result_obj.prompt
            # 初始化本卷 LLM

            # 循环每章节生成正文
            chapters_text = []
            for chapter in roll_structure.get("章节列表", []):

                chapter_text = await biography_Plan_Write_Chapter_LLM(chapter, roll_structure, roll_cards,
                                                                system_prompt,Previous_chapter,review_system_prompt)

                Previous_chapter = chapter_text
                chapters_text.append(chapter_text)

            return chapters_text

        # === 按 THEME_MAP 顺序遍历主题 ===
        for theme_id, theme_name in THEME_MAP.items():
            if theme_name not in self.plan:
                continue
            roll_structure = self.plan[theme_name]

            # 如果卷名为空则跳过
            if not roll_structure.get("卷名"):
                continue

            # 获取本卷记忆卡片
            roll_cards = []
            if self.expand_result and theme_name in self.expand_result:
                roll_cards = self.expand_result[theme_name]

            # 调用卷撰写
            chapters_text_list = await biography_Plan_Write_roll_LLM(roll_structure, roll_cards, theme_name)


            write_result[roll_structure["卷名"]] = chapters_text_list

        self.biography_text_json = write_result

        return self.biography_text_json

    async def json_to_txt(self):
        """
        将结构化传记 JSON 文件解析并写入 TXT 文件。
        JSON 结构示例：
        {
          "预章": ["# 探索之旅的起点\n1980 年，在辽宁葫芦岛..."],
          "第一部 童年与自然启蒙": ["# 第一章 山里野孩子的自由天地\n1980 年，张三出生..."]
        }
        """
        data = self.biography_text_json

        # 2. 打开输出 TXT
        with open("test.txt", 'w', encoding='utf-8') as out:
            for volume, chapters in data.items():
                out.write(f"# {volume}\n\n")
                for chapter in chapters:
                    lines = chapter.strip().split('\n\n', 1)
                    title = lines[0]
                    content = lines[1].strip() if len(lines) > 1 else ''
                    out.write(f"## {title}\n{content}\n\n")

        return f"传记内容已成功写入"

    async def biography_prologue_agent(self,biography_text_json=None):
        """

        传记序章生成

        输入
            全部传记
        输出
            序章

        """
        biography_text_json = biography_text_json or self.biography_text_json

        async with create_async_session(self.inters.engine) as session:
            result_obj = await self.inters.get_prompt(prompt_id="序章撰写",session=session)
            prologue_prompt = result_obj.prompt
        #输入参数
        user_prompt = (
                f"整体传记：{biography_text_json}\n" + f"用户姓名: {self.username}"
        )
        prologue_text = await self.llm_run(user_prompt,system_prompt= prologue_prompt)
        prologue = f"序章\n\n{prologue_text}"
        prologue_list = [prologue]
        self.biography_prologue_json["序章"] = prologue_list

        return self.biography_prologue_json

    async def final_agent(self,biography_text_json=None):
        """

        传记尾章生成

        输入
            全部传记
        输出
            序章

        """
        biography_text_json = biography_text_json or self.biography_text_json


        async with create_async_session(self.inters.engine) as session:
            result_obj = await self.inters.get_prompt(prompt_id="尾章撰写",session=session)
            final_prompt = result_obj.prompt
        #输入参数

        user_prompt = (
                f"整体传记：{biography_text_json}\n"
        )
        final_text = await self.llm_run(user_prompt,system_prompt= final_prompt)
        final = f"尾章\n\n{final_text}"
        final_list = [final]
        self.biography_final_json["尾章"] = final_list

        return self.biography_final_json

    async def name_agent(self,biography_text_json=None):
        """

        传记人名提取

        输入
            全部传记
        输出
            传记中的人名

        """
        biography_text_json = biography_text_json or self.biography_text_json

        # name_prompt_LLM = BaseModel(system_prompt= name_prompt)
        async with create_async_session(self.inters.engine) as session:
            result_obj = await self.inters.get_prompt(prompt_id="人名提取",session=session)
            name_prompt = result_obj.prompt
        #输入参数

        user_prompt = (
                f"整体传记：{biography_text_json}\n"
        )
        name_text = await self.llm_run(user_prompt,system_prompt= name_prompt)
        import ast
        self.biography_name = ast.literal_eval(name_text)

        return self.biography_name

    async def place_agent(self,biography_text_json=None):
        """

        传记地名提取

        输入
            全部传记
        输出
            传记中地名

        """
        biography_text_json = biography_text_json or self.biography_text_json


        async with create_async_session(self.inters.engine) as session:
            result_obj = await self.inters.get_prompt(prompt_id="地名提取",session=session)
            place_prompt = result_obj.prompt
        #输入参数

        user_prompt = (
                f"整体传记：{biography_text_json}\n"
        )
        name_text = await self.llm_run(user_prompt,system_prompt= place_prompt)
        import ast
        self.biography_place = ast.literal_eval(name_text)

        return self.biography_place

    async def brief_agent(self,biography_text_json=None):
        """

        传记概述和传记名字生成

        输入
            全部传记
        输出
            传记概述
            传记名字
            {
              "biography_name": "",
              "biography_brief": ""
            }

        """
        biography_text_json = biography_text_json or self.biography_text_json

        #输入参数
        async with create_async_session(self.inters.engine) as session:
            result_obj = await self.inters.get_prompt(prompt_id="传记概要",session=session)
            system_prompt = result_obj.prompt

        user_prompt = (
                f"整体传记：{biography_text_json}\n"
        )
        brief_text = await self.llm_run(user_prompt,system_prompt= system_prompt)
        # print(brief_text)
        brief_result = json.loads(extract_json(brief_text))

        self.biography_title = brief_result["biography_name"]
        self.biography_brief = brief_result["biography_brief"]
        return self.biography_title, self.biography_brief

    async def output(self,task_id:str):
        """

        Returns:
        整理好的输出结构

        """
        self.biography = {}
        self.biography["task_id"] =task_id
        self.biography["status"] =""
        self.biography["biography_title"] = self.biography_title
        self.biography["biography_brief"] = self.biography_brief

        combined = {
            **self.biography_prologue_json,
            **self.biography_text_json,
            **self.biography_final_json
        }

        self.biography_json = combined

        self.biography["biography_json"] = self.biography_json
        self.biography["biography_name"] = self.biography_name
        self.biography["biography_place"] = self.biography_place
        self.biography["error_message"] = ""
        self.biography["progress"] = 1.0

        # print(self.biography)
        return self.biography


    async def write_article(self,task_id):
        #构建传记Agent
        #整体素材获取
        log1 = await self.material_all_agent()
        logger.info(f'整体素材获取 & {type(log1)} & {log1}')

        #传记主题获取
        log2 = await self.theme_agent()
        logger.info(f'传记主题获取 & {type(log2)} & {log2}')

        #传记素材分块整理
        log3 = await self.expand_cards_agent()
        logger.info(f'传记素材分块整理 & {type(log3)} & {log3}')
        #事件排序
        log35 = await self.event_sort_agent()
        logger.info(f'事件排序 & {type(log35)} & {log35}')

        #章节规划
        log4 = await self.biography_plan_agent()
        logger.info(f'章节规划 & {type(log4)} & {log4}')

        # #传记规划的目录（服务不需要）
        # log5 = biography_agent.biography_plan_TOC()
        # print(log5)

        #撰写文章
        log6 = await self.biography_write_agent()
        logger.info(f'撰写文章 & {type(log6)} & {log6}')

        # #输出文档，服务不需要
        # log7 = biography_agent.json_to_txt()
        # print(log7)
        #写序章
        log8 = await self.biography_prologue_agent()
        logger.info(f'写序章 & {type(log8)} & {log8}')
        #写尾章
        log9 = await self.final_agent()
        logger.info(f'写尾章 &{type(log9)} &  {log9}')
        #提取人名
        log10 = await self.name_agent()
        logger.info(f'提取人名 & {type(log10)} & {log10}')
        #提取地名
        log11 = await self.place_agent()
        logger.info(f'提取地名 & {type(log11)} & {log11}')
        #写概要
        log12 = await self.brief_agent()
        logger.info(f'写概要 & {type(log12)} & {log12}')

        #组合输出结构
        result = await self.output(task_id)
        return result



class BiographyGenerate:
    def __init__(self,model_name = "",api_key = None):
        self.inters = AsyncIntel(model_name = model_name,logger=logger)
        self.model_name = model_name
        # ArkAdapter
        self.biograph_redis = get_redis_client(username = os.getenv("redis_username"), 
                                             password = os.getenv("redis_password"), 
                                             host = os.getenv("redis_host"), 
                                             port = os.getenv("redis_port"),
                                             db = 22)

        self.ark = ArkAdapter(model_name, api_key=api_key or os.getenv("ARK_API_KEY"))


    @log_func(logger)
    async def agenerate_biography_free(
        self, user_name: str, vitae: str, memory_cards: list[dict]
    ):
        
        class Biography_Free(BaseModel):
            title: str = Field(..., description="标题")
            description: str = Field(..., description="传记的简介")
            # content: str = Field(..., description="传记正文")
            
        input_data = {
                    "user_name": user_name,
                    "vitae": vitae,
                    "memory_cards": memory_cards,
                }
        

        input_data_1 = json.dumps(input_data,indent=4,ensure_ascii=False)
        # 文章性文本不建议使用format形式
        # prompt_id="biograph-free-writer"

        async with create_async_session(self.inters.engine) as session:
            result_obj = await self.inters.get_prompt(prompt_id="biograph-free-writer-content",session=session)
            

            system_prompt = result_obj.prompt
            llm_raw_output = await self.ark.aproduct(prompt=input_data_1,
                                    system_prompt=system_prompt)



        result = await self.inters.inference_format(
            input_data = llm_raw_output,
            prompt_id = "biograph-free-writer-title",
            version = None,
            OutputFormat = Biography_Free,
        )

        result.update({"content":llm_raw_output.split('\n',1)[-1]})

        return result
    
    @log_func(logger)
    async def _generate_biography(self,task_id: str, 
                                memory_cards: list,
                                vitae: str,
                                user_name: str):

        task = {
            "task_id": task_id,
            "status": "PENDING",
            "biography_title": None,
            "biography_brief": None,
            "biography_json": None,
            "biography_name": None,
            "biography_place": None,
            "error_message": None,
            "progress": 0.0,
            "request_data": "",  # 存储请求数据以备后续使用
        }
        task["status"] = "PROCESSING"
        task["progress"] = 0.1
        store_with_expiration(self.biograph_redis, task_id, task, 3600) 
        try:
            #     素材整理
            biography_agent = BiographyAgent(memory_cards,user_name,vitae,intels=self.inters,model_name = self.model_name)
            task = await biography_agent.write_article(task_id = task_id)
            biography_callback_url_success = user_callback_url + f'/api/inner/notifyBiographyStatus?generateTaskId={task_id}&status=1'
            store_with_expiration(self.biograph_redis, task_id, task, 3600) 
            await aget_(url = biography_callback_url_success)


        except Exception as e:
            task["status"] = "FAILED"
            task["error_message"] = str(e)
            task["progress"] = 1.0
            biography_callback_url_failed = user_callback_url + f'/api/inner/notifyBiographyStatus?generateTaskId={task_id}&status=0'
            store_with_expiration(self.biograph_redis, task_id, task, 3600) 

            await aget_(url = biography_callback_url_failed)
            raise 

if __name__ == "__main__":
    xx = {
    "user_name":"张强",
    "vitae": "张强，男，1980年出生于北京，清华大学计算机系毕业，曾任职于Google、百度，现为某AI公司首席科学家。",
    "memory_cards": [
        {
        "title": "出生东北",
        "content": "我出生在东北辽宁葫芦岛下面的一个小村庄. 小时候，那里的生活比较简单，人们日出而作，日落而息，生活节奏非常有规律，也非常美好。当时我们都是山里的野孩子，没有什么特别的兴趣爱好，就在山里各种疯跑。我小时候特别喜欢晚上看星星，那时的夜晚星星非常多，真的是那种突然就能看到漫天繁星的感觉。\n ![出生东北_1](http://39.96.146.47:8000/11.jpg) ",
        "time": "1995年--月--日",
        "theme_id":"1"
        },
        {
        "title": "高中的时候",
        "content": "在我高中的时候，我对天文物理和理论物理就非常感兴趣。我当时高中是在我们县城里读的，资源没有那么丰富，我们所有的精力都放在学科的学习上。\n ![高中的时候_1](http://39.96.146.47:8000/11.jpg) ",
        "time": "1995年--月--日",
        "theme_id":"1"
        },
        {
        "title": "虎跳峡的初体验",
        "content": "我第一次徒步，是在虎跳峡。徒步的第二天中午，我们计划坐车回去。上午的时候，我们想去虎跳峡下面的那条江看一看。下去要一个小时，上来要一个多小时，而且都是很陡的台阶，非常累。我们下去拍完照之后，上来的时候，已经快到车发车的时间了。我和我的朋友为了赶上那趟车，就猛爬，使劲地爬。当时我们已经很累了，因为爬楼梯、爬那种台阶很累，但是为了赶上那趟车，我们还是一直在坚持跑。正好赶上那趟车准备发车的时候，我们刚到上面，刚好赶上车。上车之后，我们累得够呛，在车上睡了一觉就到丽江了。这次徒步对我来说，最大的收获就是开启了一个新的项目。",
        "time": "2005年--月--日",
        "theme_id":"2"
        }
    ]
    }

    bg = BiographyGenerate()
    asyncio.run(bg._generate_biography(task_id = "nifg", 
                                memory_cards = [
                                                {
                                                "title": "出生东北",
                                                "content": "我出生在东北辽宁葫芦岛下面的一个小村庄. 小时候，那里的生活比较简单，人们日出而作，日落而息，生活节奏非常有规律，也非常美好。当时我们都是山里的野孩子，没有什么特别的兴趣爱好，就在山里各种疯跑。我小时候特别喜欢晚上看星星，那时的夜晚星星非常多，真的是那种突然就能看到漫天繁星的感觉。\n ![出生东北_1](http://39.96.146.47:8000/11.jpg) ",
                                                "time": "1995年--月--日",
                                                "theme_id":"1"
                                                },
                                                {
                                                "title": "高中的时候",
                                                "content": "在我高中的时候，我对天文物理和理论物理就非常感兴趣。我当时高中是在我们县城里读的，资源没有那么丰富，我们所有的精力都放在学科的学习上。\n ![高中的时候_1](http://39.96.146.47:8000/11.jpg) ",
                                                "time": "1995年--月--日",
                                                "theme_id":"1"
                                                },
                                                {
                                                "title": "虎跳峡的初体验",
                                                "content": "我第一次徒步，是在虎跳峡。徒步的第二天中午，我们计划坐车回去。上午的时候，我们想去虎跳峡下面的那条江看一看。下去要一个小时，上来要一个多小时，而且都是很陡的台阶，非常累。我们下去拍完照之后，上来的时候，已经快到车发车的时间了。我和我的朋友为了赶上那趟车，就猛爬，使劲地爬。当时我们已经很累了，因为爬楼梯、爬那种台阶很累，但是为了赶上那趟车，我们还是一直在坚持跑。正好赶上那趟车准备发车的时候，我们刚到上面，刚好赶上车。上车之后，我们累得够呛，在车上睡了一觉就到丽江了。这次徒步对我来说，最大的收获就是开启了一个新的项目。",
                                                "time": "2005年--月--日",
                                                "theme_id":"2"
                                                }
                                            ],
                                vitae = "张强，男，1980年出生于北京，清华大学计算机系毕业，曾任职于Google、百度，现为某AI公司首席科学家。",
                                user_name = "张强",
                                ))