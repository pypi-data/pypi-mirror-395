# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-08-09 15:00:05
@LastEditTime: 2025-11-06 15:24:15
@LastEditors: HuangJianYi
@Description: 
"""
from seven_cloudapp_frame.models.enum import PageCountMode
from seven_cloudapp_frame.handlers.frame_base import *
from seven_cloudapp_frame.models.order_base_model import *
from seven_cloudapp_frame.models.stat_base_model import *


class HorseracelampListHandler(ClientBaseHandler):
    """
    :description: 获取跑马灯奖品列表
    """
    def get_async(self):
        """
        :description: 获取跑马灯奖品列表
        :param act_id: 活动标识
        :param module_id: 活动模块标识
        :param page_size: 条数
        :param is_search_module: 是否查询活动模块
        :return:
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        module_id = int(self.get_param("module_id", -1))
        page_size = int(self.get_param("page_size", 30))
        is_search_module = int(self.get_param("is_search_module", 0))
        if is_search_module == 0:
            is_search_module = False
        else:
            is_search_module = True

        if not app_id or not act_id:
            return self.response_json_success({"data": []})
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        condition = invoke_result_data.data["condition"] if invoke_result_data.data.__contains__("condition") else f"create_date>'{TimeHelper.add_hours_by_format_time(hour=-1)}'"
        params = invoke_result_data.data["params"] if invoke_result_data.data.__contains__("params") else []
        order_base_model = OrderBaseModel(context=self)
        horseracelamp_list = self.business_process_executed(order_base_model.get_horseracelamp_list(app_id, act_id, module_id, is_search_module, condition, params, page_size), ref_params={})
        return self.response_json_success(horseracelamp_list)


class SyncPayOrderHandler(ClientBaseHandler):
    """
    :description: 同步淘宝支付订单给用户加资产
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 同步淘宝支付订单给用户加资产
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        open_id = self.get_param("open_id")
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = int(self.get_param("module_id", 0))
        login_token = self.get_param("login_token")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        error_return = invoke_result_data.data.get("error_return", True)
        app_key, app_secret = self.get_app_key_secret()
        order_base_model = OrderBaseModel(context=self)
        invoke_result_data = order_base_model.sync_tao_pay_order(app_id=app_id,
                                                                 act_id=act_id,
                                                                 module_id=module_id,
                                                                 user_id=user_id,
                                                                 login_token=login_token,
                                                                 handler_name=self.__class__.__name__,
                                                                 request_code=self.request_code,
                                                                 asset_type=invoke_result_data.data.get('asset_type', 3),
                                                                 goods_id=invoke_result_data.data.get('goods_id', ""),
                                                                 sku_id=invoke_result_data.data.get('sku_id', ""),
                                                                 ascription_type=invoke_result_data.data.get('ascription_type', 1),
                                                                 app_key=app_key,
                                                                 app_secret=app_secret,
                                                                 is_log=invoke_result_data.data.get('is_log', False),
                                                                 check_user_nick=invoke_result_data.data.get('check_user_nick', True),
                                                                 continue_request_expire=invoke_result_data.data.get('continue_request_expire', 1))
        if invoke_result_data.success is False and error_return is True:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        ref_params["app_id"] = app_id
        ref_params["act_id"] = act_id
        ref_params["module_id"] = module_id
        ref_params["user_id"] = user_id
        ref_params["open_id"] = open_id

        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success is False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data)

    def business_process_executed(self, result_data, ref_params):
        """
        :description: 执行后事件
        :param result_data:result_data
        :param ref_params: 关联参数
        :return:
        :last_editors: HuangJianYi
        """
        stat_base_model = StatBaseModel(context=self)
        key_list_dict = {}
        key_list_dict["PayUserCount"] = 1
        key_list_dict["PayCount"] = result_data.data["pay_num"]
        key_list_dict["PayMoneyCount"] = result_data.data["pay_price"]
        stat_base_model.add_stat_list(ref_params["app_id"], ref_params["act_id"], ref_params["module_id"], ref_params["user_id"], ref_params["open_id"], key_list_dict)
        return result_data


class SyncShakeShopPayOrderHandler(ClientBaseHandler):
    """
    :description: 同步抖店订单给用户加资产
    """
    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :description: 同步抖店订单给用户加资产
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param open_id:open_id
        :param login_token:访问令牌
        :return
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        open_id = self.get_param("open_id")
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        is_log = invoke_result_data.data.get("is_log", False)
        asset_type = invoke_result_data.data.get("asset_type", 3)
        while_count = invoke_result_data.data.get("while_count", 1)
        ascription_type = invoke_result_data.data.get("ascription_type", 0)
        order_base_model = OrderBaseModel(context=self)
        invoke_result_data = order_base_model.sync_shake_shop_pay_order(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, is_log, asset_type=asset_type, while_count=while_count, ascription_type=ascription_type)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        ref_params = {}
        ref_params["app_id"] = app_id
        ref_params["act_id"] = act_id
        ref_params["module_id"] = module_id
        ref_params["user_id"] = user_id
        ref_params["open_id"] = open_id
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data)

    def business_process_executing(self):
        """
        :description: 执行前事件
        :return:
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        invoke_result_data.data = {"is_log":False}
        return invoke_result_data

    def business_process_executed(self, result_data, ref_params):
        """
        :description: 执行后事件
        :param result_data:result_data
        :param ref_params: 关联参数
        :return:
        :last_editors: HuangJianYi
        """
        UserInfoModel(context=self).update_table("pay_price=pay_price+%s,pay_num=pay_num+%s", "act_id=%s and user_id=%s", params=[result_data.data["pay_price"], result_data.data["pay_num"], ref_params["act_id"],ref_params["user_id"]])
        stat_base_model = StatBaseModel(context=self)
        key_list_dict = {}
        key_list_dict["PayUserCount"] = 1
        key_list_dict["PayCount"] = result_data.data["pay_num"]
        key_list_dict["PayMoneyCount"] = result_data.data["pay_price"]
        stat_base_model.add_stat_list(ref_params["app_id"], ref_params["act_id"], ref_params["module_id"], ref_params["user_id"], ref_params["open_id"], key_list_dict)
        return result_data


class PrizeOrderListHandler(ClientBaseHandler):
    """
    :description: 用户奖品订单列表
    """
    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :description: 用户奖品订单列表
        :param act_id：活动标识
        :param order_no：订单号
        :param user_code：用户标识
        :param user_open_id：open_id
        :param order_status：订单状态（-1未付款-2付款中0未发货1已发货2不予发货3已退款4交易成功）
        :param create_date_start：订单创建时间开始
        :param create_date_end：订单创建时间结束
        :param page_size：页大小
        :param page_index：页索引
        :param order_by：排序
        :param is_search_roster：是否查询订单关联中奖记录
        :param page_count_mode：分页模式(0-none 1-total 2-next)
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        user_open_id = self.get_param("user_open_id")
        order_status = self.get_param_int("order_status", -10)
        create_date_start = self.get_param("create_date_start")
        create_date_end = self.get_param("create_date_end")
        order_by = self.get_param("order_by","id desc")
        is_search_roster = self.get_param_int("is_search_roster", 0)
        is_search_roster = False if is_search_roster == 0 else True
        page_index = self.get_param_int("page_index", 0)
        page_size = self.get_param_int("page_size", 10)
        page_count_mode = self.get_param_int("page_count_mode", 1)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        page_count_mode = SevenHelper.get_enum_key(PageCountMode, page_count_mode)
        condition = invoke_result_data.data["condition"] if invoke_result_data.data.__contains__("condition") else ""
        params = invoke_result_data.data["params"] if invoke_result_data.data.__contains__("params") else []
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "id desc"
        field = invoke_result_data.data["field"] if invoke_result_data.data.__contains__("field") else "*"
        prize_roster_sub_table = invoke_result_data.data["prize_roster_sub_table"] if invoke_result_data.data.__contains__("prize_roster_sub_table") else None

        order_base_model = OrderBaseModel(context=self)
        page_list = order_base_model.get_prize_order_list(app_id, act_id, user_id, user_open_id, "", "", "", "", "", order_status, create_date_start, create_date_end, page_size, page_index, order_by, field, is_search_roster=is_search_roster, is_cache=True, condition=condition, params=params, prize_roster_sub_table=prize_roster_sub_table, page_count_mode=page_count_mode)
        ref_params = {}
        if page_count_mode == "total":
            total = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params=ref_params)
            return_info = PageInfo(page_index, page_size, total, page_list)
        elif page_count_mode == "next":
            is_next = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params=ref_params)
            return_info = WaterPageInfo(page_list, is_next)
        else:
            return_info = self.business_process_executed(page_list, ref_params=ref_params)
        return self.response_json_success(return_info)


class PrizeRosterListHandler(ClientBaseHandler):
    """
    :description: 用户中奖记录列表
    """
    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :description: 用户中奖记录列表
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_code：用户标识
        :param order_no：订单号
        :param goods_type：物品类型（1虚拟2实物）
        :param prize_type：奖品类型(1现货2优惠券3红包4参与奖5预售)
        :param logistics_status：物流状态（0未发货1已发货2不予发货）
        :param prize_status：奖品状态（0未下单（未领取）1已下单（已领取）2已回购10已隐藏（删除）11无需发货）
        :param pay_status：支付状态(0未支付1已支付2已退款3处理中)
        :param page_size：页大小
        :param page_index：页索引
        :param page_count_mode：分页模式(0-none 1-total 2-next)
        :return PageInfo
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        open_id = self.get_param("open_id")
        act_id = self.get_act_id()
        module_id = int(self.get_param("module_id", 0))
        user_id = self.get_user_id()
        order_no = self.get_param("order_no")
        goods_type = int(self.get_param("goods_type", -1))
        prize_type = int(self.get_param("prize_type", -1))
        logistics_status = int(self.get_param("logistics_status", -1))
        prize_status = int(self.get_param("prize_status", -1))
        pay_status = int(self.get_param("pay_status", -1))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))
        page_count_mode = self.get_param_int("page_count_mode", 1)

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        page_count_mode = SevenHelper.get_enum_key(PageCountMode,page_count_mode)
        ref_params = {}
        order_base_model = OrderBaseModel(context=self)
        page_list = order_base_model.get_prize_roster_list(app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_id, open_id=open_id, order_no=order_no, goods_type=goods_type, prize_type=prize_type, logistics_status=logistics_status, prize_status=prize_status, pay_status=pay_status, page_size=page_size, page_index=page_index, page_count_mode=page_count_mode)
        if page_count_mode == "total":
            if len(page_list) > 0:
                total = page_list[1]
                page_list = self.business_process_executed(page_list[0], ref_params=ref_params)
            else:
                total = 0
                page_list = []
            return_info = PageInfo(page_index, page_size, total, page_list)
        elif page_count_mode == "next":
            if len(page_list) > 0:
                is_next = page_list[1]
                page_list = self.business_process_executed(page_list[0], ref_params=ref_params)
            else:
                is_next = False
                page_list = []
            return_info = WaterPageInfo(page_list, is_next)
        else:
            return_info = self.business_process_executed(page_list, ref_params=ref_params)
        return self.response_json_success(return_info)


class SubmitSkuHandler(ClientBaseHandler):
    """
    :description: 中奖记录选择SKU提交
    """
    @filter_check_params("user_prize_id,sku_id")
    def get_async(self):
        """
        :description: 提交SKU
        :param user_prize_id：用户中奖信息标识
        :param sku_name：sku属性名称
        :param sku_id：sku_id
        :return 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        open_id = self.get_param("open_id")
        user_prize_id = int(self.get_param("user_prize_id"))
        sku_name = self.get_param("sku_name")
        sku_id = self.get_param("sku_id")

        prize_roster_model = PrizeRosterModel(context=self).set_sub_table(app_id)
        prize_roster = prize_roster_model.get_entity_by_id(user_prize_id)
        if not prize_roster or prize_roster.open_id != open_id or SafeHelper.authenticat_app_id(prize_roster.app_id, app_id) == False:
            return self.response_json_error("no_user_prize", "对不起，找不到该奖品")
        if prize_roster.is_sku > 0:
            prize_roster.sku_id = sku_id
            prize_roster.sku_name = sku_name
            goods_code_list = self.json_loads(prize_roster.goods_code_list)
            goods_codes = [i for i in goods_code_list if str(i["sku_id"]) == sku_id]
            if goods_codes and len(goods_codes) > 0 and ("goods_code" in goods_codes[0].keys()):
                prize_roster.goods_code = goods_codes[0]["goods_code"]
        prize_roster_model.update_entity(prize_roster, "sku_id,sku_name,goods_code")

        return self.response_json_success()


class SelectPrizeOrderHandler(ClientBaseHandler):
    """
    :description: 中奖记录下单
    """
    @filter_check_params("login_token,real_name,telephone", check_user_code=True)
    def get_async(self):
        """
        :param act_id：活动标识
        :param user_code：用户标识
        :param login_token:用户访问令牌
        :param prize_ids:用户奖品id串，逗号分隔（为空则将所有未下单的奖品进行下单）
        :param real_name:用户名
        :param telephone:电话
        :param province:省
        :param city:市
        :param county:区县
        :param street:街道
        :param address:地址
        :return
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        login_token = self.get_param("login_token")
        prize_ids = self.get_param("prize_ids")
        real_name = self.get_param("real_name")
        telephone = self.get_param("telephone")
        province = self.get_param("province")
        city = self.get_param("city")
        county = self.get_param("county")
        street = self.get_param("street")
        address = self.get_param("address")

        order_base_model = OrderBaseModel(context=self)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        prize_ids = invoke_result_data.data["prize_ids"] if invoke_result_data.data.__contains__("prize_ids") else prize_ids
        invoke_result_data = order_base_model.select_prize_order(app_id, act_id, user_id, login_token, prize_ids, real_name, telephone, province, city, county, street,address)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        else:
            return self.response_json_success(self.business_process_executed(invoke_result_data, ref_params={}))


class UpdateOrderAddressHandler(ClientBaseHandler):
    """
    :description: 修改订单地址
    """
    @filter_check_params("main_order_no,real_name,telephone", check_user_code=True)
    def get_async(self):
        """
        :description: 修改订单地址
        :param user_id: 用户标识
        :param main_order_no: 小程序订单号
        :param real_name:用户名
        :param telephone:电话
        :param province:省
        :param city:市
        :param county:区县
        :param street:街道
        :param address:地址
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        order_no = self.get_param("main_order_no")
        real_name = self.get_param("real_name")
        telephone = self.get_param("telephone")
        province = self.get_param("province")
        city = self.get_param("city")
        county = self.get_param("county")
        street = self.get_param("street")
        address = self.get_param("address")

        if not order_no.isdigit():
            return self.response_json_error("error", "对不起，订单号格式不正确")
        try:
            frame_base_model = FrameBaseModel(context=self)
            invoke_result_data = frame_base_model.business_process_executing(app_id, act_id, 0, user_id, '', self.__class__.__name__, False, False, 1)
            if invoke_result_data.success is False:
                return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
            prize_order_model = PrizeOrderModel(context=self)
            prize_order_dict = prize_order_model.get_dict("order_no=%s", field='id,order_status,act_id,module_id,user_id,sync_status', params=[order_no])
            if not prize_order_dict:
                return self.response_json_error("error", "对不起，订单不存在")
            if prize_order_dict['act_id'] != act_id or prize_order_dict['user_id'] != user_id:
                return self.response_json_error("error", "非法操作")
            if prize_order_dict['order_status'] == 1:
                return self.response_json_error("error", "已发货，不允许修改")
            invoke_result_data = self.business_process_executed(prize_order_dict, {})
            if invoke_result_data.success is False:
                return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
            sync_status = 3 if prize_order_dict['sync_status'] == 1 else 0  # 如果是已推送，则设为3走修改地址，否则还是走创单
            real_name = frame_base_model.sensitive_encrypt(real_name) if real_name else ''
            telephone = frame_base_model.sensitive_encrypt(telephone) if telephone else ''
            address = frame_base_model.sensitive_encrypt(address) if address else ''

            result = prize_order_model.update_table('real_name=%s,telephone=%s,province=%s,city=%s,county=%s,street=%s,address=%s,sync_status=%s,sync_count=0,sync_result=%s,modify_date=%s',
                                                    "order_no=%s",
                                                    params=[real_name, telephone, province, city, county, street, address, sync_status, '', TimeHelper.get_now_format_time(), order_no])
            if result is False:
                return self.response_json_error("error", "修改失败")
            prize_order_model.delete_dependency_key(DependencyKey.prize_order_list(act_id, user_id))
            return self.response_json_success("修改成功")
        except Exception as ex:
            self.logging_link_error(f"【修改订单地址异常】{traceback.format_exc()}")
            return self.response_json_error("exception", "系统繁忙,请稍后再试")
        finally:
            frame_base_model.business_process_executed()
