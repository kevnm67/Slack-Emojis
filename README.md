# Slack-Emojis

[![CI](https://github.com/kevnm67/Slack-Emojis/actions/workflows/ci.yml/badge.svg)](https://github.com/kevnm67/Slack-Emojis/actions/workflows/ci.yml)
[![Maintainability](https://qlty.sh/gh/kevnm67/projects/Slack-Emojis/maintainability.svg)](https://qlty.sh/gh/kevnm67/projects/Slack-Emojis)
[![Code Coverage](https://qlty.sh/gh/kevnm67/projects/Slack-Emojis/coverage.svg)](https://qlty.sh/gh/kevnm67/projects/Slack-Emojis)

Emoji's commonly used for Slack, Jira, etc.

## Table of contents

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Table of contents](#table-of-contents)
- [Updating the table](#updating-the-table)
- [Emojis](#emojis)
- [Attribution](#attribution)

<!-- /TOC -->

See the [wiki](https://github.com/kevnm67/Slack-Emojis/wiki) for architecture and setup docs.

## Updating the table

```bash
make setup   # create venv, install dev deps, install pre-commit hooks
make build   # regenerate this table from Emojis/
SLACK_TOKEN=xoxp-... make fetch  # or: .venv/bin/slack-emojis-fetch
```

[`src/slack_emojis/update_emojis.py`](./src/slack_emojis/update_emojis.py) scans the `Emojis/`
directory, sanitizes filenames to lowercase snake_case, and regenerates the table below.
[`src/slack_emojis/fetch_slack_emojis.py`](./src/slack_emojis/fetch_slack_emojis.py) pulls custom
emojis from a Slack workspace via `emoji.list`, then chains into the same regeneration.

## Emojis

| Emoji              | Preview |
| ------------------ | ------- |
| 1password | <img src="./Emojis/1password.png" alt="1password" width="28"> |
| agile | <img src="./Emojis/agile.png" alt="agile" width="28"> |
| android | <img src="./Emojis/android.png" alt="android" width="28"> |
| api | <img src="./Emojis/api.png" alt="api" width="28"> |
| apple_inc | <img src="./Emojis/apple_inc.png" alt="apple_inc" width="28"> |
| apple_logo_classic | <img src="./Emojis/apple_logo_classic.png" alt="apple_logo_classic" width="28"> |
| aws | <img src="./Emojis/aws.png" alt="aws" width="28"> |
| bananadance | <img src="./Emojis/bananadance.gif" alt="bananadance" width="28"> |
| bbq | <img src="./Emojis/bbq.png" alt="bbq" width="28"> |
| bob_ross | <img src="./Emojis/bob_ross.png" alt="bob_ross" width="28"> |
| bob_ross2 | <img src="./Emojis/bob_ross2.png" alt="bob_ross2" width="28"> |
| carlton | <img src="./Emojis/carlton.gif" alt="carlton" width="28"> |
| circleci | <img src="./Emojis/circleci.png" alt="circleci" width="28"> |
| circleci_fail | <img src="./Emojis/circleci_fail.png" alt="circleci_fail" width="28"> |
| circleci_pass | <img src="./Emojis/circleci_pass.png" alt="circleci_pass" width="28"> |
| claude | <img src="./Emojis/claude.png" alt="claude" width="28"> |
| claude_code | <img src="./Emojis/claude_code.png" alt="claude_code" width="28"> |
| claude_code_animated | <img src="./Emojis/claude_code_animated.gif" alt="claude_code_animated" width="28"> |
| claude_code_incognito | <img src="./Emojis/claude_code_incognito.png" alt="claude_code_incognito" width="28"> |
| claude_dancing | <img src="./Emojis/claude_dancing.gif" alt="claude_dancing" width="28"> |
| claude_fail | <img src="./Emojis/claude_fail.png" alt="claude_fail" width="28"> |
| claude_heart | <img src="./Emojis/claude_heart.png" alt="claude_heart" width="28"> |
| claude_magic | <img src="./Emojis/claude_magic.gif" alt="claude_magic" width="28"> |
| claude_sob | <img src="./Emojis/claude_sob.png" alt="claude_sob" width="28"> |
| clawd | <img src="./Emojis/clawd.png" alt="clawd" width="28"> |
| database | <img src="./Emojis/database.png" alt="database" width="28"> |
| datadog | <img src="./Emojis/datadog.png" alt="datadog" width="28"> |
| datagrip | <img src="./Emojis/datagrip.png" alt="datagrip" width="28"> |
| delay | <img src="./Emojis/delay.png" alt="delay" width="28"> |
| dev | <img src="./Emojis/dev.png" alt="dev" width="28"> |
| devito | <img src="./Emojis/devito.png" alt="devito" width="28"> |
| doh | <img src="./Emojis/doh.png" alt="doh" width="28"> |
| dops | <img src="./Emojis/dops.png" alt="dops" width="28"> |
| downvote | <img src="./Emojis/downvote.png" alt="downvote" width="28"> |
| excellent_mrburns | <img src="./Emojis/excellent_mrburns.gif" alt="excellent_mrburns" width="28"> |
| fidget | <img src="./Emojis/fidget.gif" alt="fidget" width="28"> |
| figma | <img src="./Emojis/figma.png" alt="figma" width="28"> |
| fry | <img src="./Emojis/fry.png" alt="fry" width="28"> |
| ghostbusters | <img src="./Emojis/ghostbusters.png" alt="ghostbusters" width="28"> |
| github | <img src="./Emojis/github.png" alt="github" width="28"> |
| github_machine | <img src="./Emojis/github_machine.png" alt="github_machine" width="28"> |
| github_octocat | <img src="./Emojis/github_octocat.png" alt="github_octocat" width="28"> |
| github_octogirl | <img src="./Emojis/github_octogirl.png" alt="github_octogirl" width="28"> |
| githug | <img src="./Emojis/githug.png" alt="githug" width="28"> |
| grafana | <img src="./Emojis/grafana.png" alt="grafana" width="28"> |
| hashicorp_terraform | <img src="./Emojis/hashicorp_terraform.png" alt="hashicorp_terraform" width="28"> |
| homer | <img src="./Emojis/homer.gif" alt="homer" width="28"> |
| im_a_developer_ralph | <img src="./Emojis/im_a_developer_ralph.png" alt="im_a_developer_ralph" width="28"> |
| jaill | <img src="./Emojis/jaill.png" alt="jaill" width="28"> |
| jean_claude_code_van_damme | <img src="./Emojis/jean_claude_code_van_damme.png" alt="jean_claude_code_van_damme" width="28"> |
| jira_bug | <img src="./Emojis/jira_bug.png" alt="jira_bug" width="28"> |
| jira_epic | <img src="./Emojis/jira_epic.png" alt="jira_epic" width="28"> |
| jira_escalation | <img src="./Emojis/jira_escalation.png" alt="jira_escalation" width="28"> |
| jira_subtask | <img src="./Emojis/jira_subtask.png" alt="jira_subtask" width="28"> |
| jira_task | <img src="./Emojis/jira_task.png" alt="jira_task" width="28"> |
| johnwick | <img src="./Emojis/johnwick.jpg" alt="johnwick" width="28"> |
| johnwickq | <img src="./Emojis/johnwickq.png" alt="johnwickq" width="28"> |
| keanu | <img src="./Emojis/keanu.png" alt="keanu" width="28"> |
| kong_gateway | <img src="./Emojis/kong_gateway.png" alt="kong_gateway" width="28"> |
| linkedin | <img src="./Emojis/linkedin.png" alt="linkedin" width="28"> |
| mac_finder | <img src="./Emojis/mac_finder.gif" alt="mac_finder" width="28"> |
| magic_school_bus | <img src="./Emojis/magic_school_bus.png" alt="magic_school_bus" width="28"> |
| mainframe | <img src="./Emojis/mainframe.png" alt="mainframe" width="28"> |
| mario | <img src="./Emojis/mario.png" alt="mario" width="28"> |
| mario_luigi_dance | <img src="./Emojis/mario_luigi_dance.gif" alt="mario_luigi_dance" width="28"> |
| new_relic | <img src="./Emojis/new_relic.png" alt="new_relic" width="28"> |
| old_man_yells_at_agentforce | <img src="./Emojis/old_man_yells_at_agentforce.png" alt="old_man_yells_at_agentforce" width="28"> |
| old_man_yells_at_atlassian | <img src="./Emojis/old_man_yells_at_atlassian.png" alt="old_man_yells_at_atlassian" width="28"> |
| old_man_yells_at_azure | <img src="./Emojis/old_man_yells_at_azure.png" alt="old_man_yells_at_azure" width="28"> |
| old_man_yells_at_azure_devops | <img src="./Emojis/old_man_yells_at_azure_devops.png" alt="old_man_yells_at_azure_devops" width="28"> |
| old_man_yells_at_circleci | <img src="./Emojis/old_man_yells_at_circleci.png" alt="old_man_yells_at_circleci" width="28"> |
| old_man_yells_at_power_bi | <img src="./Emojis/old_man_yells_at_power_bi.png" alt="old_man_yells_at_power_bi" width="28"> |
| old_man_yells_at_salesforce | <img src="./Emojis/old_man_yells_at_salesforce.png" alt="old_man_yells_at_salesforce" width="28"> |
| old_man_yells_at_sentry | <img src="./Emojis/old_man_yells_at_sentry.png" alt="old_man_yells_at_sentry" width="28"> |
| old_man_yells_at_xcode | <img src="./Emojis/old_man_yells_at_xcode.png" alt="old_man_yells_at_xcode" width="28"> |
| petclaude | <img src="./Emojis/petclaude.gif" alt="petclaude" width="28"> |
| photoshop | <img src="./Emojis/photoshop.png" alt="photoshop" width="28"> |
| postman | <img src="./Emojis/postman.png" alt="postman" width="28"> |
| powerbi | <img src="./Emojis/powerbi.png" alt="powerbi" width="28"> |
| pycharm | <img src="./Emojis/pycharm.png" alt="pycharm" width="28"> |
| python | <img src="./Emojis/python.png" alt="python" width="28"> |
| salesforce | <img src="./Emojis/salesforce.png" alt="salesforce" width="28"> |
| salesforce_salespoop | <img src="./Emojis/salesforce_salespoop.png" alt="salesforce_salespoop" width="28"> |
| scrum_sprint | <img src="./Emojis/scrum_sprint.png" alt="scrum_sprint" width="28"> |
| success_kid | <img src="./Emojis/success_kid.png" alt="success_kid" width="28"> |
| swift | <img src="./Emojis/swift.png" alt="swift" width="28"> |
| ternary | <img src="./Emojis/ternary.png" alt="ternary" width="28"> |
| terraform | <img src="./Emojis/terraform.png" alt="terraform" width="28"> |
| thumbs_up_keanu | <img src="./Emojis/thumbs_up_keanu.gif" alt="thumbs_up_keanu" width="28"> |
| travisci | <img src="./Emojis/travisci.png" alt="travisci" width="28"> |
| ubiquiti | <img src="./Emojis/ubiquiti.jpg" alt="ubiquiti" width="28"> |
| unifi_logo | <img src="./Emojis/unifi_logo.png" alt="unifi_logo" width="28"> |
| vscode | <img src="./Emojis/vscode.png" alt="vscode" width="28"> |
| whoa_keanu | <img src="./Emojis/whoa_keanu.gif" alt="whoa_keanu" width="28"> |
| workato | <img src="./Emojis/workato.png" alt="workato" width="28"> |
| xcode | <img src="./Emojis/xcode.png" alt="xcode" width="28"> |
| xcode_explosion | <img src="./Emojis/xcode_explosion.gif" alt="xcode_explosion" width="28"> |
| xcode_project | <img src="./Emojis/xcode_project.png" alt="xcode_project" width="28"> |
| zoom | <img src="./Emojis/zoom.png" alt="zoom" width="28"> |

## Attribution

- Most/all of the above are from [Slackemojis](https://slackmojis.com).
