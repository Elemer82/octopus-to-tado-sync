import asyncio
from datetime import datetime
import logging
from playwright.async_api import async_playwright
from PyTado.interface import Tado


def send_reading_to_tado(username: str, password: str, reading: int = 0):
    """
    Sends the total consumption reading to Tado using its Energy IQ feature.
    """
    # tado = Tado(username, password)
    tado = tado_login(username=username, password=password)
    result = tado.set_eiq_meter_readings(reading=int(reading))
    print(result)


def send_reading_to_tado_with_date(username: str, password: str, reading: int = 0,
                                   date: datetime = datetime.now()):
    """
    Sends the consumption reading to Tado using its Energy IQ feature.
    """
    # tado = Tado(username, password)
    tado = tado_login(username=username, password=password)
    print(f"Submitting reading for {date.strftime('%Y-%m-%d')} with the value of {reading}")
    result = tado.set_eiq_meter_readings(reading=int(reading), date=date.strftime('%Y-%m-%d'))
    print(result)


async def browser_login(url: str, username: str, password: str, logger_: logging.Logger = logging.getLogger()):
    """
    Perform the login process using Playwright.
    This function will open a browser, navigate to the login page,
    fill in the username and password, and click the login button.
    It will also take a screenshot of the page after login.
    param url: The URL of the login page.
    param username: The username for login.
    param password: The password for login.
    param logger_: The logger object for logging messages.
    return: None
    """
    logger_.info(f"Logging in to Tado using Playwright...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True
        )  # Set to True if you don't want a browser window
        context = await browser.new_context()
        page = await context.new_page()

        logger_.debug(f"Opening browser to {url}")
        await page.goto(url)

        # Click the "Submit" button before login
        await page.wait_for_selector('text="Submit"', timeout=5000)
        await page.click('text="Submit"')

        # Wait for the login form to appear
        await page.wait_for_selector('input[name="loginId"]')

        # Replace with actual selectors for your site
        logger_.debug(f"Filling in username and password...")
        await page.fill('input[id="loginId"]', username)
        await page.fill('input[name="password"]', password)

        logger_.debug(f"Clicking \"Sign in\" button...")
        await page.click('button.c-btn--primary:has-text("Sign in")')

        # Optionally take a screenshot
        await page.screenshot(path="screenshot.png")

        await page.wait_for_selector(
            ".text-center.message-screen.b-bubble-screen__spaced", timeout=10000
        )

        # Take a screenshot (optional)
        screenshot_file = "screenshot.png"
        logger_.debug(f"Taking screenshot and saving to {screenshot_file}")
        await page.screenshot(path=screenshot_file)
        logger_.debug(f"Closing browser...")
        await browser.close()
    
    logger_.debug(f"Login process completed.")
    


def tado_login(username: str, password: str, logger_: logging.Logger = logging.getLogger()) -> Tado:
    """
    Login to Tado using the provided username and password.
    If the login is successful, it returns a Tado object.
    If the login is pending, it will prompt the user to complete the login process.
    """
    logger_.info(f"Logging in to Tado...")
    url = "https://my.tado.com/en-GB/login"

    tado = Tado(token_file_path="tado_refresh_token")

    status = tado.device_activation_status()

    if status == "PENDING":
        url = tado.device_verification_url()

        asyncio.run(browser_login(url=str(url), username=username, password=password))

        tado.device_activation()

        status = tado.device_activation_status()

    if status == "COMPLETED":
        logger_.info(f"Login successful")
    else:
        logger_.info(f"Login status is {status}")

    return tado
