from django.db.models import FloatField, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from django.db import models

from indicators.models import Indicator, IndicatorCategory, IndicatorScope
from indicators.view_models import CategoryVM, IndicatorVM, ScopeVM
from rating.constants import RegionScoreTypeId
from rating.models import RegionScore

def get_category_with_scopes(category_id: int, region_id: int) -> CategoryVM | None:
	category_score_subquery = RegionScore.objects.filter(
		region_id=region_id,
		score_type_id=RegionScoreTypeId.CATEGORY,
		object_id=OuterRef('id'),
	).values('value')[:1]

	category = (
		IndicatorCategory.objects.filter(id=category_id, is_active=True)
		.annotate(
			score=Coalesce(
				Subquery(category_score_subquery, output_field=FloatField()),
				Value(0.0),
			)
		)
		.first()
	)

	if category is None:
		return None

	scope_score_subquery = RegionScore.objects.filter(
		region_id=region_id,
		score_type_id=RegionScoreTypeId.SCOPE,
		object_id=OuterRef('id'),
	).values('value')[:1]

	scopes = (
		IndicatorScope.objects.filter(
			is_active=True,
			category_id=category_id,
		)
		.annotate(
			score=Coalesce(
				Subquery(scope_score_subquery, output_field=FloatField()),
				Value(0.0),
			)
		)
		.order_by('order', 'id')
	)

	scope_ids = [scope.id for scope in scopes]
	indicator_score_subquery = RegionScore.objects.filter(
		region_id=region_id,
		score_type_id=RegionScoreTypeId.INDICATOR,
		object_id=OuterRef('id'),
	).values('value')[:1]

	indicators = (
		Indicator.objects.filter(scope_id__in=scope_ids, is_active=True)
		.annotate(
			score=Coalesce(
				Subquery(indicator_score_subquery, output_field=FloatField()),
				Value(0.0),
			)
		)
		.order_by('scope_id', 'order', 'id')
	)

	indicators_by_scope: dict[int, list[IndicatorVM]] = {}
	for indicator in indicators:
		indicators_by_scope.setdefault(indicator.scope_id, []).append(
			IndicatorVM(
				id=indicator.id,
				name=indicator.label,
				order=indicator.order,
				is_active=indicator.is_active,
				measurement_unit=indicator.measurement_unit,
				score=float(indicator.score) if indicator.score is not None else None,
			)
		)

	scope_vms: list[ScopeVM] = []
	for scope in scopes:
		max_score = get_scope_max_score(scope.id)
		min_score = get_scope_min_score(scope.id)
		scope_vms.append(
			ScopeVM(
				id=scope.id,
				name=scope.label,
				order=scope.order,
				is_active=scope.is_active,
				system_name=scope.system_name,
				coefficient=float(scope.coefficient) if scope.coefficient is not None else None,
				score=float(scope.score) if scope.score is not None else None,
				indicators=indicators_by_scope.get(scope.id, []),
				max_score=max_score,
				min_score=min_score,
			)
		)

	return CategoryVM(
		id=category.id,
		name=category.label,
		order=category.order,
		is_active=category.is_active,
		system_name=category.system_name,
		coefficient=float(category.coefficient) if category.coefficient is not None else None,
		score=float(category.score) if category.score is not None else None,
		scopes=scope_vms,
	)

def get_scope_max_score(scope_id: int) -> float:
    return RegionScore.objects.filter(
        score_type_id=RegionScoreTypeId.SCOPE,
        object_id=scope_id
    ).aggregate(
        max_score=Coalesce(
            models.Max('value'),
            Value(0.0, output_field=FloatField()),
            output_field=FloatField(),
        )
    )['max_score']

def get_scope_min_score(scope_id: int) -> float:
    return RegionScore.objects.filter(
        score_type_id=RegionScoreTypeId.SCOPE,
        object_id=scope_id
    ).aggregate(
        min_score=Coalesce(
            models.Min('value'),
            Value(0.0, output_field=FloatField()),
            output_field=FloatField(),
        )
    )['min_score']
    