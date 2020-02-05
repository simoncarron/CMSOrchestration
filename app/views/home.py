from flask import Blueprint, render_template,request, flash
from flask_login import current_user, login_required
import app.module.mod_cms as cms
import config as setting

home = Blueprint('home', __name__)

a = cms.Acano(setting.CMS_IP_ADDRESS + ":" + setting.CMS_PORT, setting.CMS_USERNAME, setting.CMS_PASSWORD)


def getSpaces():

    returnUserCoSpacesList = []
    returnUserCoSpaces = {}

    coSpaces = None
    accessMethods = None

    user = a.get_users(parameters={'emailFilter': current_user.data["mail"]})


    if int(user["users"]["@total"]) != 0:

        userCoSpaces = a.get_user_coSpaces(user["users"]["user"][0]["@id"])

        for userCoSpace in userCoSpaces["userCoSpaces"]["userCoSpace"]:

            returnAccessMethodsList = []
            returnAccessMethods = {}

            coSpaces = a.get_coSpace(userCoSpace["coSpaceId"])["coSpace"]
            accessMethods = a.get_coSpace_access_methods(coSpaces["@id"])["accessMethods"]

            if int(accessMethods["@total"]) != 0:

                for accessMethod in accessMethods["accessMethod"]:
                    returnAccessMethods = {'id':accessMethod["@id"],'passcode':accessMethod["passcode"]}
                    returnAccessMethodsList.append(returnAccessMethods)

            print (coSpaces)
            try:
                returnUserCoSpaces = {"id":coSpaces["@id"],"name":coSpaces["name"],"passcode":coSpaces["passcode"],"accessMethodes":returnAccessMethodsList}
            except:
                returnUserCoSpaces = {"id":coSpaces["@id"],"name":coSpaces["name"],"passcode":"","accessMethodes":returnAccessMethodsList}

            returnUserCoSpacesList.append(returnUserCoSpaces)

    print (returnUserCoSpacesList)
    return returnUserCoSpacesList




@home.route('/')
@login_required
def index():

    return render_template('home/index.html')

@home.route('/space')
@login_required
def space():

    return render_template('home/space.html',coSpaces = getSpaces())

@home.route('/space', methods=['POST'])
@login_required
def space_post():

    if request.form['type'] == "guestPIN":
        a.modify_coSpace(request.form['coSpaceID'], payload={'passcode': request.form['passcode']})
    else:
        a.modify_coSpace_access_method(request.form['coSpaceID'],request.form['accessMethodeID'],payload={'passcode': request.form['passcode']})




    flash('You PIN has been changed')

    return render_template('home/space.html',coSpaces = getSpaces())


@home.route('/about')
def about():

    return render_template('home/about.html')
