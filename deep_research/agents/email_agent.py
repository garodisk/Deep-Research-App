import os
from typing import Dict
from agents import Agent, ModelSettings, function_tool
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

EMAIL_INSTRUCTIONS = (
    "You can send a nicely formatted HTML email based on a detailed report. "
    "Use your tool exactly once with a good subject and clean HTML."
)

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
    from_addr = os.environ.get("EMAIL_FROM")
    to_addr = os.environ.get("EMAIL_TO")
    if not from_addr or not to_addr:
        raise RuntimeError("EMAIL_FROM and EMAIL_TO env vars are required")
    mail = Mail(Email(from_addr), To(to_addr), subject, Content("text/html", html_body)).get()
    resp = sg.client.mail.send.post(request_body=mail)
    return {"status": str(resp.status_code), "message_id": resp.headers.get("X-Message-Id", "")}

email_agent = Agent(
    name="Email agent",
    instructions=EMAIL_INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)