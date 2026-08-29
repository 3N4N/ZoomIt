import time
import commentjson as json
import requests
from playwright.sync_api import sync_playwright, TimeoutError
from tqdm.auto import tqdm

with open('input.json', 'r', encoding='utf-8') as f:
    ZOOM_URLS = json.load(f)

# print(json.dumps(ZOOM_URLS, indent=2))


CHUNK_SIZE  = 10 * 1024**2
REFERER     = "https://us02web.zoom.us/"

def download_current_video(context, video_response, output):
    video_url = video_response.url
    video_len = int(video_response.headers.get("content-length"))
    headers   = video_response.all_headers()

    print(
        f"{output}: "
        f"{video_len / (1024 * 1024):.1f} MB"
    )

    with open(output, "wb") as f:
        for start in tqdm(range(0, video_len, CHUNK_SIZE)):

            end = min(
                start + CHUNK_SIZE - 1,
                video_len - 1
            )

            response = context.request.get(
                video_url,
                headers={
                    # **headers,
                    "Referer": REFERER,
                    "Range": f"bytes={start}-{end}"
                }
            )

            if response.status != 206:
                raise RuntimeError(
                    f"Expected 206, got {response.status}"
                )

            f.write(response.body())

    print("\nDone:", output)

for _item in ZOOM_URLS:
    zoom_url = _item['URL']
    password = _item['Passcode']
    output   = _item['Title']

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            accept_downloads=True
        )

        print(f"Downloading '{output}'")

        page = context.new_page()

        video_response = None

        def on_response(response):
            global video_response
            # print("--> on_response")

            url = response.url
            content_type = response.headers.get("content-type", "").lower()

            if (
                "video/mp4" in content_type
                or ".mp4" in url.lower()
            ):
                print()
                print("========================================")
                print("VIDEO RESPONSE FOUND")
                print("Status:", response.status)
                print("Content-Type:", content_type)
                print("URL:", url[:200] + "...")
                print("Range:", response.headers.get("content-range"))
                print("Length:", response.headers.get("content-length"))
                print("========================================")

                if response.status == 206 and video_response is None:
                    video_response = response

        page.on("response", on_response)

        print("Opening recording...")

        page.goto(
            zoom_url,
            wait_until="domcontentloaded"
        )

        print("Entering password...")

        password_box = page.locator('input[type="password"]')

        password_box.wait_for(
            state="visible",
            timeout=30000
        )

        password_box.fill(password)

        # Submit using Enter.
        password_box.press("Enter")

        # Wait for Zoom to request the video
        page.wait_for_timeout(30000)

        download_current_video(context, video_response, f"{output} (1).mp4")
        video_response = None

        next_recording_btn = page.get_by_role("button", name="Go Forward to next clip")
        try:
            next_recording_btn.click(trial=True, timeout=3000)
            next_recording_btn.click()
            page.wait_for_timeout(30000)
            download_current_video(context, video_response, f"{output} (2).mp4")
        except TimeoutError:
            print("No second recording.")

        browser.close()
