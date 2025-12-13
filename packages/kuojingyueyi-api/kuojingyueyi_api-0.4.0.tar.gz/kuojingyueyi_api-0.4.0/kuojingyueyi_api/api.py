"""
阔景版权服务平台

网址：https://ds.kuojingyueyi.cn/app/index

注：上传文件需要 requests-toolbelt
"""

import os
import json
import time
import hashlib
import random
from pathlib import Path
from pprint import pprint as pp

import requests

from requests import Response
# from requests_toolbelt import MultipartEncoder
from urllib.parse import urlparse, unquote

from .utils import need_login, BaseClient
from .exception import LoginError, NeedAccessTokenException

HEADERS_JSON = {
    'authorization': '',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'accept-language': 'zh-CN,zh;q=0.9'
}


class KuoJingYueYi(BaseClient):

    def __init__(self, base_url='https://ds.kuojingyueyi.cn', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url
        self.set_headers(HEADERS_JSON)
        self.data = {}
        self._access_token = None

    def set_access_token(self, access_token):
        """
        设置用户授权
        """
        HEADERS_JSON['authorization'] = access_token
        self.set_headers(HEADERS_JSON)
        # 我们获取消息数量，检查是否已经登录成功

        self._access_token = access_token

    def need_access_token(self):
        """
        检查是否已登录，我们还是只简单检查有没有 access_token
        """
        # self.get_count_message()
        if self._access_token is None:
            raise NeedAccessTokenException()

    def get_response_data(self, resp):
        """
        解析接口返回的数据
        """
        try:
            self.data = resp.json()
        except Exception as e:
            return {
                "code": 88888888,
                "data": {
                    "description": f"转换json数据失败：{e}",
                    "error_code": 88888888,
                }
            }

        # 我们不检查信息是否错误，在获取信息的时候在检查
        # if self.data['code'] != 200:
        #     raise ValueError(f'{self.data}')

        return self.data

    def un_read_count(self):
        """
        获取未读信息数量

        用来检查登录状态
        response_data = k.un_read_count()
        pp(response_data)
        if response_data['code'] == 401:
            print(f'用户登录失败：{response_data["data"]}')
        elif response_data['code'] != 200:
            print(f'发生未知错误：{response_data["data"]}')
        """
        url = f"{self.base_url}/api/admin/inner-message/unReadCount"
        r = self._session.get(url)
        return self.get_response_data(r)

    def personal_center_my_detail(self):
        """
        用户信息（当前登录账户）

        个人中心/我的信息
        网址: https://ds.kuojingyueyi.cn/app/center/info
        """
        url = f"{self.base_url}/api/admin/personal-center/detail"
        r = self._session.get(url)
        return self.get_response_data(r)

    def search_org(self, name, org_types=None, page=1, page_size=20):
        """
        搜索他方签约主体

        # 搜索 他方签约主体：org_types = [1]
        # 搜索 结算渠道：org_types = [3]
        # 搜索 所属公司：org_types = [2, 1]

        合约管理/采购合约
        网址: https://ds.kuojingyueyi.cn/app/contract-manage/cp-list?current=1&pageSize=20&authOrg=%E5%B9%BF%E5%B7%9E%E5%A4%A9%E6%9E%9C%E6%96%87%E5%8C%96%E4%BC%A0%E6%92%AD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&authOrgId=692
        """
        if org_types is None:
            org_types = [1]

        data = {
            'name': name,
            'orgTypes': org_types
        }
        url = f"{self.base_url}/api/admin/dict/org/search?pageNo={page}&pageSize={page_size}"
        r = self._session.post(url, json=data)
        return self.get_response_data(r)

    def contract_manage_cp_list(self, page=1, page_size=20, **kwargs):
        """
        采购合约列表

        合约管理/采购合约
        网址: https://ds.kuojingyueyi.cn/app/contract-manage/cp-list/?current=1&pageSize=20&offlineCode=SZQY-CGDL-20180401-200--051

        # 支持的参数
        "pageNo": 2,  # 可不用
        "current": 1,  # 可不用
        "pageSize": 20,  # 可不用
        # 内部合约编号
        "offlineCode": "SZQY-CGDL-20180401-200--051"
        """
        # print(kwargs)
        url = f"{self.base_url}/api/admin/cp-contract/list?pageNo={page}&pageSize={page_size}"
        r = self._session.post(url, json=kwargs)
        return self.get_response_data(r)

    # def search_contract_song(self, pk, copyright_type=3, page=1, page_size=20):
    #     """
    #     采购合约关联歌曲
    #
    #     合约管理/采购合约
    #     网址: https://ds.kuojingyueyi.cn/app/contract-manage/cp-view/5219?status=3&tab=related_songs
    #
    #     :param pk: 合同ID
    #     """
    #     data = {
    #         "contractId": pk,  # 合同ID
    #         "copyrightType": copyright_type  # 版权类型 1 词版权 2 曲版权 3 录音版权
    #     }
    #     url = f"{self.base_url}/api/admin/cp-contract/search-relate-song?pageNo={page}&pageSize={page_size}"
    #     r = self._session.post(url, json=data)
    #     return self.get_response_data(r)

    def get_cp_contract_work_list(self, pk, page=1, page_size=20):
        """
        采购合约-合约作品清单

        合约管理/采购合约
        网址: https://ds.kuojingyueyi.cn/app/contract-manage/cp-view/1104?tab=related_songs

        :param pk: 合同ID
        """
        data = {
            "contractId": pk,  # 合同ID
        }
        url = f"{self.base_url}/api/admin/cp-contract/work/list?pageNo={page}&pageSize={page_size}"
        r = self._session.post(url, json=data)
        return self.get_response_data(r)

    def get_cp_contract_work_related_unbound(self, pk, page=1, page_size=20):
        """
        采购合约-合约关联的作品(已入库但未在合约作品清单中)

        合约管理/采购合约
        网址: https://ds.kuojingyueyi.cn/app/contract-manage/cp-view/1104?tab=related_songs

        :param pk: 合同ID
        """
        data = {
            "contractId": pk,  # 合同ID
        }
        url = f"{self.base_url}/api/admin/cp-contract/work/related/unbound/list?pageNo={page}&pageSize={page_size}"
        r = self._session.post(url, json=data)
        return self.get_response_data(r)

    def get_cp_contract_detail(self, pk):
        """
        采购合约详情

        网址: https://ds.kuojingyueyi.cn/app/contract-manage/cp-view/17594?status=1

        :param pk: 采购合约ID
        """
        url = f"{self.base_url}/api/admin/cp-contract/detail/{pk}"
        r = self._session.get(url)
        return self.get_response_data(r)

    def get_cp_contract_detail_copyright(self, pk):
        """
        采购合约-版权信息

        网址:

        :param pk: 采购合约ID
        """
        url = f"{self.base_url}/api/admin/cp-contract/detail-copyright/{pk}"
        r = self._session.get(url)
        return self.get_response_data(r)

    def get_cp_contract_detail_settlement_list_mode(self, pk):
        """
        采购合约-结算模式

        网址:

        :param pk: 采购合约ID
        """
        url = f"{self.base_url}/api/admin/cp-contract/detail-settlement-mode-list/{pk}"
        r = self._session.get(url)
        return self.get_response_data(r)

    def get_cp_contract_detail_settlement(self, pk):
        """
        采购合约-结算信息

        网址:

        :param pk: 采购合约ID
        """
        url = f"{self.base_url}/api/admin/cp-contract/detail-settlement/list/{pk}"
        r = self._session.get(url)
        return self.get_response_data(r)

    def export_contract_data(self, pk, save_file=None, data_type=None, mode=1, type_int=70):
        """
        导出数据采购合约数据（文件）

        合约管理/采购合约
        网址: https://ds.kuojingyueyi.cn/app/contract-manage/cp-view/17961?status=3&tab=related_songs

        :param pk: 合同ID
        """
        if data_type is None:
            data_type = [1]

        data = {
            'dataType': data_type,
            'mode': mode,
            'paramJson': json.dumps({"contractId": str(pk)}, ),
            'type': type_int
        }

        url = f"{self.base_url}/api/admin/common/export/exportExcelOrTask"
        r = self._session.post(url, json=data, stream=True)

        if r.status_code == 200:
            if save_file is None:
                # 从响应头中提取文件名
                content_disposition = r.headers.get('Content-Disposition')
                if content_disposition:
                    filename_encoded = content_disposition.split('filename=')[-1].strip('\"')
                    filename = unquote(filename_encoded)  # 解码URL编码的文件名
                    save_file = f"{pk}_{os.path.basename(filename)}"  # 确保文件名是安全的
                else:
                    save_file = f'{pk}.xlsx'  # 默认文件名

            temp_save_file = save_file + ".tmp"
            try:
                # 保存文件
                with open(temp_save_file, 'wb') as file:
                    file.write(r.content)

                os.rename(temp_save_file, save_file)
                print(f"下载文件成功: {save_file}")
            except Exception as e:
                if os.path.exists(temp_save_file):
                    os.remove(temp_save_file)
                print(f"保存文件失败，已删除临时文件: {e}")
            return save_file
        else:
            print(f"访问错误: {r.status_code}")

    def contract_manage_sp_list(self, page=1, page_size=20, **kwargs):
        """
        售卖合约列表

        合约管理/售卖合约
        网址: https://ds.kuojingyueyi.cn/app/contract-manage/sp-list?current=1&pageSize=20

        # 支持的参数
        "pageNo": 2,  # 可不用
        "current": 1,  # 可不用
        "pageSize": 20,  # 可不用
        "status": '',  # 可不用

        # 内部合约编号
        offlineCode: "CON02-TME00-20241216-0035"
        """
        # print(kwargs)
        url = f"{self.base_url}/api/admin/sp-contract/search?pageNo={page}&pageSize={page_size}"
        r = self._session.post(url, json=kwargs)
        return self.get_response_data(r)

    def get_sp_contract_detail(self, pk):
        """
        售卖合约详情

        网址: https://ds.kuojingyueyi.cn/app/contract-manage/sp?contractId=25165

        :param pk: 售卖合约ID
        """
        url = f"{self.base_url}/api/admin/sp-contract/detail/{pk}"
        r = self._session.get(url)
        return self.get_response_data(r)

    def settlement_supplier_document(self, page=1, page_size=20, **kwargs):
        """
        供应商结算单

        结算管理/供应商结算单
        网址: https://ds.kuojingyueyi.cn/app/settle-manage/supplier-bill-manage?current=1&pageSize=20&contractIdOrName=QHKJ-WTZZ

        # 支持的参数
        "pageNo": 2,  # 可不用
        "current": 1,  # 可不用
        "pageSize": 20,  # 可不用
        # 合同ID/编号/名称
        contractIdOrName: "QHKJ-WTZZ"
        """
        # print(kwargs)
        # https://ds.kuojingyueyi.cn/api/admin/settlement-supplier-document/list?pageNo=1&pageSize=20
        url = f"{self.base_url}/api/admin/settlement-supplier-document/list?pageNo={page}&pageSize={page_size}"
        r = self._session.post(url, json=kwargs)
        return self.get_response_data(r)

    def supplier_bill_detail(self, pk):
        """
        供应商结算单-详情

        供应商结算单/查看详情
        网址: https://ds.kuojingyueyi.cn/app/settle-manage/supplier-bill-detail/196

        :param pk: 结算单ID
        """
        url = f"{self.base_url}/api/admin/settlement-supplier-document/detail/{pk}"
        r = self._session.get(url)
        return self.get_response_data(r)

    def supplier_bill_audit_approve(self, ids, status=0, approve='通过', msg=None):
        """
        供应商结算单-审核

        合约管理/供应商结算单
        网址: https://ds.kuojingyueyi.cn/app/app/settle-manage/supplier-bill-audit/196
        # status: 5 是当前审核状态 statusStr: "审核完成" 是状态描述
        # 可以通过 isCanApprove 来判断是否可以审核，"审核完成"和"驳回"的就算可以审核 再审核也没有意义
        # frozenStatus: 0 有审核权限的时候他也会影响审核按钮的状态 0 可以审核 1 禁止审核
        """
        # http://bq-test.karakal.com.cn:18100/api/admin/
        data = {
            "batchAudit": False,  # 批量审核
            "currentStatus": status,  # 0 初审 1 业务审核 2 复核 3 财务审核 > 流程结束
            "result": 1,  # 1 通过 0 不通过
            "supplierDocIds": ids,
            'msg': msg
        }

        if approve == '通过':
            data['result'] = 1
        else:
            data['result'] = 0
            if not msg:
                raise ValueError('请输入审批描述')

        if len(ids) > 1:
            data['batchAudit'] = True
        else:
            data['batchAudit'] = False

        url = f"{self.base_url}/api/admin/settlement-supplier-document/approve"
        r = self._session.post(url, json=data)
        return self.get_response_data(r)

    def settlement_payment_document_list(self, page=1, page_size=20, **kwargs):
        """
        支付单列表

        结算管理/支付单
        网址: https://ds.kuojingyueyi.cn/app/settle-manage/pay-bill-manage?current=1&pageSize=20

        # 支持的参数
        "pageNo": 2,  # 可不用
        "current": 1,  # 可不用
        "pageSize": 20,  # 可不用
        # 内部合约编号
        "docIdOrName": "P724_20230401_20230930_Z16OXKY"
        """
        # https://ds.kuojingyueyi.cn/api/admin//list?pageNo=1&pageSize=20
        # print(kwargs)
        url = f"{self.base_url}/api/admin/settlement-payment-document/list?pageNo={page}&pageSize={page_size}"
        r = self._session.post(url, json=kwargs)
        return self.get_response_data(r)

    def settlement_payment_document_detail(self, pk):
        """
        支付单详情

        结算管理/支付单/支付单信息
        网址: https://ds.kuojingyueyi.cn/app/settle-manage/pay-bill-detail/3682

        :param pk: 支付单ID
        """
        url = f"{self.base_url}/api/admin/settlement-payment-document/detail/{pk}"
        r = self._session.get(url)
        return self.get_response_data(r)

    def song_list(self, page=1, page_size=20, **kwargs):
        """
        歌曲列表

        内容管理/歌曲管理
        网址: https://ds.kuojingyueyi.cn/app/content-manage/song-manage?current=1&pageSize=20

        # 支持的参数
        'queryType': 1,  # 可不用
        'pageNo': 1,   # 可不用
        "current": 1,  # 可不用
        "pageSize": 20,  # 可不用
        """
        # print(kwargs)
        url = f"{self.base_url}/api/admin/song/list?pageNo={page}&pageSize={page_size}"
        r = self._session.post(url, json=kwargs)
        return self.get_response_data(r)

    def song_detail(self, pk):
        """
        歌曲详情

        歌曲管理/查看详情
        网址: https://ds-test.kuojingyueyi.cn/app/content-manage/song/detail/233616?status=1&albumId=73812

        :param pk: 歌曲ID
        """
        url = f"{self.base_url}/api/admin/song/detail/{pk}"
        r = self._session.get(url)
        return self.get_response_data(r)

    def album_list(self, page=1, page_size=20, **kwargs):
        """
        专辑列表

        内容管理/专辑管理
        网址: https://ds.kuojingyueyi.cn/app/content-manage/album-manage?current=1&pageSize=20

        # 支持的参数
        'queryType': 1,  # 可不用
        'pageNo': 1,   # 可不用
        "current": 1,  # 可不用
        "pageSize": 20,  # 可不用
        """
        # print(kwargs)
        url = f"{self.base_url}/api/admin/album/search?pageNo={page}&pageSize={page_size}"
        r = self._session.post(url, json=kwargs)
        return self.get_response_data(r)

    def album_detail(self, pk):
        """
        专辑详情

        专辑管理/查看详情
        网址: https://ds.kuojingyueyi.cn/app/content-manage/album/detail/73617?status=4

        :param pk: 专辑ID
        """
        url = f"{self.base_url}/api/admin/album/detail/{pk}"
        r = self._session.get(url)
        return self.get_response_data(r)
