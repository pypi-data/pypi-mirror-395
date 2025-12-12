# pbixtrans: Translate a PBIX report visuals into another language

**pbixtrans** is a command-line tool for translating Power BI (`.pbix`) visuals into different languages.

## Features

- 🌍 **Automatic Translation**: Translates Power BI report content using Google Translate
- 🔄 **Preserves Structure**: Maintains all report formatting, visuals, and data connections
- 🚀 **Simple CLI**: Easy-to-use command-line interface

## Currently Supported Elements

- ✅ Report page names
- ✅ Textbox content
- ✅ Action Button text
- ✅ Slicer text
- ✅ Shape text
- ⏳ *(more coming soon)*

## Installation

### From PyPI (when published)

```bash
pip install pbixtrans
```

### From Source

```bash
git clone https://github.com/tbrus/pbixtrans.git
cd pbixtrans
pip install -e .
```

## Usage

Translate `report.pbix` to `pl`:

```bash
pbixtrans -f report.pbix -l pl
```

This will create `report_pl.pbix` in the same directory.

## Limitations

- Requires internet connection for translation
- Data model (tables, columns, DAX) is not translated

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is not affiliated with or endorsed by Microsoft. Power BI and PBIX are trademarks of Microsoft Corporation.