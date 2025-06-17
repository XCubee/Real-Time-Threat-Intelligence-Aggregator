from dotenv import load_dotenv
import os
import httpx
import asyncio
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from typing import Optional

# Initialize Typer app and Rich console
app = typer.Typer()
console = Console()

# Load environment variables
load_dotenv()
API_KEY = "2540d16c13e406266dfbd6fb360e29f8600f7ffa619a811ce9af1616ea5a174c7f9d722d7c5019aa"


# AbuseIPDB API endpoint
API_URL = "https://api.abuseipdb.com/api/v2/check"

# Headers for the request
HEADERS = {
    "Key": API_KEY,
    "Accept": "application/json"
}

async def fetch_abuseip(ip: str) -> Optional[dict]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL, headers=HEADERS, params={"ipAddress": ip})
            response.raise_for_status()
            return response.json()["data"]
    except httpx.HTTPError as e:
        console.print(f"[red]HTTP Error occurred: {e}[/red]")
        return None
    except Exception as e:
        console.print(f"[red]An error occurred: {e}[/red]")
        return None

def create_result_table(data: dict) -> Table:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    # Add rows with formatted data
    table.add_row("IP Address", data["ipAddress"])
    table.add_row("Abuse Confidence Score", str(data["abuseConfidenceScore"]))
    table.add_row("Country Code", data["countryCode"])
    table.add_row("Domain", data.get("domain", "N/A"))
    table.add_row("Total Reports", str(data.get("totalReports", 0)))
    table.add_row("Last Reported", data.get("lastReportedAt", "Never"))
    
    return table

@app.command()
def check_ip(ip: str = typer.Argument(None, help="IP address to check")):
    """Check an IP address for potential threats using AbuseIPDB."""
    
    # If no IP provided, ask for input
    if ip is None:
        ip = typer.prompt("Enter IP address to check")
    
    # Print header
    console.print(Panel.fit(
        "[bold blue]IP Threat Checker[/bold blue]\n"
        "[italic]Powered by AbuseIPDB[/italic]",
        border_style="blue"
    ))
    
    # Show progress spinner
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        progress.add_task(description="Checking IP...", total=None)
        result = asyncio.run(fetch_abuseip(ip))
    
    if result:
        # Create and display the result table
        table = create_result_table(result)
        console.print("\n[bold]Results:[/bold]")
        console.print(table)
        
        # Add a summary panel
        score = result["abuseConfidenceScore"]
        if score == 0:
            status = "[green]SAFE[/green]"
        elif score < 25:
            status = "[yellow]LOW RISK[/yellow]"
        elif score < 75:
            status = "[orange]MEDIUM RISK[/orange]"
        else:
            status = "[red]HIGH RISK[/red]"
            
        console.print(Panel.fit(
            f"Status: {status}\n"
            f"Threat Percentage : {score}%",
            title="Summary",
            border_style="blue"
        ))
    else:
        console.print("[red]Failed to fetch IP data[/red]")

if __name__ == "__main__":
    app()
