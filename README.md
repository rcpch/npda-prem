# npda-prem

## Get started

```
cp envs/.env.template envs/.env
s/up
```

Visit http://localhost:8000/.


## TODO

### Translations

- Find empty translations msgstr ""
- Find unused translations (agent)
- General
  - "Go back" translation?
  - "Start again" translation?
  - "I'm not sure" is not translated?
- Front matter
  - Modify "completing the survey" as per modified english translation
- Q4
  - Should say "do you identify as"


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


### Bugs

- Allow "Next" without filling in free text fields?
- Replace uses of "child" in URLs etc with "cyp"


### Infra

- Domain name?
  - prem.npda.rcpch.ac.uk?
- Usage instructions!
- Cloudflare Turnstile
- GitHub PR check
- Admin error emails to me
- Request logging
- Favicon
- Automatic production monitoring?
  - Probably overkill, can just monitor the submission dashboard
