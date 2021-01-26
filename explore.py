import requests as r

creds = {"username": "johndoe", "password": "secret"}

# login here with credentials (this would be a POST from a login form)
login_res = r.post('http://127.0.0.1:8000/token', data = creds)

login_res.status_code
login_res.text

token = login_res.json()['access_token']

head = {'Authorization': 'Bearer ' + token}

# accessing protected data with the token provided
res = r.get('http://127.0.0.1:8000/users/me/', headers=head)

res.status_code
res.text

# access profile document
res = r.get('http://127.0.0.1:8000/johndoe')

res.status_code
res.text

# define a profile rdf document which stores username, password hash, trusted apps and permissions. Integrate server with this file (one per user) & store in user's pod
    # i.e. this file should be used to check the password hash
    # is there an rdf database to store people's pods?

# then - need to define scopes for the JWT that allows reading/writing and limits the ontologies that can be accessed

# then - implement account/profile creation in a pod (this will just be incorporating #1)

# then - write a litte application that asks for permissions to read/write from/to a pod (or just read)
    # log the permissions granted in the user profile
    # generate a JWT based on these permissions

# then - get server to comply with solid protocol

# then - create this as a pod hosting service "evergreen"
