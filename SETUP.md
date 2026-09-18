# Match GitHub’s contribution calendar and Activity overview

The reference screenshot shows GitHub’s built-in profile sections: pinned repositories, the yearly contribution calendar, and Activity overview with an organization filter and contribution-type chart. GitHub renders these below the profile README. They are controlled by your signed-in account, so committing a README cannot enable them.

## Enable the view on your profile

1. Sign in as `scakki` and open [your profile](https://github.com/scakki).
2. Above the contribution calendar, open **Contribution settings** and enable **Activity overview**. This is the setting that adds the overview and organization filtering shown in the screenshot. [GitHub instructions](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/showing-an-overview-of-your-activity-on-your-profile)
3. In the same menu, enable **Private contributions** if you want your private research work included as anonymized counts. Visitors without access will not see private repository names or commit details. [Visibility instructions](https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/manage-visibility-settings-for-private-contributions-and-achievements)
4. At [Edit profile](https://github.com/settings/profile), add `@RoLACLab` to your **bio**. As an organization member, this prioritizes the lab in Activity overview. Merely mentioning the lab in the README does not set this preference. [How GitHub orders organizations](https://docs.github.com/en/account-and-profile/concepts/contributions-on-your-profile)
5. To match the **Pinned** section as well, click **Customize your pins** on your profile, select up to six eligible repositories/gists, and save. Use the organization filter to find lab repositories you can pin. [Pinning instructions](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/pinning-items-to-your-profile)

Suggested bio:

> Ph.D. candidate at Binghamton University | Reinforcement learning, control & legged robotics | @RoLACLab

Activity overview only shows repository details a viewer can access. The `RoLACLab/bolt_rl` name visible in your colleague’s screenshot may depend on the viewer’s access. Enabling private contributions does not publish private repository details. If the lab uses SSO, an active SSO session may be needed to see the organization activity while signed in.

Public organization membership controls the separate organization badge on your profile; it does not replace the Activity overview setting.

## If contributions are missing

Make sure the author email on your research commits is associated with your GitHub account. Keep the old `sakki@mtu.edu` address associated for earlier work, and associate `sakki@binghamton.edu` for commits authored with that address. Commit credit normally requires a standalone repository and its default or `gh-pages` branch. [Contribution criteria](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference)

## What is in these repositories

- `README.md` retains the updated resume content, publications, and RoLAC lab link. It leaves the contribution display to GitHub’s native profile sections.
- `assets/Shivayogi-Akki-Resume.pdf` is an unchanged copy of the supplied resume, linked directly from the README.
- The custom recent-event card, generator, tests, and scheduled workflow have been removed.
- The portfolio embeds a yearly contribution heatmap using [GitHub Chart API](https://github.com/2016rshah/githubchart-api) at `https://ghchart.rshah.org/scakki`, and links to the native organization overview. The website chart covers all repositories visible through the public profile, not only RoLAC. The service is independently hosted and cached; it does not reproduce GitHub’s pinned items, organization filter, or contribution-type chart. No token is needed or embedded. If it is unavailable, the website provides direct GitHub links.

Repository edits must be committed and pushed to update the live README and website. The account settings above must be enabled separately while signed in. No account settings were changed by these file edits.
