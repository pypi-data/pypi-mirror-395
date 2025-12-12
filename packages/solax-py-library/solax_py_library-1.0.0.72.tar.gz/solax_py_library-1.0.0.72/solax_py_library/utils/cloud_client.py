import json
import ssl
import traceback
from datetime import datetime
from itertools import chain

import requests
from requests.adapters import HTTPAdapter

from tornado.log import app_log


class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)


class CloudClient:
    def __init__(self, base_url, ciphers=None):
        self.base_url = base_url
        self.ciphers = (
            ciphers
            if ciphers
            else "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384"
        )

    def get_context(self):
        context = ssl.create_default_context()
        context.set_ciphers(self.ciphers)
        return context

    def request(self, url, body=None, headers=None):
        # 创建异步请求
        base_headers = {"Content-Type": "application/json"}
        if headers:
            base_headers.update(headers)

        session = requests.Session()
        session.mount("https://", SSLAdapter(ssl_context=self.get_context()))

        response = session.post(url, json=body, headers=headers, timeout=5)
        if response.status_code != 200:
            raise ValueError(f"访问{url}接口失败")
        return json.loads(response.content.decode("utf-8"))

    def get_token(self, ems_sn, sn_secret):
        token_url = self.base_url + "/device/token/getByRegistrationSn"
        try:
            response_data = self.request(
                url=token_url,
                body={
                    "registrationSn": ems_sn,
                    "snSecret": sn_secret,
                },
            )
            app_log.info(f"获取token结果 {response_data}")
            if response_data.get("result"):
                return response_data["result"]
        except Exception as e:
            app_log.info(f"访问token接口失败: {str(e)}")

    def get_weather_data_from_cloud(self, ems_sn, token):
        """获取未来24小时天气数据"""
        try:
            weather_url = self.base_url + "/ess/web/v1/powerStation/station/solcast/get"
            headers = {"token": token, "Content-Type": "application/json"}
            post_dict = {"registerNo": ems_sn, "day": 1}
            response_data = self.request(
                url=weather_url,
                headers=headers,
                body=post_dict,
            )
            if response_data.get("result") is None:
                app_log.info(f"获取天气数据失败 返回数据 {response_data}")
                return False
            weather_info = {
                "timeList": [],
                "irradiance": {"valueList": []},
                "temperature": {"valueList": []},
            }
            for info in response_data["result"]:
                weather_info["timeList"].append(info["localTime"])
                weather_info["irradiance"]["valueList"].append(float(info["ghi"]))
                weather_info["temperature"]["valueList"].append(float(info["air_temp"]))
            data_length = len(weather_info["irradiance"]["valueList"])
            if weather_info["timeList"] == []:
                weather_info = {}
            else:
                weather_info["irradiance"]["maxValue"] = max(
                    weather_info["irradiance"]["valueList"]
                )
                weather_info["irradiance"]["avgValue"] = round(
                    sum(weather_info["irradiance"]["valueList"]) / data_length, 3
                )
                weather_info["irradiance"]["minValue"] = min(
                    weather_info["irradiance"]["valueList"]
                )

                weather_info["temperature"]["maxValue"] = max(
                    weather_info["temperature"]["valueList"]
                )
                weather_info["temperature"]["avgValue"] = round(
                    sum(weather_info["temperature"]["valueList"]) / data_length, 3
                )
                weather_info["temperature"]["minValue"] = min(
                    weather_info["temperature"]["valueList"]
                )
            app_log.info("获取天气数据成功")
            return weather_info
        except Exception:
            app_log.info(f"获取天气数据失败 异常 {traceback.format_exc()}")
            return False

    def get_electrovalence_data_from_cloud(self, ems_sn, token):
        try:
            price_url = self.base_url + "/powerStation/station/getCurrentElectrovalence"
            response_data = self.request(
                url=price_url,
                body={"registerNo": ems_sn},
                headers={"token": token},
            )
            if response_data.get("result") is None:
                app_log.info(f"获取电价数据失败 返回数据 {response_data}")
                return False
            if ele_price_info := self.parse_electrovalence_data(
                response_data["result"]
            ):
                app_log.info("获取电价数据成功")
                return ele_price_info
            return False
        except Exception:
            app_log.info(f"获取电价数据失败 异常 {traceback.format_exc()}")
            return False

    def parse_electrovalence_data(self, ele_price_data, now_time=None):
        today = datetime.strftime(
            datetime.now() if now_time is None else now_time, "%Y-%m-%d %H:%M:%S"
        )
        ele_price_info = {
            "buy": {},
            "sell": {},
            "date": today,
        }
        currency_code = ele_price_data["currencyCode"]
        transfer_map = {
            "GBP": (100, "p"),
            "EUR": (100, "c"),
            "SEK": (100, "öre"),
        }
        unit = ele_price_data["unit"]
        rate = 1
        if currency_code in transfer_map:
            rate, unit = transfer_map[currency_code]
        ele_price_info["ele_unit"] = f"{unit}/kWh"
        for detail_info in chain(
            ele_price_data["list"],
            ele_price_data.get("tomorrow", []),
        ):
            start_timestamp = detail_info["startTimeStamp"]
            end_timestamp = detail_info["endTimeStamp"]
            if start_timestamp is None or end_timestamp is None:
                continue
            # 处理欧分的情况
            buy_price = (
                round(detail_info["buyPrice"] * rate, 5)
                if detail_info["buyPrice"]
                else None
            )
            sale_price = (
                round(detail_info["salePrice"] * rate, 5)
                if detail_info["salePrice"]
                else None
            )
            while start_timestamp < end_timestamp:  # 每十五分钟存一段
                if buy_price:
                    ele_price_info["buy"][start_timestamp] = buy_price
                if sale_price:
                    ele_price_info["sell"][start_timestamp] = sale_price
                start_timestamp += 15 * 60 * 1000
        return ele_price_info
