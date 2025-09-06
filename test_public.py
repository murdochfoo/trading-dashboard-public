#!/usr/bin/env python3
"""
Test public version JavaScript functionality
"""

import asyncio
from playwright.async_api import async_playwright

async def test_public_dashboard():
    print("🧪 Testing Public Dashboard Data Loading")
    print("=" * 50)
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        # Load public dashboard from GitHub Pages
        await page.goto("https://murdochfoo.github.io/trading-dashboard-public/", timeout=15000)
        await page.wait_for_timeout(3000)  # Wait for full load
        
        # Check basic JavaScript execution
        basic_js = await page.evaluate("1 + 1")
        print(f"Basic JS (1+1): {basic_js}")
        
        # Check if data arrays exist
        individual_data = await page.evaluate("typeof individualData !== 'undefined' && individualData && individualData.length")
        print(f"individualData loaded: {individual_data}")
        
        spy_benchmark = await page.evaluate("typeof spyBenchmark !== 'undefined' && spyBenchmark && spyBenchmark.length") 
        print(f"spyBenchmark loaded: {spy_benchmark}")
        
        # Check individual tab table rows
        individual_rows = await page.locator("#individual-tbody tr").count()
        print(f"Individual tab rows: {individual_rows}")
        
        # Check combination tab  
        combo_rows = await page.locator("#combination-tbody tr").count()
        print(f"Combination tab rows: {combo_rows}")
        
        # Check console for errors
        console_messages = []
        def handle_console(msg):
            if msg.type in ['error', 'warning']:
                console_messages.append(f"{msg.type}: {msg.text}")
        
        page.on('console', handle_console)
        await page.wait_for_timeout(2000)
        
        if console_messages:
            print("\n❌ Console errors/warnings:")
            for msg in console_messages[:5]:
                print(f"  {msg}")
        else:
            print("\n✅ No console errors")
            
        return individual_rows > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        await browser.close()

if __name__ == "__main__":
    result = asyncio.run(test_public_dashboard())
    exit(0 if result else 1)