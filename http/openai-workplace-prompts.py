"""
MCP Server (HTTP) - Workplace Prompts
Exposes workplace prompts as MCP resources and tools via HTTP
"""

from flask import Flask, request, jsonify
from typing import Dict, List, Any
import json

app = Flask(__name__)

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


@app.route('/mcp/v1/initialize', methods=['POST'])
def initialize():
    """Handle MCP initialization"""
    return jsonify({
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
    })


@app.route('/mcp/v1/resources/list', methods=['POST'])
def list_resources():
    """List all available prompt resources"""
    resources = []
    
    for category, prompts in PROMPTS.items():
        for prompt_name, prompt_text in prompts.items():
            resources.append({
                "uri": f"prompt://{category}/{prompt_name}",
                "name": f"{category}/{prompt_name}",
                "description": prompt_text[:100] + "..." if len(prompt_text) > 100 else prompt_text,
                "mimeType": "text/plain"
            })
    
    return jsonify({"resources": resources})


@app.route('/mcp/v1/resources/read', methods=['POST'])
def read_resource():
    """Read a specific prompt resource"""
    data = request.json
    uri = data.get('uri', '')
    
    # Parse URI: prompt://category/prompt_name
    if not uri.startswith('prompt://'):
        return jsonify({"error": "Invalid URI format"}), 400
    
    path = uri.replace('prompt://', '').split('/')
    if len(path) != 2:
        return jsonify({"error": "Invalid URI path"}), 400
    
    category, prompt_name = path
    
    if category not in PROMPTS or prompt_name not in PROMPTS[category]:
        return jsonify({"error": "Resource not found"}), 404
    
    return jsonify({
        "contents": [{
            "uri": uri,
            "mimeType": "text/plain",
            "text": PROMPTS[category][prompt_name]
        }]
    })


@app.route('/mcp/v1/prompts/list', methods=['POST'])
def list_prompts():
    """List all available prompts"""
    prompts = []
    
    for category, category_prompts in PROMPTS.items():
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
    
    return jsonify({"prompts": prompts})


@app.route('/mcp/v1/prompts/get', methods=['POST'])
def get_prompt():
    """Get a specific prompt with arguments filled in"""
    data = request.json
    prompt_name = data.get('name', '')
    arguments = data.get('arguments', {})
    
    # Parse prompt name: category/prompt_name
    path = prompt_name.split('/')
    if len(path) != 2:
        return jsonify({"error": "Invalid prompt name"}), 400
    
    category, name = path
    
    if category not in PROMPTS or name not in PROMPTS[category]:
        return jsonify({"error": "Prompt not found"}), 404
    
    # Get the prompt template
    prompt_text = PROMPTS[category][name]
    
    # Fill in arguments
    for key, value in arguments.items():
        prompt_text = prompt_text.replace(f'[{key}]', str(value))
    
    return jsonify({
        "messages": [{
            "role": "user",
            "content": {
                "type": "text",
                "text": prompt_text
            }
        }]
    })


@app.route('/mcp/v1/tools/list', methods=['POST'])
def list_tools():
    """List all available tools"""
    tools = []
    
    for category, category_prompts in PROMPTS.items():
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
    
    return jsonify({"tools": tools})


@app.route('/mcp/v1/tools/call', methods=['POST'])
def call_tool():
    """Execute a tool (return the prompt with input)"""
    data = request.json
    tool_name = data.get('name', '')
    arguments = data.get('arguments', {})
    
    # Parse tool name: category/prompt_name
    path = tool_name.split('/')
    if len(path) != 2:
        return jsonify({"error": "Invalid tool name"}), 400
    
    category, name = path
    
    if category not in PROMPTS or name not in PROMPTS[category]:
        return jsonify({"error": "Tool not found"}), 404
    
    prompt_text = PROMPTS[category][name]
    user_input = arguments.get('input', '')
    
    return jsonify({
        "content": [{
            "type": "text",
            "text": f"{prompt_text}\n\nInput: {user_input}"
        }]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
