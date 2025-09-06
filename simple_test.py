#!/usr/bin/env python3
"""
Simple test to check if data loads with longer wait times
"""

import asyncio
from playwright.async_api import async_playwright

async def simple_test():
    print("🧪 Simple Data Loading Test")
    print("=" * 40)
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        # Load public dashboard
        await page.goto("https://murdochfoo.github.io/trading-dashboard-public/", timeout=20000)
        print("📡 Page loaded")
        
        # Wait much longer for data to load
        await page.wait_for_timeout(10000)  # Wait 10 seconds
        print("⏰ Waited 10 seconds for data loading")
        
        # Check if data arrays exist with longer timeout
        try:
            individual_data = await page.wait_for_function("typeof individualData !== 'undefined' && individualData && individualData.length > 0", timeout=15000)
            print(f"✅ individualData loaded: {individual_data}")
        except:
            print("❌ individualData not loaded within 15 seconds")
        
        # Check individual table rows
        individual_rows = await page.locator("#individual-tbody tr").count()
        print(f"📊 Individual tab rows: {individual_rows}")
        
        # Check if SPY Buy & Hold benchmark is present
        benchmark_rows = await page.locator("#individual-tbody .benchmark-row").count()
        print(f"📈 Benchmark rows: {benchmark_rows}")
        
        # Check if data loading functions exist
        populate_table_exists = await page.evaluate("typeof populateTable === 'function'")
        print(f"🔧 populateTable function exists: {populate_table_exists}")
        
        # Try manual table population
        if populate_table_exists:
            try:
                result = await page.evaluate("""
                    if (typeof individualData !== 'undefined' && individualData && individualData.length > 0) {
                        populateTable(individualData, 'individual-tbody');
                        return 'Manual population attempted';
                    }
                    return 'No data available for population';
                """)
                print(f"🔄 Manual population result: {result}")
                
                # Check rows after manual population
                await page.wait_for_timeout(2000)
                rows_after = await page.locator("#individual-tbody tr").count()
                print(f"📊 Rows after manual population: {rows_after}")
            except Exception as e:
                print(f"❌ Manual population failed: {e}")
        
        return individual_rows > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        await browser.close()

if __name__ == "__main__":
    result = asyncio.run(simple_test())
    print(f"\n🎯 Result: {'SUCCESS' if result else 'FAIL'}")
    exit(0 if result else 1)