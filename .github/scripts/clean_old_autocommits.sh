#!/bin/bash
set -e

echo "🔧 Checking environment..."
#git config user.name "github-actions[bot]"
#git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

# 确保仓库完整
if git rev-parse --is-shallow-repository 2>/dev/null | grep -q true; then
  git fetch --unshallow
else
  echo "✅ Repository already complete."
fi

git fetch origin --tags
git reset --hard
git clean -fd

echo "🚀 Running git filter-repo..."
git filter-repo --force --commit-callback "$(cat .github/scripts/filter_commits.py)"

echo "✅ History rewrite completed."

echo "🔗 Restoring origin remote..."
git remote add origin "https://github.com/${GITHUB_REPOSITORY}.git"
git push origin main --force
