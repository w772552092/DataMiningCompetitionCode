import json
from zhipuai import ZhipuAI
import tools
import api
import os


api_key = 'ef195d246780430f941744e45af1d0c6.vt0UA8oGOLvQeMx3'#老师的key
# 首先检查必要的文件夹是否存在
folders = ["database_in_use", "data"]
if any(not os.path.exists(folder) for folder in folders):
    # 如果文件夹不存在，创建它们
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    # 导入数据处理模块进行初始化
    import data_process
else:
    # 文件夹已存在，打印提示信息
    print("所有文件夹均已存在。不再重新预处理数据。")
    print("需要预处理数据，请删除文件夹后重新运行。")


def create_chat_completion(messages, model="glm-4-plus"):
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model, stream=False, messages=messages
    )
    return response


# In[4]:


# choose_table
def choose_table(question):
    with open("dict.json", "r", encoding="utf-8") as file:
        context_text = str(json.load(file))
    prompt = f"""我有如下数据表：<{context_text}>
    现在基于数据表回答问题：{question}。
    分析需要哪些数据表。
    仅返回需要的数据表名，无需展示分析过程。
    """
    messages = [{"role": "user", "content": prompt}]
    response = create_chat_completion(messages)
    return str(response.choices[0].message.content)


# In[5]:


def glm4_create(max_attempts, messages, tools, model="glm-4-plus"):
    """
    调用 GLM 语言模型的函数

    参数:
    max_attempts: 最大尝试次数（这里是6）
    messages: 对话历史消息列表
    tools: 可用的工具列表
    model: 使用的模型名称
    """
    # 创建 API 客户端
    client = ZhipuAI(api_key=api_key)

    # 尝试获取响应，最多尝试 max_attempts 次
    for attempt in range(max_attempts):
        # 调用 API 获取响应
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
        )

        # 检查响应中是否包含 Python 代码
        if (response.choices and
                response.choices[0].message and
                response.choices[0].message.content):

            if "```python" in response.choices[0].message.content:
                # 如果包含 Python 代码，继续尝试
                continue
            else:
                # 如果不包含 Python 代码，返回响应
                break

    return response


function_map = {
    "calculate_uptime": api.calculate_uptime,
    "compute_operational_duration": api.compute_operational_duration,
    "get_table_data": api.get_table_data,
    "load_and_filter_data": api.load_and_filter_data,
    "calculate_total_energy": api.calculate_total_energy,
    "calculate_total_deck_machinery_energy": api.calculate_total_deck_machinery_energy,
    "query_device_parameter": api.query_device_parameter,
    "get_device_status_by_time_range": api.get_device_status_by_time_range,
    "get_operation_start_time": api.get_operation_start_time,
    #新加入
    "calculate_efficiency": api.calculate_efficiency,
    #新加入
    "get_operation_end_time": api.get_operation_end_time,
    #新加入
    "compare_device_startup_order": api.compare_device_startup_order,
    #新加入
    "compare_operation_durations": api.compare_operation_durations,
    #新加入
    "calculate_action_time_diff": api.calculate_action_time_diff,
    #新加入
    "find_longest_morning_operation": api.find_longest_morning_operation,
    #新加入
    "calculate_average_morning_runtime": api.calculate_average_morning_runtime,
    #新加入
    "calculate_thruster_energy_during_dp": api.calculate_thruster_energy_during_dp,
    #新加入
    "calculate_average_thruster_energy_during_dp": api.calculate_average_thruster_energy_during_dp,
    #新加入
    "calculate_propulsion_energy_during_dp": api.calculate_propulsion_energy_during_dp,
    #新加入
    "calculate_crane_energy_ratio": api.calculate_crane_energy_ratio,
    #新加入
    "find_max_generator_energy": api.find_max_generator_energy,
    #新加入
    "calculate_crane_energy_between_boat_states": api.calculate_crane_energy_between_boat_states,
    #新加入
    "get_devices_runtime" : api.get_devices_runtime,
    #新加入
    "calculate_runtime_difference" : api.calculate_runtime_difference,
    #新加入
    "calculate_average_swing_count" : api.calculate_average_swing_count,
    #新加入
    "calculate_average_operation_time" : api.calculate_average_operation_time,
    #新加入
    "detect_angle_anomalies" : api.detect_angle_anomalies,
    #新加入
    "calculate_total_fuel_consumption" : api.calculate_total_fuel_consumption,
    #新加入
    "calculate_total_power_generation" : api.calculate_total_power_generation,
    #新加入
    "calculate_propulsion_energy_ratio" : api.calculate_propulsion_energy_ratio,
    #新加入
    "calculate_deck_machinery_power_ratio" : api.calculate_deck_machinery_power_ratio,
    #新加入
    "calculate_average_operation_energy" : api.calculate_average_operation_energy,
    #新加入
    "calculate_theoretical_power_generation" : api.calculate_theoretical_power_generation,
    #新加入
    "calculate_generator_efficiency" : api.calculate_generator_efficiency,
    #新加入
    "calculate_conqueror_ascend_ratio" : api.calculate_conqueror_ascend_ratio,
    #新加入
    "calculate_early_operation_ratio" : api.calculate_early_operation_ratio,
    #新加入
    "calculate_conqueror_entry_ratio" : api.calculate_conqueror_entry_ratio,
    #新加入
    "get_power_onoff_times" : api.get_power_onoff_times,
    #新加入
    "get_a_frame_return_time_after_entry" : api.get_a_frame_return_time_after_entry,
    #新加入
    "get_crane_power_times" : api.get_crane_power_times,
    #新加入
    "get_generator_power_range" : api.get_generator_power_range,
    #新加入
    "calculate_operation_time_and_efficiency" : api.calculate_operation_time_and_efficiency,
    #新加入
    "analyze_a_frame_swing_angles" : api.analyze_a_frame_swing_angles,
    #新加入
    "calculate_entry_to_ascend_duration" : api.calculate_entry_to_ascend_duration,
    #新加入
    "calculate_entry_to_return_duration" : api.calculate_entry_to_return_duration,
    #新加入
    "get_generator_rpm_alarm_threshold" : api.get_generator_rpm_alarm_threshold,
    #新加入
    "calculate_seated_to_shutdown_duration" : api.calculate_seated_to_shutdown_duration,
}


# def get_answer_2(question, tools, api_look: bool = True):
#     """
#     生成答案的主要函数
#     参数:
#     question: 用户问题
#     tools: 可用的工具列表
#     api_look: API查看标志（默认True）
#
#     返回:
#     tuple: (答案文本, 函数调用结果记录)
#     """
#     # 1. 准备工作：过滤工具列表
#     filtered_tools = tools
#
#     try:
#         # 2. 初始化对话消息列表
#         messages = [
#             {
#                 "role": "system",
#                 "content": "不要假设或猜测传入函数的参数值。如果用户的描述不明确，请要求用户提供必要信息。",
#             },
#             {"role": "user", "content": question},
#         ]
#
#         # 3. 第一次调用语言模型
#         response = glm4_create(6, messages, filtered_tools)
#         # 将模型响应添加到消息历史
#         messages.append(response.choices[0].message.model_dump())
#
#         # 4. 初始化函数调用结果列表
#         function_results = []
#         # 设置最大迭代次数
#         max_iterations = 6
#
#         # 5. 主要处理循环
#         for _ in range(max_iterations):
#             # 如果没有工具调用请求，退出循环
#             if not response.choices[0].message.tool_calls:
#                 break
#
#             # 获取工具调用信息
#             tool_call = response.choices[0].message.tool_calls[0]
#             # 解析函数参数
#             args = json.loads(tool_call.function.arguments)
#
#             # 获取要调用的函数名
#             function_name = tool_call.function.name
#
#             # 6. 执行工具函数
#             if function_name in function_map:
#                 # 调用相应的函数
#                 function_result = function_map[function_name](**args)
#                 # 记录函数调用结果
#                 function_results.append(function_result)
#
#                 # 将函数调用结果添加到消息历史
#                 messages.append(
#                     {
#                         "role": "tool",
#                         "content": f"{function_result}",
#                         "tool_call_id": tool_call.id,
#                     }
#                 )
#
#                 # 再次调用语言模型处理函数调用结果
#                 response = glm4_create(8, messages, filtered_tools)
#             else:
#                 # 如果找不到对应的函数，打印错误信息并退出循环
#                 print(f"未找到对应的工具函数: {function_name}")
#                 break
#
#         # 7. 返回最终结果
#         return response.choices[0].message.content, str(function_results)
#
#     except Exception as e:
#         # 错误处理
#         print(f"Error generating answer for question: {question}, {e}")
#         return None, None



import json

def get_answer_2(question, tools, api_look: bool = True):
    """
    生成答案的主要函数
    参数:
        question: 用户问题
        tools: 可用的工具列表
        api_look: API查看标志（默认True）
    返回:
        tuple: (答案文本, 函数调用结果记录)
    """
    # 1. 准备工作：过滤工具列表
    filtered_tools = tools

    # 2. 初始化对话消息列表
    messages = [
        {
            "role": "system",
            "content": "不要假设或猜测传入函数的参数值。如果用户的描述不明确，请要求用户提供必要信息。",
        },
        {"role": "user", "content": question},
    ]

    # 3. 第一次调用语言模型
    response = glm4_create(6, messages, filtered_tools)
    # 将模型响应添加到消息历史
    messages.append(response.choices[0].message.model_dump())

    # 4. 初始化函数调用结果列表
    function_results = []
    # 设置最大迭代次数
    max_iterations = 6

    # 5. 主要处理循环
    for _ in range(max_iterations):
        # 如果没有工具调用请求，退出循环
        if not response.choices[0].message.tool_calls:
            break

        # 获取工具调用信息
        tool_call = response.choices[0].message.tool_calls[0]

        # 解析函数参数
        args = json.loads(tool_call.function.arguments)

        # 获取要调用的函数名
        function_name = tool_call.function.name

        # 6. 执行工具函数
        if function_name in function_map:
            # 调用相应的函数
            function_result = function_map[function_name](**args)

            # 记录函数调用结果
            function_results.append(function_result)

            # 将函数调用结果添加到消息历史
            messages.append(
                {
                    "role": "tool",
                    "content": f"{function_result}",
                    "tool_call_id": tool_call.id,
                }
            )

            # 再次调用语言模型处理函数调用结果
            response = glm4_create(8, messages, filtered_tools)
        else:
            # 如果找不到对应的函数，打印错误信息并退出循环
            print(f"未找到对应的工具函数: {function_name}")
            break


    # 7. 返回最终结果
    return response.choices[0].message.content, str(function_results)









import re
# In[6]:

def select_api_based_on_question(question, tools):
    """
    根据问题内容选择合适的 API 工具

    Args:
        question (str): 用户的问题文本
        tools (list): 可用的工具列表
    Returns:
        tuple: (处理后的问题内容, 过滤后的工具列表)

    """
    print("问题内容：", question)

    # 优先处理深海作业相关问题
    # dp_keywords = ["深海作业A作业开始", "深海作业A作业结束", "平均作业时长"]
    dp_keywords = ["深海作业A作业开始", "深海作业A作业结束",]
    if any(keyword in question for keyword in dp_keywords):
        api_list_filter = ["get_operation_end_time" if "结束" in question
                           else "get_operation_start_time"]
        return question, filter_tools(api_list_filter, tools)

    # 效率计算问题
    elif "效率" in question and "发电" not in question and ("运行时长" not in question):
        return question, filter_tools(["calculate_efficiency"], tools)

    # 设备开机顺序比较问题
    elif ( bool(re.search(r"(\d{4}/\d{1,2}/\d{1,2})\s*(上午|下午)?.*开机发生在.*开机之(前|后)", question)) and
          any(device in question for device in ['A架', '折臂吊车'])):
        print("设备开机顺序比较问题")
        return question, filter_tools(["compare_device_startup_order"], tools)

    # 运行时长和开机时长比较问题
    elif all(keyword in question for keyword in ['运行时长', '开机时长', '相比']):
        return question, filter_tools(["compare_operation_durations"], tools)

    elif ("相隔多久" in question and
          any(action in question for action in ["摆回", "摆出"]) and
          "整数分钟输出" in question):
        return question, filter_tools(["calculate_action_time_diff"], tools)

    # 设备最后状态查询
    elif "最后一次" in question and any(action in question for action in ["落座", "关机"]):
        return question, filter_tools(["get_device_status_by_time_range"], tools)

    # 时间范围动作查询 新加入
    elif ("上午" in question and "运行时长最长" in question and
          "运行了多久" in question and "~" in question):
        return question, filter_tools(["find_longest_morning_operation"], tools)

    #平均运行时间问题 新加入
    elif (all(x in question for x in ["上午", "运行", "平均时间"]) and
          "整数分钟输出" in question):
        return question, filter_tools(["calculate_average_morning_runtime"], tools)
    #dp过程中侧推能耗问题 新加入
    elif ("DP过程中" in question and "侧推" in question and "能耗" in question and "平均" not in question):
        return question, filter_tools(["calculate_thruster_energy_during_dp"], tools)

    # DP过程中侧推平均能耗问题 新加入
    elif ("DP过程中" in question and "侧推" in question and
          "平均能耗" in question and ( "~" in question or "到" in question or "和" in question)):
        return question, filter_tools(["calculate_average_thruster_energy_during_dp"], tools)

   # DP过程中推进系统总能耗问题 新加入
    elif ("DP过程中" in question and "推进系统" in question and
          "总能耗" in question):
        return question, filter_tools(["calculate_propulsion_energy_during_dp"], tools)

    # 折臂吊车能耗比例问题 新加入
    elif ("能耗" in question and "比例" in question and
          "折臂吊车" in question and "甲板机械设备" in question):
        return question, filter_tools(["calculate_crane_energy_ratio"], tools)

    #四个发电机能耗最大问题 新加入
    elif ("四" in question or '4' in question) and "发电机" in question and "能耗最大" in question:
        return question, filter_tools(["find_max_generator_energy"], tools)

    #小艇落座和入水之间折臂吊车能耗问题 新加入
    elif "小艇入水" in question and "小艇落座" in question and "折臂吊车" in question and "能耗" in question:
        return question, filter_tools(["calculate_crane_energy_between_boat_states"], tools)

    #a架和折臂吊车的运行时间 新加入
    elif ("运行时间" in question and
          "A架" in question and "折臂吊车" in question and
          "分别" in question):
        return question, filter_tools(["get_devices_runtime"], tools)

    #a架和折臂吊车的运行时间差 新加入
    elif ("A架" in question and "折臂吊车" in question and
          "运行时间" in question and "少" in question):
        return question, filter_tools(["calculate_runtime_difference"], tools)

    #计算多天A架的平均摆动次数 新加入
    elif ("A架" in question and "平均摆动次数" in question):
        return question, filter_tools(["calculate_average_swing_count"], tools)

    #计算平均作业时长 新加入
    elif ("平均作业时长" in question and
          "ON DP" in question and "OFF DP" in question and
          "开机" in question and "关机" in question):
        return question, filter_tools(["calculate_average_operation_time"], tools)

    # 角度数据异常检测 新加入
    elif ("角度数据" in question and "异常" in question and
          "开始时间" in question and "结束时间" in question):
        return question, filter_tools(["detect_angle_anomalies"], tools)

    #计算发电机组的总燃油消耗量 新加入
    elif "发电机组" in question and "燃油消耗量" in question:
        return question, filter_tools(["calculate_total_fuel_consumption"], tools)

    # 总能耗问题 新加入
    elif "总发电量" in question and ("比例" not in question):
        return question, filter_tools(["calculate_total_power_generation"], tools)

    #计算推进系统能耗占总发电量的比例 新加入
    elif all(key in question for key in ["推进系统", "能耗", "总发电量", "比例"]):
        return question, filter_tools(["calculate_propulsion_energy_ratio"], tools)

    #计算甲板机械能耗占总发电量的比例 新加入
    elif "甲板机械能耗" in question and "总发电量" in question and "比例" in question:
        return question, filter_tools(["calculate_deck_machinery_power_ratio"], tools)

    #计算指定日期的平均作业能耗（下放+回收阶段） 新加入
    elif ("平均作业能耗" in question and "DP" in question and
          "开机" in question and "关机" in question):
        return question, filter_tools(["calculate_average_operation_energy"], tools)

    #计算指定时间段内的理论发电量 新加入
    elif "理论发电量" in question and "柴油" in question and "热值" in question:
        return question, filter_tools(["calculate_theoretical_power_generation"], tools)

    #计算指定时间段柴油机发电效率 新加入
    elif "发电效率" in question and "柴油" in question:
        return question, filter_tools(["calculate_generator_efficiency"], tools)

    #计算征服者在指定时间前出水的比例 新加入
    elif ("征服者" in question and "出水" in question and
          "比例" in question and "前" in question):
        return question, filter_tools(["calculate_conqueror_ascend_ratio"], tools)

    #计算在指定时间前开始作业(ON_DP)的比例 新加入
    elif ("开始作业" in question and "前" in question and "比例" in question):
        return question, filter_tools(["calculate_early_operation_ratio"], tools)

    #计算征服者在指定时间前入水的比例 新加入
    elif ("征服者" in question and "入水" in question and
          "前" in question and "比例" in question):
        return question, filter_tools(["calculate_conqueror_entry_ratio"], tools)

    #获取指定日期A架的开关机时间点 新加入
    elif ("A架" in question and "开机时间" in question and
          "关机时间" in question and "分别" in question):
        return question, filter_tools(["get_power_onoff_times"], tools)

    # 获取指定日期征服者入水后A架摆回时间 新加入
    elif ("征服者入水后" in question and "A架摆回" in question and
          "时间" in question):
        return question, filter_tools(["get_a_frame_return_time_after_entry"], tools)

    #获取指定日期和时间段的折臂吊车开关机时间点 新加入
    elif "折臂吊" in question and "开机" in question and "关机" in question and "时间" in question:
        return question, filter_tools(["get_crane_power_times"], tools)

    #获取发电机组的功率测量范围 新加入
    elif all(key in question for key in ["柴油发电机组", "有功功率", "范围"]):
        return question, filter_tools(["get_generator_power_range"], tools)

    #计算A架的实际运行时长和效率 新加入
    elif "实际运行时长" in question and "效率" in question:
        return question, filter_tools(["calculate_operation_time_and_efficiency"], tools)

    #计算A架外摆的最大角度范围及持续时间 新加入
    elif "A架外摆" in question and "最大角度范围" in question:
        return question, filter_tools(["analyze_a_frame_swing_angles"], tools)

    #计算征服者入水到出水的时间间隔 新加入
    elif ("征服者入水" in question and "出水" in question and
          "时间" in question and "多久" in question):
        return question, filter_tools(["calculate_entry_to_ascend_duration"], tools)


    #计算征服者入水到a架摆回的时间间隔 新加入
    elif ("征服者入水" in question and "A架摆回" in question and
          "用了多少时间" in question):
        return question, filter_tools(["calculate_entry_to_return_duration"], tools)

    #获取发电机组转速的预警阈值 新加入
    elif all(key in question for key in ["停泊/应急发电机组", "转速", "预警"]):
        return question, filter_tools(["get_generator_rpm_alarm_threshold"], tools)


    #计算征服者落座到A架关机的时间间隔 新加入
    elif ("征服者落座" in question and "A架关机" in question and
          "分钟" in question):
        return question, filter_tools(["calculate_seated_to_shutdown_duration"], tools)

    # 状态时间点查询
    elif ("XX:XX输出" in question and
          any(keyword in question for keyword in ["开机", "入水", "解除", "摆回", "摆出"])):
        return question, filter_tools(["get_device_status_by_time_range"], tools)


    # 能耗相关查询
    elif "能耗" in question:
        if "甲板机械设备" in question:
            api_list_filter = ["calculate_total_deck_machinery_energy"]
        else:
            api_list_filter = ["calculate_total_energy"]
        return question, filter_tools(api_list_filter, tools)

    # 动作查询
    elif "动作" in question:
        question += "动作直接引用不要修改,如【A架摆回】"
        return question, filter_tools(["get_device_status_by_time_range"], tools)

    # 时长查询
    elif any(keyword in question for keyword in ["开机时长", "运行时长"]):
        if "实际运行时长" not in question:
            question = question.replace("运行时长", "开机时长")
        return question, filter_tools(["calculate_uptime"], tools)

    # 默认情况：根据表名选择API
    else:
        table_name_string = choose_table(question)
        with open("dict.json", "r", encoding="utf-8") as file:
            table_data = json.load(file)

        table_name = [item for item in table_data
                      if item["数据表名"] in table_name_string]

        if any(item["数据表名"] == "设备参数详情表" for item in table_name):
            return str(table_name) + question, filter_tools(["query_device_parameter"], tools)
        else:
            return str(table_name) + question, filter_tools(["get_table_data"], tools)


def filter_tools(api_list, tools):
    """
    根据API名称列表过滤工具

    Args:
        api_list (list): API名称列表
        tools (list): 可用工具列表
    Returns:
        list: 过滤后的工具列表
    """
    print("API列表：", api_list)
    return [tool for tool in tools
            if tool.get("function", {}).get("name") in api_list]

# def select_api_based_on_question(question, tools):
#     """
#     根据问题的内容选择合适的 API 工具
#     参数:
#     question: 用户的问题文本
#     tools: 可用的工具列表
#     返回:
#     content_p_1: 处理后的问题内容
#     filtered_tool: 过滤后的工具列表
#
#     """
#     # 在select_api_based_on_question函数的开头添加
#     dp_keywords = [
#         "深海作业A作业开始",
#         "深海作业A作业结束",
#         "平均作业时长"
#     ]
#
#     is_dp_question = any(keyword in question for keyword in dp_keywords)
#
#     if is_dp_question:
#         if "结束" in question:
#             api_list_filter = ["get_operation_end_time"]
#         else:
#             api_list_filter = ["get_operation_start_time"]
#
#         content_p_1 = question
#         filtered_tools = [
#             tool for tool in tools
#             if tool.get("function", {}).get("name") in api_list_filter
#         ]
#         return content_p_1, filtered_tools
#
#     """
#     新加入的逻辑
#     """
#
#     # 检查效率相关问题
#     if "效率" in question:
#         api_list_filter = ["calculate_efficiency"]
#         return question, [tool for tool in tools
#                         if tool.get("function", {}).get("name") in api_list_filter]
#     """
#     新加入的逻辑
#     """
#     # 设备开机顺序判断 - 使用更精确的模式匹配
#     device_order_pattern = r'(\d{4}/\d{1,2}/\d{1,2})\s*(上午|下午)?.*开机发生在.*开机之(前|后)'
#     if re.search(device_order_pattern, question):
#         # 确保这里涉及的是设备开机顺序的比较
#         if ('A架' in question and '折臂吊车' in question) or ('折臂吊车' in question and 'A架' in question):
#             api_list_filter = ["compare_device_startup_order"]
#             filtered_tools = [
#                 tool for tool in tools
#                 if tool.get("function", {}).get("name") in api_list_filter
#             ]
#             return question, filtered_tools
#
#     """
#      新加入的逻辑
#     """
#
# #   if ('运行时长' in question and '开机时长' in question and
# #        '相比' in question and ('长多少' in question or '哪个长' in question)):"
#     if ('运行时长' in question and '开机时长' in question and
#             '相比' in question ):
#         api_list_filter = ["compare_operation_durations"]
#         filtered_tools = [
#             tool for tool in tools
#             if tool.get("function", {}).get("name") in api_list_filter
#         ]
#         return question, filtered_tools
#
#     """
#       新加入的逻辑
#     """
#     # 新增：时间范围动作查询
#     # if re.search(r'\d{1,2}:\d{1,2}\s*[~～]\s*\d{1,2}:\d{1,2}.*[发生|动作]', question):
#     #     api_list_filter = ["get_device_status_by_time_range"]
#     #     # 确保答案格式正确
#     #     question = question + "动作直接引用不要修改,如【A架摆回】"
#     #     return question, [tool for tool in tools
#     #                     if tool.get("function", {}).get("name") in api_list_filter]
#
#     # 新增：最后状态查询
#     if "最后一次" in question and ("落座" in question or "关机" in question):
#         api_list_filter = ["get_device_status_by_time_range"]
#         return question, [tool for tool in tools
#                         if tool.get("function", {}).get("name") in api_list_filter]
#
#     # 新增：状态时间点查询
#     time_point_keywords = ["开机", "入水", "解除", "摆回", "摆出"]
#     if "XX:XX输出" in question and any(keyword in question for keyword in time_point_keywords):
#         api_list_filter = ["get_device_status_by_time_range"]
#         return question, [tool for tool in tools
#                         if tool.get("function", {}).get("name") in api_list_filter]
#
#
#     # 第一部分：直接匹配关键词
#     if "甲板机械设备" in question and "能耗" in question:
#         # 如果问题包含"甲板机械设备"和"能耗"这两个关键词
#         api_list_filter = ["calculate_total_deck_machinery_energy"]
#
#     elif "总能耗" in question:
#         # 如果问题包含"总能耗"关键词
#         api_list_filter = ["calculate_total_energy"]
#
#     elif "动作" in question:
#         # 如果问题包含"动作"关键词
#         api_list_filter = ["get_device_status_by_time_range"]
#         # 补充问题说明，确保答案格式正确
#         question = question + "动作直接引用不要修改,如【A架摆回】"
#
#     elif "开机时长" in question:
#         # 如果问题包含"开机时长"关键词
#         api_list_filter = ["calculate_uptime"]
#         if "运行时长" in question:
#             # 如果同时包含"运行时长"，将其替换为"开机时长"
#             question = question.replace("运行时长", "开机时长")
#
#     elif "运行时长" in question and "实际运行时长" not in question:
#         # 如果包含"运行时长"但不包含"实际运行时长"
#         api_list_filter = ["calculate_uptime"]
#         question = question.replace("运行时长", "开机时长")
#
#
#
#     else:
#         # 如果没有匹配到上述任何关键词，则根据表名选择API
#         # 调用choose_table函数获取相关表名
#         table_name_string = choose_table(question)#用大模型选择表名，表名不一定只有一个
#
#         # 读取数据表映射信息
#         with open("dict.json", "r", encoding="utf-8") as file:
#             table_data = json.load(file)
#
#         # 查找匹配的表名
#         table_name = [
#             item for item in table_data
#             if item["数据表名"] in table_name_string
#         ]
#
#         # 根据表名选择合适的API
#         if "设备参数详情表" in [item["数据表名"] for item in table_name]:
#             api_list_filter = ["query_device_parameter"]
#             content_p_1 = str(table_name) + question
#         else:
#             api_list_filter = ["get_table_data"]
#             content_p_1 = str(table_name) + question
#
#     # 根据选择的API过滤工具列表
#     filtered_tools = [
#         tool for tool in tools
#         if tool.get("function", {}).get("name") in api_list_filter
#     ]
#
#     # 返回处理结果
#     if "content_p_1" in locals():
#         return content_p_1, filtered_tools
#     else:
#         return question, filtered_tools

def enhanced(prompt, context=None, instructions=None, modifiers=None):
    """
    增强提示词函数
    """
    enhanced_prompt = prompt.replace("XX小时XX分钟", "XX小时XX分钟，01小时01分钟格式")
    enhanced_prompt = prompt.replace(
        "发生了什么", "什么设备在进行什么动作，动作直接引用不要修改,如【A架摆回】"
    )
    return enhanced_prompt


def run_conversation_xietong(question):
    """
    处理对话的主要函数
    """
    # 1. 增强问题的表述
    question = enhanced(question)

    # 2. 根据问题选择合适的API和工具
    content_p_1, filtered_tool = select_api_based_on_question(
        question,
        tools.tools_all
    )

    # 3. 获取答案
    answer, select_result = get_answer_2(
        question=content_p_1,
        tools=filtered_tool,
        api_look=False
    )

    return answer


def get_answer(question):
    """
    主要的答案获取函数
    例如问题：在2024年8月24日，小艇最后一次落座是什么时候（请以XX:XX输出）？
    """
    # try:
        # 运行对话流程获取答案
    last_answer = run_conversation_xietong(question)
        # 移除答案中的空格
    print(last_answer)
    last_answer = last_answer.replace(" ", "")
    return last_answer
    # except Exception as e:
    #     print(f"Error occurred while executing get_answer: {e}")
    #     return "An error occurred while retrieving the answer."


# In[7]:


# if __name__ == "__main__":
#     question = "在2024年8月24日，小艇最后一次落座是什么时候（请以XX:XX输出）？"
#     question = "在2024年8月24日，A架第二次开机是什么时候（请以XX:XX输出）？"
#     question = "统计2024/8/23上午A架的运行时长（以整数分钟输出）？"
#     question = "24年8月27日下午17点16分发生了什么？"
#     question = "2024/8/23 19:05什么设备在进行什么动作？"
#     aa = get_answer(question)
#     print("*******************最终答案***********************")
#     print(aa)
#     # 文件路径
#     """
#     question_path = "assets/question.jsonl"
#     result_path = "./result.jsonl"
#     intermediate_result_path = "./result_zj.jsonl"
#     # 读取问题文件
#     with open(question_path, "r", encoding="utf-8") as f:
#         questions = [json.loads(line.strip()) for line in f]
#     # 处理每个问题并保存结果
#     questions=questions[:1] # 注释掉这一行以逐个回答全部问题
#     results = []
#     for question in questions:
#         query = question["question"]
#         # 调用AI模块获取答案
#         try:
#             answer =get_answer(question=query)
#             answer_str = str(answer)
#             print(f"Question: {query}")
#             print(f"Answer: {answer_str}")
#             result = {
#                 "id": question["id"],
#                 "question": query,
#                 "answer": answer_str
#             }
#             results.append(result)
#             # 将中间结果写入文件
#             with open(intermediate_result_path, "w", encoding="utf-8") as f:
#                 f.write("\n".join([json.dumps(res, ensure_ascii=False) for res in results]))
#         except Exception as e:
#             print(f"Error processing question {question['id']}: {e}")
#     # 将最终结果写入文件
#     with open(result_path, "w", encoding="utf-8") as f:
#         f.write("\n".join([json.dumps(res, ensure_ascii=False) for res in results]))
#
# """
