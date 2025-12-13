"""Main entry point for agentic-crew - Framework-Agnostic Crew Runner.

This is a generic crew runner that discovers and executes crews
defined in packages' .crew/, .crewai/, .langgraph/, or .strands/ directories.

Usage:
    # List all available packages with crews
    agentic-crew list
    agentic-crew list --json  # JSON output for external tools

    # List crews in a specific package
    agentic-crew list otterfall

    # Run a crew
    agentic-crew run otterfall game_builder --input "Create a BiomeComponent"
    agentic-crew run otterfall game_builder --input "..." --json  # JSON output

    # Run with input from file
    agentic-crew run otterfall game_builder --file tasks.md

    # Show crew details
    agentic-crew info otterfall game_builder --json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from agentic_crew.core.discovery import discover_packages, get_crew_config, list_crews
from agentic_crew.core.runner import run_crew


def cmd_list(args):
    """List available packages and crews."""
    framework = getattr(args, "framework", None)
    use_json = getattr(args, "json", False)

    crews_by_package = list_crews(
        args.package if hasattr(args, "package") else None,
        framework=framework,
    )

    if use_json:
        # Flatten to list for JSON output
        all_crews = []
        for pkg_name, crews in crews_by_package.items():
            for crew in crews:
                all_crews.append(
                    {
                        "package": pkg_name,
                        "name": crew["name"],
                        "description": crew.get("description", ""),
                        "required_framework": crew.get("required_framework"),
                    }
                )
        print(json.dumps({"crews": all_crews}, indent=2))
        return

    if not crews_by_package:
        print("No packages with crew configuration directories found.")
        print("\nTo add crews to a package, create one of:")
        print("  packages/<name>/.crew/manifest.yaml     # Framework-agnostic")
        print("  packages/<name>/.crewai/manifest.yaml   # CrewAI-specific")
        print("  packages/<name>/.langgraph/manifest.yaml  # LangGraph-specific")
        print("  packages/<name>/.strands/manifest.yaml  # Strands-specific")
        return

    print("=" * 60)
    print("AVAILABLE CREWS")
    print("=" * 60)

    for pkg_name, crews in crews_by_package.items():
        print(f"\n📦 {pkg_name}")
        for crew in crews:
            desc = crew.get("description", "")
            framework_info = ""
            if crew.get("required_framework"):
                framework_info = f" [{crew['required_framework']}]"
            print(f"   • {crew['name']}{framework_info}: {desc}")


def cmd_run(args):
    """Run a specific crew."""
    from agentic_crew.core.decomposer import detect_framework, run_crew_auto

    use_json = getattr(args, "json", False)
    start_time = time.time()

    if not use_json:
        print("=" * 60)
        print(f"🚀 Running {args.package}/{args.crew}")
        print("=" * 60)

    # Get input
    if args.file:
        input_text = Path(args.file).read_text()
    elif args.input:
        input_text = args.input
    else:
        input_text = ""

    inputs = {"spec": input_text, "component_spec": input_text, "input": input_text}

    # Discover package and load config
    packages = discover_packages()
    if args.package not in packages:
        if use_json:
            print(
                json.dumps(
                    {
                        "success": False,
                        "error": f"Package '{args.package}' not found",
                        "available_packages": list(packages.keys()),
                        "duration_ms": int((time.time() - start_time) * 1000),
                    }
                )
            )
        else:
            print(f"❌ Package '{args.package}' not found.")
            print(f"Available: {list(packages.keys())}")
        sys.exit(2)  # Exit code 2 = configuration error

    config_dir = packages[args.package]

    try:
        crew_config = get_crew_config(config_dir, args.crew)

        # Determine framework
        required = crew_config.get("required_framework")
        requested = args.framework if args.framework != "auto" else None
        framework_used = required or requested or detect_framework()

        if not use_json:
            if required:
                print(f"📋 Framework: {required} (required by .{required}/ directory)")
            elif requested:
                print(f"📋 Framework: {requested} (requested)")
            else:
                print(f"📋 Framework: {framework_used} (auto-detected)")

        result = run_crew_auto(
            crew_config,
            inputs=inputs,
            framework=requested,
        )

        duration_ms = int((time.time() - start_time) * 1000)

        if use_json:
            print(
                json.dumps(
                    {
                        "success": True,
                        "output": result,
                        "framework_used": framework_used,
                        "duration_ms": duration_ms,
                    }
                )
            )
        else:
            print("\n" + "=" * 60)
            print("📄 RESULT")
            print("=" * 60)
            print(result)

    except (ValueError, RuntimeError) as e:
        duration_ms = int((time.time() - start_time) * 1000)
        if use_json:
            print(
                json.dumps(
                    {
                        "success": False,
                        "error": str(e),
                        "duration_ms": duration_ms,
                    }
                )
            )
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)  # Exit code 1 = crew execution failed


def cmd_build(args):
    """Legacy build command - runs otterfall game_builder."""
    print("=" * 60)
    print("🎮 OTTERFALL GAME BUILDER")
    print("=" * 60)
    print()
    print(f"Building: {args.spec[:100]}...")

    inputs = {"spec": args.spec, "component_spec": args.spec}

    try:
        result = run_crew("otterfall", "game_builder", inputs)
        print("\n" + "=" * 60)
        print("📄 RESULT")
        print("=" * 60)
        print(result)
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nNote: The 'build' command requires packages/otterfall/.crewai/")
        sys.exit(1)


def cmd_info(args):
    """Show detailed info about a crew."""
    use_json = getattr(args, "json", False)
    packages = discover_packages()

    if args.package not in packages:
        if use_json:
            print(
                json.dumps(
                    {
                        "error": f"Package '{args.package}' not found",
                        "available_packages": list(packages.keys()),
                    }
                )
            )
        else:
            print(f"❌ Package '{args.package}' not found.")
            print(f"Available: {list(packages.keys())}")
        sys.exit(2)

    config_dir = packages[args.package]

    try:
        config = get_crew_config(config_dir, args.crew)
    except ValueError as e:
        if use_json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"❌ {e}")
        sys.exit(2)

    if use_json:
        print(
            json.dumps(
                {
                    "package": args.package,
                    "name": args.crew,
                    "description": config.get("description", ""),
                    "required_framework": config.get("required_framework"),
                    "agents": [
                        {"name": name, "role": cfg.get("role", name)}
                        for name, cfg in config.get("agents", {}).items()
                    ],
                    "tasks": [
                        {"name": name, "description": cfg.get("description", "")}
                        for name, cfg in config.get("tasks", {}).items()
                    ],
                    "knowledge_paths": config.get("knowledge_paths", []),
                },
                indent=2,
            )
        )
        return

    print("=" * 60)
    print(f"CREW: {args.package}/{args.crew}")
    print("=" * 60)
    print(f"\nDescription: {config.get('description', 'N/A')}")

    print("\n📋 Agents:")
    for name, cfg in config.get("agents", {}).items():
        role = cfg.get("role", name)
        print(f"   • {name}: {role}")

    print("\n📝 Tasks:")
    for name, cfg in config.get("tasks", {}).items():
        desc = cfg.get("description", "")[:60]
        print(f"   • {name}: {desc}...")

    print("\n📚 Knowledge:")
    for kp in config.get("knowledge_paths", []):
        print(f"   • {kp}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="agentic-crew - Framework-Agnostic Crew Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # List all packages with crews
    agentic-crew list
    agentic-crew list --json  # JSON output for external tools

    # List crews in a package
    agentic-crew list otterfall

    # Run a crew
    agentic-crew run otterfall game_builder --input "Create a QuestComponent"
    agentic-crew run otterfall game_builder --input "..." --json  # JSON output

    # Show crew details
    agentic-crew info otterfall game_builder --json

Exit codes:
    0 - Success
    1 - Crew execution failed
    2 - Configuration error (package/crew not found)
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List available crews")
    list_parser.add_argument("package", nargs="?", help="Package to list crews for")
    list_parser.add_argument(
        "--framework",
        choices=["crewai", "langgraph", "strands"],
        help="Filter crews by framework",
    )
    list_parser.add_argument(
        "--json", action="store_true", help="Output as JSON (for external tools)"
    )

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a crew")
    run_parser.add_argument("package", help="Package name (e.g., otterfall)")
    run_parser.add_argument("crew", help="Crew name (e.g., game_builder)")
    run_parser.add_argument("--input", "-i", help="Input specification")
    run_parser.add_argument("--file", "-f", help="Read input from file")
    run_parser.add_argument(
        "--framework",
        choices=["auto", "crewai", "langgraph", "strands"],
        default="auto",
        help="Framework to use (auto=detect, or specify). "
        "Note: If crew is in a framework-specific directory, that takes precedence.",
    )
    run_parser.add_argument(
        "--json", action="store_true", help="Output as JSON (for external tools)"
    )

    # Info command
    info_parser = subparsers.add_parser("info", help="Show crew details")
    info_parser.add_argument("package", help="Package name")
    info_parser.add_argument("crew", help="Crew name")
    info_parser.add_argument(
        "--json", action="store_true", help="Output as JSON (for external tools)"
    )

    # Legacy build command (for backwards compatibility)
    build_parser = subparsers.add_parser("build", help="Build a game component (legacy)")
    build_parser.add_argument("spec", help="Component specification")

    # Legacy commands
    subparsers.add_parser("list-knowledge", help="List knowledge sources (legacy)")
    subparsers.add_parser("test-tools", help="Test file tools (legacy)")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "run":
        cmd_run(args)
    elif args.command == "info":
        cmd_info(args)
    elif args.command == "build":
        cmd_build(args)
    elif args.command == "list-knowledge":
        # Legacy - list knowledge from otterfall
        packages = discover_packages()
        if "otterfall" in packages:
            config = get_crew_config(packages["otterfall"], "game_builder")
            print("Knowledge sources:")
            for kp in config.get("knowledge_paths", []):
                print(f"  • {kp}")
        else:
            print("No otterfall package found.")
    elif args.command == "test-tools":
        from agentic_crew.tools.file_tools import DirectoryListTool, get_workspace_root

        print(f"Workspace root: {get_workspace_root()}")
        tool = DirectoryListTool()
        print(tool._run("packages"))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
