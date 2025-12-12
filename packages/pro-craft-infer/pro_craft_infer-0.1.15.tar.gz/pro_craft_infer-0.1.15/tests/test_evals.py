from pydantic import BaseModel, ValidationError, field_validator
from json.decoder import JSONDecodeError
from sqlalchemy import select, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from toolkitz.re import extract_
from toolkitz.content import create_async_session
from .database import Prompt, UseCase, DataCollection, PromptBase
from datetime import datetime, timedelta, datetime
from tqdm.asyncio import tqdm
from tqdm import tqdm as tqdm_sync
import json
import os
import pytest
import re
from pro_craft_infer.utils import IntellectRemoveError,IntellectRemoveFormatError,ModelNameError
import logging
from modusched.core import BianXieAdapter, ArkAdapter, Adapter


def calculate_pass_rate_and_assert(results, test_name, PASS_THRESHOLD_PERCENT = 90,bad_case = []):
    """
    辅助函数：计算通过率并根据阈值进行断言。
    results: 包含 True (通过) 或 False (失败) 的列表
    test_name: 测试名称，用于打印信息
    """
    result_text = ""
    if not results:
        pytest.fail(f"测试 '{test_name}' 没有执行任何子用例。")

    total_sub_cases = len(results)
    passed_sub_cases = results.count(True)
    pass_rate = (passed_sub_cases / total_sub_cases) * 100

    result_text +=f"\n--- 测试 '{test_name}' 内部结果 ---\n"
    result_text +=f"总子用例数: {total_sub_cases}\n"
    result_text +=f"通过子用例数: {passed_sub_cases}\n"
    result_text +=f"通过率: {pass_rate:.2f}%\n"

    if pass_rate >= PASS_THRESHOLD_PERCENT:
        result_text += f"通过率 ({pass_rate:.2f}%) 达到或超过 {PASS_THRESHOLD_PERCENT}%。测试通过。\n"
        assert True # 显式断言成功
        x = 0
    else:
        result_text += f"通过率 ({pass_rate:.2f}%) 低于 {PASS_THRESHOLD_PERCENT}%。测试失败。\n"
        result_text += "bad_case:" + '\n'.join(bad_case)
        x = 1
    return result_text,x

async def atest_by_use_case(func:object,
                            eval,
                            PASS_THRESHOLD_PERCENT=90,
                           database_url = "",
                           limit_number = 100):

    engine = create_async_engine(database_url, 
                                 echo=False,
                                pool_size=10,        # 连接池中保持的连接数
                                max_overflow=20,     # 当pool_size不够时，允许临时创建的额外连接数
                                pool_recycle=3600,   # 每小时回收一次连接
                                pool_pre_ping=True,  # 使用前检查连接活性
                                pool_timeout=30      # 等待连接池中连接的最长时间（秒）
                                        )

    async with create_async_session(engine) as session:
        result = await session.execute(
              select(UseCase)
              .filter(UseCase.function==func.__name__,UseCase.is_deleted==0)
              .order_by(UseCase.timestamp.desc())
              .limit(limit_number)
        )
        usecase = result.scalars().all()
        sub_case_results = []
        bad_case = []
        for usecase_i in tqdm_sync(usecase):
            try:
                usecase_dict = json.loads(usecase_i.input_data)
                result = await func(**usecase_dict)
                await eval(result,usecase_i)
                sub_case_results.append(True)
            except AssertionError as e:
                sub_case_results.append(False)
                bad_case.append(f"input: {usecase_dict} 未通过, putput: {result}, Error Info: {e}")
            except Exception as e:
                raise Exception(f"意料之外的错误 {e}")

        return calculate_pass_rate_and_assert(sub_case_results, f"test_{func.__name__}_pass_{PASS_THRESHOLD_PERCENT}",PASS_THRESHOLD_PERCENT,
                                              bad_case=bad_case)
    