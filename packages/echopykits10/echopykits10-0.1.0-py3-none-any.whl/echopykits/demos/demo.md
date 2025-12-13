



### 包含工具节点的app应用，schema定义

```json

{
    "edges": [
        {
            "id": "03dec5fe-3993-429b-a28e-abd19530c8f0",
            "type": "app-edge",
            "endPoint": {
                "x": -20,
                "y": 2790
            },
            "pointsList": [
                {
                    "x": -210,
                    "y": 2790
                },
                {
                    "x": -100,
                    "y": 2790
                },
                {
                    "x": -130,
                    "y": 2790
                },
                {
                    "x": -20,
                    "y": 2790
                }
            ],
            "properties": {

            },
            "startPoint": {
                "x": -210,
                "y": 2790
            },
            "sourceNodeId": "start-node",
            "targetNodeId": "01db845c-271e-4071-8371-991403cd76cd",
            "sourceAnchorId": "start-node_right",
            "targetAnchorId": "01db845c-271e-4071-8371-991403cd76cd_left"
        },
        {
            "id": "aad79fa2-37e4-4f5e-a0f8-19242d07d745",
            "type": "app-edge",
            "endPoint": {
                "x": 400,
                "y": 2550
            },
            "pointsList": [
                {
                    "x": 300,
                    "y": 2790
                },
                {
                    "x": 410,
                    "y": 2790
                },
                {
                    "x": 290,
                    "y": 2550
                },
                {
                    "x": 400,
                    "y": 2550
                }
            ],
            "properties": {

            },
            "startPoint": {
                "x": 300,
                "y": 2790
            },
            "sourceNodeId": "01db845c-271e-4071-8371-991403cd76cd",
            "targetNodeId": "77611157-e198-47ca-967b-3a7429088beb",
            "sourceAnchorId": "01db845c-271e-4071-8371-991403cd76cd_right",
            "targetAnchorId": "77611157-e198-47ca-967b-3a7429088beb_left"
        }
    ],
    "nodes": [
        {
            "x": -940,
            "y": 2950,
            "id": "base-node",
            "type": "base-node",
            "properties": {
                "config": {

                },
                "height": 772.148,
                "showNode": true,
                "stepName": "基本信息",
                "node_data": {
                    "desc": "工具节点测试",
                    "name": "工具节点测试",
                    "prologue": "你好",
                    "tts_type": "BROWSER"
                },
                "input_field_list": [

                ],
                "user_input_config": {
                    "title": "用户输入"
                },
                "api_input_field_list": [

                ],
                "chat_input_field_list": [

                ],
                "user_input_field_list": [

                ]
            }
        },
        {
            "x": -370,
            "y": 2790,
            "id": "start-node",
            "type": "start-node",
            "properties": {
                "config": {
                    "fields": [
                        {
                            "label": "用户问题",
                            "value": "question"
                        }
                    ],
                    "chatFields": [

                    ],
                    "globalFields": [
                        {
                            "label": "当前时间",
                            "value": "time"
                        },
                        {
                            "label": "历史聊天记录",
                            "value": "history_context"
                        },
                        {
                            "label": "对话 ID",
                            "value": "chat_id"
                        },
                        {
                            "label": "对话用户 ID",
                            "value": "chat_user_id"
                        },
                        {
                            "label": "对话用户类型",
                            "value": "chat_user_type"
                        },
                        {
                            "label": "对话用户",
                            "value": "chat_user"
                        }
                    ]
                },
                "fields": [
                    {
                        "label": "用户问题",
                        "value": "question"
                    }
                ],
                "height": 496,
                "showNode": true,
                "stepName": "开始",
                "globalFields": [
                    {
                        "label": "当前时间",
                        "value": "time"
                    }
                ]
            }
        },
        {
            "x": 140,
            "y": 2790,
            "id": "01db845c-271e-4071-8371-991403cd76cd",
            "type": "tool-lib-node",
            "properties": {
                "config": {
                    "fields": [
                        {
                            "label": "结果",
                            "value": "result"
                        }
                    ]
                },
                "height": 456,
                "status": 200,
                "showNode": true,
                "stepName": "SplictText2Each",
                "condition": "AND",
                "node_data": {
                    "id": "319aa025-2ae8-7ea3-9863-22f148807bf1",
                    "desc": "将字符串拆分为每个字符",
                    "icon": "",
                    "name": "SplictText2Each",
                    "label": null,
                    "scope": "WORKSPACE",
                    "user_id": "f0dd8f71-e4ee-11ee-8c84-a8a1595801ab",
                    "version": null,
                    "folder_id": "default",
                    "is_active": true,
                    "is_result": false,
                    "nick_name": "系统管理员",
                    "tool_type": "CUSTOM",
                    "create_time": "2025-11-20T07:23:01.737Z",
                    "template_id": null,
                    "tool_lib_id": "319aa025-2ae8-7ea3-9863-22f148807bf1",
                    "update_time": "2025-11-20T07:48:03.837Z",
                    "workspace_id": "default",
                    "resource_type": "tool",
                    "init_field_list": [

                    ],
                    "input_field_list": [
                        {
                            "desc": "输入内容",
                            "name": "text",
                            "type": "string",
                            "value": [
                                "start-node",
                                "question"
                            ],
                            "source": "reference",
                            "is_required": true
                        }
                    ]
                }
            }
        },
        {
            "x": 560,
            "y": 2550,
            "id": "77611157-e198-47ca-967b-3a7429088beb",
            "type": "reply-node",
            "properties": {
                "config": {
                    "fields": [
                        {
                            "label": "内容",
                            "value": "answer"
                        }
                    ]
                },
                "height": 386,
                "showNode": true,
                "stepName": "指定回复",
                "condition": "AND",
                "node_data": {
                    "fields": [
                        "01db845c-271e-4071-8371-991403cd76cd",
                        "result"
                    ],
                    "content": "",
                    "is_result": true,
                    "reply_type": "referencing"
                }
            }
        }
    ]
}

```
