# Branch Protection Setup Guide

This document explains how to set up branch protection rules for the main branch to ensure only approved PRs can be merged.

## Why Branch Protection?

Branch protection rules enforce:
- ✅ All changes go through Pull Requests
- ✅ Code review approval is required
- ✅ Automated tests must pass before merging
- ✅ Branches must be up-to-date with main
- ✅ No accidental force pushes

## Step-by-Step Setup

### 1. Navigate to Branch Protection Settings

1. Go to your GitHub repository
2. Click **Settings** (top navigation)
3. Click **Branches** (left sidebar)
4. Under "Branch protection rules", click **Add rule**

### 2. Configure the Main Branch Rule

#### Basic Settings
- **Branch name pattern**: Enter `main`

#### Require a pull request before merging
- ✅ Check: "Require a pull request before merging"
- ✅ Check: "Require approvals" 
  - Set to `1` (at least 1 approval required)
- ✅ Check: "Dismiss stale pull request approvals when new commits are pushed"
- ✅ Check: "Require approval of the most recent reviewers before merging"

#### Require status checks to pass before merging
- ✅ Check: "Require branches to be up to date before merging"
- ✅ Check: "Require status checks to pass before merging"
- Select these status checks:
  - `Test (Python 3.10)` (if you have CI/CD)
  - `Test (Python 3.11)` (if applicable)
  - `Lint` (if you have linting)

#### Rules for administrators
- ☐ Uncheck: "Allow force pushes" (prevent accidental data loss)
- ☐ Uncheck: "Allow deletions" (prevent accidental branch deletion)

#### Other options
- ☐ Uncheck: "Bypass branch protections" (or restrict to nobody)

### 3. Save the Rule

Click **Create** to save the branch protection rule.

## Verification

After setup, verify that:

1. **Direct pushes are blocked**:
   ```bash
   git push origin main
   # Should fail with: "remote: error: protected branch hook declined"
   ```

2. **PR workflow is required**:
   - Create a feature branch
   - Make changes and push
   - Open a PR
   - PR shows "Approval required from @Nikhilsinghbora"
   - Once approved, the Merge button becomes active

## PR Approval Workflow

As the maintainer (@Nikhilsinghbora), follow this workflow:

1. **Contributor opens a PR** from feature branch → main
2. **GitHub requests review** from you (via CODEOWNERS)
3. **You review the changes**:
   - Check code quality
   - Verify security practices
   - Ensure tests pass
4. **Approve or request changes**:
   - Click "Approve" if all looks good
   - Click "Request changes" if modifications needed
5. **Merge when ready**:
   - Once you approve and all checks pass
   - Click the green "Merge pull request" button
   - Select "Squash and merge" or "Create a merge commit"
   - Confirm merge

## Developer Contribution Steps

For contributors, the workflow is:

```bash
# 1. Clone the repo (if new)
git clone https://github.com/Nikhilsinghbora/llm-guardrails.git

# 2. Create a feature branch
git checkout -b feature/my-feature

# 3. Make changes and commit
git add .
git commit -m "feat: add new feature"

# 4. Push to your branch
git push origin feature/my-feature

# 5. Open PR on GitHub (web interface)
# - Go to repo → Pull requests → New pull request
# - Compare: main ← feature/my-feature
# - Add description and create PR

# 6. Wait for review and approval from @Nikhilsinghbora
# - Address any requested changes
# - Re-push when making updates

# 7. PR gets merged and you're done!
```

## Managing Branch Protection Rules

To modify or delete branch protection rules:

1. Go to **Settings** → **Branches**
2. Under "Branch protection rules", click the rule you want to edit
3. Make changes or click **Delete** to remove
4. Click **Save changes**

## Additional Security Measures

### Require CODEOWNERS Review

The `.github/CODEOWNERS` file specifies that @Nikhilsinghbora must review all PRs. GitHub automatically:
- Requests your review on all PRs
- Prevents merging until you approve
- Shows which files require your review

### Required Status Checks

Connect your GitHub repository to:
- **GitHub Actions** - for automated tests and linting
- **Code quality tools** - SonarQube, CodeCov, etc.
- **Security scanners** - Dependabot, SAST tools, etc.

These will automatically block PRs that don't pass required checks.

## Troubleshooting

### "Permission denied" when pushing to main
- This is expected! Use the PR workflow instead
- Create a feature branch, make changes, open a PR

### "Merge blocked - approval required"
- Wait for @Nikhilsinghbora to review and approve your PR
- Address any requested changes
- Re-push changes to your branch

### "Merge blocked - status checks failed"
- Fix the failing tests/linting errors
- Commit and push the fixes
- Checks will automatically re-run

## References

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
- [About CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
