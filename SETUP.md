# Profile and RoLAC activity

The profile content comes from `sakki_BUResume-v2.pdf`. This repository includes an unchanged copy at `assets/Shivayogi-Akki-Resume.pdf`, linked directly from the README, so the profile can be published independently. The portfolio repository hosts a separate copy at `https://scakki.github.io/assets/Shivayogi-Akki-Resume.pdf`; replace both copies when updating the resume.

## Local changes and the live profile

Editing this folder updates the local files. The profile at `https://github.com/scakki` changes after the files are committed and pushed to the `main` branch of `scakki/scakki`. Include the README, resume, activity assets, workflow, script, and tests when publishing. The website is a separate repository and is published separately.

## Enable GitHub's organization activity overview

The checked-in `dhanushbiligiri/README.md` contains no custom activity widget. The organization breakdown below a GitHub profile is GitHub's native activity overview, controlled through account settings rather than the README.

1. On [your profile](https://github.com/scakki), open **Contribution settings** above the contribution graph and enable **Activity overview**. GitHub can then show contributions grouped by organization. [GitHub instructions](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/showing-an-overview-of-your-activity-on-your-profile)
2. If you want private work included in the graph, enable **Private contributions** in the same menu. Visitors without repository access see anonymized counts, not repository names or commit details. This does not make private events available to the portfolio card. [Visibility documentation](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/manage-visibility-settings-for-private-contributions-and-achievements)
3. Add `@RoLACLab` to your GitHub **bio** to prioritize the organization in the activity overview when you are a member. A mention in this README is separate from your account bio. [How organization ordering works](https://docs.github.com/en/account-and-profile/concepts/contributions-on-your-profile)
4. To display the lab's organization badge, open [RoLACLab → People](https://github.com/orgs/RoLACLab/people), find your membership, and change its visibility from **Private** to **Public**, if your organization permits it. This controls membership visibility, not contribution credit.
5. Ensure the author email used for your research commits is associated with your GitHub account. Keep `sakki@mtu.edu` associated for existing work and add/verify `sakki@binghamton.edu` before using it for new commits. Commit credit normally requires a standalone repository and its default or `gh-pages` branch. [Contribution criteria](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference)

Suggested account fields at [Edit profile](https://github.com/settings/profile):

- Bio: `Ph.D. candidate at Binghamton University | Reinforcement learning, control & legged robotics | @RoLACLab`
- Company: `Binghamton University`
- Location: `Johnson City, NY`
- Website: `https://scakki.github.io/`

These account settings are not changed by editing or pushing this repository. Your colleague may see more organization detail while signed in than an unauthenticated visitor can see.

## Activity card on the profile and portfolio

`scripts/update_activity.py` fetches `/users/scakki/events/public` and filters for public events authored by `scakki` in repositories owned by `RoLACLab`. It renders `assets/rolac-activity.svg`, which both the README and portfolio display. The website also has a dated local snapshot as a fallback if the remote image cannot load.

The card reports **events**, not commits or total GitHub contributions: one push may contain multiple commits, and the Events API is a limited recent feed. GitHub exposes at most 300 events from the previous 30 days, with possible processing delays. Private activity, older work, and events beyond that limit are absent. An empty card means no matching public events were returned, not that no research was done. [Events API documentation](https://docs.github.com/en/rest/activity/events)

The workflow runs daily at 11:23 UTC, on changes to its script/workflow/tests, or manually through **Actions → Update public RoLAC activity → Run workflow**. It uses the built-in `GITHUB_TOKEN` to read public events and commit the SVG to this repository; no personal access token or organization secret is needed. The script never requests private events. A failed fetch leaves the last successful card intact, and its printed date makes an old snapshot identifiable.

After pushing to `main`, check that the first workflow run succeeds. Repository rules must permit the workflow's `contents: write` permission and bot push to `main`; if branch protection blocks it, review the workflow failure and adapt it to your repository's pull request policy. Scheduled workflows can be disabled after 60 days without repository activity and may need re-enabling in Actions. A private-only organization will continue to show an empty public card even when your native contribution graph is populated.

Local refresh (Python 3.10+, no third-party dependencies):

```bash
python3 -B -m unittest discover -s tests
python3 scripts/update_activity.py
```

The refresh needs network access. `GITHUB_TOKEN` is optional locally and increases the API rate limit; never place a token in the README, SVG, or website.
