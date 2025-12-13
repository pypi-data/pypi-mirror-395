import requests
import time
from n8n_utils import get_workflow_reg
import copy
import uuid
from sqlalchemy import create_engine, text
import pandas as pd
import json
class n8n_resource():
    def clean_workflow_for_update_(self,wf):
        forbidden = [
        "id",
        "active",            # <-- MUST ADD THIS
        "createdAt",
        "updatedAt",
        "isArchived",
        "versionId",
        "meta",
        "staticData",
        "triggerCount",
        "tags",
        "pinData"
        ]
        return {k: v for k, v in wf.items() if k not in forbidden}
    def reorder_switch_main_(self,rule, switch_main):
        order=[]
        for i in rule:
            order.append(i['conditions']['conditions'][0]['rightValue'])
            # Map agent -> list
        mapping = {}
        print("order ==> ",order)
        for lst in switch_main:
            print( "Ii ==> ",lst)
            if lst and "node" in lst[0] and len(lst) > 0:
                print( "Ii =22=> ",lst)
                mapping[lst[0]["node"]] = lst
            
        print("MAP ==> ",mapping)
        # Build result in correct order
        result = []
        for agent in order:
            if agent in mapping:
                result.append(mapping[agent])
        print("rest ==>  ",result)
        return result
    def __init__(self,url,key):
        self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-N8N-API-KEY": key
            }
        self.url=url   
    def connect(self):
        res = requests.get(f"{self.url}/api/v1/workflows", headers=self.headers)
        res.raise_for_status()
        workflow=res.json()
        reg=get_workflow_reg(workflow)
        return reg
    
    def get_all_workflow(self):
        res = requests.get(f"{self.url}/api/v1/workflows", headers=self.headers)
        workflow=res.json()
        res=[]
        for i in workflow['data']:

            res.append({"id":i['id'],"name":i['name'],"nodes":i['nodes']})
        return res
    
    def get_workflow(self,name):
        res = requests.get(f"{self.url}/api/v1/workflows", headers=self.headers)
        res.raise_for_status()
        workflow=res.json()
        wf=None
        for w in workflow['data']:
            if w['name']==name:
                wf=w
        self.wf=wf
        return self.wf
    def delete_workflow(self):
        print("--->  ",self.wf)
        wf_id=self.wf['id']
        res = requests.delete(f"{self.url}/api/v1/workflows/{wf_id}", headers=self.headers)
        if res.status_code ==200:

            self.wf=None
        return res.json
        
    def get_node_by_name(self,name):
        res = self.wf
        print(res)
        
    def get_all_credentials(self):
        print("""Fetch all credentials + their full decrypted data. """,self.headers)
       
    
    
        endpoints = [
            f"{self.url.rstrip('/')}/api/v1/credentials",
            f"{self.url.rstrip('/')}/rest/credentials"
        ]

        for ep in endpoints:
            print(f"########Trying {ep}")
            res = requests.get(ep, headers=self.headers)
            if res.status_code == 200:
                print("SUCCESS:", ep)
                return res.json()
            else:
                print("FAILED:", res.status_code, res.text)

        raise Exception("No credential endpoint available. API restricted.")

    def db_account(self,host,port,database,user,password,name,type,ssl='disable',sshAuthenticateWith='password',
    sshHost='',sshPort=22,sshUser='',sshPassword='',privateKey='',passphrase=''):
        if type=="postgres":
                payload = {
                    "name": name,
                    "type": type,
                    "data": {
                        "user": user,
                        "password": password,
                        "database": database,
                        "host": host,
                        "port": port,
                        "ssl": ssl,
                        "sshAuthenticateWith": "password",
                        "sshHost": sshHost,
                        "sshPort": 22,
                        "sshUser": sshUser,
                        "sshPassword": sshPassword,
                        "privateKey": privateKey,
                        "passphrase": passphrase
                    },
            "nodesAccess": [
                {
                    "nodeType": "*",
                    "date": int(time.time() * 1000)
                }
            ]
        }
        res = requests.post(f"{self.url}/api/v1/credentials", json=payload, headers=self.headers)

        print("Status:", res.status_code)
        print("Response:", res.text)
        return  res
    
    def azure_account(self,azure_key:str,
        resource_name: str,
        api_version: str,
        endpoint: str,
        deply_name:str,
        credential_name: str):
        payload = {
            "name": credential_name,
            "type": "azureOpenAiApi",
            "data": {

                "apiKey": azure_key,
                "resourceName": resource_name,
                "apiVersion": api_version,
                "endpoint": endpoint 
                
            },
            "nodesAccess": [
                {
                    "nodeType": "*",
                    "date": int(time.time() * 1000)
                }
            ]
        }

        res = requests.post(
            f"{self.url}/api/v1/credentials",
            headers=self.headers,
            json=payload)

        print("Status:", res.status_code)
        print("Response:", res.text)
        return res
        
    def add_base_flow(self,flow_name):
       

        nodes= [
                {
                "parameters": {
                    "options": {}
                },
                "type": "@n8n/n8n-nodes-langchain.chatTrigger",
                "typeVersion": 1.3,
                "position": [
                    -496,
                    -240
                ],
                "id": "2f7fc3ec-fd67-45a1-82d8-c851c859eeae",
                "name": "When chat message received",
                "webhookId": f"whbase_{str(uuid.uuid4())}"
                },
                {
                "parameters": {
                    "promptType": "define",
                    "text": "={{ $('Webhook').item.json.body.query }}",
                    "hasOutputParser": True,
                    "options": {
                    "systemMessage": "={{ $json.prompts }}  "
                    }
                },
                "type": "@n8n/n8n-nodes-langchain.agent",
                "typeVersion": 2.2,
                "position": [
                    -16,
                    -112
                ],
                "id": f"ORCHbase_{str(uuid.uuid4())}",
                "name": "ORCH"
                },
                {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={\n  \"res\": \"no agent\",\n  \"sessionid\":\"{{ $('Webhook').item.json.body.sessionId }}\"}",
                    "options": {}
                },
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1.4,
                "position": [
                    800,
                    -432
                ],
                "id": f"no_ag_wh_{str(uuid.uuid4())}",
                "name": "no_agent"
                },
                {
                "parameters": {
                    "model": "gpt-4.1",
                    "options": {}
                },
                "type": "@n8n/n8n-nodes-langchain.lmChatAzureOpenAi",
                "typeVersion": 1,
                "position": [
                    -16,
                    64
                ],
                "id": "az_llm_mod_{str(uuid.uuid4())}",
                "name": "Azure OpenAI Chat Model",
                "credentials": {
                    "azureOpenAiApi": {
                    "id": "35HrWoNexzT6NyGi",
                    "name": "az_t_apu"
                    }
                }
                },
                {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "muti_agent",
                    "responseMode": "responseNode",
                    "options": {}
                },
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2.1,
                "position": [
                    -512,
                    -16
                ],
                "id": f"whbase_{str(uuid.uuid4())}",
                "name": "Webhook",
                "webhookId": "3df2e892-528d-4a9f-98ef-d6b2ad63f3a0"
                },
                {
                "parameters": {f
                    "operation": "executeQuery",
                    "query": "SELECT prompts, id\nFROM public.prombte\n  where id = 1;",
                    "options": {}
                },
                "type": "n8n-nodes-base.postgres",
                "typeVersion": 2.6,
                "position": [
                    -240,
                    -128
                ],
                "id": f"psqlbase_{str(uuid.uuid4())}",
                "name": "Execute a SQL query",
                "credentials": {
                    "postgres": {
                    "id": "lTIzLsX6ieIGLage",
                    "name": "pg_accoount"
                    }
                }
                },{
                "parameters": {
                    "sessionIdType": "customKey",
                    "sessionKey": "={{ $('Webhook').item.json.body.sessionId }}"
                    },
                "type": "@n8n/n8n-nodes-langchain.memoryPostgresChat",
                "typeVersion": 1.3,
                "position": [
                    64,
                    192
                ],
                "id": f"Mem_repobase_{str(uuid.uuid4())}",
                "name": "Mem_repo",
                "credentials": {
                    "postgres": {
                    "id": "lTIzLsX6ieIGLage",
                    "name": "pg_accoount"
                    }
                }
                },
                {
                "parameters": {
                    "jsonSchemaExample": "{\"user_input\": \"user input text\",\n \"selected_agents\":[\"Agent1\",\"Agent2\"],\n\"reason\": \"message includes reason of classifications\"}\n",
                    "autoFix": True
                },
                "type": "@n8n/n8n-nodes-langchain.outputParserStructured",
                "typeVersion": 1.3,
                "position": [
                    144,
                    80
                ],
                "id": f"pars_base_{str(uuid.uuid4())}",
                "name": "Structured Output Parser"
                },
                {
                "parameters": {
                    "model": "gpt-4.1",
                    "options": {}
                },
                "type": "@n8n/n8n-nodes-langchain.lmChatAzureOpenAi",
                "typeVersion": 1,
                "position": [
                    240,
                    160
                ],
                "id": f"az_nas_llm_1_{str(uuid.uuid4())}",
                "name": "Azure OpenAI Chat Model1",
                "credentials": {
                    "azureOpenAiApi": {
                    "id": "35HrWoNexzT6NyGi",
                    "name": "az_t_apu"
                    }
                }
                },
                {
                "parameters": {
                    "rules": {
                    "values": [
                        {
                        "conditions": {
                            "options": {
                            "caseSensitive": True,
                            "leftValue": "",
                            "typeValidation": "strict",
                            "version": 2
                            },
                            "conditions": [
                            {
                                "leftValue": "={{ $json.output.selected_agents }}",
                                "rightValue": "no_agent",
                                "operator": {
                                "type": "array",
                                "operation": "contains",
                                "rightType": "any"
                                },
                                "id": f"rule_base_{str(uuid.uuid4())}"
                            }
                            ],
                            "combinator": "and"
                        }
                        }
                    ]
                    },
                    "options": {
                    "allMatchingOutputs": True
                    }
                },
                "type": "n8n-nodes-base.switch",
                "typeVersion": 3.2,
                "position": [
                    384,
                    -160
                ],
                "id": f"Switch_base_{str(uuid.uuid4())}",
                "name": "Switch"
                }
            ]
        connections={
                "When chat message received": {
                "main": [
                    [
                    {
                        "node": "Execute a SQL query",
                        "type": "main",
                        "index": 0
                    }
                    ]
                ]
                },
                "ORCH": {
                "main": [
                    [
                    {
                        "node": "Switch",
                        "type": "main",
                        "index": 0
                    }
                    ]
                ]
                },
                "Azure OpenAI Chat Model": {
                "ai_languageModel": [
                    [
                    {
                        "node": "ORCH",
                        "type": "ai_languageModel",
                        "index": 0
                    }
                    ]
                ]
                },
                "Webhook": {
                "main": [
                    [
                    {
                        "node": "Execute a SQL query",
                        "type": "main",
                        "index": 0
                    }
                    ]
                ]
                },
                "Execute a SQL query": {
                "main": [
                    [
                    {
                        "node": "ORCH",
                        "type": "main",
                        "index": 0
                    }
                    ]
                ]
                },
                "Structured Output Parser": {
                "ai_outputParser": [
                    [
                    {
                        "node": "ORCH",
                        "type": "ai_outputParser",
                        "index": 0
                    }
                    ]
                ]
                },
                "Azure OpenAI Chat Model1": {
                "ai_languageModel": [
                    [
                    {
                        "node": "Structured Output Parser",
                        "type": "ai_languageModel",
                        "index": 0
                    }
                    ]
                ]
                },
                "Switch": {
                    "main": [
                        [
                        {
                            "node": "no_agent",
                            "type": "main",
                            "index": 0
                        }
                        ]
                        
                    ]
                    },
                    "Mem_repo": {
                    "ai_memory": [
                        [
                        {
                            "node": "ORCH",
                            "type": "ai_memory",
                            "index": 0
                        }
                        ]
                    ]
                    }
            }
        workflow_payload = {
            "name": flow_name,
            "nodes": nodes,
            "connections": connections,
            "settings": {}
            }
        res = requests.post(
            f"{self.url}/api/v1/workflows",
            headers=self.headers,
            json=workflow_payload
        )
        
        time.sleep(4)
        
        self.get_workflow(flow_name)

        res_activate = requests.post(f"{self.url}/api/v1/workflows/{self.wf['id']}/activate",
            headers=self.headers)
        print("Activate Status:", res_activate.status_code)
        print("Activate Response:", res_activate.text)

        return res_activate
    def activate_workflow(self):  
        ares_activate = requests.post(f"{self.url}/api/v1/workflows/{self.wf['id']}/activate",
            headers=self.headers)
        print("Activate Status:", ares_activate.status_code)
        print("Activate Response:", ares_activate.text)

        return ares_activate
    
    def deactivate_workflow(self):  
        ares_deactivate = requests.post(f"{self.url}/api/v1/workflows/{self.wf['id']}/deactivate",
            headers=self.headers)
        print("Activate Status:", ares_deactivate.status_code)
        print("Activate Response:", ares_deactivate.text)

        return ares_deactivate
    def mcp_client_node(self,name:str,
                             host: str,
                             tools: list,
                             auth="none",
                             transport="sse"):

        new_wf = copy.deepcopy(self.wf)
        workflow_payload = {
            "name": new_wf.get("name"),
            "nodes": new_wf.get("nodes", []),
            "connections": new_wf.get("connections", {}),
            "settings": new_wf.get("settings", {})
            }
        node = {
            "id": f"mcp_client_{int(time.time())}",
            "name": name,
            "type": "@n8n/n8n-nodes-langchain.mcpClientTool",
            "typeVersion": 1,
            "position": [600, 300],
            "parameters": {
                "sseEndpoint": host,
                "transport": transport,            # "sse" or "websocket"
                "authentication": auth,            # none, basic, bearer
                "include": "selected",
                "includeTools": tools                     # list of tool names
            }
        }
        print(f"urls ==> {self.url}/api/v1/workflows/{self.wf['id']} ")
        workflow_payload["nodes"].append(node)
        res = requests.put(
            f"{self.url}/api/v1/workflows/{self.wf['id']}",
            headers=self.headers,
            json=workflow_payload
        )
        print("Status:", res.status_code)
        print("Response:", res.text)
        return new_wf
    
    def add_llm_formater(self,name:str,
                             json_schema:str):
        new_uuid = str(uuid.uuid4())
        new_wf = copy.deepcopy(self.wf)
        workflow_payload = {
            "name": new_wf.get("name"),
            "nodes": new_wf.get("nodes", []),
            "connections": new_wf.get("connections", {}),
            "settings": new_wf.get("settings", {})
            }
        
        node = {
        "parameters": {
            "jsonSchemaExample": json_schema,
            "autoFix": True
        },
        "type": "@n8n/n8n-nodes-langchain.outputParserStructured",
        "typeVersion": 1.3,
        "position": [600, 300],
        "id": f"{name}_{new_uuid}",
        "name": name
        }
        workflow_payload["nodes"].append(node)
        res = requests.put(
            f"{self.url}/api/v1/workflows/{self.wf['id']}",
            headers=self.headers,
            json=workflow_payload
        )
        print("Status:", res.status_code)
        print("Response:", res.text)
        return node
    
    def add_agent(self,name: str,sw_name:str,sw_op_cond,sw_op_type,sw_op_rtype,sw_con_type="main",
                    system_message="",
                    text="",hasOutputParser=True):
    
        res=self.add_switch_route(sw_name=sw_name,ag_name=name,op_cond=sw_op_cond,op_type=sw_op_type,op_rtype=sw_op_rtype)
        time.sleep(4)
        self.get_workflow(self.wf['name'])
        new_uuid = str(uuid.uuid4())
   
        new_wf = copy.deepcopy(self.wf)

        # Create UUID
        node_id = str(uuid.uuid4())
        node = {
            "parameters": {
                "promptType": "define",
                "text": text,
                "hasOutputParser": hasOutputParser,
                "options": {
                    "systemMessage": system_message
                }
            },
            "type": "@n8n/n8n-nodes-langchain.agent",
            "typeVersion": 2.2,
            "position": [600, 300],
            "id": new_uuid,
            "name": name
        
        }
        webhokk_res={
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={\"res1\":\"{{ $json.output.res }}\",\"sessionid\":\"{{ $('Webhook').item.json.body.sessionId }}\"}",
                    "options": {}
                },
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1.4,
                "position": [
                    1376,
                    336
                ],
                "id": f"{name}_wh_resp_{new_uuid}",
                "name": f"{name}_wh_resp"
                }
        new_wf["nodes"].append(node)
        new_wf["nodes"].append(webhokk_res)
        new_wf['connections'][sw_name][sw_con_type].append(
            [{
                        "node":name ,
                        "type": "main",
                        "index": 0
                    }]

        )
        new_wf['connections']['Mem_repo']['ai_memory'][0].append(
            {
            "node": name,
            "type": "ai_memory",
            "index": 0
          }

        )
        new_wf['connections'][name] ={
                    "main": [
                        [
                        {
                            "node": f"{name}_wh_resp",
                            "type": "main",
                            "index": 0
                        }
                        ]
                    ]
                    }
        safe_wf = self.clean_workflow_for_update_(new_wf)
        res = requests.put(
            f"{self.url}/api/v1/workflows/{self.wf['id']}",
            headers=self.headers,
            json=safe_wf
        )

        print("Status:", res.status_code)
        print("Response:", res.text)
        return
    
    def add_postgres_node(self,
                          name: str,
                          query: str,
                          credential_id: str,
                          credential_name: str,
                          position=(400, 100)):
        """
        Adds a PostgreSQL query node to an n8n workflow.
        """

        new_wf = copy.deepcopy(self.wf)

        node_id = str(uuid.uuid4())

        node = {
            "parameters": {
                "operation": "executeQuery",
                "query": query,
                "options": {}
            },
            "type": "n8n-nodes-base.postgres",
            "typeVersion": 2.6,
            "position": list(position),
            "id": node_id,
            "name": name,
            "credentials": {
                "postgres": {
                    "id": credential_id,
                    "name": credential_name
                }
            }
        }

        new_wf["nodes"].append(node)

        # Make sure workflow complies with n8n PUT schema
        safe_wf = self.clean_workflow_for_update_(new_wf)

        res = requests.put(
            f"{self.url}/api/v1/workflows/{self.wf['id']}",
            headers=self.headers,
            json=safe_wf
        )

        print("Status:", res.status_code)
        print("Response:", res.text)

        return safe_wf

    def create_workflow(self, workflow_name: str):
        # Basic workflow template
        wf = self.get_workflow(workflow_name)
        print("wf ==>  ",wf)
        
        if wf is  None:
            print("--1--")
            payload = {
                    "name": workflow_name,
                    "nodes": [],
                    "connections": {},
                    "settings": {}
                    }

            res = requests.post(
                f"{self.url}/api/v1/workflows",
                headers=self.headers,
                json=payload   # MUST be json, not data
            )

            print("Status:", res)
        
            return {'Statu':False,"data":res.json()}
        else:
            return {'Statu':False}

    def add_azur_llm_model(self,name,az_account_name,llm_acount_id,llm_model):
        new_wf = copy.deepcopy(self.wf)
        node={
      "parameters": {
        "model": llm_model,
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.lmChatAzureOpenAi",
      "typeVersion": 1,
      "position": [
        240,
        160
      ],
      "id": f"{name}_{str(uuid.uuid4())}",
      "name": name,
      "credentials": {
        "azureOpenAiApi": {
          "id": llm_acount_id,
          "name": az_account_name
        }
      }
    }
        new_wf["nodes"].append(node)

        # Make sure workflow complies with n8n PUT schema
        safe_wf = self.clean_workflow_for_update_(new_wf)

        res = requests.put(
            f"{self.url}/api/v1/workflows/{self.wf['id']}",
            headers=self.headers,
            json=safe_wf
        )

        print("Status:", res.status_code)
        print("Response:", res.text)

        return safe_wf
    
    def add_switch_route(self,sw_name,ag_name,op_type,op_cond,op_rtype):
        workflow = copy.deepcopy(self.wf)
        allowed_fields = ["name", "nodes", "connections", "settings"]
        workflow_clean = {k: workflow[k] for k in allowed_fields if k in workflow}

        # 2) Find the Switch node
        switch_node = None
        for node in workflow_clean["nodes"]:
            if node["name"] == sw_name and node["type"] == "n8n-nodes-base.switch":
                switch_node = node
                break

        if not switch_node:
            raise ValueError(f"Switch node '{sw_name}' not found!")
        print(switch_node)
        # 3) Add new route to switch
        new_route = {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "loose",
                    "version": 2
                },
                "conditions": [
                    {
                        "id": f"{sw_name}__{str(uuid.uuid4())}",
                        "leftValue": "={{ $json.output.selected_agents }}",
                        "rightValue": ag_name,   # new route value
                        "operator": {
                            "type": op_type,
                            "operation": op_cond,
                            "rightType": op_rtype
                        }
                    }
                ],
                "combinator": "and"
            }
        }
        print("##  switch_node ==>  ",switch_node["parameters"])
        # Append the new route
        switch_node["parameters"]["rules"]["values"].append(new_route)

        # 4) Update workflow
        update_res = requests.put(
            f"{self.url}/api/v1/workflows/{self.wf["id"]}",
            headers=self.headers,
            data=json.dumps(workflow_clean)
        )

        if update_res.status_code in (200, 204):
            print(f"✅ Switch node '{sw_name}' updated successfully!")
        else:
            print("❌ Error updating workflow:", update_res.status_code, update_res.text)

    def delete_agent(self, agent_name: str, switch_name: str):
    #     """
    #     Completely removes an agent and all related nodes:
    #     - agent node
    #     - its MCP nodes
    #     - its LLM model nodes
    #     - its outputParser nodes
    #     - all connections
    #     - switch rules referencing this agent
    #     """

        wf = copy.deepcopy(self.wf)
        delete_ids = set()

        for node in wf["nodes"]:
            # Main agent node
            if node["name"] == agent_name:
                delete_ids.add(node["id"])

            # LLM, parser, MCP nodes downstream
            if node["name"].startswith(agent_name + "_") or agent_name in node["name"]:
                delete_ids.add(node["id"])

        print("Nodes to delete:", delete_ids)
        for node in wf["nodes"]:
            print("--1--")
            if node["name"] == switch_name and node["type"] == "n8n-nodes-base.switch":
                print("--21--")
                old_rules = node["parameters"]["rules"]["values"]
                new_rules = []

                for rule in old_rules:
                    try:
                        cond = rule["conditions"]["conditions"][0]
                        if cond["rightValue"] != agent_name:
                            new_rules.append(rule)
                    except:
                        new_rules.append(rule)
                
                node["parameters"]["rules"]["values"] = new_rules
                print(f"✔ Switch rule for '{agent_name}' removed")
        print()
        wf["nodes"] = [n for n in wf["nodes"] if n["id"] not in delete_ids]
        remove_keys = [k for k in wf["connections"].keys() if k.startswith(agent_name)]

        for key in remove_keys:
            wf["connections"].pop(key, None)

        # 3. Remove references to ag1 in other nodes’ connection lists
        for src_node, conn_types in wf["connections"].items():
            for conn_type, conn_list in conn_types.items():
                for branch in conn_list:
                    branch[:] = [
                        item for item in branch
                        if item.get("node") != agent_name and not item.get("node", "").startswith(agent_name)
                    ]
        cons=self.reorder_switch_main_(new_rules,wf["connections"]['Switch']['main'])
        wf["connections"]['Switch']['main']=cons
        safe_wf = self.clean_workflow_for_update_(wf)
        res = requests.put(
              f"{self.url}/api/v1/workflows/{self.wf['id']}",
              headers=self.headers,
              json=safe_wf)
    
        return res

    def del_switch_rule(self):
        self.get_workflow(self.wf['name'])
        wf = copy.deepcopy(self.wf)
        wf['connections']['Switch']['main'] = [lst for lst in wf['connections']['Switch']['main']  if len(lst) > 0]
        safe_wf = self.clean_workflow_for_update_(wf)

        res = requests.put(
             f"{self.url}/api/v1/workflows/{self.wf['id']}",
             headers=self.headers,
             json=safe_wf
         )

        return "res"
        



       

class n8n_connect():
    def clean_workflow_for_update_(self,wf):
        forbidden = [
        "id",
        "active",            # <-- MUST ADD THIS
        "createdAt",
        "updatedAt",
        "isArchived",
        "versionId",
        "meta",
        "staticData",
        "triggerCount",
        "tags",
        "pinData"
        ]
        return {k: v for k, v in wf.items() if k not in forbidden}
    def __init__(self,url,key):
        self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-N8N-API-KEY": key
            }
        self.url=url

    def connect(self):
        res = requests.get(f"{self.url}/api/v1/workflows", headers=self.headers)
        res.raise_for_status()
        workflow=res.json()
        reg=get_workflow_reg(workflow)
        return reg
        
    def get_workflow(self,name):
        res = requests.get(f"{self.url}/api/v1/workflows", headers=self.headers)
        res.raise_for_status()
        workflow=res.json()
        wf=None
        for w in workflow['data']:
            if w['name']==name:
                wf=w
        self.wf=wf
        return self.wf



    def connect_nodes(self, from_node: str, to_node: str,
                    output_index: int = 0, input_index: int = 0,con_type='main'):
        """
        Creates a connection from one node to another in the current workflow.

        from_node: node name or id (source)
        to_node:   node name or id (destination)
        """

        new_wf = copy.deepcopy(self.wf)
        print(new_wf)
        # resolve node IDs by name or direct id
        def find_id(name_or_id):
            for n in new_wf["nodes"]:
                if n["id"] == name_or_id or n["name"] == name_or_id:
                    return n["id"]
            raise ValueError(f"Node '{name_or_id}' not found")

        from_id = find_id(from_node)
        to_id = find_id(to_node)

        # ensure "connections" exists
        if "connections" not in new_wf:
            new_wf["connections"] = {}

        # ensure source node has main array
        if from_id not in new_wf["connections"]:
            new_wf["connections"][from_node] = {con_type: []}

        # ensure enough outputs exist
        while len(new_wf["connections"][from_node][con_type]) <= output_index:
            new_wf["connections"][from_node][con_type].append([])

        # Add the connection
        new_wf["connections"][from_node][con_type][output_index].append({
            "node": to_node,
            "type": con_type,
            "index": input_index
        })

        # clean for PUT
        safe_wf = self.clean_workflow_for_update_(new_wf)

        # send update
        res = requests.put(
            f"{self.url}/api/v1/workflows/{self.wf['id']}",
            headers=self.headers,
            json=safe_wf
        )

        print("Status:", res.status_code)
        print("Response:", res.text)

        return safe_wf


class n8n_database():
    def __init__(self,type,host,port,username,password,db_name):
        self.type=type
        if self.type=='psql':
            DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
            self.engine = create_engine(DATABASE_URL)
            self.conn=self.engine.connect()
    def get_data(self,query):
        df = pd.read_sql(text(query), self.conn)
        data_as_json = df.to_dict(orient="records")
        del df
        return data_as_json
        
    def delete_workflow(self,name):
        query = text(f"""DELETE FROM public.workflow_entity WHERE name='{name}' or "isArchived" = true""")

        try:
            with self.engine.begin() as conn:
                conn.execute(query)
            print("Deleted archived records.")

        except Exception as e:
            print("Error:", e)

    def delete_data(self,query):
        try:
            self.conn.execute(text(query))
            self.conn.commit()
            
           
            return {"status":True,"data":""}
        except Exception as e:
            return {"status":False,"data":f"Exception: {str(e)}"}


