#!/usr/bin/env python3
import click
from viafoundry.auth import Auth
from viafoundry.client import ViaFoundryClient
from viafoundry import __version__  # Import the version
import json
import logging
import os
from typing import Optional

# Configure logging
logging.basicConfig(filename="viafoundry_errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, help="Show the version of the ViaFoundry CLI.")
@click.option('--config', type=click.Path(), help="Path to a custom configuration file.")
@click.pass_context
def cli(ctx: click.Context, version: bool, config: str) -> None:
    """ViaFoundry CLI for configuration, endpoint discovery, and API requests.

    Args:
        ctx (click.Context): Click context object.
        version (bool): Flag to show version information.
        config (str): Path to custom configuration file.
    """
    if version:
        click.echo(f"ViaFoundry CLI version {__version__}")
        return

    ctx.ensure_object(dict)
    try:
        ctx.obj['client'] = ViaFoundryClient(config)
        ctx.obj['auth'] = Auth(config)
    except Exception as e:
        logging.error("Failed to initialize ViaFoundry client or authentication", exc_info=True)
        click.echo("Error: Failed to initialize the CLI. Please check your configuration file.", err=True)
        raise click.Abort()

@cli.command()
@click.option('--hostname', default=None, help="API Hostname, e.g., https://viafoundry.com")
@click.option('--username', default=None, help="Login username")
@click.option('--password', default=None, help="Login password")
@click.option('--token', default=None, help="Personal access token (alternative to username/password)")
@click.option('--identity-type', default=1, type=int, help="Identity type (default: 1)")
@click.option('--redirect-uri', default="https://viafoundry.com/user", help="Redirect URI (default: https://viafoundry.com/user)")
@click.pass_context
def configure(ctx: click.Context, hostname: str = None, username: str = None, password: str = None, token: str = None,
           identity_type: int = 1, redirect_uri: str = "https://viafoundry.com/user") -> None:
    """Configure the SDK with authentication details.
    
    You can authenticate using either:
    1. Personal access token (recommended)
    2. Username and password
    
    Examples:
        foundry configure --hostname https://viafoundry.com --token <your_token>
        foundry configure --hostname https://viafoundry.com --username user --password pass

    Args:
        ctx (click.Context): Click context object.
        hostname (str): API hostname URL.
        username (str, optional): Login username.
        password (str, optional): Login password.
        token (str, optional): Personal access token.
        identity_type (int, optional): Identity type. Defaults to 1.
        redirect_uri (str, optional): Redirect URI. Defaults to "https://viafoundry.com/user".
    """
    auth = ctx.obj['auth']
    try:
        # Prompt for hostname if not provided
        if not hostname:
            hostname = click.prompt("API Hostname", type=str)
        
        # If token is provided via CLI, use token auth
        if token:
            auth.configure_token(hostname, token)
            click.echo("Configuration saved successfully using token.")
        # If username is provided via CLI, use username/password auth
        elif username:
            if not password:
                password = click.prompt("Password", hide_input=True, type=str)
            auth.configure(hostname, username, password, identity_type=identity_type, redirect_uri=redirect_uri)
            click.echo("Configuration saved successfully.")
        # Interactive mode: ask user to choose
        else:
            click.echo("\nChoose authentication method:")
            click.echo("  1. Token (recommended)")
            click.echo("  2. Username and Password")
            auth_choice = click.prompt("Enter choice", type=click.Choice(['1', '2']), show_choices=False)
            
            if auth_choice == '1':
                token = click.prompt("Personal Access Token", type=str)
                auth.configure_token(hostname, token)
                click.echo("Configuration saved successfully using token.")
            else:
                username = click.prompt("Username", type=str)
                password = click.prompt("Password", hide_input=True, type=str)
                auth.configure(hostname, username, password, identity_type=identity_type, redirect_uri=redirect_uri)
                click.echo("Configuration saved successfully.")
    except Exception as e:
        logging.error("Failed to configure authentication", exc_info=True)
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.option('--as-json', is_flag=True, help="Output the endpoints in JSON format.")
@click.option('--search', default=None, help="Search term to filter endpoints. Use freely or as 'key=value'.")
@click.pass_context
def discover(ctx: click.Context, as_json: bool, search: Optional[str]) -> None:
    """List all available API endpoints with optional filtering.

    Args:
        ctx (click.Context): Click context object.
        as_json (bool): Flag to output in JSON format.
        search (str, optional): Search term to filter endpoints.
    """
    client = ctx.obj['client']
    try:
        endpoints = client.discover()  # Assume this returns a dictionary {endpoint: methods}.
        filtered_endpoints = {}

        # Parse search term
        search_key, search_value = None, None
        if search:
            if '=' in search:
                search_key, search_value = search.split('=', 1)
            else:
                search_value = search.lower()

        # Filter endpoints
        for endpoint, methods in endpoints.items():
            for method, details in methods.items():
                description = details.get('description', '').lower()
                include = False

                # Filter logic
                if search_key and search_value:
                    if search_key == 'endpoint' and search_value in endpoint.lower():
                        include = True
                    elif search_key == 'description' and search_value in description:
                        include = True
                elif search_value:  # Search all fields freely
                    if (search_value in endpoint.lower() or
                            search_value in description or
                            search_value in method.lower()):
                        include = True
                else:
                    include = True  # No search term provided, include all

                if include:
                    if endpoint not in filtered_endpoints:
                        filtered_endpoints[endpoint] = {}
                    filtered_endpoints[endpoint][method] = details

        # Output results
        if as_json:
            # Output filtered data as JSON
            click.echo(json.dumps(filtered_endpoints, indent=4))
        else:
            # Output filtered data in formatted text
            click.echo("Available API Endpoints:\n")
            for endpoint, methods in filtered_endpoints.items():
                for method, details in methods.items():
                    description = details.get('description', 'No description available')
                    click.echo(f"Endpoint: {endpoint}")
                    click.echo(f"Method: {method}")
                    click.echo(f"Description: '{description}'")
                    
                    # If the method is POST, print the required data
                    if method.lower() == 'post':
                        request_body = details.get('requestBody', {})
                        if 'application/json' in request_body.get('content', {}):
                            schema = request_body['content']['application/json'].get('schema', {})
                            click.echo(f"Data to send: {json.dumps(schema, indent=4)}")
                        else:
                            click.echo("Data to send: No specific schema provided.\n")
                    click.echo()  # Add a newline for readability
    except Exception as e:
        logging.error("Failed to discover endpoints", exc_info=True)
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.option('--endpoint', prompt="API Endpoint", help="The API endpoint to call (e.g., /api/some/endpoint).")
@click.option('--method', default="GET", help="HTTP method to use (GET, POST, etc.).")
@click.option('--params', default=None, help="Query parameters as JSON.")
@click.option('--data', default=None, help="Request body as JSON.")
@click.pass_context
def call(ctx: click.Context, endpoint: str, method: str, params: Optional[str], data: Optional[str]) -> None:
    """Call a specific API endpoint.

    Args:
        ctx (click.Context): Click context object.
        endpoint (str): The API endpoint to call.
        method (str): HTTP method to use.
        params (str, optional): Query parameters as JSON string.
        data (str, optional): Request body as JSON string.
    """
    client = ctx.obj['client']
    try:
        params = json.loads(params) if params else None
        data = json.loads(data) if data else None
        response = client.call(method, endpoint, params=params, data=data)
        click.echo(json.dumps(response, indent=4))
    except json.JSONDecodeError as e:
        click.echo("Error: Invalid JSON format for parameters or data.", err=True)
    except Exception as e:
        logging.error("Failed to call API endpoint", exc_info=True)
        click.echo(f"Error: {e}", err=True)

@cli.group()
@click.pass_context
def reports(ctx: click.Context) -> None:
    """Commands related to reports.

    Args:
        ctx (click.Context): Click context object.
    """
    pass

@reports.command()
@click.argument("report_id", required=False)
@click.option("--reportID", help="Report ID (alternative to positional argument).")
@click.pass_context
def fetch(ctx: click.Context, report_id: Optional[str], reportid: Optional[str]) -> None:
    """Fetch JSON data for a report.

    Args:
        ctx (click.Context): Click context object.
        report_id (str, optional): Report ID as positional argument.
        reportid (str, optional): Report ID as named argument.
    """
    client = ctx.obj["client"]
    report_id = report_id or reportid
    if not report_id:
        click.echo("Error: Report ID is required.", err=True)
        return
    try:
        report_data = client.reports.fetch_report_data(report_id)
        click.echo(json.dumps(report_data, indent=4))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@reports.command()
@click.argument("report_id", required=False)
@click.option("--reportID", help="Report ID (alternative to positional argument).")
@click.pass_context
def list_processes(ctx: click.Context, report_id: Optional[str], reportid: Optional[str]) -> None:
    """List unique processes in a report.

    Args:
        ctx (click.Context): Click context object.
        report_id (str, optional): Report ID as positional argument.
        reportid (str, optional): Report ID as named argument.
    """
    client = ctx.obj["client"]
    report_id = report_id or reportid
    if not report_id:
        click.echo("Error: Report ID is required.", err=True)
        return
    try:
        report_data = client.reports.fetch_report_data(report_id)
        process_names = client.reports.get_process_names(report_data)
        click.echo("\n".join(process_names))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@reports.command()
@click.argument("report_id", required=False)
@click.argument("process_name", required=False)
@click.option("--reportID", help="Report ID (alternative to positional argument).")
@click.option("--processName", help="Process name (alternative to positional argument).")
@click.pass_context
def list_files(ctx: click.Context, report_id: Optional[str], process_name: Optional[str], 
              reportid: Optional[str], processname: Optional[str]) -> None:
    """List files for a specific process.

    Args:
        ctx (click.Context): Click context object.
        report_id (str, optional): Report ID as positional argument.
        process_name (str, optional): Process name as positional argument.
        reportid (str, optional): Report ID as named argument.
        processname (str, optional): Process name as named argument.
    """
    client = ctx.obj["client"]
    report_id = report_id or reportid
    process_name = process_name or processname
    if not report_id or not process_name:
        click.echo("Error: Report ID and Process Name are required.", err=True)
        return
    try:
        report_data = client.reports.fetch_report_data(report_id)
        files = client.reports.get_file_names(report_data, process_name)
        click.echo(files.to_string())
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@reports.command()
@click.argument("report_id", required=False)
@click.argument("file_path", required=False)
@click.argument("download_dir", required=False, default=os.getcwd())
@click.option("--reportID", help="Report ID (alternative to positional argument).")
@click.option("--filePath", help="File Path dir/filename in pubweb directory (alternative to positional argument).")
@click.option("--downloadDir", default=os.getcwd(), help="Directory to save the file.")

@click.pass_context
def download_file(ctx, report_id, file_path, download_dir, reportid, filepath, downloaddir, ):
    """Download a file from a report."""
    client = ctx.obj["client"]
    report_id = report_id or reportid
    download_dir = download_dir or downloaddir
    file_path = file_path or filepath
    if not report_id or not file_path :
        click.echo("Error: Report ID, and File Name are required.", err=True)
        return
    try:
        report_data = client.reports.fetch_report_data(report_id)
        download_file_path = client.reports.download_file(report_data, file_path, download_dir)
        click.echo(f"File downloaded to: {download_file_path}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@reports.command()
@click.argument("report_id", required=False)
@click.option("--reportID", help="Report ID (alternative to positional argument).")
@click.pass_context
def list_all_files(ctx, report_id, reportid):
    """List all files for a specific report."""
    client = ctx.obj["client"]
    report_id = report_id or reportid
    if not report_id:
        click.echo("Error: Report ID is required.", err=True)
        return
    try:
        report_data = client.reports.fetch_report_data(report_id)
        all_files = client.reports.get_all_files(report_data)
        click.echo(all_files.to_string())
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@reports.command()
@click.argument("report_id", required=False)
@click.option("--reportID", help="Report ID (alternative to positional argument).")
@click.pass_context
def get_report_dirs(ctx, report_id, reportid):
    """List all dirs for a specific report."""
    client = ctx.obj["client"]
    report_id = report_id or reportid
    if not report_id:
        click.echo("Error: Report ID is required.", err=True)
        return
    try:
        report_dirs = client.reports.get_report_dirs(report_id)
        click.echo(report_dirs)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@reports.command()
@click.argument("report_id", required=False, type=str)
@click.argument("local_file_path", required=False, type=click.Path(exists=True))
@click.argument("remote_dir", required=False, type=str)
@click.option("--reportID", type=str, help="Report ID (alternative to positional argument).")
@click.option("--localFilePath", type=click.Path(exists=True), help="Local file path (alternative to positional argument).")
@click.option("--remoteDir", type=str, help="Directory name for organizing files (alternative to positional argument).")
@click.pass_context
def upload_report_file(ctx, report_id, local_file_path, remote_dir, reportid, localfilepath, remotedir):
    """
    Upload a file to a report.

    REPORT_ID: The ID of the report .
    FILE_PATH: The local file path of the file to upload (optional; can be specified with --filePath).
    REMOTE_DIR: Directory name for organizing files (optional; can be specified with --remoteDir).

    Examples:
      viafoundry upload-report-file <report_id> <file_path> <directory>
      viafoundry upload-report-file --reportID <report_id> --filePath <path_to_file> --remoteDir <directory>
    """
    try:
        # Fallback to options if arguments are not provided
        report_id = report_id or reportid
        local_file_path = local_file_path or localfilepath
        remote_dir = remote_dir or remotedir

        # Ensure mandatory fields are present
        if not local_file_path:
            raise ValueError("File path is required. Provide it as an argument or use the --filePath option.")
        
        # Initialize client and call upload
        client = ctx.obj["client"]
        response = client.reports.upload_report_file(report_id, local_file_path, remote_dir)
        click.echo(f"File uploaded successfully: {response}")
    except Exception as e:
        click.echo(f"Failed to upload file: {e}", err=True)

@cli.group()
@click.pass_context
def process(ctx: click.Context) -> None:
    """Commands related to process.

    Args:
        ctx (click.Context): Click context object.
    """
    pass

@process.command()
@click.pass_context
def list_processes(ctx: click.Context) -> None:
    """List all processes.

    Args:
        ctx (click.Context): Click context object.
    """
    client = ctx.obj["client"]
    processes = client.process.list_processes()
    click.echo(processes)

@process.command()
@click.argument("process_id", required=False, type=str)
@click.option("--processID", type=str, help="Process ID (alternative to positional argument).")
@click.pass_context
def get_process(ctx, process_id, processid):
    """Get details of a specific process."""
    client = ctx.obj["client"]
    process_id = process_id or processid
    process_info = client.process.get_process(process_id)
    click.echo(process_info)

@process.command()
@click.argument("process_id", required=False, type=str)
@click.option("--processID", type=str, help="Process ID (alternative to positional argument).")
@click.pass_context
def get_revisions(ctx, process_id, processid):
    """Get revisions for a specific process."""
    client = ctx.obj["client"]
    process_id = process_id or processid
    revisions = client.process.get_process_revisions(process_id)
    click.echo(revisions)

@process.command()
@click.argument("process_id", required=False, type=str)
@click.option("--processID", type=str, help="Process ID (alternative to positional argument).")
@click.pass_context
def check_usage(ctx: click.Context, process_id: Optional[str], processid: Optional[str]) -> None:
    """Check if a process is used in pipelines or runs.

    Args:
        ctx (click.Context): Click context object.
        process_id (str, optional): Process ID as positional argument.
        processid (str, optional): Process ID as named argument.
    """
    client = ctx.obj["client"]
    usage_info = client.process.check_usage(process_id)
    click.echo(usage_info)

@process.command()
@click.argument("process_id", required=False, type=str)
@click.option("--processID", type=str, help="Process ID (alternative to positional argument).")
@click.pass_context
def duplicate_process(ctx: click.Context, process_id: Optional[str], processid: Optional[str]) -> None:
    """Duplicate a process.

    Args:
        ctx (click.Context): Click context object.
        process_id (str, optional): Process ID as positional argument.
        processid (str, optional): Process ID as named argument.
    """
    client = ctx.obj["client"]
    duplicated_process = client.process.duplicate_process(process_id)
    click.echo(duplicated_process)

@process.command()
@click.argument("menu_name", required=False, type=str)
@click.option("--menuName", type=str, help="Menu name (alternative to positional argument).")
@click.pass_context
def create_menu_group(ctx: click.Context, menu_name: Optional[str], menuname: Optional[str]) -> None:
    """Create a new menu group.

    Args:
        ctx (click.Context): Click context object.
        menu_name (str, optional): Menu name as positional argument.
        menuname (str, optional): Menu name as named argument.
    """
    client = ctx.obj["client"]
    new_menu_group = client.process.create_menu_group(menu_name)
    click.echo(new_menu_group)

@process.command()
@click.argument("process_data", required=False, type=click.File('r'))
@click.option("--processData", type=click.File('r'), help="Process Data (alternative to positional argument).")

@click.pass_context
def create_process(ctx: click.Context, process_data: Optional[click.File], processdata: Optional[click.File]) -> None:
    """Create a new process from a JSON file.

    Args:
        ctx (click.Context): Click context object.
        process_data (click.File, optional): JSON data for the new process.
        processdata (click.File, optional): JSON data for the new process as named argument.
    """
    client = ctx.obj["client"]
    process_data = process_data or processdata
    process_data = json.load(process_data)
    response = client.process.create_process(process_data)
    click.echo(response)

@process.command()
@click.argument("menu_group_id", required=False, type=int)
@click.argument("menu_name", required=False, type=str)
@click.option("--menuGroupID", type=int, help="Menu Group ID (alternative to positional argument).")
@click.option("--menuName", type=str, help="Menu Name (alternative to positional argument).")
@click.pass_context
def update_menu_group(ctx: click.Context, menu_group_id: Optional[int], menu_name: Optional[str], menugroupid: Optional[int], menuname: Optional[str]) -> None:
    """Update an existing menu group.

    Args:
        ctx (click.Context): Click context object.
        menu_group_id (int, optional): ID of the menu group to update.
        menu_name (str, optional): New name for the menu group.
        menugroupid (int, optional): ID of the menu group to update as named argument.
        menuname (str, optional): New name for the menu group as named argument.
    """
    client = ctx.obj["client"]
    menu_group_id = menu_group_id or menugroupid
    menu_name = menu_name or menuname

    if not menu_group_id or not menu_name:
        click.echo("Error: Both Menu Group ID and Menu Name are required.", err=True)
        return

    response = client.process.update_menu_group(menu_group_id, menu_name)
    click.echo(response)


@process.command()
@click.argument("process_id", required=False, type=str)
@click.argument("process_data", required=False, type=click.File('r'))
@click.option("--processID", type=str, help="Process ID (alternative to positional argument).")
@click.option("--processData", type=click.File('r'), help="Process Data (alternative to positional argument).")
@click.pass_context
def update_process(ctx: click.Context, process_id: Optional[str], process_data: Optional[click.File], processid: Optional[str], processdata: Optional[click.File]) -> None:
    """Update an existing process.

    Args:
        ctx (click.Context): Click context object.
        process_id (str, optional): ID of the process to update.
        process_data (click.File, optional): JSON data for the updated process.
        processid (str, optional): ID of the process to update as named argument.
        processdata (click.File, optional): JSON data for the updated process as named argument.
    """
    client = ctx.obj["client"]
    process_id = process_id or processid
    process_data = process_data or processdata

    if not process_id or not process_data:
        click.echo("Error: Both Process ID and Process Data are required.", err=True)
        return

    process_data = json.load(process_data)
    response = client.process.update_process(process_id, process_data)
    click.echo(response)


@process.command()
@click.argument("process_id", required=False, type=str)
@click.option("--processID", type=str, help="Process ID (alternative to positional argument).")
@click.pass_context
def delete_process(ctx: click.Context, process_id: Optional[str], processid: Optional[str]) -> None:
    """Delete an existing process.

    Args:
        ctx (click.Context): Click context object.
        process_id (str, optional): ID of the process to delete.
        processid (str, optional): ID of the process to delete as named argument.
    """
    client = ctx.obj["client"]
    process_id = process_id or processid

    if not process_id:
        click.echo("Error: Process ID is required.", err=True)
        return

    response = client.process.delete_process(process_id)
    click.echo(response)

@process.command()
@click.pass_context
def list_parameters(ctx: click.Context) -> None:
    """List all parameters.

    Args:
        ctx (click.Context): Click context object.
    """
    client = ctx.obj["client"]
    response = client.process.list_parameters()
    click.echo(response)


@process.command()
@click.argument("parameter_data", required=False, type=click.File('r'))
@click.option("--parameterData", type=click.File('r'), help="Parameter Data (alternative to positional argument).")
@click.pass_context
def create_parameter(ctx: click.Context, parameter_data: Optional[click.File], parameterdata: Optional[click.File]) -> None:
    """Create a new parameter.

    Args:
        ctx (click.Context): Click context object.
        parameter_data (click.File, optional): Data for the new parameter.
        parameterdata (click.File, optional): Data for the new parameter as named argument.
    """
    client = ctx.obj["client"]
    parameter_data = parameter_data or parameterdata

    if not parameter_data:
        click.echo("Error: Parameter Data is required.", err=True)
        return

    parameter_data = json.load(parameter_data)
    response = client.process.create_parameter(parameter_data)
    click.echo(response)


@process.command()
@click.argument("parameter_id", required=False, type=str)
@click.argument("parameter_data", required=False, type=click.File('r'))
@click.option("--parameterID", type=str, help="Parameter ID (alternative to positional argument).")
@click.option("--parameterData", type=click.File('r'), help="Parameter Data (alternative to positional argument).")
@click.pass_context
def update_parameter(ctx: click.Context, parameter_id: Optional[str], parameter_data: Optional[click.File], parameterid: Optional[str], parameterdata: Optional[click.File]) -> None:
    """Update an existing parameter.

    Args:
        ctx (click.Context): Click context object.
        parameter_id (str, optional): ID of the parameter to update.
        parameter_data (click.File, optional): New data for the parameter.
        parameterid (str, optional): ID of the parameter to update as named argument.
        parameterdata (click.File, optional): New data for the parameter as named argument.
    """
    client = ctx.obj["client"]
    parameter_id = parameter_id or parameterid
    parameter_data = parameter_data or parameterdata

    if not parameter_id or not parameter_data:
        click.echo("Error: Both Parameter ID and Parameter Data are required.", err=True)
        return

    parameter_data = json.load(parameter_data)
    response = client.process.update_parameter(parameter_id, parameter_data)
    click.echo(response)


@process.command()
@click.argument("parameter_id", required=False, type=str)
@click.option("--parameterID", type=str, help="Parameter ID (alternative to positional argument).")
@click.pass_context
def delete_parameter(ctx: click.Context, parameter_id: Optional[str], parameterid: Optional[str]) -> None:
    """Delete an existing parameter.

    Args:
        ctx (click.Context): Click context object.
        parameter_id (str, optional): ID of the parameter to delete.
        parameterid (str, optional): ID of the parameter to delete as named argument.
    """
    client = ctx.obj["client"]
    parameter_id = parameter_id or parameterid

    if not parameter_id:
        click.echo("Error: Parameter ID is required.", err=True)
        return

    response = client.process.delete_parameter(parameter_id)
    click.echo(response)

@process.command()
@click.argument("group_name", required=True, type=str)
@click.pass_context
def get_menu_group_by_name(ctx: click.Context, group_name: str) -> None:
    """Find a menu group by its name and print its ID."""
    client = ctx.obj["client"]
    try:
        group_id = client.process.get_menu_group_by_name(group_name)
        if group_id:
            click.echo(group_id)
        else:
            click.echo(f"Menu group '{group_name}' not found.", err=True)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@process.command(name="get-parameters")
@click.option("--name", type=str, help="Filter by parameter name.")
@click.option("--qualifier", type=str, help="Filter by qualifier.")
@click.option("--filetype", type=str, help="Filter by file type.")
@click.option("--id", "id_", type=str, help="Filter by parameter ID.")
@click.pass_context
def get_parameters(ctx: click.Context, name: str, qualifier: str, filetype: str, id_: str) -> None:
    """Get parameters filtered by name, qualifier, filetype, or ID."""
    client = ctx.obj["client"]
    try:
        filtered = client.process.get_parameters(
            name=name,
            qualifier=qualifier,
            fileType=filetype,
            id_=id_
        )
        click.echo(filtered)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@process.command()
@click.option("--name", required=True, type=str, help="Process name.")
@click.option("--menu-group", required=True, type=str, help="Menu group name.")
@click.option("--input-params", required=True, type=click.File('r'), help="JSON file with input parameters.")
@click.option("--output-params", required=True, type=click.File('r'), help="JSON file with output parameters.")
@click.option("--summary", default="", type=str, help="Process summary.")
@click.option("--script-body", default="", type=str, help="Script body.")
@click.option("--script-language", default="bash", type=str, help="Script language.")
@click.option("--script-header", default="", type=str, help="Script header.")
@click.option("--script-footer", default="", type=str, help="Script footer.")
@click.option("--permission-settings", default=None, type=click.File('r'), help="JSON file with permission settings.")
@click.option("--revision-comment", default="Initial revision", type=str, help="Revision comment.")
@click.pass_context
def create_process_config(
    ctx: click.Context,
    name: str,
    menu_group: str,
    input_params,
    output_params,
    summary: str,
    script_body: str,
    script_language: str,
    script_header: str,
    script_footer: str,
    permission_settings,
    revision_comment: str
) -> None:
    """Create a full process configuration and print as JSON."""
    client = ctx.obj["client"]
    try:
        input_params_data = json.load(input_params)
        output_params_data = json.load(output_params)
        permission_settings_data = json.load(permission_settings) if permission_settings else None
        config = client.process.create_process_config(
            name=name,
            menu_group_name=menu_group,
            input_params=input_params_data,
            output_params=output_params_data,
            summary=summary,
            script_body=script_body,
            script_language=script_language,
            script_header=script_header,
            script_footer=script_footer,
            permission_settings=permission_settings_data,
            revision_comment=revision_comment
        )
        click.echo(json.dumps(config, indent=4))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        logging.critical("Critical error in CLI execution", exc_info=True)
        click.echo("A critical error occurred. Please check the logs for more details.", err=True)
