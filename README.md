# npda-prem

## Get started

```
cp envs/.env.template envs/.env
s/up
```

Visit http://localhost:8000/.


## TODO

### Before launch

- add columns for response rate by role

### UI questions

- Where should we apply aria labels (e.g. aria-label="Form navigation")
- Critical accessibility results (mostly around lack of contrast in RCPCH colours the AI picked)


### Bugs

- Start again menu doesn't remember language
- Role selector doesn't remember language
- CSRF error clicking "start again" from confirmation screen?
- Replace uses of "child" in URLs etc with "cyp"
- Submission closed page only applies on homepage
  - I think that's probably fine actually? Allow people to keep filling in the survey when we close it

### Improvements

- Section tracking is more complexity than it's worth
  - Just include the section intro and description as optional fields on a question
  - Doesn't matter if the section is in the URL path 


### Infra

- Usage instructions!
- GitHub PR check
- Favicon
- Automatic production monitoring?
  - Probably overkill, can just monitor the submission dashboard
