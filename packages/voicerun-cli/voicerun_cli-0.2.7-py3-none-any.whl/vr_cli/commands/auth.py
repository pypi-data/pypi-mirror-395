import time

import requests
import typer
from rich.table import Table

from ..utils.config import (
    API_BASE_URL,
    ID_STYLE,
    TITLE_STYLE,
    MAX_POLL_ATTEMPTS,
    POLL_INTERVAL,
)
from ..utils.utils import (
    confirm,
    console,
    format_date,
    get_authenticated_session,
    handle_http_error,
    make_request,
    open_browser,
    prompt,
    save_cookie,
    save_api_key,
    load_api_key,
    print_success,
    print_error,
    print_warning,
    print_info,
)

app = typer.Typer()


@app.command("signin")
def signin():
    """Sign in to the API."""
    try:
        session = get_authenticated_session()
        response = session.get(f"{API_BASE_URL}/v1/auth/session")
        if response.status_code == 200:
            print_success("Already signed in")
            return

        # Prompt for authentication method
        print_info("Authentication methods:")
        print_info("  1: Web browser (default)")
        print_info("  2: Email/Password")
        print_info("  3: API Key")
        auth_method = prompt(
            "Choose authentication method [1/2/3]",
            default="1",
            validation=None
        )

        if auth_method == "1":
            signin_web()
            return
        elif auth_method == "3":
            signin_api_key()
            return

        # Default to email/password
        email = prompt("Email")
        password = prompt("Password", hide_input=True)
        response = requests.post(
            f"{API_BASE_URL}/v1/auth/signin",
            json={"email": email, "password": password},
        )
        response.raise_for_status()
        if response.status_code == 204:
            set_cookie = response.headers.get("Set-Cookie")
            if set_cookie:
                cookie_value = set_cookie.split(";")[0]
                save_cookie(cookie_value)
                print_success("Successfully signed in!")
            else:
                print_warning("No Set-Cookie header received")
        else:
            try:
                print_error(response.json())
            except requests.exceptions.JSONDecodeError:
                print_error(f"Server response (not JSON): {response.text}")
                print_error(
                    f"Status code: '[{ID_STYLE}]{response.status_code}[/{ID_STYLE}]'"
                )
    except requests.HTTPError as e:
        handle_http_error(e)


def signin_api_key():
    """Sign in to the API using an API key."""
    try:
        api_key = prompt("Enter your API key")

        # Test the API key by making a request
        session = requests.Session()
        session.headers["Authorization"] = f"Bearer {api_key}"
        response = session.get(f"{API_BASE_URL}/v1/auth/session")
        response.raise_for_status()

        if response.status_code == 200:
            # Clear any existing cookie and save the API key
            save_cookie("")
            save_api_key(api_key)
            print_success("Successfully signed in with API key!")
        else:
            print_error("Invalid API key")
    except requests.HTTPError as e:
        print_error("Invalid API key or authentication failed")
        handle_http_error(e)
    except Exception as e:
        print_error(str(e))


@app.command("signout")
def signout():
    """Sign out of the API."""
    try:
        get_authenticated_session()
        save_cookie("")
        save_api_key("")
        print_success("Successfully signed out")
    except requests.HTTPError as e:
        handle_http_error(e)


def signin_web():
    """Sign in to the API via browser."""
    try:
        response = requests.post(f"{API_BASE_URL}/v1/auth/cli-login")
        response.raise_for_status()
        data = response.json()

        login_token = data.get("login_token")
        login_url = data.get("login_url")
        if not login_token or not login_url:
            print_error("Server did not return a login token or URL.")
            return

        open_browser(login_url)
        print_info(
            "Please complete the login in your browser. Waiting for completion..."
        )

        for _ in range(MAX_POLL_ATTEMPTS):  # Poll for up to 2 minutes
            poll = requests.get(
                f"{API_BASE_URL}/v1/auth/cli-check-login", params={"token": login_token}
            )
            poll.raise_for_status()
            poll_data = poll.json()
            if poll_data.get("status") == "complete" and poll_data.get(
                "session_cookie"
            ):
                save_cookie(f"appSession={poll_data['session_cookie']}")
                print_success("Successfully signed in!")
                return
            time.sleep(POLL_INTERVAL)
        print_warning("Login not completed in time. Please try again.")
    except requests.HTTPError as e:
        handle_http_error(e)
    except Exception as e:
        print_error(str(e))


@app.command("apikey-list")
def apikey_list():
    """List all API keys for the authenticated user."""
    try:
        response = make_request("/v1/users/apiKeys")

        if response and "data" in response:
            api_keys = response["data"]

            if not api_keys:
                print_info("No API keys found")
                return

            table = Table(title="API Keys", title_style=TITLE_STYLE)
            table.add_column("ID", style=ID_STYLE)
            table.add_column("Description")
            table.add_column("Last Used")
            table.add_column("Created")

            for key in api_keys:
                table.add_row(
                    key.get("id", ""),
                    key.get("description") or "N/A",
                    format_date(key.get("lastUsedAt")) or "Never",
                    format_date(key.get("createdAt")) or "N/A"
                )

            console.print(table)
    except Exception as e:
        print_error(f"Failed to list API keys: {str(e)}")


@app.command("apikey-create")
def apikey_create(description: str = typer.Option(None, "--description", "-d", help="Description for the API key")):
    """Create a new API key."""
    try:
        if not description:
            description = prompt("API key description (optional)", validation=None, default="")

        body = {}
        if description:
            body["description"] = description

        response = make_request("/v1/users/apiKeys", method="POST", json=body)

        if response and "data" in response:
            data = response["data"]
            token = data.get("token")

            print_success("API key created successfully!")
            print_info(f"API Key ID: [{ID_STYLE}]{data.get('id')}[/{ID_STYLE}]")
            if data.get("description"):
                print_info(f"Description: {data.get('description')}")
            print_warning("\nIMPORTANT: Save this token securely. It will not be shown again!")
            print_info(f"\nToken: {token}\n")

            use_now = confirm("Use this API key for authentication now?", default=False)
            if use_now:
                save_cookie("")  # Clear cookie
                save_api_key(token)
                print_success("API key saved. You are now authenticated with this key.")
        else:
            print_error("Failed to create API key")
    except Exception as e:
        print_error(f"Failed to create API key: {str(e)}")


@app.command("apikey-delete")
def apikey_delete(key_id: str = typer.Argument(..., help="API key ID to delete")):
    """Delete an API key."""
    try:
        confirm_delete = confirm(f"Are you sure you want to delete API key '{key_id}'?", default=False)
        if not confirm_delete:
            print_info("Deletion cancelled")
            return

        response = make_request(f"/v1/users/apiKeys/{key_id}", method="DELETE")

        if response is not None:
            print_success(f"API key '[{ID_STYLE}]{key_id}[/{ID_STYLE}]' deleted successfully")
        else:
            print_error("Failed to delete API key")
    except Exception as e:
        print_error(f"Failed to delete API key: {str(e)}")
