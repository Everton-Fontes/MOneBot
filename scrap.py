import asyncio


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()

    # Open new page
    page = await context.new_page()

    # Go to https://77uu.co/#/
    await page.goto("https://77uu.co/#/")

    # Click text=Log In
    await page.locator("text=Log In").click()
    # await expect(page).to_have_url("https://77uu.co/#/login")

    # Click [placeholder="Enter the username"]
    await page.locator("[placeholder=\"Enter the username\"]").click()

    # Fill [placeholder="Enter the username"]
    await page.locator("[placeholder=\"Enter the username\"]").fill("MrEfs66")

    # Press Tab
    await page.locator("[placeholder=\"Enter the username\"]").press("Tab")

    # Fill [placeholder="Enter the password"]
    await page.locator("[placeholder=\"Enter the password\"]").fill("Efs06j666")

    # Press Enter
    # async with page.expect_navigation(url="https://77uu.co/#/uc/safe"):
    async with page.expect_navigation():
        await page.locator("[placeholder=\"Enter the password\"]").press("Enter")

    # Go to https://77uu.co/#/gameCenter
    await page.goto("https://77uu.co/#/gameCenter?gameName=CQK1M")

    # Primeira linha
    # esquerda
    # Click text=06221211 09:11:00 0xd9****db47 SO >> b >> nth=0
    await page.locator("div.issueItem:nth-child(1) > span:nth-child(4) > b:nth-child(1)").first.click()
    # direita
    # Click text=06221211 09:11:00 0xd9****db47 SO >> b >> nth=1
    await page.locator("div.issueItem:nth-child(1) > span:nth-child(4) > b:nth-child(2)").nth(1).click()

    # tempo
    # Click text=06221212 09:12:00 0xfd****9ffb BO >> b >> nth=1
    await page.locator("div.issueItem:nth-child(1) > span:nth-child(1)").nth(1).click()
    # primeira linha

    # Click text=1.9500x >> nth=0
    await page.locator("text=1.9500x").first.click()

    # Click text=Small 1.9500x
    await page.locator("text=Small 1.9500x").click()

    # Click text=1.9500x >> nth=2
    await page.locator("text=1.9500x").nth(2).click()

    # Click text=1.9500x >> nth=3
    await page.locator("text=1.9500x").nth(3).click()

    # Click [placeholder="Amount of per bet"]
    await page.locator("[placeholder=\"Amount of per bet\"]").click()

    # Fill [placeholder="Amount of per bet"]
    await page.locator("[placeholder=\"Amount of per bet\"]").fill("0.1")

    # Click text=Bet Now
    await page.locator("text=Bet Now").click()

    # Click button:has-text("OK") >> nth=1
    await page.locator("button:has-text(\"OK\")").nth(1).click()

    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
