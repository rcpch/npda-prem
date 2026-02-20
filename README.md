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
- Section blurbs - standalone page or above first question?
  - For example - the impact on education one provides no content the title doesn't already?
  - Go back currently skips over these - is that ok?
- Should we have some kind of progress tracking (section X of X, question X of X)?
  - Would probably require new translations?
- Email in footer?
- Page for when submission is closed
- Are we correctly applying aria disabled?
- Where should we apply aria labels (e.g. aria-label="Form navigation")
- Critical accessibility results (mostly around lack of contrast in RCPCH colours the AI picked) 

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
- Replace uses of "child" in URLs etc with "cyp"


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
