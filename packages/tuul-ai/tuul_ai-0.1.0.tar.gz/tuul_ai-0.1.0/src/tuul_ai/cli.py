import typer
import os
from typing import Optional, List, Dict, Any
from rich.console import Console
from .client import TuulClient
from .exceptions import TuulError
from dotenv import load_dotenv 

# Load environment variables at the start
load_dotenv()


# --- CLI Setup ---

app = typer.Typer(help="The official CLI for the Tuul API.")
console = Console()


ENV_AGENT_ID = os.getenv("TUUL_AGENT_ID")
AGENT_ID_DEFAULT = ENV_AGENT_ID if ENV_AGENT_ID is not None else ...

TUUL_AGENT_VERSION = os.getenv("TUUL_AGENT_VERSION")
AGENT_VERSION_DEFAULT = TUUL_AGENT_VERSION if TUUL_AGENT_VERSION is not None else None

def get_client(api_key: Optional[str]) -> TuulClient:
    """Initializes and returns the TuulClient."""
    key = api_key or os.getenv("TUUL_API_KEY")
    if not key:
        console.print("[bold red]Error:[/bold red] TUUL_API_KEY not found. Please set the environment variable or use the --api-key flag.")
        raise typer.Exit(code=1)
    return TuulClient(api_key=key)

# Helper to parse CLI input for characteristics (e.g., --characteristic identity=greeter)
def parse_characteristics(ctx: typer.Context, value: Optional[List[str]]) -> Optional[List[Dict[str, str]]]:
    """Converts a list of 'key=value' strings into a List[Dict[str, str]]."""
    if not value:
        return None
    
    parsed_list = []
    for item in value:
        try:
            key, val = item.split('=', 1)
            parsed_list.append({"key": key, "value": val})
        except ValueError:
            console.print(f"[bold red]Error:[/bold red] Invalid characteristic format '{item}'. Use 'key=value'.")
            raise typer.Exit(code=1)
    return parsed_list

# --- GENERATIVE COMMAND (Simplified for CLI usage) ---

@app.command()
def generate(
    prompt: str = typer.Argument(..., help="The text prompt to send to the Generative API."),
    
    # Mandatory fields with sensible CLI defaults
    agent_id: str = typer.Option(AGENT_ID_DEFAULT, help="[MANDATORY] The ID of the agent to use."),
    session_id: str = typer.Option(..., help="[MANDATORY] A unique session ID for the request."),
    

    agent_version: Optional[str] = typer.Option(AGENT_VERSION_DEFAULT, help="[MANDATORY] The version ID of the agent instance."),
    web_search: bool = typer.Option(False, help="Enable web search for the request."),
    reasoning: bool = typer.Option(False, help="Enable reasoning ability."),

    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", help="Override TUUL_API_KEY environment variable."),
):
    """
    Test the Generative API. Uses defaults for platform/agent IDs for ease of use.
    """
    client = get_client(api_key)
    try:
        with console.status("Generating response..."):
            resp = client.generative.create(
                prompt=prompt,
                agent_id=agent_id,
                agent_version=agent_version,
                session_id=session_id,
                web_search=web_search,
                reasoning=reasoning
            )
        
        console.print(f"\n[bold green]Response (Generative):[/bold green] {resp.content}")
        console.print(f"[dim]ID: {resp.id}[/dim]")
        console.print(f"[dim]Usage: {resp.usage}[/dim]")
    except TuulError as e:
        console.print(f"\n[bold red]API Error:[/bold red] {e}")
        raise typer.Exit(code=1)

# --- LITE COMMAND (Uses the required mandatory fields) ---

@app.command()
def lite(
    prompt: str = typer.Argument(..., help="The text prompt for the Lite Mode API."),
    session_id: str = typer.Option(..., help="[MANDATORY] A unique session ID for the request."),
    characteristic: Optional[List[str]] = typer.Option(
        None, 
        "--characteristic", "-c", 
        callback=parse_characteristics,
        help="Custom characteristic in 'key=value' format. Can be used multiple times."
    ),
    cache_session: bool = typer.Option(False, "--cache", help="Set to cache the session state."),
    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", help="Override TUUL_API_KEY environment variable."),
):
    """
    Test the Lite Mode API. Requires session_id and accepts optional characteristics.
    """
    client = get_client(api_key)
    try:
        with console.status("Generating lite response..."):
            # The callback handles converting CLI strings to dicts for the SDK
            resp = client.lite.generate(
                prompt=prompt,
                session_id=session_id,
                characteristics=characteristic,
                cache_session=cache_session
            )
        
        console.print(f"\n[bold green]Response (Lite):[/bold green] {resp.content}")
        # Note: We assume latency_ms is now correctly parsed and available
        if resp.latency_ms is not None:
             console.print(f"[dim]Latency: {resp.latency_ms:.2f}ms[/dim]")
    except TuulError as e:
        console.print(f"\n[bold red]API Error:[/bold red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()