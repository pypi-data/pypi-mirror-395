import random


class UaGenerator:
    """
    User-Agent 生成器 V7.0 (最终终极版本，针对 2025 年 12 月最新 OS/浏览器版本迭代)

    所有 UA 均针对最高通过率和真实性进行优化，特别修复了 macOS/iOS 版本致命点。
    """

    # --- 关键版本范围 (收缩到 143 附近，保持最新 OS 26) ---
    CHROME_MAJOR = [143] * 3  # 严格锁定在最新稳定版 143
    EDGE_MAJOR = [143] * 3  # 严格锁定在最新稳定版 143
    FIREFOX_MAJOR = list(range(146, 150))  # 包含稳定版 146 和您确认的 147+
    SAFARI_VERSION = ["26.0"] * 3  # 严格锁定在最新 OS 伴随的 26.0

    # --- 平台碎片映射 (修复 macOS/iOS 致命点) ---
    WINDOWS_PLATFORMS = ["Windows NT 10.0; Win64; x64"] * 3  # NT 10.0 正确

    # 致命修复：macOS Safari 必须使用 10_15_7 样式
    MACOS_PLATFORMS = ["Macintosh; Intel Mac OS X 10_15_7"] * 3

    LINUX_PLATFORMS = ["X11; Linux x86_64", "X11; Ubuntu; Linux x86_64"]

    # 升级到 Android 16
    ANDROID_PLATFORMS = [
        "Linux; Android 16; Pixel 9",
        "Linux; Android 16; SM-G9980",
        "Linux; Android 16; Mi 15"
    ]
    # 致命修复：iOS/iPadOS 升级到 26.0
    IOS_PLATFORMS = [
        "iPhone; CPU iPhone OS 26_0 like Mac OS X",
        "iPad; CPU OS 26_0 like Mac OS X",
    ]

    PLATFORM_MAP = {
        'windows': WINDOWS_PLATFORMS, 'macos': MACOS_PLATFORMS, 'linux': LINUX_PLATFORMS,
        'android': ANDROID_PLATFORMS, 'ios': IOS_PLATFORMS,
    }

    # --- 核心方法保持 V4.0 结构 ---

    @staticmethod
    def rand_ver(*parts):
        return ".".join(str(random.randint(*p) if isinstance(p, tuple) else p) for p in parts)

    @classmethod
    def _get_platform_string(cls, platform_type):
        platform_type = platform_type.lower()
        if platform_type in cls.PLATFORM_MAP:
            return random.choice(cls.PLATFORM_MAP[platform_type])
        return None

    @classmethod
    def chrome(cls, *, platform: str, version=None):
        major = version or random.choice(cls.CHROME_MAJOR)
        full_version = f"{major}.0.{random.randint(7000, 7500)}.{random.randint(50, 150)}"
        mobile = "Mobile " if 'Android' in platform or 'iPhone' in platform or 'iPad' in platform else ""
        return (
            f"Mozilla/5.0 ({platform}) AppleWebKit/537.36 "
            f"(KHTML, like Gecko) Chrome/{full_version} {mobile}Safari/537.36"
        )

    @classmethod
    def edge(cls, *, platform: str, version=None):
        major = version or random.choice(cls.EDGE_MAJOR)
        full_version = f"{major}.0.{random.randint(2500, 3000)}.{random.randint(30, 120)}"

        return (
            f"Mozilla/5.0 ({platform}) AppleWebKit/537.36 "
            f"(KHTML, like Gecko) Chrome/{full_version} Safari/537.36 Edg/{full_version}"
        )

    @classmethod
    def firefox(cls, *, platform: str, version=None):
        major = version or random.choice(cls.FIREFOX_MAJOR)
        return (
            f"Mozilla/5.0 ({platform}; rv:{major}.0) "
            f"Gecko/20100101 Firefox/{major}.0"
        )

    @classmethod
    def safari(cls, *, platform: str, version=None):
        version_str = version or random.choice(cls.SAFARI_VERSION)
        is_ios = 'iPhone' in platform or 'iPad' in platform
        # 使用 Mobile/15E148 或更新的通用 Mobile/Build ID 样式
        mobile_part = " Mobile/15E148" if is_ios else ""

        return (
            f"Mozilla/5.0 ({platform}) AppleWebKit/605.1.15 "
            f"(KHTML, like Gecko) Version/{version_str}{mobile_part} Safari/605.1.15"
        )

    # --- 统一生成方法 (V4.0 结构) ---

    @classmethod
    def generate(cls, browser, platform_type, version=None, custom_platform=None):
        browser_map = {
            'chrome': cls.chrome, 'edge': cls.edge,
            'firefox': cls.firefox, 'safari': cls.safari,
        }

        browser_func = browser_map.get(browser.lower())
        if not browser_func:
            raise ValueError(f"不支持的浏览器: {browser}.")

        if custom_platform:
            platform_str = custom_platform
        else:
            platform_str = cls._get_platform_string(platform_type)
            if not platform_str:
                raise ValueError(f"不支持的平台类型: {platform_type}.")

        return browser_func(platform=platform_str, version=version)

    # --- 随机生成方法 (基于优化的真实分布) ---

    @classmethod
    def random(cls):
        r = random.random()

        if r < 0.58:
            platform_type = random.choice(['windows', 'macos', 'linux', 'android'])
            return cls.generate('chrome', platform_type)
        elif r < 0.77:
            return cls.generate('edge', 'windows')
        elif r < 0.86:
            platform_type = random.choice(['windows', 'macos', 'linux'])
            return cls.generate('firefox', platform_type)
        else:
            platform_type = random.choice(['macos', 'ios'])
            return cls.generate('safari', platform_type)
