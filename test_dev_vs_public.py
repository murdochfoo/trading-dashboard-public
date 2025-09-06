#!/usr/bin/env python3
"""
Test development version vs public version to see what changed
"""

import asyncio
from playwright.async_api import async_playwright

async def test_both_versions():
    print("🔍 Testing Development vs Public Versions")
    print("=" * 60)
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    
    results = {}
    
    # Test development version (local)
    print("\n📊 Testing Development Version (localhost:8092)")
    print("-" * 40)
    
    page = await context.new_page()
    try:
        await page.goto("http://localhost:8092", timeout=10000)
        await page.wait_for_timeout(3000)
        
        # Check data arrays
        dev_individual = await page.evaluate("typeof individualData !== 'undefined' && individualData ? individualData.length : 0")
        dev_combination = await page.evaluate("typeof combinationData !== 'undefined' && combinationData ? combinationData.length : 0")
        
        # Check table rows
        dev_individual_rows = await page.locator("#individual-tbody tr").count()
        dev_combo_rows = await page.locator("#combination-tbody tr").count()
        
        # Check functions
        dev_create_func = await page.evaluate("typeof createMacroIndividualTable === 'function'")
        dev_populate_func = await page.evaluate("typeof populateTable === 'function'")
        
        results['dev'] = {
            'individual_data': dev_individual,
            'combination_data': dev_combination,
            'individual_rows': dev_individual_rows,
            'combo_rows': dev_combo_rows,
            'create_func': dev_create_func,
            'populate_func': dev_populate_func
        }
        
        print(f"  📊 Individual data: {dev_individual}")
        print(f"  📊 Combination data: {dev_combination}")
        print(f"  📋 Individual table rows: {dev_individual_rows}")
        print(f"  📋 Combination table rows: {dev_combo_rows}")
        print(f"  🔧 createMacroIndividualTable: {dev_create_func}")
        print(f"  🔧 populateTable: {dev_populate_func}")
        
    except Exception as e:
        print(f"  ❌ Development version error: {e}")
        results['dev'] = {'error': str(e)}
    finally:
        await page.close()
    
    # Test public version (GitHub Pages)
    print("\n🌐 Testing Public Version (GitHub Pages)")
    print("-" * 40)
    
    page = await context.new_page()
    try:
        await page.goto("https://murdochfoo.github.io/trading-dashboard-public/", timeout=15000)
        await page.wait_for_timeout(5000)
        
        # Check data arrays
        pub_individual = await page.evaluate("typeof individualData !== 'undefined' && individualData ? individualData.length : 0")
        pub_combination = await page.evaluate("typeof combinationData !== 'undefined' && combinationData ? combinationData.length : 0")
        
        # Check table rows
        pub_individual_rows = await page.locator("#individual-tbody tr").count()
        pub_combo_rows = await page.locator("#combination-tbody tr").count()
        
        # Check functions
        pub_create_func = await page.evaluate("typeof createMacroIndividualTable === 'function'")
        pub_populate_func = await page.evaluate("typeof populateTable === 'function'")
        
        results['public'] = {
            'individual_data': pub_individual,
            'combination_data': pub_combination,
            'individual_rows': pub_individual_rows,
            'combo_rows': pub_combo_rows,
            'create_func': pub_create_func,
            'populate_func': pub_populate_func
        }
        
        print(f"  📊 Individual data: {pub_individual}")
        print(f"  📊 Combination data: {pub_combination}")
        print(f"  📋 Individual table rows: {pub_individual_rows}")
        print(f"  📋 Combination table rows: {pub_combo_rows}")
        print(f"  🔧 createMacroIndividualTable: {pub_create_func}")
        print(f"  🔧 populateTable: {pub_populate_func}")
        
    except Exception as e:
        print(f"  ❌ Public version error: {e}")
        results['public'] = {'error': str(e)}
    finally:
        await page.close()
    
    # Compare results
    print("\n🔍 COMPARISON ANALYSIS")
    print("=" * 40)
    
    if 'error' not in results.get('dev', {}) and 'error' not in results.get('public', {}):
        dev = results['dev']
        pub = results['public']
        
        print(f"📊 Individual Data:  Dev={dev['individual_data']} vs Public={pub['individual_data']}")
        print(f"📋 Individual Rows:  Dev={dev['individual_rows']} vs Public={pub['individual_rows']}")
        print(f"📊 Combination Data: Dev={dev['combination_data']} vs Public={pub['combination_data']}")
        print(f"📋 Combination Rows: Dev={dev['combo_rows']} vs Public={pub['combo_rows']}")
        print(f"🔧 Create Function:  Dev={dev['create_func']} vs Public={pub['create_func']}")
        print(f"🔧 Populate Function: Dev={dev['populate_func']} vs Public={pub['populate_func']}")
        
        # Identify key differences
        data_working = dev['individual_data'] > 0 and dev['individual_rows'] > 0
        public_broken = pub['individual_data'] > 0 and pub['individual_rows'] == 0
        
        if data_working and public_broken:
            print("\n🎯 KEY FINDING: Development works, Public has data but no table rows!")
            print("   This suggests table initialization/population is broken in public version")
        elif not data_working:
            print("\n⚠️  Both versions appear to have issues")
        else:
            print("\n✅ Both versions working similarly")
        
        success = dev.get('individual_rows', 0) > 0 or pub.get('individual_rows', 0) > 0
        
    else:
        print("❌ Unable to compare due to errors")
        success = False
    
    await browser.close()
    return success

if __name__ == "__main__":
    result = asyncio.run(test_both_versions())
    exit(0 if result else 1)