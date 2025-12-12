"""
DevLake API 客户端

提供与 DevLake REST API 交互的基础功能。

改进：
- 使用 requests 库替代 urllib（更简洁、更强大）
- 完善的错误处理（针对不同HTTP状态码和业务错误）
- 完整的类型注解
- 自动连接池管理

错误处理：
- HTTP 层错误：网络连接、超时、HTTP 4xx/5xx
- 业务层错误：HTTP 200 但 success=false
"""

import logging
import requests
from typing import Any, Dict, List, Optional
from requests.exceptions import RequestException, Timeout, ConnectionError as ReqConnectionError

from .config import DevLakeConfig
from .constants import get_http_retry_count

logger = logging.getLogger(__name__)


# ============================================================================
# 异常类定义
# ============================================================================

class DevLakeAPIError(Exception):
    """DevLake API 错误基类"""
    pass


class DevLakeConnectionError(DevLakeAPIError):
    """连接错误（网络不可达、DNS解析失败等）"""
    pass


class DevLakeTimeoutError(DevLakeAPIError):
    """请求超时错误"""
    pass


class DevLakeAuthError(DevLakeAPIError):
    """认证失败错误（401/403）"""
    pass


class DevLakeNotFoundError(DevLakeAPIError):
    """资源不存在错误（404）"""
    pass


class DevLakeValidationError(DevLakeAPIError):
    """请求参数验证错误（400）"""
    pass


class DevLakeServerError(DevLakeAPIError):
    """服务器错误（5xx）"""
    pass


class DevLakeBusinessError(DevLakeAPIError):
    """业务逻辑错误（HTTP 200 但业务状态异常）"""
    def __init__(self, message: str, code: Optional[int] = None, response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.response_data = response_data


class DevLakeClient:
    """
    DevLake API 客户端

    提供与 DevLake REST API 交互的基础功能，包括：
    - GET/POST/PUT/PATCH/DELETE 请求
    - 自动错误处理（HTTP层 + 业务层）
    - 响应解析
    - 自动连接池管理

    改进：
    - 使用 requests.Session 实现连接池复用
    - 更精细的错误分类和处理（区分HTTP错误和业务错误）
    - 完整的类型注解

    错误层次：
    1. HTTP 层错误 (4xx/5xx): 网络传输层面的错误
       - DevLakeConnectionError: 连接失败
       - DevLakeTimeoutError: 请求超时
       - DevLakeAuthError: 认证失败 (401/403)
       - DevLakeNotFoundError: 资源不存在 (404)
       - DevLakeValidationError: 参数错误 (400)
       - DevLakeServerError: 服务器错误 (5xx)

    2. 业务层错误 (HTTP 200 但 success=false): 应用逻辑层面的错误
       - DevLakeBusinessError: 业务逻辑错误，如字段缺失、数据验证失败等
    """

    def __init__(self, config: Optional[DevLakeConfig] = None):
        """
        初始化客户端

        Args:
            config: DevLake 配置，如果为 None 则从环境变量加载

        注意：
            推荐使用 context manager 来确保资源正确释放：

            with DevLakeClient() as client:
                client.post('/api/sessions', data)
        """
        self.config = config or DevLakeConfig.from_env()

        # 创建 requests Session（连接池复用）
        self.session = requests.Session()
        self.session.headers.update(self.config.get_headers())
        self._closed = False

    def _make_request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        max_retries: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        发起 HTTP 请求（使用 requests 库，支持自动重试）

        Args:
            method: HTTP 方法（GET, POST, PUT, PATCH, DELETE）
            path: API 路径（如 /api/connections）
            data: 请求体数据（自动转换为JSON）
            params: URL 查询参数
            max_retries: 最大重试次数（默认从环境变量读取）

        Returns:
            Dict[str, Any]: 响应 JSON 数据

        Raises:
            DevLakeConnectionError: 连接失败
            DevLakeTimeoutError: 请求超时
            DevLakeAuthError: 认证失败
            DevLakeNotFoundError: 资源不存在
            DevLakeValidationError: 验证失败
            DevLakeServerError: 服务器错误
            DevLakeBusinessError: 业务逻辑错误（HTTP 200 但业务状态异常）
            DevLakeAPIError: 其他 API 错误

        重试策略:
            - 网络错误(ConnectionError): 自动重试
            - 超时错误(Timeout): 自动重试
            - 5xx 服务器错误: 自动重试
            - 4xx 客户端错误: 不重试（参数错误、认证失败等）
        """
        # 构建完整 URL
        url = f"{self.config.base_url}{path}"

        # 获取重试次数
        if max_retries is None:
            max_retries = get_http_retry_count()

        last_exception = None

        # 重试循环（max_retries=1 表示共尝试2次：1次原始请求 + 1次重试）
        for attempt in range(max_retries + 1):
            try:
                # 发起请求
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,  # requests 会自动序列化为 JSON
                    params=params,
                    timeout=self.config.timeout,
                    verify=self.config.verify_ssl
                )

                # 检查 HTTP 状态码
                response.raise_for_status()

                # 解析响应
                if not response.text:
                    return {}

                result = response.json()

                # 检查业务层错误（HTTP 200 但业务状态异常）
                # DevLake API 统一响应格式: {"success": true/false, "error": "...", "data": {...}}
                if isinstance(result, dict) and result.get('success') is False:
                    error_msg = result.get('error', '业务逻辑错误')
                    error_code = result.get('code')  # 可选的错误码
                    raise DevLakeBusinessError(
                        f"业务错误: {error_msg}",
                        code=error_code,
                        response_data=result
                    )

                return result

            except Timeout as e:
                last_exception = e
                # 超时错误：可以重试
                should_retry = attempt < max_retries
                if should_retry:
                    logger.warning(
                        f"请求超时，准备重试（第 {attempt + 1}/{max_retries} 次）: {url}"
                    )
                    continue
                else:
                    raise DevLakeTimeoutError(
                        f"请求超时（{self.config.timeout}秒）: {url}"
                    ) from e

            except ReqConnectionError as e:
                last_exception = e
                # 网络连接错误：可以重试
                should_retry = attempt < max_retries
                if should_retry:
                    logger.warning(
                        f"连接失败，准备重试（第 {attempt + 1}/{max_retries} 次）: {url}\n原因: {str(e)}"
                    )
                    continue
                else:
                    raise DevLakeConnectionError(
                        f"连接失败: {url}\n原因: {str(e)}"
                    ) from e

            except requests.HTTPError as e:
                last_exception = e
                # 获取错误详情
                error_body = ""
                try:
                    error_body = e.response.text if e.response else ""
                except Exception:
                    error_body = "<无法读取错误详情>"

                # 优先从 response 对象获取状态码
                status_code = e.response.status_code if e.response else 0

                # 如果 response 为 None,尝试从错误消息中提取状态码
                # 例如: "400 Client Error: BAD REQUEST"
                if status_code == 0:
                    import re
                    error_str = str(e)
                    match = re.match(r'^(\d{3})\s', error_str)
                    if match:
                        status_code = int(match.group(1))

                # 判断是否应该重试（5xx 服务器错误可以重试）
                should_retry = (status_code >= 500) and (attempt < max_retries)

                if should_retry:
                    logger.warning(
                        f"服务器错误({status_code})，准备重试（第 {attempt + 1}/{max_retries} 次）: {url}"
                    )
                    continue

                # 根据状态码抛出不同的异常
                if status_code == 0:
                    # 没有收到响应（response 为 None），说明请求根本没发出去或者被中断
                    raise DevLakeAPIError(
                        f"HTTP 请求失败，未收到响应\n"
                        f"URL: {url}\n"
                        f"方法: {method}\n"
                        f"原始错误: {str(e)}"
                    ) from e
                elif status_code == 400:
                    # 添加请求数据到错误信息中，帮助调试
                    import json
                    request_data = json.dumps(data, ensure_ascii=False, indent=2) if data else "无"
                    raise DevLakeValidationError(
                        f"请求参数错误（400 Bad Request）\n"
                        f"URL: {url}\n"
                        f"请求数据: {request_data}\n"
                        f"服务器响应: {error_body}"
                    ) from e
                elif status_code == 401:
                    raise DevLakeAuthError(
                        f"认证失败，请检查 API Token"
                    ) from e
                elif status_code == 403:
                    raise DevLakeAuthError(
                        f"权限不足，无法访问资源: {path}"
                    ) from e
                elif status_code == 404:
                    raise DevLakeNotFoundError(
                        f"资源不存在: {path}"
                    ) from e
                elif status_code >= 500:
                    raise DevLakeServerError(
                        f"服务器错误({status_code}): {error_body}"
                    ) from e
                else:
                    raise DevLakeAPIError(
                        f"API错误({status_code}): {error_body}"
                    ) from e

            except RequestException as e:
                last_exception = e
                raise DevLakeAPIError(
                    f"请求失败: {str(e)}"
                ) from e

        # 理论上不会到这里，但为了安全
        if last_exception:
            raise last_exception

        # 如果所有重试都失败了，但没有捕获到异常（极端情况）
        raise DevLakeAPIError(f"请求失败，未知错误: {url}")

    def close(self):
        """
        关闭 session 释放连接池资源

        在不使用 context manager 时，建议手动调用此方法释放资源。
        """
        if not self._closed:
            self.session.close()
            self._closed = True

    def __enter__(self):
        """Context manager 进入"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager 退出，确保资源释放"""
        self.close()
        return False

    def __del__(self):
        """析构函数，确保资源最终被释放"""
        try:
            self.close()
        except Exception:
            # 析构时忽略所有异常
            pass

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        发起 GET 请求

        Args:
            path: API 路径
            params: URL 查询参数

        Returns:
            Dict[str, Any]: 响应数据
        """
        return self._make_request("GET", path, params=params)

    def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        发起 POST 请求

        Args:
            path: API 路径
            data: 请求体数据

        Returns:
            Dict[str, Any]: 响应数据
        """
        return self._make_request("POST", path, data=data)

    def put(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        发起 PUT 请求

        Args:
            path: API 路径
            data: 请求体数据

        Returns:
            Dict[str, Any]: 响应数据
        """
        return self._make_request("PUT", path, data=data)

    def patch(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        发起 PATCH 请求

        Args:
            path: API 路径
            data: 请求体数据

        Returns:
            Dict[str, Any]: 响应数据
        """
        return self._make_request("PATCH", path, data=data)

    def delete(self, path: str) -> Dict[str, Any]:
        """
        发起 DELETE 请求

        Args:
            path: API 路径

        Returns:
            Dict[str, Any]: 响应数据
        """
        return self._make_request("DELETE", path)

    def health_check(self) -> Dict[str, Any]:
        """
        健康检查

        Returns:
            Dict[str, Any]: 健康状态信息
        """
        try:
            # DevLake 的健康检查端点
            response = self.get("/api/ping")
            return {
                "status": "healthy",
                "message": "DevLake API is accessible",
                "base_url": self.config.base_url,
                "response": response
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": str(e),
                "base_url": self.config.base_url
            }

    # ========================================================================
    # AI Coding API 便捷方法（用于 Hooks）
    # ========================================================================

    def create_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建 AI 编码会话

        Args:
            session_data: 会话数据（包含 session_id, user_name, git_repo_path 等）

        Returns:
            Dict[str, Any]: 创建的会话数据
        """
        return self.post("/api/ai-coding/sessions", session_data)

    def update_session(self, session_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新 AI 编码会话

        Args:
            session_id: 会话 ID
            update_data: 更新数据

        Returns:
            Dict[str, Any]: 更新后的会话数据
        """
        return self.patch(f"/api/ai-coding/sessions/{session_id}", update_data)

    def increment_session_rounds(self, session_id: str) -> Dict[str, Any]:
        """
        增加会话的对话轮数（conversation_rounds）

        Args:
            session_id: 会话 ID

        Returns:
            Dict[str, Any]: 更新后的会话数据
        """
        return self.patch(f"/api/ai-coding/sessions/{session_id}/increment-rounds", {})


    def create_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建 Prompt 记录

        Args:
            prompt_data: Prompt 数据（包含 session_id, prompt_uuid, prompt_content 等）

        Returns:
            Dict[str, Any]: 创建的 Prompt 数据
        """
        return self.post("/api/ai-coding/prompts", prompt_data)

    def get_prompt(self, prompt_uuid: str) -> Dict[str, Any]:
        """
        获取 Prompt 记录

        Args:
            prompt_uuid: Prompt UUID（使用 generation_id）

        Returns:
            Dict[str, Any]: Prompt 数据
        """
        return self.get(f"/api/ai-coding/prompts/{prompt_uuid}")

    def update_prompt(self, prompt_uuid: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新 Prompt 记录

        Args:
            prompt_uuid: Prompt UUID（使用 generation_id）
            update_data: 更新数据（如 response_content, status, loop_count 等）

        Returns:
            Dict[str, Any]: 更新后的 Prompt 数据
        """
        return self.patch(f"/api/ai-coding/prompts/{prompt_uuid}", update_data)

    def create_file_changes(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        批量创建文件变更记录

        Args:
            changes: 文件变更列表

        Returns:
            Dict[str, Any]: 创建结果
        """
        return self.post("/api/ai-coding/file-changes", {"changes": changes})

    def create_transcript(self, transcript_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建 Transcript 记录

        Args:
            transcript_data: Transcript 数据（包含 session_id, transcript_content 等）
                           现支持 upload_source 字段：'auto', 'auto_backfill', 'manual'

        Returns:
            Dict[str, Any]: 创建的 Transcript 数据
        """
        return self.post("/api/ai-coding/transcripts", transcript_data)

    def check_transcript_exists(self, session_id: str) -> bool:
        """
        检查 Transcript 是否已在服务端存在

        Args:
            session_id: 会话 ID

        Returns:
            bool: True 表示已存在，False 表示不存在
        """
        try:
            response = self.get(f"/api/ai-coding/transcripts/{session_id}")
            # 如果能成功获取到数据，说明已存在
            # 服务端返回格式: {"success": true, "data": {...}}
            if response.get('success') and response.get('data'):
                return True
            return False
        except DevLakeNotFoundError:
            # 404 表示不存在
            return False
        except Exception as e:
            # 其他错误，记录日志后返回 False（保守策略：假设不存在，允许上传）
            logger = logging.getLogger(__name__)
            logger.warning(f"检查 transcript 是否存在时出错: {session_id} - {e}")
            return False
