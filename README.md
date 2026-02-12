# npda-prem

## Get started

```
cp envs/.env.template envs/.env
s/up
```

Visit http://localhost:8000/.

## TODO

- GitHub pr check and deploy pipeline
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
- Front and back matter from document
- Refactor to use template partials #savethetokens
- Oauth login to Django admin against whitelist of RCPCH user names
- namespaced dot string approach to translations
  - bring across from translations spreadsheet to ensure accuracy
- Weird double arrows on back buttons
- Check with IG about cookie messaging
- Admin emails to me
- Request logging
- prodmon?