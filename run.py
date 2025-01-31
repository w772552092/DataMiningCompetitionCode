# 导入需要的Python库
import json  # 用于处理JSON格式的数据
import concurrent.futures as cf  # 用于并行处理任务
import ai_brain  # 导入我们自定义的AI处理模块
import time  # 用于计时功能


def process_one(question_json):
    """
    处理单个问题的函数
    参数 question_json: 包含问题信息的JSON对象，格式为：
    {
        "id": "问题ID",
        "question": "问题内容"
    }
    """
    # 从输入的JSON对象中获取数据
    line = question_json
    query = line["question"]  # 获取问题内容

    try:
        # 打印正在处理的问题信息
        print(f"Processing question ID {line['id']}: {query}")

        # 使用AI模块获取答案
        answer = ai_brain.get_answer(question=query)
        ans = str(answer)  # 将答案转换为字符串

        # 打印答案信息
        print(f"Answer for question ID {line['id']}: {ans}")

        # 返回包含问题ID、问题内容和答案的字典
        return {
            "id": line["id"],
            "question": query,
            "answer": ans
        }

    except Exception as e:
        # 如果处理过程中出现错误，打印错误信息
        print(f"Error processing question ID {line['id']}: {e}")
        # 返回包含错误信息的字典
        return {
            "id": line["id"],
            "question": query,
            "answer": "Error: " + str(e)
        }


def main():
    """
    主函数，处理所有问题
    """
    # 定义输入和输出文件路径
    q_path = "../../assets/question.jsonl"  # 问题文件路径
    result_path = "result.jsonl"  # 结果保存路径
    result_json_list = []  # 用于存储所有处理结果的列表

    # 读取问题文件
    with open(q_path, "r", encoding="utf-8") as f:
        # 读取每一行并转换为JSON对象，存入列表
        q_json_list = [json.loads(line.strip()) for line in f]

    # 使用线程池并行处理问题
    # max_workers=20 表示最多同时运行20个线程
    with cf.ThreadPoolExecutor(max_workers=20) as executor:
        # 为每个问题创建一个任务
        future_list = [executor.submit(process_one, q_json)
                       for q_json in q_json_list]

        # 当每个任务完成时，将结果添加到结果列表中
        for future in cf.as_completed(future_list):
            result_json_list.append(future.result())

    # 按问题ID排序结果
    result_json_list.sort(key=lambda x: x["id"])

    # 将结果写入文件
    with open(result_path, "w", encoding="utf-8") as f:
        for result in result_json_list:
            # 将每个结果转换为JSON格式并写入文件
            f.write(json.dumps(result, ensure_ascii=False) + "\n")


# 当直接运行此文件时执行的代码
if __name__ == "__main__":
    # 记录开始时间
    start_time = time.time()

    # 运行主函数
    main()

    # 记录结束时间
    end_time = time.time()

    # 计算程序运行时间（转换为分钟）
    elapsed_time = end_time - start_time
    elapsed_time_minutes = elapsed_time / 60

    # 打印运行时间
    print(f"程序运行时间: {elapsed_time_minutes:.2f} 分钟")