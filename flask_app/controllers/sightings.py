from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.sighting import Sighting
from flask_app.models.user import User 


@app.route("/sightings")
def get_all_with_creator():
    if "user_id" not in session:
        flash("Login first!", 'register')
        return redirect("/")
    data= {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    sightings = Sighting.get_all_with_creator()  
    return render_template("view_all.html", all_sightings=sightings, user=user)  

#@app.route("/sightings/<int:sighting_id>/view")
#def get_one(sighting_id):
    #data= {
        #'id': session['user_id']
   # }
   # user = User.get_by_id(data) 
  #  sighting_data = Sighting.get_one(sighting_id) 
  #  return render_template("view_all.html", user=user, sighting=sighting_data)  
@app.route("/sightings/<int:sighting_id>/view")
def get_one(sighting_id):
    sighting_data = Sighting.get_one(sighting_id)
    return render_template("view_one.html", sighting=sighting_data)


@app.route("/sightings/new")
def new_sighting():
    
    return render_template("create.html")

@app.route("/sightings/create", methods=["POST"])
def create_sighting():
    data = {
        'user_id': session['user_id'],
        "location": request.form["location"],
        "happenings": request.form["happenings"],
        "date": request.form["date"],
        "number": request.form["number"],
    }

    if not Sighting.is_valid(data):
        return redirect("/sightings/new") 

    Sighting.create(data) 
    return redirect("/sightings")


@app.route("/sightings/<int:sighting_id>/edit")
def edit_sighting(sighting_id):
    sighting_data = Sighting.get_by_id(sighting_id)
    return render_template("edit.html", sighting=sighting_data)

@app.route("/sightings/<int:sighting_id>/update", methods=["POST"])
def update_sighting(sighting_id):
    data = {
        "id": sighting_id,
        "location": request.form["location"],
        "happenings": request.form["happenings"],
        "date": request.form["date"],
        "number": request.form["number"],
    }
    if not Sighting.is_valid(data):
        return redirect(f"/sightings/{sighting_id}/edit") 
    
    Sighting.update_sighting(data)
    return redirect("/sightings")

@app.route("/sightings/<int:sighting_id>/delete")
def delete_sighting(sighting_id):
    Sighting.delete_sighting(sighting_id)
    return redirect("/sightings")




