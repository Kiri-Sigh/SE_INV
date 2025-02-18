use 'social_django.context_processors.login_redirect', for template settings

steps into creating syste:
parts:
physical locker/qr code
django

django -
database model

serialization
api
OAUTH2 google  
booking system + calendar package

managing Users
super Users
admin
normal student Users

when logout -> need to clear dj session ---- logout(request)

python manage.py makemigrations social_django
python manage.py migrate social_django

user html view
user main page
-pagination of items
-filter
-navbar linking to other endp

- user item page
  -item information
  -link to add to cart
  -link to select date
  user cart page
  -every user items in the cart

user profile page
uer select date page
user see all of the user's progress page

deal with caching ,serializer,views,apis,pages,sending emails

dealing with clanedar feature:
select start and end date for both

this is cheap
select how many items to borrow before go to calendar or no need to select
selecting how many items it will show red if that date is not available
not selecting how many items will show for each date how many is available

this is exp
select

merge date(choose)
-choose
merge date(auto)
-will put items with same recieve date in same locker

also check if when new sessions check if other old to be active session if same date and same item can be put in same locker

fix if cant put all items inside 1 locker - put other item in new locker / pick up with admin
