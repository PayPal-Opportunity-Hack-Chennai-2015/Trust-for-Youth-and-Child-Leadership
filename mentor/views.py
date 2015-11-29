from django.shortcuts import render
from django.http import HttpResponseRedirect
from webapp_nkana.utils.common import mongo_instance


def register_mentor_profile(request):
    if request.method == 'POST':
        db = mongo_instance()
        keys = db.tycl.find_one({'id': 'mentor_profile_reference'})['val']
        for k in keys:
            if k in ('username', ):
                continue
            elif k == "Area_of_Expertise":
                keys[k] = request.POST[k.replace(' ', '_')].lower().split(',')
            keys[k] = request.POST[k.replace(' ', '_')]
        keys['username'] = request.user.username
        db.tycl_mentor_profile.insert(keys)
        return HttpResponseRedirect('/')

    return render(request, 'profile.html')


def mentor_landing(request):
    if request.method == "POST":
        pass

    db = mongo_instance()
    mentor_data = db.tycl_mentor_data.find_one({"username": request.user.username})
    volunteer_data = db.tycl_vol_pfle.find_one({"username": mentor_data['volunteer']}, {'_id': 0, 'username': 0}).items()
    child_data = db.tycl_vol_pfle.find_one({"username": mentor_data['child']}, {'_id': 0, 'username': 0}).items()
    return render(request, 'landing.html', {'historic_feedback': [x.items() for x in mentor_data['feedback']],
                                            'child_data': child_data, 'volunteer_data': volunteer_data})


def mentor_questionnare(request):
    db = mongo_instance()
    if request.method == "POST":
        ref_append = {'type': 'Objective'}
        for entity in db.tycl.find_one({'id': 'q_reference'})['val']:
            if entity in request.POST and request.POST[entity]:
                ref_append[entity] = request.POST[entity]

        ref_desc = {'type': 'descriptive'}
        form_elements = ['Educational performance at the school_d',
                         'Health (physical and Mental well-being)condition of the child_d',
                         'Child relationship with family members_d',
                         'Child relationship with friends_d',
                         'Participation in co-curricular activities_d',
                         'Participation in social/community events_d',
                         'Feeling safe at Home, community and School_d',
                         'Social interaction with peers_d',
                         'Personal hygiene of the child_d',
                         'Date of meeting',
                         'Place of meeting',
                         'Meeting Agenda', 'Outcome of Meeting', 'Key Accomplishment', 'Purpose of Connection',
                         'Key learnings for Mentee', 'Key Challenges faced by volunteer',
                         'Key Challenges faced by mentee', 'Key Challenges faced by mentor']

        # form elements reference
        for element in form_elements:
            if element in request.POST and request.POST[element]:
                ref_desc[element] = request.POST[element]

        db.tycl_questionnare_new.insert(ref_append)
        db.tycl_questionnare_new.insert(ref_desc)
        return HttpResponseRedirect('/')

    return render(request, 'questionnare.html')
