from indicators.models import IndicatorPriority, IndicatorCategory, IndicatorScope, Indicator, IndicatorSegment
from rating.models import RegionScore, RegionScoreType
from regions.models import Region
from indicators.view_models import CategoryVM
from rating.constants import RegionScoreTypeId
from types import SimpleNamespace


def get_region_scores_with_segments(
    region_id: int,
    segments: list[IndicatorSegment] | None = None,
    segment_score_map: dict[tuple[int, int], float] | None = None,
    overall_score_map: dict[int, float] | None = None,
) -> SimpleNamespace:
    """
    Return normalized region score object with segments_score and overall_score.
    """
    resolved_segments = segments
    if resolved_segments is None:
        resolved_segments = list(IndicatorSegment.objects.filter(is_active=True).order_by("order", "id"))

    local_segment_score_map = segment_score_map
    if local_segment_score_map is None:
        segment_ids = [segment.id for segment in resolved_segments]
        score_rows = RegionScore.objects.filter(
            region_id=region_id,
            score_type_id=RegionScoreTypeId.SEGMENT,
            object_id__in=segment_ids,
        ).values_list("region_id", "object_id", "value")
        local_segment_score_map = {
            (row_region_id, object_id): float(value) if value is not None else 0.0
            for row_region_id, object_id, value in score_rows
            if object_id is not None
        }

    segments_score = []
    for segment in resolved_segments:
        value = local_segment_score_map.get((region_id, segment.id))
        segments_score.append(
            {
                "id": segment.id,
                "label": segment.label,
                "system_name": segment.system_name,
                "score": round(value, 2) if value is not None else None,
            }
        )

    if overall_score_map is not None:
        overall_score = overall_score_map.get(region_id)
    else:
        overall_score = RegionScore.objects.filter(
            region_id=region_id,
            score_type_id=RegionScoreTypeId.OVERALL,
            object_id=None,
        ).values_list("value", flat=True).first()
        overall_score = float(overall_score) if overall_score is not None else None

    return SimpleNamespace(
        segments_score=segments_score,
        overall_score=overall_score,
    )


def get_regions_with_segment_scores() -> list[Region]:
    """
    Return regions with calculated segment scores for card rendering.
    """
    regions = list(Region.objects.all().order_by("order", "id"))
    if not regions:
        return regions

    segments = list(IndicatorSegment.objects.filter(is_active=True).order_by("order", "id"))
    if not segments:
        for region in regions:
            region.segment_scores = []
            region.overall_segment_score = None
        return regions

    region_ids = [region.id for region in regions]
    segment_ids = [segment.id for segment in segments]
    score_rows = RegionScore.objects.filter(
        region_id__in=region_ids,
        score_type_id=RegionScoreTypeId.SEGMENT,
        object_id__in=segment_ids,
    ).values_list("region_id", "object_id", "value")

    score_map = {
        (region_id, object_id): float(value) if value is not None else 0.0
        for region_id, object_id, value in score_rows
        if object_id is not None
        }

    overall_score_rows = RegionScore.objects.filter(
        region_id__in=region_ids,
        score_type_id=RegionScoreTypeId.OVERALL,
        object_id=None,
    ).values_list("region_id", "value")
    overall_score_map = {
        row_region_id: float(value) if value is not None else None
        for row_region_id, value in overall_score_rows
    }

    for region in regions:
        region_score = get_region_scores_with_segments(
            region_id=region.id,
            segments=segments,
            segment_score_map=score_map,
            overall_score_map=overall_score_map,
        )
        region.segment_scores = region_score.segments_score
        region.overall_segment_score = region_score.overall_score
    
    return sorted(regions, key=lambda r: (r.overall_segment_score is not None, r.overall_segment_score), reverse=True)

    
def get_priority_indicators_values(region_id) -> list[tuple[IndicatorPriority, float]]:
    priority_entries = list(
        IndicatorPriority.objects.select_related('indicator')
        .filter(indicator__is_active=True)
        .order_by('priority_number', 'id')
    )

    indicator_ids = [entry.indicator_id for entry in priority_entries]
    region_scores = dict(
        RegionScore.objects.filter(
            region_id=region_id,
            score_type_id=RegionScoreTypeId.INDICATOR,
            object_id__in=indicator_ids,
        ).values_list('object_id', 'value')
    )

    result: list[tuple[IndicatorPriority, float]] = []
    for entry in priority_entries:
        value = region_scores.get(entry.indicator_id)
        result.append((entry, float(value) if value is not None else 0.0))

    return result
    
def get_categories_by_segment(segment_id: int) -> list[CategoryVM]:
    categories = IndicatorCategory.objects.filter(is_active=True, segment_id=segment_id).order_by('order', 'id')
    category_vms = []
    for category in categories:
        category_score = RegionScore.objects.filter(
            score_type_id=RegionScoreTypeId.CATEGORY,
            object_id=category.id,
        ).values_list('value', flat=True).first()
        category_vms.append(
            CategoryVM(
                id=category.id,
                name=category.label,
                score=float(category_score) if category_score is not None else None,
            )
        )
    return category_vms