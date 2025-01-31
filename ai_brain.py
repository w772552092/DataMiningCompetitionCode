import json
from zhipuai import ZhipuAI
import tools
import api
import os

# api_key = '299012e2ce9e47b2abd5a6d1175bc309.CZ22MvpCGSWt4HGs' #老师的key
api_key = '6c8e45677f8d416689a1477d45b92ef2.xKiTCLH2whdkqCfz'
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
}


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

    try:
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

    except Exception as e:
        # 错误处理
        print(f"Error generating answer for question: {question}, {e}")
        return None, None

import re
# In[6]:
def select_api_based_on_question(question, tools):
    """
    根据问题的内容选择合适的 API 工具
    参数:
    question: 用户的问题文本
    tools: 可用的工具列表
    返回:
    content_p_1: 处理后的问题内容
    filtered_tool: 过滤后的工具列表

    """
    # 在select_api_based_on_question函数的开头添加
    dp_keywords = [
        "深海作业A作业开始",
        "深海作业A作业结束",
        "平均作业时长"
    ]

    is_dp_question = any(keyword in question for keyword in dp_keywords)

    if is_dp_question:
        api_list_filter = ["get_operation_start_time"]
        # 使用原有格式
        content_p_1 = question

        # 过滤工具
        filtered_tools = [
            tool for tool in tools
            if tool.get("function", {}).get("name") in api_list_filter
        ]

        return content_p_1, filtered_tools


    # 新增：时间范围动作查询
    if re.search(r'\d{1,2}:\d{1,2}\s*[~～]\s*\d{1,2}:\d{1,2}.*[发生|动作]', question):
        api_list_filter = ["get_device_status_by_time_range"]
        # 确保答案格式正确
        question = question + "动作直接引用不要修改,如【A架摆回】"
        return question, [tool for tool in tools
                        if tool.get("function", {}).get("name") in api_list_filter]

    # 新增：最后状态查询
    if "最后一次" in question and ("落座" in question or "关机" in question):
        api_list_filter = ["get_device_status_by_time_range"]
        return question, [tool for tool in tools
                        if tool.get("function", {}).get("name") in api_list_filter]

    # 新增：状态时间点查询
    time_point_keywords = ["开机", "入水", "解除", "摆回", "摆出"]
    if "XX:XX输出" in question and any(keyword in question for keyword in time_point_keywords):
        api_list_filter = ["get_device_status_by_time_range"]
        return question, [tool for tool in tools
                        if tool.get("function", {}).get("name") in api_list_filter]


    # 第一部分：直接匹配关键词
    if "甲板机械设备" in question and "能耗" in question:
        # 如果问题包含"甲板机械设备"和"能耗"这两个关键词
        api_list_filter = ["calculate_total_deck_machinery_energy"]

    elif "总能耗" in question:
        # 如果问题包含"总能耗"关键词
        api_list_filter = ["calculate_total_energy"]

    elif "动作" in question:
        # 如果问题包含"动作"关键词
        api_list_filter = ["get_device_status_by_time_range"]
        # 补充问题说明，确保答案格式正确
        question = question + "动作直接引用不要修改,如【A架摆回】"

    elif "开机时长" in question:
        # 如果问题包含"开机时长"关键词
        api_list_filter = ["calculate_uptime"]
        if "运行时长" in question:
            # 如果同时包含"运行时长"，将其替换为"开机时长"
            question = question.replace("运行时长", "开机时长")

    elif "运行时长" in question and "实际运行时长" not in question:
        # 如果包含"运行时长"但不包含"实际运行时长"
        api_list_filter = ["calculate_uptime"]
        question = question.replace("运行时长", "开机时长")



    else:
        # 如果没有匹配到上述任何关键词，则根据表名选择API
        # 调用choose_table函数获取相关表名
        table_name_string = choose_table(question)#用大模型选择表名，表名不一定只有一个

        # 读取数据表映射信息
        with open("dict.json", "r", encoding="utf-8") as file:
            table_data = json.load(file)

        # 查找匹配的表名
        table_name = [
            item for item in table_data
            if item["数据表名"] in table_name_string
        ]

        # 根据表名选择合适的API
        if "设备参数详情表" in [item["数据表名"] for item in table_name]:
            api_list_filter = ["query_device_parameter"]
            content_p_1 = str(table_name) + question
        else:
            api_list_filter = ["get_table_data"]
            content_p_1 = str(table_name) + question

    # 根据选择的API过滤工具列表
    filtered_tools = [
        tool for tool in tools
        if tool.get("function", {}).get("name") in api_list_filter
    ]

    # 返回处理结果
    if "content_p_1" in locals():
        return content_p_1, filtered_tools
    else:
        return question, filtered_tools

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
    try:
        # 运行对话流程获取答案
        last_answer = run_conversation_xietong(question)
        # 移除答案中的空格
        last_answer = last_answer.replace(" ", "")
        return last_answer
    except Exception as e:
        print(f"Error occurred while executing get_answer: {e}")
        return "An error occurred while retrieving the answer."


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
