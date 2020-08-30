from tests import apiwrappers


def register_customer(testapp, name):
    res = testapp.get("/")
    assert res.status_code == 200
    # Clicks Create Account button
    res = res.clickbutton("Sign Up")
    # Fills out the form
    form = res.forms["registerForm"]
    form["username"] = name
    form["email"] = "{}@bar.com".format(name)
    form["password"] = "secret-{}".format(name)
    form["confirm"] = "secret-{}".format(name)
    # Submits
    ret = form.submit()
    res = ret.follow()
    assert res.status_code == 200
    res.click("Log Out")
    return form["username"].value, form["password"].value


def register_merchant(testapp, username):
    res = testapp.get("/")
    assert res.status_code == 200
    # Clicks Create Account button
    res = res.clickbutton("Create merchant account")
    # Fills out the form
    form = res.forms["registerMerchantForm"]
    form["username"] = username
    form["email"] = "marie@{}.com".format(username)
    form["password"] = "secret-{}".format(username)
    form["confirm"] = "secret-{}".format(username)
    # Submits
    ret = form.submit()
    res = ret.follow()
    assert res.status_code == 200
    member_id = res.html.find(id="member_id").text
    res.click("Log Out")
    return (form["username"].value, form["password"].value), member_id


def test_pure_happy(db, testapp):
    # Register Users
    zak = register_customer(testapp, name="zak")
    sara = register_customer(testapp, name="sara")
    # Register Merchants
    acme, acme_merchant_id = register_merchant(testapp, username="acme")
    sears, sears_merchant_id = register_merchant(testapp, username="sears")
    apiwrappers.login(testapp, zak[0], zak[1])
    apiwrappers.tip(testapp, 2, acme_merchant_id)
    apiwrappers.tip(testapp, 4, sears_merchant_id)
    apiwrappers.logout(testapp)
    apiwrappers.login(testapp, sara[0], sara[1])
    apiwrappers.tip(testapp, 5, acme_merchant_id)
    apiwrappers.logout(testapp)

    assert apiwrappers.get_charges(testapp, zak) == 6
    assert apiwrappers.get_charges(testapp, sara) == 5
    assert apiwrappers.get_payments(testapp, company=acme) == 7
    assert apiwrappers.get_payments(testapp, company=sears) == 4
