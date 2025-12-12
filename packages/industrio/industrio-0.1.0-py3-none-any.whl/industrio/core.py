# industrio/core.py
import requests
import time
from .config import CONTROLS, SENSORS, REQUEST_TIMEOUT

class GatewayClient:
    def __init__(self):
        self.status = {}  # 存储解析后的设备状态

    def _parse_status(self, status_str):
        """解析网关返回的状态字符串"""
        cleaned = status_str.strip(",; ")
        devices = [d for d in cleaned.split(";") if d.strip()]
        for device in devices:
            parts = device.split(",")
            if len(parts) == 2:
                name, value = parts[0].strip(), parts[1].strip()
                # 自动转换数值类型
                try:
                    value = float(value) if "." in value else int(value)
                except ValueError:
                    pass
                self.status[name] = value

    def get_status(self, ip=None):
        """获取并更新网关状态"""
        from . import ip as global_ip  # 延迟导入，避免循环依赖
        target_ip = ip or global_ip
        if not target_ip:
            print("❌ 未设置网关IP，请先设置 industrio.ip")
            return {}
            
        url = target_ip
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            self._parse_status(response.text)
        except requests.exceptions.RequestException as e:
            print(f"状态获取失败：{e}")
            self.status = {}
        return self.status

    def post_control(self, ip=None, **kwargs):
        """发送控制指令"""
        from . import ip as global_ip  # 延迟导入，避免循环依赖
        target_ip = ip or global_ip
        if not target_ip:
            print("❌ 未设置网关IP，请先设置 industrio.ip")
            return False
            
        url = target_ip
        valid_cmds = [f"{k}={v}" for k, v in kwargs.items() if k in CONTROLS]
        if not valid_cmds:
            print("无合法控制指令")
            return False
        cmd = ";".join(valid_cmds)
        try:
            requests.post(url, data=cmd, headers={"Content-Type": "text/plain"}, timeout=REQUEST_TIMEOUT)
            print(f"指令发送成功：{cmd}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"指令发送失败：{e}")
            return False

# 实例化客户端
default_client = GatewayClient()

# 导出post函数
def post(ip=None, **kwargs):
    return default_client.post_control(ip=ip, **kwargs)

# 传感器读取封装类
class GetSensor:
    def __init__(self, client):
        self.client = client

    def _get_value(self, sensor):
        """通用传感器读取逻辑"""
        if sensor not in SENSORS:
            print(f"未知传感器：{sensor}")
            return None
        self.client.get_status()
        return self.client.status.get(sensor)

# 为每个传感器动态生成方法
for sensor in SENSORS:
    setattr(GetSensor, sensor, lambda self, s=sensor: self._get_value(s))

get = GetSensor(default_client)

def blink(light_name, times, duration, ip=None):
    """
    控制灯具闪烁指定次数，每次间隔指定秒数
    :param light_name: 灯具名称（如"GLED"、"RLED"）
    :param times: 闪烁次数（int，≥1）
    :param duration: 每次亮/暗的秒数（float，>0）
    :param ip: 网关IP地址（可选，如未设置则使用 industrio.ip）
    :return: 是否成功（bool）
    """
    from . import ip as global_ip  # 延迟导入，避免循环依赖
    target_ip = ip or global_ip
    if not target_ip:
        print("❌ 未设置网关IP，请先设置 industrio.ip")
        return False
        
    # 参数校验
    if light_name not in CONTROLS:
        print(f"❌ 未知灯具：{light_name}")
        return False
    if not isinstance(times, int) or times < 1:
        print(f"❌ 闪烁次数必须≥1，当前为：{times}")
        return False
    if not isinstance(duration, (int, float)) or duration <= 0:
        print(f"❌ 每次秒数必须>0，当前为：{duration}")
        return False

    # 执行闪烁逻辑
    try:
        for _ in range(times):
            default_client.post_control(ip=target_ip, **{light_name: 1})  # 开灯
            time.sleep(duration)
            default_client.post_control(ip=target_ip, **{light_name: 0})  # 关灯
            time.sleep(duration)
        print(f"✅ {light_name} 已闪烁 {times} 次（每次{duration}秒）")
        return True
    except Exception as e:
        print(f"❌ 闪烁失败：{e}")
        return False

def ston(light_name, duration, ip=None):
    """
    控制灯具常亮指定秒数后自动关闭
    :param light_name: 灯具名称（如"GLED"、"RLED"）
    :param duration: 常亮秒数（float，>0）
    :param ip: 网关IP地址（可选，如未设置则使用 industrio.ip）
    :return: 是否成功（bool）
    """
    from . import ip as global_ip  # 延迟导入，避免循环依赖
    target_ip = ip or global_ip
    if not target_ip:
        print("❌ 未设置网关IP，请先设置 industrio.ip")
        return False
        
    # 参数校验
    if light_name not in CONTROLS:
        print(f"❌ 未知灯具：{light_name}")
        return False
    if not isinstance(duration, (int, float)) or duration <= 0:
        print(f"❌ 常亮秒数必须>0，当前为：{duration}")
        return False

    # 执行常亮逻辑
    try:
        default_client.post_control(ip=target_ip, **{light_name: 1})  # 开灯
        print(f"✅ {light_name} 开始常亮 {duration} 秒")
        time.sleep(duration)
        default_client.post_control(ip=target_ip, **{light_name: 0})  # 自动关灯
        print(f"✅ {light_name} 已关闭")
        return True
    except Exception as e:
        print(f"❌ 常亮失败：{e}")
        return False