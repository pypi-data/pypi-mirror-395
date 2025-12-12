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

DATABASE_URL = os.getenv("database_url")


class AsyncIntel():
    def __init__(self,
                 database_url = "",
                 model_name = "",
                ):
        
        database_url = database_url or DATABASE_URL
        database_url = "mysql+aiomysql://" + database_url

        self.engine = create_async_engine(database_url, 
                                          echo=False,
                                           )

        type_ = "ark" if "doubao" in model_name else "openai" 
        self.llm = Adapter(model_name=model_name,type=type_)

        # if "gemini" in model_name:
        #     self.llm = BianXieAdapter(model_name = model_name)
        # elif "doubao" in model_name:
        #     self.llm = ArkAdapter(model_name = model_name)
        # else:
        #     raise ModelNameError("AsyncIntel init get error model_name from zxf")
        
    async def create_database(self):
        tables_to_create_names = ["ai_prompts","ai_usecase","ai_data_collection"]
        async with self.engine.begin() as conn:
            # 从 metadata 中获取对应的 Table 对象
            specific_database_objects = []
            for table_name in tables_to_create_names:
                if table_name in PromptBase.metadata.tables:
                    specific_database_objects.append(PromptBase.metadata.tables[table_name])
                else:
                    logging.warning(f"Table '{table_name}' not found in metadata.")


            if specific_database_objects:
                await conn.run_sync(PromptBase.metadata.create_all, tables=specific_database_objects)
            else:
                logging.info("No specific tables to create.")
        return 'success'

    async def _get_prompt(self,prompt_id,version,session):
        """
        获取指定 prompt_id 的最新版本数据，通过创建时间判断。
        """
        if version:
            stmt_ = select(Prompt).filter(
                Prompt.prompt_id == prompt_id,
                Prompt.version == version
            )
        else:  
            stmt_ = select(Prompt).filter(
                Prompt.prompt_id == prompt_id,
            )
        stmt = stmt_.order_by(
                desc(Prompt.timestamp), # 使用 sqlalchemy.desc() 来指定降序
                desc(Prompt.version)    # 使用 sqlalchemy.desc() 来指定降序
            )

        result = await session.execute(stmt)
        result = result.scalars().first()

        return result
    
    async def get_prompt_safe(self,
                             prompt_id: str,
                             version = None,
                             session = None) -> Prompt:
        """
        从sql获取提示词
        """
        prompt_obj = await self._get_prompt(prompt_id=prompt_id,version=version,session=session)
        if prompt_obj:
            return prompt_obj
        if version:
            prompt_obj = await self._get_prompt(prompt_id=prompt_id,version=None,session=session)

        if prompt_obj is None:
            raise IntellectRemoveError("不存在的prompt_id")
        return prompt_obj

    async def get_prompt(self,
                        prompt_id: str,
                        version = None,
                        session = None) -> Prompt:
        if session is None:
            async with create_async_session(self.engine) as session:
                prompt_obj = await self.get_prompt_safe(prompt_id = prompt_id,
                                     version = version,
                                     session = session)
        else:
            prompt_obj = await self.get_prompt_safe(prompt_id = prompt_id,
                version = version,
                session = session)
        
        return prompt_obj


    def check_json_valid(self,llm_output,OutputFormat):

        try:
            json_str = extract_(llm_output,r'json')
            llm_output_json = json.loads(json_str)
            output = OutputFormat(**llm_output_json)
            return output
        except JSONDecodeError as e:
            raise ValueError(f"LLM输出的JSON格式不正确: {e}")
        except ValidationError as e:
            raise ValueError(f"LLM输出不符合Schema要求: {e}")
        except Exception as e:
            raise
                      
    async def get_validated(self,user_theme: str,system_prompt = "",OutputFormat = None, max_retries = 3):
        for attempt in range(max_retries):
            try:
                llm_raw_output = await self.llm.aproduct(prompt=user_theme,
                                                        system_prompt=system_prompt)
                validated = self.check_json_valid(llm_raw_output,OutputFormat=OutputFormat)
                return validated
            except ValueError as e:
                logging.warning(f"尝试 {attempt + 1} 失败: {e}")
                if attempt < max_retries - 1:
                    logging.warning("正在重试...")
                    prompt_template = f"你上次的输出不符合JSON Schema或格式错误，具体错误是：{e}。请修正并重新生成。"
                    user_theme += prompt_template
                else:
                    logging.warning("所有重试均失败。")
                    raise # 最终抛出错误



    async def inference_format(self,
                    input_data: dict | str,
                    prompt_id: str,
                    version: str = None,
                    OutputFormat: object | None = None,
                    ):
        """
        这个format 是严格校验模式, 是interllect 的增强版, 会主动校验内容,并及时抛出异常(或者伺机修正)
        ConTent_Function
        AConTent_Function
        两种方式的传入方式, 内容未通过就抛出异常
        """                
        base_format_prompt = """
# !!! 必须包括MarkDown的json代码块语法
你需要严格遵循以下JSON Schema来输出内容。输出必须是只包含JSON的文本(包括 json代码块语法文本 )，不包含任何额外的解释或文本。

JSON Schema:
```json
{schema_str}
```
请确保生成的JSON是有效的，并且所有字段都符合Schema的要求。
"""
        assert isinstance(input_data,(dict,str))
        # input_data = encode(input_data) if isinstance(input_data,dict) else input_data
        input_data = json.dumps(input_data,ensure_ascii=False) if isinstance(input_data,dict) else input_data

        # get Output_format
        def deal_Output_format(OutputFormat):
            _schema = OutputFormat.model_json_schema()
            schema_str = json.dumps(_schema, indent=2, ensure_ascii=False)
            return base_format_prompt.format(schema_str = schema_str)
        output_format = deal_Output_format(OutputFormat) if OutputFormat else ""
        # output_format = deal_Output_format(OutputFormat) if not isinstance(OutputFormat,str) else OutputFormat

        # get system_prompt
        async with create_async_session(self.engine) as session:
            result_obj = await self.get_prompt(prompt_id=prompt_id,version= version,
                                                    session=session)
            system_prompt = result_obj.prompt + output_format


        # recall & running

        if OutputFormat:
            result = await self.get_validated(input_data,system_prompt=system_prompt,OutputFormat = OutputFormat)

            return result.model_dump()
        else:
            llm_raw_output = await self.llm.aproduct(prompt=input_data,
                                                    system_prompt=system_prompt)
            return llm_raw_output

  
    async def inference_format_gather(self,
                    input_datas: list[dict | str],
                    prompt_id: str,
                    version: str = None,
                    OutputFormat: object | None = None,
                    **kwargs,
                    ):
                
        tasks = []
        for input_data in input_datas:
            tasks.append(
                self.inference_format(
                    input_data = input_data,
                    prompt_id = prompt_id,
                    version = version,
                    OutputFormat = OutputFormat,
                    **kwargs,
                )
            )
        results = await tqdm.gather(*tasks,total=len(tasks))
        return results


    async def save_use_case(self,log_file,session = None):
        logging.warning("save_use_case 即将废弃")
        source_results = await session.execute(
            select(UseCase)
            .order_by(UseCase.timestamp.desc())
            .limit(1)
        )
        records_to_sync = source_results.scalars().one_or_none()
        if records_to_sync:
            last_time = records_to_sync.timestamp
            one_second = timedelta(seconds=1)
            last_time += one_second
        else:
            last_time = datetime(2025, 1, 1, 14, 30, 0)

        with open(log_file,'r') as f:
            x = f.read()

    
        def deal_log(resu):
            if len(resu) <3:
                return 
            try:
                create_time = resu[1]
                level = resu[2]
                funcname = resu[3]
                line = resu[4]
                pathname = resu[5]
                message = resu[6]

                dt_object = datetime.fromtimestamp(float(create_time.strip()))
                message_list = message.split("&")
                if len(message_list) == 3:
                    func_name, input_, output_ = message_list
                elif len(message_list) == 2:
                    input_, output_ = message_list
                    func_name = "只有两个"
                elif len(message_list) == 1:
                    input_  = message_list[0]
                    output_ = " "
                    func_name = "只有一个"

                if dt_object > last_time:
                    use_case = UseCase(
                        time = create_time.strip(),
                        level = level.strip(),
                        timestamp =dt_object.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        filepath=pathname.strip(),
                        function=func_name.strip(),
                        lines=line.strip(),
                        input_data=input_.strip(),
                        output_data=output_.strip(),
                    )
                    session.add(use_case)
            except Exception as e:
                raise


        for res in x.split("||"):
            resu = res.split("$")
            deal_log(resu)

        await session.commit() # 提交事务，将数据写入数据库
        return "success"

    async def save_use_case_2(self,log_path,session = None):
        # 只录入自己的环境的数据库
        source_results = await session.execute(
            select(DataCollection)
            .order_by(DataCollection.timestamp.desc())
            .limit(1)
        )
        records_to_sync = source_results.scalars().one_or_none()
        if records_to_sync:
            last_time = records_to_sync.timestamp
            one_second = timedelta(seconds=1)
            last_time += one_second
        else:
            last_time = datetime(2025, 1, 1, 14, 30, 0)

        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()


        log_lines = lines

        # 用于去除 ANSI 转义序列的正则表达式
        ansi_escape_pattern = re.compile(r'\x1b\[[0-9;]*m')

        # 用于解析日志行的正则表达式
        # 1. 匹配日志级别 (e.g., WARNING, INFO, USECASE)
        # 2. 匹配日期 (YYYY-MM-DD)
        # 3. 匹配时间 (HH:MM:SS)
        # 4. 捕获 '\|' 之后的所有内容作为原始消息 (raw_message)
        log_pattern = re.compile(r'^(WARNING|INFO|USECASE): (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\|(.*)$')
        timestamp_format = "%Y-%m-%d %H:%M:%S"

        parsed_logs = []

        for i, line in enumerate(log_lines):
            # 1. 去除 ANSI 转义序列
            clean_line = ansi_escape_pattern.sub('', line).strip() # .strip() 去除首尾空白和换行符

            # 2. 尝试匹配日志行
            match = log_pattern.match(clean_line)

            if match:
                log_level, timestamp, raw_message = match.groups()

                # 3. 根据 '$' 分割消息为 title 和 content
                if '$' in raw_message:
                    # 找到第一个 '$' 进行分割
                    title, content = raw_message.split('$', 1)
                else:
                    # 如果没有 '$'，则整个消息都是 title，content 为空
                    title = raw_message
                    content = "" # 或 None，根据你的偏好
                dt_object = datetime.strptime(timestamp, timestamp_format)
                unix_timestamp = dt_object.timestamp()

                parsed_logs.append({
                    'line_num': i + 1, # 添加行号方便调试
                    'level': log_level,
                    'timestamp': unix_timestamp,
                    'title': title.strip(), # 去除首尾空白
                    'content': content.strip() # 去除首尾空白
                })
            else:
                # 针对多行日志（如USECASE中的对话）的特殊处理
                # 如果上一条日志是USECASE，并且当前行没有匹配，则可能是USECASE的后续内容
                # 注意：这里假设多行内容不会包含新的时间戳和级别信息
                if parsed_logs and parsed_logs[-1]['level'] == 'USECASE' and not re.match(r'^(WARNING|INFO|USECASE):', clean_line):
                    # 将当前行追加到上一条USECASE日志的content中
                    # 如果之前content是空的，则直接赋值
                    if parsed_logs[-1]['content']:
                        parsed_logs[-1]['content'] += '\n' + clean_line
                    else:
                        parsed_logs[-1]['content'] = clean_line
                else:
                    # 如果不是USECASE的后续，就作为无法解析的行处理
                    parsed_logs.append({'line_num': i + 1, 'raw_line': clean_line, 'status': 'unparsed'})


        # 打印解析结果
        # for log_entry in parsed_logs:
        #     print(log_entry)

        # 示例：查看某个特定日志的 title 和 content
        # print("\n--- 示例：查看 USECASE 日志的 title 和 content ---")
        # for log_entry in parsed_logs:
        #     if log_entry.get('level') == 'USECASE':
        #         print(f"Title: {log_entry['title']}")
        #         print(f"Content: {log_entry['content']}")
        #         break


        for log_entry in parsed_logs:
            log_timestamp_datetimes = datetime.fromtimestamp(float(log_entry['timestamp']))
            if log_timestamp_datetimes > last_time:
                if log_entry['level'] not in ["INFO"]:
                    datacollection = DataCollection(
                        level = log_entry['level'].strip(),
                        timestamp = log_timestamp_datetimes,
                        title = log_entry['title'].strip(),
                        content = log_entry['content'].strip(),
                        is_deleted = 0,
                    )
                    session.add(datacollection)
        
        await session.commit() # 提交事务，将数据写入数据库
        return "success"


    async def sync_log(self,log_path, database_url):
        target_engine = create_async_engine(database_url, echo=False)

        async with create_async_session(target_engine) as session:
            result = await self.save_use_case_2(log_path = log_path,session = session)

        return result

