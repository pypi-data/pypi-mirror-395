from .captcha_selenium import solve_captcha_selenium
from .captcha_playwright import solve_captcha_playwright
from .captcha_nodriver import solve_captcha_nodriver
import requests
import urllib.request
import asyncio
import base64
import random
import time
import re

def detect_driver_type_type(driver):
    try:
        from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
    except ImportError:
        SeleniumWebDriver = None

    PlaywrightPage = None
    try:
        from playwright.sync_api import Page as PlaywrightPage
    except ImportError:
        try:
            from playwright.async_api import Page as PlaywrightPage
        except ImportError:
            PlaywrightPage = None

    NodriverPage = None
    try:
        from nodriver import Tab as NodriverPage
    except ImportError:
        NodriverPage = None

    if SeleniumWebDriver is not None and isinstance(driver, SeleniumWebDriver):
        return "selenium"
    if PlaywrightPage is not None and isinstance(driver, PlaywrightPage):
        return "playwright"
    if NodriverPage is not None and isinstance(driver, NodriverPage):
        return "nodriver"
    return None



def oca_solve_captcha(driver, user_api_key, action_type, number_captcha_attempts, wait_captcha_seconds, solve_captcha_speed, *args):
    driver_type = detect_driver_type_type(driver)
    if driver_type is None:
        raise ValueError("Driver not passed")
    if not isinstance(user_api_key, str) or not user_api_key.strip():
        raise ValueError("Incorrect user_api_key format")
    if not isinstance(number_captcha_attempts, int) or number_captcha_attempts <= 0:
        raise ValueError("Incorrect number_captcha_attempts format")
    if not isinstance(wait_captcha_seconds, (int, float)) or wait_captcha_seconds <= 0:
        raise ValueError("Incorrect wait_captcha_seconds format")
    if not isinstance(solve_captcha_speed, str) or not solve_captcha_speed.strip():
        raise ValueError("Incorrect solve_captcha_speed format")
    if len(args) > 0:
        selected_captcha_type = args[0].lower()
    speed_mapping = {
        "slow": 10000,
        "normal": 7500,
        "medium": 5000,
        "fast": 3000,
        "very fast": 2000,
        "super fast": 1000
    }

    solve_captcha_speed = solve_captcha_speed.lower()
    if solve_captcha_speed == "random":
        solve_captcha_speed = random.randint(1000, 10000)
    elif solve_captcha_speed in speed_mapping:
        solve_captcha_speed = speed_mapping[solve_captcha_speed]
    else:
        raise ValueError("Invalid solve_captcha_speed value. Choose from: Slow, Normal, Medium, Fast, Very Fast, Super Fast, Random")
        
    
    if driver_type.lower() == "selenium":
        solve_captcha_selenium(driver, user_api_key, action_type, number_captcha_attempts, wait_captcha_seconds, solve_captcha_speed, *args)
    elif driver_type.lower() == "playwright":
        solve_captcha_playwright(driver, user_api_key, action_type, number_captcha_attempts, wait_captcha_seconds, solve_captcha_speed, *args)
    else:
        raise ValueError("Unsupported driver type detected")

async def oca_solve_captcha_async(driver, user_api_key, action_type, number_captcha_attempts, wait_captcha_seconds, solve_captcha_speed, *args):
    driver_type = detect_driver_type_type(driver)
    if driver_type is None:
        raise ValueError("Driver not passed")
    if not isinstance(user_api_key, str) or not user_api_key.strip():
        raise ValueError("Incorrect user_api_key format")
    if not isinstance(number_captcha_attempts, int) or number_captcha_attempts <= 0:
        raise ValueError("Incorrect number_captcha_attempts format")
    if not isinstance(wait_captcha_seconds, (int, float)) or wait_captcha_seconds <= 0:
        raise ValueError("Incorrect wait_captcha_seconds format")
    if not isinstance(solve_captcha_speed, str) or not solve_captcha_speed.strip():
        raise ValueError("Incorrect solve_captcha_speed format")
    if len(args) > 0:
        selected_captcha_type = args[0].lower()
    speed_mapping = {
        "slow": 10000,
        "normal": 7500,
        "medium": 5000,
        "fast": 3000,
        "very fast": 2000,
        "super fast": 1000
    }

    solve_captcha_speed = solve_captcha_speed.lower()
    if solve_captcha_speed == "random":
        solve_captcha_speed = random.randint(1000, 10000)
    elif solve_captcha_speed in speed_mapping:
        solve_captcha_speed = speed_mapping[solve_captcha_speed]
    else:
        raise ValueError("Invalid solve_captcha_speed value. Choose from: Slow, Normal, Medium, Fast, Very Fast, Super Fast, Random")
        
    
    if driver_type.lower() == "nodriver":
        await solve_captcha_nodriver(driver, user_api_key, action_type, number_captcha_attempts, wait_captcha_seconds, solve_captcha_speed, *args)
    else:
        raise ValueError("Unsupported driver type detected")

