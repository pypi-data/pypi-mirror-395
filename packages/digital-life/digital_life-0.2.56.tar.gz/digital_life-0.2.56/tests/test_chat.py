from digital_life.core import ChatBox


async def test():

    chatbox = ChatBox()
    await chatbox.init_chatbox()


    async for word in chatbox.astream_product(prompt_with_history = "你好",
                                                            model="iv_interview",
                                                            user_id = "1",
                                                            topic = "聊聊日常"
                                                            ):
        print(word)                                        