# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
import subprocess
import time
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os


# If modifying these SCOPES, delete the token.json file
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


# instantiate an MCP server client
mcp = FastMCP("Calculator")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]




@mcp.tool()
async def open_pages() -> dict:
    """Open Pages application"""
    try:
        # Open the Pages app
        subprocess.run(["open", "-a", "Pages"], check=True)

        # Optional: Attempt to move and maximize Pages using AppleScript
        applescript = '''
        tell application "System Events"
            tell process "Pages"
                set frontmost to true
                delay 0.5
                try
                    perform action "AXZoomWindow" of window 1
                end try
            end tell
        end tell
        '''
        subprocess.run(["osascript", "-e", applescript])

        return {
            "content": [
                {
                    "type": "text",
                    "text": "Pages opened successfully and attempted to maximize."
                }
            ]
        }
    except subprocess.CalledProcessError as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error opening Pages: {str(e)}"
                }
            ]
        }


@mcp.tool()
async def insert_rectangle_in_pages() -> dict:
    """Insert a rectangle In Pages application"""
    try:
        applescript = '''
        tell application "Pages"
            activate
            if not (exists document 1) then
                make new document
            end if
        end tell

        delay 1

        tell application "System Events"
            tell process "Pages"
                set frontmost to true
                delay 0.5

                -- Click into the document to enable insertion
                try
                    click text area 1 of scroll area 1 of splitter group 1 of window 1
                    delay 0.5
                end try

                -- Insert Rectangle
                click menu item "Rectangle" of menu 1 of menu item "Shape" of menu 1 of menu bar item "Insert" of menu bar 1
                delay 0.5

                -- Use shortcut to open color picker for Fill (Cmd+Opt+Shift+C)
                keystroke "c" using {command down, option down, shift down}
                delay 1

                -- Use arrow keys and Enter to select white
                key code 123 -- Left arrow (assuming white is leftmost)
                delay 0.2
                keystroke return
            end tell
        end tell
        '''
        subprocess.run(["osascript", "-e", applescript], check=True)

        return {
            "content": [
                {
                    "type": "text",
                    "text": "Rectangle inserted and fill set to white in Pages using keyboard navigation."
                }
            ]
        }
    except subprocess.CalledProcessError as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error: {str(e)}"
                }
            ]
        }

@mcp.tool()
async def add_text_in_rectangle(text: str) -> dict:
    """Types the given text inside the selected rectangle in Pages"""
    try:
        # AppleScript to focus Pages and type into the selected shape
        applescript = f'''
        tell application "Pages"
            activate
        end tell

        delay 0.5

        tell application "System Events"
            tell process "Pages"
                set frontmost to true
                delay 0.5

                -- Type the user-provided text
                keystroke "{text}"
            end tell
        end tell
        '''
        subprocess.run(["osascript", "-e", applescript], check=True)

        return {
            "content": [
                {
                    "type": "text",
                    "text": f'Text "{text}" added to the rectangle.'
                }
            ]
        }
    except subprocess.CalledProcessError as e:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error inserting text: {str(e)}"
                }
            ]
        }


@mcp.tool()
async def send_email_gmail_api(subject, message_text, recipient):
    """Send email using gmail with a subject and message text to recipient"""
    creds = None

    # Load credentials from token.json if available
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no (valid) credentials, do OAuth2 flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Build the message
    message = MIMEText(message_text)
    message['to'] = recipient
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send the message
    message_body = {'raw': raw}
    send_message = service.users().messages().send(userId="me", body=message_body).execute()
    
    return {
            "content": [
                {
                    "type": "text",
                    "text": f"Message Id: {send_message['id']}"
                }
            ]
        }
    

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
