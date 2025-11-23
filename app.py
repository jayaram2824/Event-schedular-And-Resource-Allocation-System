from datetime import datetime, timedelta
from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for
from models import Event, EventResourceAllocation, Resource, db
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")
db_path = os.path.join(os.path.dirname(__file__), 'instance')
os.makedirs(db_path, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_path, 'events.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

main_bp = Blueprint("main", __name__)

def parse_datetime(value):
    """Parse datetime from string format YYYY-MM-DDTHH:MM"""
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M")
    except Exception:
        return None


@main_bp.route("/")
def index():
    return redirect(url_for("main.events"))

@main_bp.route("/events", methods=["GET", "POST"])
def events():
    if request.method == "POST":
        event_id = request.form.get("event_id")
        title = request.form.get("title", "").strip()
        start_time_str = request.form.get("start_time", "").strip()
        end_time_str = request.form.get("end_time", "").strip()
        description = request.form.get("description", "").strip()

        start_time = parse_datetime(start_time_str)
        end_time = parse_datetime(end_time_str)

        if event_id:
            event = Event.query.get_or_404(event_id)
            event.title = title
            event.start_time = start_time
            event.end_time = end_time
            event.description = description
        else:
            event = Event(
                title=title,
                start_time=start_time,
                end_time=end_time,
                description=description,
            )
            db.session.add(event)
        db.session.commit()
        if event_id:
            flash("Event updated successfully.", "success")
        else:
            flash("Event created successfully.", "success")
        return redirect(url_for("main.events"))

    edit_id = request.args.get("edit_id", type=int)
    event_to_edit = Event.query.get(edit_id) if edit_id else None
    events = Event.query.order_by(Event.event_id).all()
    return render_template(
        "events.html", events=events, event_to_edit=event_to_edit
    )


@main_bp.route("/events/<int:event_id>/delete", methods=["POST"])
def delete_event(event_id: int):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("main.events"))



@main_bp.route("/resources", methods=["GET", "POST"])
def resources():
    if request.method == "POST":
        resource_id = request.form.get("resource_id")
        name = request.form.get("resource_name", "").strip()
        resource_type = request.form.get("resource_type", "").strip()

        if resource_id:
            resource = Resource.query.get_or_404(resource_id)
            resource.resource_name = name
            resource.resource_type = resource_type

        else:
            resource = Resource(resource_name=name.lower(), resource_type=resource_type.lower())
            db.session.add(resource)
        db.session.commit()

        if resource_id:
            flash("Resource updated successfully.", "success")
        else:
            flash("Resource created successfully.", "success")
        return redirect(url_for("main.resources"))

    edit_id = request.args.get("edit_id", type=int)
    resource_to_edit = Resource.query.get(edit_id) if edit_id else None
    resources = Resource.query.order_by(Resource.resource_name).all()
    return render_template(
        "resources.html",
        resources=resources,
        resource_to_edit=resource_to_edit,
        resource_types=["Room", "Instructor", "Equipment"],
    )
@main_bp.route("/resources/<int:resource_id>/delete", methods=["POST"])
def delete_resource(resource_id: int):
    resource = Resource.query.get_or_404(resource_id)
    db.session.delete(resource)
    db.session.commit()
    return redirect(url_for("main.resources"))

@main_bp.route("/allocations", methods=["GET", "POST"])
def allocations():
    events = Event.query.order_by(Event.title).all()
    resources = Resource.query.order_by(Resource.resource_name).all()

    if request.method == "POST":
        allocation_id = request.form.get("allocation_id")
        event_id = request.form.get("event_id")
        resource_id = request.form.get("resource_id")

        event_id = int(event_id)
        resource_id = int(resource_id)

        event = Event.query.get(event_id)
        conflict = (
            EventResourceAllocation.query
            .join(Event)
            .filter(
                EventResourceAllocation.resource_id == resource_id,
                Event.event_id != event_id,
                event.start_time < Event.end_time,
                event.end_time > Event.start_time
            )
            .first()
        )

        if conflict:
            flash("This resource is already booked for another event during this time.", "danger")
            return redirect(url_for("main.allocations"))

        if allocation_id:
            allocation = EventResourceAllocation.query.get_or_404(allocation_id)
            allocation.event_id = event_id
            allocation.resource_id = resource_id
        else:
            existing = EventResourceAllocation.query.filter_by(
                event_id=event_id, resource_id=resource_id
            ).first()
            if existing:
                flash("This allocation already exists.", "warning")
                return redirect(url_for("main.allocations"))

            allocation = EventResourceAllocation(
                event_id=event_id,
                resource_id=resource_id,
            )
            db.session.add(allocation)

        db.session.commit()
        flash("Allocation saved successfully.", "success")
        return redirect(url_for("main.allocations"))

    edit_id = request.args.get("edit_id", type=int)
    allocation_to_edit = (
        EventResourceAllocation.query.get(edit_id) if edit_id else None
    )
    allocations = (
        EventResourceAllocation.query.join(Event).join(Resource).all()
    )
    return render_template(
        "allocations.html",
        allocations=allocations,
        allocation_to_edit=allocation_to_edit,
        events=events,
        resources=resources,
    )



@main_bp.route("/allocations/<int:allocation_id>/delete", methods=["POST"])
def delete_allocation(allocation_id: int):
    allocation = EventResourceAllocation.query.get_or_404(allocation_id)
    db.session.delete(allocation)
    db.session.commit()
    return redirect(url_for("main.allocations"))



@main_bp.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        start_date_str = request.form.get("start_date", "").strip()
        end_date_str = request.form.get("end_date", "").strip()

        start_date = parse_datetime(start_date_str) if start_date_str else None
        end_date = parse_datetime(end_date_str) if end_date_str else None

        if not start_date or not end_date:
            return redirect(url_for("main.report"))

        if start_date >= end_date:
            return redirect(url_for("main.report"))

        # Get all resources
        resources = Resource.query.order_by(Resource.resource_id).all()
        utilization_data = []
        
        for resource in resources:
            # Get all allocations for this resource
            allocations = EventResourceAllocation.query.filter_by(
                resource_id=resource.resource_id
            ).all()
            
            total_hours = 0.0
            
            for allocation in allocations:
                event = allocation.event
                
                # Check if event overlaps with the date range
                # Overlap condition: event.start_time < end_date AND event.end_time > start_date
                if event.start_time < end_date and event.end_time > start_date:
                    # Calculate overlap: min(event.end_time, end_date) - max(event.start_time, start_date)
                    overlap_start = max(event.start_time, start_date)
                    overlap_end = min(event.end_time, end_date)
                    duration = overlap_end - overlap_start
                    total_hours += duration.total_seconds() / 3600.0
            
            utilization_data.append({
                "resource_id": resource.resource_id,
                "resource_name": resource.resource_name,
                "total_hours_used": round(total_hours, 2)
            })

        # Get upcoming bookings for events after end_date
        upcoming_bookings = []
        allocations_with_events = (
            EventResourceAllocation.query
            .join(Event)
            .join(Resource)
            .filter(Event.start_time > end_date)
            .order_by(Event.start_time)
            .all()
        )

        for allocation in allocations_with_events:
            upcoming_bookings.append({
                "resource": allocation.resource,
                "event": allocation.event,
                "allocation": allocation
            })

        total_hours_sum = round(sum(item["total_hours_used"] for item in utilization_data), 2)

        return render_template(
            "report.html",
            utilization_data=utilization_data,
            upcoming_bookings=upcoming_bookings,
            start_date=start_date,
            end_date=end_date,
            total_hours_sum=round(total_hours_sum, 2)
        )

    return render_template(
        "report.html",
        utilization_data=None,
        upcoming_bookings=None,
        start_date=None,
        end_date=None,
        default_start=None,
        default_end=None
    )

app.register_blueprint(main_bp)


def init_db():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
