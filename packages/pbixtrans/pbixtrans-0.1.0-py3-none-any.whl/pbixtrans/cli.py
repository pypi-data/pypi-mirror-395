import argparse
import sys

from pbixtrans.extraction import pbix_to_folder, folder_to_pbix
from pbixtrans.layout import get_layout, translate_layout, save_layout


class NoMetavarInOptions(argparse.HelpFormatter):
    """Custom formatter that hides the metavar in the option list.
    Example:
      '-f, --file' instead of '-f file, --file file'
    """
    def _format_action_invocation(self, action):
        if not action.option_strings:
            return super()._format_action_invocation(action)

        # Option flags only, no metavar here
        return ", ".join(action.option_strings)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pbixtrans",
        description="Translate a PBIX report visuals into another language.",
        formatter_class=lambda prog: NoMetavarInOptions(prog, max_help_position=30),
        add_help=False, # Disable default help to customize
    )

    # Required arguments
    required = parser.add_argument_group("Required arguments")
    required.add_argument(
        "-f", "--file",
        metavar="file",
        required=True,
        help="Path to the input PBIX file.",
    )
    required.add_argument(
        "-l", "--lang",
        metavar="lang",
        required=True,
        help="Target language code (e.g., 'pl', 'de', 'fr').",
    )

    # Optional arguments
    optional = parser.add_argument_group("Options")
    optional.add_argument(
        "-h", "--help",
        action="help",
        help="Show this help message and exit.",
    )

    # Show help when no args are passed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args()


def translate(pbix_file: str, lang: str) -> None:
    folder = pbix_file.replace(".pbix", "") + "_extracted"
    new_pbix = pbix_file.replace(".pbix", f"_{lang}.pbix")

    pbix_to_folder(pbix_file, folder)
    layout = get_layout(folder)
    layout = translate_layout(layout, lang)
    save_layout(layout, folder)
    folder_to_pbix(folder, new_pbix)


def main() -> None:
    args = parse_args()   
    translate(
        pbix_file=args.file,
        lang=args.lang.strip().lower()
    )


if __name__ == "__main__":
    main()