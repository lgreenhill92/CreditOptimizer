

# class LoginForm(AuthenticationForm):
#     email = forms.EmailField(label='Email')
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)



To run via parent file in integrated terminal: 

python3 manage.py runserver

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py test



python3 manage.py createsuperuser
lance.greenhill@gmail.com
lancegreenhill
Password is LG210057lg I think

Regular user
noah2021
noah2021@gmail.com
BabyJib!1

Regular user
Isaiah2015
Isaiah2015@gmail.com
Babyzay15may
Bigboyzay2015

Regular user
elijah2011
elijah2011@gmail.com
Fortnightsweat1011

Shell commands

Sql look up.
	>sqlite3 /Users/lancegreenhill/Documents/GitHub/demo/db.sqlite3
 NEXT LINE >SELECT * FROM auth_user;



from django.contrib.auth import authenticate
user = authenticate(email='noah2021@gmail.com', password='pbkdf2_sha256$720000$kzUKpFoMHSwyu3d9o64lkH$YWqU/RP8qkQW1rN4XQpCNSLoaQpa6/8PO1nnzRnqJZ0=')
print(user)

def dblocation():
    #address = '/Users/lancegreenhill/Documents/GitHub/CreditOptimizer/CreditOptimizer/credit_optimiser.db'
    address = "/Users/lancegreenhill/Documents/GitHub/CreditOptimizer/Credit-Optimiser/demo/db.sqlite3"
    return address



￼


Fancy login in code.

<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h2 class="text-center">Login</h2>
                </div>
                <div class="card-body">
                    <form method="post" class="form-horizontal">
                        {% csrf_token %}
                        <div class="form-group row">
                            <label for="id_email" class="col-md-4 col-lg-3 col-form-label form-label">Email</label>
                            <div class="col-md-8 col-lg-9">
                                <input type="email" name="email" class="form-control" id="id_email" placeholder="Email">
                            </div>
                        </div>
                        <div class="form-group row">
                            <label for="id_password" class="col-md-4 col-lg-3 col-form-label form-label">Password</label>
                            <div class="col-md-8 col-lg-9">
                                <input type="password" name="password" class="form-control" id="id_password" placeholder="Password">
                            </div>
                        </div>
                        <div class="form-group">
                            <div class="col-sm-offset-1 col-sm-10">
                                <button type="submit" class="btn btn-primary btn-block">Login</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>


