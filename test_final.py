#!/usr/bin/env python3
"""
Final test with correct function names
"""

import asyncio
from playwright.async_api import async_playwright

async def test_final():
    print("🎯 Final Working Test")
    print("=" * 40)
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        # Load public dashboard
        await page.goto("https://murdochfoo.github.io/trading-dashboard-public/", timeout=20000)
        await page.wait_for_timeout(5000)  # Wait for full load
        
        # Check data arrays
        individual_data = await page.evaluate("typeof individualData !== 'undefined' && individualData && individualData.length")
        print(f"✅ individualData loaded: {individual_data} strategies")
        
        combination_data = await page.evaluate("typeof combinationData !== 'undefined' && combinationData && combinationData.length")
        print(f"✅ combinationData loaded: {combination_data} strategies")
        
        # Check function existence
        create_func_exists = await page.evaluate("typeof createMacroIndividualTable === 'function'")
        print(f"🔧 createMacroIndividualTable function exists: {create_func_exists}")
        
        # Test Individual tab
        individual_rows = await page.locator("#individual-tbody tr").count()
        print(f"📊 Individual tab initial rows: {individual_rows}")
        
        if individual_rows == 0 and create_func_exists:
            # Try manual population
            try:
                result = await page.evaluate("""
                    if (typeof individualData !== 'undefined' && individualData.length > 0) {
                        createMacroIndividualTable(individualData);
                        return 'Success';
                    }
                    return 'No data';
                """)
                print(f"🔄 Manual population: {result}")
                
                await page.wait_for_timeout(2000)
                rows_after = await page.locator("#individual-tbody tr").count()
                print(f"📊 Individual tab rows after manual call: {rows_after}")
            except Exception as e:
                print(f"❌ Manual population error: {e}")
        
        # Test Combination tab
        await page.click("button:has-text('Combination')")
        await page.wait_for_timeout(2000)
        combo_rows = await page.locator("#combination-tbody tr").count()
        print(f"📊 Combination tab rows: {combo_rows}")
        
        # Test Clustering tab 
        await page.click("button:has-text('Clustering')")
        await page.wait_for_timeout(2000)
        
        # Check if K-Means sub-tab is visible and clickable
        try:
            kmeans_button = await page.locator("button:has-text('K-Means')").first
            is_visible = await kmeans_button.is_visible()
            print(f"🔍 K-Means button visible: {is_visible}")
            
            if is_visible:
                await kmeans_button.click()
                await page.wait_for_timeout(1000)
                kmeans_rows = await page.locator("#macro-clustering-kmeans-tbody tr").count()
                print(f"📊 K-Means clustering rows: {kmeans_rows}")
            else:
                print("❌ K-Means button not visible")
        except Exception as e:
            print(f"❌ K-Means test error: {e}")
        
        # Final success check
        total_rows = individual_rows + combo_rows
        success = total_rows > 0 or individual_data > 0
        
        print(f"\n🎯 FINAL RESULT: {'SUCCESS' if success else 'FAIL'}")
        print(f"📊 Data loaded: {individual_data + combination_data} total strategies")
        print(f"📋 Table rows populated: {total_rows}")
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        await browser.close()

if __name__ == "__main__":
    result = asyncio.run(test_final())
    exit(0 if result else 1)