# npda-prem

## Get started

```
cp envs/.env.template envs/.env
s/up
```

Visit http://localhost:8000/.

## TODO

- GitHub pr check
- Q4 should say "do you identify as" (check translations?)
- Start again deletes submission??!
- Fix going back to change unit
  - Generate submission ID in session up front and modify it?
  - Also add "selected" to role, atm it doesn't remember what you answered
- Skip Q10 if Q9 is nursery
- Remove header and blurb before section X of X
- Translate section X of X?
- Typeahead lookup for clinic names using familiar list, save resulting PZ code
- Start again buttons on each page
- Change language button on each page (can redirect to homepage with prefilled next link?)
- Remove question numbers since they're not sequential to someone filling out the form
- Consider isolating conditional questions onto separate pages (triggered by first answer)
  - This is gov.uk style
- Front and back matter from document
- Refactor to use template partials #savethetokens
- Oauth login to Django admin against whitelist of RCPCH user names
- namespaced dot string approach to translations
  - bring across from translations spreadsheet to ensure accuracy
- Weird double arrows on back buttons
- Check with IG about cookie messaging
- Admin emails to me
- Request logging
- Favicon
- Remove htmx from unpkg
- Embed font rather than Google Fonts?
- Test autocomplete on iPad
- Feedback to user that an answer hasn't saved
- prodmon?