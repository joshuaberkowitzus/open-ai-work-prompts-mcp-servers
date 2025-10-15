import json
from http.server import BaseHTTPRequestHandler, HTTPServer

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

class PromptServer(BaseHTTPRequestHandler):
    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        if self.path == '/prompts':
            prompt_list = {category: list(prompts.keys()) for category, prompts in PROMPTS.items()}
            self._send_response(200, prompt_list)
        else:
            parts = self.path.strip('/').split('/')
            if len(parts) == 3 and parts[0] == 'prompts':
                category, use_case = parts[1], parts[2]
                prompt = PROMPTS.get(category, {}).get(use_case)
                if prompt:
                    self._send_response(200, {'prompt': prompt})
                else:
                    self._send_response(404, {'error': 'Prompt not found'})
            else:
                self._send_response(404, {'error': 'Invalid endpoint'})

def run_server(server_class=HTTPServer, handler_class=PromptServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
