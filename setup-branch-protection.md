# 🔒 Branch Protection Setup Guide

Since branch protection rules must be configured through GitHub's web interface or API, follow these steps:

## 1. Main Branch Protection (Production)

Go to: `https://github.com/murdochfoo/trading-dashboard-public/settings/branches`

**Add protection rule for `main`:**

### Basic Settings
- ✅ Require a pull request before merging
- ✅ Require approvals (minimum 1)
- ✅ Dismiss stale PR approvals when new commits are pushed
- ✅ Require review from code owners

### Status Checks
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- **Required checks:**
  - `test-and-validate`
  - `security-scan`

### Additional Restrictions
- ✅ Restrict pushes that create files larger than 100MB
- ✅ Do not allow bypassing the above settings
- ✅ Include administrators (recommended)

## 2. Staging Branch Protection

**Add protection rule for `staging`:**

### Basic Settings
- ✅ Require a pull request before merging
- ✅ Require approvals (minimum 1)

### Status Checks
- ✅ Require status checks to pass before merging
- **Required checks:**
  - `test-and-validate`

## 3. Development Branch Protection

**Add protection rule for `development`:**

### Basic Settings
- ❌ Allow force pushes (for development flexibility)
- ✅ Allow direct commits (for development work)

### Status Checks
- ✅ Require status checks to pass before merging to staging
- **Required checks:**
  - `test-and-validate`

## 4. Automated Setup via GitHub CLI

If you have GitHub CLI installed, run these commands:

```bash
# Install GitHub CLI first: https://cli.github.com/

# Main branch protection
gh api repos/murdochfoo/trading-dashboard-public/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["test-and-validate","security-scan"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  --field restrictions=null

# Staging branch protection  
gh api repos/murdochfoo/trading-dashboard-public/branches/staging/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["test-and-validate"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null
```

## 5. Verification

After setting up branch protection, verify by trying to:
1. ❌ Push directly to `main` (should fail)
2. ✅ Create PR from `development` → `staging` (should work)
3. ✅ Create PR from `staging` → `main` (should work)
4. ❌ Merge PR without passing tests (should fail)

## Next Steps

1. Set up the branch protection rules above
2. Push branches to GitHub: `git push -u origin development staging`
3. Create your first PR: `development` → `staging`
4. Test the CI/CD pipeline