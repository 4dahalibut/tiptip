def login(testapp, username, password):
    res = testapp.get("/")
    # Fills out login form in navbar
    form = res.forms["loginForm"]
    form["username"] = username
    form["password"] = password
    # Submits
    res = form.submit()
    assert res.status_code == 302


def logout(testapp):
    res = testapp.get("/").click("Log Out").follow()
    assert res.status_code == 200, res.status_code


def tip(testapp, amount, merchant):
    res = testapp.post("/users/tip", {"amount": amount, "merchant_id": merchant})
    assert res.status_code == 202, res.status_code


def get_charges(testapp, user):
    login(testapp, user[0], user[1])
    res = testapp.get("/users/charges")
    assert res.status_code == 200, res.status_code
    logout(testapp)
    return res.json["charge"]


def get_payments(testapp, company):
    login(testapp, company[0], company[1])
    res = testapp.get("/users/earnings")
    assert res.status_code == 200, res.status_code
    logout(testapp)
    return res.json["earnings"]
