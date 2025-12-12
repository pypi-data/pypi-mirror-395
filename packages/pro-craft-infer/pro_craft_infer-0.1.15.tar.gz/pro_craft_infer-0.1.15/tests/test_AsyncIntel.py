from pro_craft_infer.core import AsyncIntel
import pytest
import types
from toolkitz.content import create_async_session



@pytest.fixture
def intel():
    database_url="vc_agent:aihuashen%402024@rm-2ze0q808gqplb1tz72o.mysql.rds.aliyuncs.com:3306/digital-life2"
    intel = AsyncIntel(database_url=database_url,
                       model_name = "doubao-1-5-pro-32k-250115"
                       )
    return intel

def test_create_database(intel):
    # 默认可用
    pass


async def test_get_prompt_with_session(intel):

    async with create_async_session(intel.engine) as session:
        result = await intel.get_prompt(prompt_id = '',
                                version=None,
                                session = session)
        print(result,'result')
    


def test_get_prompt(intel):
    result = intel.get_prompt(prompt_id = '',
                              version=None)
    print(result)
    
    


def test_inference_format(intel):
    pass

def test_inference_format_gather(intel):
    pass

def test_sync_log(intel):
    intel.sync_log(log_path="", database_url="")
    pass

