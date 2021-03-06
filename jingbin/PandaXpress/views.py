from django.shortcuts import render,redirect
from django.http import HttpResponse
from PandaXpress import models
from django.db import connection
import re
import pandas as pd
import numpy as np
import datetime

# Create your views here.
def log_in(request):
    if request.method == "POST":
        if "signup" in request.POST:
            return redirect('/PandaXpress/signup/')
        else:
            # get the title from front end
            get_user = request.POST.get("name")
            get_pwd = request.POST.get("pwd")
            if (get_user is not None) & (get_user != ''):
                USER = models.Membership.objects.raw("SELECT * FROM Membership where username=%s", [get_user])
                if USER:
                    if str(USER[0].pwd)==get_pwd:
                        request.session['id'] = USER[0].member_id
                        print(USER[0].member_id)
                        return redirect('/PandaXpress/')
                    else:
                        return render(request, "log_in.html", {"error": "Password is not corrrect"})
                else:
                    return render(request, "log_in.html", {"error": "no such username"})
            elif get_user is None:
                return render(request, "log_in.html",{"error": "None"})
            else:
                return render(request, "log_in.html", {"error": "username cannot be empty"})
    return render(request, "log_in.html")

def sign_up(request):
    if request.method == "POST":
        # get the content from html
        username = request.POST.get("username")
        pwd = request.POST.get("pwd")
        user = models.Membership.objects.raw('SELECT * FROM Membership where username = %s', [username])
        if user:
            return render(request, "sign_up.html",{"error":"Username has been used"})
                # redirect("/PandaXpress/signup")
        else:
            with connection.cursor() as cursor:
                cursor.execute('INSERT into Membership(username,pwd) VALUES (%s, %s)', [username, pwd])
            return redirect("/PandaXpress/signin")
    return render(request, "sign_up.html")

def Home(request):
    if request.session['id'] is None:
        return redirect('/PandaXpress/signin')
    else:
        id = request.session['id']
        # request.GET.get('id')
        user_obj = models.Membership.objects.get(member_id=id)
        return render(request,"Home.html",{'id': request.session['id'],'USER':user_obj})

def User(request):
    if request.method == 'POST':
        if "changepwd" in request.POST:
            # get
            id = request.POST.get('id')
            pwd = request.POST.get('pwd')
            with connection.cursor() as cursor:
                cursor.execute('UPDATE Membership SET pwd = %s WHERE member_id = %s', [pwd, id])
            # refresh
            request.session['id'] = id
            return redirect('/PandaXpress/user')
        elif "addfollow" in request.POST:
            id = request.session['id']
            newfollow = request.POST.get('newfollow')
            try:
                newfollow1 = models.Membership.objects.get(username=newfollow)
            except:
                newfollow1 = None
            if newfollow1 is not None:
                newfollow2 = newfollow1.member_id
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Follow where member_id = %s AND following_id=%s", [id, newfollow2])
                db_test = cursor.fetchall()
                if db_test:
                    return redirect('/PandaXpress/user')
                else:
                    with connection.cursor() as cursor:
                        cursor.execute('INSERT into Follow(member_id,following_id) VALUES (%s, %s)', [id, newfollow2])
                    # refresh
                    request.session['id'] = id
                    return redirect('/PandaXpress/user')
            else:
                HttpResponse("No such user.")
        elif "addinv" in request.POST:
            id = request.session['id']
            # request.GET.get('id')
            # search
            user_obj = models.Membership.objects.get(member_id=id)
            # user_obj_list = models.Membership.objects.all()
            follow_obj = models.Membership.objects.raw(
                'SELECT b.member_id, b.username as username '
                'FROM Membership b right join Follow a on a.following_id = b.member_id where a.member_id = %s', [id])
            # models.Follow.objects.get(member_id=id)
            store_obj = models.Recipes.objects.raw(
                'SELECT b.recipe_id, b.recipe_name as recipe_name '
                'FROM Recipes b right join Store a on a.recipe_id = b.recipe_id where a.member_id = %s', [id])
            # models.Store.objects.get(member_id=id)
            inventory_obj = models.Inventory.objects.raw(
                'SELECT b.inventory_id as inventory_id, b.inventory_name as inventory_name '
                'FROM Inventory b right join Owns a on b.inventory_id = a.inventory_id where a.member_id = %s', [id])
            # follow_obj_list = models.Follow.objects.all()
            if inventory_obj:
                return render(request,'user.html',
                      {'id': request.session['id'],"USER": user_obj,
                       # "user_obj_list": user_obj_list,
                       "follow_obj": follow_obj,
                       "store_obj": store_obj,
                       "inventory_obj": inventory_obj,"error_inv":"You already have one inventory"})
            newinv = request.POST.get('newinv')
            try:
                newinv1 = models.Inventory.objects.get(inventory_id=newinv)
            except:
                newinv1 = None
            if newinv1 is not None:
                newinv2 = newinv1.inventory_id
                with connection.cursor() as cursor:
                    cursor.execute('INSERT into Owns(member_id,inventory_id) VALUES (%s, %s)', [id, newinv2])
                # refresh
                request.session['id'] = id
                return redirect('/PandaXpress/user')
            else:
                HttpResponse("No such inventory.")
        elif "logout" in request.POST:
            return redirect('/PandaXpress/signin')
        else:
            return HttpResponse("Cannot do this operation.")
    else:
        # get id
        id = request.session['id']
            #request.GET.get('id')
        # search
        user_obj = models.Membership.objects.get(member_id=id)
        # user_obj_list = models.Membership.objects.all()
        follow_obj = models.Membership.objects.raw(
            'SELECT b.member_id, b.username as username '
            'FROM Membership b right join Follow a on a.following_id = b.member_id where a.member_id = %s',[id])
            # models.Follow.objects.get(member_id=id)
        store_obj = models.Recipes.objects.raw(
            'SELECT b.recipe_id, b.recipe_name as recipe_name '
            'FROM Recipes b right join Store a on a.recipe_id = b.recipe_id where a.member_id = %s',[id])
            #models.Store.objects.get(member_id=id)
        inventory_obj = models.Inventory.objects.raw(
            'SELECT b.inventory_id as inventory_id, b.inventory_name as inventory_name '
            'FROM Inventory b right join Owns a on b.inventory_id = a.inventory_id where a.member_id = %s',[id])
        # follow_obj_list = models.Follow.objects.all()
        return render(request, 'user.html',
                      {'id': request.session['id'],"USER": user_obj,
                       # "user_obj_list": user_obj_list,
                       "follow_obj": follow_obj,
                       "store_obj": store_obj,
                       "inventory_obj": inventory_obj

        })

def Follow_recipes(request):
    if request.method=="GET":
        id = request.GET.get('id')
        user_obj = models.Membership.objects.get(member_id=id)
        MoreRecipes = models.Recipes.objects.raw(
            'SELECT r.recipe_id as recipe_id, r.recipe_name as recipe_name, r.recipe_description as recipe_description,r.cooking_time as cooking_time '
            'FROM Membership m natural join Follow f join Store s on f.following_id=s.member_id '
            'join (SELECT* FROM Recipes WHERE cooking_time < 100 ) AS r on s.recipe_id = r.recipe_id '
            'WHERE m.member_id = %s order by r.recipe_name', [id])
    return render(request, "Follow_recipes.html", {"info": MoreRecipes,"USER":user_obj})

def delete_follow(request):
    id1 = request.GET.get("id")
    id2 = request.GET.get("followid")
    models.Follow.objects.filter(member_id=id1,following_id=id2).delete()
    request.session['id'] = id1
    return redirect("/PandaXpress/user")

def delete_store(request):
    id1 = request.GET.get("id")
    id2 = request.GET.get("recipeid")
    models.Store.objects.filter(member_id=id1,recipe_id=id2).delete()
    request.session['id'] = id1
    return redirect("/PandaXpress/user")

def delete_inventory(request):
    id1 = request.GET.get("id")
    id2 = request.GET.get("inventoryid")
    models.Owns.objects.filter(member_id=id1,inventory_id=id2).delete()
    # db = models.Recipes.objects.raw('', [id])
    request.session['id'] = id1
    return redirect("/PandaXpress/user")

def RecInd(request):
    id = request.session['id']
    # request.GET.get('id')
    user_obj = models.Membership.objects.get(member_id=id)
    get_ind = request.session['ingredients_own']
    print(get_ind)
    if (get_ind is not None) & (get_ind != ''):
        ind_list = str(get_ind).split(',')
        db = []
        for i in ind_list:
            ind_list1 = "%" + i + "%"
            db2 = models.Ingredients.objects.raw(
                "SELECT ingredient_id FROM Ingredients where ingredient_name LIKE %s",
                [ind_list1])
            if db2:
                for j in db2:
                    db = db + [j.ingredient_id]
            # print(db2)
            # db = db+re.findall("\d+",str(db2))
            # print(db)
        db = tuple(db)
        if (db != ()) & (db is not None):
            db1 = models.Recipes.objects.raw(
                'SELECT Distinct r.recipe_id as recipe_id, r.recipe_name as recipe_name, r.recipe_description as recipe_description,r.cooking_time as cooking_time '
                'FROM Recipes r natural join Recipe_Incl ri WHERE ri.ingredient_id in %s order by r.recipe_name', [db])

            if db1:
                return render(request, "RecInd.html", {"data": db1, "USER": user_obj})
        return render(request, "recipeshow.html", {"error": "No recipes found", "USER": user_obj})
    elif get_ind is None:
        return render(request, "RecInd.html", {"error": "Something Wrong", "USER": user_obj})
    else:
        return render(request, "RecInd.html", {"error": "Your inventory is empty", "USER": user_obj})


def show_inven(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        db = models.Inventory.objects.raw(
            'SELECT ing.ingredient_name FROM Inventory_Incl i LEFT OUTER JOIN Ingredients ing ON i.ingredient_id = ing.ingredient_id '
            'WHERE i.inventory_id = %s;', [id])
    return (render(request, "show.html", {"data": db}))

def update_inven(request):
    if request.method == 'POST':
        inventory_name = request.POST.get("inventory_name")
        inventory_id = request.POST.get("inventory_id")
        with connection.cursor() as cursor:
            cursor.execute('UPDATE inventory SET inventory_name = %s WHERE inventory_id = %s', [inventory_name, inventory_id])
        return redirect("/inven/")
    return render(request, "inven_update.html")

def search(request):
    if request.method == 'GET':
        words = request.GET.get("name")
        temp = request.GET.get("gotem")
        print(temp)
        if temp not in ["inventory", "ingredients", None]:
            return HttpResponse("Yo this is not the right database!")
        if temp == 'ingredients':
            temp2 = 'ingredient_name'
        else:
            temp2 = 'inventory_name'
        if words:
            words = "%"+words+"%"
            with connection.cursor() as cursor:
                if temp2 == "inventory_name":
                    cursor.execute('SELECT * FROM inventory WHERE inventory_name LIKE %s', [words])
                else:
                    cursor.execute('SELECT * FROM ingredients WHERE ingredient_name LIKE %s', [words])
            return render(request, "search_results.html", {"data": cursor})
    return render(request, "search_inven.html")

def CreateInven(request):
    try:
        id = request.session['id']
        # request.GET.get('id')
        user_obj = models.Membership.objects.get(member_id=id)
    except:
        return redirect('/PandaXpress/signin')
    inv = models.Membership.objects.raw(
        "SELECT * FROM Membership m RIGHT OUTER join Owns o on m.member_id=o.member_id WHERE o.member_id = %s", [id])
    if inv:
        return redirect("/PandaXpress/invenown/show/")
    if request.method == 'POST':
        inventory_name = request.POST.get("inventory_name")
        db = models.Inventory.objects.raw(
            "SELECT * FROM Inventory WHERE inventory_name = %s",
            [inventory_name])
        if db:
            return render(request,"create_inven.html",{"error":"The name has been used, you can go to your profile to add inventory others share with you"})
        else:
            with connection.cursor() as cursor:
                cursor.execute('INSERT into Inventory(inventory_name) VALUES (%s)', [inventory_name])
            inv_id = models.Inventory.objects.raw("SELECT inventory_id FROM Inventory WHERE inventory_name = %s",[inventory_name])
            print(inv_id[0])
            inv_id = int(re.findall("\d+", str(inv_id[0]))[0])
            with connection.cursor() as cursor:
                cursor.execute('INSERT into Owns(member_id, inventory_id) VALUES (%s,%s)',[id,inv_id])
            return redirect("/PandaXpress/invenown/show")
    else:
        return render(request, "create_inven.html",{"error":"You have no inventory now, try to create one or add existing one in your profile","USER":user_obj})

def DeleteInven(request):
    id = request.GET.get("id")
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM pandaxpress.inventory WHERE inventory_id = %s', [id])
    return redirect('/inven/')

def OwnInventory(request):
    try:
        id = request.session['id']
        # request.GET.get('id')
        user_obj = models.Membership.objects.get(member_id=id)
    except:
        return redirect('/PandaXpress/signin')
    ingredient_string = ""
    inv = models.Membership.objects.raw("SELECT * FROM Membership m RIGHT OUTER join Owns o on m.member_id=o.member_id WHERE o.member_id = %s",[id])
    if inv:
        db = models.InventoryIncl.objects.raw(
            "SELECT *"
            " FROM Inventory_Incl inv LEFT OUTER JOIN Ingredients ing ON ing.ingredient_id = inv.ingredient_id "
            "WHERE inv.inventory_id IN "
            "(SELECT o.inventory_id FROM Membership m LEFT OUTER JOIN Owns o ON o.member_id = m.member_id "
            "WHERE m.member_id = %s)"
            , [id])
        if db:
            ingredient_string = ""
            for k in range(len(db)):
                ingredient_string = ingredient_string +","+str(db[k].ingredient_name)
                # print(str(db[k].ingredient_name))
            # print(ingredient_string)
            ingredient_string = re.sub(r' ', ',', ingredient_string)
            request.session['ingredients_own'] = re.sub(r'^,', '', ingredient_string)
            print(request.session['ingredients_own'])
            return (render(request, "invenown.html", {"data": db, 'id': request.session['id'], 'USER': user_obj}))
        else:
            request.session['ingredients_own'] = re.sub(r' ', ',', ingredient_string)
            print(request.session['ingredients_own'])
            return render(request,"invenown.html",{"error": "Empty",'USER':user_obj})
    else:
        return redirect('/PandaXpress/inven/create/')

def CreateOwnInven(request):
    try:
        id = request.session['id']
        # request.GET.get('id')
        user_obj = models.Membership.objects.get(member_id=id)
    except:
        return redirect('/PandaXpress/signin')
    if request.method == 'POST':
        inventory_id = models.Inventory.objects.raw("SELECT inventory_id FROM Owns WHERE member_id = %s", [id])
        inventory_id = int(re.findall("\d+", str(inventory_id[0]))[0])
        ingredient_name = request.POST.get("ingre_name")
        amnt = request.POST.get("amnt")
        unit = request.POST.get("unit")
        expiry = request.POST.get("expiry")
        get_today = datetime.date.today()
        today = get_today.strftime("%Y-%m-%d")
        if inventory_id == '':
            return redirect("/PandaXpress/invenown/show")
        identifier = inventory_id
        #Check if ingredient exists in our database, if not then insert it and query it back out.
        checker = models.Ingredients.objects.raw("SELECT * FROM Ingredients WHERE ingredient_name = %s",[ingredient_name])
        if checker:
            ingr_id = models.Ingredients.objects.raw("SELECT ingredient_id FROM Ingredients WHERE ingredient_name = %s",[ingredient_name])
            #add ingredient to our inventory_incl
            ingr_id= int(re.findall("\d+", str(ingr_id[0]))[0])
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO Inventory_Incl(inventory_id, ingredient_id, ingredient_amount, ingredient_unit, ingredient_added_date, ingredient_expiry_date) '
                                'VALUES(%s, %s, %s, %s, %s, %s)', [identifier, ingr_id, amnt, unit, today, expiry])
                cursor.execute("DELETE FROM Inventory_Incl WHERE ingredient_expiry_date = '1800-01-01'")
            return redirect("/PandaXpress/invenown/show")
        else:
            print("Ingredient doesn't exist, adding to our database.")
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Ingredients(ingredient_name) VALUES (%s)",
                                                  [ingredient_name])
            ingr_id = models.Ingredients.objects.raw("SELECT ingredient_id FROM Ingredients WHERE ingredient_name = %s",
                                                     [ingredient_name])
            # add ingredient to our inventory_incl
            ingr_id = int(re.findall("\d+", str(ingr_id[0]))[0])
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO Inventory_Incl(inventory_id, ingredient_id, ingredient_amount, ingredient_unit, ingredient_added_date, ingredient_expiry_date) '
                    'VALUES(%s, %s, %s, %s, %s, %s)', [identifier, ingr_id, amnt, unit, today, expiry])
                cursor.execute("DELETE FROM Inventory_Incl WHERE ingredient_expiry_date = '1800-01-01'")
            return redirect("/PandaXpress/invenown/show")
    else:
        return render(request, "createingr.html",{"USER":user_obj})

def UpdateOwnInven(request):
    try:
        id = request.session['id']
        # request.GET.get('id')
        user_obj = models.Membership.objects.get(member_id=id)
    except:
        return redirect('/PandaXpress/signin')
    if request.method == 'POST':
        inv_include_id = request.GET.get("id")
        ingredient_amnt = request.POST.get("ingr_amnt")
        unit = request.POST.get("unit")
        expiry = request.POST.get("expiry")
        with connection.cursor() as cursor:
            cursor.execute(
                'UPDATE Inventory_Incl SET ingredient_amount = %s, ingredient_unit = %s, ingredient_expiry_date = %s WHERE inventory_incl_id = %s ',
                [ingredient_amnt, unit, expiry, inv_include_id])
        return redirect("/PandaXpress/invenown/show/")
    else:
        return render(request, "invupdate.html",{"USER":user_obj})

def DeleteOwnInven(request):
    id = request.GET.get("id")
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM Inventory_Incl WHERE inventory_incl_id = %s', [id])
    return redirect('/PandaXpress/invenown/show/')

# Zheng's code
def ShowRecipe(request):
    try:
        id = request.session['id']
        # request.GET.get('id')
        user_obj = models.Membership.objects.get(member_id=id)
    except:
        return redirect('/PandaXpress/signin')
    if request.method == 'GET':
        get_name = request.GET.get("reci_name")
        get_ind = request.GET.get("ind")
        if get_name:
            get_name = "%" + get_name + "%"
            #db = Recipes.objects.filter(recipe_name__icontains= get_name)
            db = models.Recipes.objects.raw("SELECT * FROM Recipes where recipe_name LIKE %s", [get_name])
            if db:
                return render(request, "recipeshow.html", {"data": db,'USER':user_obj})
            else:
                return render(request, "recipeshow.html", {"error": "No Such a Recipe",'USER':user_obj})
        elif (get_ind is not None)&(get_ind !=''):
            ind_list = str(get_ind).split(',')
            db = []
            for i in ind_list:
                ind_list1 = "%" + i+ "%"
                db2 = models.Ingredients.objects.raw(
                        "SELECT ingredient_id FROM Ingredients where ingredient_name LIKE %s",
                        [ind_list1])
                if db2:
                    for j in db2:
                        db = db+[j.ingredient_id]
                # print(db2)
                # db = db+re.findall("\d+",str(db2))
                # print(db)
            db = tuple(db)
            print(db)
            if (db!=()) & (db is not None) :
                db1 = models.Recipes.objects.raw(
                'SELECT Distinct r.recipe_id as recipe_id, r.recipe_name as recipe_name, r.recipe_description as recipe_description,r.cooking_time as cooking_time '
                'FROM Recipes r natural join Recipe_Incl ri WHERE ri.ingredient_id in %s order by r.recipe_name', [db])

                if db1:
                    return render(request, "recipeshow.html", {"data": db1, "USER": user_obj})
            return render(request, "recipeshow.html", {"error": "No recipes, please try others","USER":user_obj})
        elif (get_ind is None) & (get_name is None):
            db = models.Recipes.objects.raw('SELECT * FROM Recipes ORDER BY recipe_id DESC LIMIT 10 ')
            return render(request, "recipeshow.html", {"data": db, 'id': request.session['id'], 'USER': user_obj})
        else:
            return render(request, "recipeshow.html", {"error": "Input could not be empty","USER":user_obj})
    else:
        return HttpResponse("Cannot do this operation.")

def OwnRecipe(request):
    try:
        id = request.session['id']
        # request.GET.get('id')
        user_obj = models.Membership.objects.get(member_id=id)
    except:
        return redirect('/PandaXpress/signin')
    db = models.Recipes.objects.raw('SELECT * FROM Recipes WHERE recipe_creator = %s',[id])
    return (render(request, "recipeown.html", {"data": db, 'id': request.session['id'], 'USER': user_obj}))

def DetailRecipe(request):
    try:
        id = request.session['id']
        # request.GET.get('id')
        user_obj = models.Membership.objects.get(member_id=id)
    except:
        return redirect('/PandaXpress/signin')
    if request.method == 'GET':
        recipe_id = request.GET.get("id")
        cursor = connection.cursor()
        cursor.execute('SELECT r.recipe_name AS recipe_name, r.recipe_description, r.cooking_time,'
                    '  GROUP_CONCAT(i.ingredient_name) AS ingredient_name, r.recipe_steps FROM Recipes r '
                    'NATURAL JOIN Recipe_Incl l JOIN Ingredients i ON l.ingredient_id = i.ingredient_id '
                    'WHERE recipe_id = %s',[recipe_id])
        db = cursor.fetchall()
        # print(db)
        db1 = models.Nutrients.objects.raw("SELECT n.nutrient_id,n.nutrient_name,h.nutrient_amnt FROM Nutrients n natural join Has h where h.recipe_id = %s ", [recipe_id])
        return (render(request, "recipedetail.html",
                       {"data": db, 'nutrient': db1, 'id': request.session['id'], 'USER': user_obj}))
    if request.method == 'POST':
        recipe_id = request.GET.get("id")
        if "AddLike" in request.POST:
            cursor = connection.cursor()
            cursor.execute('SELECT r.recipe_name AS recipe_name, r.recipe_description, r.cooking_time,'
                           '  GROUP_CONCAT(i.ingredient_name) AS ingredient_name, r.recipe_steps FROM Recipes r '
                           'NATURAL JOIN Recipe_Incl l JOIN Ingredients i ON l.ingredient_id = i.ingredient_id '
                           'WHERE recipe_id = %s', [recipe_id])
            db = cursor.fetchall()
            # print(db)
            db1 = models.Nutrients.objects.raw(
                "SELECT n.nutrient_id,n.nutrient_name,h.nutrient_amnt FROM Nutrients n natural join Has h where h.recipe_id = %s ",
                [recipe_id])
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Store where recipe_id = %s AND member_id=%s",[recipe_id,id])
            db_test =cursor.fetchall()
            if db_test:
                return (render(request, "recipedetail.html",
                               {"data": db, 'nutrient': db1, 'id': request.session['id'],'error':'Liked','USER': user_obj}))
            else:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT into Store(member_id,recipe_id,recipe_member_rel) VALUES (%s, %s,'Like')", [id, recipe_id])
                return render(request, "recipedetail.html",
                               {"data": db, 'nutrient': db1, 'id': request.session['id'],'USER': user_obj, 'error': "Liked"})

def CreateRecipe(request):
    try:
        id = request.session['id']
        # request.GET.get('id')
        user_obj = models.Membership.objects.get(member_id=id)
    except:
        return redirect('/PandaXpress/signin')
    if request.method == 'POST':
        recipe_name = request.POST.get("recipe_name")
        recipe_description = request.POST.get("recipe_description")
        recipe_genre = request.POST.get("recipe_genre")
        recipe_steps = request.POST.get("recipe_steps")
        cooking_time = request.POST.get("cooking_time")
        calories = request.POST.get("calories")
        fat = request.POST.get("fat")
        sugar = request.POST.get("fat")
        sodium = request.POST.get("fat")
        protein = request.POST.get("protein")
        sa_fat = request.POST.get("sa_fat")
        carbohydrates = request.POST.get("carbohydrates")
        check_recipe = models.Recipes.objects.raw("SELECT * FROM Recipes WHERE recipe_name = %s",
                                                     [recipe_name])
        if check_recipe:
            return render(request, "recipecreate.html",{"USER":user_obj,"error":"This recipe name already exists"})
        else:
            with connection.cursor() as cursor:
                cursor.execute('INSERT into Recipes(recipe_creator,recipe_name,recipe_description,recipe_genre,recipe_steps,cooking_time) VALUES (%s, %s, %s,%s,%s,%s)', [id, recipe_name, recipe_description,recipe_genre,recipe_steps,cooking_time])
            recipe_id = models.Recipes.objects.raw(
                "SELECT recipe_id FROM Recipes WHERE recipe_name = %s", [recipe_name])
            recipe_id = int(re.findall("\d+", str(recipe_id[0]))[0])
            with connection.cursor() as cursor:
                cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,1,%s)',[recipe_id,calories])
                cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,2,%s)',
                              [recipe_id, fat])
                cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,3,%s)',
                              [recipe_id, sugar])
                cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,4,%s)',
                              [recipe_id, sodium])
                cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,5,%s)',
                              [recipe_id, protein])
                cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,6,%s)',
                              [recipe_id, sa_fat])
                cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,7,%s)',
                              [recipe_id, carbohydrates])
            # add ingredient to our Recipe_Incl
            inds = request.POST.get("inds")
            ind_list = str(inds).split(',')
            for i in ind_list:
                checker = models.Ingredients.objects.raw("SELECT * FROM Ingredients WHERE ingredient_name = %s",
                                                         [i])
                if checker:
                    ingr_id = models.Ingredients.objects.raw(
                        "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = %s", [i])
                    # add ingredient to our inventory_incl
                    ingr_id = int(re.findall("\d+", str(ingr_id[0]))[0])
                    with connection.cursor() as cursor:
                        cursor.execute(
                            'INSERT INTO Recipe_Incl(recipe_id, ingredient_id) '
                            'VALUES(%s, %s)', [recipe_id, ingr_id])
                else:
                    print("Ingredient doesn't exist, adding to our database.")
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO Ingredients(ingredient_name) VALUES (%s)",
                                       [i])
                    ingr_id = models.Ingredients.objects.raw(
                        "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = %s",
                        [i])
                    # add ingredient to our inventory_incl
                    ingr_id = int(re.findall("\d+", str(ingr_id[0]))[0])
                    with connection.cursor() as cursor:
                        cursor.execute(
                            'INSERT INTO Recipe_Incl(recipe_id, ingredient_id) '
                            'VALUES(%s, %s)', [recipe_id, ingr_id])
            return redirect("/PandaXpress/recipe")
    else:
        return render(request, "recipecreate.html", {"USER": user_obj})


def DeleteRecipe(request):
    # id = request.GET['id']
    # id = User.objects.get(id=id)
    id = request.GET.get("id")
    models.Recipes.objects.filter(recipe_id=id).delete()
    models.RecipeIncl.objects.filter(recipe_id=id).delete()
    models.Has.objects.filter(recipe_id=id).delete()
    return redirect("/PandaXpress/recipe/")

def UpdateRecipe(request):
    try:
        id = request.session['id']
        # request.GET.get('id')
        user_obj = models.Membership.objects.get(member_id=id)
    except:
        return redirect('/PandaXpress/signin')
    recipe_id = request.GET.get("id")
    with connection.cursor() as cursor:
        cursor.execute("SELECT r.recipe_name AS recipe_name, r.recipe_description, r.cooking_time, GROUP_CONCAT(i.ingredient_name) AS ingredient_name,r.recipe_genre, r.recipe_steps FROM Recipes r NATURAL JOIN Recipe_Incl l JOIN Ingredients i ON l.ingredient_id = i.ingredient_id WHERE recipe_id = %s", [recipe_id])
        db_recipe = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute("SELECT r.recipe_id, h.nutrient_id, h.nutrient_amnt FROM Recipes r natural join Has h WHERE r.recipe_id = %s ORDER BY h.nutrient_id",[recipe_id])
        db_nutrients = cursor.fetchall()
    print(db_recipe)
    r_name = db_recipe[0][0]
    r_description = db_recipe[0][1]
    r_genre = db_recipe[0][4]
    r_steps = db_recipe[0][5]
    r_cooking_time = db_recipe[0][2]
    r_ingredients = db_recipe[0][3]
    print(db_nutrients[0])
    r_calories = db_nutrients[0][2]
    print(r_calories)
    r_fat = db_nutrients[1][2]
    r_sugar = db_nutrients[2][2]
    print(r_sugar)
    r_sodium = db_nutrients[3][2]
    r_protein = db_nutrients[4][2]
    r_sa_fat = db_nutrients[5][2]
    r_carbohydrates = db_nutrients[6][2]
    request.session['own_recipe'] = recipe_id
    if request.method == 'POST':
        recipe_id = request.session['own_recipe']
        recipe_name = request.POST.get("recipe_name")
        recipe_description = request.POST.get("recipe_description")
        recipe_genre = request.POST.get("recipe_genre")
        recipe_steps = request.POST.get("recipe_steps")
        cooking_time = request.POST.get("cooking_time")
        recipe_ingredients = request.POST.get("recipe_ingredients")
        check_recipe = models.Recipes.objects.raw("SELECT * FROM Recipes WHERE recipe_name = %s AND recipe_id <> %s",
                                                      [recipe_name,recipe_id])
        calories = request.POST.get('calories')
        fat = request.POST.get('fat')
        sodium = request.POST.get('sodium')
        sugar = request.POST.get('sugar')
        sa_fat = request.POST.get('sa_fat')
        protein = request.POST.get('protein')
        carbohydrates = request.POST.get('carbohydrates')

        if check_recipe:
            return render(request, "recipeupdate.html", {"USER": user_obj, "error": "This recipe name already exists"})
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    'UPDATE Recipes SET recipe_name = %s, recipe_description = %s, recipe_genre=%s, recipe_steps=%s, cooking_time = %s WHERE recipe_id = %s ', [recipe_name, recipe_description,recipe_genre,recipe_steps, cooking_time,recipe_id])
                cursor.execute(
                    'DELETE FROM Recipe_Incl WHERE recipe_id = %s',[recipe_id])
                cursor.execute(
                    'DELETE FROM Has WHERE recipe_id = %s',[recipe_id])
                with connection.cursor() as cursor:
                    cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,1,%s)',[recipe_id, calories])
                    cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,2,%s)',[recipe_id, fat])
                    cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,3,%s)',[recipe_id, sugar])
                    cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,4,%s)',[recipe_id, sodium])
                    cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,5,%s)',[recipe_id, protein])
                    cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,6,%s)',[recipe_id, sa_fat])
                    cursor.execute('INSERT into Has(recipe_id,nutrient_id,nutrient_amnt) Values(%s,7,%s)',[recipe_id, carbohydrates])
            ind_list = str(recipe_ingredients).split(',')
            for i in ind_list:
                checker = models.Ingredients.objects.raw("SELECT * FROM Ingredients WHERE ingredient_name = %s",
                                                         [i])
                if checker:
                    ingr_id = models.Ingredients.objects.raw(
                        "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = %s", [i])
                    # add ingredient to our inventory_incl
                    ingr_id = int(re.findall("\d+", str(ingr_id[0]))[0])
                    with connection.cursor() as cursor:
                        cursor.execute(
                            'INSERT INTO Recipe_Incl(recipe_id, ingredient_id) '
                            'VALUES(%s, %s)', [recipe_id, ingr_id])
                else:
                    print("Ingredient doesn't exist, adding to our database.")
                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO Ingredients(ingredient_name) VALUES (%s)",
                                       [i])
                    ingr_id = models.Ingredients.objects.raw(
                        "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = %s",
                        [i])
                    # add ingredient to our inventory_incl
                    ingr_id = int(re.findall("\d+", str(ingr_id[0]))[0])
                    with connection.cursor() as cursor:
                        cursor.execute(
                            'INSERT INTO Recipe_Incl(recipe_id, ingredient_id) '
                            'VALUES(%s, %s)', [recipe_id, ingr_id])
            return redirect("/PandaXpress/recipe/")
    else:
        return render(request, "recipeupdate.html",{"USER":user_obj,
                                                    "recipe_id":recipe_id,
                                                    "r_name":r_name,
                                                    "r_description":r_description,
                                                    "r_genre":r_genre ,
                                                    "r_steps":r_steps,
                                                    "r_cooking_time":r_cooking_time,
                                                    "r_ingredients":r_ingredients,
                                                    "r_calories": r_calories,
                                                    "r_fat": r_fat,
                                                    "r_sugar": r_sugar,
                                                    "r_sodium": r_sodium,
                                                    "r_protein": r_protein,
                                                    "r_sa_fat": r_sa_fat,
                                                    "r_carbohydrates": r_carbohydrates
                                                    })


def SearchRecipe(request):
    if request.method == 'GET':
        get_name = request.GET.get("name")
        if get_name:
            get_name = "%" + get_name + "%"
            #db = Recipes.objects.filter(recipe_name__icontains= get_name)
            db = models.Recipes.objects.raw("SELECT * FROM Recipes where recipe_name LIKE %s LIMIT 10", [get_name])
            if db:
                return render(request, "recipesearch.html", {"data": db})
            else:
                return render(request, "recipesearch.html", {"error": "No Such a Recipe"})
        else:
            return render(request, "recipesearch.html", {"error1": "Input could not be empty"})
    else:
        return (HttpResponse("Error"))

def AdvancedSearch(request):
    sql = "SELECT m.username AS username, COUNT(*) AS count, GROUP_CONCAT(r.recipe_name SEPARATOR \', \') AS list_name, " \
          "CEIL(AVG(r.cooking_time))AS cooking_average_time FROM Recipes r JOIN Membership m ON r.recipe_creator = m.member_id " \
          "WHERE  r.cooking_time < 30 GROUP BY r.recipe_creator " \
          "HAVING COUNT(*) > 5 ORDER BY COUNT(*) DESC, m.username ASC LIMIT 15"
    cursor = connection.cursor()
    cursor.execute(sql)
    db = cursor.fetchall()
    print("db",db)
    if db is not None:
        return render(request, "recipeadvance.html", {"data": db})
    else:
        render(request, "recipeadvance.html", {"error": "Wrong"})

# End of Zheng's Code

def storeprocedure(request):
    try:
        id = request.session['id']
        # request.GET.get('id')
        user_obj = models.Membership.objects.get(member_id=id)
    except:
        return redirect('/PandaXpress/signin')
    with connection.cursor() as cursor:
        cursor.callproc('FullCoverRecipe', [id])
        data = cursor.fetchall()
    recipes_name = []
    recipes_id = []
    for k in range(len(data)):
        recipes_name = recipes_name + [data[k][1]]
        recipes_id = recipes_id +[data[k][0]]
    recipes_id2 = list(set(recipes_id))
    recipes_id2.sort(key=recipes_id.index)
    recipes_name2 = list(set(recipes_name))
    recipes_name2.sort(key=recipes_name.index)
    recipes=[]
    for k in range(len(recipes_id2)):
        recipes = recipes+[[recipes_id2[k],recipes_name2[k]]]
    recipe_data = pd.DataFrame(recipes, columns=['recipe_id', 'recipe_name'])
    recipe_data['recipe_ingredients'] = [''] * len(recipes_id2)
    for k in range(len(data)):
        j = np.where(np.array(recipes_id2) == data[k][0])[0][0]
        recipe_data.iloc[j, 2] = recipe_data.iloc[j, 2] + ',' + str(data[k][3])
    recipe_data['recipe_ingredients'] = recipe_data.recipe_ingredients.apply(lambda x: re.sub('^,', '', x))
    recipe_data = recipe_data.values.tolist()
    print(recipe_data)
    return render(request, "FullCoverRecipe.html", {"data":recipe_data, "USER":user_obj})

