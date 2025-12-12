from modusched.core import Adapter
import pytest
import types

@pytest.fixture
def openai():
    openai = Adapter()
    return openai

def test_openai_predict(openai):
    result = openai.predict(prompt = "你好")
    assert isinstance(result,str)
    assert len(result) > 1

async def test_openai_apredict(openai):
    result = await openai.apredict(prompt = "你好")
    assert isinstance(result,str)
    assert len(result) > 1

def test_openai_stream(openai):
    result = openai.stream(prompt = "你好")
    assert isinstance(result, types.GeneratorType)
    for i in result:
        assert isinstance(i,str)

async def test_openai_astream(openai):
    result = openai.astream(prompt = "你好")
    assert isinstance(result, types.AsyncGeneratorType)
    async for i in result:
        assert isinstance(i,str)




def test_openai_predict_system(openai):
    try:
        result = openai.predict(system_prompt = "你好")
        raise TypeError()
    except AssertionError as e:
        pass


async def test_openai_apredict_system(openai):
    try:
        result = await openai.apredict(system_prompt = "你好")
        assert isinstance(result,str)
        assert len(result) > 1
        raise TypeError()
    except AssertionError as e:
        pass

def test_openai_stream_system(openai):
    try:
        result = openai.stream(system_prompt = "你好")
        assert isinstance(result, types.GeneratorType)
        for i in result:
            assert isinstance(i,str)
        raise TypeError()
    except AssertionError as e:
        pass
async def test_openai_astream_system(openai):
    try:
        result = openai.astream(system_prompt = "你好")
        assert isinstance(result, types.AsyncGeneratorType)
        async for i in result:
            assert isinstance(i,str)
        raise TypeError()
    except AssertionError as e:
        pass




def test_openai_predict_system_prompt(openai):
    result = openai.predict(system_prompt = "你是一个和蔼的人",prompt = "你好")
    assert isinstance(result,str)
    assert len(result) > 1

async def test_openai_apredict_system_prompt(openai):
    result = await openai.apredict(system_prompt = "你是一个和蔼的人",prompt = "你好")
    assert isinstance(result,str)
    assert len(result) > 1

def test_openai_stream_system_prompt(openai):
    result = openai.stream(system_prompt = "你是一个和蔼的人",prompt = "你好")
    assert isinstance(result, types.GeneratorType)
    for i in result:
        assert isinstance(i,str)

async def test_openai_astream_system_prompt(openai):
    result = openai.astream(system_prompt = "你是一个和蔼的人",prompt = "你好")
    assert isinstance(result, types.AsyncGeneratorType)
    async for i in result:
        assert isinstance(i,str)





def test_openai_predict_messages(openai):
    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},]}],
        [{"role": "system","content": [{"type": "text", "text": "你是一个和蔼的人"},]},
         {"role": "user","content": [{"type": "text", "text": "你好"},]},
         {"role": "assistant","content": [{"type": "text", "text": "你好 我是qq"},]},
         {"role": "user","content": [{"type": "text", "text": "你从哪里来"},]},
         ],
        [{"role": "user","content": "你好"}],
        [{"role": "system","content": "你是一个和蔼的人"},
         {"role": "user","content": "你好"},
         {"role": "assistant","content": "你好 我是qq"},
         {"role": "user","content": "你从哪里来"},
         ],
    ]
    for messages in messages_list:
        result = openai.predict(messages=messages)
        assert isinstance(result,str)
        assert len(result) > 1

async def test_openai_apredict_messages(openai):
    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},]}],
        [{"role": "system","content": [{"type": "text", "text": "你是一个和蔼的人"},]},
         {"role": "user","content": [{"type": "text", "text": "你好"},]},
         {"role": "assistant","content": [{"type": "text", "text": "你好 我是qq"},]},
         {"role": "user","content": [{"type": "text", "text": "你从哪里来"},]},
         ],
        [{"role": "user","content": "你好"}],
        [{"role": "system","content": "你是一个和蔼的人"},
         {"role": "user","content": "你好"},
         {"role": "assistant","content": "你好 我是qq"},
         {"role": "user","content": "你从哪里来"},
         ],
    ]
    for messages in messages_list:
        result = await openai.apredict(messages=messages)
        assert isinstance(result,str)
        assert len(result) > 1

def test_openai_stream_messages(openai):
    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},]}],
        [{"role": "system","content": [{"type": "text", "text": "你是一个和蔼的人"},]},
         {"role": "user","content": [{"type": "text", "text": "你好"},]},
         {"role": "assistant","content": [{"type": "text", "text": "你好 我是qq"},]},
         {"role": "user","content": [{"type": "text", "text": "你从哪里来"},]},
         ],
        [{"role": "user","content": "你好"}],
        [{"role": "system","content": "你是一个和蔼的人"},
         {"role": "user","content": "你好"},
         {"role": "assistant","content": "你好 我是qq"},
         {"role": "user","content": "你从哪里来"},
         ],
    ]
    for messages in messages_list:
        result = openai.stream(messages=messages)
        assert isinstance(result, types.GeneratorType)
        for i in result:
            assert isinstance(i,str)




async def test_openai_astream_messages(openai):
    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},]}],
        [{"role": "system","content": [{"type": "text", "text": "你是一个和蔼的人"},]},
         {"role": "user","content": [{"type": "text", "text": "你好"},]},
         {"role": "assistant","content": [{"type": "text", "text": "你好 我是qq"},]},
         {"role": "user","content": [{"type": "text", "text": "你从哪里来"},]},
         ],
        [{"role": "user","content": "你好"}],
        [{"role": "system","content": "你是一个和蔼的人"},
         {"role": "user","content": "你好"},
         {"role": "assistant","content": "你好 我是qq"},
         {"role": "user","content": "你从哪里来"},
         ],
    ]
    for messages in messages_list:
        result = openai.astream(messages=messages)
        assert isinstance(result, types.AsyncGeneratorType)
        async for i in result:
            assert isinstance(i,str)



@pytest.fixture
def ark():
    return Adapter(model_name="doubao-1-5-pro-256k-250115",type = "ark")


def test_ark_predict(ark):
    result = ark.predict(prompt = "你好")
    assert isinstance(result,str)
    assert len(result) > 1

async def test_ark_apredict(ark):
    result = await ark.apredict(prompt = "你好")
    assert isinstance(result,str)
    assert len(result) > 1

def test_ark_stream(ark):
    result = ark.stream(prompt = "你好")
    assert isinstance(result, types.GeneratorType)
    for i in result:
        assert isinstance(i,str)

async def test_ark_astream(ark):
    result = ark.astream(prompt = "你好")
    assert isinstance(result, types.AsyncGeneratorType)
    async for i in result:
        assert isinstance(i,str)




def test_ark_predict_system(ark):
    try:
        result = ark.predict(system_prompt = "你好")
        raise TypeError()
    except AssertionError as e:
        pass


async def test_ark_apredict_system(ark):
    try:
        result = await ark.apredict(system_prompt = "你好")
        assert isinstance(result,str)
        assert len(result) > 1
        raise TypeError()
    except AssertionError as e:
        pass

def test_ark_stream_system(ark):
    try:
        result = ark.stream(system_prompt = "你好")
        assert isinstance(result, types.GeneratorType)
        for i in result:
            assert isinstance(i,str)
        raise TypeError()
    except AssertionError as e:
        pass
async def test_ark_astream_system(ark):
    try:
        result = ark.astream(system_prompt = "你好")
        assert isinstance(result, types.AsyncGeneratorType)
        async for i in result:
            assert isinstance(i,str)
        raise TypeError()
    except AssertionError as e:
        pass




def test_ark_predict_system_prompt(ark):
    result = ark.predict(system_prompt = "你是一个和蔼的人",prompt = "你好")
    assert isinstance(result,str)
    assert len(result) > 1

async def test_ark_apredict_system_prompt(ark):
    result = await ark.apredict(system_prompt = "你是一个和蔼的人",prompt = "你好")
    assert isinstance(result,str)
    assert len(result) > 1

def test_ark_stream_system_prompt(ark):
    result = ark.stream(system_prompt = "你是一个和蔼的人",prompt = "你好")
    assert isinstance(result, types.GeneratorType)
    for i in result:
        assert isinstance(i,str)

async def test_ark_astream_system_prompt(ark):
    result = ark.astream(system_prompt = "你是一个和蔼的人",prompt = "你好")
    assert isinstance(result, types.AsyncGeneratorType)
    async for i in result:
        assert isinstance(i,str)





def test_ark_predict_messages(ark):
    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},]}],
        [{"role": "system","content": [{"type": "text", "text": "你是一个和蔼的人"},]},
         {"role": "user","content": [{"type": "text", "text": "你好"},]},
         {"role": "assistant","content": [{"type": "text", "text": "你好 我是qq"},]},
         {"role": "user","content": [{"type": "text", "text": "你从哪里来"},]},
         ],
        [{"role": "user","content": "你好"}],
        [{"role": "system","content": "你是一个和蔼的人"},
         {"role": "user","content": "你好"},
         {"role": "assistant","content": "你好 我是qq"},
         {"role": "user","content": "你从哪里来"},
         ],
    ]
    for messages in messages_list:
        result = ark.predict(messages=messages)
        assert isinstance(result,str)
        assert len(result) > 1

async def test_ark_apredict_messages(ark):
    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},]}],
        [{"role": "system","content": [{"type": "text", "text": "你是一个和蔼的人"},]},
         {"role": "user","content": [{"type": "text", "text": "你好"},]},
         {"role": "assistant","content": [{"type": "text", "text": "你好 我是qq"},]},
         {"role": "user","content": [{"type": "text", "text": "你从哪里来"},]},
         ],
        [{"role": "user","content": "你好"}],
        [{"role": "system","content": "你是一个和蔼的人"},
         {"role": "user","content": "你好"},
         {"role": "assistant","content": "你好 我是qq"},
         {"role": "user","content": "你从哪里来"},
         ],
    ]
    for messages in messages_list:
        result = await ark.apredict(messages=messages)
        assert isinstance(result,str)
        assert len(result) > 1

def test_ark_stream_messages(ark):
    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},]}],
        [{"role": "system","content": [{"type": "text", "text": "你是一个和蔼的人"},]},
         {"role": "user","content": [{"type": "text", "text": "你好"},]},
         {"role": "assistant","content": [{"type": "text", "text": "你好 我是qq"},]},
         {"role": "user","content": [{"type": "text", "text": "你从哪里来"},]},
         ],
        [{"role": "user","content": "你好"}],
        [{"role": "system","content": "你是一个和蔼的人"},
         {"role": "user","content": "你好"},
         {"role": "assistant","content": "你好 我是qq"},
         {"role": "user","content": "你从哪里来"},
         ],
    ]
    for messages in messages_list:
        result = ark.stream(messages=messages)
        assert isinstance(result, types.GeneratorType)
        for i in result:
            assert isinstance(i,str)




async def test_ark_astream_messages(ark):
    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},]}],
        [{"role": "system","content": [{"type": "text", "text": "你是一个和蔼的人"},]},
         {"role": "user","content": [{"type": "text", "text": "你好"},]},
         {"role": "assistant","content": [{"type": "text", "text": "你好 我是qq"},]},
         {"role": "user","content": [{"type": "text", "text": "你从哪里来"},]},
         ],
        [{"role": "user","content": "你好"}],
        [{"role": "system","content": "你是一个和蔼的人"},
         {"role": "user","content": "你好"},
         {"role": "assistant","content": "你好 我是qq"},
         {"role": "user","content": "你从哪里来"},
         ],
    ]
    for messages in messages_list:
        result = ark.astream(messages=messages)
        assert isinstance(result, types.AsyncGeneratorType)
        async for i in result:
            assert isinstance(i,str)



@pytest.fixture
def agent():
    return Adapter(type = "agent")


def test_agent_predict(agent):
    result = agent.predict(prompt = "你好")
    assert isinstance(result,str)
    assert len(result) > 1

async def test_agent_apredict(agent):
    result = await agent.apredict(prompt = "你好")
    assert isinstance(result,str)
    assert len(result) > 1

def test_agent_stream(agent):
    result = agent.stream(prompt = "你好")
    assert isinstance(result, types.GeneratorType)
    for i in result:
        assert isinstance(i,str)

async def test_agent_astream(agent):
    result = agent.astream(prompt = "你好")
    assert isinstance(result, types.AsyncGeneratorType)
    async for i in result:
        assert isinstance(i,str)




def test_agent_predict_system(agent):
    try:
        result = agent.predict(system_prompt = "你好")
        raise TypeError()
    except AssertionError as e:
        pass


async def test_agent_apredict_system(agent):
    try:
        result = await agent.apredict(system_prompt = "你好")
        assert isinstance(result,str)
        assert len(result) > 1
        raise TypeError()
    except AssertionError as e:
        pass

def test_agent_stream_system(agent):
    try:
        result = agent.stream(system_prompt = "你好")
        assert isinstance(result, types.GeneratorType)
        for i in result:
            assert isinstance(i,str)
        raise TypeError()
    except AssertionError as e:
        pass
async def test_agent_astream_system(agent):
    try:
        result = agent.astream(system_prompt = "你好")
        assert isinstance(result, types.AsyncGeneratorType)
        async for i in result:
            assert isinstance(i,str)
        raise TypeError()
    except AssertionError as e:
        pass




def test_agent_predict_system_prompt(agent):
    result = agent.predict(system_prompt = "你是一个和蔼的人",prompt = "你好")
    assert isinstance(result,str)
    assert len(result) > 1

async def test_agent_apredict_system_prompt(agent):
    result = await agent.apredict(system_prompt = "你是一个和蔼的人",prompt = "你好")
    assert isinstance(result,str)
    assert len(result) > 1

def test_agent_stream_system_prompt(agent):
    result = agent.stream(system_prompt = "你是一个和蔼的人",prompt = "你好")
    assert isinstance(result, types.GeneratorType)
    for i in result:
        assert isinstance(i,str)

async def test_agent_astream_system_prompt(agent):
    result = agent.astream(system_prompt = "你是一个和蔼的人",prompt = "你好")
    assert isinstance(result, types.AsyncGeneratorType)
    async for i in result:
        assert isinstance(i,str)





def test_agent_predict_messages(agent):
    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},]}],
        [{"role": "system","content": [{"type": "text", "text": "你是一个和蔼的人"},]},
         {"role": "user","content": [{"type": "text", "text": "你好"},]},
         {"role": "assistant","content": [{"type": "text", "text": "你好 我是qq"},]},
         {"role": "user","content": [{"type": "text", "text": "你从哪里来"},]},
         ],
        [{"role": "user","content": "你好"}],
        [{"role": "system","content": "你是一个和蔼的人"},
         {"role": "user","content": "你好"},
         {"role": "assistant","content": "你好 我是qq"},
         {"role": "user","content": "你从哪里来"},
         ],
    ]
    for messages in messages_list:
        result = agent.predict(messages=messages)
        assert isinstance(result,str)
        assert len(result) > 1

async def test_agent_apredict_messages(agent):
    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},]}],
        [{"role": "system","content": [{"type": "text", "text": "你是一个和蔼的人"},]},
         {"role": "user","content": [{"type": "text", "text": "你好"},]},
         {"role": "assistant","content": [{"type": "text", "text": "你好 我是qq"},]},
         {"role": "user","content": [{"type": "text", "text": "你从哪里来"},]},
         ],
        [{"role": "user","content": "你好"}],
        [{"role": "system","content": "你是一个和蔼的人"},
         {"role": "user","content": "你好"},
         {"role": "assistant","content": "你好 我是qq"},
         {"role": "user","content": "你从哪里来"},
         ],
    ]
    for messages in messages_list:
        result = await agent.apredict(messages=messages)
        assert isinstance(result,str)
        assert len(result) > 1

def test_agent_stream_messages(agent):
    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},]}],
        [{"role": "system","content": [{"type": "text", "text": "你是一个和蔼的人"},]},
         {"role": "user","content": [{"type": "text", "text": "你好"},]},
         {"role": "assistant","content": [{"type": "text", "text": "你好 我是qq"},]},
         {"role": "user","content": [{"type": "text", "text": "你从哪里来"},]},
         ],
        [{"role": "user","content": "你好"}],
        [{"role": "system","content": "你是一个和蔼的人"},
         {"role": "user","content": "你好"},
         {"role": "assistant","content": "你好 我是qq"},
         {"role": "user","content": "你从哪里来"},
         ],
    ]
    for messages in messages_list:
        result = agent.stream(messages=messages)
        assert isinstance(result, types.GeneratorType)
        for i in result:
            assert isinstance(i,str)




async def test_agent_astream_messages(agent):
    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},]}],
        [{"role": "system","content": [{"type": "text", "text": "你是一个和蔼的人"},]},
         {"role": "user","content": [{"type": "text", "text": "你好"},]},
         {"role": "assistant","content": [{"type": "text", "text": "你好 我是qq"},]},
         {"role": "user","content": [{"type": "text", "text": "你从哪里来"},]},
         ],
        [{"role": "user","content": "你好"}],
        [{"role": "system","content": "你是一个和蔼的人"},
         {"role": "user","content": "你好"},
         {"role": "assistant","content": "你好 我是qq"},
         {"role": "user","content": "你从哪里来"},
         ],
    ]
    for messages in messages_list:
        result = agent.astream(messages=messages)
        assert isinstance(result, types.AsyncGeneratorType)
        async for i in result:
            assert isinstance(i,str)



@pytest.fixture
def image():
    """
    "gemini-2.5-flash-image-preview",
    "gemini-2.0-flash-preview-image-generation",
    """
    return Adapter(model_name = "gemini-2.0-flash-preview-image-generation",
                   type = "openai")


from modusched.utils import image_to_base64, is_url_urllib

def test_image_stream_messages(image):
    image_path = ''
    if is_url_urllib(image_path):
        image_content = image_path
    else:
        image_base64 = image_to_base64(image_path)
        image_content = f"data:image/jpeg;base64,{image_base64}"

    messages_list =[
        [{"role": "user","content": [{"type": "text", "text": "你好"},
                                     {"type": "image_url", "image_url": {"url": image_content}}]}],
    ]
    for messages in messages_list:
        result = image.image_predict(messages=messages)
        assert isinstance(result, types.GeneratorType)
        for i in result:
            assert isinstance(i,str)