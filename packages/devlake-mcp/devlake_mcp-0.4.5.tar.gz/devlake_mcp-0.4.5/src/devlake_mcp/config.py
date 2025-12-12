"""
DevLake 配置管理

统一管理 DevLake 的所有配置：
- MCP 服务器配置（DevLakeConfig）
- Hooks 环境配置（init_hooks_env）
- Git 信息缓存机制
"""

import os
import sys
from dataclasses import dataclass
from typing import Optional, Dict

# 导入常量配置
from .constants import (
    DEFAULT_API_BASE_URL,
    API_REQUEST_TIMEOUT,
)


@dataclass
class DevLakeConfig:
    """DevLake 配置类（用于 MCP 服务器和 Hooks）"""

    # API 基础 URL
    base_url: str

    # API Token（如果需要认证）
    api_token: Optional[str] = None

    # 超时设置（秒）
    timeout: int = 30

    # 是否启用 SSL 验证
    verify_ssl: bool = True

    # Git 配置（用于 Hooks）
    git_repo_path: Optional[str] = None
    git_email: Optional[str] = None
    git_author: Optional[str] = None

    @classmethod
    def from_env(cls, include_git: bool = False) -> "DevLakeConfig":
        """
        从环境变量加载配置

        Args:
            include_git: 是否包含 Git 配置（Hooks 使用）

        环境变量：
        - DEVLAKE_BASE_URL: DevLake API 地址（默认：http://devlake.test.chinawayltd.com）
        - DEVLAKE_API_TOKEN: API Token（可选）
        - DEVLAKE_TIMEOUT: 请求超时时间（默认：5 秒）
        - DEVLAKE_VERIFY_SSL: 是否验证 SSL（默认：true）

        Git 环境变量（include_git=True 时）：
        - GIT_REPO_PATH: Git仓库路径
        - GIT_EMAIL: Git邮箱
        - GIT_AUTHOR: Git用户名

        Returns:
            DevLakeConfig: 配置实例
        """
        # API 配置
        base_url = os.getenv('DEVLAKE_BASE_URL', DEFAULT_API_BASE_URL)
        api_token = os.getenv('DEVLAKE_API_TOKEN')
        timeout = int(os.getenv('DEVLAKE_TIMEOUT', str(API_REQUEST_TIMEOUT)))
        verify_ssl = os.getenv('DEVLAKE_VERIFY_SSL', "true").lower() == "true"

        config = cls(
            base_url=base_url.rstrip("/"),
            api_token=api_token,
            timeout=timeout,
            verify_ssl=verify_ssl
        )

        # 加载 Git 配置（Hooks 专用）
        if include_git:
            config._load_git_config()

        return config

    def _load_git_config(self) -> None:
        """加载 Git 配置并同步到环境变量（内部方法）"""
        self.git_repo_path = os.getenv('GIT_REPO_PATH')
        self.git_email = os.getenv('GIT_EMAIL')
        self.git_author = os.getenv('GIT_AUTHOR')

        # 如果环境变量未设置，尝试从 Git 配置读取
        if not self.git_repo_path or not self.git_email:
            try:
                from .git_utils import get_git_repo_path, get_git_info

                cwd = os.getcwd()

                if not self.git_repo_path:
                    self.git_repo_path = get_git_repo_path(cwd)
                    os.environ['GIT_REPO_PATH'] = self.git_repo_path

                if not self.git_email or not self.git_author:
                    git_info = get_git_info(cwd, include_user_info=True)
                    if not self.git_email:
                        self.git_email = git_info.get('git_email', 'unknown')
                        os.environ['GIT_EMAIL'] = self.git_email
                    if not self.git_author:
                        self.git_author = git_info.get('git_author', 'unknown')
                        os.environ['GIT_AUTHOR'] = self.git_author

            except Exception as e:
                print(f"\n⚠️  警告：获取 Git 配置失败：{str(e)}", file=sys.stderr)
                if not self.git_repo_path:
                    self.git_repo_path = 'unknown'
                    os.environ['GIT_REPO_PATH'] = 'unknown'
                if not self.git_email:
                    self.git_email = 'unknown'
                    os.environ['GIT_EMAIL'] = 'unknown'
                if not self.git_author:
                    self.git_author = 'unknown'
                    os.environ['GIT_AUTHOR'] = 'unknown'

        # 验证必需的 Git 配置
        self._validate_git_config()

    def _validate_git_config(self):
        """验证 Git 配置（内部方法）"""
        missing_configs = []

        if not self.git_repo_path or self.git_repo_path == 'unknown' or self.git_repo_path.startswith('local/'):
            missing_configs.append('remote.origin.url')

        if not self.git_email or self.git_email == 'unknown':
            missing_configs.append('user.email')

        if missing_configs:
            print("\n" + "="*60, file=sys.stderr)
            print("❌ 错误：缺少必需的 Git 配置", file=sys.stderr)
            print("="*60, file=sys.stderr)
            print("\n📝 请按照以下步骤配置 Git：\n", file=sys.stderr)

            if 'remote.origin.url' in missing_configs:
                print("1️⃣  配置 Git 远程仓库：", file=sys.stderr)
                print("   git remote add origin <repository-url>", file=sys.stderr)
                print("", file=sys.stderr)

            if 'user.email' in missing_configs:
                print("2️⃣  配置 Git 用户邮箱：", file=sys.stderr)
                print("   git config user.email 'your-email@example.com'", file=sys.stderr)
                print("", file=sys.stderr)

            print("💡 提示：配置完成后，请重新运行命令。", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            sys.exit(2)

    def get_headers(self) -> Dict[str, str]:
        """
        获取请求头

        Returns:
            dict: 请求头字典
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        return headers

    @classmethod
    def initialize_for_hooks(cls) -> "DevLakeConfig":
        """
        为 Hooks 环境初始化配置

        这个方法会：
        1. 从环境变量加载 API 配置
        2. 获取静态 Git 信息（author, email, repo_path）并缓存到环境变量
        3. 验证配置完整性

        注意：
        - 只缓存静态信息（author, email, repo_path）
        - 动态信息（branch, commit）每次都重新获取，确保最新值

        Returns:
            DevLakeConfig: 已初始化的配置实例

        使用示例：
            # 在 hooks 启动脚本中调用一次
            config = DevLakeConfig.initialize_for_hooks()

            # 静态信息从环境变量读取（已缓存）
            git_author = os.getenv('GIT_AUTHOR')
            git_email = os.getenv('GIT_EMAIL')

            # 动态信息每次获取最新值
            git_info = get_git_info(cwd, include_user_info=False)
            git_branch = git_info.get('git_branch')
        """
        # 加载配置并获取静态 Git 信息（会自动缓存到环境变量）
        config = cls.from_env(include_git=True)

        return config
