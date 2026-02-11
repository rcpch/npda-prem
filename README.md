# npda-prem

## Get started

```
cp .env.template .env
s/up
```

## TODO

- Add Azure password file config and stand up in ACA
- Q4 should say "do you identify as" (check translations?)
- Skip Q10 if Q9 is nursery
- Remove header and blurb before section X of X
- Translate section X of X?
- Typeahead lookup for clinic names using familiar list, save resulting PZ code
- Infer region from clinic name?
- Start again buttons on each page
- Change language button on each page (can redirect to homepage with prefilled next link?)
- Remove question numbers since they're not sequential to someone filling out the form
- Consider isolating conditional questions onto separate pages (triggered by first answer)
  - This is gov.uk style
- Whitenoise to serve static assets