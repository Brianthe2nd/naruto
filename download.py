from playwright.sync_api import sync_playwright
import os

def download_file(url, download_button_selector= "div#app form"):
    # Define download path and create "naruto" folder if it doesn't exist
    download_path = os.path.join(os.getcwd(), "naruto")
    os.makedirs(download_path, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the URL
        page.goto(url)
        
        # Wait for 2 seconds to ensure the page has loaded
        page.wait_for_timeout(2000)
        
        # Click a random position on the page
        page.mouse.click(10, 10)  # Clicking somewhere relatively harmless
        
        # Wait for the download button to be available on the page
        page.wait_for_selector(download_button_selector, timeout=10000)  # Wait up to 10 seconds
        
        # Initiate the download by clicking the download button
        with page.expect_download() as download_info:
            page.click(download_button_selector)
        
        # Wait for the download to complete and get the download object
        download = download_info.value
        
        # Save the file in the "naruto" folder with the suggested filename
        download.save_as(os.path.join(download_path, download.suggested_filename))

        browser.close()

    print(f"Downloaded file saved in: {download_path}")

if __name__ == "__main__":
    download_file("https://kwik.si/f/ZLqOlO0YBg1x")
