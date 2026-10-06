from datetime import datetime


def invest_object(obj, amount):
    obj.invested_amount += amount

    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.utcnow()


def invest(
    new_object,
    objects,
):
    changed_objects = [new_object]

    if new_object.invested_amount == new_object.full_amount:
        new_object.fully_invested = True
        new_object.close_date = datetime.utcnow()
        return [new_object]

    for obj in objects:
        new_available = (
            new_object.full_amount - new_object.invested_amount
        )
        obj_available = (
            obj.full_amount - obj.invested_amount
        )

        if new_available <= 0:
            break

        if obj_available <= 0:
            continue

        amount = min(new_available, obj_available)

        invest_object(new_object, amount)
        invest_object(obj, amount)

        changed_objects.append(obj)

        if new_object.invested_amount == new_object.full_amount:
            break

    return changed_objects
