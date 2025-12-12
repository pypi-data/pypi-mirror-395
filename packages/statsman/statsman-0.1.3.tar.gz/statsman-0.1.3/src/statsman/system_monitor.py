import psutil
import time
from dataclasses import dataclass
from typing import List, Dict, Any
from collections import deque


@dataclass
class CPUInfo:
    percent: float
    percent_per_core: List[float]
    frequency: float
    load_avg: List[float]
    count: int
    count_logical: int


@dataclass
class MemoryInfo:
    total: int
    available: int
    used: int
    percent: float
    swap_total: int
    swap_used: int
    swap_percent: float


@dataclass
class DiskInfo:
    total: int
    used: int
    free: int
    percent: float
    read_bytes: int
    write_bytes: int
    read_count: int
    write_count: int


@dataclass
class NetworkInfo:
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int
    interfaces: Dict[str, Dict[str, int]]


@dataclass
class ProcessInfo:
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_rss: int
    status: str
    cmdline: List[str]


class SystemMonitor:
    def __init__(self, history_size: int = 60):
        self.history_size = history_size
        self.cpu_history = deque(maxlen=history_size)
        self.memory_history = deque(maxlen=history_size)
        self.network_history = deque(maxlen=history_size)
        self._last_net_io = psutil.net_io_counters()
        self._last_disk_io = psutil.disk_io_counters()
        self._last_time = time.time()
    
    def get_cpu_info(self) -> CPUInfo:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_percent_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
        
        try:
            freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0.0
        except (AttributeError, OSError):
            freq = 0.0
        
        try:
            load_avg = list(psutil.getloadavg())
        except (AttributeError, OSError):
            load_avg = [0.0, 0.0, 0.0]
        
        return CPUInfo(
            percent=cpu_percent,
            percent_per_core=cpu_percent_per_core,
            frequency=freq,
            load_avg=load_avg,
            count=psutil.cpu_count(logical=False) or 0,
            count_logical=psutil.cpu_count(logical=True) or 0,
        )
    
    def get_memory_info(self) -> MemoryInfo:
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return MemoryInfo(
            total=memory.total,
            available=memory.available,
            used=memory.used,
            percent=memory.percent,
            swap_total=swap.total,
            swap_used=swap.used,
            swap_percent=swap.percent,
        )
    
    def get_disk_info(self) -> DiskInfo:
        disk_usage = psutil.disk_usage('/')
        
        current_disk_io = psutil.disk_io_counters()
        if current_disk_io and self._last_disk_io:
            time_delta = time.time() - self._last_time
            read_bytes = max(0, current_disk_io.read_bytes - self._last_disk_io.read_bytes)
            write_bytes = max(0, current_disk_io.write_bytes - self._last_disk_io.write_bytes)
            read_count = max(0, current_disk_io.read_count - self._last_disk_io.read_count)
            write_count = max(0, current_disk_io.write_count - self._last_disk_io.write_count)
        else:
            read_bytes = write_bytes = read_count = write_count = 0
        
        self._last_disk_io = current_disk_io
        
        return DiskInfo(
            total=disk_usage.total,
            used=disk_usage.used,
            free=disk_usage.free,
            percent=disk_usage.percent,
            read_bytes=read_bytes,
            write_bytes=write_bytes,
            read_count=read_count,
            write_count=write_count,
        )
    
    def get_network_info(self) -> NetworkInfo:
        current_net_io = psutil.net_io_counters()
        
        if current_net_io and self._last_net_io:
            bytes_sent = max(0, current_net_io.bytes_sent - self._last_net_io.bytes_sent)
            bytes_recv = max(0, current_net_io.bytes_recv - self._last_net_io.bytes_recv)
            packets_sent = max(0, current_net_io.packets_sent - self._last_net_io.packets_sent)
            packets_recv = max(0, current_net_io.packets_recv - self._last_net_io.packets_recv)
        else:
            bytes_sent = bytes_recv = packets_sent = packets_recv = 0
        
        self._last_net_io = current_net_io
        
        interfaces = {}
        try:
            net_if_addrs = psutil.net_if_addrs()
            net_io_stats = psutil.net_io_counters(pernic=True)
            
            for interface_name in net_if_addrs:
                if interface_name in net_io_stats:
                    interfaces[interface_name] = {
                        'bytes_sent': net_io_stats[interface_name].bytes_sent,
                        'bytes_recv': net_io_stats[interface_name].bytes_recv,
                        'packets_sent': net_io_stats[interface_name].packets_sent,
                        'packets_recv': net_io_stats[interface_name].packets_recv,
                    }
        except (OSError, AttributeError):
            pass
        
        return NetworkInfo(
            bytes_sent=bytes_sent,
            bytes_recv=bytes_recv,
            packets_sent=packets_sent,
            packets_recv=packets_recv,
            interfaces=interfaces,
        )
    
    def get_process_info(self, limit: int = 10) -> List[ProcessInfo]:
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 
                                        'memory_info', 'status', 'cmdline']):
            try:
                pinfo = proc.info
                if pinfo['cpu_percent'] is None:
                    pinfo['cpu_percent'] = 0.0
                if pinfo['memory_percent'] is None:
                    pinfo['memory_percent'] = 0.0
                
                processes.append(ProcessInfo(
                    pid=pinfo['pid'],
                    name=pinfo['name'] or 'Unknown',
                    cpu_percent=pinfo['cpu_percent'],
                    memory_percent=pinfo['memory_percent'],
                    memory_rss=pinfo['memory_info'].rss if pinfo['memory_info'] else 0,
                    status=pinfo['status'] or 'Unknown',
                    cmdline=pinfo['cmdline'] or [],
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        processes.sort(key=lambda p: p.cpu_percent, reverse=True)
        return processes[:limit]
    
    def update_history(self) -> None:
        cpu_info = self.get_cpu_info()
        memory_info = self.get_memory_info()
        network_info = self.get_network_info()
        
        self.cpu_history.append(cpu_info.percent)
        self.memory_history.append(memory_info.percent)
        self.network_history.append({
            'bytes_sent': network_info.bytes_sent,
            'bytes_recv': network_info.bytes_recv,
        })
        
        self._last_time = time.time()
    
    def get_cpu_history(self) -> List[float]:
        return list(self.cpu_history)
    
    def get_memory_history(self) -> List[float]:
        return list(self.memory_history)
    
    def get_network_history(self) -> List[Dict[str, int]]:
        return list(self.network_history)
