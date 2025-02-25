design json frontend

#quantity_avaialbe = qtt thats in stock right now
"/" ok
user

basic_user_profile

(grid all cheap comp) 6 items
cheap_item
-component_id,name,category,stock,quantity_available,weight,image
(gridd all expesive comp) 6 items
expensive item
-component_id,name,category,stock,quantity_available,weight,image

## filter

## search

/login #ok

/cp-item/?<pagination> ok

/exp-item/?<pagination> ok

/cp-item/<component_id>/
(show only component data)
cheap_item
component_id,name,category,stock,description,quantity_available,weight,max_time,requires_admin_approval,image

/exp-item/<component_id>/
(grid show all items)
expesive_item
component_id,name,category,stock,description,quantity_available,component_status,late_penalty,change_hands_interval,max_time,weight,image

search time span see if any available during that time,
filter (avalable/unavaiable)

/exp-item/spec/<item_id>/?<pagination>
exp_item_data
item_id,user,expensive_item,serial_id,stock,item_status,weight,condition,max_time,late_penalty,requires_admin_approval,change_hands_interval,reserved,image

if force_reserved = True, then wont show in the web

cart has 1 usercart with many user cart item
/cart/<user_id>/ (auth)(id)

usercart
-cart_id,user

usercartItem
-user_cart_item_id,expensive_item_data/cheap_item,quantity_specified,date_specified,date_start,date_end

/session/<user_id>/(auth)(id)

/session/<user_id>/<session_id>/ (auth)(id)

/qr/<session_id>/ (auth)(id)

complete_user profile
/user-profile/<user_id> (auth)(id)

give qr for selected locker
/admin-locker/select/<user_id>/ (auth)(id)(admin)
locker_set
locker

give qr for all open all locker in that lockerset
/admin-locker/all/<user_id> (auth)(id)(admin)
locker_set
