import requests
import urllib.request
import base64
import random
import time
import re
import json

def solve_captcha_selenium(driver, user_api_key, action_type, number_captcha_attempts, wait_captcha_seconds, solve_captcha_speed, *args):
    if len(args) > 0:
        selected_captcha_type = args[0].lower()
    def get_captcha_image_selenium(driver, blob_url):
        image_data = driver.execute_async_script("""const blobUrl = arguments[0]; const callback = arguments[1]; fetch(blobUrl) .then(response => response.blob()) .then(blob => { const reader = new FileReader(); reader.onloadend = function() { callback(reader.result); }; reader.readAsDataURL(blob); }) .catch(error => callback(null));""", blob_url)
        if image_data is None:
            raise ValueError("Error when getting captcha image (blob fetch failed)")
        
        if "base64" in image_data:
            image_data = image_data.split(",")[1]
            return image_data   
        raise ValueError("Blob fetch returned unexpected image_data")

    if not number_captcha_attempts or number_captcha_attempts <= 0:
        number_captcha_attempts = 1
    if not wait_captcha_seconds or wait_captcha_seconds <= 0:
        wait_captcha_seconds = 0
    action_type = action_type.lower()
    if action_type in ("tiktokwhirl", "tiktokslide", "tiktok3d", "tiktokicon"):
        try:
            start_time = time.time()
            while time.time() - start_time < wait_captcha_seconds:
                wait_is_exist_captcha_whirl = driver.execute_script("""var elements = document.evaluate('//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")] | //div[contains(@class, "cap") and count(img) = 2 and contains(img/@style, "circle")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")        
                wait_is_exist_captcha_slide = driver.execute_script("""var elements = document.evaluate('//div[contains(@class, "captcha") and contains(@class, "verify")]//img[contains(@class, "captcha_verify_img_slide")] | //div[contains(@class, "cap")]//div[contains(@draggable, "true")]/img[contains(@draggable, "false")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")             
                wait_is_exist_captcha_3d = driver.execute_script("""var elements = document.evaluate('//img[contains(@id,"verify")][contains(@src,"/3d_")] | //div[contains(@class,"cap")]//img/following-sibling::button /parent::div/parent::div/parent::div//img[(contains(@src,"blob") or contains(@src,"/3d_")) and //div[contains(@class,"cap")]//img/following-sibling::button and //div[contains(@class,"cap")]//span[contains(text(), "2")]]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")
                wait_is_exist_captcha_icon = driver.execute_script("""var elements = document.evaluate('//div[contains(@class,"verify") and count(img) = 1]/img[contains(@src,"icon")] | //div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//img[(contains(@src,"blob") or contains(@src,"/icon_")) and //div[contains(@class,"cap")]//img/following-sibling::button and  //div[contains(@class,"cap")]//span[contains(text(), "?")]]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")
                if wait_is_exist_captcha_whirl or wait_is_exist_captcha_slide or wait_is_exist_captcha_3d or wait_is_exist_captcha_icon:
                    break
                time.sleep(1)
            for i in range(0, number_captcha_attempts):
                is_exist_captcha_whirl = driver.execute_script("""var elements = document.evaluate('//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")] | //div[contains(@class, "cap") and count(img) = 2 and contains(img/@style, "circle")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")        
                is_exist_captcha_slide = driver.execute_script("""var elements = document.evaluate('//div[contains(@class, "captcha") and contains(@class, "verify")]//img[contains(@class, "captcha_verify_img_slide")] | //div[contains(@class, "cap")]//div[contains(@draggable, "true")]/img[contains(@draggable, "false")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")             
                is_exist_captcha_3d = driver.execute_script("""var elements = document.evaluate('//img[contains(@id,"verify")][contains(@src,"/3d_")] | //div[contains(@class,"cap")]//img/following-sibling::button /parent::div/parent::div/parent::div//img[(contains(@src,"blob") or contains(@src,"/3d_")) and //div[contains(@class,"cap")]//img/following-sibling::button and //div[contains(@class,"cap")]//span[contains(text(), "2")]]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")             
                is_exist_captcha_icon = driver.execute_script("""var elements = document.evaluate('//div[contains(@class,"verify") and count(img) = 1]/img[contains(@src,"icon")] | //div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//img[(contains(@src,"blob") or contains(@src,"/icon_")) and //div[contains(@class,"cap")]//img/following-sibling::button and  //div[contains(@class,"cap")]//span[contains(text(), "?")]]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")
                if not (is_exist_captcha_whirl or is_exist_captcha_slide or is_exist_captcha_3d or is_exist_captcha_icon): 
                    break
                else:
                    get_refresh_button = driver.execute_script("""var elements = document.evaluate('//a[contains(@class,"refresh")]/span[contains(@class,"refresh")][text()] | //button[contains(@class,"cap-items")][1]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")
                    if get_refresh_button:
                        update_captcha_img = driver.execute_script("""var element = document.evaluate('/a[contains(@class,"refresh")]/span[contains(@class,"refresh")][text()] | //button[contains(@class,"cap-items")][1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; return element;""")
                    else:
                        update_captcha_img = driver.execute_script("""var element = document.evaluate('//div[contains(@class,"captcha_verify_action")]//button[1]//div[contains(@class,"Button-label")][text()]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; return element;""")
                    
                    if is_exist_captcha_whirl:
                        get_captcha_data = driver.execute_script("""var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForElementAndGetData() { return new Promise((resolve, reject) => { var interval = setInterval(() => { var imgElement = document.evaluate( '//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")] | //div[contains(@class, "cap") and count(img) = 2 and contains(img/@style, "circle")]/img[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; var sliderElement = document.evaluate( '//div[contains(@class,"slidebar")] | //div[contains(@class, "cap")]/div[contains(@draggable, "true")]/parent::div', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (imgElement && sliderElement) { clearInterval(interval); var imgUrl = imgElement.getAttribute("src"); var width = window.getComputedStyle(sliderElement).getPropertyValue("width"); var height = window.getComputedStyle(sliderElement).getPropertyValue("height"); resolve({ url: imgUrl, width: Math.round(parseFloat(width)), height: Math.round(parseFloat(height)) }); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); reject("Image or slider element not found or not visible after 10 seconds."); } }, checkInterval); }); } return waitForElementAndGetData();""")
                        full_img_url = get_captcha_data['url'].strip()
                        img_width = round(get_captcha_data['width'])
                        img_height = round(get_captcha_data['height'])
                        if "blob:" in full_img_url:
                            full_img = get_captcha_image_selenium(driver, full_img_url)
                        elif full_img_url.startswith("data:image"):
                            full_img = full_img_url.strip()
                        else:                 
                            open_full_img_url = urllib.request.urlopen(full_img_url)
                            full_img_url_html_bytes = open_full_img_url.read()
                            full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                            full_img = full_screenshot_img_url_base64
                        small_img_url = driver.execute_script("""var elements = document.evaluate('//div[contains(@class,"captcha_verify_container")]/div/img[2][contains(@style,"transform: translate(-50%, -50%) rotate")] | //div[contains(@class, "cap") and count(img) = 2 and contains(img/@style, "circle")]/img[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null); var imgElement = elements.singleNodeValue; if (imgElement) {return imgElement.getAttribute("src");} return null;""")                        
                        if "blob:" in small_img_url:
                            small_img = get_captcha_image_selenium(driver, small_img_url)
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
                            driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForElement(callback) { var interval = setInterval(() => { var element = document.evaluate( '//div[contains(@class,"secsdk-captcha-drag-icon")]//*[name()="svg"] | ' + '//div[contains(@class, "cap")]/div[contains(@draggable, "true")]/button//*[name()="svg"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (element && element.offsetParent !== null && !element.disabled) { clearInterval(interval); callback(element); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); } }, checkInterval); } waitForElement((element) => { var rect = element.getBoundingClientRect(); var startX = rect.left + window.scrollX; var startY = rect.top + window.scrollY; var intermediateX = arguments[0]; var targetX = arguments[1]; var duration = arguments[2]; var pixelDelay = arguments[3]; function easeOutQuad(t) { return t * (2 - t); } function moveElement(fromX, toX, callback) { var totalSteps = Math.abs(toX - fromX); var currentX = fromX; var step = 0; var interval = setInterval(() => { step++; var progress = step / totalSteps; var easedProgress = easeOutQuad(progress); currentX = fromX + (toX - fromX) * easedProgress; var randomYOffset = Math.sin(progress * Math.PI) * (Math.random() * 3); var dragEvent = new DragEvent('drag', { bubbles: true, cancelable: true, clientX: currentX, clientY: startY + randomYOffset }); element.dispatchEvent(dragEvent); if (step >= totalSteps) { clearInterval(interval); callback(); } }, pixelDelay); } var fakeStartX = startX + Math.random() * 5 - 2; var fakeStartY = startY + Math.random() * 5 - 2; var dragStartEvent = new DragEvent('dragstart', { bubbles: true, cancelable: true, clientX: fakeStartX, clientY: fakeStartY }); element.dispatchEvent(dragStartEvent); setTimeout(() => { moveElement(fakeStartX, startX + intermediateX, () => { setTimeout(() => { moveElement(startX + intermediateX, startX + targetX, () => { var dropEvent = new DragEvent('drop', { bubbles: true, cancelable: true, clientX: startX + targetX, clientY: startY }); element.dispatchEvent(dropEvent); var dragEndEvent = new DragEvent('dragend', { bubbles: true, cancelable: true, clientX: startX + targetX, clientY: startY }); element.dispatchEvent(dragEndEvent); }); }, Math.random() * 100 + 50); }); }, Math.random() * 100 + 50); }); """, response_coordinate_x_random_move, response_coordinate_x, solve_captcha_speed, pixel_delay)
                            time.sleep(random.uniform(8, 10))
                        else:
                            driver.execute_script("arguments[0].click();", update_captcha_img)
                            time.sleep(random.uniform(8, 10))
                    elif is_exist_captcha_slide:
                        get_captcha_data = driver.execute_script("""var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForElementAndGetData() { return new Promise((resolve, reject) => { var interval = setInterval(() => { var element = document.evaluate( '//div[contains(@class, "verify") and count(img) = 2]/img[1] | //div[contains(@class, "cap") and count(img) = 2]/img[1] | //img[contains(@id, "verify")][1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (element && element.offsetParent !== null) { clearInterval(interval); var imgUrl = element.getAttribute("src"); var width = window.getComputedStyle(element).getPropertyValue("width"); var height = window.getComputedStyle(element).getPropertyValue("height"); resolve({ url: imgUrl, width: Math.round(parseFloat(width)), height: Math.round(parseFloat(height)) }); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); reject("Element not found or not visible after 10 seconds."); } }, checkInterval); }); } return waitForElementAndGetData();""")
                        full_img_url = get_captcha_data['url'].strip()
                        img_width = round(get_captcha_data['width'])
                        img_height = round(get_captcha_data['height'])
                        if "blob:" in full_img_url:
                            full_img = get_captcha_image_selenium(driver, full_img_url)
                        elif full_img_url.startswith("data:image"):
                            full_img = full_img_url.strip()
                        else: 
                            open_full_img_url = urllib.request.urlopen(full_img_url)
                            full_img_url_html_bytes = open_full_img_url.read()
                            full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                            full_img = full_screenshot_img_url_base64  
                        small_img_url = driver.execute_script("""var elements = document.evaluate('//div[contains(@class, "verify") and count(img) = 2]/img[2] | //div[contains(@class, "cap") and count(img) = 2]/img[2] | //img[contains(@id, "verify")]/following-sibling::div[contains(@draggable, "true")]/img', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null); var imgElement = elements.singleNodeValue; if (imgElement) {return imgElement.getAttribute("src");} return null;""")
                        if "blob:" in small_img_url:
                            small_img = get_captcha_image_selenium(driver, small_img_url)
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
                            driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForElement(callback) { var interval = setInterval(() => { var element = document.evaluate( '//div[contains(@class,"secsdk-captcha-drag-icon")]//*[name()="svg"] | ' + '//div[contains(@class, "cap")]/div[contains(@draggable, "true")]/button//*[name()="svg"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (element && element.offsetParent !== null && !element.disabled) { clearInterval(interval); callback(element); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); } }, checkInterval); } waitForElement((element) => { var rect = element.getBoundingClientRect(); var startX = rect.left + window.scrollX; var startY = rect.top + window.scrollY; var intermediateX = arguments[0]; var targetX = arguments[1]; var duration = arguments[2]; var pixelDelay = arguments[3]; function easeOutQuad(t) { return t * (2 - t); } function moveElement(fromX, toX, callback) { var totalSteps = Math.abs(toX - fromX); var currentX = fromX; var step = 0; var interval = setInterval(() => { step++; var progress = step / totalSteps; var easedProgress = easeOutQuad(progress); currentX = fromX + (toX - fromX) * easedProgress; var randomYOffset = Math.sin(progress * Math.PI) * (Math.random() * 3); var dragEvent = new DragEvent('drag', { bubbles: true, cancelable: true, clientX: currentX, clientY: startY + randomYOffset }); element.dispatchEvent(dragEvent); if (step >= totalSteps) { clearInterval(interval); callback(); } }, pixelDelay); } var fakeStartX = startX + Math.random() * 5 - 2; var fakeStartY = startY + Math.random() * 5 - 2; var dragStartEvent = new DragEvent('dragstart', { bubbles: true, cancelable: true, clientX: fakeStartX, clientY: fakeStartY }); element.dispatchEvent(dragStartEvent); setTimeout(() => { moveElement(fakeStartX, startX + intermediateX, () => { setTimeout(() => { moveElement(startX + intermediateX, startX + targetX, () => { var dropEvent = new DragEvent('drop', { bubbles: true, cancelable: true, clientX: startX + targetX, clientY: startY }); element.dispatchEvent(dropEvent); var dragEndEvent = new DragEvent('dragend', { bubbles: true, cancelable: true, clientX: startX + targetX, clientY: startY }); element.dispatchEvent(dragEndEvent); }); }, Math.random() * 100 + 50); }); }, Math.random() * 100 + 50); }); """, response_coordinate_x_random_move, response_coordinate_x, solve_captcha_speed, pixel_delay)
                            time.sleep(random.uniform(8, 10))
                        else:
                            driver.execute_script("arguments[0].click();", update_captcha_img)
                            time.sleep(random.uniform(8, 10))
                    elif is_exist_captcha_icon:
                        get_captcha_data = driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForCaptchaElement() { return new Promise((resolve, reject) => { var interval = setInterval(() => { var imgElement = document.evaluate( '//div[contains(@class,"verify") and count(img) = 1]/img[contains(@src,"icon")] | ' + '//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//' + 'img[(contains(@src,"blob") or contains(@src,"/icon_")) and ' + '//div[contains(@class,"cap")]//img/following-sibling::button and ' + '//div[contains(@class,"cap")]//span[contains(text(), "?")]]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; var questionElement = document.evaluate( '//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//span[text()]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (imgElement && questionElement) { clearInterval(interval); var imgRect = imgElement.getBoundingClientRect(); resolve({ width: imgElement.width, height: imgElement.height, x: imgRect.left + window.scrollX, y: imgRect.top + window.scrollY, url: imgElement.getAttribute("src"), question: questionElement.textContent }); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); reject("Captcha element not found or not visible within 10 seconds."); } }, checkInterval); }); } return waitForCaptchaElement(); """)
                        img_width = round(get_captcha_data['width'])
                        img_height = round(get_captcha_data['height'])
                        coordinate_full_img_url_x = round(get_captcha_data['x']) 
                        coordinate_full_img_url_y = round(get_captcha_data['y']) 
                        get_question = get_captcha_data['question'].strip()
                        full_img_url = get_captcha_data['url'].strip()
                        if "blob:" in full_img_url:
                            full_img = get_captcha_image_selenium(driver, full_img_url)
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
                                driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function easeOutQuad(t) { return t * (2 - t); } function waitForElement(xpath, callback) { var interval = setInterval(() => { var element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (element && element.offsetParent !== null) { if (element.tagName.toLowerCase() === 'img') { if (element.complete && element.naturalHeight > 0) { clearInterval(interval); callback(element); } } else { clearInterval(interval); callback(element); } } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); } }, checkInterval); } function smoothMoveAndClick(targetX, targetY, element) { var startX = window.innerWidth * Math.random(); var startY = window.innerHeight * Math.random(); var steps = Math.floor(10 + Math.random() * 10); var currentX = startX; var currentY = startY; var moveInterval = setInterval(() => { steps--; var progress = 1 - steps / 10; var easedProgress = easeOutQuad(progress); currentX = startX + (targetX - startX) * easedProgress; currentY = startY + (targetY - startY) * easedProgress; var moveEvent = new MouseEvent('mousemove', { bubbles: true, cancelable: true, clientX: currentX, clientY: currentY }); document.dispatchEvent(moveEvent); if (steps <= 0) { clearInterval(moveInterval); setTimeout(() => { var mouseDownEvent = new MouseEvent('mousedown', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }); element.dispatchEvent(mouseDownEvent); setTimeout(() => { var mouseUpEvent = new MouseEvent('mouseup', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }); element.dispatchEvent(mouseUpEvent); var clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }); element.dispatchEvent(clickEvent); }, Math.random() * 100 + 50); }, Math.random() * 100 + 50); } }, Math.random() * 20 + 10); } var targetXpath = '//div[contains(@class,"verify") and count(img) = 1]/img[contains(@src,"icon")] | ' + '//div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//' + 'img[(contains(@src,"blob") or contains(@src,"/icon_")) and ' + '//div[contains(@class,"cap")]//img/following-sibling::button and ' + '//div[contains(@class,"cap")]//span[contains(text(), "?")]]'; waitForElement(targetXpath, (element) => { var rect = element.getBoundingClientRect(); var adjustedX = rect.left + window.scrollX + rect.width / 2; var adjustedY = rect.top + window.scrollY + rect.height / 2; smoothMoveAndClick(arguments[0], arguments[1], element); }); """, target_coordinate_x, target_coordinate_y)
                                time.sleep(random.uniform(solve_captcha_speed / 1000 / 5, solve_captcha_speed / 1000 / 10))                      
                            time.sleep(random.uniform(solve_captcha_speed / 1000 / 3, solve_captcha_speed / 1000 / 5))  
                            driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForElementAndClick() { var interval = setInterval(() => { var submitButton = document.evaluate( '//div[contains(@class,"verify-captcha-submit-button")] | //div[contains(@class,"cap")]//img/following-sibling::button[contains(@aria-disabled,"false")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (submitButton && submitButton.offsetParent !== null && !submitButton.disabled) { clearInterval(interval); var clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true }); submitButton.dispatchEvent(clickEvent); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); } }, checkInterval); } waitForElementAndClick();""")
                            time.sleep(random.uniform(8, 10))
                        else:
                            driver.execute_script("arguments[0].click();", update_captcha_img)
                            time.sleep(random.uniform(8, 10))                                                
                    elif is_exist_captcha_3d:
                        get_captcha_data = driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForCaptchaElement() { return new Promise((resolve, reject) => { var interval = setInterval(() => { var imgElement = document.evaluate( '//div[contains(@class,"verify") and count(img) = 1] | //div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//img[contains(@src,"/3d_") or contains(@src,"blob")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (imgElement) { clearInterval(interval); var imgRect = imgElement.getBoundingClientRect(); resolve({ width: imgElement.width, height: imgElement.height, x: imgRect.left + window.scrollX, y: imgRect.top + window.scrollY, url: imgElement.getAttribute("src") }); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); reject("Captcha element not found or not visible within 10 seconds."); } }, checkInterval); }); } return waitForCaptchaElement(); """) 
                        img_width = round(get_captcha_data['width'])
                        img_height = round(get_captcha_data['height'])
                        coordinate_full_img_url_x = round(get_captcha_data['x']) 
                        coordinate_full_img_url_y = round(get_captcha_data['y']) 
                        full_img_url = get_captcha_data['url'].strip()                     
                        if "blob:" in full_img_url:
                            full_img = get_captcha_image_selenium(driver, full_img_url)
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
                                driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function easeOutQuad(t) { return t * (2 - t); } function waitForElement(xpath, callback) { var interval = setInterval(() => { var element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (element && element.offsetParent !== null) { if (element.tagName.toLowerCase() === 'img') { if (element.complete && element.naturalHeight > 0) { clearInterval(interval); callback(element); } } else { clearInterval(interval); callback(element); } } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); } }, checkInterval); } function smoothMoveAndClick(targetX, targetY, element) { var startX = window.innerWidth * Math.random(); var startY = window.innerHeight * Math.random(); var steps = Math.floor(10 + Math.random() * 10); var currentX = startX; var currentY = startY; var moveInterval = setInterval(() => { steps--; var progress = 1 - steps / 10; var easedProgress = easeOutQuad(progress); currentX = startX + (targetX - startX) * easedProgress; currentY = startY + (targetY - startY) * easedProgress; var moveEvent = new MouseEvent('mousemove', { bubbles: true, cancelable: true, clientX: currentX, clientY: currentY }); document.dispatchEvent(moveEvent); if (steps <= 0) { clearInterval(moveInterval); setTimeout(() => { var mouseDownEvent = new MouseEvent('mousedown', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }); element.dispatchEvent(mouseDownEvent); setTimeout(() => { var mouseUpEvent = new MouseEvent('mouseup', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }); element.dispatchEvent(mouseUpEvent); var clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }); element.dispatchEvent(clickEvent); }, Math.random() * 100 + 50); }, Math.random() * 100 + 50); } }, Math.random() * 20 + 10); } var targetXpath = '//div[contains(@class,"verify") and count(img) = 1] | //div[contains(@class,"cap")]//img/following-sibling::button/parent::div/parent::div/parent::div/div//img[contains(@src,"/3d_") or contains(@src,"blob")]'; waitForElement(targetXpath, (element) => { var rect = element.getBoundingClientRect(); var adjustedX = rect.left + window.scrollX + rect.width / 2; var adjustedY = rect.top + window.scrollY + rect.height / 2; smoothMoveAndClick(arguments[0], arguments[1], element); }); """, target_coordinate_x, target_coordinate_y)
                                time.sleep(random.uniform(solve_captcha_speed / 1000 / 5, solve_captcha_speed / 1000 / 10))                      
                            time.sleep(random.uniform(solve_captcha_speed / 1000 / 3, solve_captcha_speed / 1000 / 5))  
                            driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForElementAndClick() { var interval = setInterval(() => { var submitButton = document.evaluate( '//div[contains(@class,"verify-captcha-submit-button")] | //div[contains(@class,"cap")]//img/following-sibling::button[contains(@aria-disabled,"false")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (submitButton && submitButton.offsetParent !== null && !submitButton.disabled) { clearInterval(interval); var clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true }); submitButton.dispatchEvent(clickEvent); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); } }, checkInterval); } waitForElementAndClick();""")
                            time.sleep(random.uniform(8, 10))
                        else:
                            driver.execute_script("arguments[0].click();", update_captcha_img)
                            time.sleep(random.uniform(8, 10))
                            
        except Exception as e:
            print(f"Error: {e}")
    elif action_type == "datadomeaudio" or action_type == "datadomeimage":
        try:
            start_time = time.time()
            while time.time() - start_time < wait_captcha_seconds:
                wait_is_exist_capctha = driver.execute_script("""var elements = document.evaluate('//html[1]/body[1]//iframe[1][contains(@src,"https://geo.captcha-delivery.com")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")        
                if wait_is_exist_capctha :
                    break
                time.sleep(1)
            for i in range(0, number_captcha_attempts):
                is_exist_captcha_slide = driver.execute_script(""" var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (iframe) { var iframeDoc = iframe.contentDocument || iframe.contentWindow.document; return iframeDoc.evaluate('//div[contains(@id,"captcha__puzzle")]', iframeDoc, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null).snapshotLength > 0; } return false; """)
                is_exist_captcha_audio = driver.execute_script(""" var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (iframe) { var iframeDoc = iframe.contentDocument || iframe.contentWindow.document; return iframeDoc.evaluate('//button[contains(@class,"audio-captcha-play-button")]', iframeDoc, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null).snapshotLength > 0; } return false; """)                
                if not (is_exist_captcha_slide or is_exist_captcha_audio): 
                    break
                else:
                    if (selected_captcha_type == 'audio'):
                        select_capctha_slide = driver.execute_script(""" var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (iframe) { var iframeDoc = iframe.contentDocument || iframe.contentWindow.document; return iframeDoc.evaluate('//div[contains(@id,"switch")]//button[contains(@id,"puzzle")][contains(@class,"captcha-toggle")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; } return null; """)
                        driver.execute_script("arguments[0].click();", select_capctha_slide)
                        time.sleep(random.uniform(1, 3))
                    else:
                        select_capctha_audio = driver.execute_script(""" var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (iframe) { var iframeDoc = iframe.contentDocument || iframe.contentWindow.document; return iframeDoc.evaluate('//div[contains(@id,"switch")]//button[contains(@id,"audio")][contains(@class,"captcha-toggle")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; } return null; """)
                        driver.execute_script("arguments[0].click();", select_capctha_audio)
                    update_captcha_img = driver.execute_script(""" var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; var button = null; if (iframe) { var iframeDoc = iframe.contentDocument || iframe.contentWindow.document; button = iframeDoc.evaluate('//button[contains(@id,"reload")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; } if (!button) { button = document.evaluate('//button[contains(@id,"reload")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; } if (button) { return button; } return null; """)
                    if is_exist_captcha_slide:
                        get_captcha_data = driver.execute_script(""" var iframe = document.evaluate('//html[1]//body[1]//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (iframe) { var iframeDoc = iframe.contentDocument || iframe.contentWindow.document; var linkElement = iframeDoc.evaluate('//html//link[contains(@rel,"preload")][1]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; var href = linkElement ? linkElement.getAttribute('href') : null; var puzzleElement = iframeDoc.evaluate('//div[contains(@id,"captcha__puzzle")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; var width = puzzleElement ? puzzleElement.offsetWidth : null; var height = puzzleElement ? puzzleElement.offsetHeight : null; return { href: href, width: width, height: height }; } return null; """)                       
                        full_img_url = get_captcha_data['url'].strip()
                        img_width = round(get_captcha_data['width'])
                        img_height = round(get_captcha_data['height'])
                        if "blob:" in full_img_url:
                            full_img = get_captcha_image_selenium(driver, full_img_url)
                        elif full_img_url.startswith("data:image"):
                            full_img = full_img_url.strip()
                        else: 
                            open_full_img_url = urllib.request.urlopen(full_img_url)
                            full_img_url_html_bytes = open_full_img_url.read()
                            full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8')
                            full_img = full_screenshot_img_url_base64  
                        small_img_url = driver.execute_script(""" var iframe = document.evaluate('//html[1]//body[1]//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (iframe) { var iframeDoc = iframe.contentDocument || iframe.contentWindow.document; var elements = iframeDoc.evaluate('//html//link[contains(@rel,"preload")][2]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null); var linkElement = elements.singleNodeValue; if (linkElement) { return linkElement.getAttribute('href'); } } return null; """)
                        if "blob:" in small_img_url:
                            small_img = get_captcha_image_selenium(driver, small_img_url)
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
                            driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; var iframe = document.evaluate("//html[1]//body[1]//iframe[1]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (iframe) { var iframeDoc = iframe.contentDocument || iframe.contentWindow.document; function waitForElement(callback) { var interval = setInterval(() => { // Новый XPath с учётом iframe var element = iframeDoc.evaluate( '//div[contains(@class,"sliderContainer")]//i[contains(@class,"sliderIcon")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (element && element.offsetParent !== null && !element.disabled) { clearInterval(interval); callback(element); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); } }, checkInterval); } waitForElement((element) => { var rect = element.getBoundingClientRect(); var startX = rect.left; var startY = rect.top; var intermediateX = arguments[0]; var targetX = arguments[1]; var duration = arguments[2]; var pixelDelay = arguments[3]; function moveElement(fromX, toX, callback) { var steps = Math.abs(toX - fromX); var stepSize = (toX - fromX) / steps; var currentX = fromX; var interval = setInterval(() => { currentX += stepSize; var dragEvent = new DragEvent('drag', { bubbles: true, cancelable: true, clientX: currentX, clientY: startY }); element.dispatchEvent(dragEvent); if ((stepSize > 0 && currentX >= toX) || (stepSize < 0 && currentX <= toX)) { clearInterval(interval); callback(); } }, pixelDelay); } var dragStartEvent = new DragEvent('dragstart', { bubbles: true, cancelable: true, clientX: startX, clientY: startY }); element.dispatchEvent(dragStartEvent); moveElement(startX, startX + intermediateX, () => { moveElement(startX + intermediateX, startX + targetX, () => { var dropEvent = new DragEvent('drop', { bubbles: true, cancelable: true, clientX: startX + targetX, clientY: startY }); element.dispatchEvent(dropEvent); var dragEndEvent = new DragEvent('dragend', { bubbles: true, cancelable: true, clientX: startX + targetX, clientY: startY }); element.dispatchEvent(dragEndEvent); }); }); }); } """, response_coordinate_x_random_move, response_coordinate_x, solve_captcha_speed, random.uniform(solve_captcha_speed / 500, solve_captcha_speed / 300))
                            time.sleep(random.uniform(8, 10))
                        else:
                            driver.execute_script("arguments[0].click();", update_captcha_img)
                            time.sleep(random.uniform(8, 10))
                    elif is_exist_captcha_audio:
                        get_captcha_data = driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForCaptchaAudioSrc() { return new Promise((resolve, reject) => { var interval = setInterval(() => { var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (iframe) { var iframeDoc = iframe.contentDocument || iframe.contentWindow.document; var audioButton = iframeDoc.evaluate( '//button[contains(@class,"audio-captcha-play-button")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (audioButton) { clearInterval(interval); resolve(audioButton.getAttribute("src")); } } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); reject("Audio captcha button not found after 10 seconds."); } }, checkInterval); }); } return waitForCaptchaAudioSrc(); """)
                        get_audio_url = get_captcha_data['url'].strip()
                        if get_audio_url and "/en/" not in get_audio_url:
                            get_audio_url = re.sub(r"/[a-z]{2}/", "/en/", get_audio_url)
                        if "blob:" in get_audio_url:
                            audio_data = get_captcha_image_selenium(driver, get_audio_url)
                        elif audio_url.startswith("data:image"):
                            audio_data = audio_url.strip()
                        else:                    
                            open_audio_url = urllib.request.urlopen(get_audio_url)
                            audio_url_html_bytes = open_audio_url.read()
                            audio_url_base64 = base64.b64encode(audio_url_html_bytes).decode('utf-8')
                            audio_data = audio_url_base64
                        captcha_click_play =  driver.execute_script(""" var iframe = document.evaluate('//html[1]//body[1]//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; var button = null; if (iframe) { var iframeDoc = iframe.contentDocument || iframe.contentWindow.document; button = iframeDoc.evaluate('//button[contains(@class,"audio-captcha-play-button")]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; } if (!button) { button = document.evaluate('//button[contains(@class,"audio-captcha-play-button")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; } if (button) { var mouseDownEvent = new MouseEvent('mousedown', { bubbles: true, cancelable: true, view: window, button: 0, clientX: button.getBoundingClientRect().left + 1, clientY: button.getBoundingClientRect().top + 1 }); button.dispatchEvent(mouseDownEvent); var mouseUpEvent = new MouseEvent('mouseup', { bubbles: true, cancelable: true, view: window, button: 0, clientX: button.getBoundingClientRect().left + 1, clientY: button.getBoundingClientRect().top + 1 }); button.dispatchEvent(mouseUpEvent); // Эмуляция самого клика var clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true, view: window, button: 0, clientX: button.getBoundingClientRect().left + 1, clientY: button.getBoundingClientRect().top + 1 }); button.dispatchEvent(clickEvent); } """)
                        driver.execute_script("arguments[0].click();", captcha_click_play)
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
                            driver.execute_script(""" var responseCode = arguments[0]; var iframe = document.evaluate('//iframe[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (iframe) { var iframeDoc = iframe.contentDocument || iframe.contentWindow.document; var inputField = iframeDoc.evaluate('//div[contains(@class,"audio-captcha-input-container")]/input[contains(@class,"audio-captcha-input")][1]', iframeDoc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (inputField) { inputField.value = responseCode; inputField.dispatchEvent(new Event('input', { bubbles: true })); return true; } } return false; """, response_code)
                            time.sleep(random.uniform(8, 10))
                        else:
                            driver.execute_script("arguments[0].click();", update_captcha_img)
                            time.sleep(random.uniform(8, 10))
        except Exception as e:
            print(f"Error: {e}")
    elif action_type == "geetesticon":
        time.sleep(random.uniform(1, 3))
        try:
            start_time = time.time()
            while time.time() - start_time < wait_captcha_seconds:
                wait_is_exist_capctha = driver.execute_script("""var elements = document.evaluate('//div[contains(@class,"geetest_box_wrap")]/div[contains(@class,"geetest_box")]/div[contains(@class,"geetest_container")]/div[contains(@class,"geetest_wrap")]/div[contains(@class,"geetest_subitem")]/div[contains(@class,"geetest_window")]/div[contains(@class,"geetest_bg")] | //div[contains(@class,"geetest_close") or contains(@class,"geetest_nextReady")]//div[contains(@class,"geetest_btn_click")] | //div[contains(@class,"geetest_close") or contains(@class,"geetest_nextReady")]//div[contains(@class,"geetest_btn_click")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")        
                if wait_is_exist_capctha :
                    break
                time.sleep(1)
            is_exist_capctha_success = driver.execute_script("""var elements = document.evaluate('//div[contains(@class,"geetest_lock_success")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")        
            if not (is_exist_capctha_success):
                open_captcha_button = driver.execute_script("""var element = document.evaluate('//div[contains(@class,"geetest_btn_click")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; return element;""")
                driver.execute_script("arguments[0].click();", open_captcha_button)
                while time.time() - start_time < wait_captcha_seconds:
                    wait_is_exist_capctha = driver.execute_script("""var elements = document.evaluate('//div[contains(@class,"geetest_box_wrap")]/div[contains(@class,"geetest_box")]/div[contains(@class,"geetest_container")]/div[contains(@class,"geetest_wrap")]/div[contains(@class,"geetest_subitem")]/div[contains(@class,"geetest_window")]/div[contains(@class,"geetest_bg")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")        
                    if wait_is_exist_capctha :
                        break
                time.sleep(1)
            for i in range(0, number_captcha_attempts):
                is_exist_capctha_icon = driver.execute_script("""var elements = document.evaluate('//div[contains(@class,"geetest_box_wrap")]/div[contains(@class,"geetest_box")]/div[contains(@class,"geetest_container")]/div[contains(@class,"geetest_wrap")]/div[contains(@class,"geetest_subitem")]/div[contains(@class,"geetest_window")]/div[contains(@class,"geetest_bg")]', document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null); return elements.snapshotLength > 0;""")        
                if not (is_exist_capctha_icon):
                    break
                else:
                    update_captcha_img = driver.execute_script("""var element = document.evaluate('//button[contains(@class,"geetest_refresh")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; return element;""")
                    if is_exist_capctha_icon:
                        get_captcha_data = driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForCaptchaElement() { return new Promise((resolve, reject) => { var interval = setInterval(() => { var imgElement = document.evaluate('//div[contains(@class,"geetest_box_wrap")]/div[contains(@class,"geetest_box")]/div[contains(@class,"geetest_container")]/div[contains(@class,"geetest_wrap")]/div[contains(@class,"geetest_subitem")]/div[contains(@class,"geetest_window")]/div[contains(@class,"geetest_bg")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (imgElement) { clearInterval(interval); var imgRect = imgElement.getBoundingClientRect(); resolve({ width: imgRect.width, height: imgRect.height, x: imgRect.left + window.scrollX, y: imgRect.top + window.scrollY, url: imgElement.getAttribute("style") }); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); reject("Captcha element not found or not visible within 10 seconds."); } }, checkInterval); }); } return waitForCaptchaElement(); """)
                        img_width = round(get_captcha_data['width'])
                        img_height = round(get_captcha_data['height']) 
                        coordinate_full_img_url_x = round(get_captcha_data['x'])
                        coordinate_full_img_url_y = round(get_captcha_data['y'])
                        full_img_url = get_captcha_data['url'] 
                        full_img_url_start = full_img_url.find('url("') + len('url("')
                        full_img_url_end = full_img_url.find('")', full_img_url_start)
                        full_img_url = full_img_url[full_img_url_start:full_img_url_end]                    
                        if "blob:" in full_img_url:
                            full_img = get_captcha_image_selenium(driver, full_img_url)
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
                            for target_coordinate_x, target_coordinate_y in target_coordinates:
                                driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function easeOutQuad(t) { return t * (2 - t); } function waitForElement(xpath, callback) { var interval = setInterval(() => { var element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (element && element.offsetParent !== null) { clearInterval(interval); callback(element); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); } }, checkInterval); } function smoothMoveAndClick(targetX, targetY, element) { var startX = Math.random() * window.innerWidth; var startY = Math.random() * window.innerHeight; var steps = Math.floor(30 + Math.random() * 20); var currentX = startX; var currentY = startY; var moveInterval = setInterval(() => { steps--; var progress = 1 - steps / 30; var easedProgress = easeOutQuad(progress); currentX = startX + (targetX - startX) * easedProgress; currentY = startY + (targetY - startY) * easedProgress; var moveEvents = [ new MouseEvent('mousemove', { bubbles: true, cancelable: true, clientX: currentX, clientY: currentY }), new PointerEvent('pointermove', { bubbles: true, cancelable: true, clientX: currentX, clientY: currentY }), new MouseEvent('mouseover', { bubbles: true, cancelable: true, clientX: currentX, clientY: currentY }), new MouseEvent('mouseenter', { bubbles: true, cancelable: true, clientX: currentX, clientY: currentY }) ]; moveEvents.forEach(evt => { document.dispatchEvent(evt); element.dispatchEvent(evt); }); if (steps <= 0) { clearInterval(moveInterval); setTimeout(() => { var pointerDownEvent = new PointerEvent('pointerdown', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }); var mouseDownEvent = new MouseEvent('mousedown', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }); element.dispatchEvent(pointerDownEvent); document.dispatchEvent(pointerDownEvent); element.dispatchEvent(mouseDownEvent); document.dispatchEvent(mouseDownEvent); setTimeout(() => { var pointerUpEvent = new PointerEvent('pointerup', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }); var mouseUpEvent = new MouseEvent('mouseup', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }); var clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true, clientX: targetX, clientY: targetY }); element.dispatchEvent(pointerUpEvent); document.dispatchEvent(pointerUpEvent); element.dispatchEvent(mouseUpEvent); document.dispatchEvent(mouseUpEvent); element.dispatchEvent(clickEvent); document.dispatchEvent(clickEvent); }, Math.random() * 150 + 50); }, Math.random() * 150 + 50); } }, Math.random() * 30 + 10); } var targetXpath = '//div[contains(@class,"geetest_box_wrap")]/div[contains(@class,"geetest_box")]/div[contains(@class,"geetest_container")]/div[contains(@class,"geetest_wrap")]/div[contains(@class,"geetest_subitem")]/div[contains(@class,"geetest_window")]/div[contains(@class,"geetest_bg")]'; waitForElement(targetXpath, (element) => { var rect = element.getBoundingClientRect(); var adjustedX = rect.left + window.scrollX + rect.width / 2; var adjustedY = rect.top + window.scrollY + rect.height / 2; if (window.getComputedStyle(element).display !== 'none' && window.getComputedStyle(element).visibility !== 'hidden' && element.offsetWidth > 0 && element.offsetHeight > 0) { smoothMoveAndClick(adjustedX, adjustedY, element); } }); """, target_coordinate_x, target_coordinate_y)
                                time.sleep(random.uniform(solve_captcha_speed / 1000 / 5, solve_captcha_speed / 1000 / 10))                      
                            time.sleep(random.uniform(solve_captcha_speed / 1000 / 3, solve_captcha_speed / 1000 / 5))  
                            driver.execute_script(""" var maxWaitTime = 10000; var checkInterval = 100; var totalTimeWaited = 0; function waitForElementAndClick() { var interval = setInterval(() => { var submitButton = document.evaluate( '//div[contains(@class,"geetest_box_wrap")]/div[contains(@class,"geetest_box")]/div[contains(@class,"geetest_container")]/div[contains(@class,"geetest_wrap")]/div[contains(@class,"geetest_subitem")]/div[contains(@class,"geetest_submit")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue; if (submitButton && submitButton.offsetParent !== null && !submitButton.disabled) { clearInterval(interval); var clickEvent = new MouseEvent('click', { bubbles: true, cancelable: true }); submitButton.dispatchEvent(clickEvent); } totalTimeWaited += checkInterval; if (totalTimeWaited >= maxWaitTime) { clearInterval(interval); } }, checkInterval); } waitForElementAndClick();""")
                            time.sleep(random.uniform(8, 10))
                        else:
                            driver.execute_script("arguments[0].click();", update_captcha_img)
                            time.sleep(random.uniform(8, 10))
        except Exception as e:
            print(f"Error: {e}")
    else:
        ("Invalid action type / Supports: tiktokWhirl, tiktokSlide, tiktok3D, tiktokIcon, dataDomeAudio, dataDomeImage, geeTestIcon")

