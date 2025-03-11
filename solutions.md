# Barn Owl Bagels CTF Solutions

## IDOR

- The /idor page makes a request to http://localhost:8000/orderdetails/215. Find the flag by making a request to for order 639.

## Gift Cards
- The /gift-cards page makes a request to http://localhost:8000/api/gift-cards?isManaged=true and returns only a few gift card details. If you change the isManaged parameter to false you will get a lot more data, including the flag.

## Missing Auth

- The /mauth page has a zip for download. The password for opening the zip file can be found in the page source. Once the .zip is extracted, you will see a single file with no interesting data and a .git folder. By looking through the .git history, you will see that another file was previously removed. By checking out the original commit, you can restore the file, which points to an endpoint on the app. The endpoint has no authorization checks, so by viewing this endpoint you will find the flag.

## Path Traversal

- The /path page makes a request to http://localhost:8000/imageContent?file=owlheader2.png. The file parameter can be used to inject a path traversal payload. The application filters out '../' or '..\' from the parameter but it only runs the filter twice. If you include a payload where removing '../' twice still includes a '../' (for example '......///') you can exploit the path traversal bug and find the flag.

## Client-side Access Restrictions

- This challenge does not have a flag. There is a cookie called 'vSecureCookie' which has the b64 encoded value 'cookieFlagBypass=False'. Change this to 'cookieFlagBypass=True' and you have solved the challenge.

