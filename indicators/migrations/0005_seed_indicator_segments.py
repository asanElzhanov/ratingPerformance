from django.db import migrations


SEGMENTS = [
    (1, "Оценка результативности", "result", 1, True, "0.333"),
    (2, "Операционная эффективность", "work", 2, True, "0.333"),
    (3, "Оценка населения", "people", 3, True, "0.333"),
]


def create_segments(apps, schema_editor):
    IndicatorSegment = apps.get_model("indicators", "IndicatorSegment")

    for segment_id, label, system_name, order, is_active, coefficient in SEGMENTS:
        IndicatorSegment.objects.update_or_create(
            id=segment_id,
            defaults={
                "label": label,
                "system_name": system_name,
                "order": order,
                "is_active": is_active,
                "coefficient": coefficient,
            },
        )


def delete_segments(apps, schema_editor):
    IndicatorSegment = apps.get_model("indicators", "IndicatorSegment")
    segment_ids = [segment_id for segment_id, *_ in SEGMENTS]
    IndicatorSegment.objects.filter(id__in=segment_ids).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("indicators", "0004_alter_indicatorsegment_id"),
    ]

    operations = [
        migrations.RunPython(create_segments, delete_segments),
    ]
