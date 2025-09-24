---
on:
  issues:
    types: [opened, reopened]
permissions:
  contents: read
  actions: read
engine: codex
network: defaults
tools:
  github:
    allowed:
      - get_issue
      - add_issue_comment
      - create_issue
safe-outputs:
  add-comment:
  update-issue:
  add-labels:
---

# issue-triage

Scan the existing issues and highlight if this is a potential duplicate by commenting on the issue and adding a label.

<!--
## TODO: Customize this workflow

The workflow has been generated based on your selections. Consider adding:

- [ ] More specific instructions for the AI
- [ ] Error handling requirements
- [ ] Output format specifications
- [ ] Integration with other workflows
- [ ] Testing and validation steps

## Configuration Summary

- **Trigger**: Issue opened or reopened
- **AI Engine**: claude
- **Tools**: github
- **Safe Outputs**: add-comment, update-issue, add-labels
- **Network Access**: defaults

## Next Steps

1. Review and customize the workflow content above
2. Remove TODO sections when ready
3. Run `gh aw compile` to generate the GitHub Actions workflow
4. Test the workflow with a manual trigger or appropriate event
-->
