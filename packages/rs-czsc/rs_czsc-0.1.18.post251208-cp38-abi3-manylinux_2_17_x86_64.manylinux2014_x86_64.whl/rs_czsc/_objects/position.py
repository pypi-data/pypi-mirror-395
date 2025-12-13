import pandas as pd
from rs_czsc._rs_czsc import Position as PyPosition
from rs_czsc._utils._df_convert import arrow_bytes_to_pd_df


class Position:
    """Position wrapper that provides API compatibility with Python version

    This wrapper handles the conversion from Rust's Position to provide the expected API.
    """

    def __init__(self, *args, **kwargs):
        self._inner = PyPosition(*args, **kwargs)

    @property
    def name(self):
        return self._inner.name

    @property
    def symbol(self):
        return self._inner.symbol

    @property
    def interval(self):
        return self._inner.interval

    @property
    def pos(self):
        return self._inner.pos

    @property
    def pos_changed(self):
        return self._inner.pos_changed

    @property
    def opens(self):
        return self._inner.opens

    @property
    def exits(self):
        return self._inner.exits

    @property
    def unique_signals(self):
        return self._inner.unique_signals

    @property
    def pairs(self):
        """获取交易对数据，返回DataFrame格式

        兼容原Python API，返回可直接用于pandas.DataFrame构造的数据
        """
        try:
            # 获取原始pairs数据
            raw_pairs = None

            # 如果Rust实现有字节数据方法，使用arrow转换
            if hasattr(self._inner, 'pairs') and callable(self._inner.pairs):
                bytes_data = self._inner.pairs()
                if isinstance(bytes_data, bytes):
                    raw_pairs = arrow_bytes_to_pd_df(bytes_data)

            # 如果有getter属性，直接返回
            if raw_pairs is None and hasattr(self._inner, 'pairs') and not callable(self._inner.pairs):
                raw_pairs = self._inner.pairs

            if raw_pairs is None:
                return []

            # 处理时间字段格式兼容性
            # CZSC的PairsPerformance期望时间字段是datetime对象，而不是字符串
            processed_pairs = []
            for pair in raw_pairs:
                processed_pair = dict(pair)  # 复制字典

                # 转换时间字段从字符串到datetime对象
                time_fields = ['开仓时间', '平仓时间']
                for field in time_fields:
                    if field in processed_pair and isinstance(processed_pair[field], str):
                        try:
                            import datetime
                            processed_pair[field] = datetime.datetime.strptime(
                                processed_pair[field], '%Y-%m-%d %H:%M:%S'
                            )
                        except ValueError:
                            # 如果解析失败，保持原值
                            pass

                processed_pairs.append(processed_pair)

            return processed_pairs
        except Exception:
            # 出错时返回空列表保持兼容性
            return []

    @property
    def holds(self):
        """获取持仓历史数据，兼容原Python版本格式

        返回列表格式，每个元素是包含dt, pos, price字段的字典
        """
        try:
            # Rust实现的holds()方法返回的是Arrow格式的字节数据
            if hasattr(self._inner, 'holds') and callable(self._inner.holds):
                bytes_data = self._inner.holds()
                if isinstance(bytes_data, bytes):
                    # 转换Arrow字节数据为DataFrame
                    df = arrow_bytes_to_pd_df(bytes_data)
                    # 转换为字典列表
                    return df.to_dict('records')

            # 如果有属性访问方式，直接返回
            if hasattr(self._inner, 'holds') and not callable(self._inner.holds):
                raw_holds = self._inner.holds
                # 处理n1b字段的兼容性：将None值替换为0.0
                processed_holds = []
                for hold in raw_holds:
                    processed_hold = dict(hold)
                    if 'n1b' in processed_hold and processed_hold['n1b'] is None:
                        processed_hold['n1b'] = 0.0
                    processed_holds.append(processed_hold)
                return processed_holds

            return []
        except Exception:
            # 出错时返回空列表保持兼容性
            return []

    def update(self, *args, **kwargs):
        """更新Position状态

        支持多种调用方式：
        1. update(signals_dict) - 字典格式，Rust层会自动解析
        2. update(signals_list, lite_bar) - Signal列表和LiteBar对象

        字典格式示例:
            s = {
                'symbol': 'BTCUSDT',
                'dt': Timestamp('2025-09-01 00:00:00'),
                'id': 1,
                'close': 100.0,
                '60分钟_D1BOLL20S20MO5_BS辅助V230212': '看多',
                '60分钟_D1_涨跌停V230331': '正常',
            }

        Rust层已经实现了完整的字典解析逻辑，包括：
        - 提取dt, id, close字段构造LiteBar
        - 提取信号字段构造Signal集合
        - 执行update逻辑
        """
        return self._inner.update(*args, **kwargs)

    def dump(self, with_data=True):
        """导出Position数据为字典"""
        return self._inner.dump(with_data)

    @classmethod
    def load(cls, data):
        """从字典数据加载Position"""
        # 如果data是字符串，尝试解析为JSON
        if isinstance(data, str):
            import json
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                raise ValueError(f"无法解析Position JSON数据: {e}")

        # 确保data是字典类型
        if not isinstance(data, dict):
            raise TypeError(f"Position.load expects dict or JSON string, got {type(data)}")

        inner = PyPosition.load(data)
        wrapper = cls.__new__(cls)
        wrapper._inner = inner
        return wrapper

    def __getattr__(self, name):
        """代理到内部实现，处理其他属性和方法"""
        # 避免在pickle/deepcopy过程中的递归
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return getattr(self._inner, name)

    def __reduce__(self):
        """支持pickle序列化"""
        # 使用dump/load方法来序列化Position
        data = self._inner.dump(with_data=True)
        return (self.__class__.load, (data,))

    def __repr__(self):
        return f"Position(name='{self.name}', symbol='{self.symbol}', opens={len(self.opens)}, exits={len(self.exits)})"