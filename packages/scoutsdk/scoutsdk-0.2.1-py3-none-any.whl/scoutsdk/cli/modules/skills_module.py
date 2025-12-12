import argparse
from pathlib import Path

from .base_module import BaseModule
from ..config import Config
from ..error_handler import ValidationError
from ..utils import get_data_path
from scoutsdk.api import ScoutAPI


class SkillsModule(BaseModule):
    def __init__(self, config: Config) -> None:
        self.config = config

    def get_command(self) -> str:
        return "skills"

    def add_parser(self, subparsers: argparse._SubParsersAction) -> None:
        skills_parser = subparsers.add_parser(
            self.get_command(), help="Manage global skills"
        )

        # Create subparsers for skills commands
        skills_subparsers = skills_parser.add_subparsers(
            dest="skills_command", required=True
        )

        # skills init
        init_parser = skills_subparsers.add_parser(
            "init", help="Create a skills.json from template"
        )
        init_parser.add_argument(
            "-d",
            "--directory",
            type=str,
            default=".",
            help="Directory to create the skill files in (default: current directory)",
        )
        init_parser.set_defaults(func=self._init_skill)

        # skills list
        list_parser = skills_subparsers.add_parser(
            "list", help="List all global skills"
        )
        list_parser.set_defaults(func=self._list_skills)

        # skills synchronize
        sync_parser = skills_subparsers.add_parser(
            "synchronize", help="Synchronize skills from config file"
        )
        sync_parser.add_argument(
            "-f", "--file", type=str, required=True, help="Path to skills.json file"
        )
        sync_parser.add_argument(
            "--force", action="store_true", help="Force overwrite skill files"
        )
        sync_parser.set_defaults(func=self._synchronize_skills)

    def execute(self, args: argparse.Namespace) -> None:
        """Execute the skills command."""
        # This will be called by the specific subcommand
        args.func(args)

    def _init_skill(self, args: argparse.Namespace) -> None:
        """Initialize a new skills.json from template."""
        # Prompt for skill name
        skill_name = input("\nEnter skill name: ").strip()
        if not skill_name:
            raise ValidationError("Skill name cannot be empty")

        # Prompt for skill description
        skill_description = input("Enter skill description: ").strip()
        if not skill_description:
            raise ValidationError("Skill description cannot be empty")

        # Generate skill identifier (lowercase with underscores)
        skill_id = self._normalize_skill_name(skill_name)

        # Create target directory if it doesn't exist
        target_dir = Path(args.directory)
        target_dir.mkdir(exist_ok=True)

        # Load template
        template_path = get_data_path("skills", "skills_template.json")
        if not template_path.exists():
            raise ValidationError("Skills template file not found")

        with open(template_path, "r") as f:
            content = f.read()

        # Replace placeholders in the template
        content = content.replace("{SKILL_IDENTIFIER}", skill_id)
        content = content.replace("{SKILL_NAME}", skill_name)
        content = content.replace("{SKILL_DESCRIPTION}", skill_description)

        # Write to target directory as skills.json
        output_file = target_dir / "skills.json"
        with open(output_file, "w") as f:
            f.write(content)

        # Create functions directory and copy template files
        self._create_functions_directory(target_dir)

        print(f"Created skill '{skill_name}' with config file '{output_file}'")

        # Offer to create initial function
        create_function = (
            input("\nWould you like to create an initial function? (y/n) [y]: ")
            .strip()
            .lower()
        )

        if create_function == "" or create_function == "y":
            self._create_initial_function(functions_dir=target_dir / "functions")

        print(
            "\nSkill initialized successfully!\n"
            "\nNext steps:\n"
            "  1. Edit your function(s) in functions/\n"
            "  2. Update requirements.txt with any dependencies\n"
            "  3. Run 'scoutcli skills synchronize -f skills.json' to deploy"
        )

    def _list_skills(self, args: argparse.Namespace) -> None:
        """List all global skills from server."""
        try:
            scout_api = ScoutAPI()
            skills = scout_api.skills.list_all()

            if not skills:
                print("No global skills found")
                return

            print(f"Found {len(skills)} global skill(s):")
            for skill in skills:
                name = skill.get("name", "N/A")
                skill_id = skill.get("id", "N/A")
                description = skill.get("description") or "No description"
                skill_type = skill.get("type", "N/A")
                status = skill.get("functions_status", "N/A")

                print(f"  - {name}")
                print(f"    ID: {skill_id}")
                print(f"    Description: {description}")
                print(f"    Type: {skill_type}, Status: {status}")
                print()

        except Exception as e:
            raise ValidationError(f"Failed to list skills: {str(e)}")

    def _synchronize_skills(self, args: argparse.Namespace) -> None:
        """Synchronize skills from config file."""
        from .pkg_module import PkgModule
        from .skills_sync_module import SkillsSyncModule

        pkg_module = PkgModule(config=self.config)
        sync_module = SkillsSyncModule(config=self.config, pkg_module=pkg_module)

        # Create args compatible with the sync module
        sync_args = argparse.Namespace()
        sync_args.config = args.file
        sync_args.force = getattr(args, "force", False)

        sync_module.execute(sync_args)

    def _normalize_skill_name(self, name: str) -> str:
        """Normalize skill name to lowercase with underscores."""
        from ..utils import normalize_snake_case_name

        return normalize_snake_case_name(name, default="custom_skill")

    def _create_functions_directory(self, target_dir: Path) -> None:
        """Create functions directory and copy template files."""
        from .functions_module import FunctionsModule

        # Create functions directory
        functions_dir = target_dir / "functions"
        functions_dir.mkdir(exist_ok=True)

        # Use FunctionsModule to copy template files
        functions_module = FunctionsModule(config=self.config)
        functions_module.ensure_template_files(str(functions_dir))

    def _create_initial_function(self, functions_dir: Path) -> None:
        """
        Create an initial function using FunctionsModule's template system.

        Delegates to FunctionsModule._init_function() for complete workflow.

        Args:
            functions_dir (Path): The functions directory to create the function in
        """
        from .functions_module import FunctionsModule
        import argparse

        # Prepare mock args for FunctionsModule
        mock_args = argparse.Namespace()
        mock_args.directory = str(functions_dir)

        # Delegate to FunctionsModule for complete function creation workflow
        # This handles: template selection, name prompting, validation, file creation
        functions_module = FunctionsModule(config=self.config)
        functions_module._init_function(mock_args)
