"""Interactive setup wizard for Streamlit App Generator."""
import click
from typing import Dict, Any, Optional


class SetupWizard:
    """Interactive wizard for guiding users through app setup."""

    # Application templates
    TEMPLATES = {
        "basic": {
            "name": "Basic App",
            "emoji": "📱",
            "description": "Simple multi-page app",
            "pages": ["home", "dashboard", "settings"],
            "best_for": "General purpose, learning, prototypes"
        },
        "dashboard": {
            "name": "Dashboard/Analytics",
            "emoji": "📊",
            "description": "Data visualization and analytics dashboard",
            "pages": ["overview", "metrics", "charts", "data", "settings"],
            "best_for": "Business intelligence, data analysis, reporting"
        },
        "crud": {
            "name": "CRUD Application",
            "emoji": "📝",
            "description": "Create, Read, Update, Delete operations",
            "pages": ["list", "create", "edit", "view", "settings"],
            "best_for": "Management systems, admin panels, data entry"
        },
        "ecommerce": {
            "name": "E-commerce",
            "emoji": "🛒",
            "description": "Online store with products and cart",
            "pages": ["catalog", "cart", "checkout", "orders", "profile"],
            "best_for": "Online shops, product catalogs, sales"
        },
        "blog": {
            "name": "Blog/CMS",
            "emoji": "📰",
            "description": "Content management system",
            "pages": ["posts", "create_post", "categories", "comments", "settings"],
            "best_for": "Blogs, news sites, content platforms"
        },
        "custom": {
            "name": "Custom",
            "emoji": "🎨",
            "description": "Define your own pages",
            "pages": None,  # Will be asked
            "best_for": "Specific requirements, unique workflows"
        }
    }

    # Database information with descriptions and use cases
    DATABASES = {
        "all": {
            "name": "All Databases",
            "emoji": "🗄️",
            "description": "Install support for all databases (recommended for learning)",
            "pros": [
                "Try different databases without reinstalling",
                "Switch databases easily",
                "Learn and compare different options",
                "Full flexibility"
            ],
            "cons": [
                "Larger installation size",
                "More dependencies to download",
                "Takes more time to install"
            ],
            "use_cases": [
                "Learning and experimentation",
                "Development environment",
                "Testing different databases",
                "Maximum flexibility"
            ],
            "requires_config": True
        },
        "sqlite": {
            "name": "SQLite",
            "emoji": "📁",
            "description": "Banco de dados em arquivo único (padrão)",
            "pros": [
                "Zero configuração necessária",
                "Perfeito para desenvolvimento e prototipação",
                "Não precisa de servidor",
                "Leve e rápido para apps pequenos"
            ],
            "cons": [
                "Não recomendado para produção com múltiplos usuários",
                "Performance limitada com grandes volumes"
            ],
            "use_cases": [
                "Protótipos e MVPs",
                "Apps pessoais",
                "Desenvolvimento local",
                "Aplicações simples"
            ],
            "requires_config": False
        },
        "postgresql": {
            "name": "PostgreSQL",
            "emoji": "🐘",
            "description": "Banco de dados relacional robusto e confiável",
            "pros": [
                "Excelente para produção",
                "Alta performance e escalabilidade",
                "Suporte a queries complexas",
                "ACID compliant",
                "Muitas features avançadas"
            ],
            "cons": [
                "Requer instalação e configuração de servidor",
                "Mais complexo que SQLite"
            ],
            "use_cases": [
                "Aplicações em produção",
                "Sistemas com múltiplos usuários",
                "Dados estruturados e relacionais",
                "Apps que precisam de confiabilidade"
            ],
            "requires_config": True
        },
        "mysql": {
            "name": "MySQL/MariaDB",
            "emoji": "🐬",
            "description": "Banco de dados relacional popular e amplamente usado",
            "pros": [
                "Muito popular e bem documentado",
                "Grande comunidade",
                "Integração fácil com PHP",
                "Bom para web apps tradicionais"
            ],
            "cons": [
                "Algumas limitações vs PostgreSQL",
                "Requer servidor"
            ],
            "use_cases": [
                "Aplicações web tradicionais",
                "Integração com WordPress/PHP",
                "Ambientes compartilhados",
                "Apps legados"
            ],
            "requires_config": True
        },
        "mongodb": {
            "name": "MongoDB",
            "emoji": "🍃",
            "description": "Banco NoSQL orientado a documentos",
            "pros": [
                "Schema flexível",
                "Excelente para dados não estruturados",
                "Alta escalabilidade horizontal",
                "Rápido desenvolvimento"
            ],
            "cons": [
                "Não ideal para dados muito relacionais",
                "Requer servidor MongoDB"
            ],
            "use_cases": [
                "Dados não estruturados",
                "IoT e logs",
                "Catálogos de produtos",
                "Apps que mudam frequentemente"
            ],
            "requires_config": True
        },
        "redis": {
            "name": "Redis",
            "emoji": "🔴",
            "description": "Banco em memória ultra-rápido (cache e sessões)",
            "pros": [
                "Extremamente rápido",
                "Ideal para cache",
                "Suporte a estruturas de dados avançadas",
                "Pub/Sub e filas"
            ],
            "cons": [
                "Dados em memória (limitado por RAM)",
                "Não é banco primário",
                "Requer servidor Redis"
            ],
            "use_cases": [
                "Cache de alta performance",
                "Sessões de usuário",
                "Rate limiting",
                "Filas de tarefas",
                "Leaderboards e contadores"
            ],
            "requires_config": True
        },
        "oracle": {
            "name": "Oracle Database",
            "emoji": "🏛️",
            "description": "Banco de dados empresarial de alto desempenho",
            "pros": [
                "Máxima confiabilidade",
                "Features empresariais avançadas",
                "Alta disponibilidade",
                "Suporte corporativo"
            ],
            "cons": [
                "Licença paga (exceto XE)",
                "Complexo de configurar",
                "Mais pesado"
            ],
            "use_cases": [
                "Sistemas corporativos grandes",
                "ERP e sistemas legados",
                "Aplicações mission-critical",
                "Ambientes enterprise"
            ],
            "requires_config": True
        }
    }

    AUTH_STYLES = {
        "basic": {
            "name": "Basic",
            "emoji": "🔒",
            "description": "Login simples e funcional",
            "preview": "Interface limpa com campos de usuário e senha",
            "best_for": "Apps corporativos internos, MVPs, protótipos"
        },
        "modern": {
            "name": "Modern",
            "emoji": "✨",
            "description": "Login moderno com design bonito",
            "preview": "Interface moderna com gradientes e animações",
            "best_for": "Apps voltados ao público, SaaS, landing pages"
        },
        "minimal": {
            "name": "Minimal",
            "emoji": "⚪",
            "description": "Login minimalista e clean",
            "preview": "Design minimalista e direto ao ponto",
            "best_for": "Dashboards, ferramentas internas, apps focados"
        }
    }

    THEMES = {
        "light": {
            "name": "Light",
            "emoji": "☀️",
            "description": "Tema claro e profissional",
            "best_for": "Documentação, relatórios, apps corporativos"
        },
        "dark": {
            "name": "Dark",
            "emoji": "🌙",
            "description": "Tema escuro moderno",
            "best_for": "Dashboards, analytics, trabalho noturno"
        },
        "custom": {
            "name": "Custom",
            "emoji": "🎨",
            "description": "Personalize suas próprias cores",
            "best_for": "Branding específico, identidade visual única"
        }
    }

    def __init__(self, language: str = None):
        """Initialize the wizard."""
        self.config: Dict[str, Any] = {}
        self.language = language
        self.i18n = None

    def print_header(self, title: str, emoji: str = "🚀") -> None:
        """Print a styled header."""
        click.echo()
        click.echo("=" * 70)
        click.echo(f"{emoji}  {title}")
        click.echo("=" * 70)
        click.echo()

    def print_section(self, title: str) -> None:
        """Print a section title."""
        click.echo()
        click.echo(click.style(f"📌 {title}", bold=True, fg="cyan"))
        click.echo("-" * 70)

    def choose_language(self) -> str:
        """Interactive language selection."""
        self.print_header("Language Selection / Seleção de Idioma", "🌍")

        click.echo("Please choose your preferred language:")
        click.echo("Por favor, escolha seu idioma preferido:")
        click.echo()
        click.echo("  1. 🇺🇸 English")
        click.echo("  2. 🇧🇷 Português (Brasil)")
        click.echo()

        while True:
            choice = click.prompt("Your choice / Sua escolha", type=str, default="1").strip()

            if choice == "1" or choice.lower() in ["en", "english", "inglês", "ingles"]:
                click.echo()
                click.echo(click.style("✅ Selected: English", fg="green", bold=True))
                return "en"
            elif choice == "2" or choice.lower() in ["pt", "pt-br", "português", "portugues", "portuguese"]:
                click.echo()
                click.echo(click.style("✅ Selecionado: Português (Brasil)", fg="green", bold=True))
                return "pt-BR"
            else:
                click.echo(click.style("❌ Invalid option / Opção inválida. Try again / Tente novamente.", fg="red"))

    def choose_template(self) -> tuple:
        """Interactive template selection."""
        from .i18n import get_i18n

        if not self.i18n:
            self.i18n = get_i18n(self.language)
        t = self.i18n.t

        self.print_header(t("wizard.template.title"), "📱")

        click.echo(t("wizard.template.question"))
        click.echo()

        template_list = list(self.TEMPLATES.keys())
        for idx, template_key in enumerate(template_list, 1):
            template = self.TEMPLATES[template_key]
            click.echo(f"  {idx}. {template['emoji']} {template['name']:20} - {template['description']}")
            click.echo(f"      {click.style(f'{t("wizard.auth.best_for")}: {template["best_for"]}', fg='blue')}")
            if template['pages']:
                pages_label = t("wizard.summary.pages") if self.language == "pt-BR" else "Pages"
                click.echo(f"      {click.style(f'{pages_label}: {", ".join(template["pages"])}', dim=True)}")
            click.echo()

        while True:
            choice = click.prompt(t("wizard.database.prompt"), type=str, default="1").strip()

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(template_list):
                    selected_key = template_list[idx]
                    selected = self.TEMPLATES[selected_key]
                    click.echo()
                    selected_msg = t("wizard.template.selected", emoji=selected['emoji'], name=selected['name'])
                    click.echo(click.style(f"✅ {selected_msg}", fg="green", bold=True))

                    # Return template key and pages
                    return selected_key, selected['pages']
            except ValueError:
                if choice in template_list:
                    selected = self.TEMPLATES[choice]
                    click.echo()
                    selected_msg = t("wizard.template.selected", emoji=selected['emoji'], name=selected['name'])
                    click.echo(click.style(f"✅ {selected_msg}", fg="green", bold=True))
                    return choice, selected['pages']

            click.echo(click.style(f"❌ {t('wizard.database.invalid')}", fg="red"))

    def print_database_info(self, db_key: str) -> None:
        """Print detailed information about a database."""
        from .i18n import get_i18n

        if not self.i18n:
            self.i18n = get_i18n(self.language)
        t = self.i18n.t

        db = self.DATABASES[db_key]

        click.echo()
        click.echo(click.style(f"{db['emoji']} {db['name']}", bold=True, fg="green"))

        # Use translated description if available
        db_info = t(f"databases.{db_key}")
        if not isinstance(db_info, dict):
            db_info = {}

        if db_info and 'description' in db_info:
            click.echo(f"   {db_info['description']}")
        else:
            click.echo(f"   {db['description']}")
        click.echo()

        click.echo(click.style(f"   ✅ {t('wizard.database.advantages')}:", fg="green"))
        pros_list = db_info.get('pros', db['pros']) if db_info else db['pros']
        for pro in pros_list:
            click.echo(f"      • {pro}")

        if db['cons']:
            click.echo()
            click.echo(click.style(f"   ⚠️  {t('wizard.database.considerations')}:", fg="yellow"))
            cons_list = db_info.get('cons', db['cons']) if db_info else db['cons']
            for con in cons_list:
                click.echo(f"      • {con}")

        click.echo()
        click.echo(click.style(f"   💡 {t('wizard.database.ideal_for')}:", fg="blue"))
        use_cases_list = db_info.get('use_cases', db['use_cases']) if db_info else db['use_cases']
        for use_case in use_cases_list:
            click.echo(f"      • {use_case}")

        if db['requires_config']:
            click.echo()
            click.echo(click.style(f"   ⚙️  {t('wizard.database.requires_config')}", fg="yellow"))

        click.echo()

    def choose_database(self) -> str:
        """Interactive database selection with detailed info."""
        from .i18n import get_i18n

        if not self.i18n:
            self.i18n = get_i18n(self.language)
        t = self.i18n.t

        self.print_header(t("wizard.database.title"), "🗄️")

        click.echo(t("wizard.database.question"))
        click.echo()
        click.echo(t("wizard.database.type_info"))
        click.echo()

        # List databases
        db_list = list(self.DATABASES.keys())
        for idx, db_key in enumerate(db_list, 1):
            db = self.DATABASES[db_key]
            # Try to get translated description
            db_info = t(f"databases.{db_key}")
            if not isinstance(db_info, dict):
                db_info = {}
            description = db_info.get('description', db['description']) if db_info else db['description']
            click.echo(f"  {idx}. {db['emoji']} {db['name']:17} - {description}")

        click.echo()
        click.echo(f"  📖 {t('wizard.database.info_command')}")
        click.echo(f"  ⬅️  {t('wizard.database.back_command')}")
        click.echo()

        while True:
            choice = click.prompt(t("wizard.database.prompt"), type=str, default="1").lower().strip()

            # Handle 'info' command
            if choice.startswith("info"):
                try:
                    info_idx = int(choice.split()[1]) - 1
                    if 0 <= info_idx < len(db_list):
                        self.print_database_info(db_list[info_idx])
                        continue
                except (IndexError, ValueError):
                    pass
                click.echo(click.style(f"❌ {t('wizard.database.invalid')}", fg="red"))
                continue

            # Handle number choice
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(db_list):
                    selected = db_list[idx]
                    click.echo()
                    selected_msg = t("wizard.database.selected", emoji=self.DATABASES[selected]['emoji'], name=self.DATABASES[selected]['name'])
                    click.echo(click.style(f"✅ {selected_msg}", fg="green", bold=True))
                    return selected
            except ValueError:
                pass

            # Handle name choice
            if choice in db_list:
                click.echo()
                selected_msg = t("wizard.database.selected", emoji=self.DATABASES[choice]['emoji'], name=self.DATABASES[choice]['name'])
                click.echo(click.style(f"✅ {selected_msg}", fg="green", bold=True))
                return choice

            click.echo(click.style(f"❌ {t('wizard.database.invalid')}", fg="red"))

    def choose_auth_style(self) -> str:
        """Interactive auth style selection."""
        from .i18n import get_i18n

        if not self.i18n:
            self.i18n = get_i18n(self.language)
        t = self.i18n.t

        self.print_header(t("wizard.auth.title"), "🔐")

        click.echo(t("wizard.auth.question"))
        click.echo()

        auth_list = list(self.AUTH_STYLES.keys())
        for idx, auth_key in enumerate(auth_list, 1):
            auth = self.AUTH_STYLES[auth_key]
            # Try to get translated info
            auth_info = t(f"auth_styles.{auth_key}")
            if not isinstance(auth_info, dict):
                auth_info = {}
            description = auth_info.get('description', auth['description']) if auth_info else auth['description']
            preview = auth_info.get('preview', auth['preview']) if auth_info else auth['preview']
            best_for = auth_info.get('best_for', auth['best_for']) if auth_info else auth['best_for']

            click.echo(f"  {idx}. {auth['emoji']} {auth['name']:10} - {description}")
            click.echo(f"      {click.style(f'{t("wizard.auth.preview")}: {preview}', dim=True)}")
            click.echo(f"      {click.style(f'{t("wizard.auth.best_for")}: {best_for}', fg='blue')}")
            click.echo()

        while True:
            choice = click.prompt(t("wizard.database.prompt"), type=str, default="2").strip()

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(auth_list):
                    selected = auth_list[idx]
                    click.echo()
                    selected_msg = t("wizard.auth.selected", emoji=self.AUTH_STYLES[selected]['emoji'], name=self.AUTH_STYLES[selected]['name'])
                    click.echo(click.style(f"✅ {selected_msg}", fg="green", bold=True))
                    return selected
            except ValueError:
                if choice in auth_list:
                    click.echo()
                    selected_msg = t("wizard.auth.selected", emoji=self.AUTH_STYLES[choice]['emoji'], name=self.AUTH_STYLES[choice]['name'])
                    click.echo(click.style(f"✅ {selected_msg}", fg="green", bold=True))
                    return choice

            click.echo(click.style(f"❌ {t('wizard.database.invalid')}", fg="red"))

    def choose_theme(self) -> str:
        """Interactive theme selection."""
        from .i18n import get_i18n

        if not self.i18n:
            self.i18n = get_i18n(self.language)
        t = self.i18n.t

        self.print_header(t("wizard.theme.title"), "🎨")

        click.echo(t("wizard.theme.question"))
        click.echo()

        theme_list = list(self.THEMES.keys())
        for idx, theme_key in enumerate(theme_list, 1):
            theme = self.THEMES[theme_key]
            # Try to get translated info
            theme_info = t(f"themes.{theme_key}")
            if not isinstance(theme_info, dict):
                theme_info = {}
            description = theme_info.get('description', theme['description']) if theme_info else theme['description']
            best_for = theme_info.get('best_for', theme['best_for']) if theme_info else theme['best_for']

            click.echo(f"  {idx}. {theme['emoji']} {theme['name']:10} - {description}")
            click.echo(f"      {click.style(f'{t("wizard.auth.best_for")}: {best_for}', fg='blue')}")
            click.echo()

        while True:
            choice = click.prompt(t("wizard.database.prompt"), type=str, default="1").strip()

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(theme_list):
                    selected = theme_list[idx]
                    click.echo()
                    selected_msg = t("wizard.theme.selected", emoji=self.THEMES[selected]['emoji'], name=self.THEMES[selected]['name'])
                    click.echo(click.style(f"✅ {selected_msg}", fg="green", bold=True))
                    return selected
            except ValueError:
                if choice in theme_list:
                    click.echo()
                    selected_msg = t("wizard.theme.selected", emoji=self.THEMES[choice]['emoji'], name=self.THEMES[choice]['name'])
                    click.echo(click.style(f"✅ {selected_msg}", fg="green", bold=True))
                    return choice

            click.echo(click.style(f"❌ {t('wizard.database.invalid')}", fg="red"))

    def choose_pages(self) -> list:
        """Interactive page selection."""
        from .i18n import get_i18n

        if not self.i18n:
            self.i18n = get_i18n(self.language)
        t = self.i18n.t

        self.print_header(t("wizard.pages.title"), "📄")

        click.echo(t("wizard.pages.question"))
        click.echo()
        click.echo(t("wizard.pages.instructions"))
        click.echo()
        click.echo(click.style(f"💡 {t('wizard.pages.tip')}", fg="blue"))
        click.echo()
        click.echo(t("wizard.pages.examples"))
        click.echo(f"  • {t('wizard.pages.ex1')}")
        click.echo(f"  • {t('wizard.pages.ex2')}")
        click.echo(f"  • {t('wizard.pages.ex3')}")
        click.echo()

        default_pages = "home,dashboard,settings"
        pages_input = click.prompt(t("wizard.pages.prompt"), default=default_pages)

        pages = [p.strip() for p in pages_input.split(",") if p.strip()]

        click.echo()
        selected_msg = t("wizard.pages.selected", pages=', '.join(pages))
        click.echo(click.style(f"✅ {selected_msg}", fg="green", bold=True))

        return pages

    def run(self, app_name: str) -> Dict[str, Any]:
        """Run the complete interactive wizard."""
        click.clear()

        # Step 1: Choose language if not set
        if not self.language:
            self.language = self.choose_language()

        # Initialize i18n
        from .i18n import get_i18n
        self.i18n = get_i18n(self.language)
        t = self.i18n.t

        # Welcome (translated)
        if self.language == "pt-BR":
            self.print_header("Bem-vindo ao Streamlit App Generator! 🎉", "🚀")
            click.echo(f"Vamos criar seu app: {click.style(app_name, bold=True, fg='cyan')}")
            click.echo()
            click.echo("Este wizard vai te guiar através de algumas escolhas.")
            click.echo("Você poderá mudar tudo depois!")
            click.echo()
            if not click.confirm("Pronto para começar?", default=True):
                click.echo("Ok, até logo! 👋")
                return None
        else:
            self.print_header("Welcome to Streamlit App Generator! 🎉", "🚀")
            click.echo(f"Let's create your app: {click.style(app_name, bold=True, fg='cyan')}")
            click.echo()
            click.echo("This wizard will guide you through some choices.")
            click.echo("You can change everything later!")
            click.echo()
            if not click.confirm("Ready to start?", default=True):
                click.echo("Ok, see you later! 👋")
                return None

        # Step 2: Choose template
        template_key, template_pages = self.choose_template()

        # Step 3: Collect other choices
        database = self.choose_database()
        auth_style = self.choose_auth_style()
        theme = self.choose_theme()

        # Step 4: Pages (from template or custom)
        if template_pages is None:  # Custom template
            pages = self.choose_pages()
        else:
            pages = template_pages

        config = {
            "name": app_name,
            "template": template_key,
            "database": database,
            "auth_style": auth_style,
            "theme": theme,
            "pages": pages
        }

        # Summary
        self.print_header(t("wizard.summary.title"), "📋")

        template_name = self.TEMPLATES[template_key]['name']
        click.echo(f"  📱 {t('wizard.summary.app_name')}     {click.style(config['name'], bold=True)}")
        click.echo(f"  🎯 Template:            {self.TEMPLATES[template_key]['emoji']} {template_name}")
        click.echo(f"  🗄️  {t('wizard.summary.database')}     {self.DATABASES[config['database']]['emoji']} {self.DATABASES[config['database']]['name']}")
        click.echo(f"  🔐 {t('wizard.summary.auth')}     {self.AUTH_STYLES[config['auth_style']]['emoji']} {self.AUTH_STYLES[config['auth_style']]['name']}")
        click.echo(f"  🎨 {t('wizard.summary.theme')}          {self.THEMES[config['theme']]['emoji']} {self.THEMES[config['theme']]['name']}")
        click.echo(f"  📄 {t('wizard.summary.pages')}        {', '.join(config['pages'])}")
        click.echo()

        # Confirm
        if not click.confirm(t("wizard.summary.confirm"), default=True):
            click.echo(t("wizard.summary.cancelled") + " 👋")
            return None

        return config

    def show_next_steps(self, app_name: str, database: str) -> None:
        """Show next steps after app creation."""
        from .i18n import get_i18n

        if not self.i18n:
            self.i18n = get_i18n(self.language)
        t = self.i18n.t

        self.print_header(t("wizard.completion.title"), "✅")

        click.echo(t("wizard.completion.next_steps"))
        click.echo()
        click.echo(f"  1️⃣  {t('wizard.completion.step1')}")
        click.echo(f"      cd {app_name}")
        click.echo()
        click.echo(f"  2️⃣  {t('wizard.completion.step2')}")
        click.echo(f"      pip install -r requirements.txt")
        click.echo()

        # Database-specific instructions
        if database in self.DATABASES and self.DATABASES[database]["requires_config"]:
            click.echo(click.style(f"  ⚙️  {t('wizard.completion.config_db')}", fg="yellow", bold=True))
            click.echo(f"      {t('wizard.completion.config_edit')}")
            click.echo(f"      {t('wizard.completion.config_see')}")
            click.echo()

        click.echo(f"  3️⃣  {t('wizard.completion.step3')}")
        click.echo(f"      streamlit run app.py")
        click.echo()
        click.echo(f"  🌐 {t('wizard.completion.access')} http://localhost:8501")
        click.echo()
        click.echo(f"  👤 {t('wizard.completion.login')}")
        click.echo(f"      {t('wizard.completion.username')}")
        click.echo(f"      {t('wizard.completion.password')}")
        click.echo()
        click.echo(click.style(f"📚 {t('wizard.completion.docs')}", fg="blue", bold=True))
        click.echo(f"    • {t('wizard.completion.docs_complete')}")
        click.echo(f"    • {t('wizard.completion.docs_setup')}")
        click.echo(f"    • {t('wizard.completion.docs_env')}")
        click.echo()
        click.echo(click.style(f"💡 {t('wizard.completion.tip')}", fg="green") + f" {t('wizard.completion.help_command')}")
        click.echo()
        click.echo("=" * 70)
        click.echo()
