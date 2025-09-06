#!/usr/bin/env python3
"""
Verify public dashboard with Playwright - comprehensive tab testing
"""

import asyncio
from playwright.async_api import async_playwright

async def verify_public_dashboard():
    print("🔍 Comprehensive Public Dashboard Verification")
    print("=" * 60)
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)  # Visible for debugging
    context = await browser.new_context()
    page = await context.new_page()
    
    try:
        # Load public dashboard from GitHub Pages
        print("📡 Loading GitHub Pages dashboard...")
        await page.goto("https://murdochfoo.github.io/trading-dashboard-public/", timeout=15000)
        await page.wait_for_timeout(5000)  # Wait for full load
        
        # Check basic page load
        title = await page.title()
        print(f"📄 Page title: {title}")
        
        # Check basic JavaScript execution
        basic_js = await page.evaluate("1 + 1")
        print(f"⚡ Basic JS (1+1): {basic_js}")
        
        # Check if data arrays exist
        print("\n🔍 Checking JavaScript data arrays:")
        individual_data = await page.evaluate("typeof individualData !== 'undefined' && individualData && individualData.length")
        print(f"  individualData: {individual_data}")
        
        spy_benchmark = await page.evaluate("typeof spyBenchmark !== 'undefined' && spyBenchmark && spyBenchmark.length")
        print(f"  spyBenchmark: {spy_benchmark}")
        
        combination_data = await page.evaluate("typeof combinationData !== 'undefined' && combinationData && combinationData.length")
        print(f"  combinationData: {combination_data}")
        
        # Check specific clustering data
        kmeans_data = await page.evaluate("typeof kMeansClusteringData !== 'undefined' && kMeansClusteringData && kMeansClusteringData.length")
        print(f"  kMeansClusteringData: {kmeans_data}")
        
        # Test Individual tab
        print("\n📊 Testing Individual Macro tab:")
        individual_rows = await page.locator("#individual-tbody tr").count()
        print(f"  Rows in Individual tab: {individual_rows}")
        
        if individual_rows > 0:
            first_row_text = await page.locator("#individual-tbody tr").first.text_content()
            print(f"  First row sample: {first_row_text[:100]}...")
        
        # Test Combination tab
        print("\n📊 Testing Combination tab:")
        await page.click("button:has-text('Combination')")
        await page.wait_for_timeout(1000)
        combo_rows = await page.locator("#combination-tbody tr").count()
        print(f"  Rows in Combination tab: {combo_rows}")
        
        # Test Clustering tab
        print("\n📊 Testing Clustering tab:")
        await page.click("button:has-text('Clustering')")
        await page.wait_for_timeout(1000)
        
        # Test K-Means sub-tab
        await page.click("button:has-text('K-Means')")
        await page.wait_for_timeout(1000)
        kmeans_rows = await page.locator("#macro-clustering-kmeans-tbody tr").count()
        print(f"  K-Means clustering rows: {kmeans_rows}")
        
        # Test ML Analysis tab
        print("\n📊 Testing ML Analysis tab:")
        await page.click("button:has-text('ML Analysis')")
        await page.wait_for_timeout(1000)
        ml_rows = await page.locator("#spy-ml-tbody tr").count()
        print(f"  ML Analysis rows: {ml_rows}")
        
        # Test Technical SPY section
        print("\n📊 Testing Technical SPY section:")
        await page.click("button:has-text('Technical SPY')")
        await page.wait_for_timeout(1000)
        
        # Check Technical Individual
        technical_individual_rows = await page.locator("#technical-individual-tbody tr").count()
        print(f"  Technical Individual rows: {technical_individual_rows}")
        
        # Test Orthogonal Combined
        print("\n📊 Testing Orthogonal Combined tab:")
        await page.click("button:has-text('Orthogonal Combined')")
        await page.wait_for_timeout(2000)
        orthogonal_rows = await page.locator("#orthogonal-combined-tbody tr").count()
        print(f"  Orthogonal Combined rows: {orthogonal_rows}")
        
        # Check console for any errors
        console_messages = []
        def handle_console(msg):
            if msg.type in ['error', 'warning']:
                console_messages.append(f"{msg.type}: {msg.text}")
        
        page.on('console', handle_console)
        await page.wait_for_timeout(2000)
        
        if console_messages:
            print("\n❌ Console errors/warnings:")
            for msg in console_messages[:10]:
                print(f"  {msg}")
        else:
            print("\n✅ No console errors")
        
        # Summary
        total_data_loaded = individual_rows + combo_rows + kmeans_rows + ml_rows + technical_individual_rows + orthogonal_rows
        print(f"\n📈 SUMMARY:")
        print(f"  Total data rows across all tabs: {total_data_loaded}")
        print(f"  Individual tab: {individual_rows} rows")
        print(f"  Combination tab: {combo_rows} rows")
        print(f"  K-Means clustering: {kmeans_rows} rows")
        print(f"  ML Analysis: {ml_rows} rows")
        print(f"  Technical Individual: {technical_individual_rows} rows")
        print(f"  Orthogonal Combined: {orthogonal_rows} rows")
        
        if total_data_loaded > 0:
            print("✅ SUCCESS: Data is loading in dashboard")
        else:
            print("❌ ISSUE: No data found in any tabs")
        
        # Keep browser open for manual inspection
        print(f"\n🔍 Browser staying open for 30 seconds for manual inspection...")
        await page.wait_for_timeout(30000)
        
        return total_data_loaded > 0
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False
    finally:
        await browser.close()

if __name__ == "__main__":
    result = asyncio.run(verify_public_dashboard())
    print(f"\n🎯 Final Result: {'PASS' if result else 'FAIL'}")
    exit(0 if result else 1)