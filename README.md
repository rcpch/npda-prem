# npda-prem

## Get started

```
cp envs/.env.template envs/.env
s/up
```

Visit http://localhost:8000/.


## TODO

### UI questions

- If you follow the start link and you already have a session, send you back to the last unanswered question?
  - Yes, to a "continue" page. Translations required.
- Email in footer?
- Page for when submission is closed
- Are we correctly applying aria disabled?
- Where should we apply aria labels (e.g. aria-label="Form navigation")
- Critical accessibility results (mostly around lack of contrast in RCPCH colours the AI picked)
- Export submissions by PZ code as CSV

### Translations

- Find any AI generated translations by comparing .po files to source docs
- Front matter: Modify "completing the survey" as per modified english translation
- Back matter full translation
- "or"
- "I'm not sure" on region selector
- "Start again"
- "Go back"


### Bugs

- Missing front matter in tablet mode (and also missing unit name in the footer)
- CSRF error clicking "start again" from confirmation screen?
- Replace uses of "child" in URLs etc with "cyp"
- Make all questions optional except demographic questions

### Improvements

- Section tracking is more complexity than it's worth
  - Just include the section intro and description as optional fields on a question
  - Doesn't matter if the section is in the URL path 


### Infra

- Domain name?
  - prem.npda.rcpch.ac.uk?
- Usage instructions!
- Cloudflare Turnstile
  - Error handling (atm would be generic suspicious operation page)
  - Move history out of session for cookie size (can just calculate it by replaying forward based on role and submission?)
- GitHub PR check
- Admin error emails to me
- Request logging
- Favicon
- Automatic production monitoring?
  - Probably overkill, can just monitor the submission dashboard
