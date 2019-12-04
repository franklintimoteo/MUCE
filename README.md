<p align="center">
  <img src="app/static/images/muce-banner.gif" >
</a></p>
<h5 align="center">Modern Unsolicited Commercial Email</h5>

#### Initialize the database
```shell script
flask init-db
```

#### Create admin login
```shell script
flask init-admin -u username -p password
```

#### Add new spam templates
```
Create templates named with prefix spam_
Example: spam_smartphone5g.html
Put templates on app/templates/ directory.
```

#### Configure Template
Add `{{ url_coupon }}` on html template
```html
Example:
<html>
<head><title>Coupon Paypal</title></head>
<body>
    <a href="{{ url_coupon }}">Redeem coupon</a>
</body>
</html>

```

#### Configure your mail
```shell script
app.__init__.py - update with your mail "SERVER", "PORT", "SENDER", "DDNS"

- Define vars
(Linux)
export MAIL_SENDER=youcompleteemail@domain.com
export DDNS=muce.ddns.net
export MAIL_USERNAME=usernameEmail
export MAIL_PASSWORD=p@sSWorD

(Windows) 
set MAIL_SENDER=youcompleteemail@domain.com
set DDNS=muce.ddns.net
set MAIL_USERNAME=username
set MAIL_PASSWORD=p@sSWorD
```

