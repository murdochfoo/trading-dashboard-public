#!/usr/bin/env python3
"""
Final visual test to confirm data is displaying
"""

import asyncio
from playwright.async_api import async_playwright

async def final_visual_test():
    print("👀 Final Visual Dashboard Test")
    print("=" * 50)
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)  # Visible browser
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        # Load public dashboard
        await page.goto("https://murdochfoo.github.io/trading-dashboard-public/", timeout=20000)
        print("📡 Page loaded, waiting for full initialization...")
        await page.wait_for_timeout(8000)  # Wait longer for everything to load
        
        # Check basic data loading
        individual_count = await page.evaluate("individualData ? individualData.length : 0")
        print(f"📊 Individual data array: {individual_count} strategies")
        
        # Check if tables have actual content
        individual_rows = await page.locator("#individual-tbody tr").count()
        print(f"📋 Individual table rows: {individual_rows}")
        
        if individual_rows > 0:
            # Get sample of first row content
            first_row_text = await page.locator("#individual-tbody tr").first.text_content()
            print(f"✅ First row content: {first_row_text[:100]}...")
            
            # Check for SPY benchmark
            spy_row = await page.locator("#individual-tbody .benchmark-row").count()
            print(f"📈 SPY Buy & Hold benchmark row: {spy_row}")
        
        # Test other tabs
        await page.click("button:has-text('Combination')")
        await page.wait_for_timeout(2000)
        combo_rows = await page.locator("#combination-tbody tr").count()
        print(f"📋 Combination table rows: {combo_rows}")
        
        if combo_rows > 0:
            combo_text = await page.locator("#combination-tbody tr").first.text_content()
            print(f"✅ Combination row sample: {combo_text[:80]}...")
        
        # Test clustering tab
        await page.click("button:has-text('Clustering')")
        await page.wait_for_timeout(2000)
        
        # Check if sub-tabs are visible
        kmeans_visible = await page.locator("button:has-text('K-Means')").is_visible()
        print(f"🔍 K-Means sub-tab visible: {kmeans_visible}")
        
        if kmeans_visible:
            await page.click("button:has-text('K-Means')")
            await page.wait_for_timeout(2000)
            kmeans_rows = await page.locator("#macro-clustering-kmeans-tbody tr").count()
            print(f"📋 K-Means table rows: {kmeans_rows}")
        
        # Overall success metrics
        total_working_tabs = 0
        if individual_rows > 0:
            total_working_tabs += 1
        if combo_rows > 0:
            total_working_tabs += 1
        if kmeans_visible and kmeans_rows > 0:
            total_working_tabs += 1
        
        print(f"\n📊 DASHBOARD SUMMARY:")
        print(f"   🎯 Working tabs: {total_working_tabs}/3+ expected")
        print(f"   📋 Total table rows: {individual_rows + combo_rows + (kmeans_rows if kmeans_visible else 0)}")
        print(f"   💾 Data arrays loaded: {individual_count} individual strategies")
        
        success = individual_rows > 0 or combo_rows > 0
        result_emoji = "✅" if success else "❌"
        print(f"\n{result_emoji} FINAL STATUS: {'SUCCESS - Data is displaying!' if success else 'FAIL - Tables still empty'}")
        
        # Keep browser open for manual inspection
        print(f"\n🔍 Browser staying open for 30 seconds for visual inspection...")
        await page.wait_for_timeout(30000)
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        await browser.close()

if __name__ == "__main__":
    result = asyncio.run(final_visual_test())
    print(f"\n🏁 Final Result: {'PASS ✅' if result else 'FAIL ❌'}")
    exit(0 if result else 1)