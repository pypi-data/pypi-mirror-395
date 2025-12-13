
from fastapi.responses import JSONResponse
from typing import Dict, List, Tuple, Any, Optional, ClassVar
from datetime import datetime, timedelta
from mctech_actuator import get_health_manager, MetricIndicator


async def _metric_endpoint():
    results = {}
    for k, v in rpc_clients.items():
        results[k] = v.__json__()
    return JSONResponse(results)

get_health_manager().add_metric(MetricIndicator(
    # 相对于/actuator/metrics的路径，必须以'/'开头
    path='/rpc-clients',
    endpoint=_metric_endpoint
))

rpc_clients: Dict[str, "ApiInvokeStat"] = {}

STAT_MAX_REMAIN = 48  # 48小时
ONE_HOUR = 3600 * 1000


class ApiInvokeStat:
    def __init__(self):
        self.total = InvokeStat()
        self.clients: Dict[str, DetailInvokeStat] = {}
        self._LAST_INVOKE = None

    def record(self, client_name: str, invoke_info: "InvokeInfo"):
        info = InvokeInfo(
            start=invoke_info.start,
            end=invoke_info.end,
            success=invoke_info.error is not None and invoke_info.status is not None and invoke_info.status < 400
        )

        self._LAST_INVOKE = info

        client_invoke_stat = self.clients.get(client_name)
        if client_invoke_stat is None:
            client_invoke_stat = DetailInvokeStat()
            self.clients[client_name] = client_invoke_stat
        client_invoke_stat.record(info)
        self.total.increment()

    def __json__(self):
        clients = {}
        for k, v in self.clients.items():
            clients[k] = v.__json__()
        return {
            'total': self.total.__json__(),
            'clients': clients
        }


class InvokeStat:
    current: ClassVar[datetime]

    def __init__(self):
        self._CURRENT = -1
        # 最近 {STAT_MAX_REMAIN} 小时调用统计分布
        # @type {Tuple[datetime, int][]}
        self.stats: List[Tuple[datetime, int]] = []

    def increment(self):
        if self._CURRENT != InvokeStat.current:
            # 清理历史统计信息

            # 新增加一个统计段
            self.stats.insert(0, tuple[datetime, int]([InvokeStat.current, 0]))
            self._CURRENT = InvokeStat.current
            # 清除时间最远的段，最多保留48条数据
            # 不是48小时，如果是隔两小时调一次，则保留48条数据对应着96小时
            # 在获取统计信息时会清理掉不在48小时内的数据
            if len(self.stats) > STAT_MAX_REMAIN > 0:
                self.stats = self.stats[0:STAT_MAX_REMAIN]
        # 计数
        current_stat = self.stats[0]
        self.stats[0] = tuple[datetime, int]([current_stat[0], current_stat[1] + 1])

    def __json__(self) -> Any:
        now = datetime.now()
        json = []
        self.stats = []
        for stat in self.stats:
            hours = int((now - stat[0]).total_seconds() / ONE_HOUR)
            if hours >= STAT_MAX_REMAIN:
                continue

            padding_count = len(json) - hours
            if padding_count > 0:
                # 扩展数组成员个数，确保json[hours] 不会出错
                json.append(None)
            json[hours] = stat[1]
            self.stats.append(stat)
        return json


# 当前小时
InvokeStat.current = datetime.min


class InvokeInfo:
    start: datetime
    end: datetime
    duration: timedelta
    success: bool
    status: Optional[int]
    error: Optional[Exception]

    def __init__(self, start: datetime, end: datetime, success: bool,
                 status: Optional[int] = None, error: Optional[Exception] = None):
        self.start = start
        self.end = end
        self.duration = end - start
        self.status = status
        self.success = success
        self.error = error

    def __json__(self):
        return {
            'start': self.start.timestamp(),
            'end': self.end.timestamp(),
            'duration': self.duration.total_seconds(),
            'success': self.success,
            'status': self.status,
            'error': str(self.error) if self.error else None
        }


class DetailInvokeStat(InvokeStat):
    def __init__(self):
        super().__init__()
        self.last: Optional[InvokeInfo] = None

    def record(self, info: InvokeInfo):
        if (info.start - InvokeStat.current).total_seconds() >= ONE_HOUR:
            # 设置为新的统计区间
            # setMinutes方法返回调整过的日期的毫秒表示。在 ECMAScript 标准化之前，该方法什么都不返回。
            InvokeStat.current = info.start.replace(hour=0, minute=0, second=0, microsecond=0)

        self.increment()
        self.last = info

    def __json__(self):
        return {
            'stat': super().__json__(),
            'last': self.last.__json__() if self.last else None
        }


def add_rpc_client_metric(api_key: str, client_name: str, invoke_info: InvokeInfo):
    api_invoke_stat = rpc_clients[api_key]
    if not api_invoke_stat:
        api_invoke_stat = ApiInvokeStat()
        rpc_clients[api_key] = api_invoke_stat

    api_invoke_stat.record(client_name, invoke_info)
