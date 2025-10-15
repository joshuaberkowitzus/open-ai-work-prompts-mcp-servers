"""
MCP Server (stdio) - Workplace Prompts
Exposes workplace prompts as MCP resources and tools via stdin/stdout
"""

import json
import sys
from typing import Dict, List, Any

PROMPTS = {
    "communication-writing": {
        "write-professional-email": "Write a professional email to [recipient]. The email is about [topic] and should be polite, clear, and concise. Provide a subject line and a short closing.",
        "rewrite-for-clarity": "Rewrite the following text so it is easier to understand. The text will be used in a professional setting. Ensure the tone is clear, respectful, and concise. Text: [paste text].",
        "adapt-message-for-audience": "Reframe this message for [audience type: executives, peers, or customers]. The message was originally written for [context]. Adjust tone, word choice, and style to fit the intended audience. Text: [paste text].",
        "draft-meeting-invite": "Draft a meeting invitation for a session about [topic]. The meeting will include [attendees/roles] and should outline agenda items, goals, and preparation required. Provide the text in calendar-invite format.",
        "summarize-long-email": "Summarize this email thread into a short recap. The thread includes several back-and-forth messages. Highlight key decisions, action items, and open questions. Email: [paste text]."
    },
    "meetings-collaboration": {
        "create-meeting-agenda": "Create a structured agenda for a meeting about [topic]. The meeting will last [time] and include [attendees]. Break the agenda into sections with time estimates and goals for each section.",
        "summarize-meeting-notes": "Summarize these meeting notes into a structured recap. The notes are rough and informal. Organize them into categories: key decisions, next steps, and responsibilities. Notes: [paste text].",
        "create-action-items-list": "Turn the following meeting notes into a clean task list. The tasks should be grouped by owner and include deadlines if mentioned. Notes: [paste text].",
        "prep-questions-for-meeting": "Suggest thoughtful questions to ask in a meeting about [topic]. The purpose of the meeting is [purpose]. Provide a list of at least 5 questions that show preparation and insight.",
        "draft-follow-up-email": "Write a professional follow-up email after a meeting about [topic]. Include a recap of key points, assigned responsibilities, and next steps with deadlines. Use a clear and polite tone."
    },
    "problem-solving-decision-making": {
        "identify-root-cause": "Analyze the following workplace issue: [describe issue]. The context is that the problem has occurred multiple times. Identify possible root causes and suggest questions to confirm them.",
        "compare-options": "Compare the following two or more possible solutions: [list options]. The decision needs to be made in [timeframe]. Evaluate pros, cons, and potential risks for each option.",
        "decision-criteria": "Help define clear decision-making criteria for [describe decision]. The context is that multiple stakeholders are involved. Provide a short list of weighted criteria to guide the choice.",
        "risk-assessment": "Assess the potential risks of the following plan: [describe plan]. The plan is set to start on [date]. List risks by likelihood and impact, and suggest mitigation strategies.",
        "recommend-best-option": "Based on the following background: [describe situation and options], recommend the most suitable option. Explain your reasoning clearly and suggest first steps for implementation."
    },
    "organization-productivity": {
        "document-daily-priorities": "Create a prioritized to-do list from the following tasks: [paste tasks]. The context is a typical workday with limited time. Suggest which tasks should be done first and why.",
        "create-weekly-plan": "Build a weekly work plan for [describe role or situation]. The week includes deadlines, meetings, and individual focus time. Provide a balanced schedule with recommended priorities.",
        "summarize-long-document": "Summarize the following document into 5 key points and 3 recommended actions. The document is [type: report, plan, or notes]. Keep the summary concise and professional. Text: [paste document].",
        "brainstorm-solutions": "Brainstorm potential solutions to the following workplace challenge: [describe challenge]. Provide at least 5 varied ideas, noting pros and cons for each.",
        "write-project-update": "Draft a short project update for stakeholders. The project is [describe project]. Include progress made, current blockers, and next steps. Write in a professional, concise style."
    }
}


class MCPServer:
    def __init__(self):
        self.prompts = PROMPTS
    
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request"""
        return {
            "protocolVersion": "1.0",
            "serverInfo": {
                "name": "workplace-prompts-server",
                "version": "1.0.0"
            },
            "capabilities": {
                "resources": {},
                "tools": {},
                "prompts": {}
            }
        }
    
    def handle_resources_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List all available prompt resources"""
        resources = []
        
        for category, prompts in self.prompts.items():
            for prompt_name, prompt_text in prompts.items():
                resources.append({
                    "uri": f"prompt://{category}/{prompt_name}",
                    "name": f"{category}/{prompt_name}",
                    "description": prompt_text[:100] + "..." if len(prompt_text) > 100 else prompt_text,
                    "mimeType": "text/plain"
                })
        
        return {"resources": resources}
    
    def handle_resources_read(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read a specific prompt resource"""
        uri = params.get('uri', '')
        
        # Parse URI: prompt://category/prompt_name
        if not uri.startswith('prompt://'):
            return {"error": {"code": -32602, "message": "Invalid URI format"}}
        
        path = uri.replace('prompt://', '').split('/')
        if len(path) != 2:
            return {"error": {"code": -32602, "message": "Invalid URI path"}}
        
        category, prompt_name = path
        
        if category not in self.prompts or prompt_name not in self.prompts[category]:
            return {"error": {"code": -32602, "message": "Resource not found"}}
        
        return {
            "contents": [{
                "uri": uri,
                "mimeType": "text/plain",
                "text": self.prompts[category][prompt_name]
            }]
        }
    
    def handle_prompts_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List all available prompts"""
        prompts = []
        
        for category, category_prompts in self.prompts.items():
            for prompt_name, prompt_text in category_prompts.items():
                # Extract arguments from prompt text
                arguments = []
                if '[recipient]' in prompt_text or '[topic]' in prompt_text:
                    if '[recipient]' in prompt_text:
                        arguments.append({
                            "name": "recipient",
                            "description": "The recipient of the email",
                            "required": True
                        })
                    if '[topic]' in prompt_text:
                        arguments.append({
                            "name": "topic",
                            "description": "The topic or subject matter",
                            "required": True
                        })
                if '[paste text]' in prompt_text:
                    arguments.append({
                        "name": "text",
                        "description": "The text to process",
                        "required": True
                    })
                
                prompts.append({
                    "name": f"{category}/{prompt_name}",
                    "description": prompt_text[:100] + "..." if len(prompt_text) > 100 else prompt_text,
                    "arguments": arguments
                })
        
        return {"prompts": prompts}
    
    def handle_prompts_get(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get a specific prompt with arguments filled in"""
        prompt_name = params.get('name', '')
        arguments = params.get('arguments', {})
        
        # Parse prompt name: category/prompt_name
        path = prompt_name.split('/')
        if len(path) != 2:
            return {"error": {"code": -32602, "message": "Invalid prompt name"}}
        
        category, name = path
        
        if category not in self.prompts or name not in self.prompts[category]:
            return {"error": {"code": -32602, "message": "Prompt not found"}}
        
        # Get the prompt template
        prompt_text = self.prompts[category][name]
        
        # Fill in arguments
        for key, value in arguments.items():
            prompt_text = prompt_text.replace(f'[{key}]', str(value))
        
        return {
            "messages": [{
                "role": "user",
                "content": {
                    "type": "text",
                    "text": prompt_text
                }
            }]
        }
    
    def handle_tools_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List all available tools"""
        tools = []
        
        for category, category_prompts in self.prompts.items():
            for prompt_name in category_prompts.keys():
                tools.append({
                    "name": f"{category}/{prompt_name}",
                    "description": f"Generate workplace content using the {prompt_name} prompt",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "input": {
                                "type": "string",
                                "description": "The input text or parameters for the prompt"
                            }
                        },
                        "required": ["input"]
                    }
                })
        
        return {"tools": tools}
    
    def handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool (return the prompt with input)"""
        tool_name = params.get('name', '')
        arguments = params.get('arguments', {})
        
        # Parse tool name: category/prompt_name
        path = tool_name.split('/')
        if len(path) != 2:
            return {"error": {"code": -32602, "message": "Invalid tool name"}}
        
        category, name = path
        
        if category not in self.prompts or name not in self.prompts[category]:
            return {"error": {"code": -32602, "message": "Tool not found"}}
        
        prompt_text = self.prompts[category][name]
        user_input = arguments.get('input', '')
        
        return {
            "content": [{
                "type": "text",
                "text": f"{prompt_text}\n\nInput: {user_input}"
            }]
        }
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Route request to appropriate handler"""
        method = request.get('method', '')
        params = request.get('params', {})
        
        handlers = {
            'initialize': self.handle_initialize,
            'resources/list': self.handle_resources_list,
            'resources/read': self.handle_resources_read,
            'prompts/list': self.handle_prompts_list,
            'prompts/get': self.handle_prompts_get,
            'tools/list': self.handle_tools_list,
            'tools/call': self.handle_tools_call
        }
        
        handler = handlers.get(method)
        if handler:
            result = handler(params)
            return {
                "jsonrpc": "2.0",
                "id": request.get('id'),
                "result": result
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get('id'),
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    def run(self):
        """Main loop for stdio communication"""
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)


if __name__ == '__main__':
    server = MCPServer()
    server.run()
