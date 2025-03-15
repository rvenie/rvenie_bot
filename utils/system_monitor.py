import psutil
import platform
from datetime import datetime

def get_size(bytes, suffix="B"):
    """Преобразование байтов в человекочитаемый формат"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_system_info():
    """Получение информации о системе"""
    system_info = {}
    
    # Информация о системе
    system_info["system"] = platform.system()
    system_info["node"] = platform.node()
    system_info["release"] = platform.release()
    
    # Информация о CPU
    cpu_info = {}
    cpu_info["physical_cores"] = psutil.cpu_count(logical=False)
    cpu_info["total_cores"] = psutil.cpu_count(logical=True)
    cpu_info["usage_percent"] = psutil.cpu_percent(interval=1)
    system_info["cpu"] = cpu_info
    
    # Информация о RAM
    memory = psutil.virtual_memory()
    ram_info = {}
    ram_info["total"] = get_size(memory.total)
    ram_info["available"] = get_size(memory.available)
    ram_info["used"] = get_size(memory.used)
    ram_info["percent"] = memory.percent
    system_info["ram"] = ram_info
    
    # Информация о диске
    disk_info = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            disk_info[partition.device] = {
                "mountpoint": partition.mountpoint,
                "total": get_size(partition_usage.total),
                "used": get_size(partition_usage.used),
                "free": get_size(partition_usage.free),
                "percent": partition_usage.percent
            }
        except Exception:
            pass
    system_info["disk"] = disk_info
    
    # Информация о сети
    net_info = {}
    net_io = psutil.net_io_counters()
    net_info["bytes_sent"] = get_size(net_io.bytes_sent)
    net_info["bytes_recv"] = get_size(net_io.bytes_recv)
    system_info["network"] = net_info
    
    return system_info

def format_system_info(system_info):
    """Форматирование информации о системе в читаемый текст"""
    result = "📊 Информация о сервере:\n\n"
    
    # Общая информация
    result += f"🖥️ Система: {system_info['system']} {system_info['release']}\n"
    result += f"🏠 Хост: {system_info['node']}\n\n"
    
    # CPU
    cpu = system_info['cpu']
    result += f"🔄 CPU:\n"
    result += f"  • Физические ядра: {cpu['physical_cores']}\n"
    result += f"  • Логические ядра: {cpu['total_cores']}\n"
    result += f"  • Загрузка: {cpu['usage_percent']}%\n\n"
    
    # RAM
    ram = system_info['ram']
    result += f"🧠 RAM:\n"
    result += f"  • Всего: {ram['total']}\n"
    result += f"  • Доступно: {ram['available']}\n"
    result += f"  • Использовано: {ram['used']} ({ram['percent']}%)\n\n"
    
    # Диск
    result += f"💾 Диск:\n"
    for device, disk in system_info['disk'].items():
        result += f"  • {device} ({disk['mountpoint']}):\n"
        result += f"    - Всего: {disk['total']}\n"
        result += f"    - Свободно: {disk['free']}\n"
        result += f"    - Использовано: {disk['used']} ({disk['percent']}%)\n"
    result += "\n"
    
    # Сеть
    net = system_info['network']
    result += f"🌐 Сеть:\n"
    result += f"  • Отправлено: {net['bytes_sent']}\n"
    result += f"  • Получено: {net['bytes_recv']}\n"
    
    return result
