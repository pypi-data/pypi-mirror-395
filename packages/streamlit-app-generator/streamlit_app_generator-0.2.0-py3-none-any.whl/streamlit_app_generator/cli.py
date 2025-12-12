"""Command-line interface for streamlit-app-generator."""
import click
import sys
from typing import Optional, List
from pathlib import Path
from .generator import AppGenerator
from .wizard import SetupWizard

# Fix encoding for Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


@click.group()
@click.version_option(version="0.2.0")
def main() -> None:
    """Streamlit App Generator - Generate complete Streamlit applications with authentication and database templates."""
    pass


@main.command()
@click.argument("name")
@click.option(
    "--database",
    "-d",
    type=click.Choice(["postgresql", "mysql", "sqlite", "mongodb", "redis", "oracle"]),
    default="sqlite",
    help="Database type to use",
)
@click.option(
    "--auth",
    "-a",
    type=click.Choice(["basic", "modern", "minimal"]),
    default="basic",
    help="Authentication style",
)
@click.option(
    "--theme",
    "-t",
    type=click.Choice(["light", "dark"]),
    default="light",
    help="Application theme",
)
@click.option(
    "--pages",
    "-p",
    default="home,dashboard,settings",
    help="Comma-separated list of pages to create",
)
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Interactive mode with prompts",
)
@click.option(
    "--language",
    "-l",
    type=click.Choice(["en", "pt-BR", "pt"]),
    default=None,
    help="Language for wizard and messages (en=English, pt-BR=Portuguese)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default=".",
    help="Output directory",
)
def create(
    name: str,
    database: str,
    auth: str,
    theme: str,
    pages: str,
    interactive: bool,
    language: str,
    output: str,
) -> None:
    """Create a new Streamlit application.

    Args:
        name: Name of the application to create
        database: Database type to use
        auth: Authentication style
        theme: Application theme
        pages: Comma-separated list of pages
        interactive: Enable interactive mode
        output: Output directory

    Examples:
        \b
        # Create a basic app
        $ streamlit-app-generator create my_app

        \b
        # Create with PostgreSQL and modern auth
        $ streamlit-app-generator create my_app --database postgresql --auth modern

        \b
        # Interactive mode
        $ streamlit-app-generator create my_app --interactive
    """
    try:
        # Initialize i18n
        from .i18n import get_i18n
        i18n = get_i18n(language)
        t = i18n.t

        # Use rich interactive wizard if interactive mode is enabled
        if interactive:
            wizard = SetupWizard(language=language)
            config = wizard.run(name)

            if config is None:
                # User cancelled
                return

            name = config["name"]
            database = config["database"]
            auth = config["auth_style"]
            theme = config["theme"]
            page_list = config["pages"]
        else:
            # Non-interactive mode: use command line arguments
            page_list = [p.strip() for p in pages.split(",") if p.strip()]

            click.echo(f"\n🚀 {t('cli.creating', name=click.style(name, bold=True, fg='cyan'))}")
            click.echo(f"   🗄️  {t('cli.database')}: {database}")
            click.echo(f"   🔐 {t('cli.auth')}: {auth}")
            click.echo(f"   🎨 {t('cli.theme')}: {theme}")
            click.echo(f"   📄 {t('cli.pages')}: {', '.join(page_list)}\n")

        # Generate the app
        click.echo(f"⏳ {t('cli.generating')}")

        generator = AppGenerator(
            name=name,
            database=database,
            auth_style=auth,
            pages=page_list,
            theme=theme,
            output_dir=Path(output),
        )

        generator.generate()

        # Show next steps (wizard will show its own if interactive)
        if interactive:
            wizard = SetupWizard(language=language)
            wizard.show_next_steps(name, database)
        else:
            click.echo()
            click.echo(click.style(f"✅ {t('cli.success', name=name)}", fg="green", bold=True))
            click.echo()
            click.echo(f"{t('cli.next_steps')}")
            click.echo(f"   1️⃣  {t('cli.step_cd', name=name)}")
            click.echo(f"   2️⃣  {t('cli.step_install')}")
            click.echo(f"   3️⃣  {t('cli.step_config')}")
            click.echo(f"   4️⃣  {t('cli.step_run')}")
            click.echo()
            click.echo(f"   📖 {t('cli.see_docs')}")
            click.echo()

    except Exception as e:
        click.echo(f"\nError: {str(e)}", err=True)
        raise click.Abort()


@main.command()
@click.argument("database_type")
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True),
    default=".",
    help="Path to the Streamlit project",
)
def add_database(database_type: str, path: str) -> None:
    """Add a database connector to an existing project.

    Args:
        database_type: Type of database to add
        path: Path to the project

    Examples:
        \b
        $ streamlit-app-generator add-database postgresql
        $ streamlit-app-generator add-database mysql --path ./my_app
    """
    click.echo(f"Adding {database_type} database to project at {path}")
    click.echo("WARNING: This feature is coming soon!")


@main.command()
@click.argument("page_name")
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True),
    default=".",
    help="Path to the Streamlit project",
)
def add_page(page_name: str, path: str) -> None:
    """Add a new page to an existing project.

    Args:
        page_name: Name of the page to add
        path: Path to the project

    Examples:
        \b
        $ streamlit-app-generator add-page analytics
        $ streamlit-app-generator add-page reports --path ./my_app
    """
    click.echo(f"Adding page '{page_name}' to project at {path}")
    click.echo("WARNING: This feature is coming soon!")


@main.command()
def info() -> None:
    """Display information about streamlit-app-generator."""
    click.echo("\nStreamlit App Generator v0.1.0")
    click.echo("\nCreated by: Leandro Meyer")
    click.echo("License: MIT")
    click.echo("\nRepository: https://github.com/leandrodalcortivo/streamlit-app-generator.git")
    click.echo("\nSupported databases:")
    click.echo("  - PostgreSQL")
    click.echo("  - MySQL")
    click.echo("  - SQLite")
    click.echo("  - MongoDB")
    click.echo("  - Redis")
    click.echo("  - Oracle")
    click.echo("\nAuthentication styles:")
    click.echo("  - Basic - Simple and functional")
    click.echo("  - Modern - Beautiful UI with animations")
    click.echo("  - Minimal - Clean minimalist design")
    click.echo()


if __name__ == "__main__":
    main()
