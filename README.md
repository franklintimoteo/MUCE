<p align="center">
  <img src="app/static/images/muce-banner.gif" >
</a></p>
<h5 align="center">Modern Unsolicited Commercial Email</h5>

#### Add new spam templates
```
Create templates named with prefix spam_
Example: spam_smartphone5g.html
Put templates on app/templates/ directory.
```

#### Configure your mail
```
app.__init__.py - update with your mail server, port

- Define vars
(Linux)
export MAIL_USERNAME=username@gmail.com
export MAIL_PASSWORD=p@sSWorD

(Windows) 
set MAIL_USERNAME=username@gmail.com
set MAIL_PASSWORD=p@sSWorD
```