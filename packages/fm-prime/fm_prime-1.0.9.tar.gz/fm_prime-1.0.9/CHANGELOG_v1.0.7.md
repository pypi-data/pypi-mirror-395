# Changelog

## [1.0.7] - 2025-11-29 - Python Package (fm-prime)

### Bug Fixes - File Output Count

#### Fixed: Split file cumulative count bug
- **Files**:
  - `fm_prime/textUtils.py`
  - `src/services-py/textUtils.py`
- **Issue**: The final count at the end of each split file showed only the count of primes in that specific file instead of the cumulative total
- **Example**: For 30,100,000 primes (1,863,719 total), the last file showed `(32309)` instead of `(1863719)`
- **Fix**: Changed `data += f"\n({len(current_file)})"` to `data += f"\n({global_index + len(current_file)})"` in both file write locations
- **Impact**: File counts now accurately reflect the cumulative total of all primes across all files

#### Fixed: File sorting issue in read_primes_from_folder
- **Files**:
  - `fm_prime/prime_hyperbolic_optimized.py`
  - `src/services-py/prime_hyperbolic_optimized.py`
- **Issue**: Files were sorted lexicographically (output10.txt, output100.txt, output2.txt) instead of numerically
- **Fix**: Added `extract_number()` function to sort files numerically by extracting the number from filename
- **Impact**: Primes are now read in the correct order when loading from cache

#### Fixed: Filename double extension bug
- **File**: `src/services-py/textUtils.py`
- **Issue**: Files were created with names like `Outputoutput2.txt.txt` due to incorrect filename handling
- **Fix**: Updated `write_data_to_file()` to check if filename already has extension or starts with "output"/"Output"
- **Impact**: Files now have correct names like `output2.txt`

### Testing
- Verified with 30,100,000 primes (1,863,719 total) ✅
- All three implementations produce identical correct results:
  - fm_prime Python package ✓
  - src/services-py Python source ✓
  - Verification: 1,857,859 primes ≤ 30,000,000 (matches known count) ✓

---

## [1.0.3] - 2025-11-29 - Node.js Package (primefm)

### Bug Fixes - File Output Count

#### Fixed: Split file cumulative count bug
- **File**: `src/services/fileOperations.mjs`
- **Issue**: The final count at the end of each split file showed only the count of primes in that specific file instead of the cumulative total
- **Example**: For 30,100,000 primes (1,863,719 total), the last file showed `(32309)` instead of `(1863719)`
- **Fix**: Changed `` data += `\n(${currentFile.length})` `` to `` data += `\n(${globalIndex + currentFile.length})` `` at lines 391 and 419
- **Impact**: File counts now accurately reflect the cumulative total of all primes across all files

### Testing
- Verified with 30,100,000 primes (1,863,719 total) ✅
- Verification: 1,857,859 primes ≤ 30,000,000 (matches known count) ✓
- File format consistency across all output files ✓

### Notes
All fixes maintain backward compatibility. No breaking changes. These fixes ensure accurate prime counting across split files in the caching system used by the hyperbolic sieve implementation.
