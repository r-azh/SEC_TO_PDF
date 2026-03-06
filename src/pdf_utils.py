from playwright.async_api import async_playwright


async def get_browser_async():
    """Start Playwright and launch a Chromium browser.

    Returns a tuple (playwright_instance, browser) so that the caller can stop
    the Playwright service later.
    """
    p = await async_playwright().start()
    browser = await p.chromium.launch()
    return p, browser


async def close_browser(p, browser):
    """Close browser and stop Playwright service asynchronously."""
    await browser.close()
    await p.stop()


async def convert_to_pdf_async(html: str, output_path: str) -> None:
    """Render HTML content as a PDF asynchronously."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.set_content(html)
        await page.pdf(path=output_path, format="A4")
        await context.close()
        await browser.close()

