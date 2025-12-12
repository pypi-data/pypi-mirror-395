"""AI chat commands for VirtualDojo CLI."""

from typing import Optional
from uuid import UUID

import typer

from ..client import SyncVirtualDojoClient
from ..utils.output import console, print_error, print_success

app = typer.Typer(help="AI chat and conversations")


@app.command("chat")
def chat(
    message: str = typer.Argument(..., help="Message to send to AI"),
    conversation_id: Optional[str] = typer.Option(
        None,
        "--conversation",
        "-c",
        help="Continue an existing conversation by ID",
    ),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """Send a message to the AI assistant.

    Examples:
        vdojo ai chat "How many accounts do I have?"
        vdojo ai chat "Create an opportunity for Acme Corp worth $50,000"
        vdojo ai chat "What are my top deals?" --conversation abc-123
    """
    try:
        client = SyncVirtualDojoClient(profile)

        data = {"message": message}
        if conversation_id:
            data["conversation_id"] = conversation_id

        result = client.post("/api/v1/ai/chat", data)

        response = result.get("response", "No response")
        conv_id = result.get("conversation_id")
        metadata = result.get("metadata", {})

        # Display the AI response
        console.print("\n[bold cyan]AI Assistant:[/bold cyan]")
        console.print(response)

        # Show citations if available
        citations = metadata.get("citations", [])
        if citations:
            console.print("\n[dim]Sources:[/dim]")
            for cite in citations:
                console.print(f"  - {cite.get('file_title', 'Unknown')} ({cite.get('relevance', 0):.0%})")

        # Show conversation ID for continuing
        if conv_id:
            console.print(f"\n[dim]Conversation ID: {conv_id}[/dim]")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("conversations")
def list_conversations(
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum conversations to return"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """List your AI conversations.

    Examples:
        vdojo ai conversations
        vdojo ai conversations --limit 10
    """
    try:
        client = SyncVirtualDojoClient(profile)
        result = client.get("/api/v1/ai/conversations", params={"limit": limit})

        conversations = result if isinstance(result, list) else result.get("data", [])

        if not conversations:
            console.print("[dim]No conversations found[/dim]")
            return

        from rich.table import Table

        table = Table(show_header=True, header_style="bold cyan", title="AI Conversations")
        table.add_column("ID", style="dim")
        table.add_column("Title")
        table.add_column("Messages")
        table.add_column("Last Activity")

        for conv in conversations:
            table.add_row(
                str(conv.get("id", "-"))[:8] + "...",
                conv.get("title", "-")[:40],
                str(conv.get("message_count", 0)),
                str(conv.get("last_activity_at", "-"))[:19],
            )

        console.print(table)
        console.print(f"\n[dim]{len(conversations)} conversations[/dim]")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)


@app.command("history")
def conversation_history(
    conversation_id: str = typer.Argument(..., help="Conversation ID"),
    limit: int = typer.Option(50, "--limit", "-l", help="Maximum messages to return"),
    profile: Optional[str] = typer.Option(None, "--profile", "-p"),
) -> None:
    """View messages from a conversation.

    Examples:
        vdojo ai history abc-123-def
        vdojo ai history abc-123-def --limit 10
    """
    try:
        client = SyncVirtualDojoClient(profile)
        result = client.get(
            f"/api/v1/ai/conversations/{conversation_id}/messages",
            params={"limit": limit},
        )

        messages = result if isinstance(result, list) else result.get("data", [])

        if not messages:
            console.print("[dim]No messages found[/dim]")
            return

        console.print(f"\n[bold]Conversation: {conversation_id}[/bold]\n")

        for msg in messages:
            sender = msg.get("sender_type", "unknown")
            text = msg.get("message_text", "")
            sent_at = str(msg.get("sent_at", ""))[:19]

            if sender == "user":
                console.print(f"[bold green]You[/bold green] [dim]({sent_at})[/dim]")
            else:
                console.print(f"[bold cyan]AI[/bold cyan] [dim]({sent_at})[/dim]")

            console.print(f"  {text}\n")

    except Exception as e:
        if hasattr(e, "message"):
            print_error(e.message, getattr(e, "hint", None))
        else:
            print_error(str(e))
        raise typer.Exit(1)
