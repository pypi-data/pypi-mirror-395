from datetime import datetime

from tornado.log import app_log

from solax_py_library.smart_scene.core.condition.base import BaseCondition
from solax_py_library.smart_scene.types.condition import (
    PriceConditionItemData,
    PriceConditionType,
    SmartSceneUnit,
    ConditionFunc,
    ConditionType,
)
from solax_py_library.utils.time_util import (
    get_left_timestamp,
    hour_to_today_timestamp,
)


class ElePriceCondition(BaseCondition):
    def __init__(self, update_value_function, **kwargs):
        super().__init__(update_value_function, **kwargs)
        self.buy = None

    def meet_func_price(
        self, function_value: ConditionFunc, data_value, current_data
    ) -> bool:
        """电价条件的判定"""
        app_log.info(f"meet_func_price: {current_data}, data_value: {data_value[0]}")
        return function_value.function()(current_data, data_value[0])

    def meet_func_highest_price(self, data_value, current_data) -> bool:
        value, unit = data_value
        price = self.value["price"]
        max_num = max(price.values())
        if unit == SmartSceneUnit.NUM:  # 比最高电价低X元
            base = round(max_num - value, 5)
        else:  # 比最高电价低X%
            if max_num < 0:
                base = round(max_num * (1 + value / 100), 5)
            else:
                base = round(max_num * (1 - value / 100), 5)
        app_log.info(f"meet_func_highest_price: {base}, data_value: {current_data}")
        if current_data <= base:
            return True
        else:
            return False

    def meet_func_lowest_price(self, data_value, current_data) -> bool:
        value, unit = data_value
        price = self.value["price"]
        min_num = min(price.values())
        if unit == SmartSceneUnit.NUM:  # 比最低电价高X元
            base = round(min_num + value, 5)
        else:  # 比最低电价高X%
            if min_num < 0:
                base = round(min_num * (1 - value / 100), 5)
            else:
                base = round(min_num * (1 + value / 100), 5)
        app_log.info(f"meet_func_lowest_price: {base}, data_value: {current_data}")
        if current_data >= base:
            return True
        else:
            return False

    def meet_func_highest_or_lowest_hours(
        self, data_value, current_timestamp, reverse
    ) -> bool:
        start_time = data_value[0]
        end_time = data_value[1]
        hours = data_value[2]
        price = self.value["price"]
        start_timestamp = hour_to_today_timestamp(int(start_time.split(":")[0])) * 1000
        end_timestamp = hour_to_today_timestamp(int(end_time.split(":")[0])) * 1000
        ret = []
        for timestamp_key, price_value in price.items():
            if (
                start_timestamp >= int(timestamp_key) + 15 * 60 * 1000
                or int(timestamp_key) >= end_timestamp
            ):
                continue
            ret.append([timestamp_key, price_value])
        sorted_price = sorted(ret, key=lambda x: x[1], reverse=reverse)
        top_sorted_price = sorted_price[: int(hours * 4)]
        if current_timestamp in [int(t) for (t, _) in top_sorted_price]:
            return True
        return False

    def meet_func(self, data: PriceConditionItemData, ctx):
        if not self.value or not self.value.get("price"):
            # 未获取到价格数据，直接返回
            return False
        child_data = data.childData
        child_type = data.childType
        data_value = child_data.data
        now_time = int(datetime.now().timestamp() * 1000)
        current_timestamp = get_left_timestamp(now_time)
        if str(current_timestamp) not in self.value["price"]:
            return False
        current_data = self.value["price"][str(current_timestamp)]
        if child_type == PriceConditionType.price:
            return self.meet_func_price(child_data.function, data_value, current_data)
        elif child_type == PriceConditionType.lowerPrice:
            return self.meet_func_highest_price(data_value, current_data)
        elif child_type == PriceConditionType.higherPrice:
            return self.meet_func_lowest_price(data_value, current_data)
        elif child_type == PriceConditionType.expensiveHours:
            return self.meet_func_highest_or_lowest_hours(
                data_value, current_timestamp, reverse=True
            )
        elif child_type == PriceConditionType.cheapestHours:
            return self.meet_func_highest_or_lowest_hours(
                data_value, current_timestamp, reverse=False
            )
        return False


class EleSellPriceCondition(ElePriceCondition):
    condition_type = ConditionType.sellingPrice

    def __init__(self, update_value_function, **kwargs):
        super().__init__(update_value_function, **kwargs)
        self.buy = False


class ElsBuyPriceCondition(ElePriceCondition):
    condition_type = ConditionType.buyingPrice

    def __init__(self, update_value_function, **kwargs):
        super().__init__(update_value_function, **kwargs)
        self.buy = True
