"""Analyze command - analyze project and recommend agents/MCP."""

from pathlib import Path

import typer
from rich.console import Console

console = Console()


def analyze(
    path: Path | None = typer.Argument(None, help="Chemin du projet (défaut: .)"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Afficher recommandations sans installer"
    ),
    auto_install: bool = typer.Option(False, "--auto-install", help="Installer sans confirmation"),
    agents_only: bool = typer.Option(False, "--agents", help="Recommander agents uniquement"),
    mcp_only: bool = typer.Option(False, "--mcp", help="Recommander MCP uniquement"),
) -> None:
    """Analyser un projet et recommander les agents/MCP adaptés."""
    project_path = (path or Path.cwd()).resolve()

    if not project_path.exists():
        console.print(f"[red]Erreur: Le chemin {project_path} n'existe pas[/red]")
        raise typer.Exit(1)

    if not project_path.is_dir():
        console.print(f"[red]Erreur: {project_path} n'est pas un répertoire[/red]")
        raise typer.Exit(1)

    console.print(f"\n[bold]Analyse du projet: {project_path}[/bold]\n")

    # Scan project structure
    console.print("[dim]Scan de la structure du projet...[/dim]")
    detected = _quick_detect(project_path)

    console.print("\n[bold]Technologies détectées:[/bold]")
    if detected["languages"]:
        console.print(f"  Langages: {', '.join(detected['languages'])}")
    if detected["frameworks"]:
        console.print(f"  Frameworks: {', '.join(detected['frameworks'])}")
    if detected["tools"]:
        console.print(f"  Outils: {', '.join(detected['tools'])}")
    if detected["files"]:
        console.print(f"  Fichiers clés: {', '.join(detected['files'])}")

    # Get recommendations
    from claude_manager.library.loader import LibraryLoader

    loader = LibraryLoader()

    if not mcp_only:
        console.print("\n[bold]Agents recommandés:[/bold]")
        recommended_agents = _get_recommended_agents(loader, detected)
        if recommended_agents:
            for agent in recommended_agents:
                console.print(
                    f"  [green]•[/green] {agent['name']} - {agent.get('description', '')}"
                )
        else:
            console.print("  [dim]Aucun agent spécifique recommandé[/dim]")

    if not agents_only:
        console.print("\n[bold]Serveurs MCP recommandés:[/bold]")
        recommended_mcp = _get_recommended_mcp(loader, detected)
        if recommended_mcp:
            for server in recommended_mcp:
                console.print(
                    f"  [green]•[/green] {server['name']} - {server.get('description', '')}"
                )
        else:
            console.print("  [dim]Aucun serveur MCP spécifique recommandé[/dim]")

    if dry_run:
        console.print("\n[dim]--dry-run: aucune modification effectuée[/dim]")
        return

    # Install if confirmed
    if auto_install:
        console.print("\n[yellow]Installation automatique en cours d'implémentation...[/yellow]")
    else:
        if typer.confirm("\nInstaller les agents et MCP recommandés ?"):
            console.print("\n[yellow]Installation en cours d'implémentation...[/yellow]")
        else:
            console.print("[dim]Installation annulée[/dim]")


def _quick_detect(project_path: Path) -> dict:
    """Quick detection of project technologies without using strands-agents."""
    detected = {
        "languages": [],
        "frameworks": [],
        "tools": [],
        "files": [],  # Track which marker files were found
    }

    # File markers - maps filename to what it indicates
    markers = {
        "package.json": {"lang": "javascript/typescript", "file": "package.json"},
        "pom.xml": {"lang": "java", "framework": "spring", "file": "pom.xml"},
        "build.gradle": {"lang": "java/kotlin", "framework": "spring", "file": "build.gradle"},
        "build.gradle.kts": {"lang": "kotlin", "framework": "spring", "file": "build.gradle.kts"},
        "go.mod": {"lang": "go", "file": "go.mod"},
        "Cargo.toml": {"lang": "rust", "file": "Cargo.toml"},
        "pyproject.toml": {"lang": "python", "file": "pyproject.toml"},
        "requirements.txt": {"lang": "python", "file": "requirements.txt"},
        "setup.py": {"lang": "python", "file": "setup.py"},
        "Dockerfile": {"tool": "docker", "file": "Dockerfile"},
        "docker-compose.yml": {"tool": "docker-compose", "file": "docker-compose.yml"},
        "docker-compose.yaml": {"tool": "docker-compose", "file": "docker-compose.yaml"},
        ".gitlab-ci.yml": {"tool": "gitlab-ci", "file": ".gitlab-ci.yml"},
        ".github": {"tool": "github-actions", "file": ".github"},
        "Makefile": {"tool": "make", "file": "Makefile"},
        "vite.config.ts": {"framework": "vite", "file": "vite.config.ts"},
        "vite.config.js": {"framework": "vite", "file": "vite.config.js"},
        "next.config.js": {"framework": "nextjs", "file": "next.config.js"},
        "next.config.mjs": {"framework": "nextjs", "file": "next.config.mjs"},
        "nuxt.config.ts": {"framework": "nuxt", "file": "nuxt.config.ts"},
        "angular.json": {"framework": "angular", "file": "angular.json"},
        "svelte.config.js": {"framework": "svelte", "file": "svelte.config.js"},
    }

    # Backend markers that should be searched in subdirectories
    # (e.g., src-tauri/Cargo.toml, backend/go.mod, api/pom.xml)
    backend_markers = {"Cargo.toml", "go.mod", "pom.xml", "build.gradle", "build.gradle.kts"}

    def _apply_marker(name: str, subdir: str = None):
        """Apply marker detection, optionally from a subdirectory."""
        if name in markers:
            info = markers[name]
            file_display = f"{subdir}/{info['file']}" if subdir else info["file"]
            if "lang" in info and info["lang"] not in detected["languages"]:
                detected["languages"].append(info["lang"])
            if "framework" in info and info["framework"] not in detected["frameworks"]:
                detected["frameworks"].append(info["framework"])
            if "tool" in info and info["tool"] not in detected["tools"]:
                detected["tools"].append(info["tool"])
            if file_display not in detected["files"]:
                detected["files"].append(file_display)

    # Scan root level
    for item in project_path.iterdir():
        name = item.name
        _apply_marker(name)

        # Scan subdirectories for backend markers
        if (
            item.is_dir()
            and not name.startswith(".")
            and name not in ("node_modules", "vendor", "target", "dist", "build")
        ):
            for subitem in item.iterdir():
                if subitem.name in backend_markers:
                    _apply_marker(subitem.name, name)

    # Check for specific framework in package.json
    package_json = project_path / "package.json"
    if package_json.exists():
        import json

        try:
            data = json.loads(package_json.read_text())
            deps = list(data.get("dependencies", {}).keys()) + list(
                data.get("devDependencies", {}).keys()
            )
            if "vue" in deps:
                if "vue" not in detected["frameworks"]:
                    detected["frameworks"].append("vue")
            if "react" in deps:
                if "react" not in detected["frameworks"]:
                    detected["frameworks"].append("react")
            if "svelte" in deps:
                if "svelte" not in detected["frameworks"]:
                    detected["frameworks"].append("svelte")
            if "@sveltejs/kit" in deps:
                if "sveltekit" not in detected["frameworks"]:
                    detected["frameworks"].append("sveltekit")
        except (json.JSONDecodeError, OSError):
            pass

    # Check for terraform files
    if any(f.suffix == ".tf" for f in project_path.glob("*.tf")):
        if "terraform" not in detected["tools"]:
            detected["tools"].append("terraform")
        if "*.tf" not in detected["files"]:
            detected["files"].append("*.tf")

    # Check for SQL files
    if any(f.suffix == ".sql" for f in project_path.glob("**/*.sql")):
        if "sql" not in detected["tools"]:
            detected["tools"].append("sql")
        if "*.sql" not in detected["files"]:
            detected["files"].append("*.sql")

    # Check git remote for gitlab/github
    git_config = project_path / ".git" / "config"
    if git_config.exists():
        try:
            content = git_config.read_text().lower()
            if "gitlab" in content:
                if "gitlab" not in detected["tools"]:
                    detected["tools"].append("gitlab")
            if "github" in content:
                if "github" not in detected["tools"]:
                    detected["tools"].append("github")
        except OSError:
            pass

    return detected


def _get_recommended_agents(loader, detected: dict) -> list:
    """Get recommended agents based on detected technologies."""
    recommended = []

    # Build a set of all detected items for matching
    all_detected = set()
    for lang in detected["languages"]:
        all_detected.add(lang.lower())
        # Add individual parts for composite languages
        for part in lang.split("/"):
            all_detected.add(part.lower())
    for fw in detected["frameworks"]:
        all_detected.add(fw.lower())
    for tool in detected["tools"]:
        all_detected.add(tool.lower())
    for f in detected["files"]:
        all_detected.add(f.lower())

    # Get agents index
    index = loader.get_agents_index()

    # Match agents by tags
    project = index.get("project", {})
    categories = project.get("categories", {})

    for category, agents in categories.items():
        for agent in agents:
            tags = [t.lower() for t in agent.get("tags", [])]
            # Check if any tag matches detected technologies
            matches = set(tags) & all_detected
            if matches:
                agent_with_meta = {**agent, "category": category, "matched": list(matches)}
                if agent_with_meta not in recommended:
                    recommended.append(agent_with_meta)

    return recommended


def _get_recommended_mcp(loader, detected: dict) -> list:
    """Get recommended MCP servers based on detected technologies."""
    recommended = []

    # Build detection set
    all_detected = set()
    for lang in detected["languages"]:
        all_detected.add(lang.lower())
        for part in lang.split("/"):
            all_detected.add(part.lower())
    for fw in detected["frameworks"]:
        all_detected.add(fw.lower())
    for tool in detected["tools"]:
        all_detected.add(tool.lower())
    for f in detected["files"]:
        all_detected.add(f.lower())

    # Get MCP catalog
    catalog = loader.get_mcp_catalog()

    # Match MCP servers by tags
    for server in catalog.get("project", []):
        tags = [t.lower() for t in server.get("tags", [])]
        matches = set(tags) & all_detected
        if matches:
            server_with_meta = {**server, "matched": list(matches)}
            if server_with_meta not in recommended:
                recommended.append(server_with_meta)

    return recommended
