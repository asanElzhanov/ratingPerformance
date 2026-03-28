from django.db import migrations


SCORE_TYPES = [
    (1, "Segment"),
    (2, "Category"),
    (3, "Scope"),
    (4, "Indicator"),
    (5, "Overall"),
]


def seed_region_score_types(apps, schema_editor):
    RegionScoreType = apps.get_model("rating", "RegionScoreType")

    for score_type_id, label in SCORE_TYPES:
        RegionScoreType.objects.update_or_create(
            id=score_type_id,
            defaults={"label": label},
        )


def unseed_region_score_types(apps, schema_editor):
    RegionScoreType = apps.get_model("rating", "RegionScoreType")
    score_type_ids = [score_type_id for score_type_id, _ in SCORE_TYPES]
    RegionScoreType.objects.filter(id__in=score_type_ids).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("rating", "0005_alter_regionscoretype_options_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_region_score_types, unseed_region_score_types),
    ]
