"""
BiogasProjectInformation domain model and its repository implementation.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, List, Optional, Union, Generic, TypeVar

from enn_iot_oc.infrastructure.repository.single_repo_base import SingleRepoBase
from enn_iot_oc.infrastructure.repository.multi_repo_base import MultiRepoBase
from enn_iot_oc.util.string_util import parse_object, parse_array

__all__ = ["BiogasProjectInformation", "BiogasProjectInformationRepoImpl"]

T = TypeVar('T')

# 定义基类 - 确保使用Generic[T]
BiogasProjectInformationRepoBase = SingleRepoBase[T]

#------------- Domain Model -------------
@dataclass
class BiogasProjectInformation:
    """
    沼气项目信息
    """

    comOneid: str = ""
    annualOperatingDays: int = 0
    annualOperatingDays9t2rj: int = 0
    dailyBiogasProcessingCapacity: str = ""
    dailyBiogasProcessingCapacityPwk7d: str = ""
    keHuXianYouZhaoQiLiYongFangShi: str = ""
    yuJiNianChanZhaoQiLiangWanFang: str = ""
    zhaoQiXianYouYongTuDanFangQiShouYi: str = ""
    zhaoQiXianYouYongTuDanFangQiShouYiYuanFang: float = 0.0
    annualEnergySavingIncome: str = ""
    annualGasSalesRevenue: str = ""
    annualNaturalGasSupply: str = ""
    averageElectricityPrice: float = 0.0
    biogasMethaneContent: str = ""
    biogasPurchasePrice: str = ""
    customerName: str = ""
    cvcuId: str = ""
    data: str = ""
    equipmentDepreciationYears: str = ""
    gasPipelineDistance: str = ""
    hydrogenSulfideContent: int = 0
    incomeTax: str = ""
    indicator: str = ""
    intermediateVariable: str = ""
    investmentReturnPeriod: str = ""
    methaneContent: int = 0
    methanecontentA6lof: str = ""
    naturalGasPrice: float = 0.0
    naturalGasPrice1u5ts: float = 0.0
    netProfit: str = ""
    note: str = ""
    operationYears: str = ""
    returnOnInvestment: str = ""
    systemInstalledCapacity: str = ""
    totalInvestment: str = ""
    totalProfit: str = ""
    totalRevenue: str = ""
    unit: str = ""
    uploadData: str = ""

#------------- Repository Implementation -------------
class BiogasProjectInformationRepoImpl(BiogasProjectInformationRepoBase[BiogasProjectInformation]):
    """
    沼气项目信息
    """
    def __init__(self, eo_id: str = "", instance_id: str = "") -> None:
        """
        初始化方法
        """
        super().__init__(model_code="biogas_project_information", eo_id=eo_id, instance_id=instance_id)

    def to_domain(self, row: Dict[str, Any]) -> BiogasProjectInformation:
        """
        将数据库行转换为领域模型
        """
        return BiogasProjectInformation(
            annualOperatingDays=parse_object(row.get("annual_operating_days"), int),
            annualOperatingDays9t2rj=parse_object(row.get("annual_operating_days9t2rj"), int),
            dailyBiogasProcessingCapacity=parse_object(row.get("daily_biogas_processing_capacity"), str),
            dailyBiogasProcessingCapacityPwk7d=parse_object(row.get("daily_biogas_processing_capacity_pwk7d"), str),
            keHuXianYouZhaoQiLiYongFangShi=parse_object(row.get("ke_hu_xian_you_zhao_qi_li_yong_fang_shi"), str),
            yuJiNianChanZhaoQiLiangWanFang=parse_object(row.get("yu_ji_nian_chan_zhao_qi_liang_wan_fang"), str),
            zhaoQiXianYouYongTuDanFangQiShouYi=parse_object(row.get("zhao_qi_xian_you_yong_tu_dan_fang_qi_shou_yi"), str),
            zhaoQiXianYouYongTuDanFangQiShouYiYuanFang=parse_object(row.get("zhao_qi_xian_you_yong_tu_dan_fang_qi_shou_yi_yuan_fang"), float),
            annualEnergySavingIncome=parse_object(row.get("annual_energy_saving_income"), str),
            annualGasSalesRevenue=parse_object(row.get("annual_gas_sales_revenue"), str),
            annualNaturalGasSupply=parse_object(row.get("annual_natural_gas_supply"), str),
            averageElectricityPrice=parse_object(row.get("average_electricity_price"), float),
            biogasMethaneContent=parse_object(row.get("biogas_methane_content"), str),
            biogasPurchasePrice=parse_object(row.get("biogas_purchase_price"), str),
            comOneid=parse_object(row.get("com_oneid"), str),
            customerName=parse_object(row.get("customer_name"), str),
            cvcuId=parse_object(row.get("cvcu_id"), str),
            data=parse_object(row.get("data"), str),
            equipmentDepreciationYears=parse_object(row.get("equipment_depreciation_years"), str),
            gasPipelineDistance=parse_object(row.get("gas_pipeline_distance"), str),
            hydrogenSulfideContent=parse_object(row.get("hydrogen_sulfide_content"), int),
            incomeTax=parse_object(row.get("income_tax"), str),
            indicator=parse_object(row.get("indicator"), str),
            intermediateVariable=parse_object(row.get("intermediate_variable"), str),
            investmentReturnPeriod=parse_object(row.get("investment_return_period"), str),
            methaneContent=parse_object(row.get("methane_content"), int),
            methanecontentA6lof=parse_object(row.get("methanecontent_a6lof"), str),
            naturalGasPrice=parse_object(row.get("natural_gas_price"), float),
            naturalGasPrice1u5ts=parse_object(row.get("natural_gas_price1u5ts"), float),
            netProfit=parse_object(row.get("net_profit"), str),
            note=parse_object(row.get("note"), str),
            operationYears=parse_object(row.get("operation_years"), str),
            returnOnInvestment=parse_object(row.get("return_on_investment"), str),
            systemInstalledCapacity=parse_object(row.get("system_installed_capacity"), str),
            totalInvestment=parse_object(row.get("total_investment"), str),
            totalProfit=parse_object(row.get("total_profit"), str),
            totalRevenue=parse_object(row.get("total_revenue"), str),
            unit=parse_object(row.get("unit"), str),
            uploadData=parse_object(row.get("upload_data"), str),
        )

    def from_domain(self, entity) -> Dict[str, Any]:
        """
        将领域模型转换为数据库行
        """
        return {
            "annual_operating_days": getattr(entity, "annualOperatingDays", None),
            "annual_operating_days9t2rj": getattr(entity, "annualOperatingDays9t2rj", None),
            "daily_biogas_processing_capacity": getattr(entity, "dailyBiogasProcessingCapacity", None),
            "daily_biogas_processing_capacity_pwk7d": getattr(entity, "dailyBiogasProcessingCapacityPwk7d", None),
            "ke_hu_xian_you_zhao_qi_li_yong_fang_shi": getattr(entity, "keHuXianYouZhaoQiLiYongFangShi", None),
            "yu_ji_nian_chan_zhao_qi_liang_wan_fang": getattr(entity, "yuJiNianChanZhaoQiLiangWanFang", None),
            "zhao_qi_xian_you_yong_tu_dan_fang_qi_shou_yi": getattr(entity, "zhaoQiXianYouYongTuDanFangQiShouYi", None),
            "zhao_qi_xian_you_yong_tu_dan_fang_qi_shou_yi_yuan_fang": getattr(entity, "zhaoQiXianYouYongTuDanFangQiShouYiYuanFang", None),
            "annual_energy_saving_income": getattr(entity, "annualEnergySavingIncome", None),
            "annual_gas_sales_revenue": getattr(entity, "annualGasSalesRevenue", None),
            "annual_natural_gas_supply": getattr(entity, "annualNaturalGasSupply", None),
            "average_electricity_price": getattr(entity, "averageElectricityPrice", None),
            "biogas_methane_content": getattr(entity, "biogasMethaneContent", None),
            "biogas_purchase_price": getattr(entity, "biogasPurchasePrice", None),
            "com_oneid": getattr(entity, "comOneid", None),
            "customer_name": getattr(entity, "customerName", None),
            "cvcu_id": getattr(entity, "cvcuId", None),
            "data": getattr(entity, "data", None),
            "equipment_depreciation_years": getattr(entity, "equipmentDepreciationYears", None),
            "gas_pipeline_distance": getattr(entity, "gasPipelineDistance", None),
            "hydrogen_sulfide_content": getattr(entity, "hydrogenSulfideContent", None),
            "income_tax": getattr(entity, "incomeTax", None),
            "indicator": getattr(entity, "indicator", None),
            "intermediate_variable": getattr(entity, "intermediateVariable", None),
            "investment_return_period": getattr(entity, "investmentReturnPeriod", None),
            "methane_content": getattr(entity, "methaneContent", None),
            "methanecontent_a6lof": getattr(entity, "methanecontentA6lof", None),
            "natural_gas_price": getattr(entity, "naturalGasPrice", None),
            "natural_gas_price1u5ts": getattr(entity, "naturalGasPrice1u5ts", None),
            "net_profit": getattr(entity, "netProfit", None),
            "note": getattr(entity, "note", None),
            "operation_years": getattr(entity, "operationYears", None),
            "return_on_investment": getattr(entity, "returnOnInvestment", None),
            "system_installed_capacity": getattr(entity, "systemInstalledCapacity", None),
            "total_investment": getattr(entity, "totalInvestment", None),
            "total_profit": getattr(entity, "totalProfit", None),
            "total_revenue": getattr(entity, "totalRevenue", None),
            "unit": getattr(entity, "unit", None),
            "upload_data": getattr(entity, "uploadData", None),
        }

    def empty_object(self) -> BiogasProjectInformation:
        """
        创建一个空的领域模型对象
        """
        return BiogasProjectInformation(
            annualOperatingDays=0,
            annualOperatingDays9t2rj=0,
            dailyBiogasProcessingCapacity="",
            dailyBiogasProcessingCapacityPwk7d="",
            keHuXianYouZhaoQiLiYongFangShi="",
            yuJiNianChanZhaoQiLiangWanFang="",
            zhaoQiXianYouYongTuDanFangQiShouYi="",
            zhaoQiXianYouYongTuDanFangQiShouYiYuanFang=0.0,
            annualEnergySavingIncome="",
            annualGasSalesRevenue="",
            annualNaturalGasSupply="",
            averageElectricityPrice=0.0,
            biogasMethaneContent="",
            biogasPurchasePrice="",
            comOneid="",
            customerName="",
            cvcuId="",
            data="",
            equipmentDepreciationYears="",
            gasPipelineDistance="",
            hydrogenSulfideContent=0,
            incomeTax="",
            indicator="",
            intermediateVariable="",
            investmentReturnPeriod="",
            methaneContent=0,
            methanecontentA6lof="",
            naturalGasPrice=0.0,
            naturalGasPrice1u5ts=0.0,
            netProfit="",
            note="",
            operationYears="",
            returnOnInvestment="",
            systemInstalledCapacity="",
            totalInvestment="",
            totalProfit="",
            totalRevenue="",
            unit="",
            uploadData="",
        )
