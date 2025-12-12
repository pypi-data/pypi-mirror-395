# Publishing Guide: fm-prime

This guide explains how to publish `fm-prime` to both npm (JavaScript) and PyPI (Python).

---

## Prerequisites

### For npm (JavaScript)
1. **Node.js** installed (v14 or higher)
2. **npm account**: Create at https://www.npmjs.com/signup
3. **npm CLI** logged in

### For PyPI (Python)
1. **Python** installed (3.7 or higher)
2. **PyPI account**: Create at https://pypi.org/account/register/
3. **TestPyPI account** (optional, for testing): https://test.pypi.org/account/register/
4. **Build tools** installed

---

## Part 1: Publishing to npm (JavaScript)

### Step 1: Login to npm

```bash
npm login
```

Enter your npm username, password, and email when prompted.

### Step 2: Test Your Package Locally

```bash
# Test if the package builds correctly
npm pack

# This creates a .tgz file you can inspect
# Test install it locally
npm install ./fm-prime-1.0.0.tgz
```

### Step 3: Update Package Version (if needed)

```bash
# For patch release (1.0.0 -> 1.0.1)
npm version patch

# For minor release (1.0.0 -> 1.1.0)
npm version minor

# For major release (1.0.0 -> 2.0.0)
npm version major
```

### Step 4: Publish to npm

```bash
# Publish to npm
npm publish

# For scoped packages (if you want @yourusername/fm-prime)
npm publish --access public
```

### Step 5: Verify Publication

Visit https://www.npmjs.com/package/fm-prime to see your package!

### Step 6: Test Installation

```bash
# In a different directory
npm install fm-prime

# Test the CLI
npx fm-prime

# Test in code
node
> const { isPrimeOptimized } = await import('fm-prime/checker');
> console.log(isPrimeOptimized('17'));
```

---

## Part 2: Publishing to PyPI (Python)

### Step 1: Install Build Tools

```bash
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build twine
```

### Step 2: Build the Distribution

```bash
# Build the package
python3 -m build

# This creates:
# - dist/fm_prime-1.0.0-py3-none-any.whl
# - dist/fm-prime-1.0.0.tar.gz
```

### Step 3: Test on TestPyPI (Optional but Recommended)

```bash
# Upload to TestPyPI first
python3 -m twine upload --repository testpypi dist/*

# Test install from TestPyPI
python3 -m pip install --index-url https://test.pypi.org/simple/ fm-prime
```

### Step 4: Publish to PyPI

```bash
# Upload to PyPI
python3 -m twine upload dist/*
```

You'll be prompted for your PyPI username and password.

**Alternative: Use API Token (More Secure)**

1. Go to https://pypi.org/manage/account/token/
2. Create a new API token
3. Use the token when prompted:
   - Username: `__token__`
   - Password: `pypi-...` (your token)

Or create `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...your-token-here
```

### Step 5: Verify Publication

Visit https://pypi.org/project/fm-prime/ to see your package!

### Step 6: Test Installation

```bash
# In a different directory or virtualenv
pip install fm-prime

# Test the CLI
fm-prime

# Test in code
python3
>>> from fm_prime import is_prime_optimized, sieve_wheel210
>>> print(is_prime_optimized(17))
>>> primes = sieve_wheel210(100)
>>> print(len(primes))
```

---

## Updating Your Package

### npm Update

```bash
# 1. Make your changes
# 2. Update version
npm version patch  # or minor, or major

# 3. Publish
npm publish
```

### PyPI Update

```bash
# 1. Make your changes
# 2. Update version in setup.py and pyproject.toml
# 3. Clean old builds
rm -rf dist/ build/ *.egg-info

# 4. Build new distribution
python3 -m build

# 5. Upload
python3 -m twine upload dist/*
```

---

## Best Practices

### Before Publishing

1. ✅ **Test locally** - Make sure everything works
2. ✅ **Update README** - Ensure documentation is current
3. ✅ **Update CHANGELOG** - Document what changed
4. ✅ **Run tests** - Verify all tests pass
5. ✅ **Check version number** - Follow semantic versioning
6. ✅ **Review .npmignore / MANIFEST.in** - Don't include unnecessary files

### Semantic Versioning

- **MAJOR** (1.0.0 -> 2.0.0): Breaking changes
- **MINOR** (1.0.0 -> 1.1.0): New features, backward compatible
- **PATCH** (1.0.0 -> 1.0.1): Bug fixes, backward compatible

### Git Tags

```bash
# After publishing, tag the release
git tag v1.0.0
git push origin v1.0.0
```

---

## Troubleshooting

### npm Issues

**Error: Package already exists**
- You can't publish the same version twice
- Increment version with `npm version patch`

**Error: 403 Forbidden**
- Make sure you're logged in: `npm whoami`
- Re-login: `npm login`

**Error: Name taken**
- Choose a different package name in package.json
- Or use a scoped name: `@yourusername/fm-prime`

### PyPI Issues

**Error: File already exists**
- You can't upload the same version twice
- Update version in setup.py and pyproject.toml
- Clean old builds: `rm -rf dist/ build/`

**Error: 403 Forbidden**
- Check your username/password
- Consider using API token instead

**ModuleNotFoundError when importing**
- Check package structure with __init__.py
- Verify MANIFEST.in includes all necessary files

---

## Package URLs After Publishing

### npm
- **Package**: https://www.npmjs.com/package/fm-prime
- **Install**: `npm install fm-prime`
- **CLI**: `npx fm-prime`

### PyPI
- **Package**: https://pypi.org/project/fm-prime/
- **Install**: `pip install fm-prime`
- **CLI**: `fm-prime`

---

## Security Notes

1. **Never commit API tokens** to git
2. **Use .gitignore** to exclude sensitive files
3. **Use 2FA** on npm and PyPI accounts
4. **Review your package** before publishing
5. **Keep dependencies updated** for security

---

## Automation (Optional)

You can automate publishing with GitHub Actions:

### npm GitHub Action

Create `.github/workflows/npm-publish.yml`:

```yaml
name: Publish to npm

on:
  release:
    types: [created]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### PyPI GitHub Action

Create `.github/workflows/pypi-publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: python -m pip install build twine
      - run: python -m build
      - run: python -m twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
```

---

## Next Steps

1. ✅ Create npm and PyPI accounts
2. ✅ Test your packages locally
3. ✅ Publish to npm: `npm publish`
4. ✅ Publish to PyPI: `python3 -m twine upload dist/*`
5. ✅ Share your package with the world! 🎉

For questions or issues, open a GitHub issue at:
https://github.com/faridmasjedi/fm-prime/issues
