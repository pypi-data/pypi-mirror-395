#!/bin/bash
# Update branch protection to address OpenSSF Scorecard alert #293
# This script updates the main branch protection to require:
# - At least 1 approving review (automated bot review)
# - Last push approval (prevents self-approval of last commit)
# - Linear history (already enforced, but not showing in API?)

set -euo pipefail

echo "Updating branch protection for main branch..."

gh api -X PUT repos/reuteras/miniflux-tui-py/branches/main/protection \
    --input - <<'EOF'
{
    "required_pull_request_reviews": {
        "dismiss_stale_reviews": true,
        "require_code_owner_reviews": false,
        "require_last_push_approval": true,
        "required_approving_review_count": 1
    },
    "restrictions": null,
    "enforce_admins": true,
    "required_linear_history": true,
    "allow_force_pushes": false,
    "allow_deletions": false,
    "required_signatures": true,
    "required_status_checks": {
        "strict": true,
        "contexts": ["MegaLinter", "Check Issue Link"]
    }
}
EOF

echo "✅ Branch protection updated successfully!"
echo ""
echo "New settings:"
echo "- Required approving reviews: 1"
echo "- Dismiss stale reviews: true"
echo "- Last push approval: true (prevents self-approval)"
echo "- Linear history: true (no merge commits)"
echo "- Required signatures: true (GPG/SSH signing)"
echo "- Enforce for admins: true"
echo ""
echo "Note: The maintainer must provide the required approval."
echo "All status checks must pass before approval can be granted."
