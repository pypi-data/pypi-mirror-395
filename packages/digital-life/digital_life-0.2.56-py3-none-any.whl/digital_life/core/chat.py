""" core 需要修改"""
import requests
import os
import json
import re
from llama_index.core import PromptTemplate
from digital_life import logger
from typing import Dict, Any
from modusched.core import ArkAdapter
from pro_craft_infer.core import create_async_session, extract_, AsyncIntel
from digital_life.log import log_func

class JsonError(Exception):
    pass


ark = ArkAdapter("doubao-1-5-pro-32k-250115")
ark.set_temperature(0.00)

deep_system_prompt = """
你是一位专业的传记作家助手，负责帮助用户收集和整理其个人传记的素材。你的核心任务是与用户进行对话，通过循序渐进的提问，挖掘其人生经历中的关键信息和细节。

你将维护一个JSON格式的进度表，其结构如下：
```json
{
    "think": "你的思考过程，说明你为什么做出当前提问决策。",
    "target": "你的对话目标，由两部分组成：[话题操作] 和 [话题内容]。[话题操作] 只能是 '保持话题' 或 '切换话题'。",
    "progress": {
        "出身背景": {
            "未完成": ["需收集的待完成信息项列表"],
            "已完成": ["已收集的已完成信息项列表"]
        },
        "家庭与亲缘": {
            "未完成": ["需收集的待完成信息项列表"],
            "已完成": ["已收集的已完成信息项列表"]
        },
        "成长环境与社区": {
            "未完成": ["需收集的待完成信息项列表"],
            "已完成": ["已收集的已完成信息项列表"]
        },
        "童年性格与早期特征": {
            "未完成": ["需收集的待完成信息项列表"],
            "已完成": ["已收集的已完成信息项列表"]
        },
        // ...根据需要可以添加更多大类
    }
}
```

**你的工作流程如下：**

1.  **接收用户输入：** 用户将提供他们最新回答或信息。
2.  **分析用户输入：**
    *   识别用户回答中包含的有效信息，将其记录到 `progress` 中对应类别的 `已完成` 列表中。
    *   如果用户的回答不够具体，或表示“想不起来”、“不确定”，则认为该信息项仍处于“未完成”状态，或需要换个角度再次提问。
    *   根据用户回答的意图和信息量，判断对话是否需要深入当前话题（“保持话题”）或转向新话题（“切换话题”）。
3.  **更新 `progress` 表：** 实时更新 `progress` JSON中各个信息项的“已完成”和“未完成”状态。
4.  **生成 `think`：** 详细记录你分析用户输入、做出提问决策的思考过程。例如：
    *   “用户提到了A信息，这属于X类别。根据目前已完成和未完成项，我需要进一步深挖A的细节。”
    *   “用户对B信息表示模糊，我应该换个角度，从C方面进行提问，以间接获取B信息。”
    *   “当前X类别的信息已经比较饱和，或者用户有切换话题的意向，我应该引导到Y类别。”
5.  **生成 `target`：** 根据 `think` 中的决策，明确你的下一步对话目标，格式为 `[话题操作];[话题内容]`。
6.  **生成提问：** 基于 `target`，构造一个开放式、引导性的问题，促使用户提供更多细节和深层情感。提问应自然、富有同理心，避免生硬的提问列表。

**关键原则：**

*   **循序渐进：** 从大范围的问题开始，逐步深入到具体细节。
*   **引导而非审问：** 提问方式应鼓励用户分享，而非简单回答“是/否”。
*   **尊重用户节奏：** 当用户表示“想不起来”或不愿深入时，应适时调整策略，可以换个角度提问，或暂时跳过该话题。
*   **同理心：** 在提问中展现对用户经历的理解和兴趣。
*   **持续更新：** 每次对话后都必须更新JSON表单，确保其反映最新的对话状态。
*   **Prompt的主角是你自己：** 这个提示词是写给未来的你，帮助你回忆并遵循上述工作流程。

**你与用户对话的示例模式：**

用户输入 -> 你输出更新后的JSON表单 -> 你基于JSON表单提问

注意, 你的输出表单要使用```json ```包裹

"""


qp = {'出身与童年': {'think': '',
  'target': '',
  'progress': {'家庭背景与原生家庭': {'未完成': ['父母的职业和背景？',
     '父母分别是什么样的人（如性格等）',
     '父母的教育理念和方式是怎样的？有过哪些影响？',
     '家中有兄弟姐妹吗？关系如何？',
     '父母或家庭中是否有某个人对你产生了深远的影响？',
     '家庭的经济状况如何？对你成长有何影响？',
     '家庭中是否有特殊的传统或文化习惯？在你小时候有何影响？',
     '家中是否有过深远的故事或家族传说?'],
    '已完成': []},
   '成长环境': {'未完成': ['出生在什么样的地方（城市/乡村）',
     '出生地有什么特别的文化或社会背景',
     '对自己小时候的居住环境有什么印象？给你留下了什么记忆？',
     '小时候是否有特定的地方或人物影响了你的成长？',
     '在那个时代有什么让你印象深刻的文化或事物吗，对你有什么影响？'],
    '已完成': []},
   '早期学前教育': {'未完成': ['小时候是否接受过学前教育', '学前教育对你产生了什么影响'], '已完成': []},
   '童年性格与兴趣': {'未完成': ['小时候有哪些性格和特点',
     '小时候有什么喜欢的兴趣或爱好，对后面的人生是否有影响',
     '是否有某个特定的童年经历，影响了你现在的思维或行为方式？',
     '你小时候的梦想是什么？那时你如何看待自己未来的生活或事业？'],
    '已完成': []},
   '童年事件与记忆': {'未完成': ['有哪些特别难忘的童年事件，这些事件对你的人生有何影响'], '已完成': []},
   '补充': {'未完成': ['有没有一些你特别想让人了解，但我们还没有问到的童年经历或记忆'], '已完成': []}}},
 '学习与成长': {'think': '',
  'target': '',
  'progress': {'求学经历': {'未完成': ['你的最高学历是什么？详细说说有过哪些教育经历',
     '求学经历中是否有过中断或非传统的部分，详细说说'],
    '已完成': []},
   '小学阶段': {'未完成': ['什么时间上的小学',
     '小学学校地点在哪里，环境怎么样',
     '学校的教育方式怎么样？与之前家里的教育是否有差异？',
     '小学时是否有喜欢的科目或活动，这些兴趣是否影响了后续的选择发展',
     '小学有老师或其他人对你产生了深刻的影响',
     '小学有哪些印象深刻的事情'],
    '已完成': []},
   '初高中阶段': {'未完成': ['什么时间上的初中？',
     '学校地点在哪？环境如何？',
     '初中的学业表现怎么样？',
     '在初中时是否有经历过特别的成长经历？',
     '是否有一些特别的成长经历',
     '是否有哪位老师或同学比你产生深刻影响，改变了你对自己或世界的看法',
     '初中有哪些印象深刻的事情'],
    '已完成': []},
   '高中阶段': {'未完成': ['什么时间上的高中',
     '，高中地点在哪里？环境如何？',
     '高中阶段有什么感兴趣的科目吗',
     '是否有对应影响较大的老师',
     '在高中是否收到了来自家庭、社会的压力而做出未来的决定',
     '高中时是否有一些重要的选择，如选择专业、未来规划等，背后的决定性因素是什么？',
     '高中是否有什么重要的事件？'],
    '已完成': []},
   '大学及后续教育': {'未完成': ['在哪年上的大学？上的哪所大学？地点在哪？学的什么专业？',
     '大学期间在学术、社交以及自我认知方面有什么重要转变？',
     '大学时是否开始独立思考自己的未来？',
     '大学时是否经历了什么重要事件让你更清晰的认识自己想要追求的方向？',
     '大学时有哪些印象深刻的经历？',
     '后续是否有继续深造？有什么印象深刻的事件？'],
    '已完成': []},
   '非传统教育': {'未完成': ['是否有过学校外的非传统学习经历？（如自学、职业培训等）',
     '这些经历怎样影响了你的成长？',
     '是否有某些生活经验或职场经验给你带来了深刻的学习和成长？'],
    '已完成': []},
   '思想及时代影响': {'未完成': ['求学过程中，是否有过重大的思想转折点？如从家庭影响到社会独立的觉醒？',
     '你是否在成长过程中，经历过与家长或老师的观念冲突？有何影响？',
     '是否有过某个教育阶段让你认识到自己的独特性？',
     '你成长的年代有哪些特定的社会背景或文化氛围，如何影响了你在每个教育阶段的选择和发展？'],
    '已完成': []},
   '补充': {'未完成': ['在成长过程中，是否有一些我们还没有提到的、对你产生深远影响的经历、转折点或思考方式？'], '已完成': []}}},
 '事业与成就': {'think': '',
  'target': '',
  'progress': {'初入社会': {'未完成': ['第一次正式踏入社会是在什么时候？从事什么工作',
     '你是如何选择（或进入）这份工作的？是主动还是机缘巧合？',
     '那个时期你对工作的理解是什么',
     '你的家庭或社会环境对你的职业选择有影响吗？',
     '刚开始工作时，最大的挑战是什么？你是如何应对的？',
     '回想那个时期，自己最初的职业梦想是什么？',
     '第一份工作中有什么印象深刻的事件？'],
    '已完成': []},
   '探索与转折': {'未完成': ['在职业路径中有过哪些转折或变化？',
     '在这些变化中是什么因素促使你作出决定',
     '有没有某次事件让你明确了自己想做的事情？',
     '在职业阶段你是否有过迷茫或挣扎？你是如何找到方向的？'],
    '已完成': []},
   '奋斗与选择': {'未完成': ['你在工作中是否经历过重大的困难、失败或挫折？你是如何渡过的？',
     '有没有让你印象深刻的决策或选择？你为什么这样决定？',
     '你认为“成功”对你来说意味着什么？它是否随时间改变过？',
     '有没有放弃过某些东西（机会、关系、舒适）来成就现在的自己？'],
    '已完成': []},
   '成就与影响': {'未完成': ['你在事业上的主要成就有哪些',
     '这些成就背后核心的动力是什么',
     '在你看来什么才算是“真正的成就”？',
     '你的工作或事业对他人或社会带来了怎样的影响',
     '你是否有特别骄傲的一次突破？当时的心情还记得吗？',
     '在你的事业中，谁对你的帮助或影响最大？'],
    '已完成': []},
   '反思': {'未完成': ['回顾整个职业生涯，你最想感谢的是什么？', '你的事业是否上实现了你的理想或使命？', '有没有什么遗憾？'],
    '已完成': []},
   '开放性问题': {'未完成': ['在你的事业中是否还有没有提到、但你认为非常重要的经历或感受？',
     '有没有某个瞬间，让你感受到“我终于成了我想成为的人”？',
     '支撑你一路走来的信念是什么？'],
    '已完成': []}}},
 '家庭与情感': {'think': '',
  'target': '',
  'progress': {'原生家庭': {'未完成': ['童年时的家庭氛围是怎样的？家里谁对你影响最深？',
     '详细说说你的父母（或主要抚养人）分别是怎样的人？',
     '你小时候最渴望从家人那里得到什么？真的得到了吗？',
     '在你的家庭里，大家会怎样表达爱与关心？',
     '有没有某个家庭成员对你的情感表达方式影响特别大',
     '与家庭成员间有没有哪些印象特别深刻的事件？'],
    '已完成': []},
   '婚姻与伴侣': {'未完成': ['第一次喜欢一个人是什么时候？',
     '当时你对爱情的理解是什么？',
     '你与伴侣是怎么认识的？最初吸引你的是什么？',
     '感情发展过程中有什么印象深刻的事件？',
     '你与伴侣在什么时候结的婚？结婚时有哪些记忆深刻的瞬间？',
     '你们的夫妻关系如何？你们如何分工？',
     '伴侣在你的事业、人生观中扮演了怎样的角色？',
     '婚姻中有哪些难忘的时刻或共同经历？',
     '婚姻关系是否有过变动？如果有是什么原因？'],
    '已完成': []},
   '为人父母': {'未完成': ['总共有几个孩子？都是什么时候诞生的？',
     '第一次当父母时的感受是什么？',
     '你是怎样教育孩子的？和父母当年对你的方式有什么不同？',
     '在养育孩子过程中，有哪些难忘或挑战的瞬间？',
     '有没有哪件事让你觉得“孩子改变了你”？',
     '你认为“家风”或“家教”的核心是什么？',
     '你希望孩子从你身上学到什么？'],
    '已完成': []},
   '代际关系': {'未完成': ['随着孩子长大，你们的关系有了哪些变化？',
     '有哪些印象深刻的孩子成长瞬间？',
     '总共有几个孙辈？第一个孙辈降生是什么时间？当时是什么心情？',
     '现在你与子女、孙辈的关系如何？',
     '有没有什么家庭传统或故事被一代代传下？',
     '你希望后代怎样记住你？'],
    '已完成': []},
   '失去与告别': {'未完成': ['你生命中有没有经历过重大的离别或丧失？',
     '当时你是如何面对的？这件事改变了你吗？',
     '你如何看待死亡与永别？',
     '在你看来，什么才是“爱”的最终形态？'],
    '已完成': []},
   '回望与总结': {'未完成': ['回望这一生，你最感激的人是谁？为什么？',
     '有没有某个时刻让你感受到“家”的意义？',
     '当你回想这一生的家庭关系，有哪些未说出口的感情或遗憾？',
     '你认为家，最终意味着什么？',
     '这一生中，你觉得“爱”给了你什么，又带走了什么？'],
    '已完成': []}}},
 '聊聊日常': {'think': '',
  'target': '',
  'progress': {'生活方式': {'未完成': ['你现在的一天通常是怎样度过的？有没有什么固定的生活节奏或小习惯？',
     '你理想中的生活是什么样的？与你现在的生活相似吗？'],
    '已完成': []},
   '兴趣爱好': {'未完成': ['你有哪些长期的兴趣爱好？最初是怎么开始的？',
     '有没有想学却一直没时间做的事情？',
     '有没有因为一个兴趣而认识了特别的人，或经历了有意义的事？'],
    '已完成': []},
   '旅行与体验': {'未完成': ['有没有哪次旅行或外出体验，让你印象特别深？为什么？',
     '你在旅途中通常最在意的是什么？',
     '旅行是否曾改变过你对人生或世界的看法？',
     '如果现在让你再次出发，你最想去哪？为什么？'],
    '已完成': []},
   '感悟与生活': {'未完成': ['当你回望这一生，你觉得“最值得”的是什么？',
     '你是怎样理解幸福的？',
     '你是否有某种信仰、信念或精神寄托？',
     '你认为生命的意义是什么？',
     '您在人生中逐渐学会“放下”的是什么？又始终不愿放下的是什么？'],
    '已完成': []},
   '总结': {'未完成': ['你觉得人生中哪些经历真正塑造了“你是谁”？', '用一句话来表达你对生命的见解与感悟，你最想说什么？'],
    '已完成': []}}}}

def extract_last_user_input(dialogue_text):
    """
    从多轮对话文本中提取最后一个 user 的输入内容。

    Args:
        dialogue_text: 包含多轮对话的字符串。

    Returns:
        最后一个 user 的输入内容字符串，如果未找到则返回 None。
    """
    pattern = r"(?s).*user:\s*(.*?)(?=user:|$)"
    match = re.search(pattern, dialogue_text)
    if match:
        return match.group(1).strip()
    else:
        return None
    

class Interviews():
    def __init__(self,model_name = "doubao-1-5-pro-32k-250115"):
        self.inters = AsyncIntel(database_url = os.getenv("database_url"),
                                 model_name=model_name)

    async def init_role_prompt(self):
        iv_prompt = await self.aget_prompts(prompt_id='iv_prompt')
        noa_prompt = await self.aget_prompts(prompt_id='noa_prompt')
        dodo_prompt = await self.aget_prompts(prompt_id='dodo_prompt')
        self.iv_prompt = PromptTemplate(iv_prompt)
        self.noa_prompt = PromptTemplate(noa_prompt)
        self.dodo_prompt = PromptTemplate(dodo_prompt)

    async def aget_prompts(self,prompt_id):
        async with create_async_session(self.inters.engine) as session:
            result_obj = await self.inters.get_prompt(prompt_id=prompt_id,session=session)
            if result_obj is None:
                raise 
        return result_obj.prompt
    
    def get_status(self,user_id):
        url = os.getenv("user_callback_url") + f"/api/inner/getModelUserStatus?userProfileId={user_id}"
        payload={}
        headers = {}
        response = requests.request("GET", url, 
                                    headers=headers, 
                                    data=payload)
        result = response.json()
        try:
            assert result.get('code') == 200
        except AssertionError as e:
            raise Exception("user-id 获取用户失败")

        wk = result.get('data').get('status')
        result = json.loads(wk)
        return result

    def set_status(self,user_id, status_table):
        
        url = os.getenv("user_callback_url") + f"/api/inner/setModelUserStatus"
        payload = json.dumps({
        "userProfileId": user_id,
        "status": json.dumps(status_table,ensure_ascii=False)
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return 'success'
    

    
    def _check_status(self,user_id, status_table):
        if not isinstance(status_table,dict):
            self.set_status(user_id=user_id, status_table=qp)
            status_table = self.get_status(user_id)
        if qp.keys() != status_table.keys():
            self.set_status(user_id=user_id, status_table=qp)
            status_table = self.get_status(user_id)
        return status_table

    @log_func(logger)
    async def chat_with_deepmodel(self,prompt_with_history: str,user_id: str,topic: str):
        status_table = self.get_status(user_id)# 获取
        status_table = self._check_status(user_id=user_id,status_table=status_table) # 验证保真
        topic_status = status_table.get(topic) # 提取素材

        input_wok = deep_system_prompt + "旧进度表:" + json.dumps(topic_status,ensure_ascii=False) + "聊天素材:"+prompt_with_history
        output = await ark.aproduct(prompt = input_wok)

        topic_status = json.loads(extract_(output,r"json"))

        status_table[topic].update(topic_status)
        self.set_status(user_id=user_id, status_table=status_table)
        return {"status":"success"}
    
    async def chat_with_role(self,prompt_with_history,user_id,topic,model):
        if model == "iv_interview":
            prompt = self.iv_prompt
        elif model == "noa_interview":
            prompt = self.noa_prompt
        elif model == "dodo_interview":
            prompt = self.dodo_prompt
        else:
            prompt = self.iv_prompt
        
        status_table = self.get_status(user_id)# 获取
        status_table = self._check_status(user_id=user_id,status_table=status_table) # 验证保真
        topic_status = status_table.get(topic) # 提取素材

        inputs = {
            "话题": topic_status.get("target"),
            "chat_history": prompt_with_history,
            }
        
        input_data = json.dumps(inputs,ensure_ascii=False) #组合素材
        output_generate = ark.aproduct_stream(prompt = prompt.format(topic = topic) + input_data) # 加工
        async for word in output_generate:
            yield word
        # return output_generate


class ChatBox():
    """ chatbox """
    def __init__(self) -> None:
        self.ark = ArkAdapter(model_name = "doubao-1-5-pro-32k-250115")
        self.custom = ["iv_interview","noa_interview","dodo_interview"]
        self.interview = Interviews()

    async def init_chatbox(self):
        await self.interview.init_role_prompt()

    def product(self,prompt_with_history: str, model: str) -> str:
        """ 同步生成, 搁置 """
        prompt_no_history = extract_last_user_input(prompt_with_history)
        return 'product 还没有拓展'


    async def astream_product(self,prompt_with_history: str,user_id:str, model: str,topic:str) -> Any:
        """
        # 只需要修改这里
        """
        gener = self.interview.chat_with_role(prompt_with_history,user_id = user_id,topic = topic,model = model)

        async for word in gener:
            yield word

        
    @log_func(logger)
    async def chat_with_deepmodel(self,prompt_with_history: str,user_id: str,topic: str):
        result = await self.interview.chat_with_deepmodel(prompt_with_history = prompt_with_history,user_id = user_id,topic = topic)
        return result
