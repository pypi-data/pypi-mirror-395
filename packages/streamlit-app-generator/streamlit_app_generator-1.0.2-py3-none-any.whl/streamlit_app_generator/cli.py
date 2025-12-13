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
@click.version_option(version="1.0.2")
@click.help_option("--help", "-h")
def main() -> None:
    """
    \b
    🚀 Streamlit App Generator v1.0.2

    Generate production-ready Streamlit applications with:
    • 🔐 Secure authentication (Basic, Modern, or Minimal styles)
    • 🗄️ Multiple database support (PostgreSQL, MySQL, SQLite, MongoDB, Redis, Oracle)
    • 👥 Admin Panel with user management (CRUD operations)
    • 🔒 Role-based access control (admin/user roles)
    • 🎨 Customizable themes (Light/Dark)
    • 📱 6 application templates (Basic, Dashboard, CRUD, E-commerce, Blog, Custom)

    \b
    Quick Start:
      streamlit-app-generator create my_app
      cd my_app
      pip install -r requirements.txt
      streamlit run app.py

    \b
    Login with:
      Username: admin | Password: admin123

    \b
    For more help on a specific command:
      streamlit-app-generator create --help
      streamlit-app-generator info

    \b
    Created by: Leandro Meyer Dal Cortivo
    GitHub: https://github.com/leandrodalcortivo/streamlit-app-generator
    """
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
    "--cloud-optimized",
    "-c",
    is_flag=True,
    help="Optimize for Streamlit Community Cloud deployment",
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
    cloud_optimized: bool,
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
            cloud_optimized=cloud_optimized,
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
    """Display detailed information about streamlit-app-generator."""
    click.echo()
    click.echo(click.style("━" * 70, fg="cyan"))
    click.echo(click.style("🚀 Streamlit App Generator v1.0.2", fg="cyan", bold=True))
    click.echo(click.style("━" * 70, fg="cyan"))
    click.echo()

    click.echo(click.style("📦 Features:", fg="yellow", bold=True))
    click.echo("  ✓ Production-ready Streamlit applications")
    click.echo("  ✓ Secure authentication with bcrypt password hashing")
    click.echo("  ✓ Admin Panel for user management (CRUD)")
    click.echo("  ✓ Role-based access control (admin/user)")
    click.echo("  ✓ Multi-database support")
    click.echo("  ✓ Interactive wizard in multiple languages")
    click.echo("  ✓ 6 application templates")
    click.echo()

    click.echo(click.style("🗄️  Supported Databases:", fg="yellow", bold=True))
    click.echo("  📁 SQLite       - Lightweight, zero-config (default)")
    click.echo("  🐘 PostgreSQL   - Production-grade relational DB")
    click.echo("  🐬 MySQL        - Popular relational database")
    click.echo("  🍃 MongoDB      - NoSQL document database")
    click.echo("  🔴 Redis        - In-memory data store")
    click.echo("  🏛️  Oracle       - Enterprise database")
    click.echo()

    click.echo(click.style("🔐 Authentication Styles:", fg="yellow", bold=True))
    click.echo("  • Basic   - Simple and functional login")
    click.echo("  • Modern  - Beautiful UI with gradients and animations")
    click.echo("  • Minimal - Clean minimalist design")
    click.echo()

    click.echo(click.style("📱 Application Templates:", fg="yellow", bold=True))
    click.echo("  1. Basic App         - General purpose, prototypes")
    click.echo("  2. Dashboard         - Business intelligence, analytics")
    click.echo("  3. CRUD Application  - Management systems, admin panels")
    click.echo("  4. E-commerce        - Online shops, product catalogs")
    click.echo("  5. Blog/CMS          - Content management platforms")
    click.echo("  6. Custom            - Define your own pages")
    click.echo()

    click.echo(click.style("📚 Installation Options:", fg="yellow", bold=True))
    click.echo("  pip install streamlit-app-generator")
    click.echo("  pip install streamlit-app-generator[postgresql]")
    click.echo("  pip install streamlit-app-generator[mysql]")
    click.echo("  pip install streamlit-app-generator[mongodb]")
    click.echo("  pip install streamlit-app-generator[redis]")
    click.echo("  pip install streamlit-app-generator[oracle]")
    click.echo("  pip install streamlit-app-generator[all-databases]")
    click.echo()

    click.echo(click.style("🎯 Quick Examples:", fg="yellow", bold=True))
    click.echo("  # Interactive wizard (recommended)")
    click.echo("  streamlit-app-generator create my_app -i")
    click.echo()
    click.echo("  # Quick start with defaults")
    click.echo("  streamlit-app-generator create my_app")
    click.echo()
    click.echo("  # Custom configuration")
    click.echo("  streamlit-app-generator create my_app -d postgresql -a modern -t dark")
    click.echo()

    click.echo(click.style("👨‍💻 Author:", fg="yellow", bold=True))
    click.echo("  Leandro Meyer Dal Cortivo")
    click.echo("  GitHub: https://github.com/leandrodalcortivo")
    click.echo("  Email: lmdcorti@gmail.com")
    click.echo()

    click.echo(click.style("🔗 Links:", fg="yellow", bold=True))
    click.echo("  📦 PyPI:   https://pypi.org/project/streamlit-app-generator/")
    click.echo("  📖 GitHub: https://github.com/leandrodalcortivo/streamlit-app-generator")
    click.echo("  🐛 Issues: https://github.com/leandrodalcortivo/streamlit-app-generator/issues")
    click.echo()

    click.echo(click.style("💖 Support the Project:", fg="yellow", bold=True))
    click.echo("  🇧🇷 PIX:    lmdcorti@gmail.com")
    click.echo("  💰 BTC:     bc1qqkhzmz0fmlgt8m0sn2d3hf9qpz56mpsrmkz4k9")
    click.echo("  💰 ETH:     0x4533957C8a21043ce3843bD3ACB2e09ca59541F8")
    click.echo("  ⭐ Star:    https://github.com/leandrodalcortivo/streamlit-app-generator")
    click.echo()

    click.echo(click.style("📄 License:", fg="yellow", bold=True))
    click.echo("  MIT License - Copyright (c) 2024 Leandro Meyer Dal Cortivo")
    click.echo()
    click.echo(click.style("━" * 70, fg="cyan"))
    click.echo()


if __name__ == "__main__":
    main()
