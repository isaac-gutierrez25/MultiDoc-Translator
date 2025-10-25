const { readFileSync, existsSync } = require('fs');
const { join } = require('path');

const languages = [
    { code: 'en', bundleFile: 'bundle.l10n.json', packageFile: 'package.nls.json' },
    { code: 'id', bundleFile: 'bundle.l10n.id.json', packageFile: 'package.nls.id.json' },
    { code: 'fr', bundleFile: 'bundle.l10n.fr.json', packageFile: 'package.nls.fr.json' },
    { code: 'es', bundleFile: 'bundle.l10n.es.json', packageFile: 'package.nls.es.json' },
    { code: 'de', bundleFile: 'bundle.l10n.de.json', packageFile: 'package.nls.de.json' },
    { code: 'pt', bundleFile: 'bundle.l10n.pt.json', packageFile: 'package.nls.pt.json' },
    { code: 'ru', bundleFile: 'bundle.l10n.ru.json', packageFile: 'package.nls.ru.json' },
    { code: 'jp', bundleFile: 'bundle.l10n.jp.json', packageFile: 'package.nls.jp.json' },
    { code: 'kr', bundleFile: 'bundle.l10n.kr.json', packageFile: 'package.nls.kr.json' },
    { code: 'pl', bundleFile: 'bundle.l10n.pl.json', packageFile: 'package.nls.pl.json' },
    { code: 'zh', bundleFile: 'bundle.l10n.zh.json', packageFile: 'package.nls.zh.json' }
];

// Helper function to read JSON files with BOM handling
function readJSONFile(filePath) {
    if (!existsSync(filePath)) {
        return null;
    }
    
    let content = readFileSync(filePath, 'utf8');
    
    // Remove UTF-8 BOM if present
    if (content.charCodeAt(0) === 0xFEFF) {
        content = content.slice(1);
    }
    
    return JSON.parse(content);
}

console.log('🧪 Testing Localization Files...\n');

// Test package.nls files
console.log('📦 Testing package.nls files:');
languages.forEach(lang => {
    const packageFile = join('package.nls', lang.packageFile);
    
    console.log(`   📝 Testing ${lang.code.toUpperCase()}:`);
    
    if (existsSync(packageFile)) {
        try {
            const packageData = readJSONFile(packageFile);
            console.log(`      ✅ ${packageFile} - ${Object.keys(packageData).length} strings`);
            
            // Check required fields
            const requiredFields = ['displayName', 'description', 'commands.category'];
            requiredFields.forEach(field => {
                if (!packageData[field]) {
                    console.log(`      ❌ Missing field: ${field}`);
                }
            });
        } catch (error) {
            console.log(`      ❌ JSON Parse Error: ${error.message}`);
        }
    } else {
        console.log(`      ❌ Missing: ${packageFile}`);
    }
});

console.log('\n📚 Testing bundle.l10n files:');
languages.forEach(lang => {
    const bundleFile = join('l10n', lang.bundleFile);
    
    console.log(`   📝 Testing ${lang.code.toUpperCase()}:`);
    
    if (existsSync(bundleFile)) {
        try {
            const bundleData = readJSONFile(bundleFile);
            console.log(`      ✅ ${bundleFile} - ${Object.keys(bundleData).length} strings`);
            
            // Check required fields
            const requiredBundleFields = ['extension.title', 'extension.description', 'actions.generate'];
            requiredBundleFields.forEach(field => {
                if (!bundleData[field]) {
                    console.log(`      ❌ Missing field: ${field}`);
                }
            });
        } catch (error) {
            console.log(`      ❌ JSON Parse Error: ${error.message}`);
        }
    } else {
        console.log(`      ❌ Missing: ${bundleFile}`);
    }
});

console.log('\n🔍 Validating consistency...');

// Check package.nls consistency
const basePackagePath = join('package.nls', 'package.nls.json');
if (existsSync(basePackagePath)) {
    const basePackageData = readJSONFile(basePackagePath);
    
    languages.filter(lang => lang.code !== 'en').forEach(lang => {
        const packageFilePath = join('package.nls', lang.packageFile);
        if (existsSync(packageFilePath)) {
            try {
                const packageData = readJSONFile(packageFilePath);
                const missingKeys = Object.keys(basePackageData).filter(key => !packageData[key]);
                if (missingKeys.length > 0) {
                    console.log(`❌ ${lang.code} package.nls missing keys: ${missingKeys.join(', ')}`);
                }
            } catch (error) {
                console.log(`❌ ${lang.code} package.nls parse error: ${error.message}`);
            }
        }
    });
}

// Check bundle.l10n consistency
const baseBundlePath = join('l10n', 'bundle.l10n.json');
if (existsSync(baseBundlePath)) {
    const baseBundleData = readJSONFile(baseBundlePath);
    
    languages.filter(lang => lang.code !== 'en').forEach(lang => {
        const bundleFilePath = join('l10n', lang.bundleFile);
        if (existsSync(bundleFilePath)) {
            try {
                const bundleData = readJSONFile(bundleFilePath);
                const missingKeys = Object.keys(baseBundleData).filter(key => !bundleData[key]);
                if (missingKeys.length > 0) {
                    console.log(`❌ ${lang.code} bundle.l10n missing keys: ${missingKeys.join(', ')}`);
                }
            } catch (error) {
                console.log(`❌ ${lang.code} bundle.l10n parse error: ${error.message}`);
            }
        }
    });
}

console.log('\n✅ Localization testing completed!');