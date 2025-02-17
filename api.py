import pandas as pd

def calculate_uptime(start_time, end_time, shebeiname="折臂吊车"):
    """
    计算指定时间段内的开机时长，并返回三种格式的开机时长
    :param start_time: 查询的开始时间（字符串或 datetime 类型）
    :param end_time: 查询的结束时间（字符串或 datetime 类型）
    :param shebeiname: 设备名称，默认为 '折臂吊车'
    :return: 包含三种格式开机时长的字符串
    """
    print("-------calculate_uptime执行***计算开机时间-------")
    # 设备配置映射：设备名称 -> (文件路径, 开机状态, 关机状态)
    device_config = {
        "折臂吊车": (
            "database_in_use/device_13_11_meter_1311.csv",
            "折臂吊车开机",
            "折臂吊车关机",
        ),
        "A架": ("database_in_use/Ajia_plc_1.csv", "开机", "关机"),
        "DP": ("database_in_use/Port3_ksbg_9.csv", "ON_DP", "OFF_DP"),
    }

    # 检查设备名称是否有效
    if shebeiname not in device_config:
        raise ValueError(f"未知的设备名称: {shebeiname}")

    # 获取设备配置
    file_path, start_status, end_status = device_config[shebeiname]

    # 读取 CSV 文件
    df = pd.read_csv(file_path)

    # 将时间列转换为 datetime 类型
    df["csvTime"] = pd.to_datetime(df["csvTime"])

    # 将传入的开始时间和结束时间转换为 datetime 类型
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)

    # 筛选出指定时间段内的数据
    df_filtered = df[(df["csvTime"] >= start_time) & (df["csvTime"] <= end_time)]

    # 初始化变量
    total_duration = pd.Timedelta(0)
    start_uptime = None

    # 遍历筛选后的数据
    for index, row in df_filtered.iterrows():
        if row["status"] == start_status:
            start_uptime = row["csvTime"]
        elif row["status"] == end_status and start_uptime is not None:
            end_uptime = row["csvTime"]
            total_duration += end_uptime - start_uptime
            start_uptime = None

    # 计算三种格式的开机时长
    seconds = total_duration.total_seconds()
    minutes = int(seconds / 60)
    hours = int(seconds // 3600)
    remaining_minutes = int((seconds % 3600) // 60)

    # 将小时和分钟格式化为两位数
    hours_str = f"{hours:02d}"  # 使用格式化字符串确保两位数
    minutes_str = f"{remaining_minutes:02d}"  # 使用格式化字符串确保两位数

    # 返回三种格式的开机时长
    result = {
        "function": "calculate_uptime",  # 说明这个返回结果来自哪个函数
        "result": (
            # f'开机时长：{seconds}秒',
            f"开机时长：{minutes}分钟",
            # f'开机时长：{hours_str}小时{minutes_str}分钟'
        ),
    }
    return result


def compute_operational_duration(start_time, end_time, device_name="A架"):
    # 设备配置映射：设备名称 -> (文件路径, 开机状态, 关机状态)
    print("-------compute_operational_duration执行-------")
    device_config = {
        "A架": ("database_in_use/Ajia_plc_1.csv", "开机", "关机"),
    }
    # 检查设备名称是否有效
    if device_name not in device_config:
        raise ValueError(f"未知的设备名称: {device_name}")

    # 获取设备配置
    file_path, start_status, end_status = device_config[device_name]

    # 读取 CSV 文件
    df = pd.read_csv(file_path)

    # 将时间列转换为 datetime 类型
    df["csvTime"] = pd.to_datetime(df["csvTime"])

    # 将传入的开始时间和结束时间转换为 datetime 类型
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)

    # 筛选出指定时间段内的数据
    df_filtered = df[(df["csvTime"] >= start_time) & (df["csvTime"] <= end_time)]

    # 初始化变量
    total_duration = pd.Timedelta(0)
    start_uptime = None
    # 遍历筛选后的数据
    for index, row in df_filtered.iterrows():
        if row["status"] == start_status:
            start_uptime = row["csvTime"]
        elif row["status"] == end_status and start_uptime is not None:
            end_uptime = row["csvTime"]
            total_duration += end_uptime - start_uptime
            start_uptime = None

    # 计算三种格式的开机时长
    seconds = total_duration.total_seconds()
    minutes = int(seconds / 60)
    hours = int(seconds // 3600)
    remaining_minutes = int((seconds % 3600) // 60)

    # 将小时和分钟格式化为两位数
    hours_str = f"{hours:02d}"  # 使用格式化字符串确保两位数
    minutes_str = f"{remaining_minutes:02d}"  # 使用格式化字符串确保两位数

    result = {
        "function": "calculate_uptime",  # 说明这个返回结果来自哪个函数
        "result": (
            # f'运行时长：{seconds}秒',
            f"运行时长：{minutes}分钟",
            # f'运行时长：{hours_str}小时{minutes_str}分钟'
        ),
    }
    return result


def get_table_data(table_name, start_time, end_time, columns=None, status=None):
    """
    根据数据表名、开始时间、结束时间、列名和状态获取指定时间范围内的相关数据。

    参数:
    table_name (str): 数据表名
    start_time (str): 开始时间，格式为 'YYYY-MM-DD HH:MM:SS'
    end_time (str): 结束时间，格式为 'YYYY-MM-DD HH:MM:SS'
    columns (list): 需要查询的列名列表，如果为None，则返回所有列
    status (str): 需要筛选的状态（例如 "开机"、"关机"），如果为None，则不筛选状态

    返回:
    dict: 包含指定列名和对应值的字典，或错误信息
    """
    # 创建一个字典来存储元数据
    metadata = {
        "table_name": table_name,
        "start_time": start_time,
        "end_time": end_time,
        "columns": columns,
        "status": status,
    }

    try:
        df = pd.read_csv(f"database_in_use/{table_name}.csv")
    except FileNotFoundError:
        return {"error": f"数据表 {table_name} 不存在", "metadata": metadata}

    # 将csvTime列从时间戳转换为datetime类型
    df["csvTime"] = pd.to_datetime(df["csvTime"], unit="ns")  # 假设时间戳是纳秒级别

    # 将开始时间和结束时间转换为datetime类型
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)
    # 如果开始时间和结束时间是同一分钟
    if (
            start_time.minute == end_time.minute
            and start_time.hour == end_time.hour
            and start_time.day == end_time.day
    ):
        # 将开始时间设置为这一分钟的00秒
        start_time = start_time.replace(second=0)
        # 将结束时间设置为这一分钟的59秒
        end_time = end_time.replace(second=59)
    # 筛选指定时间范围内的数据
    filtered_data = df[(df["csvTime"] >= start_time) & (df["csvTime"] <= end_time)]

    if filtered_data.empty:
        return {
            "error": f"在数据表 {table_name} 中未找到时间范围 {start_time} 到 {end_time} 的数据",
            "metadata": metadata,
        }

    # 如果传入了 status 参数，则进一步筛选状态
    if status is not None:
        filtered_data = filtered_data[filtered_data["status"] == status]
        if filtered_data.empty:
            return {
                "error": f"在数据表 {table_name} 中未找到状态为 {status} 的数据",
                "metadata": metadata,
            }

    # 如果未指定列名，则返回所有列
    if columns is None:
        columns = filtered_data.columns.tolist()

    # 检查列名是否存在
    missing_columns = [
        column for column in columns if column not in filtered_data.columns
    ]
    if missing_columns:
        return {
            "error": f"列名 {missing_columns} 在数据表 {table_name} 中不存在",
            "metadata": metadata,
        }

    # 获取指定列名和对应的值
    result = {}
    for column in columns:
        if column == "csvTime":
            # 将时间格式化为字符串
            result[column] = (
                filtered_data[column].dt.strftime("%Y-%m-%d %H:%M:%S").tolist()
            )
        else:
            result[column] = filtered_data[column].values.tolist()

    # 返回结果和元数据
    return {"result": result, "metadata": metadata}


# 能耗计算
def load_and_filter_data(file_path, start_time, end_time, power_column):
    """
    加载 CSV 文件并筛选指定时间范围内的数据
    :param file_path: CSV 文件路径
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param power_column: 功率列名
    :return: 筛选后的 DataFrame
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 {file_path} 未找到")

    # 确保时间列是 datetime 类型
    try:
        df["csvTime"] = pd.to_datetime(df["csvTime"])
    except Exception as e:
        raise ValueError(f"时间列转换失败: {e}")

    # 筛选特定时间范围内的数据
    filtered_data = df[
        (df["csvTime"] >= start_time) & (df["csvTime"] < end_time)
        ].copy()

    if filtered_data.empty:
        return None

    # 计算时间差（秒）
    filtered_data.loc[:, "diff_seconds"] = (
        filtered_data["csvTime"].diff().dt.total_seconds().shift(-1)
    )

    print('测试时间差',filtered_data["diff_seconds"])

    # 计算每个时间间隔的能耗（kWh）
    filtered_data.loc[:, "energy_kWh"] = (
            filtered_data["diff_seconds"] * filtered_data[power_column] / 3600
    )

    return filtered_data


def calculate_total_energy(start_time, end_time, device_name="折臂吊车"):
    """
    计算指定时间段内的总能耗
    :param start_time: 查询的开始时间（字符串或 datetime 类型）
    :param end_time: 查询的结束时间（字符串或 datetime 类型）
    :param device_name: 设备名称，默认为 '折臂吊车'
    :return: 总能耗（kWh，float 类型）
    """
    # 设备配置映射：设备名称 -> (表名, 功率列名)
    device_config = {
        "折臂吊车": ("device_13_11_meter_1311", "13-11-6_v"),
        "一号门架": ("device_1_5_meter_105", "1-5-6_v"),  # 一号门架的配置
        "二号门架": ("device_13_14_meter_1314", "13-14-6_v"),  # 二号门架的配置
        "绞车": ("device_1_15_meter_115", "1-15-6_v"),  # 添加绞车的配置
    }

    # 检查设备名称是否有效
    if device_name not in device_config:
        raise ValueError(f"未知的设备名称: {device_name}")

    # 获取设备配置
    table_name, power_column = device_config[device_name]

    # 读取 CSV 文件并计算能耗
    file_path = f"database_in_use/{table_name}.csv"
    try:
        filtered_data = load_and_filter_data(
            file_path, start_time, end_time, power_column
        )
        if filtered_data is None:
            return None
        total_energy_kWh = filtered_data["energy_kWh"].sum()
        return round(total_energy_kWh, 2)
    except Exception as e:
        raise ValueError(f"计算能耗时出错: {e}")


def calculate_total_deck_machinery_energy(start_time, end_time):
    """
    计算所有设备（折臂吊车、一号门架、二号门架、绞车）在指定时间范围内的总能耗
    :param start_time: 查询的开始时间（字符串或 datetime 类型）
    :param end_time: 查询的结束时间（字符串或 datetime 类型）
    :return: 所有设备的总能耗（kWh，float 类型）
    """
    # 定义设备列表
    devices = ["折臂吊车", "一号门架", "二号门架", "绞车"]

    total_energy = 0  # 初始化总能耗

    # 遍历每个设备，计算能耗并累加
    for device in devices:
        try:
            energy = calculate_total_energy(start_time, end_time, device_name=device)
            if energy is not None:
                total_energy += energy
        except Exception as e:
            print(f"计算设备 {device} 能耗时出错: {e}")
    return round(total_energy, 2)  # 返回总能耗，保留两位小数


def calculate_energy_consumption(start_time, end_time):
    """
    计算指定时间范围内的侧推的总能耗
    :param start_time: 开始时间（字符串或 datetime 类型）
    :param end_time: 结束时间（字符串或 datetime 类型）
    :return: 总能耗（kWh，float 类型），如果数据为空则返回 None
    """
    # 文件路径和功率列名直接定义在函数内部
    file_path = "database_in_use/Port3_ksbg_9.csv"
    power_column = "P3_18"  # 使用 "艏推功率反馈,单位:kW" 列

    try:
        # 加载 CSV 文件
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 {file_path} 未找到")

    # 确保时间列是 datetime 类型
    try:
        df["csvTime"] = pd.to_datetime(df["csvTime"])
    except Exception as e:
        raise ValueError(f"时间列转换失败: {e}")

    # 筛选特定时间范围内的数据
    filtered_data = df[
        (df["csvTime"] >= start_time) & (df["csvTime"] < end_time)
        ].copy()

    if filtered_data.empty:
        return None

    # 计算时间差（秒）
    filtered_data.loc[:, "diff_seconds"] = (
        filtered_data["csvTime"].diff().dt.total_seconds().shift(-1)
    )

    # 计算每个时间间隔的能耗（kWh）
    filtered_data.loc[:, "energy_kWh"] = (
            filtered_data["diff_seconds"] * filtered_data[power_column] / 3600
    )

    # 计算总能耗
    total_energy_kWh = filtered_data["energy_kWh"].sum()

    return round(total_energy_kWh, 2)


def query_device_parameter(parameter_name_cn):
    """
    通过参数中文名查询设备参数信息
    :param parameter_name_cn: 参数中文名
    :param device_parameter_file: 设备参数详情表的文件路径，默认为'设备参数详情表.csv'
    :return: 返回包含参数信息的字典
    """
    print("-------query_device_parameter执行-------")
    # 读取设备参数详情表
    df = pd.read_csv("database_in_use/设备参数详情表.csv")

    # 检查参数中文名是否包含在 Channel_Text_CN 列中
    if not df["Channel_Text_CN"].str.contains(parameter_name_cn).any():
        raise ValueError(f"未找到包含 '{parameter_name_cn}' 的参数中文名")

    # 获取包含参数中文名的所有行
    parameter_info = df[df["Channel_Text_CN"].str.contains(parameter_name_cn)].iloc[0]

    # 将参数信息转换为字典
    parameter_dict = {
        "参数名": parameter_info["Channel_Text"],
        "参数中文名": parameter_info["Channel_Text_CN"],
        "参数下限": parameter_info["Alarm_Information_Range_Low"],
        "参数上限": parameter_info["Alarm_Information_Range_High"],
        "报警值的单位": parameter_info["Alarm_Information_Unit"],
        "报警值": parameter_info["Parameter_Information_Alarm"],
        "屏蔽值": parameter_info["Parameter_Information_Inhibit"],
        "延迟值": parameter_info["Parameter_Information_Delayed"],
        "安全保护设定值": parameter_info["Safety_Protection_Set_Value"],
        "附注": parameter_info["Remarks"],
    }
    return parameter_dict


def calculate_total_energy_consumption(start_time, end_time, query_type="all"):
    """
    计算指定时间范围内两个推进变频器或推进系统的总能耗
    :param start_time: 开始时间（字符串或 datetime 类型）
    :param end_time: 结束时间（字符串或 datetime 类型）
    :param query_type: 查询类型，可选值为 '1'（一号推进）、'2'（二号推进）、'all'（整个推进系统）
    :return: 总能耗（kWh，float 类型），如果数据为空则返回 None
    """
    # 文件路径和功率列名
    file_path_1 = "database_in_use/Port3_ksbg_8.csv"
    power_column_1 = "P3_15"  # 一号推进变频器功率反馈,单位:kW

    file_path_2 = "database_in_use/Port4_ksbg_7.csv"
    power_column_2 = "P4_15"  # 二号推进变频器功率反馈,单位:kW
    try:
        # 加载 CSV 文件
        df1 = pd.read_csv(file_path_1)
        df2 = pd.read_csv(file_path_2)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"文件未找到: {e}")

    # 确保时间列是 datetime 类型
    try:
        df1["csvTime"] = pd.to_datetime(df1["csvTime"])
        df2["csvTime"] = pd.to_datetime(df2["csvTime"])
    except Exception as e:
        raise ValueError(f"时间列转换失败: {e}")

    # 筛选特定时间范围内的数据
    filtered_data_1 = df1[
        (df1["csvTime"] >= start_time) & (df1["csvTime"] < end_time)
        ].copy()
    filtered_data_2 = df2[
        (df2["csvTime"] >= start_time) & (df2["csvTime"] < end_time)
        ].copy()

    if filtered_data_1.empty or filtered_data_2.empty:
        return None

    # 计算时间差（秒）
    filtered_data_1.loc[:, "diff_seconds"] = (
        filtered_data_1["csvTime"].diff().dt.total_seconds().shift(-1)
    )
    filtered_data_2.loc[:, "diff_seconds"] = (
        filtered_data_2["csvTime"].diff().dt.total_seconds().shift(-1)
    )

    # 计算每个时间间隔的能耗（kWh）
    filtered_data_1.loc[:, "energy_kWh"] = (
            filtered_data_1["diff_seconds"] * filtered_data_1[power_column_1] / 3600
    )
    filtered_data_2.loc[:, "energy_kWh"] = (
            filtered_data_2["diff_seconds"] * filtered_data_2[power_column_2] / 3600
    )

    # 计算总能耗
    total_energy_kWh_1 = filtered_data_1["energy_kWh"].sum()
    total_energy_kWh_2 = filtered_data_2["energy_kWh"].sum()

    # 根据查询类型返回相应的能耗
    if query_type == "1":
        return round(total_energy_kWh_1, 2)
    elif query_type == "2":
        return round(total_energy_kWh_2, 2)
    elif query_type == "all":
        return round(total_energy_kWh_1 + total_energy_kWh_2, 2)
    else:
        raise ValueError("query_type 参数无效，请输入 '1'、'2' 或 'all'")



def get_device_status_by_time_range(start_time, end_time):
    """
    根据数据表名、开始时间和结束时间，查询设备在该时间段内的状态变化，并排除 status 为 'False' 的记录。
    参数:
    start_time (str): 开始时间，格式为 'YYYY-MM-DD HH:MM:SS'
    end_time (str): 结束时间，格式为 'YYYY-MM-DD HH:MM:SS'

    返回:
    dict: 包含设备状态变化的时间点和对应状态的字典，或错误信息
    """

    def get_status_changes(table_name, device_name):
        """
        辅助函数：获取指定设备在指定时间范围内的状态变化。

        参数:
        table_name (str): 数据表名
        device_name (str): 设备名称

        返回:
        dict: 包含设备状态变化的时间点和对应状态的字典，或错误信息
        """
        metadata = {
            "table_name": table_name,
            "start_time": start_time,
            "end_time": end_time,
        }

        try:
            df = pd.read_csv(f"database_in_use/{table_name}.csv")
        except FileNotFoundError:
            return {"error": f"数据表 {table_name} 不存在", "metadata": metadata}

        # 将csvTime列从时间戳转换为datetime类型
        df["csvTime"] = pd.to_datetime(df["csvTime"], unit="ns")  # 假设时间戳是纳秒级别

        # 将开始时间和结束时间转换为datetime类型
        start_time_dt = pd.to_datetime(start_time)
        end_time_dt = pd.to_datetime(end_time)

        # 筛选指定时间范围内的数据，并排除 status 为 'False' 的记录
        filtered_data = df[
            (df["csvTime"] >= start_time_dt)
            & (df["csvTime"] <= end_time_dt)
            & (df["status"] != "False")
            ]

        if filtered_data.empty:
            return {
                "error": f"在数据表 {table_name} 中未找到时间范围 {start_time} 到 {end_time} 且 status 不为 'False' 的数据",
                "metadata": metadata,
            }

        # 检查是否存在status列
        if "status" not in filtered_data.columns:
            return {
                "error": f"数据表 {table_name} 中不存在 'status' 列",
                "metadata": metadata,
            }

        # 获取设备状态变化的时间点和对应状态
        status_changes = filtered_data[
            ["csvTime", "status"]
        ].copy()  # 显式创建副本以避免警告

        # 使用 .loc 避免 SettingWithCopyWarning
        status_changes.loc[:, "csvTime"] = status_changes["csvTime"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # 将结果转换为字典
        return {
            "设备名称": device_name,
            "正在进行的关键动作": status_changes.to_dict(orient="records"),
        }

    # 获取三个设备的状态变化
    result1 = get_status_changes("Ajia_plc_1", "A架")
    result2 = get_status_changes("device_13_11_meter_1311", "折臂吊车")
    result3 = get_status_changes("Port3_ksbg_9", "定位设备")

    # 过滤掉包含错误的结果
    results = [
        result for result in [result1, result2, result3] if "error" not in result
    ]

    # 返回结果和元数据
    return {
        "result": results,
        "metadata": {"start_time": start_time, "end_time": end_time},
    }


def get_operation_start_time(target_date):
    """
    获取指定日期深海作业A的开始时间

    参数:
    target_date (str): 目标日期，格式为 'YYYY/MM/DD'

    返回:
    str: 深海作业A开始的时间 (HH:MM 格式)，如果没有找到则返回 None
    """
    import pandas as pd
    from datetime import datetime

    try:
        # 读取CSV文件
        df = pd.read_csv('database_in_use/Port3_ksbg_9.csv')

        # 将csvTime转换为datetime类型
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 将目标日期转换为datetime对象
        target_date = datetime.strptime(target_date, '%Y/%m/%d').date()

        # 过滤指定日期的数据
        daily_data = df[df['csvTime'].dt.date == target_date]

        if daily_data.empty:
            return None

        # 找到该日期第一次ON_DP的时间
        start_time = daily_data[daily_data['status'] == 'ON_DP']['csvTime'].iloc[0]

        # 返回格式化的时间字符串 (HH:MM)
        return start_time.strftime('%H:%M')

    except Exception as e:
        print(f"Error in get_operation_start_time: {e}")
        return None

#新加入的代码
def calculate_efficiency(start_time, end_time, device_name='A架'):
    """
    计算设备效率
    """
    print("-------calculate_efficiency执行***计算效率-------")
    try:
        # 计算开机时长
        uptime_data = calculate_uptime(start_time, end_time, device_name)
        uptime_minutes = _extract_duration_minutes(uptime_data)

        # 计算实际运行时长
        operation_data = compute_operational_duration(start_time, end_time, device_name)
        operation_minutes = _extract_duration_minutes(operation_data)

        if uptime_minutes == 0:
            return {
                "function": "calculate_efficiency",
                "result": (
                    f"实际运行时长：0分钟",
                    f"效率：0.00%"
                ),
            }

        # 计算效率
        efficiency = (operation_minutes / uptime_minutes) * 100

        return {
            "function": "calculate_efficiency",
            "result": (
                f"实际运行时长：{operation_minutes}分钟",
                f"效率：{efficiency:.2f}%"
            ),
        }

    except Exception as e:
        print(f"Error calculating efficiency: {e}")
        return None

import re
def _extract_duration_minutes(time_result):
    """从时间结果中提取分钟数"""
    try:
        if isinstance(time_result, dict) and 'result' in time_result:
            time_str = time_result['result'][0]
            match = re.search(r'(\d+)分钟', time_str)
            if match:
                return int(match.group(1))
        return 0
    except Exception:
        return 0

#新加入的代码
from datetime import datetime
def get_operation_end_time(target_date):
    """
    获取指定日期深海作业A的结束时间
    以征服者落座为标志

    Args:
        target_date (str): 目标日期，格式为 'YYYY/MM/DD'
    Returns:
        str or None: 结束时间 (HH:MM 格式)
    """
    try:
        # 读取A架的数据文件
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')

        # 将时间列转换为datetime类型
        df['csvTime'] = pd.to_datetime(df['csvTime'])
        # 将目标日期转换为datetime对象
        target_date = datetime.strptime(target_date, '%Y/%m/%d').date()

        # 筛选指定日期且状态为"征服者落座"的数据
        daily_data = df[
            (df['csvTime'].dt.date == target_date) &
            (df['status'] == '征服者落座')
            ]

        if daily_data.empty:
            return None

        # 获取征服者落座的时间点
        end_time = daily_data['csvTime'].iloc[-1]  # 取最后一次落座时间

        # 返回格式化的时间字符串 (HH:MM)
        return end_time.strftime('%H:%M')

    except Exception as e:
        print(f"Error in get_operation_end_time: {e}")
        return None

#新加入的代码
def compare_device_startup_order(date, period='afternoon'):
    """
    比较两个设备开机时间的先后顺序

    Args:
        date (str): 日期，格式为'YYYY/MM/DD'
        period (str): 时间段，'morning'或'afternoon'
    Returns:
        bool or None: True表示A架先开机，False表示折臂吊车先开机，None表示无法判断
    """
    try:
        # 读取A架数据
        ajia_df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
        ajia_df['csvTime'] = pd.to_datetime(ajia_df['csvTime'])

        # 读取折臂吊车数据
        crane_df = pd.read_csv('database_in_use/device_13_11_meter_1311.csv')
        crane_df['csvTime'] = pd.to_datetime(crane_df['csvTime'])

        # 将日期转换为datetime
        target_date = pd.to_datetime(date).date()

        # 设置时间范围（下午12:00-23:59）
        start_time = pd.to_datetime(f"{date} 12:00:00")
        end_time = pd.to_datetime(f"{date} 23:59:59")

        # 筛选A架开机数据
        ajia_startup = ajia_df[
            (ajia_df['csvTime'] >= start_time) &
            (ajia_df['csvTime'] <= end_time) &
            (ajia_df['status'] == '开机')
            ]

        # 筛选折臂吊车开机数据
        crane_startup = crane_df[
            (crane_df['csvTime'] >= start_time) &
            (crane_df['csvTime'] <= end_time) &
            (crane_df['status'] == '折臂吊车开机')
            ]

        # 如果任一设备没有开机记录，返回None
        if ajia_startup.empty or crane_startup.empty:
            return None

        # 获取各自最早的开机时间
        ajia_time = ajia_startup['csvTime'].iloc[0]
        crane_time = crane_startup['csvTime'].iloc[0]

        # 返回时间比较结果
        return {
            "function": "compare_device_startup_order",
            "result": {
                "is_ajia_first": ajia_time < crane_time,
                "ajia_time": ajia_time.strftime("%H:%M:%S"),
                "crane_time": crane_time.strftime("%H:%M:%S")
            }
        }

    except Exception as e:
        print(f"Error comparing startup order: {e}")
        return None

#新加入的代码
def compare_operation_durations(date):
    """
    比较指定日期上午A架运行时长和下午开机时长

    Args:
        date (str): 目标日期，格式为 'YYYY/MM/DD'
    Returns:
        dict: 包含比较结果的字典
    """
    try:
        # 构造上午和下午的时间范围
        morning_start = f"{date} 00:00:00"
        morning_end = f"{date} 12:00:00"
        afternoon_start = f"{date} 12:00:00"
        afternoon_end = f"{date} 23:59:59"

        # 计算上午运行时长
        morning_duration = compute_operational_duration(
            morning_start,
            morning_end,
            device_name="A架"
        )

        # 计算下午开机时长
        afternoon_duration = calculate_uptime(
            afternoon_start,
            afternoon_end,
            shebeiname="A架"
        )

        # 提取时长数值（假设返回格式为 "运行时长：XX分钟" 或 "开机时长：XX分钟"）
        morning_minutes = int(re.search(r'(\d+)分钟', morning_duration['result'][0]).group(1))
        afternoon_minutes = int(re.search(r'(\d+)分钟', afternoon_duration['result'][0]).group(1))

        # 计算差值
        diff = abs(morning_minutes - afternoon_minutes)

        return {
            "function": "compare_operation_durations",
            "result": {
                "morning_duration": morning_minutes,
                "afternoon_duration": afternoon_minutes,
                "difference": diff,
                "longer": "上午" if morning_minutes > afternoon_minutes else "下午"
            }
        }

    except Exception as e:
        print(f"Error comparing durations: {e}")
        return None

#新加入的代码

def calculate_action_time_diff(date, action1, action2):
    """
    计算同一天内两个设备动作之间的时间差

    Args:
        date (str): 日期，格式为'YYYY/MM/DD'
        action1 (str): 第一个动作名称
        action2 (str): 第二个动作名称
    Returns:
        int or None: 两个动作之间的时间差(分钟)，如果找不到则返回None
    """
    try:
        # 读取A架数据
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')

        # 转换时间列
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 构造目标日期范围
        target_date = pd.to_datetime(date).date()
        start_time = pd.to_datetime(f"{date} 00:00:00")
        end_time = pd.to_datetime(f"{date} 23:59:59")

        # 筛选当天数据
        daily_data = df[
            (df['csvTime'] >= start_time) &
            (df['csvTime'] <= end_time)
            ]

        # 查找两个动作的时间点
        action1_time = daily_data[daily_data['status'] == action1]['csvTime'].iloc[0]
        action2_time = daily_data[daily_data['status'] == action2]['csvTime'].iloc[0]

        if action1_time is None or action2_time is None:
            return None

        # 计算时间差（分钟）
        time_diff = int(abs((action2_time - action1_time).total_seconds() / 60))

        return {
            "function": "calculate_action_time_diff",
            "result": time_diff
        }

    except Exception as e:
        print(f"Error calculating action time difference: {e}")
        return None

#新加入的代码

def find_longest_morning_operation(start_date, end_date, device_name="A架"):
    """
    查找指定日期范围内上午运行时长最长的一天

    Args:
        start_date (str): 起始日期，格式 'YYYY/MM/DD'
        end_date (str): 结束日期，格式 'YYYY/MM/DD'
        device_name (str): 设备名称，默认为"A架"
    Returns:
        dict: 包含最长运行时间的日期和时长
    """
    try:
        # 转换日期格式
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        date_range = pd.date_range(start, end)

        # 存储每天的运行时长
        daily_durations = {}

        # 计算每天上午的运行时长
        for date in date_range:
            morning_start = date.strftime('%Y-%m-%d 00:00:00')
            morning_end = date.strftime('%Y-%m-%d 12:00:00')

            # 调用现有的运行时长计算函数
            duration_result = calculate_uptime(
                morning_start,
                morning_end,
                shebeiname=device_name
            )

            # 提取分钟数
            if duration_result and 'result' in duration_result:
                minutes = int(re.search(r'(\d+)分钟', duration_result['result'][0]).group(1))
                daily_durations[date.strftime('%Y/%m/%d')] = minutes

        if not daily_durations:
            return None

        # 找出运行时长最长的一天
        max_date = max(daily_durations.items(), key=lambda x: x[1])

        return {
            "function": "find_longest_morning_operation",
            "result": {
                "date": max_date[0],
                "duration": max_date[1]
            }
        }

    except Exception as e:
        print(f"Error finding longest morning operation: {e}")
        return None


#新加入的代码
def calculate_average_morning_runtime(date1, date2, device_name="A架"):
    """
    计算两个日期上午的平均运行时间

    Args:
        date1 (str): 第一个日期，格式'YYYY/MM/DD'
        date2 (str): 第二个日期，格式'YYYY/MM/DD'
        device_name (str): 设备名称，默认为"A架"
    Returns:
        dict: 包含平均运行时间的结果字典
    """
    try:
        durations = []
        dates = [date1, date2]

        # 计算每天上午的运行时长
        for date in dates:
            morning_start = f"{date} 00:00:00"
            morning_end = f"{date} 12:00:00"

            # 使用现有的计算时长函数
            duration_result = calculate_uptime(
                morning_start,
                morning_end,
                shebeiname=device_name
            )

            # 提取分钟数
            if duration_result and 'result' in duration_result:
                minutes = int(re.search(r'(\d+)分钟', duration_result['result'][0]).group(1))
                durations.append(minutes)

        # 计算平均值并四舍五入
        if durations:
            average_minutes = round(sum(durations) / len(durations))
            return {
                "function": "calculate_average_morning_runtime",
                "result": average_minutes
            }
        return None

    except Exception as e:
        print(f"Error calculating average morning runtime: {e}")
        return None

#新加入的代码
# def calculate_thruster_energy_during_dp(date):
#     """
#     计算特定日期DP过程中侧推(艏推)的总能耗
#
#     Args:
#         date (str): 目标日期，格式'YYYY/MM/DD'
#     Returns:
#         dict: 包含总能耗的结果字典
#     """
#     try:
#         # 读取包含DP状态的数据
#         dp_df = pd.read_csv('database_in_use/Port3_ksbg_9.csv')
#         dp_df['csvTime'] = pd.to_datetime(dp_df['csvTime'])
#
#         # 设置日期范围
#         start_time = pd.to_datetime(f"{date} 00:00:00")
#         end_time = pd.to_datetime(f"{date} 23:59:59")
#
#         # 筛选当天数据
#         daily_data = dp_df[
#             (dp_df['csvTime'] >= start_time) &
#             (dp_df['csvTime'] <= end_time)
#             ]
#
#         # 获取DP开启和关闭的时间点
#         dp_periods = []
#         dp_start = None
#
#         for idx, row in daily_data.iterrows():
#             if row['status'] == 'ON_DP' and dp_start is None:
#                 dp_start = row['csvTime']
#             elif row['status'] == 'OFF_DP' and dp_start is not None:
#                 dp_periods.append((dp_start, row['csvTime']))
#                 dp_start = None
#
#         # 计算每个DP期间的能耗
#         total_energy = 0
#         for start, end in dp_periods:
#             # 提取该时间段内的艏推功率数据
#             period_data = daily_data[
#                 (daily_data['csvTime'] >= start) &
#                 (daily_data['csvTime'] <= end)
#                 ]
#
#             # 计算时间间隔（小时）
#             period_data['time_diff'] = (
#                     period_data['csvTime'].diff().dt.total_seconds() / 3600
#             )
#
#             # 计算能耗 (功率 * 时间)
#             # P3_18是艏推功率反馈
#             period_energy = (
#                     period_data['P3_18'] * period_data['time_diff']
#             ).sum()
#
#             total_energy += period_energy
#
#         return {
#             "function": "calculate_thruster_energy_during_dp",
#             "result": round(total_energy, 2)
#         }
#
#     except Exception as e:
#         print(f"Error calculating thruster energy: {e}")
#         return None

#新加入的代码

# def calculate_thruster_energy_during_dp(date):
#     """
#     计算特定日期第一个DP周期内的侧推(艏推)总能耗
#     通过status字段识别DP状态,在周期内累加所有时间点的能耗
#
#     Args:
#         date (str): 目标日期，格式'YYYY/MM/DD'
#     Returns:
#         float: 总能耗(kWh)，保留2位小数
#     """
#     try:
#         # 读取数据
#         df = pd.read_csv('database_in_use/Port3_ksbg_9.csv')
#         df['csvTime'] = pd.to_datetime(df['csvTime'])
#
#         # 筛选当天数据
#         daily_data = df[df['csvTime'].dt.date == pd.to_datetime(date).date()]
#
#         # 找到第一个DP周期的起止索引
#         start_idx = daily_data[daily_data['status'] == 'ON_DP'].index[0]
#         end_idx = daily_data[daily_data['status'] == 'OFF_DP'].index[0]
#
#         # 获取DP周期内的所有数据
#         dp_period = daily_data.loc[start_idx:end_idx].copy()
#
#         # 计算时间差（小时）
#         dp_period['time_diff'] = dp_period['csvTime'].diff().dt.total_seconds() / 3600
#
#         # 计算能耗: 当前功率 * 到下一时刻的时间差
#         total_energy = (dp_period['P3_18'] * dp_period['time_diff']).sum()
#
#         return {
#              "function": "calculate_thruster_energy_during_dp",
#              "result": round(total_energy, 2)
#         }
#
#     except Exception as e:
#         print(f"计算能耗错误: {str(e)}")
#         raise


def calculate_thruster_energy_during_dp(date):
    """
    计算特定日期第一个DP周期内的侧推(艏推)总能耗
    ON DP判定: P3_33/P3_18数值从0增加
    OFF DP判定: P3_33/P3_18数值归零
    只计算当天第一次ON DP到OFF DP的时间段

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含函数名和计算结果的字典
    """
    try:
        # 读取数据
        df = pd.read_csv('database_in_use/Port3_ksbg_9.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 筛选当天数据
        daily_data = df[df['csvTime'].dt.date == pd.to_datetime(date).date()].copy()
        daily_data = daily_data.sort_values('csvTime').reset_index(drop=True)

        # 找到第一次ON DP的索引
        for i in range(len(daily_data) - 1):
            if (daily_data.iloc[i]['P3_18'] == 0 and daily_data.iloc[i]['P3_33'] == 0) and \
                    (daily_data.iloc[i + 1]['P3_18'] > 0 or daily_data.iloc[i + 1]['P3_33'] > 0):
                start_idx = i + 1
                break

        # 找到对应的第一次OFF DP的索引
        for i in range(start_idx, len(daily_data) - 1):
            if (daily_data.iloc[i]['P3_18'] > 0 or daily_data.iloc[i]['P3_33'] > 0) and \
                    (daily_data.iloc[i + 1]['P3_18'] == 0 and daily_data.iloc[i + 1]['P3_33'] == 0):
                end_idx = i + 1
                break

        # 获取第一个DP周期内的所有数据
        dp_period = daily_data.loc[start_idx:end_idx].copy()

        # 计算时间差（小时）
        dp_period['time_diff'] = (dp_period['csvTime'].diff().dt.total_seconds() / 3600).shift(-1)



        # 计算能耗: 当前功率 * 到下一时刻的时间差
        total_energy = (dp_period['P3_18'] * dp_period['time_diff']).sum()



        return {
            "function": "calculate_thruster_energy_during_dp",
            "result": round(total_energy, 2)
        }

    except Exception as e:
        print(f"计算能耗错误: {str(e)}")
        raise

#
#
# def calculate_average_thruster_energy_during_dp(dates):
#     """
#     计算多天DP过程中侧推的平均能耗
#
#     Args:
#         dates (list): 日期列表，每个日期格式为'YYYY/MM/DD'
#     Returns:
#         dict: 包含平均能耗的结果字典
#     """
#     # try:
#     total_energy = 0
#     valid_days = 0
#
#     # 计算每天的能耗并累加
#     for date in dates:
#         daily_result = calculate_thruster_energy_during_dp(date)
#         if daily_result and 'result' in daily_result:
#             total_energy += daily_result['result']
#             print(f"{date}日的功耗是{daily_result['result']}")
#             valid_days += 1
#
#     # 计算平均值
#     if valid_days > 0:
#         average_energy = total_energy / valid_days
#         return {
#             "function": "calculate_average_thruster_energy_during_dp",
#             "result": round(average_energy, 2)  # 保留2位小数
#         }
#     return None
#
#     # except Exception as e:
#     #     print(f"Error calculating average thruster energy: {e}")
#     #     return None

#新加入的代码


def calculate_average_thruster_energy_during_dp(dates):
    """
    计算多天DP过程中侧推的平均能耗
    使用status判断DP状态，直接使用固定时间系数计算能耗

    Args:
        dates (list): 日期列表，每个日期格式为'YYYY/MM/DD'
    Returns:
        dict: 包含平均能耗的结果字典
    """
    try:
        # 读取数据
        df = pd.read_csv('database_in_use/Port3_ksbg_9.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        total_energy = 0
        valid_days = 0

        for date in dates:
            # 筛选当天数据
            daily_data = df[df['csvTime'].dt.date == pd.to_datetime(date).date()].copy()
            daily_data = daily_data.sort_values('csvTime').reset_index(drop=True)

            # 找到第一组ON_DP到OFF_DP的数据
            first_on_dp = daily_data[daily_data['status'] == 'ON_DP'].index.min()
            if pd.isna(first_on_dp):
                continue

            first_off_dp = daily_data[
                (daily_data.index > first_on_dp) &
                (daily_data['status'] == 'OFF_DP')
                ].index.min()
            if pd.isna(first_off_dp):
                continue

            # 获取第一个DP周期的数据
            dp_period = daily_data.loc[first_on_dp:first_off_dp]

            # 计算能耗：功率和乘以固定系数
            daily_energy = dp_period['P3_18'].sum() * 0.0166666666666
            total_energy += daily_energy
            valid_days += 1

            print(f"{date}日的功耗是{daily_energy}")

        if valid_days > 0:
            average_energy = total_energy / valid_days
            return {
                "function": "calculate_average_thruster_energy_during_dp",
                "result": round(average_energy, 2)
            }
        return None

    except Exception as e:
        print(f"计算平均能耗错误: {str(e)}")
        return None
# def calculate_propulsion_energy_during_dp(date):
#     """
#     计算DP过程中推进系统的总能耗
#
#     参数:
#         date (str): 目标日期，格式'YYYY/MM/DD'
#     返回:
#         dict: 包含总能耗的结果字典
#     """
#     try:
#         # 1. 首先获取DP的时间段
#         dp_df = pd.read_csv('database_in_use/Port3_ksbg_9.csv')
#         dp_df['csvTime'] = pd.to_datetime(dp_df['csvTime'])
#
#         # 设置时间范围
#         start_time = pd.to_datetime(f"{date} 00:00:00")
#         end_time = pd.to_datetime(f"{date} 23:59:59")
#
#         dp_df = dp_df[(dp_df['csvTime'] >= start_time) &
#                       (dp_df['csvTime'] <= end_time)]
#
#         # 2. 识别DP周期
#         dp_periods = []
#         dp_start = None
#
#         for idx, row in dp_df.iterrows():
#             if row['status'] == 'ON_DP' and dp_start is None:
#                 dp_start = row['csvTime']
#             elif row['status'] == 'OFF_DP' and dp_start is not None:
#                 dp_periods.append((dp_start, row['csvTime']))
#                 dp_start = None
#
#         if not dp_periods:
#             return None
#
#         total_energy = 0
#
#         # 3. 计算每个DP周期的能耗
#         for period_start, period_end in dp_periods:
#             # 3.1 计算艏推能耗
#             bow_thruster_energy = calculate_bow_thruster_energy(
#                 period_start,
#                 period_end,
#                 dp_df
#             )
#
#             # 3.2 计算推进变频器能耗
#             propulsion_energy = calculate_propulsion_converter_energy(
#                 period_start,
#                 period_end
#             )
#
#             total_energy += bow_thruster_energy + propulsion_energy
#
#         return {
#             "function": "calculate_propulsion_energy_during_dp",
#             "result": round(total_energy, 2)
#         }
#
#     except Exception as e:
#         print(f"Error calculating propulsion energy: {e}")
#         return None


def calculate_propulsion_energy_during_dp(date):
    """
    计算第一个DP周期内推进系统的总能耗
    包括艏推和推进变频器的能耗

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含函数名和计算结果的字典
    """
    try:
        # 1. 读取相关数据
        dp_df = pd.read_csv('database_in_use/Port3_ksbg_9.csv')  # 艏推数据
        dp_df['csvTime'] = pd.to_datetime(dp_df['csvTime'])

        propulsion_df = pd.read_csv('database_in_use/Port3_ksbg_8.csv')  # 推进变频器数据
        propulsion_df['csvTime'] = pd.to_datetime(propulsion_df['csvTime'])

        propulsion2_df = pd.read_csv('database_in_use/Port4_ksbg_7.csv')  # 二号推进变频器数据
        propulsion2_df['csvTime'] = pd.to_datetime(propulsion2_df['csvTime'])

        # 2. 筛选当天数据
        daily_dp = dp_df[dp_df['csvTime'].dt.date == pd.to_datetime(date).date()].copy()
        daily_dp = daily_dp.sort_values('csvTime').reset_index(drop=True)

        # 3. 找到第一个DP周期的起止点
        start_idx = daily_dp[daily_dp['status'] == 'ON_DP'].index[0]
        end_idx = daily_dp[daily_dp['status'] == 'OFF_DP'].index[0]

        # 4. 分别计算三个系统在该DP周期内的能耗
        # 4.1 艏推能耗
        dp_period = daily_dp.loc[start_idx:end_idx]
        dp_period['time_diff'] = (dp_period['csvTime'].diff().dt.total_seconds() / 3600).shift(-1)
        bow_thruster_energy = (dp_period['P3_18'] * dp_period['time_diff']).sum()

        # 4.2 一号推进变频器能耗
        prop1_period = propulsion_df[
            (propulsion_df['csvTime'] >= dp_period['csvTime'].iloc[0]) &
            (propulsion_df['csvTime'] < dp_period['csvTime'].iloc[-1])
            ].copy()
        prop1_period['time_diff'] = (prop1_period['csvTime'].diff().dt.total_seconds() / 3600).shift(-1)
        prop1_energy = (prop1_period['P3_15'] * prop1_period['time_diff']).sum()

        # 4.3 二号推进变频器能耗
        prop2_period = propulsion2_df[
            (propulsion2_df['csvTime'] >= dp_period['csvTime'].iloc[0]) &
            (propulsion2_df['csvTime'] < dp_period['csvTime'].iloc[-1])
            ].copy()
        prop2_period['time_diff'] = (prop2_period['csvTime'].diff().dt.total_seconds() / 3600).shift(-1)
        prop2_energy = (prop2_period['P4_16'] * prop2_period['time_diff']).sum()

        # 5. 计算总能耗
        total_energy = bow_thruster_energy + prop1_energy + prop2_energy

        return {
            "function": "calculate_propulsion_energy_during_dp",
            "result": round(total_energy, 2)
        }

    except Exception as e:
        print(f"计算推进系统能耗错误: {str(e)}")
        return None








def calculate_bow_thruster_energy(start_time, end_time, dp_df):
    """计算艏推能耗"""
    # 使用P3_18(艏推功率反馈)计算能耗
    period_data = dp_df[
        (dp_df['csvTime'] >= start_time) &
        (dp_df['csvTime'] <= end_time)
        ]
    period_data['time_diff'] = (
            period_data['csvTime'].diff().dt.total_seconds() / 3600
    )
    return (period_data['P3_18'] * period_data['time_diff']).sum()


def calculate_propulsion_converter_energy(start_time, end_time):
    """计算推进变频器能耗"""
    total = 0

    # 读取一号和二号推进变频器数据
    for system in ['Port3_ksbg_8', 'Port4_ksbg_7']:
        df = pd.read_csv(f'database_in_use/{system}.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        df = df[
            (df['csvTime'] >= start_time) &
            (df['csvTime'] <= end_time)
            ]

        # 使用功率反馈字段(P3_15或P4_16)
        power_col = 'P3_15' if system == 'Port3_ksbg_8' else 'P4_16'

        df['time_diff'] = df['csvTime'].diff().dt.total_seconds() / 3600
        total += (df[power_col] * df['time_diff']).sum()

    return total

#新加入的代码
# def calculate_crane_energy_ratio(date, period='morning'):
#     """
#     计算折臂吊车能耗占甲板机械设备的比例
#
#     Args:
#         date (str): 目标日期，格式'YYYY/MM/DD'
#         period (str): 时间段，默认'morning'表示上午
#     Returns:
#         dict: 包含能耗比例的结果字典
#     """
#     try:
#         # 构造时间范围
#         start_time = f"{date} 00:00:00"
#         end_time = f"{date} 12:00:00"
#
#         # 计算折臂吊车能耗
#         crane_energy = calculate_total_energy(
#             start_time,
#             end_time,
#             device_name="折臂吊车"
#         )
#
#         # 计算甲板机械总能耗
#         total_energy = calculate_total_deck_machinery_energy(
#             start_time,
#             end_time
#         )
#
#         # 计算比例
#         if total_energy and total_energy > 0:
#             ratio = (crane_energy / total_energy) * 100
#             return {
#                 "function": "calculate_crane_energy_ratio",
#                 "result": round(ratio, 2)
#             }
#         return None
#
#     except Exception as e:
#         print(f"Error calculating crane energy ratio: {e}")
#         return None


def calculate_crane_energy_ratio(date, period='morning'):
    """
    计算指定时间段折臂吊车能耗占甲板机械设备的比例

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
        period (str): 时间段，'morning'表示上午，'afternoon'表示下午
    Returns:
        dict: 包含能耗比例的结果字典
    """
    try:
        # 1. 根据period参数设置时间范围
        if period == 'morning':
            start_time = pd.to_datetime(f"{date} 00:00:00")
            end_time = pd.to_datetime(f"{date} 12:00:00")
        elif period == 'afternoon':
            start_time = pd.to_datetime(f"{date} 12:00:00")
            end_time = pd.to_datetime(f"{date} 23:59:59")
        else:
            raise ValueError("period参数必须为'morning'或'afternoon'")


        time_diff = 0.0166666666666

        # 2. 读取所需的数据文件
        # 折臂吊车数据
        crane_df = pd.read_csv('database_in_use/device_13_11_meter_1311.csv')
        crane_df['csvTime'] = pd.to_datetime(crane_df['csvTime'])

        # 一号门架数据
        portal1_df = pd.read_csv('database_in_use/device_1_5_meter_105.csv')
        portal1_df['csvTime'] = pd.to_datetime(portal1_df['csvTime'])

        # 二号门架数据
        portal2_df = pd.read_csv('database_in_use/device_13_14_meter_1314.csv')
        portal2_df['csvTime'] = pd.to_datetime(portal2_df['csvTime'])

        # 绞车数据
        winch_df = pd.read_csv('database_in_use/device_1_15_meter_115.csv')
        winch_df['csvTime'] = pd.to_datetime(winch_df['csvTime'])

        # 3. 计算折臂吊车能耗
        crane_data = crane_df[
            (crane_df['csvTime'] >= start_time) &
            (crane_df['csvTime'] < end_time)
            ].copy()
        crane_data['time_diff'] = (crane_data['csvTime'].diff().dt.total_seconds() / 3600).shift(-1)
        crane_energy = (crane_data['13-11-6_v'] * crane_data['time_diff']).sum()


        print(crane_data['time_diff'])

        # 4. 计算甲板机械总能耗
        # 4.1 一号门架能耗
        portal1_data = portal1_df[
            (portal1_df['csvTime'] >= start_time) &
            (portal1_df['csvTime'] < end_time)
            ].copy()
        portal1_data['time_diff'] = (portal1_data['csvTime'].diff().dt.total_seconds() / 3600).shift(-1)
        portal1_energy =( portal1_data['1-5-6_v'] * portal1_data['time_diff'] ).sum()

        # 4.2 二号门架能耗
        portal2_data = portal2_df[
            (portal2_df['csvTime'] >= start_time) &
            (portal2_df['csvTime'] < end_time)
            ].copy()
        portal2_data['time_diff'] = (portal2_data['csvTime'].diff().dt.total_seconds()/ 3600).shift(-1)
        portal2_energy = (portal2_data['13-14-6_v']* portal2_data['time_diff']).sum()

        # 4.3 绞车能耗
        winch_data = winch_df[
            (winch_df['csvTime'] >= start_time) &
            (winch_df['csvTime'] < end_time)
            ].copy()
        winch_data['time_diff'] = (winch_data['csvTime'].diff().dt.total_seconds()/ 3600).shift(-1)
        winch_energy = (winch_data['1-15-6_v'] * winch_data['time_diff']).sum()

        # 5. 计算总能耗
        total_energy = crane_energy + portal1_energy + portal2_energy + winch_energy

        print("总能耗：",total_energy)

        # 6. 计算比例
        if total_energy > 0:
            ratio = (crane_energy / total_energy) * 100
            return {
                "function": "calculate_crane_energy_ratio",
                "result": round(ratio, 2)
            }
        return None

    except Exception as e:
        print(f"计算折臂吊车能耗比例错误: {str(e)}")
        return None

















#新加入的代码
def find_max_generator_energy(start_time, end_time):
    """
    查找指定时间段内能耗最大的发电机

    Args:
        start_time (str): 开始时间
        end_time (str): 结束时间
    Returns:
        dict: 包含最大能耗发电机及其能耗值的结果
    """
    try:
        # 一号和二号发电机数据
        df1 = pd.read_csv('database_in_use/Port1_ksbg_3.csv')
        df1['csvTime'] = pd.to_datetime(df1['csvTime'])
        df1 = df1[(df1['csvTime'] >= start_time) & (df1['csvTime'] <= end_time)]

        # 三号发电机数据
        df2 = pd.read_csv('database_in_use/Port2_ksbg_2.csv')
        df2['csvTime'] = pd.to_datetime(df2['csvTime'])
        df2 = df2[(df2['csvTime'] >= start_time) & (df2['csvTime'] <= end_time)]

        # 四号发电机数据
        df3 = pd.read_csv('database_in_use/Port2_ksbg_3.csv')
        df3['csvTime'] = pd.to_datetime(df3['csvTime'])
        df3 = df3[(df3['csvTime'] >= start_time) & (df3['csvTime'] <= end_time)]

        # 计算每个发电机的能耗
        energies = {}

        # 计算一号发电机能耗
        if not df1.empty:
            df1['time_diff'] = df1['csvTime'].diff().dt.total_seconds() / 3600
            energies['一号发电机'] = round((df1['P1_66'] * df1['time_diff']).sum(), 2)

        # 计算二号发电机能耗
        if not df1.empty:
            df1['time_diff'] = df1['csvTime'].diff().dt.total_seconds() / 3600
            energies['二号发电机'] = round((df1['P1_75'] * df1['time_diff']).sum(), 2)

        # 计算三号发电机能耗
        if not df2.empty:
            df2['time_diff'] = df2['csvTime'].diff().dt.total_seconds() / 3600
            energies['三号发电机'] = round((df2['P2_51'] * df2['time_diff']).sum(), 2)

        # 计算四号发电机能耗
        if not df3.empty:
            df3['time_diff'] = df3['csvTime'].diff().dt.total_seconds() / 3600
            energies['四号发电机'] = round((df3['P2_60'] * df3['time_diff']).sum(), 2)

        # 找出最大能耗的发电机
        if energies:
            max_generator = max(energies.items(), key=lambda x: x[1])
            return {
                "function": "find_max_generator_energy",
                "result": {
                    "generator": max_generator[0],
                    "energy": max_generator[1]
                }
            }

        return None

    except Exception as e:
        print(f"Error finding max generator energy: {e}")
        return None

#新加入的代码
def calculate_crane_energy_between_boat_states(date1, date2):
    """
    计算指定日期小艇入水到落座期间折臂吊车的总能耗

    Args:
        date1 (str): 第一个日期，格式'YYYY/MM/DD'
        date2 (str): 第二个日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含总能耗的结果字典
    """
    try:
        total_energy = 0

        for date in [date1, date2]:
            # 读取折臂吊车数据（包含小艇状态和能耗数据）
            df = pd.read_csv('database_in_use/device_13_11_meter_1311.csv')
            df['csvTime'] = pd.to_datetime(df['csvTime'])

            # 筛选当天数据
            start_time = pd.to_datetime(f"{date} 00:00:00")
            end_time = pd.to_datetime(f"{date} 23:59:59")
            daily_data = df[
                (df['csvTime'] >= start_time) &
                (df['csvTime'] <= end_time)
                ].copy()

            if daily_data.empty:
                continue

            # 找出小艇入水和落座的时间点
            boat_periods = []
            entry_time = None

            for idx, row in daily_data.iterrows():
                if row['status'] == '小艇入水':
                    entry_time = row['csvTime']
                elif row['status'] == '小艇落座' and entry_time is not None:
                    boat_periods.append((entry_time, row['csvTime']))
                    entry_time = None

            # 计算每个时间段的能耗
            for start, end in boat_periods:
                period_data = daily_data[
                    (daily_data['csvTime'] >= start) &
                    (daily_data['csvTime'] <= end)
                    ].copy()

                # 计算时间差（小时）
                period_data['time_diff'] = (
                        period_data['csvTime'].diff().dt.total_seconds() / 3600
                )

                # 使用折臂吊车液压的有功功率计算能耗
                # 13-11-6_v 是折臂吊车液压-Pt有功功率
                energy = (period_data['13-11-6_v'] * period_data['time_diff']).sum()
                total_energy += energy

        return {
            "function": "calculate_crane_energy_between_boat_states",
            "result": round(total_energy, 2)
        }

    except Exception as e:
        print(f"Error calculating crane energy: {e}")
        return None

#新加入的代码
def get_devices_runtime(date):
    """
    获取指定日期A架和折臂吊车的运行时间

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含两个设备运行时间的结果
    """
    try:
        start_time = f"{date} 00:00:00"
        end_time = f"{date} 23:59:59"

        # 获取A架运行时间
        ajia_result = calculate_uptime(
            start_time,
            end_time,
            shebeiname="A架"
        )

        # 获取折臂吊车运行时间
        crane_result = calculate_uptime(
            start_time,
            end_time,
            shebeiname="折臂吊车"
        )

        # 提取分钟数
        ajia_minutes = int(re.search(r'(\d+)分钟', ajia_result['result'][0]).group(1))
        crane_minutes = int(re.search(r'(\d+)分钟', crane_result['result'][0]).group(1))

        return {
            "function": "get_devices_runtime",
            "result": {
                "A架": ajia_minutes,
                "折臂吊车": crane_minutes
            }
        }

    except Exception as e:
        print(f"Error getting devices runtime: {e}")
        return None

#新加入的代码
def calculate_runtime_difference(date):
    """
    计算A架和折臂吊车的运行时间差

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含运行时间差的结果
    """
    try:
        # 复用get_devices_runtime获取两个设备的运行时间
        runtime_result = get_devices_runtime(date)

        if runtime_result and 'result' in runtime_result:
            ajia_time = runtime_result['result']['A架']
            crane_time = runtime_result['result']['折臂吊车']

            # 计算差值（A架时间 - 折臂吊车时间）
            time_diff = abs(ajia_time - crane_time)  # 使用绝对值

            return {
                "function": "calculate_runtime_difference",
                "result": time_diff
            }

        return None

    except Exception as e:
        print(f"Error calculating runtime difference: {e}")
        return None

#新加入的代码
def calculate_average_swing_count(dates):
    """
    计算多个日期A架的平均摆动次数

    Args:
        dates (list): 日期列表，每个日期格式'YYYY/MM/DD'
    Returns:
        dict: 包含平均摆动次数的结果
    """
    try:
        total_swings = 0
        valid_days = 0
        print(dates)
        for date in dates:
            # 读取A架数据
            df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
            df['csvTime'] = pd.to_datetime(df['csvTime'])

            # 筛选当天数据
            start_time = pd.to_datetime(f"{date} 00:00:00")
            end_time = pd.to_datetime(f"{date} 23:59:59")
            daily_data = df[
                (df['csvTime'] >= start_time) &
                (df['csvTime'] <= end_time)
                ]

            if not daily_data.empty:
                # 统计A架摆出和摆回的次数
                swing_count = len(daily_data[
                                      daily_data['status'].isin(['A架摆出', 'A架摆回'])
                                  ])

                total_swings += swing_count
                valid_days += 1

        if valid_days > 0:
            # 计算平均摆动次数
            average_swings = total_swings / valid_days
            return {
                "function": "calculate_average_swing_count",
                "result": int(round(average_swings))  # 四舍五入到整数
            }

        return None

    except Exception as e:
        print(f"Error calculating average swing count: {e}")
        return None

#新加入的代码  计算多天的平均作业时长（下放+回收阶段）
def calculate_average_operation_time(dates):
    """
    计算多天的平均作业时长（下放+回收阶段）

    Args:
        dates (list): 日期列表，格式['YYYY/MM/DD']
    Returns:
        dict: 包含平均作业时长的结果（整数分钟）
    """
    try:
        total_duration = 0
        valid_days = 0

        for date in dates:
            # 计算下放阶段时长（DP过程）
            dp_duration = calculate_dp_phase_duration(date)

            # 计算回收阶段时长（A架开关机过程）
            recovery_duration = calculate_recovery_phase_duration(date)

            if dp_duration is not None and recovery_duration is not None:
                total_duration += (dp_duration + recovery_duration)
                valid_days += 1

        if valid_days > 0:
            average_duration = round(total_duration / valid_days)  # 四舍五入
            return {
                "function": "calculate_average_operation_time",
                "result": average_duration
            }
        return None

    except Exception as e:
        print(f"Error calculating average operation time: {e}")
        return None


def calculate_dp_phase_duration(date):
    """计算下放阶段（DP过程）时长"""
    try:
        # 读取DP数据
        df = pd.read_csv('database_in_use/Port3_ksbg_9.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 筛选当天数据
        start_time = pd.to_datetime(f"{date} 00:00:00")
        end_time = pd.to_datetime(f"{date} 23:59:59")
        daily_data = df[
            (df['csvTime'] >= start_time) &
            (df['csvTime'] <= end_time)
            ]

        if daily_data.empty:
            return None

        # 找出ON_DP和OFF_DP时间点
        dp_on = daily_data[daily_data['status'] == 'ON_DP']['csvTime'].iloc[0]
        dp_off = daily_data[daily_data['status'] == 'OFF_DP']['csvTime'].iloc[0]

        # 计算时长（分钟）
        return (dp_off - dp_on).total_seconds() / 60

    except Exception:
        return None


def calculate_recovery_phase_duration(date):
    """计算回收阶段（A架开关机过程）时长"""
    try:
        # 读取A架数据
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 筛选当天数据
        start_time = pd.to_datetime(f"{date} 00:00:00")
        end_time = pd.to_datetime(f"{date} 23:59:59")
        daily_data = df[
            (df['csvTime'] >= start_time) &
            (df['csvTime'] <= end_time)
            ]

        if daily_data.empty:
            return None

        # 找出开机和关机时间点（取最后一组开关机记录）
        power_on = daily_data[daily_data['status'] == '开机']['csvTime'].iloc[-1]
        power_off = daily_data[daily_data['status'] == '关机']['csvTime'].iloc[-1]

        # 计算时长（分钟）
        return (power_off - power_on).total_seconds() / 60

    except Exception:
        return None

#新加入的代码 检测A架角度数据的异常
def detect_angle_anomalies():
    """
    检测A架角度数据异常（数据为error的情况）

    Returns:
        dict: 包含异常时间段的结果
    """
    try:
        # 读取A架数据
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 提取日期信息
        df['date'] = df['csvTime'].dt.date

        # 检查左舷和右舷角度是否为error
        anomaly_days = set()

        # 检查左舷角度(Ajia-1_v)和右舷角度(Ajia-0_v)
        for angle_col in ['Ajia-1_v', 'Ajia-0_v']:
            error_data = df[df[angle_col] == 'error']
            if not error_data.empty:
                anomaly_days.update(error_data['date'].unique())

        if anomaly_days:
            # 转换为列表并排序
            anomaly_list = sorted(list(anomaly_days))

            # 识别连续的时间段
            anomaly_ranges = []
            start = anomaly_list[0]
            prev = start

            for curr in anomaly_list[1:] + [None]:
                if curr is None or (curr - prev).days > 1:
                    anomaly_ranges.append((
                        start.strftime('%Y/%m/%d'),
                        prev.strftime('%Y/%m/%d')
                    ))
                    if curr is not None:
                        start = curr
                prev = curr if curr else prev

            return {
                "function": "detect_angle_anomalies",
                "result": anomaly_ranges
            }

        return None

    except Exception as e:
        print(f"Error detecting angle anomalies: {e}")
        return None

#新加入的代码 计算指定时间段内所有发电机组的总燃油消耗量
def calculate_total_fuel_consumption(start_time, end_time):
    """
    计算指定时间段内所有发电机组的总燃油消耗量

    Args:
        start_time (str): 开始时间，格式 'YYYY/MM/DD HH:MM:SS'
        end_time (str): 结束时间，格式 'YYYY/MM/DD HH:MM:SS'
    Returns:
        dict: 包含总燃油消耗量的结果（L）
    """
    # try:
    total_consumption = 0

    # 读取一号、二号发电机数据
    df1 = pd.read_csv('database_in_use/Port1_ksbg_1.csv')
    df1['csvTime'] = pd.to_datetime(df1['csvTime'])

    # 读取三号、四号发电机数据
    df2 = pd.read_csv('database_in_use/Port2_ksbg_1.csv')
    df2['csvTime'] = pd.to_datetime(df2['csvTime'])

    # 时间范围筛选
    period1 = df1[
        (df1['csvTime'] >= start_time) &
        (df1['csvTime'] <= end_time)
        ]
    period2 = df2[
        (df2['csvTime'] >= start_time) &
        (df2['csvTime'] <= end_time)
        ]

    if not period1.empty:
        # 计算一号发电机消耗
        period1['time_diff'] = period1['csvTime'].diff().dt.total_seconds() / 3600
        consumption1 = (period1['P1_3'] * period1['time_diff']).sum()

        # 计算二号发电机消耗
        consumption2 = (period1['P1_25'] * period1['time_diff']).sum()

        total_consumption += (consumption1 + consumption2)

    if not period2.empty:
        # 计算三号发电机消耗
        period2['time_diff'] = period2['csvTime'].diff().dt.total_seconds() / 3600
        consumption3 = (period2['P2_3'] * period2['time_diff']).sum()

        # 计算四号发电机消耗
        consumption4 = (period2['P2_25'] * period2['time_diff']).sum()

        total_consumption += (consumption3 + consumption4)

    return {
        "function": "calculate_total_fuel_consumption",
        "result": round(total_consumption, 2)
    }

    # except Exception as e:
    #     print(f"Error calculating fuel consumption: {e}")
    #     return None


#新加入的代码 计算指定时间段内所有发电机组的总发电量
def calculate_total_power_generation(start_time, end_time):
    """
    计算指定时间段内所有发电机组的总发电量

    Args:
        start_time (str): 开始时间
        end_time (str): 结束时间
    Returns:
        dict: 包含总发电量的结果(kWh)
    """
    try:
        total_power = 0

        # 计算一号和二号发电机组发电量
        df1 = pd.read_csv('database_in_use/Port1_ksbg_3.csv')
        df1['csvTime'] = pd.to_datetime(df1['csvTime'])
        df1 = df1[(df1['csvTime'] >= start_time) & (df1['csvTime'] <= end_time)]

        if not df1.empty:
            df1['time_diff'] = df1['csvTime'].diff().dt.total_seconds() / 3600
            # P1_66: 一号机组有功功率，P1_75: 二号机组有功功率
            total_power += (df1['P1_66'] * df1['time_diff']).sum()
            total_power += (df1['P1_75'] * df1['time_diff']).sum()

        # 计算三号发电机组发电量
        df2 = pd.read_csv('database_in_use/Port2_ksbg_2.csv')
        df2['csvTime'] = pd.to_datetime(df2['csvTime'])
        df2 = df2[(df2['csvTime'] >= start_time) & (df2['csvTime'] <= end_time)]

        if not df2.empty:
            df2['time_diff'] = df2['csvTime'].diff().dt.total_seconds() / 3600
            # P2_51: 三号机组有功功率
            total_power += (df2['P2_51'] * df2['time_diff']).sum()

        # 计算四号发电机组发电量
        df3 = pd.read_csv('database_in_use/Port2_ksbg_3.csv')
        df3['csvTime'] = pd.to_datetime(df3['csvTime'])
        df3 = df3[(df3['csvTime'] >= start_time) & (df3['csvTime'] <= end_time)]

        if not df3.empty:
            df3['time_diff'] = df3['csvTime'].diff().dt.total_seconds() / 3600
            # P2_60: 四号机组有功功率
            total_power += (df3['P2_60'] * df3['time_diff']).sum()

        return {
            "function": "calculate_total_power_generation",
            "result": round(total_power, 2)
        }

    except Exception as e:
        print(f"Error calculating total power generation: {e}")
        return None

#新加入的代码 计算推进系统能耗占总发电量的比例
def calculate_propulsion_energy_ratio(start_time, end_time):
    """
    计算推进系统能耗占总发电量的比例

    Args:
        start_time (str): 开始时间
        end_time (str): 结束时间
    Returns:
        dict: 包含能耗比例的结果(%)
    """
    try:
        # 1. 计算推进系统总能耗
        propulsion_energy = 0

        # 1.1 计算一号推进变频器能耗 (Port3_ksbg_8)
        df1 = pd.read_csv('database_in_use/Port3_ksbg_8.csv')
        df1['csvTime'] = pd.to_datetime(df1['csvTime'])
        df1 = df1[(df1['csvTime'] >= start_time) & (df1['csvTime'] <= end_time)]

        if not df1.empty:
            df1['time_diff'] = df1['csvTime'].diff().dt.total_seconds() / 3600
            # P3_15: 一号推进变频器功率反馈
            propulsion_energy += (df1['P3_15'] * df1['time_diff']).sum()

        # 1.2 计算二号推进变频器能耗 (Port4_ksbg_7)
        df2 = pd.read_csv('database_in_use/Port4_ksbg_7.csv')
        df2['csvTime'] = pd.to_datetime(df2['csvTime'])
        df2 = df2[(df2['csvTime'] >= start_time) & (df2['csvTime'] <= end_time)]

        if not df2.empty:
            df2['time_diff'] = df2['csvTime'].diff().dt.total_seconds() / 3600
            # P4_16: 二号推进变频器功率反馈
            propulsion_energy += (df2['P4_16'] * df2['time_diff']).sum()

        # 1.3 计算艏推能耗 (Port3_ksbg_9)
        df3 = pd.read_csv('database_in_use/Port3_ksbg_9.csv')
        df3['csvTime'] = pd.to_datetime(df3['csvTime'])
        df3 = df3[(df3['csvTime'] >= start_time) & (df3['csvTime'] <= end_time)]

        if not df3.empty:
            df3['time_diff'] = df3['csvTime'].diff().dt.total_seconds() / 3600
            # P3_18: 艏推功率反馈
            propulsion_energy += (df3['P3_18'] * df3['time_diff']).sum()

        # 2. 计算总发电量
        total_power = 0

        # 2.1 计算一二号发电机组发电量
        df4 = pd.read_csv('database_in_use/Port1_ksbg_3.csv')
        df4['csvTime'] = pd.to_datetime(df4['csvTime'])
        df4 = df4[(df4['csvTime'] >= start_time) & (df4['csvTime'] <= end_time)]

        if not df4.empty:
            df4['time_diff'] = df4['csvTime'].diff().dt.total_seconds() / 3600
            # P1_66: 一号机组有功功率，P1_75: 二号机组有功功率
            total_power += (df4['P1_66'] * df4['time_diff']).sum()
            total_power += (df4['P1_75'] * df4['time_diff']).sum()

        # 2.2 计算三号发电机组发电量
        df5 = pd.read_csv('database_in_use/Port2_ksbg_2.csv')
        df5['csvTime'] = pd.to_datetime(df5['csvTime'])
        df5 = df5[(df5['csvTime'] >= start_time) & (df5['csvTime'] <= end_time)]

        if not df5.empty:
            df5['time_diff'] = df5['csvTime'].diff().dt.total_seconds() / 3600
            # P2_51: 三号机组有功功率
            total_power += (df5['P2_51'] * df5['time_diff']).sum()

        # 2.3 计算四号发电机组发电量
        df6 = pd.read_csv('database_in_use/Port2_ksbg_3.csv')
        df6['csvTime'] = pd.to_datetime(df6['csvTime'])
        df6 = df6[(df6['csvTime'] >= start_time) & (df6['csvTime'] <= end_time)]

        if not df6.empty:
            df6['time_diff'] = df6['csvTime'].diff().dt.total_seconds() / 3600
            # P2_60: 四号机组有功功率
            total_power += (df6['P2_60'] * df6['time_diff']).sum()

        # 3. 计算比例
        if total_power > 0:
            ratio = (propulsion_energy / total_power) * 100
            return {
                "function": "calculate_propulsion_energy_ratio",
                "result": round(ratio, 2)
            }

        return None

    except Exception as e:
        print(f"Error calculating propulsion energy ratio: {e}")
        return None

#新加入的代码 计算甲板机械能耗占总发电量的比例
def calculate_deck_machinery_power_ratio(start_time, end_time):
    """
    计算甲板机械能耗占总发电量的比例

    Args:
        start_time (str): 开始时间
        end_time (str): 结束时间
    Returns:
        dict: 包含能耗比例的结果(%)
    """
    try:
        # 1. 计算甲板机械总能耗
        machinery_energy = 0

        # 1.1 计算绞车变频器能耗
        df1 = pd.read_csv('database_in_use/device_1_15_meter_115.csv')
        df1['csvTime'] = pd.to_datetime(df1['csvTime'])
        df1 = df1[(df1['csvTime'] >= start_time) & (df1['csvTime'] <= end_time)]

        if not df1.empty:
            df1['time_diff'] = df1['csvTime'].diff().dt.total_seconds() / 3600
            # 1-15-6_v: 绞车变频器有功功率
            machinery_energy += (df1['1-15-6_v'] * df1['time_diff']).sum()

        # 1.2 计算折臂吊车能耗
        df2 = pd.read_csv('database_in_use/device_13_11_meter_1311.csv')
        df2['csvTime'] = pd.to_datetime(df2['csvTime'])
        df2 = df2[(df2['csvTime'] >= start_time) & (df2['csvTime'] <= end_time)]

        if not df2.empty:
            df2['time_diff'] = df2['csvTime'].diff().dt.total_seconds() / 3600
            # 13-11-6_v: 折臂吊车液压有功功率
            machinery_energy += (df2['13-11-6_v'] * df2['time_diff']).sum()

        # 1.3 计算一号门架主液压泵能耗
        df3 = pd.read_csv('database_in_use/device_1_5_meter_105.csv')
        df3['csvTime'] = pd.to_datetime(df3['csvTime'])
        df3 = df3[(df3['csvTime'] >= start_time) & (df3['csvTime'] <= end_time)]

        if not df3.empty:
            df3['time_diff'] = df3['csvTime'].diff().dt.total_seconds() / 3600
            # 1-5-6_v: 一号门架主液压泵有功功率
            machinery_energy += (df3['1-5-6_v'] * df3['time_diff']).sum()

        # 1.4 计算二号门架主液压泵能耗
        df4 = pd.read_csv('database_in_use/device_13_14_meter_1314.csv')
        df4['csvTime'] = pd.to_datetime(df4['csvTime'])
        df4 = df4[(df4['csvTime'] >= start_time) & (df4['csvTime'] <= end_time)]

        if not df4.empty:
            df4['time_diff'] = df4['csvTime'].diff().dt.total_seconds() / 3600
            # 13-14-6_v: 二号门架主液压泵有功功率
            machinery_energy += (df4['13-14-6_v'] * df4['time_diff']).sum()

        # 2. 获取总发电量
        total_power = calculate_total_power_generation(start_time, end_time)
        if total_power and 'result' in total_power:
            total_power_value = total_power['result']

            # 3. 计算比例
            if total_power_value > 0:
                ratio = (machinery_energy / total_power_value) * 100
                return {
                    "function": "calculate_deck_machinery_power_ratio",
                    "result": round(ratio, 2)
                }

        return None

    except Exception as e:
        print(f"Error calculating deck machinery power ratio: {e}")
        return None

#新加入的代码 计算指定日期的平均作业能耗（下放+回收阶段）
def calculate_average_operation_energy(dates):
    """
    计算指定日期的平均作业能耗（下放+回收阶段）

    Args:
        dates (list): 日期列表，格式['YYYY/MM/DD']
    Returns:
        dict: 包含平均能耗的结果(kWh)
    """
    try:
        total_energy = 0
        valid_days = 0

        for date in dates:
            daily_energy = 0

            # 1. 下放阶段能耗计算（ON_DP到OFF_DP）
            dp_df = pd.read_csv('database_in_use/Port3_ksbg_9.csv')
            dp_df['csvTime'] = pd.to_datetime(dp_df['csvTime'])

            # 筛选当天数据
            start_time = pd.to_datetime(f"{date} 00:00:00")
            end_time = pd.to_datetime(f"{date} 23:59:59")
            dp_data = dp_df[
                (dp_df['csvTime'] >= start_time) &
                (dp_df['csvTime'] <= end_time)
                ]

            if not dp_data.empty:
                # 找到DP开始和结束时间
                dp_start = dp_data[dp_data['status'] == 'ON_DP']['csvTime'].iloc[0]
                dp_end = dp_data[dp_data['status'] == 'OFF_DP']['csvTime'].iloc[0]

                # 统计下放阶段能耗
                dp_period = dp_data[
                    (dp_data['csvTime'] >= dp_start) &
                    (dp_data['csvTime'] <= dp_end)
                    ]

                if not dp_period.empty:
                    dp_period['time_diff'] = dp_period['csvTime'].diff().dt.total_seconds() / 3600
                    # P3_18: 艏推功率反馈
                    daily_energy += (dp_period['P3_18'] * dp_period['time_diff']).sum()

            # 2. 回收阶段能耗计算（A架开机到关机）
            ajia_df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
            ajia_df['csvTime'] = pd.to_datetime(ajia_df['csvTime'])

            ajia_data = ajia_df[
                (ajia_df['csvTime'] >= start_time) &
                (ajia_df['csvTime'] <= end_time)
                ]

            if not ajia_data.empty:
                # 找到最后一次开关机时间点
                power_on = ajia_data[ajia_data['status'] == '开机']['csvTime'].iloc[-1]
                power_off = ajia_data[ajia_data['status'] == '关机']['csvTime'].iloc[-1]

                # 获取回收阶段的功率数据
                recovery_period = ajia_data[
                    (ajia_data['csvTime'] >= power_on) &
                    (ajia_data['csvTime'] <= power_off)
                    ]

                if not recovery_period.empty:
                    recovery_period['time_diff'] = recovery_period['csvTime'].diff().dt.total_seconds() / 3600
                    # Ajia-3_v和Ajia-5_v分别是启动柜电流
                    daily_energy += (recovery_period['Ajia-3_v'].astype(float) * recovery_period['time_diff']).sum()
                    daily_energy += (recovery_period['Ajia-5_v'].astype(float) * recovery_period['time_diff']).sum()

            if daily_energy > 0:
                total_energy += daily_energy
                valid_days += 1

        # 计算平均值
        if valid_days > 0:
            average_energy = total_energy / valid_days
            return {
                "function": "calculate_average_operation_energy",
                "result": round(average_energy, 2)
            }

        return None

    except Exception as e:
        print(f"Error calculating average operation energy: {e}")
        return None


#新加入的代码 计算指定时间段内的理论发电量
def calculate_theoretical_power_generation(start_time, end_time, oil_density=0.8448, oil_heat_value=42.6):
    """
    计算理论发电量

    Args:
        start_time (str): 开始时间
        end_time (str): 结束时间
        oil_density (float): 柴油密度(kg/L)
        oil_heat_value (float): 柴油热值(MJ/kg)
    Returns:
        dict: 包含理论发电量的结果(kWh)
    """
    try:
        total_fuel = 0

        # 1. 计算一、二号发电机组燃油消耗
        df1 = pd.read_csv('database_in_use/Port1_ksbg_1.csv')
        df1['csvTime'] = pd.to_datetime(df1['csvTime'])
        df1 = df1[(df1['csvTime'] >= start_time) & (df1['csvTime'] <= end_time)]

        if not df1.empty:
            df1['time_diff'] = df1['csvTime'].diff().dt.total_seconds() / 3600  # 转换为小时
            # P1_3: 一号柴油发电机组燃油消耗率
            # P1_25: 二号柴油发电机组燃油消耗率
            total_fuel += (df1['P1_3'] * df1['time_diff']).sum()
            total_fuel += (df1['P1_25'] * df1['time_diff']).sum()

        # 2. 计算三、四号发电机组燃油消耗
        df2 = pd.read_csv('database_in_use/Port2_ksbg_1.csv')
        df2['csvTime'] = pd.to_datetime(df2['csvTime'])
        df2 = df2[(df2['csvTime'] >= start_time) & (df2['csvTime'] <= end_time)]

        if not df2.empty:
            df2['time_diff'] = df2['csvTime'].diff().dt.total_seconds() / 3600
            # P2_3: 三号柴油发电机组燃油消耗率
            # P2_25: 四号柴油发电机组燃油消耗率
            total_fuel += (df2['P2_3'] * df2['time_diff']).sum()
            total_fuel += (df2['P2_25'] * df2['time_diff']).sum()

        # 3. 计算理论发电量
        # 总耗油量(L) -> 总质量(kg) -> 总热量(MJ) -> 电量(kWh)
        total_mass = total_fuel * oil_density  # kg
        total_energy_mj = total_mass * oil_heat_value  # MJ
        theoretical_power = total_energy_mj / 3.6  # 1kWh = 3.6MJ

        return {
            "function": "calculate_theoretical_power_generation",
            "result": round(theoretical_power, 2)
        }

    except Exception as e:
        print(f"Error calculating theoretical power: {e}")
        return None


#新加入的代码 计算柴油机发电效率
def calculate_generator_efficiency(start_time, end_time, oil_density=0.8448, oil_heat_value=42.6):
    """
    计算柴油机发电效率

    Args:
        start_time (str): 开始时间
        end_time (str): 结束时间
        oil_density (float): 柴油密度(kg/L)
        oil_heat_value (float): 柴油热值(MJ/kg)
    Returns:
        dict: 包含发电效率的结果(%)
    """
    try:
        # 1. 获取理论发电量
        theoretical_result = calculate_theoretical_power_generation(
            start_time,
            end_time,
            oil_density,
            oil_heat_value
        )

        if not theoretical_result or 'result' not in theoretical_result:
            return None

        theoretical_power = theoretical_result['result']

        # 2. 计算实际发电量
        actual_power = 0

        # 2.1 计算一二号发电机组发电量
        df1 = pd.read_csv('database_in_use/Port1_ksbg_3.csv')
        df1['csvTime'] = pd.to_datetime(df1['csvTime'])
        df1 = df1[(df1['csvTime'] >= start_time) & (df1['csvTime'] <= end_time)]

        if not df1.empty:
            df1['time_diff'] = df1['csvTime'].diff().dt.total_seconds() / 3600
            # P1_66: 一号机组有功功率，P1_75: 二号机组有功功率
            actual_power += (df1['P1_66'] * df1['time_diff']).sum()
            actual_power += (df1['P1_75'] * df1['time_diff']).sum()

        # 2.2 计算三号发电机组发电量
        df2 = pd.read_csv('database_in_use/Port2_ksbg_2.csv')
        df2['csvTime'] = pd.to_datetime(df2['csvTime'])
        df2 = df2[(df2['csvTime'] >= start_time) & (df2['csvTime'] <= end_time)]

        if not df2.empty:
            df2['time_diff'] = df2['csvTime'].diff().dt.total_seconds() / 3600
            # P2_51: 三号机组有功功率
            actual_power += (df2['P2_51'] * df2['time_diff']).sum()

        # 2.3 计算四号发电机组发电量
        df3 = pd.read_csv('database_in_use/Port2_ksbg_3.csv')
        df3['csvTime'] = pd.to_datetime(df3['csvTime'])
        df3 = df3[(df3['csvTime'] >= start_time) & (df3['csvTime'] <= end_time)]

        if not df3.empty:
            df3['time_diff'] = df3['csvTime'].diff().dt.total_seconds() / 3600
            # P2_60: 四号机组有功功率
            actual_power += (df3['P2_60'] * df3['time_diff']).sum()

        # 3. 计算效率
        if theoretical_power > 0:
            efficiency = (actual_power / theoretical_power) * 100
            return {
                "function": "calculate_generator_efficiency",
                "result": round(efficiency, 2)
            }

        return None

    except Exception as e:
        print(f"Error calculating generator efficiency: {e}")
        return None


#新加入的代码 计算征服者在指定时间前出水的比例
def calculate_conqueror_ascend_ratio(start_date, end_date, time_threshold='16:00:00'):
    """
    计算征服者在指定时间前出水的比例

    Args:
        start_date (str): 开始日期，格式'YYYY/MM/DD'
        end_date (str): 结束日期，格式'YYYY/MM/DD'
        time_threshold (str): 时间阈值，默认'16:00:00'
    Returns:
        dict: 包含比例的结果(%)
    """
    try:
        # 读取A架数据
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 设置日期范围
        start_time = pd.to_datetime(f"{start_date} 00:00:00")
        end_time = pd.to_datetime(f"{end_date} 23:59:59")

        # 筛选日期范围内的数据
        df = df[(df['csvTime'] >= start_time) & (df['csvTime'] <= end_time)]

        if df.empty:
            return None

        # 获取所有征服者出水事件
        ascend_events = df[df['status'] == '征服者出水']

        if ascend_events.empty:
            return None

        # 统计总事件数和指定时间前的事件数
        total_events = len(ascend_events)
        before_threshold = len(ascend_events[
                                   ascend_events['csvTime'].dt.strftime('%H:%M:%S') < time_threshold
                                   ])

        # 计算比例
        if total_events > 0:
            ratio = (before_threshold / total_events) * 100
            return {
                "function": "calculate_conqueror_ascend_ratio",
                "result": round(ratio, 2)
            }

        return None

    except Exception as e:
        print(f"Error calculating conqueror ascend ratio: {e}")
        return None


#新加入的代码 计算指定时间段内的开机时长
def calculate_early_operation_ratio(start_date, end_date, time_threshold='09:00:00'):
    """
    计算在指定时间前开始作业(ON_DP)的比例

    Args:
        start_date (str): 开始日期，格式'YYYY/MM/DD'
        end_date (str): 结束日期，格式'YYYY/MM/DD'
        time_threshold (str): 时间阈值，默认'09:00:00'
    Returns:
        dict: 包含比例的结果(%)
    """
    try:
        # 读取DP数据
        df = pd.read_csv('database_in_use/Port3_ksbg_9.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 设置日期范围
        start_time = pd.to_datetime(f"{start_date} 00:00:00")
        end_time = pd.to_datetime(f"{end_date} 23:59:59")

        # 筛选日期范围内的数据
        df = df[(df['csvTime'] >= start_time) &
                (df['csvTime'] <= end_time)]

        if df.empty:
            return None

        # 按日期分组，找到每天第一次ON_DP的时间
        df['date'] = df['csvTime'].dt.date
        daily_starts = []

        for date, group in df.groupby('date'):
            dp_events = group[group['status'] == 'ON_DP']
            if not dp_events.empty:
                daily_starts.append(dp_events['csvTime'].iloc[0])

        if not daily_starts:
            return None

        # 统计早于阈值的天数
        total_days = len(daily_starts)
        early_starts = sum(1 for time in daily_starts
                           if time.strftime('%H:%M:%S') < time_threshold)

        # 计算比例
        if total_days > 0:
            ratio = (early_starts / total_days) * 100
            return {
                "function": "calculate_early_operation_ratio",
                "result": round(ratio, 2)
            }

        return None

    except Exception as e:
        print(f"Error calculating early operation ratio: {e}")
        return None

#新加入的代码 计算征服者在指定时间前入水的比例
def calculate_conqueror_entry_ratio(start_date, end_date, time_threshold='09:00:00'):
    """
    计算征服者在指定时间前入水的比例

    Args:
        start_date (str): 开始日期，格式'YYYY/MM/DD'
        end_date (str): 结束日期，格式'YYYY/MM/DD'
        time_threshold (str): 时间阈值，默认'09:00:00'
    Returns:
        dict: 包含比例的结果(%)
    """
    try:
        # 读取A架数据
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 设置日期范围
        start_time = pd.to_datetime(f"{start_date} 00:00:00")
        end_time = pd.to_datetime(f"{end_date} 23:59:59")

        # 筛选时间范围内的数据
        df = df[(df['csvTime'] >= start_time) &
                (df['csvTime'] <= end_time)]

        if df.empty:
            return None

        # 筛选征服者入水事件并按日期分组
        entry_events = df[df['status'] == '征服者入水']
        if entry_events.empty:
            return None

        # 统计总事件数和时间阈值前的事件数
        total_entries = len(entry_events)
        early_entries = len(entry_events[
                                entry_events['csvTime'].dt.strftime('%H:%M:%S') < time_threshold
                                ])

        # 计算比例
        if total_entries > 0:
            ratio = (early_entries / total_entries) * 100
            return {
                "function": "calculate_conqueror_entry_ratio",
                "result": round(ratio, 2)
            }

        return None

    except Exception as e:
        print(f"Error calculating conqueror entry ratio: {e}")
        return None


#新加入的代码 获取指定日期A架的开关机时间点
def get_power_onoff_times(date):
    """
    获取指定日期A架的开关机时间点

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含开关机时间的结果
    """
    try:
        # 读取A架数据
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 筛选当天数据
        start_time = pd.to_datetime(f"{date} 00:00:00")
        end_time = pd.to_datetime(f"{date} 23:59:59")
        daily_data = df[
            (df['csvTime'] >= start_time) &
            (df['csvTime'] <= end_time)
            ]

        if daily_data.empty:
            return None

        # 提取开机和关机时间
        power_on_times = daily_data[daily_data['status'] == '开机']
        power_off_times = daily_data[daily_data['status'] == '关机']

        if power_on_times.empty or power_off_times.empty:
            return None

        # 格式化时间点
        on_times = power_on_times['csvTime'].dt.strftime('%H:%M').tolist()
        off_times = power_off_times['csvTime'].dt.strftime('%H:%M').tolist()

        return {
            "function": "get_power_onoff_times",
            "result": {
                "power_on": on_times,
                "power_off": off_times
            }
        }

    except Exception as e:
        print(f"Error getting power on/off times: {e}")
        return None


#新加入的代码 获取指定日期征服者入水后A架摆回时间
def get_a_frame_return_time_after_entry(date):
    """
    获取指定日期征服者入水后A架摆回时间

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含A架摆回时间的结果
    """
    try:
        # 读取A架数据
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 筛选当天数据
        start_time = pd.to_datetime(f"{date} 00:00:00")
        end_time = pd.to_datetime(f"{date} 23:59:59")
        daily_data = df[
            (df['csvTime'] >= start_time) &
            (df['csvTime'] <= end_time)
            ]

        if daily_data.empty:
            return None

        # 找到每个征服者入水和之后的A架摆回时间点
        entry_times = daily_data[daily_data['status'] == '征服者入水'].index.tolist()
        return_times = daily_data[daily_data['status'] == 'A架摆回'].index.tolist()

        for entry_idx in entry_times:
            # 找到入水后的第一个摆回时间
            for return_idx in return_times:
                if return_idx > entry_idx:
                    return_time = daily_data.loc[return_idx, 'csvTime']
                    return {
                        "function": "get_a_frame_return_time_after_entry",
                        "result": return_time.strftime('%H:%M')
                    }

        return None

    except Exception as e:
        print(f"Error getting A-frame return time: {e}")
        return None


#新加入的代码 获取指定日期上午折臂吊车的开关机时间
def get_crane_power_times_morning(date):
    """
    获取指定日期上午折臂吊车的开关机时间

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含开关机时间的结果
    """
    try:
        # 读取折臂吊车数据
        df = pd.read_csv('database_in_use/device_13_11_meter_1311.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 筛选上午时段数据
        morning_start = pd.to_datetime(f"{date} 00:00:00")
        morning_end = pd.to_datetime(f"{date} 12:00:00")

        morning_data = df[
            (df['csvTime'] >= morning_start) &
            (df['csvTime'] <= morning_end)
            ]

        if morning_data.empty:
            return None

        # 获取开机和关机时间
        power_on_time = morning_data[
            morning_data['status'] == '折臂吊车开机'
            ]['csvTime'].iloc[0].strftime('%H:%M')

        power_off_time = morning_data[
            morning_data['status'] == '折臂吊车关机'
            ]['csvTime'].iloc[0].strftime('%H:%M')

        return {
            "function": "get_crane_power_times_morning",
            "result": {
                "power_on": power_on_time,
                "power_off": power_off_time
            }
        }

    except Exception as e:
        print(f"Error getting crane power times: {e}")
        return None


#新加入的代码 获取指定日期和时间段的折臂吊车开关机时间
def get_crane_power_times(date, period=None):
    """
    获取指定日期和时间段的折臂吊车开关机时间

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
        period (str, optional): 时间段，如'上午'/'下午'/None
                              None表示全天
    Returns:
        dict: 包含开关机时间的结果
    """

    print("period:", period)
    try:
        # 读取折臂吊车数据
        df = pd.read_csv('database_in_use/device_13_11_meter_1311.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 设置时间范围
        start_time = pd.to_datetime(f"{date} 00:00:00")
        end_time = pd.to_datetime(f"{date} 23:59:59")

        # 根据时间段筛选数据
        if period == '上午':
            end_time = pd.to_datetime(f"{date} 12:00:00")
        elif period == '下午':
            start_time = pd.to_datetime(f"{date} 12:00:00")

        # 筛选指定时间段数据
        period_data = df[
            (df['csvTime'] >= start_time) &
            (df['csvTime'] <= end_time)
            ]

        if period_data.empty:
            return None

        # 查找开关机时间点
        power_times = {
            'power_on': [],
            'power_off': []
        }

        # 获取所有开机时间点
        on_times = period_data[
            period_data['status'] == '折臂吊车开机'
            ]['csvTime'].dt.strftime('%H:%M').tolist()

        # 获取所有关机时间点
        off_times = period_data[
            period_data['status'] == '折臂吊车关机'
            ]['csvTime'].dt.strftime('%H:%M').tolist()

        return {
            "function": "get_crane_power_times",
            "result": {
                "power_on": on_times,
                "power_off": off_times
            }
        }

    except Exception as e:
        print(f"Error getting crane power times: {e}")
        return None


#新加入的代码 获取发电机组的功率测量范围
def get_generator_power_range(generator_name="一号柴油发电机组", parameter_type="有功功率测量"):
    """
    获取发电机组的功率测量范围

    Args:
        generator_name (str): 发电机组名称
        parameter_type (str): 参数类型
    Returns:
        dict: 包含功率范围的结果
    """
    try:
        # 读取设备参数详情表
        df = pd.read_csv('database_in_use/设备参数详情表.csv')

        # 构建查询条件
        query_name = f"{generator_name}{parameter_type}"

        # 查找对应参数
        param_info = df[df['Channel_Text_CN'] == query_name]

        if param_info.empty:
            return None

        # 获取范围值
        range_low = param_info['Alarm_Information_Range_Low'].iloc[0]
        range_high = param_info['Alarm_Information_Range_High'].iloc[0]

        return {
            "function": "get_generator_power_range",
            "result": {
                "low": range_low,
                "high": range_high
            }
        }

    except Exception as e:
        print(f"Error getting generator power range: {e}")
        return None


#新加入的代码 计算A架的实际运行时长和效率
def calculate_operation_time_and_efficiency(date):
    """
    计算A架的实际运行时长和效率

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含运行时长和效率的结果
    """
    try:
        # 读取A架数据
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 获取当天数据
        start_time = pd.to_datetime(f"{date} 00:00:00")
        end_time = pd.to_datetime(f"{date} 23:59:59")
        daily_data = df[
            (df['csvTime'] >= start_time) &
            (df['csvTime'] <= end_time)
            ].copy()

        if daily_data.empty:
            return None

        # 计算开机时长（开机到关机的总时间）
        power_cycles = []
        power_on = None

        for idx, row in daily_data.iterrows():
            if row['status'] == '开机':
                power_on = row['csvTime']
            elif row['status'] == '关机' and power_on is not None:
                power_cycles.append((power_on, row['csvTime']))
                power_on = None

        total_power_time = sum(
            (end - start).total_seconds()
            for start, end in power_cycles
        ) / 60  # 转换为分钟

        # 计算实际运行时长（有电流的时间）
        daily_data['Ajia-3_v'] = pd.to_numeric(daily_data['Ajia-3_v'], errors='coerce')
        daily_data['Ajia-5_v'] = pd.to_numeric(daily_data['Ajia-5_v'], errors='coerce')

        # 标记有电流的时间段
        daily_data['has_current'] = (
                (daily_data['Ajia-3_v'] > 0) |
                (daily_data['Ajia-5_v'] > 0)
        )

        # 计算有电流的时间段
        current_time = 0
        for _, group in daily_data.groupby((daily_data['has_current'] != daily_data['has_current'].shift()).cumsum()):
            if group['has_current'].iloc[0]:
                current_time += (group['csvTime'].max() - group['csvTime'].min()).total_seconds() / 60

        # 计算效率
        efficiency = (current_time / total_power_time * 100) if total_power_time > 0 else 0

        # 格式化结果
        hours = int(current_time // 60)
        minutes = int(current_time % 60)
        time_str = f"{hours:02d}:{minutes:02d}"

        return {
            "function": "calculate_operation_time_and_efficiency",
            "result": {
                "operation_time": time_str,
                "efficiency": round(efficiency, 2)
            }
        }

    except Exception as e:
        print(f"Error calculating operation time and efficiency: {e}")
        return None



#新加入的代码 计算A架外摆的最大角度范围及持续时间
def analyze_a_frame_swing_angles(date):
    """
    分析A架外摆的最大角度范围及持续时间

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含最大角度和持续时间的结果
    """
    try:
        # 读取A架数据
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 设置时间范围
        start_time = pd.to_datetime(f"{date} 00:00:00")
        end_time = pd.to_datetime(f"{date} 23:59:59")

        daily_data = df[
            (df['csvTime'] >= start_time) &
            (df['csvTime'] <= end_time)
            ].copy()

        if daily_data.empty:
            return None

        # 标记入水周期
        entry_phases = []
        start_idx = None
        for idx, row in daily_data.iterrows():
            if row['status'] == '征服者起吊':
                start_idx = idx
            elif row['status'] == 'A架摆回' and start_idx is not None:
                entry_phases.append((start_idx, idx))
                start_idx = None

        if not entry_phases:
            return None

        # 分析每个入水周期的角度数据
        max_angles = {'left': 0, 'right': 0}
        max_duration = 0
        max_duration_start = None

        for start_idx, end_idx in entry_phases:
            phase_data = daily_data.loc[start_idx:end_idx].copy()

            # 转换角度数据为数值类型
            phase_data['left_angle'] = pd.to_numeric(
                phase_data['Ajia-1_v'],
                errors='coerce'
            )
            phase_data['right_angle'] = pd.to_numeric(
                phase_data['Ajia-0_v'],
                errors='coerce'
            )

            # 获取最大角度
            max_left = phase_data['left_angle'].abs().max()
            max_right = phase_data['right_angle'].abs().max()

            if max_left > max_angles['left']:
                max_angles['left'] = max_left
            if max_right > max_angles['right']:
                max_angles['right'] = max_right

            # 计算最大角度持续时间
            mask = (phase_data['left_angle'].abs() >= max_left * 0.95) | \
                   (phase_data['right_angle'].abs() >= max_right * 0.95)

            continuous_periods = phase_data[mask].groupby(
                (phase_data[mask]['csvTime'].diff() > pd.Timedelta('1min')).cumsum()
            )

            for _, period in continuous_periods:
                duration = (period['csvTime'].max() - period['csvTime'].min()).total_seconds() / 60
                if duration > max_duration:
                    max_duration = duration
                    max_duration_start = period['csvTime'].min()

        # 格式化持续时间
        hours = int(max_duration // 60)
        minutes = int(max_duration % 60)

        analyze_result =  {
            "function": "analyze_a_frame_swing_angles",
            "result": {
                "left_angle": round(max_angles['left'], 2),
                "right_angle": round(max_angles['right'], 2),
                "duration": f"{hours:02d}:{minutes:02d}"
            }
        }

        return analyze_result

    except Exception as e:
        print(f"Error analyzing A-frame swing angles: {e}")
        return None



#新加入的代码 计算征服者入水到出水的时间间隔
def calculate_entry_to_ascend_duration(date):
    """
    计算征服者入水到出水的时间间隔

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含时间间隔的结果
    """
    try:
        # 读取A架数据
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 筛选当天数据
        start_time = pd.to_datetime(f"{date} 00:00:00")
        end_time = pd.to_datetime(f"{date} 23:59:59")
        daily_data = df[
            (df['csvTime'] >= start_time) &
            (df['csvTime'] <= end_time)
            ]

        if daily_data.empty:
            return None

        # 获取入水和出水时间点
        entry_times = daily_data[daily_data['status'] == '征服者入水']['csvTime']
        ascend_times = daily_data[daily_data['status'] == '征服者出水']['csvTime']

        if entry_times.empty or ascend_times.empty:
            return None

        # 获取第一次入水和对应的出水时间
        entry_time = entry_times.iloc[0]

        # 找到入水后的第一次出水时间
        ascend_time = ascend_times[ascend_times > entry_time].iloc[0]

        # 计算时间差（分钟）
        duration = (ascend_time - entry_time).total_seconds() / 60

        # 转换为小时和分钟
        hours = int(duration // 60)
        minutes = int(duration % 60)

        return {
            "function": "calculate_entry_to_ascend_duration",
            "result": f"{hours:02d}小时{minutes:02d}分钟"
        }

    except Exception as e:
        print(f"Error calculating entry to ascend duration: {e}")
        return None


#新加入的代码 计算征服者入水到A架摆回的时间间隔
def calculate_entry_to_return_duration(date):
    """
    计算征服者入水到A架摆回的时间间隔

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含时间间隔的结果（分钟）
    """
    try:
        # 读取A架数据
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 筛选当天数据
        start_time = pd.to_datetime(f"{date} 00:00:00")
        end_time = pd.to_datetime(f"{date} 23:59:59")
        daily_data = df[
            (df['csvTime'] >= start_time) &
            (df['csvTime'] <= end_time)
            ]

        if daily_data.empty:
            return None

        # 找到入水和摆回的时间点
        entry_times = daily_data[daily_data['status'] == '征服者入水']['csvTime']
        return_times = daily_data[daily_data['status'] == 'A架摆回']['csvTime']

        if entry_times.empty or return_times.empty:
            return None

        # 获取入水时间点
        entry_time = entry_times.iloc[0]

        # 找到入水后的第一次摆回时间
        return_time = return_times[return_times > entry_time].iloc[0]

        # 计算时间差（分钟）
        duration = int((return_time - entry_time).total_seconds() / 60)

        return {
            "function": "calculate_entry_to_return_duration",
            "result": duration,

        }

    except Exception as e:
        print(f"Error calculating entry to return duration: {e}")
        return None


#新加入的代码 获取发电机组转速的预警阈值
def get_generator_rpm_alarm_threshold(generator_name="停泊/应急发电机组"):
    """
    获取发电机组转速的预警阈值

    Args:
        generator_name (str): 发电机组名称
    Returns:
        dict: 包含预警阈值的结果
    """
    try:
        # 读取设备参数详情表
        df = pd.read_csv('database_in_use/设备参数详情表.csv')

        # 精确匹配转速参数
        rpm_param = df[
            df['Channel_Text_CN'].str.contains(
                f"{generator_name}.*转速",
                na=False
            )
        ].iloc[0]

        # 获取报警阈值
        alarm_value = rpm_param['Parameter_Information_Alarm']

        if pd.notna(alarm_value):
            return {
                "function": "get_generator_rpm_alarm_threshold",
                "result": alarm_value
            }

        return None

    except Exception as e:
        print(f"Error getting generator rpm alarm threshold: {e}")
        return None


def calculate_seated_to_shutdown_duration(date):
    """
    计算征服者落座到A架关机的时间间隔

    Args:
        date (str): 目标日期，格式'YYYY/MM/DD'
    Returns:
        dict: 包含时间间隔的结果（分钟）
    """
    try:
        # 读取A架数据
        df = pd.read_csv('database_in_use/Ajia_plc_1.csv')
        df['csvTime'] = pd.to_datetime(df['csvTime'])

        # 筛选当天数据
        start_time = pd.to_datetime(f"{date} 00:00:00")
        end_time = pd.to_datetime(f"{date} 23:59:59")
        daily_data = df[
            (df['csvTime'] >= start_time) &
            (df['csvTime'] <= end_time)
            ]

        if daily_data.empty:
            print(1)
            return None

        # 找到征服者落座和其后第一次A架关机的时间
        seated_time = daily_data[
            daily_data['status'] == '征服者落座'
            ]['csvTime'].iloc[-1]  # 取最后一次落座

        # 在落座时间之后找到第一次关机
        shutdown_times = daily_data[
            (daily_data['status'] == '关机') &
            (daily_data['csvTime'] > seated_time)
            ]['csvTime']

        if shutdown_times.empty:
            print(2)
            return None

        shutdown_time = shutdown_times.iloc[0]

        # 计算时间差（分钟）
        duration = int((shutdown_time - seated_time).total_seconds() / 60)

        return {
            "function": "calculate_seated_to_shutdown_duration",
            "result": duration
        }

    except Exception as e:
        print(f"Error calculating seated to shutdown duration: {e}")
        return None





if __name__ == "__main__":
    # 调用函数，查询指定时间段内的开机时长
    """
    start_time = '2024/8/23 0:00'
    end_time = '2024/8/23 12:00'
    uptime = calculate_uptime(start_time, end_time, shebeiname='折臂吊车')
    # 输出结果
    print(f"指定时间段内的开机时长: {uptime} 秒")
    uptime = compute_operational_duration(start_time, end_time, device_name='A架')
    # 输出结果
    print(f"指定时间段内的运行时长: {uptime} 秒")
    """
    # 示例调用
    # 示例调用
    table_name = "Ajia_plc_1"
    start_time = "2024-08-19 00:00:00"  # 开始时间
    end_time = "2024-08-19 23:59:59"  # 结束时间
    columns = ["csvTime", "status"]  # 需要查询的列名
    status = "开机"  # 筛选状态为 "开机"

    # 获取数据
    data = get_table_data(table_name, start_time, end_time, columns, status)
    # print(data)
    start_time = "2024-08-23 00:00:00"  # 开始时间
    end_time = "2024-08-23 11:59:59"
    device_name = "折臂吊车"

    # Correctly constructing the tuple

    # data = compute_operational_duration(start_time, end_time, device_name)

    print(data)
    data = calculate_uptime(start_time, end_time, device_name)

    print(data)

    start_time = "2024-08-24 00:00:00"  # 开始时间
    end_time = "2024-08-24 11:59:59"
    device_name = "折臂吊车"

    print(calculate_total_energy(start_time, end_time, device_name=device_name))
    print(calculate_total_deck_machinery_energy(start_time, end_time))

    # 获取数据
    data = get_table_data(table_name, start_time, end_time, columns, status)
    # print(data)
    start_time = "2024-08-23 00:00:00"  # 开始时间
    end_time = "2024-08-23 11:59:59"
    device_name = "A架"

    # Correctly constructing the tuple

    data = compute_operational_duration(start_time, end_time, device_name)

    print(data)

    start_time = "2024-08-23 12:00:00"  # 开始时间
    end_time = "2024-08-23 23:59:59"
    device_name = "A架"

    data = calculate_uptime(start_time, end_time, device_name)

    print(data)
