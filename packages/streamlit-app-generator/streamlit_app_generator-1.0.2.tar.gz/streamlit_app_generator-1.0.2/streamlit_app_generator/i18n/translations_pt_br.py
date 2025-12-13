"""Traduções em Português (Brasil)."""

TRANSLATIONS = {
    # Mensagens do CLI
    "cli": {
        "creating": "Criando aplicação Streamlit: {name}",
        "database": "Banco de Dados",
        "auth": "Autenticação",
        "theme": "Tema",
        "pages": "Páginas",
        "generating": "Gerando estrutura do app...",
        "success": "Criado com sucesso: {name}!",
        "next_steps": "Próximos passos:",
        "step_cd": "cd {name}",
        "step_install": "pip install -r requirements.txt",
        "step_config": "Configure .streamlit/secrets.toml (se necessário)",
        "step_run": "streamlit run app.py",
        "see_docs": "Veja SETUP_GUIDE.md para guia completo",
    },

    # Wizard
    "wizard": {
        "welcome": {
            "title": "Bem-vindo ao Streamlit App Generator!",
            "creating": "Vamos criar seu app: {name}",
            "description": "Este wizard vai te guiar através de algumas escolhas.",
            "can_change": "Você poderá mudar tudo depois!",
            "ready": "Pronto para começar?",
            "goodbye": "Ok, até logo!",
        },

        "database": {
            "title": "Escolha do Banco de Dados",
            "question": "Qual banco de dados você deseja usar?",
            "type_info": "Digite o número ou nome para ver mais informações:",
            "info_command": "Digite 'info <numero>' para ver detalhes (ex: info 1)",
            "back_command": "Digite 'back' para voltar",
            "prompt": "Sua escolha",
            "selected": "Selecionado: {emoji} {name}",
            "invalid": "Opção inválida. Tente novamente.",
            "advantages": "Vantagens:",
            "considerations": "Considerações:",
            "ideal_for": "Ideal para:",
            "requires_config": "Requer configuração após criar o app",
        },

        "auth": {
            "title": "Estilo de Autenticação",
            "question": "Escolha o estilo de login:",
            "preview": "Preview",
            "best_for": "Ideal para",
            "selected": "Selecionado: {emoji} {name}",
        },

        "theme": {
            "title": "Tema Visual",
            "question": "Escolha o tema do seu app:",
            "selected": "Selecionado: {emoji} {name}",
        },

        "template": {
            "title": "Template de Aplicação",
            "question": "Escolha o tipo de aplicação:",
            "selected": "Selecionado: {emoji} {name}",
        },

        "pages": {
            "title": "Páginas do App",
            "question": "Quais páginas você quer criar?",
            "instructions": "Digite os nomes separados por vírgula (ex: home,dashboard,relatorios)",
            "tip": "Dica: Você pode adicionar mais páginas depois!",
            "examples": "Exemplos populares:",
            "ex1": "home,dashboard,settings (padrão)",
            "ex2": "vendas,produtos,clientes,relatorios",
            "ex3": "usuarios,perfil,configuracoes",
            "prompt": "Páginas",
            "selected": "Páginas selecionadas: {pages}",
        },

        "summary": {
            "title": "Resumo da Configuração",
            "app_name": "Nome do App:",
            "database": "Banco de Dados:",
            "auth": "Autenticação:",
            "theme": "Tema:",
            "pages": "Páginas:",
            "confirm": "Confirmar e criar o app?",
            "cancelled": "Cancelado. Você pode executar novamente quando quiser!",
        },

        "completion": {
            "title": "App Criado com Sucesso!",
            "next_steps": "Próximos passos:",
            "step1": "Entre na pasta do app:",
            "step2": "Instale as dependências:",
            "step3": "Execute o app:",
            "access": "Acesse:",
            "login": "Login padrão:",
            "username": "Usuário: admin",
            "password": "Senha: admin123",
            "docs": "Documentação e exemplos:",
            "docs_complete": "README.md - Documentação completa",
            "docs_setup": "SETUP_GUIDE.md - Guia de configuração",
            "docs_env": ".env.example - Exemplos de configuração",
            "tip": "Dica:",
            "help_command": "Use 'streamlit-app-generator --help' para mais comandos",
            "config_db": "Configure o banco de dados:",
            "config_edit": "Edite o arquivo: .streamlit/secrets.toml",
            "config_see": "Veja o exemplo em: secrets.toml.example",
        }
    },

    # Descrições dos bancos de dados
    "databases": {
        "all": {
            "name": "Todos os Bancos",
            "emoji": "🗄️",
            "description": "Instalar suporte para todos os bancos (recomendado para aprendizado)",
            "pros": [
                "Experimente diferentes bancos sem reinstalar",
                "Troque de banco facilmente",
                "Aprenda e compare diferentes opções",
                "Máxima flexibilidade"
            ],
            "cons": [
                "Tamanho de instalação maior",
                "Mais dependências para baixar",
                "Leva mais tempo para instalar"
            ],
            "use_cases": [
                "Aprendizado e experimentação",
                "Ambiente de desenvolvimento",
                "Testar diferentes bancos",
                "Máxima flexibilidade"
            ]
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
            ]
        },
        "postgresql": {
            "name": "PostgreSQL",
            "emoji": "🐘",
            "description": "Banco de dados relacional robusto e confiável",
            "pros": [
                "Excelente para produção",
                "Alta performance e escalabilidade",
                "Suporte a queries complexas",
                "ACID completo",
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
            ]
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
            ]
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
            ]
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
            ]
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
            ]
        }
    },

    # Estilos de autenticação
    "auth_styles": {
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
    },

    # Temas
    "themes": {
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
}
