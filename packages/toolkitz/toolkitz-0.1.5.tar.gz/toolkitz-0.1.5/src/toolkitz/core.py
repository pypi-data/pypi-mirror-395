
import time
from contextlib import contextmanager
from contextlib import asynccontextmanager # 注意这里是 asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine # 异步核心
from sqlalchemy.orm import sessionmaker


@contextmanager
def check_time(title:str,logger):
    """ try catch"""
    time1 = time.time()
    yield
    time2 = time.time()
    logger.debug(f"{title}: {time2-time1}")

@contextmanager
def create_session(engine):
    # 5. 创建会话 (Session)
    # Session 是与数据库交互的主要接口，它管理着你的对象和数据库之间的持久化操作
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session

    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback() # 发生错误时回滚事务
    finally:
        session.close() # 关闭会话，释放资源


@asynccontextmanager
async def create_async_session(async_engine):
    # 5. 创建会话 (Session)
    # Session 是与数据库交互的主要接口，它管理着你的对象和数据库之间的持久化操作
    Session = sessionmaker(bind=async_engine,
                           expire_on_commit=False, 
                           class_=AsyncSession
                           )
    session = Session()
    try:
        yield session
        # await session.commit() # 在成功的情况下自动提交事务

    except Exception as e:
        print(f"An error occurred: {e}")
        await session.rollback() # 发生错误时回滚事务
        raise # 重新抛出异常，让调用者知道操作失败
    finally:
        await session.close() # 关闭会话，释放资源


## File


""" 文件工具 """
import importlib
import yaml


def load_inpackage_file(package_name: str, file_name: str, file_type="yaml"):
    """load config"""
    with importlib.resources.open_text(package_name, file_name) as f:
        if file_type == "yaml":
            return yaml.safe_load(f)
        else:
            return f.read()

import toml

def get_pyproject_toml():
    # 从文件读取
    try:
        with open('pyproject.toml', 'r', encoding='utf-8') as f:
            data = toml.load(f)
        print("--- Loaded TOML data ---")
        print(data)
        print("\n--- Accessing data ---")
        print(f"Project name: {data['project']['name']}")
        print(f"Dependencies: {data['project']['dependencies']}")
        print(f"UV cache dir: {data['tool']['uv']['cache-dir']}")
        print(f"Lint check imports: {data['tool']['lint']['check-imports']}")

    except FileNotFoundError:
        print("pyproject.toml not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # 从字符串读取
    toml_string = """
    [user]
    name = "Alice"
    age = 30
    is_active = true
    """
    parsed_string_data = toml.loads(toml_string)
    print("\n--- Parsed string data ---")
    print(parsed_string_data)
    print(f"User name: {parsed_string_data['user']['name']}")

## RE

import re

def extract_(text: str, pattern_key = r"json",multi = False):
    pattern = r"```"+ pattern_key + r"([\s\S]*?)```"
    matches = re.findall(pattern, text)
    if multi:
        [match.strip() for match in matches]
        if matches:
            return [match.strip() for match in matches]    
        else:
            return ""  # 返回空字符串或抛出异常，此处返回空字符串
    else:
        if matches:
            return matches[0].strip()  # 添加strip()去除首尾空白符
        else:
            return ""  # 返回空字符串或抛出异常，此处返回空字符串



