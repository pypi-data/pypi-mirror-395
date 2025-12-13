#!/usr/bin/env python3
import json
import sys
import requests
import logging
import time

logging.disable(logging.CRITICAL)

def get_token(qinglong_url, client_id, client_secret):
    try:
        url = f"{qinglong_url}/open/auth/token"
        params = {"client_id": client_id, "client_secret": client_secret}
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        return result["data"]["token"] if result.get("code") == 200 else None
    except Exception:
        return None

def main():
    for line in sys.stdin:
        request = None
        try:
            line = line.strip()
            if not line:
                continue
            
            request = json.loads(line)
            method = request.get("method")
            
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request["id"],
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "qinglong-mcp-cloud", "version": "1.0.0"}
                    }
                }
                print(json.dumps(response), flush=True)
            elif method == "notifications/initialized":
                pass  # Notifications don't require response
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": request["id"],
                    "result": {
                        "tools": [
                            {
                                "name": "list_qinglong_tasks",
                                "description": "查询青龙面板中的所有定时任务列表",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "qinglong_url": {"type": "string", "description": "青龙面板 URL"},
                                        "client_id": {"type": "string", "description": "Client ID"},
                                        "client_secret": {"type": "string", "description": "Client Secret"}
                                    },
                                    "required": ["qinglong_url", "client_id", "client_secret"]
                                }
                            },
                            {
                                "name": "run_task",
                                "description": "执行任务并等待完成，返回执行日志（最多等待30秒）",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "qinglong_url": {"type": "string", "description": "青龙面板 URL"},
                                        "client_id": {"type": "string", "description": "Client ID"},
                                        "client_secret": {"type": "string", "description": "Client Secret"},
                                        "task_id": {"type": "integer", "description": "任务 ID"}
                                    },
                                    "required": ["qinglong_url", "client_id", "client_secret", "task_id"]
                                }
                            },
                            {
                                "name": "run_task_async",
                                "description": "异步启动任务，不等待执行完成",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "qinglong_url": {"type": "string", "description": "青龙面板 URL"},
                                        "client_id": {"type": "string", "description": "Client ID"},
                                        "client_secret": {"type": "string", "description": "Client Secret"},
                                        "task_id": {"type": "integer", "description": "任务 ID"}
                                    },
                                    "required": ["qinglong_url", "client_id", "client_secret", "task_id"]
                                }
                            },
                            {
                                "name": "get_task_logs",
                                "description": "获取青龙面板中指定任务的执行日志",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "qinglong_url": {"type": "string", "description": "青龙面板 URL"},
                                        "client_id": {"type": "string", "description": "Client ID"},
                                        "client_secret": {"type": "string", "description": "Client Secret"},
                                        "task_id": {"type": "integer", "description": "任务 ID"}
                                    },
                                    "required": ["qinglong_url", "client_id", "client_secret", "task_id"]
                                }
                            },
                            {
                                "name": "get_task_status",
                                "description": "获取青龙面板中指定任务的执行状态",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "qinglong_url": {"type": "string", "description": "青龙面板 URL"},
                                        "client_id": {"type": "string", "description": "Client ID"},
                                        "client_secret": {"type": "string", "description": "Client Secret"},
                                        "task_id": {"type": "integer", "description": "任务 ID"}
                                    },
                                    "required": ["qinglong_url", "client_id", "client_secret", "task_id"]
                                }
                            }
                        ]
                    }
                }
                print(json.dumps(response), flush=True)
            elif method == "tools/call":
                tool_name = request["params"]["name"]
                arguments = request["params"]["arguments"]
                
                qinglong_url = arguments.get("qinglong_url")
                client_id = arguments.get("client_id")
                client_secret = arguments.get("client_secret")
                
                if not all([qinglong_url, client_id, client_secret]):
                    response = {
                        "jsonrpc": "2.0",
                        "id": request["id"],
                        "error": {"code": -32602, "message": "缺少必需参数: qinglong_url, client_id, client_secret"}
                    }
                    print(json.dumps(response), flush=True)
                    continue
                
                token = get_token(qinglong_url, client_id, client_secret)
                if not token:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request["id"],
                        "error": {"code": -32603, "message": "获取 token 失败，请检查凭证是否正确"}
                    }
                    print(json.dumps(response), flush=True)
                    continue
                
                if tool_name == "list_qinglong_tasks":
                    try:
                        url = f"{qinglong_url}/open/crons"
                        headers = {"Authorization": f"Bearer {token}"}
                        resp = requests.get(url, headers=headers, timeout=10)
                        result = resp.json()
                    except Exception as e:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "error": {"code": -32603, "message": f"请求失败: {str(e)}"}
                        }
                        print(json.dumps(response), flush=True)
                        continue
                    
                    if result.get("code") == 200:
                        data = result["data"]
                        crons = data.get("data", [])
                        crons.sort(key=lambda x: x.get('id', 0))
                        total = data.get("total", 0)
                        
                        output = f"青龙面板: {qinglong_url}\n共 {total} 个任务:\n\n"
                        for cron in crons:
                            output += f"ID: {cron.get('id')}\n"
                            output += f"名称: {cron.get('name')}\n"
                            output += f"命令: {cron.get('command')}\n"
                            output += f"定时: {cron.get('schedule')}\n"
                            output += f"状态: {'启用' if cron.get('isDisabled') == 0 else '禁用'}\n"
                            last_running = cron.get('last_running_time')
                            if last_running:
                                output += f"上次运行时长: {last_running}秒\n"
                            output += "-" * 50 + "\n"
                        
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "result": {"content": [{"type": "text", "text": output}]}
                        }
                    else:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "error": {"code": -32603, "message": f"获取任务列表失败: {result}"}
                        }
                
                elif tool_name == "run_task_async":
                    task_id = arguments.get("task_id")
                    try:
                        url = f"{qinglong_url}/open/crons/run"
                        headers = {"Authorization": f"Bearer {token}"}
                        data = [task_id]
                        
                        resp = requests.put(url, headers=headers, json=data, timeout=10)
                        result = resp.json()
                    except Exception as e:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "error": {"code": -32603, "message": f"请求失败: {str(e)}"}
                        }
                        print(json.dumps(response), flush=True)
                        continue
                    
                    if result.get("code") == 200:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "result": {"content": [{"type": "text", "text": f"任务 {task_id} 已成功启动"}]}
                        }
                    else:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "error": {"code": -32603, "message": f"运行任务失败: {result}"}
                        }
                
                elif tool_name == "get_task_logs":
                    task_id = arguments.get("task_id")
                    try:
                        url = f"{qinglong_url}/open/crons/{task_id}"
                        headers = {"Authorization": f"Bearer {token}"}
                        resp = requests.get(url, headers=headers, timeout=10)
                        result = resp.json()
                    except Exception as e:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "error": {"code": -32603, "message": f"请求失败: {str(e)}"}
                        }
                        print(json.dumps(response), flush=True)
                        continue
                    
                    if result.get("code") == 200:
                        cron = result["data"]
                        log_path = cron.get("log_path", "")
                        
                        if log_path:
                            try:
                                log_url = f"{qinglong_url}/open/crons/{task_id}/log"
                                log_resp = requests.get(log_url, headers=headers, timeout=10)
                                log_result = log_resp.json()
                                
                                if log_result.get("code") == 200:
                                    log_content = log_result["data"]
                                    output = f"任务 {task_id} ({cron.get('name')}) 的执行日志:\n\n{log_content}"
                                else:
                                    output = f"获取日志失败: {log_result}"
                            except Exception as e:
                                output = f"读取日志失败: {str(e)}"
                        else:
                            output = f"任务 {task_id} ({cron.get('name')}) 暂无执行日志"
                        
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "result": {"content": [{"type": "text", "text": output}]}
                        }
                    else:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "error": {"code": -32603, "message": f"获取任务信息失败: {result}"}
                        }
                
                elif tool_name == "get_task_status":
                    task_id = arguments.get("task_id")
                    try:
                        url = f"{qinglong_url}/open/crons/{task_id}"
                        headers = {"Authorization": f"Bearer {token}"}
                        resp = requests.get(url, headers=headers, timeout=10)
                        result = resp.json()
                    except Exception as e:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "error": {"code": -32603, "message": f"请求失败: {str(e)}"}
                        }
                        print(json.dumps(response), flush=True)
                        continue
                    
                    if result.get("code") == 200:
                        cron = result["data"]
                        status_map = {0: "运行中", 1: "空闲", 2: "禁用"}
                        status = status_map.get(cron.get("status"), "未知")
                        
                        output = f"任务 {task_id} 状态信息:\n\n"
                        output += f"名称: {cron.get('name')}\n"
                        output += f"状态: {status}\n"
                        output += f"是否禁用: {'是' if cron.get('isDisabled') == 1 else '否'}\n"
                        output += f"是否置顶: {'是' if cron.get('isPinned') == 1 else '否'}\n"
                        last_running = cron.get('last_running_time')
                        output += f"上次运行时长: {last_running}秒\n" if last_running else "上次运行时长: 未运行\n"
                        output += f"最后执行时间: {cron.get('last_execution_time', '未执行')}\n"
                        
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "result": {"content": [{"type": "text", "text": output}]}
                        }
                    else:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "error": {"code": -32603, "message": f"获取任务状态失败: {result}"}
                        }
                
                elif tool_name == "run_task":
                    task_id = arguments.get("task_id")
                    headers = {"Authorization": f"Bearer {token}"}
                    
                    try:
                        url = f"{qinglong_url}/open/crons/run"
                        resp = requests.put(url, headers=headers, json=[task_id], timeout=10)
                        result = resp.json()
                        if result.get("code") != 200:
                            response = {
                                "jsonrpc": "2.0",
                                "id": request["id"],
                                "error": {"code": -32603, "message": f"启动任务失败: {result}"}
                            }
                            print(json.dumps(response), flush=True)
                            continue
                    except Exception as e:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "error": {"code": -32603, "message": f"启动任务失败: {str(e)}"}
                        }
                        print(json.dumps(response), flush=True)
                        continue
                    
                    time.sleep(2)
                    response = None
                    task_started = False
                    
                    for _ in range(6):
                        time.sleep(5)
                        try:
                            status_url = f"{qinglong_url}/open/crons/{task_id}"
                            status_resp = requests.get(status_url, headers=headers, timeout=10)
                            status_result = status_resp.json()
                            
                            if status_result.get("code") == 200:
                                cron = status_result["data"]
                                task_status = cron.get("status")
                                
                                # status: 0=运行中, 1=空闲
                                if task_status == 0:
                                    task_started = True
                                elif task_status == 1 and task_started:
                                    log_url = f"{qinglong_url}/open/crons/{task_id}/log"
                                    log_resp = requests.get(log_url, headers=headers, timeout=10)
                                    log_result = log_resp.json()
                                    
                                    if log_result.get("code") == 200:
                                        response = {
                                            "jsonrpc": "2.0",
                                            "id": request["id"],
                                            "result": {"content": [{"type": "text", "text": log_result["data"]}]}
                                        }
                                    else:
                                        response = {
                                            "jsonrpc": "2.0",
                                            "id": request["id"],
                                            "error": {"code": -32603, "message": f"获取日志失败: {log_result}"}
                                        }
                                    break
                        except Exception as e:
                            response = {
                                "jsonrpc": "2.0",
                                "id": request["id"],
                                "error": {"code": -32603, "message": f"检查任务失败: {str(e)}"}
                            }
                            break
                    
                    if response is None:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request["id"],
                            "result": {"content": [{"type": "text", "text": f"任务 {task_id} 超时（30秒），请使用 get_task_logs 查看日志"}]}
                        }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request["id"],
                        "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                    }
                
                print(json.dumps(response), flush=True)
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }
                print(json.dumps(response), flush=True)
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if request else None,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    main()
