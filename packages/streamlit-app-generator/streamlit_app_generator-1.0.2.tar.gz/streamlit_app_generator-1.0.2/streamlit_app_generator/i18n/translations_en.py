"""English translations."""

TRANSLATIONS = {
    # CLI Messages
    "cli": {
        "creating": "Creating Streamlit application: {name}",
        "database": "Database",
        "auth": "Auth",
        "theme": "Theme",
        "pages": "Pages",
        "generating": "Generating app structure...",
        "success": "Successfully created {name}!",
        "next_steps": "Next steps:",
        "step_cd": "cd {name}",
        "step_install": "pip install -r requirements.txt",
        "step_config": "Configure .streamlit/secrets.toml (if needed)",
        "step_run": "streamlit run app.py",
        "see_docs": "See SETUP_GUIDE.md for complete guide",
    },

    # Wizard
    "wizard": {
        "welcome": {
            "title": "Welcome to Streamlit App Generator!",
            "creating": "Let's create your app: {name}",
            "description": "This wizard will guide you through some choices.",
            "can_change": "You can change everything later!",
            "ready": "Ready to start?",
            "goodbye": "Ok, see you later!",
        },

        "database": {
            "title": "Database Selection",
            "question": "Which database would you like to use?",
            "type_info": "Type a number or name to see more information:",
            "info_command": "Type 'info <number>' to see details (e.g., info 1)",
            "back_command": "Type 'back' to go back",
            "prompt": "Your choice",
            "selected": "Selected: {emoji} {name}",
            "invalid": "Invalid option. Try again.",
            "advantages": "Advantages:",
            "considerations": "Considerations:",
            "ideal_for": "Ideal for:",
            "requires_config": "Requires configuration after creating the app",
        },

        "auth": {
            "title": "Authentication Style",
            "question": "Choose the login style:",
            "preview": "Preview",
            "best_for": "Best for",
            "selected": "Selected: {emoji} {name}",
        },

        "theme": {
            "title": "Visual Theme",
            "question": "Choose your app's theme:",
            "selected": "Selected: {emoji} {name}",
        },

        "template": {
            "title": "Application Template",
            "question": "Choose the application type:",
            "selected": "Selected: {emoji} {name}",
        },

        "pages": {
            "title": "App Pages",
            "question": "Which pages do you want to create?",
            "instructions": "Type the names separated by comma (e.g., home,dashboard,reports)",
            "tip": "Tip: You can add more pages later!",
            "examples": "Popular examples:",
            "ex1": "home,dashboard,settings (default)",
            "ex2": "sales,products,customers,reports",
            "ex3": "users,profile,settings",
            "prompt": "Pages",
            "selected": "Selected pages: {pages}",
        },

        "summary": {
            "title": "Configuration Summary",
            "app_name": "App Name:",
            "database": "Database:",
            "auth": "Authentication:",
            "theme": "Theme:",
            "pages": "Pages:",
            "confirm": "Confirm and create the app?",
            "cancelled": "Cancelled. You can run again whenever you want!",
        },

        "completion": {
            "title": "App Created Successfully!",
            "next_steps": "Next steps:",
            "step1": "Enter the app folder:",
            "step2": "Install dependencies:",
            "step3": "Run the app:",
            "access": "Access:",
            "login": "Default login:",
            "username": "Username: admin",
            "password": "Password: admin123",
            "docs": "Documentation and examples:",
            "docs_complete": "README.md - Complete documentation",
            "docs_setup": "SETUP_GUIDE.md - Setup guide",
            "docs_env": ".env.example - Configuration examples",
            "tip": "Tip:",
            "help_command": "Use 'streamlit-app-generator --help' for more commands",
            "config_db": "Configure the database:",
            "config_edit": "Edit the file: .streamlit/secrets.toml",
            "config_see": "See the example at: secrets.toml.example",
        }
    },

    # Database descriptions
    "databases": {
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
            ]
        },
        "sqlite": {
            "name": "SQLite",
            "emoji": "📁",
            "description": "Single-file database (default)",
            "pros": [
                "Zero configuration required",
                "Perfect for development and prototyping",
                "No server needed",
                "Fast and lightweight for small apps"
            ],
            "cons": [
                "Not recommended for production with multiple users",
                "Limited performance with large volumes"
            ],
            "use_cases": [
                "Prototypes and MVPs",
                "Personal apps",
                "Local development",
                "Simple applications"
            ]
        },
        "postgresql": {
            "name": "PostgreSQL",
            "emoji": "🐘",
            "description": "Robust and reliable relational database",
            "pros": [
                "Excellent for production",
                "High performance and scalability",
                "Support for complex queries",
                "ACID compliant",
                "Many advanced features"
            ],
            "cons": [
                "Requires server installation and configuration",
                "More complex than SQLite"
            ],
            "use_cases": [
                "Production applications",
                "Multi-user systems",
                "Structured and relational data",
                "Apps requiring reliability"
            ]
        },
        "mysql": {
            "name": "MySQL/MariaDB",
            "emoji": "🐬",
            "description": "Popular and widely-used relational database",
            "pros": [
                "Very popular and well-documented",
                "Large community",
                "Easy integration with PHP",
                "Good for traditional web apps"
            ],
            "cons": [
                "Some limitations vs PostgreSQL",
                "Requires server"
            ],
            "use_cases": [
                "Traditional web applications",
                "WordPress/PHP integration",
                "Shared hosting environments",
                "Legacy apps"
            ]
        },
        "mongodb": {
            "name": "MongoDB",
            "emoji": "🍃",
            "description": "Document-oriented NoSQL database",
            "pros": [
                "Flexible schema",
                "Excellent for unstructured data",
                "High horizontal scalability",
                "Fast development"
            ],
            "cons": [
                "Not ideal for highly relational data",
                "Requires MongoDB server"
            ],
            "use_cases": [
                "Unstructured data",
                "IoT and logs",
                "Product catalogs",
                "Frequently changing apps"
            ]
        },
        "redis": {
            "name": "Redis",
            "emoji": "🔴",
            "description": "Ultra-fast in-memory database (cache and sessions)",
            "pros": [
                "Extremely fast",
                "Ideal for caching",
                "Support for advanced data structures",
                "Pub/Sub and queues"
            ],
            "cons": [
                "In-memory data (limited by RAM)",
                "Not a primary database",
                "Requires Redis server"
            ],
            "use_cases": [
                "High-performance caching",
                "User sessions",
                "Rate limiting",
                "Task queues",
                "Leaderboards and counters"
            ]
        },
        "oracle": {
            "name": "Oracle Database",
            "emoji": "🏛️",
            "description": "High-performance enterprise database",
            "pros": [
                "Maximum reliability",
                "Advanced enterprise features",
                "High availability",
                "Corporate support"
            ],
            "cons": [
                "Paid license (except XE)",
                "Complex to configure",
                "Heavier"
            ],
            "use_cases": [
                "Large corporate systems",
                "ERP and legacy systems",
                "Mission-critical applications",
                "Enterprise environments"
            ]
        }
    },

    # Auth styles
    "auth_styles": {
        "basic": {
            "name": "Basic",
            "emoji": "🔒",
            "description": "Simple and functional login",
            "preview": "Clean interface with username and password fields",
            "best_for": "Corporate internal apps, MVPs, prototypes"
        },
        "modern": {
            "name": "Modern",
            "emoji": "✨",
            "description": "Modern login with beautiful design",
            "preview": "Modern interface with gradients and animations",
            "best_for": "Public-facing apps, SaaS, landing pages"
        },
        "minimal": {
            "name": "Minimal",
            "emoji": "⚪",
            "description": "Minimalist and clean login",
            "preview": "Minimalist and straight-to-the-point design",
            "best_for": "Dashboards, internal tools, focused apps"
        }
    },

    # Themes
    "themes": {
        "light": {
            "name": "Light",
            "emoji": "☀️",
            "description": "Light and professional theme",
            "best_for": "Documentation, reports, corporate apps"
        },
        "dark": {
            "name": "Dark",
            "emoji": "🌙",
            "description": "Modern dark theme",
            "best_for": "Dashboards, analytics, night work"
        },
        "custom": {
            "name": "Custom",
            "emoji": "🎨",
            "description": "Customize your own colors",
            "best_for": "Specific branding, unique visual identity"
        }
    }
}
