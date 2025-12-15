import logging
from datetime import datetime, timedelta
from os import environ
from pathlib import Path
from typing import Callable, Optional

import httpx
import maxminddb
import pandas as pd


# --- 配置日志 ---
logger = logging.getLogger("iplocate")
logger.setLevel(logging.INFO)

# --- 常量配置 ---
IPLOCATE_API_KEY = environ.get("IPLOCATE_API_KEY", "xxx-xxx-xxx")
CSV_URL = f"https://www.iplocate.io/download/ip-to-asn.csv?apikey={IPLOCATE_API_KEY}&variant=daily"
MMDB_URL = f"https://www.iplocate.io/download/ip-to-asn.mmdb?apikey={IPLOCATE_API_KEY}&variant=daily"

# 缓存和输出配置
CACHE_DIR = Path("./cache")
OUTPUT_DIR = Path(".")
FILE_PREFIX = "ruleset-"
CACHE_EXPIRE_HOURS = 24


def download_ip_asn_data(
    url: str,
    cache_dir: Path = CACHE_DIR,
    expire_hours: int = CACHE_EXPIRE_HOURS,
) -> Path:
    """
    下载IP-ASN数据到缓存目录，返回缓存文件路径

    Args:
        url: 数据源URL
        cache_dir: 缓存目录
        expire_hours: 缓存过期时间（小时）

    Returns:
        Path: 缓存文件路径
    """
    cache_dir.mkdir(parents=True, exist_ok=True)

    # 从URL生成缓存文件名
    url_path = Path(url.split("?")[0])
    cache_file = cache_dir / url_path.name

    # 检查缓存文件是否存在且未过期
    if cache_file.exists():
        file_mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if datetime.now() - file_mtime < timedelta(hours=expire_hours):
            logger.info(f"使用缓存文件: {cache_file}")
            return cache_file
        else:
            logger.info(f"缓存文件已过期（超过 {expire_hours} 小时）")

    # 下载新数据
    logger.info(f"开始下载数据: {url}")
    try:
        with httpx.Client(headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }) as client:
            response = client.get(url, follow_redirects=True, timeout=300)
            response.raise_for_status()

            # 保存到缓存文件
            cache_file.write_bytes(response.content)
            logger.info(f"数据已缓存到: {cache_file}")

            return cache_file
    except httpx.HTTPError as e:
        logger.error(f"下载失败: {e}")
        raise


def generate_asn_ruleset_from_csv(
    file_path: Path,
    country_code: str = "CN",
    output_dir: Path = OUTPUT_DIR,
    file_prefix: str = FILE_PREFIX,
) -> Path:
    """
    从 CSV/ZIP 文件中提取 ASN，生成规则集

    Args:
        file_path: CSV 或 ZIP 文件路径
        country_code: 国家代码
        output_dir: 输出目录
        file_prefix: 输出文件前缀

    Returns:
        Path: 生成的配置文件路径
    """
    logger.info(f"处理 CSV 文件: {file_path}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 根据文件扩展名决定如何读取
    if file_path.suffix.lower() == ".zip":
        # ZIP 压缩的 CSV
        df = pd.read_csv(file_path, compression="zip")
    elif file_path.suffix.lower() == ".csv":
        # 直接的 CSV
        df = pd.read_csv(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {file_path.suffix}")

    # 筛选指定国家的ASN
    df_filtered = df[df["country_code"] == country_code]
    as_numbers = sorted(set(df_filtered["asn"].values))

    # 生成配置文件
    output_file = output_dir / f"{file_prefix}asn-{country_code.lower()}-v2.conf"

    with open(output_file, "w", encoding="utf8") as wf:
        rules = [f"IP-ASN,{as_number}" for as_number in as_numbers]
        wf.write("\n".join(rules))

    logger.info(f"已生成配置文件: {output_file} (共 {len(as_numbers)} 个ASN)")
    return output_file


def generate_asn_ruleset_from_mmdb(
    file_path: Path,
    country_code: Optional[str] = None,  # MMDB 通常不支持按国家筛选
    output_dir: Path = OUTPUT_DIR,
    file_prefix: str = FILE_PREFIX,
) -> Path:
    """
    从 MMDB 文件中提取 ASN，生成规则集

    Args:
        file_path: MMDB 文件路径
        country_code: 国家代码（MMDB 通常不支持此参数）
        output_dir: 输出目录
        file_prefix: 输出文件前缀

    Returns:
        Path: 生成的配置文件路径
    """
    logger.info(f"处理 MMDB 文件: {file_path}")
    output_dir.mkdir(parents=True, exist_ok=True)

    as_numbers = set()

    try:
        with maxminddb.open_database(file_path) as reader:
            for _, record in reader:
                if record and record.get("country_code") == "CN":
                    as_numbers.add(record["asn"])
    except maxminddb.InvalidDatabaseError as e:
        logger.error(f"MMDB 文件无效: {e}")
        raise

    sorted_as_numbers = sorted(as_numbers)

    # 生成配置文件名
    if country_code:
        output_file = output_dir / f"{file_prefix}asn-{country_code.lower()}-v2.conf"
    else:
        output_file = output_dir / f"{file_prefix}asn-all-mmdb.conf"

    with open(output_file, "w", encoding="utf8") as wf:
        rules = [f"IP-ASN,{as_number}" for as_number in sorted_as_numbers]
        wf.write("\n".join(rules))

    logger.info(f"已生成配置文件: {output_file} (共 {len(sorted_as_numbers)} 个ASN)")
    return output_file


def get_processor(file_path: Path) -> Callable[[Path, str, Path, str], Path]:
    """
    根据文件路径的后缀选择相应的处理函数

    Args:
        file_path: 文件路径

    Returns:
        Callable: 处理函数
    """
    suffix = file_path.suffix.lower()

    if suffix in [".csv", ".zip"]:
        return generate_asn_ruleset_from_csv
    elif suffix == ".mmdb":
        return generate_asn_ruleset_from_mmdb
    else:
        raise ValueError(f"不支持的文件格式: {suffix}")


def process_ip_asn_data(
    url: str,
    country_code: str = "CN",
    cache_dir: Path = CACHE_DIR,
    output_dir: Path = OUTPUT_DIR,
    file_prefix: str = FILE_PREFIX,
) -> Path:
    """
    完整的数据处理流程：下载并处理 IP-ASN 数据

    Args:
        url: 数据源URL
        country_code: 国家代码
        cache_dir: 缓存目录
        output_dir: 输出目录
        file_prefix: 输出文件前缀

    Returns:
        Path: 生成的配置文件路径
    """
    # 1. 下载数据，获取文件路径
    file_path = download_ip_asn_data(url, cache_dir)

    # 2. 获取对应的处理函数
    processor = get_processor(file_path)
    logger.info(f"选择处理器: {processor.__name__}")

    # 3. 处理数据
    output_path = processor(
        file_path=file_path,
        country_code=country_code,
        output_dir=output_dir,
        file_prefix=file_prefix
    )

    return output_path


# --- 主程序逻辑 ---
if __name__ == "__main__":
    # 选择要使用的数据源
    current_url = MMDB_URL  # 或 MMDB_URL
    target_country = "CN"

    try:
        output_path = process_ip_asn_data(
            url=current_url,
            country_code=target_country
        )

        print(f"\n任务完成，使用的URL: {current_url}")
        print(f"输出文件: {output_path}")

    except Exception as e:
        logger.error(f"执行失败: {e}", exc_info=True)
