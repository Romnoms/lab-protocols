"""
Convert all HTML protocol files to PDF format using Playwright
Uses headless Chromium for perfect rendering of Tailwind CSS and Alpine.js
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# Get the directory where this script is located
base_dir = Path(__file__).parent
pdf_dir = base_dir / "pdf_versions"

# Ensure PDF directory exists
pdf_dir.mkdir(exist_ok=True)

# List of HTML files to convert
html_files = [
    "astrocyte-isolation.html",
    "bodipy-staining.html",
    "cell-culture.html",
    "celltiter-fluor-assay.html",
    "delta-ct-calculation.html",
    "h-and-e-staining.html",
    "hepatocyte-isolation.html",
    "immunofluorescence.html",
    "immunohistochemistry.html",
    "lentivirus-production.html",
    "mouse-genotyping.html",
    "neural-progenitor-culture.html",
    "recipes.html",
    "rna-isolation-cdna-synthesis.html",
    "seahorse-mito-stress-test.html",
    "soft-agar-assay.html",
    "western-blot.html"
]

async def convert_to_pdf(html_file):
    """Convert a single HTML file to PDF"""
    html_path = base_dir / html_file
    pdf_name = html_file.replace('.html', '.pdf')
    pdf_path = pdf_dir / pdf_name

    if not html_path.exists():
        return (html_file, False, "File not found")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # Load the HTML file
            await page.goto(f'file:///{html_path.as_posix()}')

            # Wait for any dynamic content to load
            await page.wait_for_load_state('networkidle')

            # Generate PDF with proper settings
            await page.pdf(
                path=str(pdf_path),
                format='Letter',
                margin={
                    'top': '0.5in',
                    'right': '0.5in',
                    'bottom': '0.5in',
                    'left': '0.5in'
                },
                print_background=True
            )

            await browser.close()

        return (html_file, True, pdf_name)
    except Exception as e:
        return (html_file, False, str(e))

async def main():
    """Main conversion function"""
    print("Starting PDF conversion with Playwright...")
    print(f"Output directory: {pdf_dir}")
    print("-" * 60)

    converted = 0
    failed = 0

    for html_file in html_files:
        print(f"Converting: {html_file}...", end=" ", flush=True)
        file_name, success, result = await convert_to_pdf(html_file)

        if success:
            print(f"[OK] -> {result}")
            converted += 1
        else:
            print(f"[ERROR]: {result}")
            failed += 1

    print("-" * 60)
    print(f"\nConversion complete!")
    print(f"[OK] Successfully converted: {converted}")
    if failed > 0:
        print(f"[ERROR] Failed: {failed}")
    print(f"\nPDF files saved to: {pdf_dir}")

if __name__ == "__main__":
    asyncio.run(main())
