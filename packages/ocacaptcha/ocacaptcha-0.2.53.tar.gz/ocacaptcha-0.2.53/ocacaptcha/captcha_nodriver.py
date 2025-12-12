import requests
import urllib.request
import base64
import random
import asyncio
import time
import re
import json

async def solve_captcha_nodriver(tab, user_api_key, action_type, number_captcha_attempts, wait_captcha_seconds, solve_captcha_speed, *args):
    if len(args) > 0:
        selected_captcha_type = args[0].lower()
    else:
        selected_captcha_type = None

    async def get_captcha_image_nodriver(tab, blob_url: str):
        blob_url_js = json.dumps(blob_url)
        js_code = f""" (async () => {{ try {{ const response = await fetch({blob_url_js}); const blob = await response.blob(); return await new Promise((resolve) => {{ const reader = new FileReader(); reader.onloadend = () => resolve(reader.result); reader.readAsDataURL(blob); }}); }} catch (error) {{ return null; }} }})() """
        image_data = await tab.evaluate(js_code, await_promise=True, return_by_value=True)
        if not image_data:
            raise ValueError("Error when getting captcha image (blob fetch failed)")
        
        if "base64" in image_data:
            return image_data.split(",")[1]
        raise ValueError("Blob fetch returned unexpected data")

    async def element_exists(tab, xpath: str) -> bool:
        try:
            js = f""" (() => {{ try {{ return document.evaluate({xpath!r}, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue !== null; }} catch (e) {{ return false; }} }})() """
            return await tab.evaluate(js)
        except Exception:
            return False
        
    async def safe_get_js_attributes(el):
        try:
            await el.update()           
            js = """ function (e) { try { var rect = e.getBoundingClientRect ? e.getBoundingClientRect() : { left:0, top:0, width:0, height:0 }; var computed = window.getComputedStyle ? window.getComputedStyle(e) : null; var width = rect.width || (computed ? parseFloat(computed.width) || 0 : 0); var height = rect.height || (computed ? parseFloat(computed.height) || 0 : 0); var left = Math.round(rect.left + (window.scrollX || 0)); var top = Math.round(rect.top + (window.scrollY || 0)); var tag = e.tagName || null; var src = null; if (tag && tag.toLowerCase() === 'img') { src = e.src || (e.getAttribute ? e.getAttribute('src') : null) || null; } else { src = (e.getAttribute ? e.getAttribute('src') : null) || null; } return JSON.stringify({ src: src, width: Math.round(width), height: Math.round(height), x: left, y: top, tag: tag }); } catch(err) { return JSON.stringify({ src: null, width: 0, height: 0, x: 0, y: 0, tag: (e.tagName || null), error: String(err) }); } } """
            data_str = await el.apply(js, return_by_value=True)
            if not data_str:
                return {}
            info = json.loads(data_str)
            return { "src": info.get("src"), "width": int(info.get("width", 0)), "height": int(info.get("height", 0)), "left": int(info.get("left", 0)), "top": int(info.get("top", 0)), "tag": info.get("tag") }
        except Exception as e:
            print("safe_get_js_attributes failed:", e)
            return {}

    async def safe_get_text(el):
        try:
            if not el:
                return None
            await el.update()
            text = await el.apply("""(e) => e.textContent || e.innerText || ''""")
            return text.strip() if text else None
        except Exception as e:
            print("safe_get_text failed:", e)
            return None

    async def eval_js(js_code: str):
        try:
            result = await tab.evaluate(js_code, await_promise=True, return_by_value=False)
            return result
        except Exception as e:
            print(f"[eval_js] Error executing JS: {e}")
            return None
    
    if not number_captcha_attempts or number_captcha_attempts <= 0:
        number_captcha_attempts = 1
    if not wait_captcha_seconds or wait_captcha_seconds <= 0:
        wait_captcha_seconds = 0
    action_type = action_type.lower()
    if action_type in ("tiktokwhirl", "tiktokslide", "tiktok3d", "tiktokicon"):
        try: 
            start_time = time.time()
            while time.time() - start_time < wait_captcha_seconds:
                wait_is_exist_captcha_whirl = await element_exists(tab, '//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")] | ' + '//div[contains(@class, "cap") and count(img) = 2 and contains(img/@style, "circle")]')
                wait_is_exist_captcha_slide = await element_exists(tab, '//div[contains(@class, "captcha") and contains(@class, "verify")]//img[contains(@class, "captcha_verify_img_slide")] | ' + '//div[contains(@class, "cap")]//div[contains(@draggable, "true")]/img[contains(@draggable, "false")]')
                wait_is_exist_captcha_3d = await element_exists(tab, '//img[contains(@id,"verify")][contains(@src,"/3d_")] | ' + '//div[contains(@class,"cap")]//img/following-sibling::button /parent::div/parent::div/parent::div//' + 'img[(contains(@src,"blob") or contains(@src,"/3d_")) and ' + '//div[contains(@class,"cap")]//img/following-sibling::button and ' + '//div[contains(@class,"cap")]//span[contains(text(), "2")]]')
                wait_is_exist_captcha_icon = await element_exists(tab, '//div[contains(@class,"verify") and count(img) = 1]/img[contains(@src,"icon")] | ' + '//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//' + 'img[(contains(@src,"blob") or contains(@src,"/icon_")) and ' + '//div[contains(@class,"cap")]//img/following-sibling::button and ' + '//div[contains(@class,"cap")]//span[contains(text(), "?")]]')
                if (wait_is_exist_captcha_whirl or wait_is_exist_captcha_slide or wait_is_exist_captcha_3d or wait_is_exist_captcha_icon):
                    break
                time.sleep(1)

            for i in range(0, number_captcha_attempts):
                is_exist_captcha_whirl = await element_exists(tab, '//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")] | ' + '//div[contains(@class, "cap") and count(img) = 2 and contains(img/@style, "circle")]')
                is_exist_captcha_slide = await element_exists(tab, '//div[contains(@class, "captcha") and contains(@class, "verify")]//img[contains(@class, "captcha_verify_img_slide")] | ' + '//div[contains(@class, "cap")]//div[contains(@draggable, "true")]/img[contains(@draggable, "false")]')
                is_exist_captcha_3d = await element_exists(tab, '//img[contains(@id,"verify")][contains(@src,"/3d_")] | ' + '//div[contains(@class,"cap")]//img/following-sibling::button /parent::div/parent::div/parent::div//' + 'img[(contains(@src,"blob") or contains(@src,"/3d_")) and ' + '//div[contains(@class,"cap")]//img/following-sibling::button and ' + '//div[contains(@class,"cap")]//span[contains(text(), "2")]]')
                is_exist_captcha_icon = await element_exists(tab, '//div[contains(@class,"verify") and count(img) = 1]/img[contains(@src,"icon")] | ' + '//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//' + 'img[(contains(@src,"blob") or contains(@src,"/icon_")) and ' + '//div[contains(@class,"cap")]//img/following-sibling::button and ' + '//div[contains(@class,"cap")]//span[contains(text(), "?")]]')
                if not (is_exist_captcha_whirl or is_exist_captcha_slide or is_exist_captcha_3d or is_exist_captcha_icon):
                    break

                get_refresh_button = await element_exists(tab, '//a[contains(@class,"refresh")]/span[contains(@class,"refresh")][text()] | //button[contains(@class,"cap-items")][1]')
                if get_refresh_button:
                    update_captcha_img_click = await tab.xpath('/a[contains(@class,"refresh")]/span[contains(@class,"refresh")][text()] | //button[contains(@class,"cap-items")][1]')
                else:
                    update_captcha_img_click = await tab.xpath('//div[contains(@class,"captcha_verify_action")]//button[1]//div[contains(@class,"Button-label")][text()]')
                
                if is_exist_captcha_whirl:
                    get_captcha_data = await tab.xpath('//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")] | ' + '//div[contains(@class, "cap") and count(img) = 2 and contains(img/@style, "circle")]/img[1]')
                    get_captcha_data_slider = await tab.xpath('//div[contains(@class,"slidebar")] | ' + '//div[contains(@class, "cap")]/div[contains(@draggable, "true")]/parent::div')
                    img_el_image = get_captcha_data[0]
                    img_el_slider = get_captcha_data_slider[0]
                    get_captcha_data = await safe_get_js_attributes(img_el_image)
                    get_captcha_data_slider = await safe_get_js_attributes(img_el_slider)
                    full_img_url = get_captcha_data.get("src")
                    img_width = get_captcha_data_slider.get("width", 0)
                    img_height = get_captcha_data_slider.get("height", 0)
                    if "blob:" in full_img_url:
                        full_img = await get_captcha_image_nodriver(tab, full_img_url)
                    elif full_img_url.startswith("data:image"):
                        full_img = full_img_url.strip()
                    else: 
                        open_full_img_url = urllib.request.urlopen(full_img_url)
                        full_img_url_html_bytes = open_full_img_url.read()
                        full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                        full_img = full_screenshot_img_url_base64

                    get_captcha_data = await tab.xpath('//div[contains(@class,"captcha_verify_container")]/div/img[2][contains(@style,"transform: translate(-50%, -50%) rotate")] |' + ' //div[contains(@class, "cap") and count(img) = 2 and contains(img/@style, "circle")]/img[2]')
                    img_el = get_captcha_data[0]
                    get_captcha_data = await safe_get_js_attributes(img_el)
                    small_img_url = get_captcha_data.get("src")
                    if "blob:" in small_img_url:
                        small_img = await get_captcha_image_nodriver(tab, small_img_url)
                    elif small_img_url.startswith("data:image"):
                        small_img = small_img_url.strip()
                    else: 
                        open_small_img_url = urllib.request.urlopen(small_img_url)
                        small_img_url_html_bytes = open_small_img_url.read()
                        small_screenshot_img_url_base64 = base64.b64encode(small_img_url_html_bytes).decode('utf-8')
                        small_img = small_screenshot_img_url_base64
                    captcha_action_type = "tiktokWhirl"
                    multipart_form_data = {
                        'FULL_IMG_CAPTCHA': (None, full_img),
                        'SMALL_IMG_CAPTCHA': (None, small_img),
                        'FULL_IMG_WIDTH': (None, img_width),
                        'FULL_IMG_HEIGHT': (None, img_height),
                        'ACTION': (None, captcha_action_type),
                        'USER_KEY': (None, user_api_key)
                    }
                    request_solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                    response_solve_captcha_content = request_solve_captcha.content
                    if isinstance(response_solve_captcha_content, bytes):
                        response_solve_captcha_content = response_solve_captcha_content.decode('utf-8')

                    if response_solve_captcha_content == "ERROR_USER_KEY":
                        raise Exception("Invalid API key / Make sure you using correct API key")
                    elif response_solve_captcha_content == "INVALID_ACTION":
                        raise Exception("Invalid action type / Supports: tiktokWhirl, tiktokSlide, tiktok3D, tiktokIcon")
                    elif response_solve_captcha_content == "ZERO_BALANCE":
                        raise Exception("Balance is zero / Top up your balance")

                    if response_solve_captcha_content.strip().startswith('{') and response_solve_captcha_content.strip().endswith('}'):
                        response_solve_captcha = request_solve_captcha.json()
                        response_coordinate_x = int(response_solve_captcha["coordinate_x"])
                        response_coordinate_y = int(response_solve_captcha["coordinate_y"])
                        random_move_left_right = random.randint(15, 50)
                        random_move_number = random.randint(1, 2)
                        if random_move_number == 1:
                            response_coordinate_x_random_move = int(response_coordinate_x) - int(random_move_left_right)
                        else:
                            response_coordinate_x_random_move = int(response_coordinate_x) + int(random_move_left_right)
                        time.sleep(random.uniform(0.1, 0.3))
                        pixel_delay = random.uniform(solve_captcha_speed / 300, solve_captcha_speed / 500)
                        params_json = { "intermediateX": response_coordinate_x_random_move, "targetX": response_coordinate_x, "duration": solve_captcha_speed, "pixelDelay": pixel_delay }
                        params_json = json.dumps(params_json)
                        await eval_js(f""" (() => {{ const params = {params_json}; const {{ intermediateX, targetX, duration, pixelDelay }} = params; var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForElement(callback) {{ var interval = setInterval(() => {{ var element = document.evaluate( '//div[contains(@class,"secsdk-captcha-drag-icon")]//*[name()="svg"] | ' + '//div[contains(@class, "cap")]/div[contains(@draggable, "true")]/button//*[name()="svg"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (element && element.offsetParent !== null && !element.disabled) {{ clearInterval(interval); callback(element); }} totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) {{ clearInterval(interval); }} }}, checkInterval); }} waitForElement((element) => {{ var rect = element.getBoundingClientRect(); var startX = rect.left + window.scrollX; var startY = rect.top + window.scrollY; function easeOutQuad(t) {{ return t * (2 - t); }} function moveElement(fromX, toX, callback) {{ var totalSteps = Math.abs(toX - fromX); var currentX = fromX; var step = 0; var interval = setInterval(() => {{ step++; var progress = step / totalSteps; var easedProgress = easeOutQuad(progress); currentX = fromX + (toX - fromX) * easedProgress; var randomYOffset = Math.sin(progress * Math.PI) * (Math.random() * 3); var dragEvent = new DragEvent('drag', {{ bubbles: true, cancelable: true, clientX: currentX, clientY: startY + randomYOffset }}); element.dispatchEvent(dragEvent); if (step >= totalSteps) {{ clearInterval(interval); callback(); }} }}, pixelDelay); }} var fakeStartX = startX + Math.random() * 5 - 2; var fakeStartY = startY + Math.random() * 5 - 2; var dragStartEvent = new DragEvent('dragstart', {{ bubbles: true, cancelable: true, clientX: fakeStartX, clientY: fakeStartY }}); element.dispatchEvent(dragStartEvent); setTimeout(() => {{ moveElement(fakeStartX, startX + intermediateX, () => {{ setTimeout(() => {{ moveElement(startX + intermediateX, startX + targetX, () => {{ var dropEvent = new DragEvent('drop', {{ bubbles: true, cancelable: true, clientX: startX + targetX, clientY: startY }}); element.dispatchEvent(dropEvent); var dragEndEvent = new DragEvent('dragend', {{ bubbles: true, cancelable: true, clientX: startX + targetX, clientY: startY }}); element.dispatchEvent(dragEndEvent); }}); }}, Math.random() * 100 + 50); }}); }}, Math.random() * 100 + 50); }}); }})(); """)
                        time.sleep(random.uniform(8, 10))
                    else:
                        await update_captcha_img_click[0].click()
                        time.sleep(random.uniform(8, 10))

                elif is_exist_captcha_slide:
                    get_captcha_data = await tab.xpath('//div[contains(@class, "verify") and count(img) = 2]/img[1] | ' + '//div[contains(@class, "cap") and count(img) = 2]/img[1] | ' + '//img[contains(@id, "verify")][1]')
                    img_el_image = get_captcha_data[0]
                    get_captcha_data = await safe_get_js_attributes(img_el_image)
                    full_img_url = get_captcha_data.get("src")
                    img_width = get_captcha_data.get("width", 0)
                    img_height = get_captcha_data.get("height", 0)
                    if "blob:" in full_img_url:
                        full_img = await get_captcha_image_nodriver(tab, full_img_url)
                    elif full_img_url.startswith("data:image"):
                        full_img = full_img_url.strip()
                    else: 
                        open_full_img_url = urllib.request.urlopen(full_img_url)
                        full_img_url_html_bytes = open_full_img_url.read()
                        full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                        full_img = full_screenshot_img_url_base64
                    get_captcha_data = await tab.xpath('//div[contains(@class, "verify") and count(img) = 2]/img[2] | ' + '//div[contains(@class, "cap") and count(img) = 2]/img[2] | ' + '//img[contains(@id, "verify")]/following-sibling::div[contains(@draggable, "true")]/img')
                    img_el = get_captcha_data[0]
                    get_captcha_data = await safe_get_js_attributes(img_el)
                    small_img_url = get_captcha_data.get("src")
                    if "blob:" in small_img_url:
                        small_img = await get_captcha_image_nodriver(tab, small_img_url)
                    elif small_img_url.startswith("data:image"):
                        small_img = small_img_url.strip()
                    else: 
                        open_small_img_url = urllib.request.urlopen(small_img_url)
                        small_img_url_html_bytes = open_small_img_url.read()
                        small_screenshot_img_url_base64 = base64.b64encode(small_img_url_html_bytes).decode('utf-8')
                        small_img = small_screenshot_img_url_base64
                    captcha_action_type = "tiktokSlide"
                    multipart_form_data = {
                        'FULL_IMG_CAPTCHA': (None, full_img),
                        'SMALL_IMG_CAPTCHA': (None, small_img),
                        'FULL_IMG_WIDTH': (None, img_width),
                        'FULL_IMG_HEIGHT': (None, img_height),
                        'ACTION': (None, captcha_action_type),
                        'USER_KEY': (None, user_api_key)
                    }
                    request_solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                    response_solve_captcha_content = request_solve_captcha.content
                    if isinstance(response_solve_captcha_content, bytes):
                        response_solve_captcha_content = response_solve_captcha_content.decode('utf-8')

                    if response_solve_captcha_content == "ERROR_USER_KEY":
                        raise Exception("Invalid API key / Make sure you using correct API key")
                    elif response_solve_captcha_content == "INVALID_ACTION":
                        raise Exception("Invalid action type / Supports: tiktokWhirl, tiktokSlide, tiktok3D, tiktokIcon")
                    elif response_solve_captcha_content == "ZERO_BALANCE":
                        raise Exception("Balance is zero / Top up your balance")

                    if response_solve_captcha_content.strip().startswith('{') and response_solve_captcha_content.strip().endswith('}'):
                        response_solve_captcha = request_solve_captcha.json()
                        response_coordinate_x = int(response_solve_captcha["coordinate_x"])
                        response_coordinate_y = int(response_solve_captcha["coordinate_y"])
                        random_move_left_right = random.randint(15, 50)
                        random_move_number = random.randint(1, 2)
                        if random_move_number == 1:
                            response_coordinate_x_random_move = int(response_coordinate_x) - int(random_move_left_right)
                        else:
                            response_coordinate_x_random_move = int(response_coordinate_x) + int(random_move_left_right)
                        time.sleep(random.uniform(0.1, 0.3))
                        pixel_delay = random.uniform(solve_captcha_speed / 300, solve_captcha_speed / 500)
                        params_json = { "intermediateX": response_coordinate_x_random_move, "targetX": response_coordinate_x, "duration": solve_captcha_speed, "pixelDelay": pixel_delay }
                        params_json = json.dumps(params_json)
                        await eval_js(f""" (() => {{ const params = {params_json}; const {{ intermediateX, targetX, duration, pixelDelay }} = params; var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForElement(callback) {{ var interval = setInterval(() => {{ var element = document.evaluate( '//div[contains(@class,"secsdk-captcha-drag-icon")]//*[name()="svg"] | ' + '//div[contains(@class, "cap")]/div[contains(@draggable, "true")]/button//*[name()="svg"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (element && element.offsetParent !== null && !element.disabled) {{ clearInterval(interval); callback(element); }} totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) {{ clearInterval(interval); }} }}, checkInterval); }} waitForElement((element) => {{ var rect = element.getBoundingClientRect(); var startX = rect.left + window.scrollX; var startY = rect.top + window.scrollY; function easeOutQuad(t) {{ return t * (2 - t); }} function moveElement(fromX, toX, callback) {{ var totalSteps = Math.abs(toX - fromX); var currentX = fromX; var step = 0; var interval = setInterval(() => {{ step++; var progress = step / totalSteps; var easedProgress = easeOutQuad(progress); currentX = fromX + (toX - fromX) * easedProgress; var randomYOffset = Math.sin(progress * Math.PI) * (Math.random() * 3); var dragEvent = new DragEvent('drag', {{ bubbles: true, cancelable: true, clientX: currentX, clientY: startY + randomYOffset }}); element.dispatchEvent(dragEvent); if (step >= totalSteps) {{ clearInterval(interval); callback(); }} }}, pixelDelay); }} var fakeStartX = startX + Math.random() * 5 - 2; var fakeStartY = startY + Math.random() * 5 - 2; var dragStartEvent = new DragEvent('dragstart', {{ bubbles: true, cancelable: true, clientX: fakeStartX, clientY: fakeStartY }}); element.dispatchEvent(dragStartEvent); setTimeout(() => {{ moveElement(fakeStartX, startX + intermediateX, () => {{ setTimeout(() => {{ moveElement(startX + intermediateX, startX + targetX, () => {{ var dropEvent = new DragEvent('drop', {{ bubbles: true, cancelable: true, clientX: startX + targetX, clientY: startY }}); element.dispatchEvent(dropEvent); var dragEndEvent = new DragEvent('dragend', {{ bubbles: true, cancelable: true, clientX: startX + targetX, clientY: startY }}); element.dispatchEvent(dragEndEvent); }}); }}, Math.random() * 100 + 50); }}); }}, Math.random() * 100 + 50); }}); }})(); """)
                        time.sleep(random.uniform(8, 10))
                    else:
                        await update_captcha_img_click[0].click()
                        time.sleep(random.uniform(8, 10))

                elif is_exist_captcha_icon:
                        get_captcha_data = await tab.xpath('//div[contains(@class,"verify") and count(img) = 1]/img[contains(@src,"icon")] | ' + '//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//' + 'img[(contains(@src,"blob") or contains(@src,"/icon_")) and ' + '//div[contains(@class,"cap")]//img/following-sibling::button and ' + '//div[contains(@class,"cap")]//span[contains(text(), "?")]]')
                        img_el_image = get_captcha_data[0]
                        get_captcha_data = await safe_get_js_attributes(img_el_image)
                        full_img_url = get_captcha_data.get("src")
                        img_width = get_captcha_data.get("width", 0)
                        img_height = get_captcha_data.get("height", 0)
                        coordinate_full_img_url_x = get_captcha_data.get("x", 0)
                        coordinate_full_img_url_y = get_captcha_data.get("y", 0)
                        get_question = await tab.xpath('//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//span')
                        get_question = await safe_get_text(get_question[0])
                        if "blob:" in full_img_url:
                            full_img = await get_captcha_image_nodriver(tab, full_img_url)
                        elif full_img_url.startswith("data:image"):
                            full_img = full_img_url.strip()
                        else: 
                            open_full_img_url = urllib.request.urlopen(full_img_url)
                            full_img_url_html_bytes = open_full_img_url.read()
                            full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                            full_img = full_screenshot_img_url_base64
                        captcha_action_type = "tiktokIcon"
                        multipart_form_data = {
                            'FULL_IMG_CAPTCHA': (None, full_img),
                            'CAPTCHA_QUESTION': (None, get_question),
                            'FULL_IMG_WIDTH': (None, img_width),
                            'FULL_IMG_HEIGHT': (None, img_height),
                            'ACTION': (None, captcha_action_type),
                            'USER_KEY': (None, user_api_key)
                        }   
                        request_solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                        response_solve_captcha_content = request_solve_captcha.content
                        if isinstance(response_solve_captcha_content, bytes):
                            response_solve_captcha_content = response_solve_captcha_content.decode('utf-8')
                        if response_solve_captcha_content == "ERROR_USER_KEY":
                            raise Exception("Invalid API key / Make sure you using correct API key")
                        elif response_solve_captcha_content == "INVALID_ACTION":
                            raise Exception("Invalid action type / Supports: tiktokWhirl, tiktokSlide, tiktok3D, tiktokIcon")
                        elif response_solve_captcha_content == "ZERO_BALANCE":
                            raise Exception("Balance is zero / Top up your balance")
                        if response_solve_captcha_content.strip().startswith('{') and response_solve_captcha_content.strip().endswith('}'):
                            json_solve_captcha_data = request_solve_captcha.json()
                            coordinates = [(f"coordinate_x{i}", f"coordinate_y{i}") for i in range(1, len(json_solve_captcha_data) // 2 + 1)]
                            target_coordinates = []
                            for x_key, y_key in coordinates:
                                coordinate_x = int(json_solve_captcha_data[x_key])
                                coordinate_y = int(json_solve_captcha_data[y_key])
                                random_move_number = random.randint(1, 2)
                                random_click_coordinates = random.randint(0, 5)
                                if random_move_number == 1:
                                    target_coordinate_x = coordinate_x + coordinate_full_img_url_x - random_click_coordinates
                                    target_coordinate_y = coordinate_y + coordinate_full_img_url_y - random_click_coordinates
                                else:
                                    target_coordinate_x = coordinate_x + coordinate_full_img_url_x + random_click_coordinates
                                    target_coordinate_y = coordinate_y + coordinate_full_img_url_y + random_click_coordinates
                                target_coordinates.append((target_coordinate_x, target_coordinate_y))
                            for target_coordinate_x, target_coordinate_y in target_coordinates:
                                await eval_js(f""" (() => {{ const params = {params_json}; const {{ targetX, targetY }} = params; var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function easeOutQuad(t) {{ return t * (2 - t); }} function waitForElement(xpath, callback) {{ var interval = setInterval(() => {{ var element = document.evaluate( xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (element && element.offsetParent !== null) {{ if (element.tagName.toLowerCase() === 'img') {{ if (element.complete && element.naturalHeight > 0) {{ clearInterval(interval); callback(element); }} }} else {{ clearInterval(interval); callback(element); }} }} totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) {{ clearInterval(interval); }} }}, checkInterval); }} function smoothMoveAndClick(targetX, targetY, element) {{ var startX = window.innerWidth * Math.random(); var startY = window.innerHeight * Math.random(); var steps = Math.floor(10 + Math.random() * 10); var currentX = startX; var currentY = startY; var moveInterval = setInterval(() => {{ steps--; var progress = 1 - steps / 10; var easedProgress = easeOutQuad(progress); currentX = startX + (targetX - startX) * easedProgress; currentY = startY + (targetY - startY) * easedProgress; var moveEvent = new MouseEvent('mousemove', {{ bubbles: true, cancelable: true, clientX: currentX, clientY: currentY }}); document.dispatchEvent(moveEvent); if (steps <= 0) {{ clearInterval(moveInterval); setTimeout(() => {{ var mouseDownEvent = new MouseEvent('mousedown', {{ bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }}); element.dispatchEvent(mouseDownEvent); setTimeout(() => {{ var mouseUpEvent = new MouseEvent('mouseup', {{ bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }}); element.dispatchEvent(mouseUpEvent); var clickEvent = new MouseEvent('click', {{ bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }}); element.dispatchEvent(clickEvent); }}, Math.random() * 100 + 50); }}, Math.random() * 100 + 50); }} }}, Math.random() * 20 + 10); }} // XPath: находим иконку или blob в капче var targetXpath = '//div[contains(@class,"verify") and count(img) = 1]/img[contains(@src,"icon")] | ' + '//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//' + 'img[(contains(@src,"blob") or contains(@src,"/icon_")) and ' + '//div[contains(@class,"cap")]//img/following-sibling::button and ' + '//div[contains(@class,"cap")]//span[contains(text(), "?")]]'; waitForElement(targetXpath, (element) => {{ var rect = element.getBoundingClientRect(); var adjustedX = rect.left + window.scrollX + rect.width / 2; var adjustedY = rect.top + window.scrollY + rect.height / 2; smoothMoveAndClick(targetX, targetY, element); }}); }})(); """)
                                time.sleep(random.uniform(solve_captcha_speed / 1000 / 5, solve_captcha_speed / 1000 / 10))                               
                            time.sleep(random.uniform(solve_captcha_speed / 1000 / 3, solve_captcha_speed / 1000 / 5))                          
                            await eval_js(""" (() => { var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForElementAndClick() { var interval = setInterval(() => { var submitButton = document.evaluate( '//div[contains(@class,"verify-captcha-submit-button")] | ' + '//div[contains(@class,"cap")]//img/following-sibling::button[contains(@aria-disabled,"false")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (submitButton && submitButton.offsetParent !== null && !submitButton.disabled) { clearInterval(interval); var clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true }); submitButton.dispatchEvent(clickEvent); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); } }, checkInterval); } waitForElementAndClick(); })(); """)
                            time.sleep(random.uniform(8, 10))
                        else:
                            await update_captcha_img_click[0].click()
                            time.sleep(random.uniform(8, 10))
                                                                         
                elif is_exist_captcha_3d:
                    get_captcha_data = await tab.xpath('//div[contains(@class,"verify") and count(img) = 1] | ' + '//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//img[contains(@src,"/3d_") or contains(@src,"blob")]')
                    img_el_image = get_captcha_data[0]
                    get_captcha_data = await safe_get_js_attributes(img_el_image)
                    full_img_url = get_captcha_data.get("src")
                    img_width = get_captcha_data.get("width", 0)
                    img_height = get_captcha_data.get("height", 0)
                    coordinate_full_img_url_x = get_captcha_data.get("x", 0)
                    coordinate_full_img_url_y = get_captcha_data.get("y", 0)
                    if "blob:" in full_img_url:
                        full_img = get_captcha_image_nodriver(page, full_img_url)
                    elif full_img_url.startswith("data:image"):
                        full_img = full_img_url.strip()
                    else: 
                        open_full_img_url = urllib.request.urlopen(full_img_url)
                        full_img_url_html_bytes = open_full_img_url.read()
                        full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                        full_img = full_screenshot_img_url_base64
                    captcha_action_type = "tiktok3D"
                    multipart_form_data = {
                        'FULL_IMG_CAPTCHA': (None, full_img),
                        'FULL_IMG_WIDTH': (None, img_width),
                        'FULL_IMG_HEIGHT': (None, img_height),
                        'ACTION': (None, captcha_action_type),
                        'USER_KEY': (None, user_api_key)
                    }   
                    request_solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                    response_solve_captcha_content = request_solve_captcha.content
                    if isinstance(response_solve_captcha_content, bytes):
                        response_solve_captcha_content = response_solve_captcha_content.decode('utf-8')
                    if response_solve_captcha_content == "ERROR_USER_KEY":
                        raise Exception("Invalid API key / Make sure you using correct API key")
                    elif response_solve_captcha_content == "INVALID_ACTION":
                        raise Exception("Invalid action type / Supports: tiktokWhirl, tiktokSlide, tiktok3D, tiktokIcon")
                    elif response_solve_captcha_content == "ZERO_BALANCE":
                        raise Exception("Balance is zero / Top up your balance")
                    if response_solve_captcha_content.strip().startswith('{') and response_solve_captcha_content.strip().endswith('}'):
                        json_solve_captcha_data = request_solve_captcha.json()
                        coordinates = [(f"coordinate_x{i}", f"coordinate_y{i}") for i in range(1, len(json_solve_captcha_data) // 2 + 1)]
                        target_coordinates = []
                        for x_key, y_key in coordinates:
                            coordinate_x = int(json_solve_captcha_data[x_key])
                            coordinate_y = int(json_solve_captcha_data[y_key])
                            random_move_number = random.randint(1, 2)
                            random_click_coordinates = random.randint(0, 5)
                            if random_move_number == 1:
                                target_coordinate_x = coordinate_x + coordinate_full_img_url_x - random_click_coordinates
                                target_coordinate_y = coordinate_y + coordinate_full_img_url_y - random_click_coordinates
                            else:
                                target_coordinate_x = coordinate_x + coordinate_full_img_url_x + random_click_coordinates
                                target_coordinate_y = coordinate_y + coordinate_full_img_url_y + random_click_coordinates
                            target_coordinates.append((target_coordinate_x, target_coordinate_y))
                        for target_coordinate_x, target_coordinate_y in target_coordinates:
                            params = { "targetX": target_coordinate_x, "targetY": target_coordinate_y }
                            params_json = json.dumps(params)
                            await eval_js(f""" (() => {{ const params = {params_json}; const {{ targetX, targetY }} = params; var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function easeOutQuad(t) {{ return t * (2 - t); }} function waitForElement(xpath, callback) {{ var interval = setInterval(() => {{ var element = document.evaluate( xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (element && element.offsetParent !== null) {{ if (element.tagName.toLowerCase() === 'img') {{ if (element.complete && element.naturalHeight > 0) {{ clearInterval(interval); callback(element); }} }} else {{ clearInterval(interval); callback(element); }} }} totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) {{ clearInterval(interval); }} }}, checkInterval); }} function smoothMoveAndClick(targetX, targetY, element) {{ var startX = window.innerWidth * Math.random(); var startY = window.innerHeight * Math.random(); var steps = Math.floor(10 + Math.random() * 10); var currentX = startX; var currentY = startY; var moveInterval = setInterval(() => {{ steps--; var progress = 1 - steps / 10; var easedProgress = easeOutQuad(progress); currentX = startX + (targetX - startX) * easedProgress; currentY = startY + (targetY - startY) * easedProgress; var moveEvent = new MouseEvent('mousemove', {{ bubbles: true, cancelable: true, clientX: currentX, clientY: currentY }}); document.dispatchEvent(moveEvent); if (steps <= 0) {{ clearInterval(moveInterval); setTimeout(() => {{ var mouseDownEvent = new MouseEvent('mousedown', {{ bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }}); element.dispatchEvent(mouseDownEvent); setTimeout(() => {{ var mouseUpEvent = new MouseEvent('mouseup', {{ bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }}); element.dispatchEvent(mouseUpEvent); var clickEvent = new MouseEvent('click', {{ bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }}); element.dispatchEvent(clickEvent); }}, Math.random() * 100 + 50); }}, Math.random() * 100 + 50); }} }}, Math.random() * 20 + 10); }} var targetXpath = '//div[contains(@class,"verify") and count(img) = 1] | ' + '//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//' + 'img[contains(@src,"/3d_") or contains(@src,"blob")]'; waitForElement(targetXpath, (element) => {{ var rect = element.getBoundingClientRect(); var adjustedX = rect.left + window.scrollX + rect.width / 2; var adjustedY = rect.top + window.scrollY + rect.height / 2; smoothMoveAndClick(targetX, targetY, element); }}); }})(); """)
                            time.sleep(random.uniform(solve_captcha_speed / 1000 / 5, solve_captcha_speed / 1000 / 10))                                  
                        time.sleep(random.uniform(solve_captcha_speed / 1000 / 3, solve_captcha_speed / 1000 / 5))                                 
                        await eval_js(""" (() => { var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForElementAndClick() { var interval = setInterval(() => { var submitButton = document.evaluate( '//div[contains(@class,"verify-captcha-submit-button")] | ' + '//div[contains(@class,"cap")]//img/following-sibling::button[contains(@aria-disabled,"false")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (submitButton && submitButton.offsetParent !== null && !submitButton.disabled) { clearInterval(interval); var clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true }); submitButton.dispatchEvent(clickEvent); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); } }, checkInterval); } waitForElementAndClick(); })(); """)                    
                        time.sleep(random.uniform(8, 10))
                    else:
                        await update_captcha_img_click[0].click()
                        time.sleep(random.uniform(8, 10))
                            
        except Exception as e:
            print(f"Error: {e}")
    elif action_type == "datadomeaudio" or action_type == "datadomeimage":
        try:        
            start_time = time.time()
            while time.time() - start_time < wait_captcha_seconds:
                wait_is_exist_capctha = eval_js("""() => {
                    var elements = document.evaluate('//html[1]/body[1]//iframe[1][contains(@src,"https://geo.captcha-delivery.com")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
                    return elements.snapshotLength > 0;
                }""")
                if wait_is_exist_capctha:
                    break
                time.sleep(1)

            for i in range(0, number_captcha_attempts):
                is_exist_captcha_slide = eval_js("""() => {
                    var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (iframe) {
                        var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                        return iframeDoc.evaluate('//div[contains(@id,"captcha__puzzle")]', iframeDoc, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null).snapshotLength > 0;
                    }
                    return false;
                }""")
                is_exist_captcha_audio = eval_js("""() => {
                    var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (iframe) {
                        var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                        return iframeDoc.evaluate('//button[contains(@class,"audio-captcha-play-button")]', iframeDoc, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null).snapshotLength > 0;
                    }
                    return false;
                }""")
                if not (is_exist_captcha_slide or is_exist_captcha_audio):
                    break
                else:
                    if (selected_captcha_type == 'audio'):
                        select_capctha_slide_click = """() => {
                            var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            if (iframe) {
                                var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                                var btn = iframeDoc.evaluate('//div[contains(@id,"switch")]//button[contains(@id,"puzzle")][contains(@class,"captcha-toggle")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                if (btn) { btn.click(); return true; }
                            }
                            return false;
                        }"""
                        eval_js(select_capctha_slide_click)
                        time.sleep(random.uniform(1, 3))
                    else:
                        select_capctha_audio_click = """() => {
                            var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            if (iframe) {
                                var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                                var btn = iframeDoc.evaluate('//div[contains(@id,"switch")]//button[contains(@id,"audio")][contains(@class,"captcha-toggle")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                if (btn) { btn.click(); return true; }
                            }
                            return false;
                        }"""
                        eval_js(select_capctha_audio_click)

                    update_captcha_img_click_iframe = """() => {
                        var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        var button = null;
                        if (iframe) {
                            var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                            button = iframeDoc.evaluate('//button[contains(@id,"reload")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        }
                        if (!button) {
                            button = document.evaluate('//button[contains(@id,"reload")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        }
                        if (button) { button.click(); return true; } return false;
                    }"""

                    if is_exist_captcha_slide:
                        get_captcha_data = eval_js("""() => {
                            var iframe = document.evaluate('//html[1]//body[1]//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            if (iframe) {
                                var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                                var linkElement = iframeDoc.evaluate('//html//link[contains(@rel,"preload")][1]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                var href = linkElement ? linkElement.getAttribute('href') : null;
                                var puzzleElement = iframeDoc.evaluate('//div[contains(@id,"captcha__puzzle")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                var width = puzzleElement ? puzzleElement.offsetWidth : null;
                                var height = puzzleElement ? puzzleElement.offsetHeight : null;
                                return { url: href, width: width, height: height };
                            }
                            return null;
                        }""")
                        full_img_url = get_captcha_data['url'].strip()
                        img_width = round(get_captcha_data['width'])
                        img_height = round(get_captcha_data['height'])
                        if "blob:" in full_img_url:
                            full_img = get_captcha_image_nodriver(tab, full_img_url)
                        elif full_img_url.startswith("data:image"):
                            full_img = full_img_url.strip()
                        else: 
                            open_full_img_url = urllib.request.urlopen(full_img_url)
                            full_img_url_html_bytes = open_full_img_url.read()
                            full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                            full_img = full_screenshot_img_url_base64

                        small_img_url = eval_js("""() => {
                            var iframe = document.evaluate('//html[1]//body[1]//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            if (iframe) {
                                var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                                var elements = iframeDoc.evaluate('//html//link[contains(@rel,"preload")][2]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                                var linkElement = elements.singleNodeValue;
                                if (linkElement) { return linkElement.getAttribute('href'); }
                            }
                            return null;
                        }""")
                        if "blob:" in small_img_url:
                            small_img = get_captcha_image_nodriver(tab, small_img_url)
                        elif small_img_url.startswith("data:image"):
                            small_img = small_img_url.strip()
                        else: 
                            open_small_img_url = urllib.request.urlopen(small_img_url)
                            small_img_url_html_bytes = open_small_img_url.read()
                            small_screenshot_img_url_base64 = base64.b64encode(small_img_url_html_bytes).decode('utf-8')
                            small_img = small_screenshot_img_url_base64

                        captcha_action_type = "dataDomeImage"
                        multipart_form_data = {
                            'FULL_IMG_CAPTCHA': (None, full_img),
                            'SMALL_IMG_CAPTCHA': (None, small_img),
                            'FULL_IMG_WIDTH': (None, img_width),
                            'FULL_IMG_HEIGHT': (None, img_height),
                            'ACTION': (None, captcha_action_type),
                            'USER_KEY': (None, user_api_key)
                        }
                        request_solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                        response_solve_captcha_content = request_solve_captcha.content
                        if isinstance(response_solve_captcha_content, bytes):
                            response_solve_captcha_content = response_solve_captcha_content.decode('utf-8')

                        if response_solve_captcha_content == "ERROR_USER_KEY":
                            raise Exception("Invalid API key / Make sure you using correct API key")
                        elif response_solve_captcha_content == "INVALID_ACTION":
                            raise Exception("Invalid action type / Supports: dataDomeAudio, dataDomeImage")
                        elif response_solve_captcha_content == "ZERO_BALANCE":
                            raise Exception("Balance is zero / Top up your balance")

                        if response_solve_captcha_content.strip().startswith('{') and response_solve_captcha_content.strip().endswith('}'):
                            response_solve_captcha = request_solve_captcha.json()
                            response_coordinate_x = int(response_solve_captcha["coordinate_x"])
                            response_coordinate_y = int(response_solve_captcha["coordinate_y"])
                            random_move_left_right = random.randint(15, 50)
                            random_move_number = random.randint(1, 2)
                            if random_move_number == 1:
                                response_coordinate_x_random_move = int(response_coordinate_x) - int(random_move_left_right)
                            else:
                                response_coordinate_x_random_move = int(response_coordinate_x) + int(random_move_left_right)
                            time.sleep(random.uniform(0.1, 0.3))

                            pixel_delay_val = random.uniform(solve_captcha_speed / 500, solve_captcha_speed / 300)
                            drag_js_iframe = """
                            ({ intermediateX, targetX, duration, pixelDelay }) => {
                                var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0;
                                var iframe = document.evaluate("//html[1]//body[1]//iframe[1]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                if (iframe) {
                                    var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                                    function waitForElement(callback) {
                                        var interval = setInterval(() => {
                                            var element = iframeDoc.evaluate('//div[contains(@class,"sliderContainer")]//i[contains(@class,"sliderIcon")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                            if (element && element.offsetParent !== null && !element.disabled) { clearInterval(interval); callback(element); }
                                            totalTimeWaited += checkInterval;
                                            if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); }
                                        }, checkInterval);
                                    }
                                    waitForElement((element) => {
                                        var rect = element.getBoundingClientRect();
                                        var startX = rect.left;
                                        var startY = rect.top;
                                        function moveElement(fromX, toX, callback) {
                                            var steps = Math.max(1, Math.abs(Math.round(toX - fromX)));
                                            var stepSize = (toX - fromX) / steps;
                                            var currentX = fromX;
                                            var interval = setInterval(() => {
                                                currentX += stepSize;
                                                var dragEvent = new DragEvent('drag', { bubbles: true, cancelable: true, clientX: currentX, clientY: startY });
                                                element.dispatchEvent(dragEvent);
                                                if ((stepSize > 0 && currentX >= toX) || (stepSize < 0 && currentX <= toX)) { clearInterval(interval); callback(); }
                                            }, pixelDelay);
                                        }
                                        var dragStartEvent = new DragEvent('dragstart', { bubbles: true, cancelable: true, clientX: startX, clientY: startY });
                                        element.dispatchEvent(dragStartEvent);
                                        moveElement(startX, startX + intermediateX, () => {
                                            moveElement(startX + intermediateX, startX + targetX, () => {
                                                var dropEvent = new DragEvent('drop', { bubbles: true, cancelable: true, clientX: startX + targetX, clientY: startY });
                                                element.dispatchEvent(dropEvent);
                                                var dragEndEvent = new DragEvent('dragend', { bubbles: true, cancelable: true, clientX: startX + targetX, clientY: startY });
                                                element.dispatchEvent(dragEndEvent);
                                            });
                                        });
                                    });
                                }
                            }
                            """
                            eval_js(drag_js_iframe, {
                                "intermediateX": response_coordinate_x_random_move,
                                "targetX": response_coordinate_x,
                                "duration": solve_captcha_speed,
                                "pixelDelay": pixel_delay_val
                            })
                            time.sleep(random.uniform(8, 10))
                        else:
                            eval_js(update_captcha_img_click_iframe)
                            time.sleep(random.uniform(8, 10))

                    elif is_exist_captcha_audio:
                        get_captcha_data = eval_js("""() => {
                            var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0;
                            function waitForCaptchaAudioSrc() {
                                return new Promise((resolve, reject) => {
                                    var interval = setInterval(() => {
                                        var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                        if (iframe) {
                                            var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                                            var audioButton = iframeDoc.evaluate('//button[contains(@class,"audio-captcha-play-button")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                            if (audioButton) { clearInterval(interval); resolve(audioButton.getAttribute("src")); }
                                        }
                                        totalTimeWaited += checkInterval;
                                        if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); reject("Audio captcha button not found after 10 seconds."); }
                                    }, checkInterval);
                                });
                            }
                            return waitForCaptchaAudioSrc();
                        }""")
                        get_audio_url = get_captcha_data['url'].strip()
                        if get_audio_url and "/en/" not in get_audio_url:
                            get_audio_url = re.sub(r"/[a-z]{2}/", "/en/", get_audio_url)
                        if "blob:" in get_audio_url:
                            audio_data = get_captcha_image_nodriver(tab, get_audio_url)
                        elif audio_url.startswith("data:image"):
                            audio_data = audio_url.strip()
                        else: 
                            open_audio_url = urllib.request.urlopen(get_audio_url)
                            audio_url_html_bytes = open_audio_url.read()
                            audio_data = base64.b64encode(audio_url_html_bytes).decode('utf-8')

                        click_play_js = """() => {
                            var iframe = document.evaluate('//html[1]//body[1]//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            var button = null;
                            if (iframe) {
                                var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                                button = iframeDoc.evaluate('//button[contains(@class,"audio-captcha-play-button")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            }
                            if (!button) {
                                button = document.evaluate('//button[contains(@class,"audio-captcha-play-button")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            }
                            if (button) {
                                var rect = button.getBoundingClientRect();
                                var x = rect.left + 1;
                                var y = rect.top + 1;
                                var mouseDownEvent = new MouseEvent('mousedown', { bubbles: true, cancelable: true, view: window, button: 0, clientX: x, clientY: y });
                                button.dispatchEvent(mouseDownEvent);
                                var mouseUpEvent = new MouseEvent('mouseup', { bubbles: true, cancelable: true, view: window, button: 0, clientX: x, clientY: y });
                                button.dispatchEvent(mouseUpEvent);
                                var clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true, view: window, button: 0, clientX: x, clientY: y });
                                button.dispatchEvent(clickEvent);
                                return true;
                            }
                            return false;
                        }"""
                        eval_js(click_play_js)
                        captcha_action_type = "dataDomeAudio"
                        multipart_form_data = {
                            'AUDIO_CAPTCHA': (None, audio_data),
                            'ACTION': (None, captcha_action_type),
                            'USER_KEY': (None, user_api_key)
                        }
                        request_solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                        response_solve_captcha_content = request_solve_captcha.content
                        if isinstance(response_solve_captcha_content, bytes):
                            response_solve_captcha_content = response_solve_captcha_content.decode('utf-8')

                        if response_solve_captcha_content == "ERROR_USER_KEY":
                            raise Exception("Invalid API key / Make sure you using correct API key")
                        elif response_solve_captcha_content == "INVALID_ACTION":
                            raise Exception("Invalid action type / Supports: dataDomeAudio, dataDomeImage")
                        elif response_solve_captcha_content == "ZERO_BALANCE":
                            raise Exception("Balance is zero / Top up your balance")

                        if response_solve_captcha_content.strip().startswith('{') and response_solve_captcha_content.strip().endswith('}'):
                            response_solve_captcha = request_solve_captcha.json()
                            response_code = int(response_solve_captcha["response_code"])
                            fill_input_js = """({ responseCode }) => {
                                var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                if (iframe) {
                                    var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                                    var inputField = iframeDoc.evaluate('//div[contains(@class,"audio-captcha-input-container")]/input[contains(@class,"audio-captcha-input")][1]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                    if (inputField) {
                                        inputField.value = responseCode;
                                        inputField.dispatchEvent(new Event('input', { bubbles: true }));
                                        return true;
                                    }
                                }
                                return false;
                            }"""
                            eval_js(fill_input_js, {"responseCode": response_code})
                            time.sleep(random.uniform(8, 10))
                        else:
                            eval_js(update_captcha_img_click_iframe)
                            time.sleep(random.uniform(8, 10))
        except Exception as e:
            print(f"Error: {e}")
    elif action_type == "geetesticon":
        try:
            start_time = time.time()
            while time.time() - start_time < wait_captcha_seconds:
                wait_is_exist_capctha = eval_js("""() => {
                    var elements = document.evaluate('//div[contains(@class,"geetest_box_wrap")]/div[contains(@class,"geetest_box")]/div[contains(@class,"geetest_container")]/div[contains(@class,"geetest_wrap")]/div[contains(@class,"geetest_subitem")]/div[contains(@class,"geetest_window")]/div[contains(@class,"geetest_bg")] | //div[contains(@class,"geetest_close") or contains(@class,"geetest_nextReady")]//div[contains(@class,"geetest_btn_click")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
                    return elements.snapshotLength > 0;
                }""")
                if wait_is_exist_capctha:
                    break
                time.sleep(1)

            is_exist_capctha_success = eval_js("""() => {
                var elements = document.evaluate('//div[contains(@class,"geetest_lock_success")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
                return elements.snapshotLength > 0;
            }""")
            if not is_exist_capctha_success:
                open_captcha_button_click = """() => {
                    var element = document.evaluate('//div[contains(@class,"geetest_btn_click")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (element) { element.click(); return true; } return false;
                }"""
                eval_js(open_captcha_button_click)

                while time.time() - start_time < wait_captcha_seconds:
                    wait_is_exist_capctha = eval_js("""() => {
                        var elements = document.evaluate('//div[contains(@class,"geetest_box_wrap")]/div[contains(@class,"geetest_box")]/div[contains(@class,"geetest_container")]/div[contains(@class,"geetest_wrap")]/div[contains(@class,"geetest_subitem")]/div[contains(@class,"geetest_window")]/div[contains(@class,"geetest_bg")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
                        return elements.snapshotLength > 0;
                    }""")
                    if wait_is_exist_capctha:
                        break
                    time.sleep(1)
                time.sleep(1)

            for i in range(0, number_captcha_attempts):
                is_exist_capctha_icon = eval_js("""() => {
                    var elements = document.evaluate('//div[contains(@class,"geetest_box_wrap")]/div[contains(@class,"geetest_box")]/div[contains(@class,"geetest_container")]/div[contains(@class,"geetest_wrap")]/div[contains(@class,"geetest_subitem")]/div[contains(@class,"geetest_window")]/div[contains(@class,"geetest_bg")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
                    return elements.snapshotLength > 0;
                }""")
                if not is_exist_capctha_icon:
                    break
                else:
                    update_captcha_img_click = """() => {
                        var element = document.evaluate('//button[contains(@class,"geetest_refresh")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (element) { element.click(); return true; } return false;
                    }"""
                    get_captcha_data = eval_js("""() => {
                        var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0;
                        function waitForCaptchaElement() {
                            return new Promise((resolve, reject) => {
                                var interval = setInterval(() => {
                                    var imgElement = document.evaluate('//div[contains(@class,"geetest_box_wrap")]/div[contains(@class,"geetest_box")]/div[contains(@class,"geetest_container")]/div[contains(@class,"geetest_wrap")]/div[contains(@class,"geetest_subitem")]/div[contains(@class,"geetest_window")]/div[contains(@class,"geetest_bg")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                    if (imgElement) {
                                        clearInterval(interval);
                                        var imgRect = imgElement.getBoundingClientRect();
                                        resolve({ width: imgRect.width, height: imgRect.height, x: imgRect.left + window.scrollX, y: imgRect.top + window.scrollY, url: imgElement.getAttribute("style") });
                                    }
                                    totalTimeWaited += checkInterval;
                                    if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); reject("Captcha element not found or not visible within 10 seconds."); }
                                }, checkInterval);
                            });
                        }
                        return waitForCaptchaElement();
                    }""")
                    img_width = round(get_captcha_data['width'])
                    img_height = round(get_captcha_data['height'])
                    coordinate_full_img_url_x = round(get_captcha_data['x'])
                    coordinate_full_img_url_y = round(get_captcha_data['y'])
                    full_img_url = get_captcha_data['url']
                    start = full_img_url.find('url("') + len('url("')
                    end = full_img_url.find('")', start)
                    full_img_url = full_img_url[start:end]
                    if "blob:" in full_img_url:
                        full_img = get_captcha_image_nodriver(tab, full_img_url)
                    elif full_img_url.startswith("data:image"):
                        full_img = full_img_url.strip()
                    else: 
                        open_full_img_url = urllib.request.urlopen(full_img_url)
                        full_img_url_html_bytes = open_full_img_url.read()
                        full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                        full_img = full_screenshot_img_url_base64

                    captcha_action_type = "geeTestIcon"
                    multipart_form_data = {
                        'FULL_IMG_CAPTCHA': (None, full_img),
                        'FULL_IMG_WIDTH': (None, img_width),
                        'FULL_IMG_HEIGHT': (None, img_height),
                        'ACTION': (None, captcha_action_type),
                        'USER_KEY': (None, user_api_key)
                    }
                    request_solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                    response_solve_captcha_content = request_solve_captcha.content
                    if isinstance(response_solve_captcha_content, bytes):
                        response_solve_captcha_content = response_solve_captcha_content.decode('utf-8')

                    if response_solve_captcha_content == "ERROR_USER_KEY":
                        raise Exception("Invalid API key / Make sure you using correct API key")
                    elif response_solve_captcha_content == "INVALID_ACTION":
                        raise Exception("Invalid action type / Supports: geeTestIcon")
                    elif response_solve_captcha_content == "ZERO_BALANCE":
                        raise Exception("Balance is zero / Top up your balance")

                    if response_solve_captcha_content.strip().startswith('{') and response_solve_captcha_content.strip().endswith('}'):
                        json_solve_captcha_data = request_solve_captcha.json()
                        coordinates = [(f"coordinate_x{i}", f"coordinate_y{i}") for i in range(1, len(json_solve_captcha_data) // 2 + 1)]
                        target_coordinates = []
                        for x_key, y_key in coordinates:
                            coordinate_x = int(json_solve_captcha_data[x_key])
                            coordinate_y = int(json_solve_captcha_data[y_key])
                            random_move_number = random.randint(1, 2)
                            random_click_coordinates = random.randint(0, 5)
                            if random_move_number == 1:
                                target_coordinate_x = coordinate_x + coordinate_full_img_url_x - random_click_coordinates
                                target_coordinate_y = coordinate_y + coordinate_full_img_url_y - random_click_coordinates
                            else:
                                target_coordinate_x = coordinate_x + coordinate_full_img_url_x + random_click_coordinates
                                target_coordinate_y = coordinate_y + coordinate_full_img_url_y + random_click_coordinates
                            target_coordinates.append((target_coordinate_x, target_coordinate_y))

                        click_js = """
                        ({ targetX, targetY }) => {
                            var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0;
                            function easeOutQuad(t) { return t * (2 - t); }
                            function waitForElement(xpath, callback) {
                                var interval = setInterval(() => {
                                    var element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                    if (element && element.offsetParent !== null) { clearInterval(interval); callback(element); }
                                    totalTimeWaited += checkInterval;
                                    if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); }
                                }, checkInterval);
                            }
                            function smoothMoveAndClick(targetX, targetY, element) {
                                var startX = Math.random() * window.innerWidth;
                                var startY = Math.random() * window.innerHeight;
                                var steps = Math.floor(30 + Math.random() * 20);
                                var currentX = startX;
                                var currentY = startY;
                                var moveInterval = setInterval(() => {
                                    steps--;
                                    var progress = 1 - steps / 30;
                                    var easedProgress = easeOutQuad(progress);
                                    currentX = startX + (targetX - startX) * easedProgress;
                                    currentY = startY + (targetY - startY) * easedProgress;
                                    var moveEvents = [
                                        new MouseEvent('mousemove', { bubbles: true, cancelable: true, clientX: currentX, clientY: currentY }),
                                        new PointerEvent('pointermove', { bubbles: true, cancelable: true, clientX: currentX, clientY: currentY }),
                                        new MouseEvent('mouseover', { bubbles: true, cancelable: true, clientX: currentX, clientY: currentY }),
                                        new MouseEvent('mouseenter', { bubbles: true, cancelable: true, clientX: currentX, clientY: currentY })
                                    ];
                                    moveEvents.forEach(evt => { document.dispatchEvent(evt); element.dispatchEvent(evt); });
                                    if (steps <= 0) {
                                        clearInterval(moveInterval);
                                        setTimeout(() => {
                                            var pointerDownEvent = new PointerEvent('pointerdown', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY });
                                            var mouseDownEvent = new MouseEvent('mousedown', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY });
                                            element.dispatchEvent(pointerDownEvent); document.dispatchEvent(pointerDownEvent);
                                            element.dispatchEvent(mouseDownEvent); document.dispatchEvent(mouseDownEvent);
                                            setTimeout(() => {
                                                var pointerUpEvent = new PointerEvent('pointerup', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY });
                                                var mouseUpEvent = new MouseEvent('mouseup', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY });
                                                var clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY });
                                                element.dispatchEvent(pointerUpEvent); document.dispatchEvent(pointerUpEvent);
                                                element.dispatchEvent(mouseUpEvent); document.dispatchEvent(mouseUpEvent);
                                                element.dispatchEvent(clickEvent); document.dispatchEvent(clickEvent);
                                            }, Math.random() * 150 + 50);
                                        }, Math.random() * 150 + 50);
                                    }
                                }, Math.random() * 30 + 10);
                            }
                            var targetXpath = '//div[contains(@class,"geetest_box_wrap")]/div[contains(@class,"geetest_box")]/div[contains(@class,"geetest_container")]/div[contains(@class,"geetest_wrap")]/div[contains(@class,"geetest_subitem")]/div[contains(@class,"geetest_window")]/div[contains(@class,"geetest_bg")]';
                            waitForElement(targetXpath, (element) => {
                                var rect = element.getBoundingClientRect();
                                var adjustedX = rect.left + window.scrollX + rect.width / 2;
                                var adjustedY = rect.top + window.scrollY + rect.height / 2;
                                if (window.getComputedStyle(element).display !== 'none' && window.getComputedStyle(element).visibility !== 'hidden' && element.offsetWidth > 0 && element.offsetHeight > 0) {
                                    smoothMoveAndClick(targetX, targetY, element);
                                }
                            });
                        }
                        """
                        for target_coordinate_x, target_coordinate_y in target_coordinates:
                            eval_js(click_js, {"targetX": target_coordinate_x, "targetY": target_coordinate_y})
                            time.sleep(random.uniform(solve_captcha_speed / 1000 / 5, solve_captcha_speed / 1000 / 10))

                        time.sleep(random.uniform(solve_captcha_speed / 1000 / 3, solve_captcha_speed / 1000 / 5))

                        eval_js("""() => {
                            var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0;
                            function waitForElementAndClick() {
                                var interval = setInterval(() => {
                                    var submitButton = document.evaluate('//div[contains(@class,"geetest_box_wrap")]/div[contains(@class,"geetest_box")]/div[contains(@class,"geetest_container")]/div[contains(@class,"geetest_wrap")]/div[contains(@class,"geetest_subitem")]/div[contains(@class,"geetest_submit")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                    if (submitButton && submitButton.offsetParent !== null && !submitButton.disabled) {
                                        clearInterval(interval);
                                        var clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true });
                                        submitButton.dispatchEvent(clickEvent);
                                    }
                                    totalTimeWaited += checkInterval;
                                    if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); }
                                }, checkInterval);
                            }
                            waitForElementAndClick();
                        }""")
                        time.sleep(random.uniform(8, 10))
                    else:
                        eval_js(update_captcha_img_click)
                        time.sleep(random.uniform(8, 10))

        except Exception as e:
            print(f"Error: {e}")
    else:
        ("Invalid action type / Supports: tiktokWhirl, tiktokSlide, tiktok3D, tiktokIcon, dataDomeAudio, dataDomeImage, geeTestIcon")