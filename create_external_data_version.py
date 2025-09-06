#!/usr/bin/env python3
"""
Create version that loads data from external JSON to avoid truncation issues
"""

import json
import re

def create_external_data_version():
    print("🔧 Creating external data loading version...")
    
    # Read the current HTML file
    with open('index.html', 'r') as f:
        content = f.read()
    
    # Extract all the data arrays from the JavaScript
    data_arrays = {}
    
    # Find each const data array definition
    array_patterns = [
        'individualData',
        'combinationData', 
        'spyBenchmark',
        'macroClusteringKmeansData',
        'macroClusteringHierarchicalData',
        'macroClusteringPcaData', 
        'macroClusteringDbscanData',
        'macroClusteringGaussianData',
        'macroClusteringSpectralData',
        'spyMLData',
        'technicalIndividualData',
        'technicalCombinationData',
        'spyClusteringData',
        'macroOrthogonalData',
        'spyOrthogonalData',
        'combinedOrthogonalData'
    ]
    
    for array_name in array_patterns:
        pattern = rf'const {array_name} = (\[.*?\]);'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            array_str = match.group(1)
            try:
                # Convert JavaScript array to Python and back to JSON
                # This is a simple approach - for production, would use proper JS parser
                array_str = array_str.replace('true', 'True').replace('false', 'False')
                array_data = eval(array_str)
                data_arrays[array_name] = array_data
                print(f"  ✅ Extracted {array_name}: {len(array_data) if isinstance(array_data, list) else 1} items")
            except Exception as e:
                print(f"  ⚠️  Failed to parse {array_name}: {e}")
    
    # Save data to external JSON file
    with open('dashboard_data.json', 'w') as f:
        json.dump(data_arrays, f, separators=(',', ':'))  # Compact format
    
    print(f"💾 Saved {len(data_arrays)} data arrays to dashboard_data.json")
    
    # Create new HTML with external data loading
    new_js_section = """
        // External data loading
        let individualData = [];
        let combinationData = [];
        let spyBenchmark = [];
        let macroClusteringKmeansData = [];
        let macroClusteringHierarchicalData = [];
        let macroClusteringPcaData = [];
        let macroClusteringDbscanData = [];
        let macroClusteringGaussianData = [];
        let macroClusteringSpectralData = [];
        let spyMLData = [];
        let technicalIndividualData = [];
        let technicalCombinationData = [];
        let spyClusteringData = [];
        let macroOrthogonalData = [];
        let spyOrthogonalData = [];
        let combinedOrthogonalData = [];
        
        // Load external data
        async function loadDashboardData() {
            try {
                console.log('🔄 Loading dashboard data...');
                const response = await fetch('dashboard_data.json');
                const data = await response.json();
                
                // Assign data to global variables
                individualData = data.individualData || [];
                combinationData = data.combinationData || [];
                spyBenchmark = data.spyBenchmark || [];
                macroClusteringKmeansData = data.macroClusteringKmeansData || [];
                macroClusteringHierarchicalData = data.macroClusteringHierarchicalData || [];
                macroClusteringPcaData = data.macroClusteringPcaData || [];
                macroClusteringDbscanData = data.macroClusteringDbscanData || [];
                macroClusteringGaussianData = data.macroClusteringGaussianData || [];
                macroClusteringSpectralData = data.macroClusteringSpectralData || [];
                spyMLData = data.spyMLData || [];
                technicalIndividualData = data.technicalIndividualData || [];
                technicalCombinationData = data.technicalCombinationData || [];
                spyClusteringData = data.spyClusteringData || [];
                macroOrthogonalData = data.macroOrthogonalData || [];
                spyOrthogonalData = data.spyOrthogonalData || [];
                combinedOrthogonalData = data.combinedOrthogonalData || [];
                
                console.log('✅ Dashboard data loaded successfully!');
                console.log('📊 Individual strategies:', individualData.length);
                console.log('📊 Combination strategies:', combinationData.length);
                
                // Initialize tables after data is loaded
                initializeTables();
                
            } catch (error) {
                console.error('❌ Failed to load dashboard data:', error);
                
                // Fallback to minimal demo data
                individualData = [
                    {
                        "indicator": "SPY Buy & Hold",
                        "transform_type": "benchmark",
                        "terminal_value": 43265.41,
                        "annual_return": 0.10234,
                        "volatility": 0.15435,
                        "max_drawdown": -0.18766,
                        "sharpe_ratio": 0.6634,
                        "sortino_ratio": 0.9845,
                        "calmar_ratio": 0.5453,
                        "win_rate": 0.5234,
                        "total_trades": 366,
                        "avg_trades_per_year": 24.4
                    }
                ];
                
                console.log('🔄 Using fallback demo data');
                initializeTables();
            }
        }
        
        // Initialize all tables
        function initializeTables() {
            console.log('🚀 Initializing dashboard tables...');
            
            if (typeof createMacroIndividualTable === 'function' && individualData) {
                console.log('Creating macro individual table with', individualData.length, 'strategies');
                createMacroIndividualTable(individualData);
            }
            
            if (typeof createMacroCombinationTable === 'function' && combinationData) {
                console.log('Creating macro combination table with', combinationData.length, 'strategies');
                createMacroCombinationTable(combinationData);
            }
            
            if (typeof createMacroClusteringTable === 'function' && macroClusteringKmeansData) {
                console.log('Creating macro clustering kmeans table with', macroClusteringKmeansData.length, 'strategies');
                createMacroClusteringTable(macroClusteringKmeansData, 'kmeans');
            }
            
            if (typeof createMacroClusteringTable === 'function' && macroClusteringHierarchicalData) {
                console.log('Creating macro clustering hierarchical table with', macroClusteringHierarchicalData.length, 'strategies');
                createMacroClusteringTable(macroClusteringHierarchicalData, 'hierarchical');
            }
            
            if (typeof createMacroClusteringTable === 'function' && macroClusteringPcaData) {
                console.log('Creating macro clustering pca table with', macroClusteringPcaData.length, 'strategies');
                createMacroClusteringTable(macroClusteringPcaData, 'pca');
            }
            
            if (typeof createMacroClusteringTable === 'function' && macroClusteringDbscanData) {
                console.log('Creating macro clustering dbscan table with', macroClusteringDbscanData.length, 'strategies');
                createMacroClusteringTable(macroClusteringDbscanData, 'dbscan');
            }
            
            if (typeof createMacroClusteringTable === 'function' && macroClusteringGaussianData) {
                console.log('Creating macro clustering gaussian table with', macroClusteringGaussianData.length, 'strategies');
                createMacroClusteringTable(macroClusteringGaussianData, 'gaussian');
            }
            
            if (typeof createMacroClusteringTable === 'function' && macroClusteringSpectralData) {
                console.log('Creating macro clustering spectral table with', macroClusteringSpectralData.length, 'strategies');
                createMacroClusteringTable(macroClusteringSpectralData, 'spectral');
            }
            
            if (typeof createSPYMLTable === 'function' && spyMLData) {
                console.log('Creating SPY ML table with', spyMLData.length, 'strategies');
                createSPYMLTable(spyMLData);
            }
            
            if (typeof createSPYClusteringTable === 'function' && spyClusteringData) {
                console.log('Creating SPY clustering table with', spyClusteringData.length, 'strategies');
                createSPYClusteringTable(spyClusteringData);
            }
            
            if (typeof createOrthogonalTable === 'function' && macroOrthogonalData) {
                console.log('Creating macro orthogonal table with', macroOrthogonalData.length, 'strategies');
                createOrthogonalTable(macroOrthogonalData, 'macro-orthogonal-tbody');
            }
            
            if (typeof createOrthogonalTable === 'function' && spyOrthogonalData) {
                console.log('Creating SPY orthogonal table with', spyOrthogonalData.length, 'strategies');
                createOrthogonalTable(spyOrthogonalData, 'spy-orthogonal-tbody');
            }
            
            if (typeof createOrthogonalTable === 'function' && combinedOrthogonalData) {
                console.log('Creating combined orthogonal table with', combinedOrthogonalData.length, 'strategies');
                createOrthogonalTable(combinedOrthogonalData, 'orthogonal-combined-tbody');
            }
            
            console.log('Enhanced dashboard with clustering and ML analysis initialization complete!');
        }
    """
    
    # Find and replace the data section
    script_start = content.find('<script>')
    data_start = content.find('// Data arrays', script_start)
    
    if data_start == -1:
        data_start = content.find('const individualData', script_start)
    
    if data_start != -1:
        # Find where the functions start
        func_start = content.find('function formatCurrency', data_start)
        if func_start == -1:
            func_start = content.find('function ', data_start)
        
        if func_start != -1:
            # Replace the data section with external loading
            new_content = content[:data_start] + new_js_section + "\n        " + content[func_start:]
            
            # Update the DOMContentLoaded handler
            old_init = 'document.addEventListener(\'DOMContentLoaded\', function() {'
            new_init = 'document.addEventListener(\'DOMContentLoaded\', function() {\n            loadDashboardData(); // Load external data instead of inline initialization'
            new_content = new_content.replace(old_init, new_init)
            
            # Remove the old initialization calls (they'll be in initializeTables now)
            lines_to_remove = [
                'console.log(\'Initializing final enhanced dashboard tables...\');',
                'if (typeof createMacroIndividualTable === \'function\' && individualData) {',
                'console.log(\'Creating macro individual table with\', individualData.length, \'strategies\');',
                'createMacroIndividualTable(individualData);'
            ]
            
            for line in lines_to_remove:
                new_content = new_content.replace('            ' + line + '\n', '')
            
            # Write the new file
            with open('index.html', 'w') as f:
                f.write(new_content)
            
            print("✅ Created external data loading version")
            file_size_kb = len(new_content) / 1024
            print(f"📏 New HTML size: {file_size_kb:.1f}KB (reduced from {len(content)/1024:.1f}KB)")
            return True
    
    print("❌ Failed to find data section to replace")
    return False

if __name__ == "__main__":
    success = create_external_data_version()
    exit(0 if success else 1)