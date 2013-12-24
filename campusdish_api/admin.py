from flask import render_template, request
from campusdish_api import app
from campusdish_api.auth import requires_auth
from campusdish_api.models import DiningHall, DiningHallSchedule, db
import datetime

@app.route("/admin/schedule", methods=["GET", "POST"])
@requires_auth
def admin_schedule():
    if request.args.get("del", None) != None:
        sched = DiningHallSchedule.query.get(request.args['del'])
        if sched != None:
            db.session.delete(sched)
            db.session.commit()

    if request.method == "POST":
        did = request.form["dining_hall_id"]
        dining_hall = DiningHall.query.get(did)

        sched = DiningHallSchedule()
        sched.dining_hall_id = did
        sched.dining_hall = dining_hall

        # Parse the open/close times
        open_val = request.form['open_time']
        open_val = map(int, open_val.split(":"))
        close_val = request.form['close_time']
        close_val = map(int, close_val.split(":"))
        open_time = datetime.time(open_val[0], open_val[1])
        close_time = datetime.time(close_val[0], close_val[1])

        # Parse the start/end dates
        start_val = request.form['date_start']
        start_val = map(int, start_val.split("-"))
        end_val = request.form['date_end']
        end_val = map(int, end_val.split("-"))
        start_date = datetime.date(start_val[0], start_val[1], start_val[2])
        end_date = datetime.date(end_val[0], end_val[1], end_val[2])

        # Parse the normal
        regular = False
        if request.form.get("regular", None) != None:
            regular = True

        sched.open_time = open_time
        sched.close_time = close_time
        sched.date_begin = start_date
        sched.date_end = end_date
        sched.days_of_week = request.form['days_of_week']
        sched.regular_schedule = regular
        db.session.add(sched)
        db.session.commit()

    dining_halls = DiningHall.query.all()

    return render_template("admin_schedule.html",
        dining_halls = dining_halls,
    )
