/**
 * Example: Using the Optimized Hyperbolic Prime Method with Caching (JavaScript)
 *
 * This example demonstrates how to use the production-ready hyperbolic prime
 * detection method with file-level granular caching.
 *
 * Run this file directly:
 *     node examples/example_hyperbolic_optimized.mjs
 */

import {
  sieveHyperbolicOptimized,
  isPrimeHyperbolicOptimized,
  getHyperbolicCacheStats
} from '../src/services/primeHyperbolic.optimized.mjs';


async function demonstrate() {
  console.log('='.repeat(70));
  console.log('OPTIMIZED HYPERBOLIC PRIME DETECTION WITH CACHING (JavaScript)');
  console.log('='.repeat(70));
  console.log();

  // Show cache status
  const stats = getHyperbolicCacheStats();
  console.log('📊 Cache Status:');
  console.log(`   Cached folders: ${stats.folders}`);
  console.log(`   Largest limit: ${stats.largestLimit ? stats.largestLimit.toLocaleString() : 'No cache available'}`);
  console.log();

  // Test 1: Generate primes with caching
  console.log('TEST 1: Generate primes up to 100,000');
  console.log('-'.repeat(70));

  const start1 = Date.now();
  const primes = sieveHyperbolicOptimized('100000');
  const elapsed1 = Date.now() - start1;

  console.log(`Found ${primes.length.toLocaleString()} primes in ${elapsed1}ms`);
  console.log(`First 10: [${primes.slice(0, 10).join(', ')}]`);
  console.log(`Last 10: [${primes.slice(-10).join(', ')}]`);
  console.log(`Verification: ${primes.length === 9592} (expected 9,592)`);
  console.log();

  // Test 2: Check individual primes
  console.log('TEST 2: Check individual numbers');
  console.log('-'.repeat(70));

  const testNumbers = [
    ['15485863', true, '1 millionth prime'],
    ['999983', true, 'largest prime < 1M'],
    ['15485864', false, 'composite number'],
    ['1000000', false, 'composite number'],
  ];

  for (const [num, expected, desc] of testNumbers) {
    const start = Date.now();
    const result = isPrimeHyperbolicOptimized(num);
    const elapsed = Date.now() - start;

    const status = result === expected ? '✓' : '✗';
    const resultStr = result ? 'PRIME' : 'COMPOSITE';
    console.log(`${status} ${num.padStart(10)} (${desc})`);
    console.log(`  Result: ${resultStr}, Time: ${elapsed.toFixed(3)}ms`);
  }

  console.log();

  // Final cache stats
  const finalStats = getHyperbolicCacheStats();
  console.log('📊 Final Cache Status:');
  console.log(`   Cached folders: ${finalStats.folders}`);
  console.log(`   Largest limit: ${finalStats.largestLimit ? finalStats.largestLimit.toLocaleString() : 'No cache available'}`);
  console.log();

  // Verification table
  console.log('Known Prime Counts for Verification:');
  console.log('─'.repeat(70));
  console.log('Limit          | Expected Count | Status');
  console.log('─'.repeat(70));

  const knownCounts = [
    [100, 25],
    [1000, 168],
    [10000, 1229],
    [100000, 9592],
  ];

  for (const [limitVal, expectedCount] of knownCounts) {
    const actualPrimes = primes.filter(p => p <= BigInt(limitVal));
    const actualCount = actualPrimes.length;
    const status = actualCount === expectedCount ? '✓ PASS' : '✗ FAIL';
    console.log(`${limitVal.toLocaleString().padStart(14)} | ${expectedCount.toLocaleString().padStart(14)} | ${status} (actual: ${actualCount.toLocaleString()})`);
  }

  console.log('─'.repeat(70));
}


function basicUsageExamples() {
  console.log('\n' + '='.repeat(70));
  console.log('BASIC USAGE EXAMPLES');
  console.log('='.repeat(70));
  console.log();

  console.log('Example 1: Check if a number is prime');
  console.log('-'.repeat(70));
  console.log('import { isPrimeHyperbolicOptimized } from \'./src/services/primeHyperbolic.optimized.mjs\';');
  console.log();
  console.log('const result = isPrimeHyperbolicOptimized(\'999983\');');
  console.log(`>>> ${isPrimeHyperbolicOptimized('999983')}  // true`);
  console.log();

  console.log('Example 2: Generate all primes up to N');
  console.log('-'.repeat(70));
  console.log('import { sieveHyperbolicOptimized } from \'./src/services/primeHyperbolic.optimized.mjs\';');
  console.log();
  console.log('const primes = sieveHyperbolicOptimized(\'1000\');');
  const primes1000 = sieveHyperbolicOptimized('1000');
  console.log(`>>> Found ${primes1000.length} primes`);
  console.log(`>>> [${primes1000.slice(0, 10).join(', ')}] ...`);
  console.log();

  console.log('Example 3: Check cache status');
  console.log('-'.repeat(70));
  console.log('import { getHyperbolicCacheStats } from \'./src/services/primeHyperbolic.optimized.mjs\';');
  console.log();
  console.log('const stats = getHyperbolicCacheStats();');
  const stats = getHyperbolicCacheStats();
  console.log(`>>> Cached folders: ${stats.folders}`);
  console.log(`>>> Largest cached: ${stats.largestLimit ? stats.largestLimit.toLocaleString() : 'No cache'}`);
  console.log();
}


// Run demonstrations
demonstrate().then(() => {
  basicUsageExamples();
}).catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
