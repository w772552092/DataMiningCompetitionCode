import os
import sys
import json
from datetime import datetime
import pandas as pd
from ai_brain import get_answer


def run_single_status_tests():
    """
    运行单一状态时间查询的测试用例
    """
    test_cases = [
        # 基础状态查询
        # {
        #     "id": "7",
        #     "question": "2024/8/23 A架开机的时间点（请以XX:XX输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 期望格式：XX:XX
        # },
        # {
        #     "id": "8",
        #     "question": "2024/8/24 征服者入水时间点（请以XX:XX输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'
        # },
        # {
        #     "id": "9",
        #     "question": "2024/8/24 揽绳解除的时间点（请以XX:XX输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'
        # },
        # {
        #     "id": "10",
        #     "question": "2024/8/24 A架摆回的时间点（请以XX:XX输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'
        # },
        # {
        #     "id": "11",
        #     "question": "2024/8/24 A架摆出的时间点（请以XX:XX输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'
        # },
        # # 变体格式测试
        # {
        #     "id": "61",
        #     "question": "2024年5月20日征服者入水的时间是？（请以XX:XX输出）",
        #     "expected_pattern": r'^\d{2}:\d{2}$'
        # },
        # {
        #     "id": "80",
        #     "question": "8月15日早上，A架的开机时间是几点（请以XX:XX输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'
        # },
        # {
        #     "id": "82",
        #     "question": "在2024年8月28日，A架的关机时间是几点（请以XX:XX输出）",
        #     "expected_pattern": r'^\d{2}:\d{2}$'
        # },
        # # 特殊条件测试
        # {
        #     "id": "93",
        #     "question": "在2024年9月3日，折臂吊车最后一次开机是什么时候（请以XX:XX输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'
        # },
        # {
        #     "id": "95",
        #     "question": "在2024年8月24日，A架第二次开机是什么时候（请以XX:XX输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'
        # }

        # 新增测试
        # {
        #     "id": "gysxdmx_00015",
        #     "question": "以征服者落座为标志，2024/8/23 的深海作业A作业结束的时间（请以XX:XX输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },
        #
        # {
        #     "id": "gysxdmx_00019",
        #     "question": "2024/8/24 下午，A架开机发生在折臂吊车开机之前，是否正确？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00022",
        #     "question": "2024/8/23/上午A架的运行时长和下午A架开机时长相比，哪个长，长多少（以整数分钟输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00023",
        #     "question": "2024/8/24A架摆回和摆出的时间相隔多久（以整数分钟输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00024",
        #     "question": "2024/8/23 ~ 2024/8/25 早上A架在9点前开机的有几天？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },


        # {
        #     "id": "gysxdmx_00025",
        #     "question": "2024/8/23 ~ 2024/8/25 哪一天上午A架的运行时长最长，运行了多久（以整数分钟输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00026",
        #     "question" : "2024/8/23 和 2024/8/24 上午A架运行的平均时间多少（四舍五入至整数分钟输出）",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00027",
        #     "question": "2024/8/23 和 2024/8/24 征服者从起吊到入水平均需要多久（以分钟输出，保留一位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00028",
        #     "question": "2024/8/23 DP过程中，侧推的总能耗是多少（单位化成kWh，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00029",
        #     "question": "2024/8/23 上午折臂吊车的总能耗是多少（单位化成kWh，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },


        # {
        #     "id": "gysxdmx_00030",
        #     "question": "2024/8/23 和 2024/8/24 的DP过程中，侧推的平均能耗是多少（单位化成kWh，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        {
            "id": "gysxdmx_00031",
            "question" : "2024/8/24 DP过程中，推进系统的总能耗是多少（单位化成kWh，保留2位小数）？",
            "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        },

        # {
        #     "id": "gysxdmx_00032",
        #     "question": "2024/8/24 上午，甲板机械设备的总能耗是多少（单位化成kWh，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },


        # {
        #     "id": "gysxdmx_00033",
        #     "question": "2024/8/24 上午，折臂吊车的能耗占甲板机械设备的比例（以%输出，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },


        # {
        #     "id": "gysxdmx_00034",
        #     "question": "2024/8/23 0:00 ~ 2024/8/25 0:00四个发电机中哪个的能耗最大，能耗为多少（单位化成kWh，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00035",
        #     "question": "2024/8/23和2024/8/25小艇入水到小艇落座，折臂吊车的总能耗是多少（单位化成kWh，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00036",
        #     "question": "2024/8/23 A架和折臂吊车的运行时间分别是多少（以整数分钟输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00037",
        #     "question": "2024/8/23 A架比折臂吊车的运行时间少多少（以整数分钟输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00039",
        #     "question": "2024/8/23、 2024/8/24和2024/8/25 A架的平均摆动次数是多少次？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00040",
        #     "question": "2024/8/23和2024/8/25 平均作业时长是多久（四舍五入至整数分钟输出，下放阶段以ON DP和OFF DP为标志，回收阶段以A架开机和关机为标志）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00042",
        #     "question": "数据中有部分时间A架的角度数据出现了异常，请指出开始时间和结束时间（精确到天）",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00048",
        #     "question": "2024/8/23 0:00 ~ 2024/8/25 0:00发电机组的燃油消耗量为多少（单位化成L，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00049",
        #     "question": "2024/8/23 0:00 ~ 2024/8/25 0:00总发电量是多少（单位化为kWh，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00050",
        #     "question": "2024/8/23 0:00 ~ 2024/8/25 0:00推进系统能耗占总发电量的比例（以%输出，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00051",
        #     "question": "2024/8/23 0:00 ~ 2024/8/25 0:00甲板机械能耗占总发电量的比例（以%输出，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00052",
        #     "question": "2024/8/23和2024/8/25 平均作业能耗是多久（单位化成kWh，保留2位小数，下放阶段以ON DP和OFF DP为标志，回收阶段以A架开机和关机为标志）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00053",
        #     "question": "假设柴油的密度为0.8448kg/L，柴油热值为42.6MJ/kg，请计算2024/8/23 0:00 ~ 2024/8/25 0:00的理论发电量（单位化成kWh，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00054",
        #     "question": "假设柴油的密度为0.8448kg/L，柴油热值为42.6MJ/kg，请计算2024/8/23 0:00 ~ 2024/8/25 0:00柴油机的发电效率（%，保留2位小数）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00057",
        #     "question": "统计2024/8/24-8/30征服者在16:00前出水的比例（%，保留2位小数）",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00058",
        #     "question": "统计2024/8/24-8/30在9点前开始作业的比例（%，保留2位小数）",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00059",
        #     "question": "统计2024/8/24-8/30征服者在9点前入水的比例（%，保留2位小数）",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00060",
        #     "question": "24年5月19日A架的开机时间分别是几点，关机时间分别是几点？（请以XX:XX输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00062",
        #     "question": "2024年5月20日征服者入水后A架摆回到位的时间是？（请以XX:XX输出）",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00065",
        #     "question": "24年8月23日上午折臂吊开机和关机的时间分别是几点？（请用XX:XX表示）",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00068",
        #     "question": "一号柴油发电机组有功功率测量的范围是多少kW到多少kW？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00071",
        #     "question": "2024年5月19日A架的实际运行时长是多久？效率是多少？（请以XX:XX输出时长，XX.XX%输出效率）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00072",
        #     "question": "5月20日征服者入水A架外摆的最大角度范围分别是多少度，持续了多久？（请以XX:XX输出）？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00074",
        #     "question": "24年8月23日征服者入水时间距离征服者出水时间是多久？（请用XX小时XX分钟表示）",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00075",
        #     "question": "5月20日征服者入水到A架摆回用了多少时间？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00077",
        #     "question": "停泊/应急发电机组转速高于多少RPM时会发生预警？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },

        # {
        #     "id": "gysxdmx_00079",
        #     "question": "8月24日征服者落座几分钟后A架关机的？",
        #     "expected_pattern": r'^\d{2}:\d{2}$'  # 严格匹配时间格式（如 15:30）
        # },
    ]

    test_results = {
        "total": len(test_cases),
        "passed": 0,
        "failed": 0,
        "details": []
    }

    print("开始运行单一状态时间查询测试...\n")

    for case in test_cases:
        print(f"测试用例 {case['id']}:")
        print(f"问题: {case['question']}")

        # 获取答案
        result = get_answer(case['question'])
        print(f"答案: {result}")

        # 验证答案格式
        import re
        format_correct = bool(re.match(case['expected_pattern'], result.strip()))

        # 记录结果
        test_results['details'].append({
            "id": case['id'],
            "question": case['question'],
            "answer": result,
            "format_correct": format_correct
        })

        if format_correct:
            test_results['passed'] += 1
            print("✓ 格式验证通过")
        else:
            test_results['failed'] += 1
            print("✗ 格式验证失败")
        print()

    # 打印测试总结
    print("\n测试总结:")
    print(f"总用例数: {test_results['total']}")
    print(f"通过数量: {test_results['passed']}")
    print(f"失败数量: {test_results['failed']}")
    print(f"通过率: {(test_results['passed'] / test_results['total'] * 100):.2f}%")

    return test_results


if __name__ == "__main__":
    test_results = run_single_status_tests()

    # 保存测试报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f'single_status_test_report_{timestamp}.json'