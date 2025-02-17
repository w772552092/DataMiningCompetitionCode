# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 10:41:39 2024

@author: 86187
"""

tools_all = [
    {
        "type": "function",
        "function": {
            "name": "get_table_data",
            "description": "根据数据表名、开始时间、结束时间、列名和状态获取指定时间范围内的相关数据。返回值为包含指定列名和对应值的字典。",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "数据表名，例如 'device_logs'。",
                    },
                    "start_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "查询的开始时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如 '2024-08-23 00:00:00'。",
                    },
                    "end_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "查询的结束时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如 '2024-08-23 12:00:00'。",
                    },
                    "columns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "需要查询的列名列表。如果未提供，则返回所有列。",
                        "default": [],
                    },
                    "status": {
                        "type": "string",
                        "description": "需要筛选的状态（例如 '开机'、'关机'）。如果未提供，则不筛选状态。",
                        "default": "",
                    },
                },
                "required": ["table_name", "start_time", "end_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_total_energy",
            "description": "计算指定时间段内指定设备的总能耗。返回值为总能耗（kWh，float 类型）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "查询的开始时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如 '2024-08-23 00:00:00'。",
                    },
                    "end_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "查询的结束时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如 '2024-08-23 12:00:00'。",
                    },
                    "device_name": {
                        "type": "string",
                        "description": "设备名称，支持以下值：'折臂吊车'、'一号门架'、'二号门架'、'绞车'",
                        "enum": ["折臂吊车", "一号门架", "二号门架", "绞车"],
                    },
                },
                "required": ["start_time", "end_time", "device_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_total_deck_machinery_energy",
            "description": "计算甲板机械设备在指定时间范围内的总能耗。返回值为总能耗（kWh，float 类型）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "查询的开始时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如 '2024-08-23 00:00:00'。",
                    },
                    "end_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "查询的结束时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如 '2024-08-23 12:00:00'。",
                    },
                },
                "required": ["start_time", "end_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_device_parameter",
            "description": "通过参数中文名查询设备参数信息。返回包含参数信息的字典。",
            "parameters": {
                "type": "object",
                "properties": {
                    "parameter_name_cn": {
                        "type": "string",
                        "description": "参数中文名，用于查询设备参数信息。",
                    }
                },
                "required": ["parameter_name_cn"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_device_status_by_time_range",
            "description": "根据开始时间和结束时间，查询设备设备在进行什么动作。返回正在进行设备动作",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "查询的开始时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如 '2024-08-23 00:00:00'。",
                    },
                    "end_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "查询的结束时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如 '2024-08-23 12:00:00'。",
                    },
                },
                "required": ["start_time", "end_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_uptime",
            "description": "计算指定时间段内的开机时长，并返回三种格式的开机时长。设备名称支持 '折臂吊车'、'A架' 和 'DP'。",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "查询的开始时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如 '2024-08-23 00:00:00'。",
                    },
                    "end_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "查询的结束时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如 '2024-08-23 12:00:00'。",
                    },
                    "shebeiname": {
                        "type": "string",
                        "enum": ["折臂吊车", "A架", "DP"],
                        "description": "设备名称，支持 '折臂吊车'、'A架' 和 'DP'，默认为 '折臂吊车'。",
                        "default": "折臂吊车",
                    },
                },
                "required": ["start_time", "end_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compute_operational_duration",
            "description": "计算指定时间段内设备的运行时长，并返回三种格式的运行时长。设备名称支持 'A架'。",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "查询的开始时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如 '2024-08-23 00:00:00'。",
                    },
                    "end_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "查询的结束时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如 '2024-08-23 12:00:00'。",
                    },
                    "device_name": {
                        "type": "string",
                        "enum": ["A架"],
                        "description": "设备名称，支持 'A架'，默认为 'A架'。",
                        "default": "A架",
                    },
                },
                "required": ["start_time", "end_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_operation_start_time",
            "description": "获取指定日期深海作业A的开始时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_date": {
                        "type": "string",
                        "description": "目标日期，格式为 'YYYY/MM/DD'",
                    }
                },
                "required": ["target_date"]
            }
        }
    },



#新加入
    {
    "type": "function",
    "function": {
        "name": "calculate_efficiency",
        "description": "计算设备效率，返回实际运行时长和效率",
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "开始时间，格式为 'YYYY-MM-DD HH:MM:SS'",
                },
                "end_time": {
                    "type": "string",
                    "format": "date-time",
                    "description": "结束时间，格式为 'YYYY-MM-DD HH:MM:SS'",
                },
                "device_name": {
                    "type": "string",
                    "description": "设备名称，默认为'A架'",
                    "default": "A架",
                },
            },
            "required": ["start_time", "end_time"],
        },
    },
},
#新加入
    {
    "type": "function",
    "function": {
        "name": "get_operation_end_time",
        "description": "获取深海作业A的结束时间（以征服者落座为标志）",
        "parameters": {
            "type": "object",
            "properties": {
                "target_date": {
                    "type": "string",
                    "description": "目标日期，格式为 'YYYY/MM/DD'"
                }
            },
            "required": ["target_date"]
        }
    }
},
#新加入
    {
    "type": "function",
    "function": {
        "name": "compare_device_startup_order",
        "description": "比较A架和折臂吊车开机时间的先后顺序",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式为 'YYYY/MM/DD'"
                },
                "period": {
                    "type": "string",
                    "description": "时间段，morning或afternoon",
                    "default": "afternoon"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入
    {
    "type": "function",
    "function": {
        "name": "compare_operation_durations",
        "description": "比较上午运行时长和下午开机时长",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式为 'YYYY/MM/DD'"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入
    {
    "type": "function",
    "function": {
        "name": "calculate_action_time_diff",
        "description": "计算两个设备动作之间的时间差",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式为 'YYYY/MM/DD'"
                },
                "action1": {
                    "type": "string",
                    "description": "第一个动作名称"
                },
                "action2": {
                    "type": "string",
                    "description": "第二个动作名称"
                }
            },
            "required": ["date", "action1", "action2"]
        }
    }
},
#新加入
    {
    "type": "function",
    "function": {
        "name": "find_longest_morning_operation",
        "description": "查找指定日期范围内上午运行时长最长的一天",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "起始日期，格式为 'YYYY/MM/DD'"
                },
                "end_date": {
                    "type": "string",
                    "description": "结束日期，格式为 'YYYY/MM/DD'"
                },
                "device_name": {
                    "type": "string",
                    "description": "设备名称",
                    "default": "A架"
                }
            },
            "required": ["start_date", "end_date"]
        }
    }
},
#新加入
    {
    "type": "function",
    "function": {
        "name": "calculate_average_morning_runtime",
        "description": "计算两个日期上午的平均运行时间",
        "parameters": {
            "type": "object",
            "properties": {
                "date1": {
                    "type": "string",
                    "description": "第一个日期，格式'YYYY/MM/DD'"
                },
                "date2": {
                    "type": "string",
                    "description": "第二个日期，格式'YYYY/MM/DD'"
                },
                "device_name": {
                    "type": "string",
                    "description": "设备名称",
                    "default": "A架"
                }
            },
            "required": ["date1", "date2"]
        }
    }
},
#新加入
    {
    "type": "function",
    "function": {
        "name": "calculate_thruster_energy_during_dp",
        "description": "计算DP过程中侧推的总能耗",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD'"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入 计算多天DP过程中侧推的平均能耗
    {
    "type": "function",
    "function": {
        "name": "calculate_average_thruster_energy_during_dp",
        "description": "计算多天DP过程中侧推的平均能耗",
        "parameters": {
            "type": "object",
            "properties": {
                "dates": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "日期列表，格式为['YYYY/MM/DD', 'YYYY/MM/DD']"
                }
            },
            "required": ["dates"]
        }
    }
},
#新加入 计算DP过程中推进系统的总能耗
    {
    "type": "function",
    "function": {
        "name": "calculate_propulsion_energy_during_dp",
        "description": "计算DP过程中推进系统的总能耗",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD'"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入 计算折臂吊车能耗占甲板机械设备的比例
    {
    "type": "function",
    "function": {
        "name": "calculate_crane_energy_ratio",
        "description": "计算折臂吊车能耗占甲板机械设备的比例",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD'"
                },
                "period": {
                    "type": "string",
                    "description": "时间段，morning或afternoon",
                    "default": "morning"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入 查找能耗最大的发电机
    {
    "type": "function",
    "function": {
        "name": "find_max_generator_energy",
        "description": "查找能耗最大的发电机",
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "description": "开始时间，格式'YYYY/MM/DD HH:MM:SS'"
                },
                "end_time": {
                    "type": "string",
                    "description": "结束时间，格式'YYYY/MM/DD HH:MM:SS'"
                }
            },
            "required": ["start_time", "end_time"]
        }
    }
},
#新加入 计算小艇入水到落座期间折臂吊车的总能耗
    {
    "type": "function",
    "function": {
        "name": "calculate_crane_energy_between_boat_states",
        "description": "计算小艇入水到落座期间折臂吊车的总能耗",
        "parameters": {
            "type": "object",
            "properties": {
                "date1": {
                    "type": "string",
                    "description": "第一个日期，格式'YYYY/MM/DD'"
                },
                "date2": {
                    "type": "string",
                    "description": "第二个日期，格式'YYYY/MM/DD'"
                }
            },
            "required": ["date1", "date2"]
        }
    }
},
#新加入 获取A架和折臂吊车的运行时间
    {
    "type": "function",
    "function": {
        "name": "get_devices_runtime",
        "description": "获取A架和折臂吊车的运行时间",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD'"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入 计算A架和折臂吊车的运行时间差值
    {
    "type": "function",
    "function": {
        "name": "calculate_runtime_difference",
        "description": "计算A架和折臂吊车的运行时间差值",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD'"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入 计算多天A架的平均摆动次数
    {
    "type": "function",
    "function": {
        "name": "calculate_average_swing_count",
        "description": "计算多天A架的平均摆动次数",
        "parameters": {
            "type": "object",
            "properties": {
                "dates": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "日期列表，格式为['YYYY/MM/DD']"
                }
            },
            "required": ["dates"]
        }
    }
},
#新加入 计算多天的平均作业时长
    {
    "type": "function",
    "function": {
        "name": "calculate_average_operation_time",
        "description": "计算多天的平均作业时长",
        "parameters": {
            "type": "object",
            "properties": {
                "dates": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "日期列表，格式['YYYY/MM/DD']"
                }
            },
            "required": ["dates"]
        }
    }
},
#新加入 测A架角度数据的异常情况
    {
        "type": "function",
        "function": {
            "name": "detect_angle_anomalies",
            "description": "检测A架角度数据为error的异常情况",
            "parameters": {
                "type": "object",
                "properties": {},  # 移除之前的参数定义，因为不需要传入参数
                "required": []
            }
        }
    },
#新加入 计算发电机组的总燃油消耗量
    {
    "type": "function",
    "function": {
        "name": "calculate_total_fuel_consumption",
        "description": "计算发电机组的总燃油消耗量",
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "description": "开始时间，格式'YYYY/MM/DD HH:MM:SS'"
                },
                "end_time": {
                    "type": "string",
                    "description": "结束时间，格式'YYYY/MM/DD HH:MM:SS'"
                }
            },
            "required": ["start_time", "end_time"]
        }
    }
},
#新加入 计算所有发电机组的总发电量
    {
    "type": "function",
    "function": {
        "name": "calculate_total_power_generation",
        "description": "计算所有发电机组的总发电量",
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "description": "开始时间，格式'YYYY/MM/DD HH:MM:SS'"
                },
                "end_time": {
                    "type": "string",
                    "description": "结束时间，格式'YYYY/MM/DD HH:MM:SS'"
                }
            },
            "required": ["start_time", "end_time"]
        }
    }
},
#新加入 计算推进系统能耗占总发电量的比例
    {
    "type": "function",
    "function": {
        "name": "calculate_propulsion_energy_ratio",
        "description": "计算推进系统能耗占总发电量的比例",
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "description": "开始时间，格式'YYYY/MM/DD HH:MM:SS'"
                },
                "end_time": {
                    "type": "string",
                    "description": "结束时间，格式'YYYY/MM/DD HH:MM:SS'"
                }
            },
            "required": ["start_time", "end_time"]
        }
    }
},
#新加入 计算甲板机械能耗占总发电量的比例
    {
    "type": "function",
    "function": {
        "name": "calculate_deck_machinery_power_ratio",
        "description": "计算甲板机械能耗占总发电量的比例",
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "description": "开始时间，格式'YYYY/MM/DD HH:MM:SS'"
                },
                "end_time": {
                    "type": "string",
                    "description": "结束时间，格式'YYYY/MM/DD HH:MM:SS'"
                }
            },
            "required": ["start_time", "end_time"]
        }
    }
},
#新加入 计算平均作业能耗（包括下放和回收阶段）
    {
    "type": "function",
    "function": {
        "name": "calculate_average_operation_energy",
        "description": "计算平均作业能耗（包括下放和回收阶段）",
        "parameters": {
            "type": "object",
            "properties": {
                "dates": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "日期列表，格式['YYYY/MM/DD']"
                }
            },
            "required": ["dates"]
        }
    }
},
#新加入 计算柴油发电机组的理论发电量
    {
    "type": "function",
    "function": {
        "name": "calculate_theoretical_power_generation",
        "description": "计算柴油发电机组的理论发电量",
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "description": "开始时间，格式'YYYY/MM/DD HH:MM:SS'"
                },
                "end_time": {
                    "type": "string",
                    "description": "结束时间，格式'YYYY/MM/DD HH:MM:SS'"
                },
                "oil_density": {
                    "type": "number",
                    "description": "柴油密度(kg/L)",
                    "default": 0.8448
                },
                "oil_heat_value": {
                    "type": "number",
                    "description": "柴油热值(MJ/kg)",
                    "default": 42.6
                }
            },
            "required": ["start_time", "end_time"]
        }
    }
},
#新加入 计算柴油发电机组的理论发电量
    {
    "type": "function",
    "function": {
        "name": "calculate_generator_efficiency",
        "description": "计算柴油机发电效率",
        "parameters": {
            "type": "object",
            "properties": {
                "start_time": {
                    "type": "string",
                    "description": "开始时间，格式'YYYY/MM/DD HH:MM:SS'"
                },
                "end_time": {
                    "type": "string",
                    "description": "结束时间，格式'YYYY/MM/DD HH:MM:SS'"
                }
            },
            "required": ["start_time", "end_time"]
        }
    }
},
#新加入 计算征服者在指定时间前出水的比例
    {
    "type": "function",
    "function": {
        "name": "calculate_conqueror_ascend_ratio",
        "description": "计算征服者在指定时间前出水的比例",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "开始日期，格式'YYYY/MM/DD'"
                },
                "end_date": {
                    "type": "string",
                    "description": "结束日期，格式'YYYY/MM/DD'"
                },
                "time_threshold": {
                    "type": "string",
                    "description": "时间阈值，格式'HH:MM:SS'",
                    "default": "16:00:00"
                }
            },
            "required": ["start_date", "end_date"]
        }
    }
},
#新加入 计算早于指定时间开始作业的比例
    {
    "type": "function",
    "function": {
        "name": "calculate_early_operation_ratio",
        "description": "计算早于指定时间开始作业的比例",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "开始日期，格式'YYYY/MM/DD'"
                },
                "end_date": {
                    "type": "string",
                    "description": "结束日期，格式'YYYY/MM/DD'"
                },
                "time_threshold": {
                    "type": "string",
                    "description": "时间阈值，格式'HH:MM:SS'",
                    "default": "09:00:00"
                }
            },
            "required": ["start_date", "end_date"]
        }
    }
},
#新加入 计算征服者在指定时间前入水的比例
    {
    "type": "function",
    "function": {
        "name": "calculate_conqueror_entry_ratio",
        "description": "计算征服者在指定时间前入水的比例",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "开始日期，格式'YYYY/MM/DD'"
                },
                "end_date": {
                    "type": "string",
                    "description": "结束日期，格式'YYYY/MM/DD'"
                },
                "time_threshold": {
                    "type": "string",
                    "description": "时间阈值，格式'HH:MM:SS'",
                    "default": "09:00:00"
                }
            },
            "required": ["start_date", "end_date"]
        }
    }
},
#新加入 获取A架的开关机时间点
    {
    "type": "function",
    "function": {
        "name": "get_power_onoff_times",
        "description": "获取A架的开关机时间点",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD'"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入 获取征服者入水后A架摆回到位的时间
    {
    "type": "function",
    "function": {
        "name": "get_a_frame_return_time_after_entry",
        "description": "获取征服者入水后A架摆回到位的时间",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD'"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入 获取折臂吊车的开关机时间
    {
    "type": "function",
    "function": {
        "name": "get_crane_power_times",
        "description": "获取折臂吊车的开关机时间",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD'"
                },
                "period": {
                    "type": "string",
                    "description": "时间段，可选值：上午/下午/None",
                    "enum": ["上午", "下午", None]
                }
            },
            "required": ["date"]
        }
    }
},
#新加入 获取发电机组的功率测量范围
    {
    "type": "function",
    "function": {
        "name": "get_generator_power_range",
        "description": "获取发电机组的功率测量范围",
        "parameters": {
            "type": "object",
            "properties": {
                "generator_name": {
                    "type": "string",
                    "description": "发电机组名称",
                    "default": "一号柴油发电机组"
                },
                "parameter_type": {
                    "type": "string",
                    "description": "参数类型",
                    "default": "有功功率测量"
                }
            },
            "required": []
        }
    }
},
#新加入 计算A架的实际运行时长和效率
    {
    "type": "function",
    "function": {
        "name": "calculate_operation_time_and_efficiency",
        "description": "计算A架的实际运行时长和效率",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD'"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入 计算A架的摆动次数和持续时间
    {
    "type": "function",
    "function": {
        "name": "analyze_a_frame_swing_angles",
        "description": "分析A架外摆的最大角度范围及持续时间",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD' 如果没有提供年份，则默认为2024年"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入 计算征服者入水到出水的时间间隔
    {
    "type": "function",
    "function": {
        "name": "calculate_entry_to_ascend_duration",
        "description": "计算征服者入水到出水的时间间隔",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD'"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入 计算征服者入水到A架摆回的时间间隔
    {
    "type": "function",
    "function": {
        "name": "calculate_entry_to_return_duration",
        "description": "计算征服者入水到A架摆回的时间间隔,返回值为时间间隔（分钟）",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD' 如果没有提供年份，则默认为2024年"
                }
            },
            "required": ["date"]
        }
    }
},
#新加入 获取发电机组转速的预警阈值
    {
    "type": "function",
    "function": {
        "name": "get_generator_rpm_alarm_threshold",
        "description": "获取发电机组转速的预警阈值",
        "parameters": {
            "type": "object",
            "properties": {
                "generator_name": {
                    "type": "string",
                    "description": "发电机组名称",
                    "default": "停泊/应急发电机组"
                }
            },
            "required": []
        }
    }
},
#新加入 计算征服者落座到A架关机的时间间隔
    {
    "type": "function",
    "function": {
        "name": "calculate_seated_to_shutdown_duration",
        "description": "计算征服者落座到A架关机的时间间隔,返回值为时间间隔（分钟）",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "目标日期，格式'YYYY/MM/DD' 如果没有提供年份，则默认为2024年"
                }
            },
            "required": ["date"]
        }
    }
}
]
